#!/usr/bin/env python3
"""
manim_layout_audit.py
=====================
Bear's Notes — deterministic LAYOUT QA pass for Manim scenes.

The video analogue of ai1-cli's `npm run audit:layout`. Instead of inspecting
rendered pixels, it asks Manim itself for the exact bounding box of every Text
object on screen — so it is deterministic, OCR-free, and font-agnostic.

It hooks the scene at every steady-state moment (each `wait`, and the end of
each `play`) and flags two classes of layout defect:

  1. TEXT-ON-TEXT      two different Text objects whose boxes overlap
                       (e.g. a swapping caption colliding with an axis label)
  2. OUT-OF-FRAME      a Text whose box leaves the safe area (WARN) or the
                       visible frame entirely (ERROR)

For each flag it records the moment (snapshot #, approx timestamp), the text
strings involved, their boxes, and — with --png — saves an annotated frame so
you can see the collision.

Run on ONE video folder (cd into it, or pass --scene):

    ai
    cd ~/Documents/Cowork/Manim/energy-levels-arent-evenly-spaced
    python ../../bears-doodles/scripts/manim_layout_audit.py energy_levels_arent_evenly_spaced.py

Outputs (next to the scene):
    layout_audit.json   machine-readable findings
    layout_audit.md      human-readable report
    layout_audit_frames/ annotated PNGs (only with --png)

Exit code 0 = clean, 1 = warnings only, 2 = errors (out-of-frame / hard overlap).
Advisory by design: it reports, it never edits your scene.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

# ---------------------------------------------------------------- tunables ----
DEFAULTS = dict(
    safe_w=6.3,          # house safe-area half-width  (matches scenes' SAFE_W)
    safe_h=3.4,          # house safe-area half-height (matches scenes' SAFE_H)
    min_overlap=0.12,    # flag a text pair when intersection >= this * smaller box area
    min_box=0.02,        # ignore degenerate/empty boxes below this area
    curve_inset=0.15,    # world units to inset a label's centerline (ignore corner clips)
    max_segs=6000,       # cap stroke segments per snapshot (perf guard)
    curve_strict=False,  # when True, TEXT/CURVE is an ERROR (else WARN)
)


def _seg_seg(x1, y1, x2, y2, x3, y3, x4, y4) -> bool:
    """Do segments (1-2) and (3-4) intersect? Ported from ai1-cli's SVG
    layout auditor (scripts/svg-layout-audit.mjs)."""
    d = (x2 - x1) * (y4 - y3) - (y2 - y1) * (x4 - x3)
    if d == 0:
        return False
    t = ((x3 - x1) * (y4 - y3) - (y3 - y1) * (x4 - x3)) / d
    u = ((x3 - x1) * (y2 - y1) - (y3 - y1) * (x2 - x1)) / d
    return 0.0 <= t <= 1.0 and 0.0 <= u <= 1.0


def _struck(box, strokes, inset):
    """True if any stroke segment crosses the label's horizontal OR vertical
    centerline (each inset so a connector merely clipping a corner is ignored).
    Same rule as the SVG auditor's TEXT/LINE + TEXT/PATH check."""
    x0, y0, x1, y1 = box
    px = min(inset, (x1 - x0) / 4.0)
    py = min(inset, (y1 - y0) / 4.0)
    cx, cy = (x0 + x1) / 2.0, (y0 + y1) / 2.0
    for (sx1, sy1, sx2, sy2) in strokes:
        if _seg_seg(sx1, sy1, sx2, sy2, x0 + px, cy, x1 - px, cy) or \
           _seg_seg(sx1, sy1, sx2, sy2, cx, y0 + py, cx, y1 - py):
            return True
    return False

# These are filled in once manim is imported (so this file imports without it).
TEXT_TYPES: tuple = ()
config = None


