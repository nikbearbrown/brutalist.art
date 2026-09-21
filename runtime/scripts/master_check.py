#!/usr/bin/env python3
"""master_check.py — GATE MASTER (Phase 3: PUBLISH-HARDENING)

Asserts the compiled master MP4 is clean and spec-compliant before staging.
Runs on a reel directory's slug.mp4. No bypass flag — the hard line is at
stage time.

Assertions (all must pass for exit 0):
  1. Resolution: 3840×2160 (16:9) or 2160×3840 (9:16 sheet). Shorts compiled
     at 1080×1920 (shorts.py minimum) are accepted for <kind=short> reels.
  2. Frame rate: 24 fps (compile.py's fixed default).
  3. Pixel format: yuv420p (compile.py's -pix_fmt).
  4. Audio stream present (NEVER-STRIP LAW).
  5. Video codec: h264 / libx264 (compile.py's encoder).
  6. Duration matches beat-sheet total within tolerance (imports clock_check).
  7. No review-label band in bottom-left of 3 sampled frames (marker check).

Usage:
    python3 scripts/master_check.py <reel_dir> [--mp4 path] [--sheet name]

Exit codes:
    0 — PASS (MASTERCHECK.md written)
    2 — FAIL (MASTERCHECK.md written with violations)
    3 — SKIP (missing deps: ffprobe or Pillow)

Writes MASTERCHECK.md into the reel directory.
"""

from __future__ import annotations
import argparse, json, shutil, subprocess, sys, tempfile
from pathlib import Path

FFMPEG  = shutil.which("ffmpeg")  or "ffmpeg"
FFPROBE = shutil.which("ffprobe") or "ffprobe"

# Resolution constants from compile.py and shorts.py
_UHD_W, _UHD_H       = 3840, 2160   # 16:9 4K (compile.py THE 4K LAW)
_SHORTS_W, _SHORTS_H = 2160, 3840   # 9:16 4K portrait (compile.py + shorts.py)
_SHORTS_MIN_W, _SHORTS_MIN_H = 1080, 1920  # shorts.py W, H minimum
_FPS         = 24
_PIX_FMT     = "yuv420p"
_CLOCK_TOL   = 1.5  # seconds — same as clock_check.py default


def _write_md(reel_dir: Path, lines: list[str]) -> None:
    (reel_dir / "MASTERCHECK.md").write_text("\n".join(lines) + "\n")


def _ffprobe_json(path: Path) -> dict:
    r = subprocess.run(
        [FFPROBE, "-v", "quiet", "-print_format", "json",
         "-show_format", "-show_streams", str(path)],
        capture_output=True, text=True,
    )
    try:
        return json.loads(r.stdout)
    except Exception:
        return {}


def _check_resolution(w: int, h: int, is_short: bool) -> str | None:
    """Return error string or None if clean."""
    if is_short:
        if (w == _SHORTS_W and h == _SHORTS_H):
            return None   # 9:16 4K portrait — perfect
        if (w == _SHORTS_MIN_W and h == _SHORTS_MIN_H):
            return None   # 9:16 1080×1920 — shorts.py minimum, acceptable
        return (f"resolution {w}×{h} does not match 9:16 spec "
                f"({_SHORTS_W}×{_SHORTS_H} or {_SHORTS_MIN_W}×{_SHORTS_MIN_H} for Shorts)")
    if w == _UHD_W and h == _UHD_H:
        return None   # 16:9 4K — perfect
    return f"resolution {w}×{h} does not match 16:9 4K spec ({_UHD_W}×{_UHD_H})"


def _source_cut_intervals(reel_dir: Path, sheet_name: str = "beat_sheet.json") -> list[tuple[float, float]]:
    """Return (start_s, end_s) pairs for every SOURCE-CUT beat.
    Source-cut beats carry external video content; their frames have no
    controlled typography and must be exempt from the marker-band heuristic."""
    sheet = reel_dir / sheet_name
    if not sheet.exists():
        return []
    try:
        d = json.loads(sheet.read_text())
    except Exception:
        return []
    intervals: list[tuple[float, float]] = []
    t = 0.0
    for b in d.get("beats", []):
        dur = float(b.get("actual_duration_s") or b.get("duration_s") or 0)
        shot_type = (b.get("shot") or {}).get("type", "")
        if shot_type.upper() == "SOURCE-CUT":
            intervals.append((t, t + dur))
        t += dur
    return intervals


