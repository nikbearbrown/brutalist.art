#!/usr/bin/env python3
"""
final_frame_check.py — GATE V: frame-level visual QC on the FINAL compiled reel.

The Manim gates (A/W/B) only inspect Manim scenes before they're slotted. The
Remotion beats, composer scenes, and slates go through NO frame-level check, and
the mp4 probe (duration/frame count) is a FILE check that never counts as QC.
This gate closes that hole: it samples the final mp4 and audits EVERY beat's
pixels against the title-safe area.

Checks (16:9 canvas 1920x1080, SAFE inset x96-1824 y54-1026 — from layout.ts):
  EDGE-BLEED  (BLOCKER) — content ink in the outer title-safe margin
                          (clipping / overflow — the B20 left clip, B00 right
                          overflow, B31 bottom caption bleed).
  CANVAS-FILL (MAJOR)   — content bounding box covers < FILL_MIN of SAFE, or
                          clusters in one region leaving a large empty band
                          (the negative-space defect — B16, B20).
  LOW-CONTRAST(MAJOR)   — ink-vs-background luminance separation too low to read.

Exit: 2 if any BLOCKER or MAJOR (default — gates block, per the hardening spec);
      1 if only MINOR; 0 if clean. --lenient downgrades MAJOR to a warning.

Writes <reel>/_qc/REPORT.md and a contact sheet <reel>/_qc/contact_sheet.png
that the build agent Reads as the human-eye backstop.

Usage:
  final_frame_check.py <reel_dir> [--mp4 path] [--fill-min 0.55] [--lenient] [--quiet]
  final_frame_check.py --frames-dir <dir>   # test mode: analyze PNGs directly
"""
import argparse, glob, json, os, subprocess, sys, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from build_safety import (BuildError, is_source_report, positive_duration,
                          validate_project, writable_path, atomic_text)
try:
    from PIL import Image
    import numpy as np
except ImportError:
    sys.stderr.write("final_frame_check needs Pillow + numpy (pip install pillow numpy)\n")
    sys.exit(3)

# --- canvas + safe area (mirrors runtime/remotion/src/tokens/layout.ts) --------
CANVAS = (1920, 1080)
SAFE   = {"x": 96, "y": 54, "r": 1824, "b": 1026, "w": 1728, "h": 972}
SAFE916 = {"x": 54, "y": 96, "r": 1026, "b": 1824, "w": 972, "h": 1728}
INK_DELTA = 28        # per-channel distance from background to count as content ink
FILL_MIN  = 0.55      # min content-bbox coverage of SAFE (canvas-fill law)
CONTRAST_MIN = 0.30   # min luminance separation ink vs bg (0..1)
BURN_IN_EXCLUDE = (0.0, 0.94, 0.60, 1.0)  # (x0,y0,x1,y1) frac — QC burn-in strip, ignored


def _safe_for(w, h):
    if h > w:  # portrait
        s = dict(SAFE916); scale = w / CANVAS916_W
        return {k: int(v * scale) for k, v in s.items()}
    scale = w / CANVAS[0]
    return {k: int(v * scale) for k, v in SAFE.items()}

CANVAS916_W = 1080