def _import_manim_and_patch(snapshots: list):
    """Import manim, record the Text-like classes, and hook Scene.wait/play
    so each steady-state moment appends a snapshot of on-screen text boxes."""
    global TEXT_TYPES, config
    import manim as M
    from manim import Scene, config as cfg

    config = cfg
    # Text-like leaf types we treat as "labels". Tex/MathTex included when present.
    names = ["Text", "MarkupText", "Tex", "MathTex", "Title", "Paragraph"]
    TEXT_TYPES = tuple(getattr(M, n) for n in names if hasattr(M, n))

    orig_wait = Scene.wait
    orig_play = Scene.play

    def _clock(scene):
        # best-effort timestamp; Manim tracks renderer.time
        return round(float(getattr(getattr(scene, "renderer", None), "time", 0.0) or 0.0), 2)

    def patched_wait(self, *a, **k):
        _snapshot(self, "wait", _clock(self), snapshots)
        return orig_wait(self, *a, **k)

    def patched_play(self, *a, **k):
        r = orig_play(self, *a, **k)
        _snapshot(self, "play-end", _clock(self), snapshots)
        return r

    Scene.wait = patched_wait
    Scene.play = patched_play
    return M


def _collect_texts(mob, out):
    """Walk the mobject tree; record Text-like nodes WITHOUT descending into
    their own glyph submobjects."""
    if isinstance(mob, TEXT_TYPES):
        out.append(mob)
        return
    for s in getattr(mob, "submobjects", []):
        _collect_texts(s, out)


def _collect_strokes(mob, out, cap):
    """Flatten every visible stroked (non-text) leaf VMobject into world-space
    line segments — curves, axes, connectors, rung lines. Text glyphs are skipped
    (they are labels, not strokes). A mobject may declare itself an INTENTIONAL
    annotation (strike-through, editor's ring) via `mob._qc_intentional = True`
    — that subtree is exempt from TEXT_ON_CURVE; everything else still audits."""
    if len(out) >= cap:
        return
    if getattr(mob, "_qc_intentional", False):
        return
    if isinstance(mob, TEXT_TYPES):
        return
    subs = getattr(mob, "submobjects", [])
    if subs:
        for s in subs:
            _collect_strokes(s, out, cap)
        return
    # leaf mobject
    try:
        if float(mob.get_stroke_opacity()) <= 0.02:
            return
    except Exception:
        return
    try:
        anchors = mob.get_anchors()
    except Exception:
        return
    if anchors is None or len(anchors) < 2:
        return
    for k in range(len(anchors) - 1):
        if len(out) >= cap:
            return
        x1, y1 = float(anchors[k][0]), float(anchors[k][1])
        x2, y2 = float(anchors[k + 1][0]), float(anchors[k + 1][1])
        if (x1 - x2) ** 2 + (y1 - y2) ** 2 > 1e-6:
            out.append((x1, y1, x2, y2))


def _visible(mob) -> bool:
    try:
        fo = float(mob.get_fill_opacity())
    except Exception:
        fo = 1.0
    try:
        so = float(mob.get_stroke_opacity())
    except Exception:
        so = 0.0
    return (fo > 0.02) or (so > 0.02)


def _aabb(mob):
    """Axis-aligned bounding box via edge points: (x0,y0,x1,y1)."""
    try:
        x0, x1 = float(mob.get_left()[0]), float(mob.get_right()[0])
        y0, y1 = float(mob.get_bottom()[1]), float(mob.get_top()[1])
    except Exception:
        return None
    if x1 < x0:
        x0, x1 = x1, x0
    if y1 < y0:
        y0, y1 = y1, y0
    return (x0, y0, x1, y1)


def _text_of(mob) -> str:
    for attr in ("text", "original_text", "tex_string"):
        v = getattr(mob, attr, None)
        if isinstance(v, str) and v.strip():
            return v.strip().replace("\n", " ")
    return f"<{type(mob).__name__}>"


def _area(b):
    return max(0.0, b[2] - b[0]) * max(0.0, b[3] - b[1])


def _intersect_area(a, b):
    ix = min(a[2], b[2]) - max(a[0], b[0])
    iy = min(a[3], b[3]) - max(a[1], b[1])
    if ix <= 0 or iy <= 0:
        return 0.0
    return ix * iy


def _snapshot(scene, kind, t, snapshots):
    texts = []
    for m in list(getattr(scene, "mobjects", [])):
        _collect_texts(m, texts)
    items = []
    for m in texts:
        if not _visible(m):
            continue
        b = _aabb(m)
        if b is None or _area(b) < DEFAULTS["min_box"]:
            continue
        items.append((_text_of(m), b))
    if items:
        strokes = []
        for m in list(getattr(scene, "mobjects", [])):
            _collect_strokes(m, strokes, DEFAULTS["max_segs"])
        snapshots.append(dict(idx=len(snapshots), kind=kind, t=t,
                              items=items, strokes=strokes))


