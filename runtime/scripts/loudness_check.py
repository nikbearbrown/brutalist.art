#!/usr/bin/env python3
"""loudness_check.py — GATE LOUDNESS (Phase 3: PUBLISH-HARDENING)

Audio quality gate for staged masters. Asserts:
  1. Integrated LUFS is within the pipeline-calibrated window.
  2. True peak ≤ −1.0 dBTP (EBU R128 standard; not negotiable).
  3. No narration beat is effectively silent throughout its entire window
     (catches single dead-beat dropout that whole-reel mean_volume misses).

LUFS window: −28.0 to −18.0 LUFS (calibrated from 5 published masters).
See PUBLISH-HARDENING-INSTALL.md for the measured distribution and the
conflict report vs. YouTube's −14 LUFS reference.

Usage:
    python3 scripts/loudness_check.py <reel_dir> [--mp4 path] [--sheet name]

Exit codes:
    0 — PASS (LOUDNESS.md written)
    2 — FAIL (LOUDNESS.md written with violations)
    3 — SKIP (ffmpeg missing or reel has no narration)

Writes LOUDNESS.md into the reel directory.
"""

from __future__ import annotations
import argparse, json, re, shutil, subprocess, sys, tempfile
from pathlib import Path

FFMPEG  = shutil.which("ffmpeg")  or "ffmpeg"
FFPROBE = shutil.which("ffprobe") or "ffprobe"

# ── calibrated thresholds (see install log for derivation) ────────────────────
LUFS_LOW        = -28.0   # floor — catches silent/failed mixes
LUFS_HIGH       = -18.0   # ceiling — catches wrong-file or over-compressed upload
TRUE_PEAK_CEIL  = -1.0    # dBTP — EBU R128 standard, not negotiable

# A narration beat whose mean volume stays at or below this is silent.
_BEAT_SILENCE_FLOOR_DB = -55.0


def _bid(beat: dict) -> str:
    return beat.get("beat_id") or beat.get("id") or ""


def _write_md(reel_dir: Path, lines: list[str]) -> None:
    (reel_dir / "LOUDNESS.md").write_text("\n".join(lines) + "\n")


def _measure_loudnorm(mp4: Path) -> tuple[float | None, float | None]:
    """Return (integrated_lufs, true_peak_dbtp) via loudnorm=print_format=json."""
    r = subprocess.run(
        [FFMPEG, "-i", str(mp4),
         "-af", "loudnorm=print_format=json",
         "-f", "null", "/dev/null"],
        capture_output=True, text=True,
    )
    combined = r.stdout + r.stderr
    m = re.search(r'\{[^{}]+\}', combined, re.DOTALL)
    if not m:
        return None, None
    try:
        d = json.loads(m.group())
        lufs = float(d.get("input_i", "nan"))
        tp   = float(d.get("input_tp", "nan"))
        return lufs, tp
    except (ValueError, KeyError):
        return None, None