def _background(arr):
    """Modal color from the four corner patches = the background plate."""
    h, w, _ = arr.shape
    p = max(4, min(h, w) // 40)
    corners = np.vstack([
        arr[:p, :p].reshape(-1, 3), arr[:p, -p:].reshape(-1, 3),
        arr[-p:, :p].reshape(-1, 3), arr[-p:, -p:].reshape(-1, 3),
    ])
    # modal color via coarse binning
    q = (corners // 16).astype(np.int32)
    keys = q[:, 0] * 1024 + q[:, 1] * 32 + q[:, 2]
    vals, counts = np.unique(keys, return_counts=True)
    k = vals[counts.argmax()]
    return np.array([(k // 1024) * 16 + 8, ((k // 32) % 32) * 16 + 8, (k % 32) * 16 + 8], float)


def _ink_mask(arr, bg):
    d = np.abs(arr.astype(float) - bg).max(axis=2)
    m = d > INK_DELTA
    # blank the QC burn-in strip so it isn't read as edge-bleed content
    h, w = m.shape
    x0, y0, x1, y1 = BURN_IN_EXCLUDE
    m[int(y0 * h):int(y1 * h), int(x0 * w):int(x1 * w)] = False
    return m


def _lum(c):
    return (0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]) / 255.0


def contrast_regions(arr, regions):
    """Measure declared text regions in mixed-color footage, not its dimming scrim.

    Normalized boxes are explicit reviewable claims about where essential text
    lives. They replace only the whole-frame average-ink contrast measurement;
    empty-frame, safe-area and fill checks still run. Every region must pass.
    """
    if not isinstance(regions, list) or not regions:
        raise BuildError('contrast_regions must be a nonempty list')
    h, w = arr.shape[:2]
    defects = []
    for region in regions:
        if not isinstance(region, dict) or not isinstance(region.get('label'), str) or not region['label'].strip():
            raise BuildError('contrast region requires a label')
        box = region.get('box')
        if not isinstance(box, list) or len(box) != 4 or not all(
                isinstance(v, (int, float)) and not isinstance(v, bool) and np.isfinite(v) for v in box):
            raise BuildError('contrast region requires four finite normalized coordinates')
        x0, y0, x1, y1 = box
        if not (0 <= x0 < x1 <= 1 and 0 <= y0 < y1 <= 1):
            raise BuildError('contrast region must lie inside the frame')
        crop = arr[int(y0*h):int(y1*h), int(x0*w):int(x1*w)]
        if min(crop.shape[:2]) < 16:
            raise BuildError('contrast region is too small to inspect')
        bg = _background(crop)
        ink = np.abs(crop.astype(float) - bg).max(axis=2) > INK_DELTA
        label = region['label']
        if ink.mean() < .003:
            defects.append(('MAJOR', 'empty-contrast-region', f'{label}: no visible text/content'))
            continue
        sep = abs(_lum(crop[ink].astype(float).mean(axis=0)) - _lum(bg))
        if sep < CONTRAST_MIN:
            defects.append(('MAJOR', 'low-contrast',
                            f'{label}: regional luminance separation {sep:.2f} < {CONTRAST_MIN}'))
    return defects


def analyze_frame(path, regions=None):
    im = Image.open(path).convert("RGB")
    arr = np.asarray(im)
    h, w, _ = arr.shape
    safe = _safe_for(w, h)
    bg = _background(arr)
    ink = _ink_mask(arr, bg)
    defects = []
    ink_frac = ink.sum() / float(h * w)
    if ink_frac < 0.003:
        return [('MAJOR', 'empty-frame', 'steady-state sample contains no visible content')], 0.0

    ys, xs = np.where(ink)
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()

    # EDGE-BLEED / CLIPPING: ink outside the title-safe inset
    margin = max(2, int(0.004 * w))
    over = []
    if x0 < safe["x"] - margin: over.append("left")
    if x1 > safe["r"] + margin: over.append("right")
    if y0 < safe["y"] - margin: over.append("top")
    if y1 > safe["b"] + margin: over.append("bottom")
    if over:
        defects.append(("BLOCKER", "edge-bleed",
                        f"content crosses the title-safe {'/'.join(over)} edge — clipping/overflow"))

    # CANVAS-FILL: bbox coverage of SAFE
    bbox_area = max(1, (x1 - x0)) * max(1, (y1 - y0))
    cover = bbox_area / float(safe["w"] * safe["h"])
    if cover < FILL_MIN:
        defects.append(("MAJOR", "underfill",
                        f"content fills only {cover*100:.0f}% of the safe area "
                        f"(min {FILL_MIN*100:.0f}%) — too much negative space"))
    else:
        # clustered: content occupies < half of one axis leaving a big empty band
        wspan = (x1 - x0) / float(safe["w"]); hspan = (y1 - y0) / float(safe["h"])
        if wspan < 0.5 or hspan < 0.5:
            defects.append(("MAJOR", "clustered",
                            f"content clusters ({wspan*100:.0f}%×{hspan*100:.0f}% of safe) "
                            f"with a large empty band"))

    # LOW-CONTRAST: ink luminance vs bg
    ink_rgb = arr[ink].astype(float).mean(axis=0)
    sep = abs(_lum(ink_rgb) - _lum(bg))
    if regions is not None:
        defects.extend(contrast_regions(arr, regions))
    elif sep < CONTRAST_MIN:
        defects.append(("MAJOR", "low-contrast",
                        f"ink/background luminance separation {sep:.2f} < {CONTRAST_MIN} — hard to read"))
    return defects, cover


def sample_frames(mp4, outdir, fps=2):
    os.makedirs(outdir, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-i", mp4, "-vf", f"fps={fps}",
                    os.path.join(outdir, "%05d.png")],
                   check=True, capture_output=True)
    return sorted(glob.glob(os.path.join(outdir, "*.png")))


def full_bleed_beats(reel, sheet_path=None):
    """Beat ids that DECLARE themselves full-bleed, via `qc.full_bleed: true`.

    Some compositions fill the frame on purpose — a tiled logo sting, an
    edge-to-edge plate. For those, edge-bleed is the design, not a defect. The
    declaration lives in the beat sheet so it is per-beat, reviewable in the
    diff, and can never be a blanket switch that quietly disarms the gate for a
    whole reel. Underfill and every other check still apply.
    """
    try:
        bs = json.load(open(sheet_path or os.path.join(reel, "beat_sheet.json")))
    except Exception:
        return set()
    return {b.get("beat_id") for b in bs.get("beats", [])
            if (b.get("qc") or {}).get("full_bleed") is True}


def sparse_by_design_beats(reel, sheet_path=None):
    """Beat ids that DECLARE themselves sparse, via `qc.sparse_by_design: true`
    plus a written `qc.sparse_reason`.

    Some mandated compositions are sparse on purpose — the hesitant-writer
    typing bookend accumulates one line token by token, so a mid-beat frame is
    mostly cream by design. Like full_bleed, the declaration lives in the beat
    sheet, per beat, with a reason a reviewer can read in the diff. Only the
    underfill / clustered checks are waived; empty-frame, edge-bleed and
    contrast still apply. A declaration without a reason is a build error.
    """
    try:
        bs = json.load(open(sheet_path or os.path.join(reel, "beat_sheet.json")))
    except Exception:
        return set()
    out = set()
    for b in bs.get("beats", []):
        qc = b.get("qc") or {}
        if qc.get("sparse_by_design") is True:
            if not isinstance(qc.get("sparse_reason"), str) or not qc["sparse_reason"].strip():
                raise BuildError(f"{b.get('beat_id')}: sparse_by_design needs a written sparse_reason")
            out.add(b.get("beat_id"))
    return out


def beat_spans(reel, sheet_path=None):
    """(beat_id, start_s, dur_s) per beat, from the beat sheet's durations."""
    try:
        bs = json.load(open(sheet_path or os.path.join(reel, "beat_sheet.json")))
    except (OSError, ValueError) as exc:
        raise BuildError(f'Cannot read QC beat sheet: {exc}')
    validate_project(bs)
    t, spans = 0.0, []
    for b in bs.get("beats", []):
        d = positive_duration(b.get('render_duration_s') or b.get('actual_duration_s')
                              or b.get('estimated_duration_s'), b.get('beat_id', '?'))
        spans.append((b.get("beat_id", "?"), t, d)); t += d
    return spans


def sample_beats(mp4, spans, outdir, fracs=(0.5, 0.85)):
    """Sample each beat at its STEADY STATE (mid + late), never at the
    animate-in/out where a transition frame would false-flag as underfill."""
    os.makedirs(outdir, exist_ok=True)
    frames = []
    for bid, start, dur in spans:
        for fr in fracs:
            t = start + dur * fr
            out = os.path.join(outdir, f"{bid}_{int(fr*100)}.png")
            r = subprocess.run(["ffmpeg", "-y", "-ss", f"{t:.6f}", "-i", mp4,
                                "-frames:v", "1", out], capture_output=True)
            if r.returncode or not os.path.isfile(out) or os.path.getsize(out) == 0:
                raise BuildError(f'Cannot inspect {bid} at {t:.3f}s; incomplete QC is not a pass')
            frames.append(out)
    return frames


def contact_sheet(frames, out, cols=4, thumb=480):
    if not frames:
        return
    pick = frames[:: max(1, len(frames) // 16)][:16]
    ims = [Image.open(f).convert("RGB") for f in pick]
    tw = thumb; th = int(thumb * ims[0].height / ims[0].width)
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw, rows * th), (20, 20, 20))
    for i, im in enumerate(ims):
        sheet.paste(im.resize((tw, th)), ((i % cols) * tw, (i // cols) * th))
    with tempfile.TemporaryDirectory(prefix='.contact-', dir=Path(out).parent) as scratch:
        candidate = Path(scratch) / 'contact.png'
        sheet.save(candidate)
        os.replace(candidate, out)


def main():
    global FILL_MIN
    ap = argparse.ArgumentParser()
    ap.add_argument("reel", nargs="?", help="reel dir (expects <slug>-slate.mp4 or <slug>.mp4)")
    ap.add_argument("--mp4")
    ap.add_argument('--sheet', help='resolved timeline sheet; defaults to reel/beat_sheet.json')
    ap.add_argument("--frames-dir", help="test mode: analyze these PNGs directly")
    ap.add_argument("--fill-min", type=float, default=FILL_MIN)
    ap.add_argument("--lenient", action="store_true", help="downgrade MAJOR to warning")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()
    FILL_MIN = a.fill_min
    try:
        with tempfile.TemporaryDirectory(prefix='brutalist-qc-') as scratch:
            return inspect(a, scratch)
    except (BuildError, OSError, ValueError, subprocess.SubprocessError) as exc:
        try:
            root = Path(a.frames_dir) if a.frames_dir else Path(a.reel or '.')
            relative = 'REPORT.md' if a.frames_dir else '_qc/REPORT.md'
            atomic_text(writable_path(root, relative), f'# Gate V — FAILED\n\n{exc}\n')
        except (BuildError, OSError):
            pass
        sys.stderr.write(f'[gate-v] FAILED: {exc}\n')
        return 2


def inspect(a, tmp):
    if a.reel:
        writable_path(a.reel, '_qc/.check')

    if a.frames_dir:
        frames = sorted(glob.glob(os.path.join(a.frames_dir, "*.png")))
        outdir = a.frames_dir
    else:
        mp4 = a.mp4
        if not mp4 and a.reel:
            cands = glob.glob(os.path.join(a.reel, "*-slate.mp4")) or \
                    [f for f in glob.glob(os.path.join(a.reel, "*.mp4")) if "-slate" not in f]
            mp4 = cands[0] if cands else None
        if not mp4 or not os.path.exists(mp4):
            raise BuildError('No mp4 to inspect; cannot report clean')
        spans = beat_spans(a.reel, a.sheet) if a.reel else []
        # beat-aware steady-state sampling when we have the beat sheet; else uniform.
        frames = sample_beats(mp4, spans, tmp) if spans else sample_frames(mp4, tmp)
        outdir = os.path.join(a.reel or ".", "_qc"); os.makedirs(outdir, exist_ok=True)

    if not frames:
        raise BuildError('No frames inspected; cannot report clean')
    exempt = full_bleed_beats(a.reel, a.sheet) if a.reel else set()
    sparse = sparse_by_design_beats(a.reel, a.sheet) if a.reel else set()
    reports = set()
    regional = {}
    if a.reel:
        bs = json.load(open(a.sheet or os.path.join(a.reel, 'beat_sheet.json')))
        reports = {b['beat_id'] for b in bs.get('beats', []) if is_source_report(b, bs)}
        for b in bs.get('beats', []):
            qc = b.get('qc') or {}
            if 'contrast_regions' in qc:
                if not isinstance(qc.get('contrast_reason'), str) or not qc['contrast_reason'].strip():
                    raise BuildError('Regional contrast needs a written contrast_reason')
                regional[b['beat_id']] = qc['contrast_regions']

    worst = {}   # frame -> list of defects
    for f in frames:
        bid = os.path.basename(f).rsplit('_', 1)[0]
        if bid in reports:
            # Source footage is not a flat-color title card. Confirm decoding
            # and coverage here; humans review its content/framing, not ink-bbox heuristics.
            with Image.open(f) as im:
                im.load()
            continue
        d, _ = analyze_frame(f, regional.get(bid))
        if d and exempt:
            # frames are named "<beat_id>_<pct>.png"
            bid = os.path.basename(f).rsplit("_", 1)[0]
            if bid in exempt:
                d = [x for x in d if x[1] != "edge-bleed"]
        if d and sparse and bid in sparse:
            d = [x for x in d if x[1] not in ("underfill", "clustered")]
        if d:
            worst[f] = d

    # write report
    report = os.path.join(outdir if a.frames_dir else os.path.join(a.reel or ".", "_qc"), "REPORT.md")
    os.makedirs(os.path.dirname(report), exist_ok=True)
    n_block = sum(1 for d in worst.values() for sev, *_ in d if sev == "BLOCKER")
    n_major = sum(1 for d in worst.values() for sev, *_ in d if sev == "MAJOR")
    lines = ["# Gate V — visual QC report", "",
             f"Frames sampled: {len(frames)}  ·  BLOCKER: {n_block}  ·  MAJOR: {n_major}", ""]
    if reports:
        lines += ['Source-report samples: decoded/covered; template styling checks not applicable. '
                  'Human content/framing review remains required.', '']
    if regional:
        lines += ['Regional text-contrast checks (all declared regions required): ' +
                  ', '.join(sorted(regional)) + '. Whole-frame dimming/scene color is not text contrast; '
                  'empty-frame, fill and declared safe-area checks remain active. Visual content review remains required.', '']
    for f in sorted(worst):
        lines.append(f"### {os.path.basename(f)}")
        for sev, kind, msg in worst[f]:
            lines.append(f"- **{sev}** `{kind}` — {msg}")
        lines.append("")
    if not worst:
        lines.append("Clean — no BLOCKER/MAJOR defects. ✓")
    atomic_text(report, "\n".join(lines))

    if not a.frames_dir:
        contact_sheet(frames, os.path.join(os.path.dirname(report), "contact_sheet.png"))

    if not a.quiet:
        print(f"[gate-v] frames={len(frames)} BLOCKER={n_block} MAJOR={n_major} → {report}")
    blocking = n_block + (0 if a.lenient else n_major)
    if blocking:
        if not a.quiet:
            print(f"[gate-v] FAILED — {blocking} blocking defect(s). Reel not clean; fix and re-render.")
        return 2
    return 1 if worst else 0


if __name__ == "__main__":
    sys.exit(main())