def _analyze(snapshots, opt):
    """Turn raw snapshots into deduped findings."""
    half_w = float(config.frame_width) / 2.0
    half_h = float(config.frame_height) / 2.0
    sw, sh = opt["safe_w"], opt["safe_h"]

    overlaps = {}   # key -> finding
    offframe = {}   # key -> finding
    struck = {}     # key -> finding (text sitting on a curve/line)

    for snap in snapshots:
        items = snap["items"]
        strokes = snap.get("strokes", [])
        # --- text struck by a curve / line (ported from the SVG layout auditor) ---
        if strokes:
            for txt, b in items:
                if not _struck(b, strokes, opt["curve_inset"]):
                    continue
                sev = "ERROR" if opt.get("curve_strict") else "WARN"
                rec = struck.get(txt)
                if rec is None:
                    struck[txt] = dict(
                        type="TEXT_ON_CURVE", severity=sev, text=txt,
                        t=snap["t"], snap=snap["idx"],
                        box=[round(v, 2) for v in b],
                    )
        # --- text-on-text ---
        for i in range(len(items)):
            ti, bi = items[i]
            for j in range(i + 1, len(items)):
                tj, bj = items[j]
                if ti == tj:
                    continue  # same string twice = almost always intentional echo
                inter = _intersect_area(bi, bj)
                if inter <= 0:
                    continue
                ratio = inter / max(1e-9, min(_area(bi), _area(bj)))
                if ratio < opt["min_overlap"]:
                    continue
                key = tuple(sorted((ti, tj)))
                sev = "ERROR" if ratio >= 0.25 else "WARN"   # visible is visible
                rec = overlaps.get(key)
                if rec is None or ratio > rec["ratio"]:
                    overlaps[key] = dict(
                        type="TEXT_ON_TEXT", severity=sev, ratio=round(ratio, 3),
                        a=ti, b=tj, t=snap["t"], snap=snap["idx"],
                        box_a=[round(v, 2) for v in bi],
                        box_b=[round(v, 2) for v in bj],
                    )
        # --- out of frame / safe area ---
        for txt, b in items:
            hard = (b[0] < -half_w - 0.05 or b[2] > half_w + 0.05 or
                    b[1] < -half_h - 0.05 or b[3] > half_h + 0.05)
            soft = (b[0] < -sw or b[2] > sw or b[1] < -sh or b[3] > sh)
            if not (hard or soft):
                continue
            key = txt
            sev = "ERROR" if hard else "WARN"
            rec = offframe.get(key)
            if rec is None or (sev == "ERROR" and rec["severity"] != "ERROR"):
                offframe[key] = dict(
                    type=("OFF_FRAME" if hard else "OFF_SAFE_AREA"),
                    severity=sev, text=txt, t=snap["t"], snap=snap["idx"],
                    box=[round(v, 2) for v in b],
                )

    findings = list(overlaps.values()) + list(offframe.values()) + list(struck.values())
    findings.sort(key=lambda f: (0 if f["severity"] == "ERROR" else 1, f["t"]))
    return findings