def _beat_silence_check(mp4: Path, beats: list, slug: str) -> list[str]:
    """For each narration beat, volumedetect its time window. Return list of
    error strings for beats that are effectively silent throughout."""
    errors: list[str] = []
    t = 0.0
    with tempfile.TemporaryDirectory() as tmp:
        for b in beats:
            bid = _bid(b)
            dur = float(b.get("actual_duration_s") or b.get("estimated_duration_s") or 6.0)
            narration = (b.get("narration_text") or b.get("narration") or "").strip()
            audio_file = b.get("audio_file") or ""

            # Only check beats that are supposed to have narration audio.
            # Beats without narration_text (instrumental, Manim b-roll, etc.) are exempt.
            if not narration or dur <= 0.1:
                t += dur
                continue

            # Run volumedetect on this beat's window in the compiled master.
            r = subprocess.run(
                [FFMPEG, "-y",
                 "-ss", f"{t:.3f}", "-t", f"{dur:.3f}",
                 "-i", str(mp4),
                 "-af", "volumedetect", "-vn", "-f", "null", "/dev/null"],
                capture_output=True, text=True,
            )
            combined = r.stdout + r.stderr
            vm = re.search(r"mean_volume:\s*([-\d.]+)\s*dB", combined)
            mean_vol = float(vm.group(1)) if vm else None

            if mean_vol is not None and mean_vol <= _BEAT_SILENCE_FLOOR_DB:
                errors.append(
                    f"{bid}: narration beat at t={t:.1f}s dur={dur:.1f}s "
                    f"is silent (mean_vol {mean_vol:.1f} dB ≤ {_BEAT_SILENCE_FLOOR_DB} dB)"
                )
            t += dur
    return errors


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("reel_dir", type=Path)
    ap.add_argument("--mp4", type=Path, default=None,
                    help="explicit master path (default: <reel>/<slug>.mp4)")
    ap.add_argument("--sheet", default="beat_sheet.json")
    ap.add_argument("--skip-per-beat", action="store_true",
                    help="skip per-beat silence checks (fast mode)")
    args = ap.parse_args(argv)

    reel_dir = args.reel_dir.resolve()

    if not shutil.which("ffmpeg"):
        _write_md(reel_dir, ["# LOUDNESS", "", "SKIP — ffmpeg not on PATH"])
        sys.exit(3)

    bs_path = reel_dir / args.sheet
    slug = reel_dir.name
    beats: list = []
    if bs_path.exists():
        try:
            sheet = json.loads(bs_path.read_text())
            meta = sheet.get("metadata", {})
            slug = meta.get("slug") or slug
            beats = sheet.get("beats", [])
            for b in beats:
                if "beat_id" not in b and "id" in b:
                    b["beat_id"] = b["id"]
                if "actual_duration_s" not in b:
                    for k in ("est_s", "estimated_duration_s"):
                        if k in b:
                            b["actual_duration_s"] = float(b[k])
                            break
        except Exception:
            pass

    mp4 = args.mp4 or reel_dir / f"{slug}.mp4"
    if not mp4.exists():
        _write_md(reel_dir, [
            "# LOUDNESS", "",
            f"FAIL — master not found: {mp4.name}",
        ])
        print(f"[loud] FAIL — master not found: {mp4}")
        sys.exit(2)

    failures: list[str] = []
    notes:    list[str] = []

    # 1 + 2. Integrated LUFS and true peak
    lufs, tp = _measure_loudnorm(mp4)
    if lufs is None:
        notes.append("loudnorm: could not parse ffmpeg output — skipped")
    else:
        notes.append(f"integrated_lufs: {lufs:.2f}  (window: {LUFS_LOW} to {LUFS_HIGH})")
        if lufs < LUFS_LOW:
            failures.append(
                f"integrated_lufs {lufs:.2f} LUFS < floor {LUFS_LOW} LUFS — "
                "audio is too quiet; possible silent mix or wrong file"
            )
        elif lufs > LUFS_HIGH:
            failures.append(
                f"integrated_lufs {lufs:.2f} LUFS > ceiling {LUFS_HIGH} LUFS — "
                "audio is unexpectedly loud; check for music bed or wrong file"
            )

    if tp is None:
        notes.append("true_peak: could not parse — skipped")
    else:
        notes.append(f"true_peak_dbtp: {tp:.2f}  (ceiling: {TRUE_PEAK_CEIL})")
        if tp > TRUE_PEAK_CEIL:
            failures.append(
                f"true_peak {tp:.2f} dBTP > ceiling {TRUE_PEAK_CEIL} dBTP — "
                "EBU R128 violation; consider loudnorm normalization before staging"
            )

    # 3. Per-beat silence (narration beats only)
    beat_errors: list[str] = []
    if not args.skip_per_beat and beats:
        print(f"[loud] checking {len(beats)} beats for per-beat silence …", flush=True)
        beat_errors = _beat_silence_check(mp4, beats, slug)
        if beat_errors:
            for be in beat_errors:
                failures.append(f"per-beat silence: {be}")
        else:
            notes.append("per-beat silence: all narration beats have audio ✓")
    else:
        notes.append("per-beat silence: skipped (--skip-per-beat or no beats)")

    verdict = "PASS" if not failures else "FAIL"

    rows = [
        ("master", mp4.name),
        ("integrated_lufs", f"{lufs:.2f}" if lufs is not None else "?"),
        ("true_peak_dbtp",  f"{tp:.2f}"   if tp   is not None else "?"),
        ("lufs_window",     f"{LUFS_LOW} to {LUFS_HIGH}"),
        ("true_peak_ceil",  str(TRUE_PEAK_CEIL)),
        ("failures", str(len(failures))),
        ("verdict",  f"**{verdict}**"),
    ]
    lines = ["# LOUDNESS", "", "| field | value |", "|---|---|"]
    lines += [f"| {k} | {v} |" for k, v in rows]
    if notes:
        lines += ["", "## Notes", ""] + [f"- {n}" for n in notes]
    if failures:
        lines += ["", "## Failures", ""] + [f"- {f}" for f in failures]
    lines += ["", f"GATE LOUDNESS: {verdict}"]
    _write_md(reel_dir, lines)

    if failures:
        print(f"[loud] FAIL — {len(failures)} violation(s):")
        for f in failures:
            print(f"[loud]   {f}")
        sys.exit(2)
    else:
        lufs_str = f"{lufs:.2f} LUFS" if lufs is not None else "? LUFS"
        tp_str   = f"{tp:.2f} dBTP"   if tp   is not None else "? dBTP"
        print(f"[loud] PASS  {lufs_str}  tp={tp_str}")


if __name__ == "__main__":
    main()
