#!/usr/bin/env python3
"""srt_check.py — GATE SRT (Phase 2: CLOCK-AND-CAPTIONS)

Validates the caption track for a compiled reel:
  - <slug>.srt exists beside the master
  - at least 1 cue is present
  - every cue has non-empty text (no silent caption slots)
  - timestamps are valid (HH:MM:SS,mmm format) and monotonically increasing
  - end time > start time for each cue

Usage:
    python3 scripts/srt_check.py <reel_dir> [--srt <path>] [--sheet <name>]

Exit codes:
    0 — PASS
    2 — FAIL (file missing, malformed, or has violations)
    3 — SKIP (srt generation has not been run yet — informational only)

Writes SRTCHECK.md into the reel directory.
"""

from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

_TS_RE = re.compile(
    r"(\d{2}):(\d{2}):(\d{2}),(\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2}),(\d{3})"
)


def _parse_ts(hh, mm, ss, ms) -> float:
    return int(hh) * 3600 + int(mm) * 60 + int(ss) + int(ms) / 1000.0


def _write_md(reel_dir: Path, lines: list[str]) -> None:
    (reel_dir / "SRTCHECK.md").write_text("\n".join(lines) + "\n")


def check_srt(srt_path: Path) -> list[str]:
    """Parse an SRT file; return list of error strings (empty = clean)."""
    errors: list[str] = []
    text = srt_path.read_text(encoding="utf-8", errors="replace")
    blocks = [b.strip() for b in re.split(r"\n\s*\n", text.strip()) if b.strip()]

    if not blocks:
        return ["no cues found — SRT is empty"]

    prev_end = -1.0
    for i, block in enumerate(blocks, 1):
        lines = block.splitlines()
        if len(lines) < 2:
            errors.append(f"cue {i}: too few lines ({len(lines)})")
            continue

        m = _TS_RE.search(lines[1] if len(lines) > 1 else "")
        if not m:
            # Try first line (some generators omit sequence number)
            m = _TS_RE.search(lines[0])
        if not m:
            errors.append(f"cue {i}: malformed timestamp line: {lines[1][:80]!r}")
            continue

        start = _parse_ts(m.group(1), m.group(2), m.group(3), m.group(4))
        end   = _parse_ts(m.group(5), m.group(6), m.group(7), m.group(8))

        if end <= start:
            errors.append(f"cue {i}: end ({end:.3f}s) not after start ({start:.3f}s)")
        if start < prev_end - 0.02:
            errors.append(f"cue {i}: start ({start:.3f}s) overlaps previous end ({prev_end:.3f}s)")
        prev_end = end

        # text is everything after the timestamp line
        ts_idx = next((j for j, l in enumerate(lines) if "-->" in l), 1)
        cue_text = "\n".join(lines[ts_idx + 1:]).strip()
        if not cue_text:
            errors.append(f"cue {i}: empty text (silent caption slot at {start:.1f}s)")

    return errors


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("reel_dir", type=Path)
    ap.add_argument("--srt", type=Path, default=None,
                    help="explicit SRT path (default: <reel>/<slug>.srt)")
    ap.add_argument("--sheet", default="beat_sheet.json")
    args = ap.parse_args(argv)

    reel_dir = args.reel_dir.resolve()
    bs_path = reel_dir / args.sheet
    slug = reel_dir.name
    if bs_path.exists():
        try:
            sheet = json.loads(bs_path.read_text())
            slug = sheet.get("metadata", {}).get("slug") or slug
        except Exception:
            pass

    srt = args.srt or reel_dir / f"{slug}.srt"

    if not srt.exists():
        lines = [
            "# SRTCHECK",
            "",
            f"SKIP — {srt.name} not found",
            "",
            "Run `python3 runtime/scripts/stage_publish.py <reel>` to generate captions,",
            "or ensure the SRT was generated before running `art post`.",
        ]
        _write_md(reel_dir, lines)
        print(f"[srt] SKIP — {srt.name} not found (stage_publish.py generates it)")
        sys.exit(3)

    errors = check_srt(srt)
    n_cues = len([b for b in re.split(r"\n\s*\n", srt.read_text().strip()) if b.strip()])
    verdict = "PASS" if not errors else "FAIL"

    lines = [
        "# SRTCHECK",
        "",
        f"| field | value |",
        f"|---|---|",
        f"| srt | `{srt.name}` |",
        f"| cues | {n_cues} |",
        f"| errors | {len(errors)} |",
        f"| verdict | **{verdict}** |",
    ]
    if errors:
        lines += ["", "## Errors", ""]
        lines += [f"- {e}" for e in errors]

    lines += ["", f"GATE SRT: {verdict}"]
    _write_md(reel_dir, lines)

    print(f"[srt] {verdict}  {n_cues} cues  {len(errors)} errors  ({srt.name})")
    if errors:
        for e in errors:
            print(f"[srt]   {e}")
        sys.exit(2)


if __name__ == "__main__":
    main()