def _write_reports(folder: Path, scene_name: str, snapshots, findings, opt):
    errors = [f for f in findings if f["severity"] == "ERROR"]
    warns = [f for f in findings if f["severity"] == "WARN"]
    payload = dict(
        scene=scene_name, snapshots=len(snapshots),
        errors=len(errors), warnings=len(warns),
        safe_area=[opt["safe_w"], opt["safe_h"]],
        min_overlap=opt["min_overlap"], findings=findings,
    )
    (folder / "layout_audit.json").write_text(json.dumps(payload, indent=2))

    lines = [f"# Layout audit — {scene_name}", ""]
    lines.append(f"- snapshots inspected: **{len(snapshots)}**")
    lines.append(f"- errors: **{len(errors)}**  ·  warnings: **{len(warns)}**")
    lines.append(f"- safe area (half-extents): ±{opt['safe_w']} x / ±{opt['safe_h']} y")
    lines.append("")
    if not findings:
        lines.append("✅ No text overlaps or out-of-frame text detected.")
    else:
        def fmt(f):
            if f["type"] == "TEXT_ON_TEXT":
                return (f"- **{f['severity']}** · t≈{f['t']}s · text-on-text "
                        f"(overlap {int(f['ratio']*100)}%): "
                        f"`{f['a']}`  ✕  `{f['b']}`")
            if f["type"] == "OFF_FRAME":
                return (f"- **{f['severity']}** · t≈{f['t']}s · off-frame: "
                        f"`{f['text']}`  box={f['box']}")
            if f["type"] == "TEXT_ON_CURVE":
                return (f"- **{f['severity']}** · t≈{f['t']}s · label on a curve/line: "
                        f"`{f['text']}`  box={f['box']}")
            return (f"- **{f['severity']}** · t≈{f['t']}s · outside safe area: "
                    f"`{f['text']}`  box={f['box']}")
        if errors:
            lines.append("## Errors")
            lines += [fmt(f) for f in errors]
            lines.append("")
        if warns:
            lines.append("## Warnings")
            lines += [fmt(f) for f in warns]
            lines.append("")
    (folder / "layout_audit.md").write_text("\n".join(lines) + "\n")
    return errors, warns


def main(argv=None):
    ap = argparse.ArgumentParser(description="Deterministic text-overlap / out-of-frame audit for a Manim scene.")
    ap.add_argument("scene", nargs="?", help="scene .py file (default: the only non-helper .py in cwd)")
    ap.add_argument("--class", dest="cls", default="BearsDoodlesVideo", help="Scene subclass name")
    ap.add_argument("--safe-w", type=float, default=DEFAULTS["safe_w"])
    ap.add_argument("--safe-h", type=float, default=DEFAULTS["safe_h"])
    ap.add_argument("--min-overlap", type=float, default=DEFAULTS["min_overlap"],
                    help="min intersection / smaller-box-area to flag a text pair (0-1)")
    ap.add_argument("--png", action="store_true", help="save annotated frames at flagged moments")
    ap.add_argument("--portrait", action="store_true",
                    help="audit the 9:16 render (1080x1920) instead of the default 16:9")
    ap.add_argument("--curve-strict", action="store_true",
                    help="treat TEXT-ON-CURVE (label struck by a graph/line) as an ERROR, not a warning")
    args = ap.parse_args(argv)
    if args.portrait:
        # portrait safe band (half-extents) ~ matches bn_layout's portrait content band
        args.safe_w, args.safe_h = 1.95, 3.4

    opt = dict(safe_w=args.safe_w, safe_h=args.safe_h, min_overlap=args.min_overlap,
               curve_inset=DEFAULTS["curve_inset"], max_segs=DEFAULTS["max_segs"],
               curve_strict=args.curve_strict)

    # locate the scene file
    if args.scene:
        scene_path = Path(args.scene).resolve()
    else:
        cands = [p for p in Path.cwd().glob("*.py")
                 if not p.name.endswith("_svg_doodles.py")
                 and p.name not in {"manim_layout_audit.py"}]
        if len(cands) != 1:
            print(f"[audit] specify a scene file; found {len(cands)} candidates in {Path.cwd()}", file=sys.stderr)
            return 2
        scene_path = cands[0].resolve()
    if not scene_path.exists():
        print(f"[audit] scene not found: {scene_path}", file=sys.stderr)
        return 2

    folder = scene_path.parent
    snapshots: list = []
    M = _import_manim_and_patch(snapshots)

    # render headless: no file writes, fast, deterministic geometry
    from manim import tempconfig, config as _cfg

    # For a portrait audit, set the 9:16 resolution BEFORE importing the scene, so
    # bn_layout's frame-sync (which runs at scene import) sees portrait pixels.
    if args.portrait:
        _cfg.pixel_width, _cfg.pixel_height = 1080, 1920
        _cfg.frame_height = 8.0
        _cfg.frame_width = 4.5

    # ensure relative paths (mp3/timings.json) resolve from the scene folder
    cwd0 = Path.cwd()
    try:
        import os
        os.chdir(folder)
        if str(folder) not in sys.path:  # reel-local helpers (e.g. seis_graphics.py) import like manim does from the reel dir
            sys.path.insert(0, str(folder))
        spec = importlib.util.spec_from_file_location("bn_audit_scene", str(scene_path))
        mod = importlib.util.module_from_spec(spec)
        sys.modules["bn_audit_scene"] = mod
        spec.loader.exec_module(mod)
        SceneCls = getattr(mod, args.cls, None)
        if SceneCls is None:
            print(f"[audit] class {args.cls} not found in {scene_path.name}", file=sys.stderr)
            return 2
        cfg = {"dry_run": True, "disable_caching": True, "write_to_movie": False, "verbosity": "ERROR"}
        if args.portrait:
            cfg.update({"pixel_width": 1080, "pixel_height": 1920, "frame_width": 4.5, "frame_height": 8.0})
        else:
            cfg["quality"] = "low_quality"
        with tempconfig(cfg):
            scene = SceneCls()
            scene.render()
    finally:
        os.chdir(cwd0)

    findings = _analyze(snapshots, opt)
    errors, warns = _write_reports(folder, scene_path.stem, snapshots, findings, opt)

    if args.png and findings:
        _save_frames(scene_path, args.cls, folder, findings, opt)

    status = "CLEAN" if not findings else (f"{len(errors)} error(s), {len(warns)} warning(s)")
    print(f"[audit] {scene_path.stem}: {len(snapshots)} snapshots → {status}")
    print(f"[audit] report: {folder/'layout_audit.md'}")
    return 0 if not findings else (2 if errors else 1)


