#!/usr/bin/env python3
"""
render_bookends.py — render the Medhavy Remotion intro/outro and lay narration on them.

Reads beat_sheet.json, and for each Remotion beat (B00 MedhavyOpen, B99 MedhavyOutro):
  1. renders the silent Remotion composition with the beat's props, then
  2. muxes the beat's narration (mp3/beat-<ID>.mp3) onto it, freezing the
     last frame if the narration runs longer than the composition so nothing clips.

Output: <folder>/media/B00.mp4 and <folder>/media/B99.mp4 (video + voice).

Prereq: run generate_audio_kokoro.py <folder> --only B00 B99  first (writes the mp3s).
Requires: the Medhavy Remotion project (src/index.ts with MedhavyOpen/MedhavyOutro),
          node/npx, ffmpeg/ffprobe.

Usage:
    python render_bookends.py <folder> --remotion-dir path/to/remotion-pass/remotion
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path


def run(cmd, cwd=None):
    print("[cmd]", " ".join(str(c) for c in cmd))
    subprocess.run(cmd, check=True, cwd=cwd)


def dur(path: Path) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nk=1:nw=1", str(path)],
        capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


def render_beat(beat, folder: Path, remotion_dir: Path, entry: str):
    rem = beat["shot"]["remotion"]
    pattern = rem["pattern"]                     # MedhavyOpen | MedhavyOutro
    props = rem.get("props", {})
    media = folder / "media"
    media.mkdir(exist_ok=True)
    silent = media / f"{beat['beat_id']}_silent.mp4"
    final = folder / rem["rendered"]["out"]      # media/B00.mp4
    final.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(props, f)
        props_file = f.name

    # Remotion 4.x: npx remotion render <entry> <CompId> <out> --props=<file>
    run(["npx", "--no-install", "remotion", "render", entry, pattern,
         str(silent.resolve()), f"--props={props_file}"], cwd=str(remotion_dir))

    audio = folder / (beat.get("audio_file") or f"mp3/beat-{beat['beat_id']}.mp3")
    if not audio.exists():
        print(f"[bookends] WARN no narration {audio}; leaving silent render for {beat['beat_id']}")
        silent.replace(final)
        return final

    vlen, alen = dur(silent), dur(audio)
    tail = max(0.0, alen - vlen + 0.3)           # hold last frame to cover the voice
    vf = f"[0:v]tpad=stop_mode=clone:stop_duration={tail}[v]"
    run(["ffmpeg", "-y", "-i", str(silent), "-i", str(audio),
         "-filter_complex", vf, "-map", "[v]", "-map", "1:a:0",
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "medium",
         "-c:a", "aac", "-b:a", "192k", "-shortest", str(final)])
    print(f"[bookends] {beat['beat_id']} → {final}  (video {vlen:.1f}s + voice {alen:.1f}s)")
    return final


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("folder")
    ap.add_argument("--remotion-dir", required=True,
                    help="the Medhavy Remotion project dir (contains src/index.ts)")
    ap.add_argument("--entry", default="src/index.ts")
    args = ap.parse_args()

    folder = Path(args.folder).expanduser().resolve()
    remotion_dir = Path(args.remotion_dir).expanduser().resolve()
    if not (remotion_dir / args.entry).exists():
        sys.exit(f"[bookends] no Remotion entry at {remotion_dir/args.entry}")

    sheet = json.loads((folder / "beat_sheet.json").read_text())
    for beat in sheet["beats"]:
        if beat.get("shot", {}).get("source") == "remotion":
            render_beat(beat, folder, remotion_dir, args.entry)
    print("[bookends] done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
