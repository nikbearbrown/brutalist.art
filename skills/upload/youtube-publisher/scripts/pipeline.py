#!/usr/bin/env python3
"""
pipeline.py — build ONE NotebookLM sandwich video, end to end (everything except upload).

Runs, in order:
  1. transcribe.py        NotebookLM mp4 → <name>.transcript.json
  2. match_chapter.py     rank chapters; pick best (or --chapter override)
  3. build_beatsheet.py   write the folder + beat_sheet.json (B00/B50/B99)
  4. generate_audio_kokoro.py    Kokoro am_onyx TTS for B00 + B99 only
  5. render_bookends.py   Remotion MedhavyOpen/Outro + narration → media/B00,B99.mp4
  6. sandwich.py          intro + NotebookLM + outro → mp4/<slug>.mp4
  7. chapter_markers.py   propose timestamped chapters (offset by intro length)
  8. build_description.py YouTube description draft (house style)

Then a human refines the description labels + hook and runs
build_description.py --refresh, and finally publish_playlist.py to post.

Paths to the two REUSED tools default to their location in this repo; override with
flags or env vars (MEDHAVY_SCRIPTS_DIR, MEDHAVY_REMOTION_DIR) if the layout differs.

Usage:
    python pipeline.py path/to/Video.mp4 --chapters path/to/chapters
    python pipeline.py path/to/Video.mp4 --chapters ../chapters --title "Custom Title"
    python pipeline.py path/to/Video.mp4 --chapters ../chapters --chapter ../chapters/05-*.md
    python pipeline.py path/to/Video.mp4 --chapters ../chapters --skip-transcribe   # reuse json
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
# Reused tooling — defaults assume the bear-textbooks repo layout.
REPO = HERE.parents[2] if len(HERE.parents) >= 3 else HERE
DEFAULT_SCRIPTS = os.environ.get(
    "MEDHAVY_SCRIPTS_DIR",
    str(REPO / "skills/make/sketch-explainer/scripts"))
DEFAULT_REMOTION = os.environ.get(
    "MEDHAVY_REMOTION_DIR",
    str(REPO / "runtime/remotion"))


def sh(cmd: list[str]) -> None:
    print("\n$", " ".join(str(c) for c in cmd))
    subprocess.run([str(c) for c in cmd], check=True)


def title_from_filename(mp4: Path) -> str:
    name = mp4.stem.replace("_", " ")
    name = re.sub(r"\s+", " ", name).strip(" -–—")
    return name


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("video")
    ap.add_argument("--chapters", required=True, help="chapter dir for matching")
    ap.add_argument("--chapter", default=None, help="force a specific chapter .md (skip auto-match)")
    ap.add_argument("--title", default=None, help="YouTube title (default: from filename)")
    ap.add_argument("--model", default="small", help="whisper model size")
    ap.add_argument("--scripts-dir", default=DEFAULT_SCRIPTS, help="dir with generate_audio.py")
    ap.add_argument("--remotion-dir", default=DEFAULT_REMOTION)
    ap.add_argument("--skip-transcribe", action="store_true", help="reuse existing .transcript.json")
    ap.add_argument("--skip-audio", action="store_true", help="skip TTS + bookends + sandwich (draft only)")
    args = ap.parse_args()

    video = Path(args.video).expanduser().resolve()
    py = sys.executable
    transcript = video.with_suffix("").with_suffix(".transcript.json") \
        if video.suffix else Path(str(video) + ".transcript.json")
    transcript = Path(str(video.with_suffix("")) + ".transcript.json")

    # 1. transcribe
    if not args.skip_transcribe or not transcript.exists():
        sh([py, HERE / "transcribe.py", video, "--model", args.model])

    # 2. match chapter (unless forced)
    chapter = args.chapter
    if not chapter:
        out = subprocess.run(
            [py, str(HERE / "match_chapter.py"), str(transcript),
             "--chapters", args.chapters, "--json"],
            check=True, capture_output=True, text=True).stdout
        best = json.loads(out)["best"]
        chapter = str(Path(args.chapters).expanduser().resolve() / best["file"])
        print(f"\n[pipeline] auto-matched → ch{best['number']} {best['title']} "
              f"(score {best['score']}). Override with --chapter if wrong.")

    title = args.title or title_from_filename(video)

    # 3. beat sheet — capture stdout to extract the exact folder path it created
    result = subprocess.run(
        [str(py), str(HERE / "build_beatsheet.py"), str(video),
         "--chapter", chapter, "--title", title],
        check=True, capture_output=False, text=True,
        stdout=subprocess.PIPE, stderr=None)
    print(result.stdout, end="")
    folder_line = next(
        (l for l in result.stdout.splitlines() if l.startswith("[beatsheet] folder = ")),
        None)
    if folder_line is None:
        sys.exit("[pipeline] could not parse folder from build_beatsheet output")
    folder = Path(folder_line.split(" = ", 1)[1].strip())

    if not args.skip_audio:
        # 4. TTS for bookends only
        sh([py, Path(args.scripts_dir) / "generate_audio.py", folder, "--only", "B00", "B99"])
        # 5. render Remotion bookends + narration
        sh([py, HERE / "render_bookends.py", folder, "--remotion-dir", args.remotion_dir])
        # 6. sandwich
        sh([py, HERE / "sandwich.py", folder])

    # 7. chapter markers
    sh([py, HERE / "chapter_markers.py", folder, "--transcript", transcript])
    # 8. description draft
    sh([py, HERE / "build_description.py", folder, "--chapter", chapter])

    print(f"\n[pipeline] DONE → {folder}")
    print("[pipeline] Next: edit chapters.json labels + the -youtube.md hook, then:")
    print(f"           python {HERE/'build_description.py'} {folder} --refresh")
    print("           python publish_playlist.py --root <parent-of-folders>")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