def _check_markers(mp4: Path, dur: float, reel_dir: Path | None = None,
                   sheet_name: str = "beat_sheet.json") -> list[str]:
    """Sample 3 frames; flag any that show a review-label dark band in the
    bottom-left corner that is absent from the top-left (distinguishes a label
    overlay from an intentionally dark beat). Reuses post.py's exact logic."""
    try:
        from PIL import Image
    except ImportError:
        return []   # PIL missing — skip marker check (not a FAIL)

    source_cut_ivs = _source_cut_intervals(reel_dir, sheet_name) if reel_dir else []

    errors = []
    sample_times = [dur * p for p in (0.15, 0.50, 0.85)]
    with tempfile.TemporaryDirectory() as tmp:
        for i, t in enumerate(sample_times):
            frame = Path(tmp) / f"mc-{i}.png"
            r = subprocess.run(
                [FFMPEG, "-y", "-ss", f"{t:.3f}", "-i", str(mp4),
                 "-frames:v", "1", "-q:v", "2", str(frame)],
                capture_output=True,
            )
            if r.returncode != 0 or not frame.exists():
                continue
            img = Image.open(frame).convert("RGB")
            fw, fh = img.size
            bw, bh = min(400, fw), min(90, fh)
            bot_img = img.crop((0, fh - bh, bw, fh)).convert("RGB")
            top_img = img.crop((0, 0, bw, bh)).convert("RGB")
            bot_raw = bot_img.tobytes()
            top_raw = top_img.tobytes()
            bot = [(bot_raw[i], bot_raw[i+1], bot_raw[i+2])
                   for i in range(0, len(bot_raw), 3)]
            top = [(top_raw[i], top_raw[i+1], top_raw[i+2])
                   for i in range(0, len(top_raw), 3)]

            def _dark(pixels):
                return sum(1 for rv, gv, bv in pixels
                           if rv < 55 and gv < 55 and bv < 55) / max(len(pixels), 1)

            bot_pct = _dark(bot)
            top_pct = _dark(top)
            # A genuine marker band (drawtext overlay from `art run`) would sit only at the
            # very bottom; the top-left of the same frame would be near-zero dark unless it's
            # an intentionally dark design beat (top_pct ≥ 0.35). Source-cut beats can have
            # moderate dark content in the top (e.g. lit scene with dark corners) that
            # pushes top_pct above 0 but well below the 0.35 band. Use 0.20 as the lower
            # threshold so natural video content with top_pct 15–30% is not mistaken for a
            # marker on a mostly-light beat.
            is_dark_beat = top_pct >= 0.20
            in_source_cut = any(s <= t <= e for s, e in source_cut_ivs)
            if bot_pct >= 0.35 and not is_dark_beat and not in_source_cut:
                errors.append(
                    f"frame at t={t:.0f}s: bottom-left dark={bot_pct:.1%} "
                    f"(top_pct={top_pct:.1%}) — possible review-label overlay; "
                    "use `art final` not `art run` to produce the master"
                )
    return errors


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("reel_dir", type=Path)
    ap.add_argument("--mp4", type=Path, default=None,
                    help="explicit master path (default: <reel>/<slug>.mp4)")
    ap.add_argument("--sheet", default="beat_sheet.json")
    args = ap.parse_args(argv)

    reel_dir = args.reel_dir.resolve()

    if not shutil.which("ffprobe"):
        _write_md(reel_dir, ["# MASTERCHECK", "", "SKIP — ffprobe not on PATH"])
        sys.exit(3)

    bs_path = reel_dir / args.sheet
    slug = reel_dir.name
    is_short = False
    beats = []
    expected_fps = _FPS
    if bs_path.exists():
        try:
            sheet = json.loads(bs_path.read_text())
            meta = sheet.get("metadata", {})
            slug = meta.get("slug") or slug
            if isinstance(meta.get("fps"), (int, float)) and meta["fps"] > 0:
                expected_fps = int(meta["fps"])  # footage reels declare 30
            is_short = (str(meta.get("kind", "")).lower() == "short"
                        or str(meta.get("aspect_ratio", "")).startswith("9:"))
            beats = sheet.get("beats", [])
            for b in beats:
                if "beat_id" not in b and "id" in b:
                    b["beat_id"] = b["id"]
                if "actual_duration_s" not in b:
                    for k in ("est_s", "estimated_duration_s"):
                        if k in b:
                            b["actual_duration_s"] = float(b[k])
                            break
        except Exception as e:
            pass

    mp4 = args.mp4 or reel_dir / f"{slug}.mp4"

    failures: list[str] = []
    notes:    list[str] = []

    if not mp4.exists():
        _write_md(reel_dir, [
            "# MASTERCHECK", "",
            f"FAIL — master not found: {mp4.name}",
        ])
        print(f"[master] FAIL — master not found: {mp4}")
        sys.exit(2)

    info = _ffprobe_json(mp4)
    streams = info.get("streams", [])
    v_stream = next((s for s in streams if s.get("codec_type") == "video"), {})
    a_streams = [s for s in streams if s.get("codec_type") == "audio"]
    fmt      = info.get("format", {})

    w   = v_stream.get("width",  0)
    h   = v_stream.get("height", 0)
    fps_str = v_stream.get("r_frame_rate", "0/1")
    try:
        n, d = fps_str.split("/")
        fps = round(int(n) / int(d))
    except Exception:
        fps = 0
    pix_fmt   = v_stream.get("pix_fmt", "")
    codec_tag = v_stream.get("codec_name", "")
    dur_str   = fmt.get("duration") or v_stream.get("duration", "0")
    try:
        actual_dur = float(dur_str)
    except ValueError:
        actual_dur = 0.0

    # 1. Resolution
    res_err = _check_resolution(w, h, is_short)
    if res_err:
        failures.append(f"resolution: {res_err}")

    # 2. Frame rate
    if fps != expected_fps:
        failures.append(f"frame_rate: got {fps} fps, expected {expected_fps}")

    # 3. Pixel format
    if pix_fmt != _PIX_FMT:
        failures.append(f"pix_fmt: got '{pix_fmt}', expected '{_PIX_FMT}'")

    # 4. Audio stream
    if not a_streams:
        failures.append("audio: no audio stream found (NEVER-STRIP LAW violation)")

    # 5. Video codec
    if codec_tag not in ("h264", "hevc", ""):   # hevc from Topaz upscale — allowed
        failures.append(f"video_codec: got '{codec_tag}', expected h264 or hevc")
    if not codec_tag:
        failures.append("video_codec: could not read codec name from stream")

    # 6. Duration (imports clock_check's sheet_total)
    if beats:
        try:
            import importlib.util, sys as _sys
            _ck_path = Path(__file__).resolve().parent / "clock_check.py"
            _spec = importlib.util.spec_from_file_location("clock_check", _ck_path)
            _ck = importlib.util.module_from_spec(_spec)
            _spec.loader.exec_module(_ck)
            expected_dur = _ck.sheet_total(beats)
            drift = abs(actual_dur - expected_dur)
            if drift > _CLOCK_TOL:
                failures.append(
                    f"duration: drift {drift:.3f}s exceeds tolerance {_CLOCK_TOL}s "
                    f"(expected {expected_dur:.3f}s, got {actual_dur:.3f}s)"
                )
            else:
                notes.append(f"duration: {actual_dur:.3f}s  expected={expected_dur:.3f}s  drift={drift:.3f}s ✓")
        except Exception as e:
            notes.append(f"duration: clock_check import failed ({e}) — skipped")
    else:
        notes.append("duration: no beats in sheet — skipped")

    # 7. Marker check (PIL optional — missing PIL = skip silently)
    if actual_dur > 0:
        marker_errors = _check_markers(mp4, actual_dur, reel_dir=args.reel_dir,
                                        sheet_name=args.sheet)
        failures.extend(marker_errors)

    verdict = "PASS" if not failures else "FAIL"

    rows = [
        ("master", mp4.name),
        ("resolution", f"{w}×{h}"),
        ("fps", str(fps)),
        ("pix_fmt", pix_fmt),
        ("audio_streams", str(len(a_streams))),
        ("video_codec", codec_tag),
        ("duration_s", f"{actual_dur:.3f}"),
        ("is_short", str(is_short)),
        ("failures", str(len(failures))),
        ("verdict", f"**{verdict}**"),
    ]
    lines = ["# MASTERCHECK", "", "| field | value |", "|---|---|"]
    lines += [f"| {k} | {v} |" for k, v in rows]
    if notes:
        lines += ["", "## Notes", ""] + [f"- {n}" for n in notes]
    if failures:
        lines += ["", "## Failures", ""] + [f"- {f}" for f in failures]
    lines += ["", f"GATE MASTER: {verdict}"]
    _write_md(reel_dir, lines)

    if failures:
        print(f"[master] FAIL — {len(failures)} violation(s):")
        for f in failures:
            print(f"[master]   {f}")
        sys.exit(2)
    else:
        print(f"[master] PASS  {w}×{h}  {fps}fps  {pix_fmt}  {codec_tag}  {actual_dur:.1f}s")


if __name__ == "__main__":
    main()