def _save_frames(scene_path, cls, folder, findings, opt):
    """Re-render only the flagged snapshot indices and dump annotated PNGs.
    Best-effort; skipped silently if the renderer can't hand back a frame."""
    try:
        from PIL import Image, ImageDraw
    except Exception:
        print("[audit] --png needs Pillow (pip install pillow --break-system-packages); skipping frames")
        return
    flagged = sorted({f["snap"] for f in findings})
    out = folder / "layout_audit_frames"
    out.mkdir(exist_ok=True)

    captures: dict = {}
    snap_counter = {"n": 0}
    import manim as M
    from manim import Scene, config as cfg
    orig_wait, orig_play = Scene.wait, Scene.play

    def grab(self):
        i = snap_counter["n"]
        snap_counter["n"] += 1
        if i in flagged and i not in captures:
            try:
                captures[i] = self.renderer.get_frame()
            except Exception:
                pass

    def w(self, *a, **k):
        grab(self); return orig_wait(self, *a, **k)

    def p(self, *a, **k):
        r = orig_play(self, *a, **k); grab(self); return r

    Scene.wait, Scene.play = w, p
    try:
        import os
        cwd0 = os.getcwd(); os.chdir(folder)
        spec = importlib.util.spec_from_file_location("bn_audit_scene_png", str(scene_path))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        SceneCls = getattr(mod, cls)
        from manim import tempconfig
        with tempconfig({"quality": "low_quality", "dry_run": True,
                         "disable_caching": True, "write_to_movie": False,
                         "verbosity": "ERROR"}):
            SceneCls().render()
    except Exception as e:
        print(f"[audit] frame capture failed: {e}")
        return
    finally:
        Scene.wait, Scene.play = orig_wait, orig_play
        os.chdir(cwd0)

    pw, ph = int(cfg.pixel_width), int(cfg.pixel_height)
    fw, fh = float(cfg.frame_width), float(cfg.frame_height)

    def to_px(x, y):
        return (int((x + fw / 2) / fw * pw), int((fh / 2 - y) / fh * ph))

    by_snap = {}
    for f in findings:
        by_snap.setdefault(f["snap"], []).append(f)
    for idx, arr in captures.items():
        try:
            img = Image.fromarray(arr).convert("RGB")
        except Exception:
            continue
        d = ImageDraw.Draw(img)
        for f in by_snap.get(idx, []):
            boxes = []
            if f["type"] == "TEXT_ON_TEXT":
                boxes = [f["box_a"], f["box_b"]]
            else:
                boxes = [f["box"]]
            for b in boxes:
                x0, y0 = to_px(b[0], b[3])
                x1, y1 = to_px(b[2], b[1])
                d.rectangle([x0, y0, x1, y1], outline=(192, 57, 43), width=4)
        img.save(out / f"snap_{idx:03d}.png")
    print(f"[audit] annotated frames: {out}")


if __name__ == "__main__":
    raise SystemExit(main())
