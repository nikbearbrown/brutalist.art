#!/usr/bin/env python3
"""
sandwich.py — concatenate the Medhavy intro, the NotebookLM body, and the outro.

Order is taken straight from beat_sheet.json:
  B00 media/B00.mp4   (Remotion intro + voice)
  B50 raw_video       (the NotebookLM .mp4, audio kept as-is)
  B99 media/B99.mp4   (Remotion outro + voice)

Because the three clips come from different sources (Remotion vs NotebookLM) they
almost never share codec/resolution/fps/audio layout, and ffmpeg's concat demuxer
silently corrupts output when they differ. So each segment is first re-encoded to
ONE canonical format (1920x1080 @ 30fps, h264/yuv420p, AAC 48k stereo, scaled +
letterboxed to fit), then concatenated. Slower than a stream copy, but correct.

Output: <folder>/mp4/<slug>.mp4   (the upload master)

Usage:
    python sandwich.py <folder> [--width 1920 --height 1080 --fps 30]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path


def run(cmd):
    print("[ffmpeg]", " ".join(str(c) for c in cmd))
    subprocess.run(cmd, check=True)


def normalize(src: Path, dst: Path, w: int, h: int, fps: int):
    """Scale to fit inside WxH, pad (letterbox) to exactly WxH, force fps + canonical
    audio. Guarantees every segment is byte-compatible for concat."""
    vf = (f"scale={w}:{h}:force_original_aspect_ratio=decrease,"
          f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:color=0x0B1020,fps={fps},setsar=1")
    run(["ffmpeg", "-y", "-i", str(src),
         "-vf", vf, "-r", str(fps),
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "19", "-preset", "medium",
         "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
         "-af", "aresample=async=1:first_pts=0",
         str(dst)])


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("folder")
    ap.add_argument("--width", type=int, default=1920)
    ap.add_argument("--height", type=int, default=1080)
    ap.add_argument("--fps", type=int, default=30)
    args = ap.parse_args()

    folder = Path(args.folder).expanduser().resolve()
    sheet = json.loads((folder / "beat_sheet.json").read_text())
    slug = sheet["metadata"]["slug"]

    # Resolve each beat to a concrete source file, in beat order.
    sources = []
    for b in sheet["beats"]:
        if b.get("raw_video"):
            p = Path(b["raw_video"]).expanduser()
        else:
            p = folder / b["shot"]["remotion"]["rendered"]["out"]
        if not p.exists():
            sys.exit(f"[sandwich] missing segment for {b['beat_id']}: {p}")
        sources.append((b["beat_id"], p))

    out_dir = folder / "mp4"
    out_dir.mkdir(exist_ok=True)
    final = out_dir / f"{slug}.mp4"

    with tempfile.TemporaryDirectory() as td:
        norm_paths = []
        for bid, src in sources:
            dst = Path(td) / f"{bid}.mp4"
            print(f"[sandwich] normalizing {bid}: {src.name}")
            normalize(src, dst, args.width, args.height, args.fps)
            norm_paths.append(dst)

        listfile = Path(td) / "concat.txt"
        listfile.write_text("\n".join(f"file '{p}'" for p in norm_paths))
        run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(listfile),
             "-c", "copy", str(final)])

    print(f"[sandwich] master → {final}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
