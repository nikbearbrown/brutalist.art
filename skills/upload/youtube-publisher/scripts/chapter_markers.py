#!/usr/bin/env python3
"""
chapter_markers.py — propose YouTube chapter timestamps from a transcript.

YouTube chapters need: a marker at 0:00, at least three markers, each ≥10s apart,
in ascending order. This script proposes markers at natural topic boundaries
(pauses between transcript segments, spaced at least --min-gap seconds apart) and —
crucially — offsets every timestamp by the intro's real duration, because the intro
beat is prepended to the final video and pushes the NotebookLM body later.

The labels it emits are SNIPPET GUESSES (first words after each boundary). They are
placeholders: a human/agent rewrites them into real topic titles before upload.

Output: <folder>/chapters.json
  [{"seconds": 0,  "t": "0:00", "label": "Intro", "snippet": ""},
   {"seconds": 27, "t": "0:27", "label": "<rewrite me>", "snippet": "first words…"}, …]

Usage:
    python chapter_markers.py <folder> --transcript path/to/Video.transcript.json
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def hhmmss(sec: float) -> str:
    sec = int(round(sec))
    h, rem = divmod(sec, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def intro_duration(folder: Path) -> float:
    """Real intro length: prefer mp3/timings.json (ground truth), else the beat sheet's
    B00 actual_duration_s, else its estimate. The whole body shifts by this much."""
    sheet = json.loads((folder / "beat_sheet.json").read_text())
    b00 = next((b for b in sheet["beats"] if b["beat_id"] == "B00"), None)
    timings = folder / "mp3" / "timings.json"
    if timings.exists():
        data = json.loads(timings.read_text())
        for k in ("B00", "beat-B00", "INTRO"):
            if k in data:
                return float(data[k])
    if b00:
        return float(b00.get("actual_duration_s") or b00.get("estimated_duration_s") or 11.0)
    return 11.0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("folder")
    ap.add_argument("--transcript", required=True)
    ap.add_argument("--min-gap", type=float, default=45.0,
                    help="minimum seconds between chapter markers (default 45)")
    ap.add_argument("--snippet-words", type=int, default=9)
    args = ap.parse_args()

    folder = Path(args.folder).expanduser().resolve()
    tr = json.loads(Path(args.transcript).read_text())
    segs = tr["segments"]
    offset = intro_duration(folder)

    markers = [{"seconds": 0, "t": "0:00", "label": "Intro", "snippet": ""}]
    last = 0.0
    # first real marker = start of the NotebookLM body
    body_start = offset
    markers.append({
        "seconds": int(round(body_start)), "t": hhmmss(body_start),
        "label": "<rewrite me>",
        "snippet": " ".join(segs[0]["text"].split()[:args.snippet_words]) if segs else "",
    })
    last = body_start

    for i, s in enumerate(segs):
        t = s["start"] + offset
        # boundary candidate: a real pause before this segment and enough spacing
        prev_end = segs[i - 1]["end"] + offset if i else body_start
        pause = t - prev_end
        if t - last >= args.min_gap and (pause >= 0.6 or i == 0):
            markers.append({
                "seconds": int(round(t)), "t": hhmmss(t),
                "label": "<rewrite me>",
                "snippet": " ".join(s["text"].split()[:args.snippet_words]),
            })
            last = t

    # de-dup identical seconds, keep ascending
    seen, clean = set(), []
    for m in markers:
        if m["seconds"] in seen:
            continue
        seen.add(m["seconds"])
        clean.append(m)

    out = folder / "chapters.json"
    out.write_text(json.dumps(clean, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"[markers] intro offset = {offset:.1f}s; {len(clean)} markers → {out}")
    for m in clean:
        print(f"  {m['t']:>7}  {m['label']}   {m['snippet']}")
    if len(clean) < 3:
        print("[markers] NOTE: fewer than 3 markers — YouTube needs ≥3 to show chapters. "
              "Lower --min-gap or add markers by hand.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
