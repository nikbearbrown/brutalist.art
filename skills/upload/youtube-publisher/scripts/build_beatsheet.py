#!/usr/bin/env python3
"""
build_beatsheet.py — assemble the beat_sheet.json for a NotebookLM sandwich video.

The NotebookLM .mp4 already IS the body of the video (it has its own narration and
visuals). This skill only adds a Medhavy Remotion intro beat (B00) and outro beat
(B99) that bookend it — brand stamp in, subscribe/brand out. So the beat sheet has
exactly three beats:

  B00  MEDHAVY INTRO   Remotion MedhavyOpen  + Kokoro narration (spoken)
  B50  NOTEBOOKLM      the raw .mp4, used as-is (its own audio, NO TTS)
  B99  MEDHAVY OUTRO   Remotion MedhavyOutro + Kokoro narration (spoken)

Only B00 and B99 get TTS — run generate_audio_kokoro.py with `--only B00 B99`. B50 is
never sent to TTS; sandwich.py drops the real .mp4 in that slot with its
original audio intact.

Usage:
    python build_beatsheet.py <video.mp4> \
        --chapter path/to/05-the-infinite-square-well.md \
        --title "Deriving the Infinite Square Well" \
        [--out-dir path/to/folder]     # default: <video-dir>/<slug>/
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

BOOK_TITLE = "Quantum Mechanics, Volume One"


def slugify(s: str) -> str:
    s = re.sub(r"[^\w\s-]", "", s.lower()).strip()
    return re.sub(r"[\s_]+", "-", s)


def probe_duration(mp4: Path) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nk=1:nw=1", str(mp4)],
        capture_output=True, text=True)
    try:
        return round(float(r.stdout.strip()), 2)
    except ValueError:
        return 0.0


def chapter_meta(chapter: Path) -> tuple[int | None, str, str]:
    """Return (number, short_title, hook). short_title strips the 'Chapter N — ' prefix.
    hook = the first non-heading, non-empty paragraph of the chapter (a ready first
    line for the intro narration and the description)."""
    num = None
    m = re.match(r"(\d+)", chapter.stem)
    if m:
        num = int(m.group(1))
    title = chapter.stem
    hook = ""
    lines = chapter.read_text(encoding="utf-8", errors="ignore").splitlines()
    for line in lines:
        if line.startswith("# "):
            title = line[2:].strip()
            break
    short = re.sub(r"^Chapter\s+\d+\s*[—:-]\s*", "", title).strip()
    for line in lines:
        s = line.strip()
        if s and not s.startswith(("#", "!", "|", "-", "*", ">", "`")):
            hook = s
            break
    return num, short, hook


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("video")
    ap.add_argument("--chapter", required=True, help="matched chapter .md")
    ap.add_argument("--title", required=True, help="human video title (becomes the YouTube title)")
    ap.add_argument("--out-dir", default=None)
    ap.add_argument("--book-title", default=BOOK_TITLE)
    ap.add_argument("--playlist", default="Quantum Mechanics Volume 1 (NotebookLM)")
    args = ap.parse_args()

    video = Path(args.video).expanduser().resolve()
    if not video.exists():
        sys.exit(f"[beatsheet] no such video: {video}")
    chapter = Path(args.chapter).expanduser().resolve()
    num, short_title, hook = chapter_meta(chapter)

    slug = slugify(args.title)
    out_dir = Path(args.out_dir).expanduser().resolve() if args.out_dir else video.parent / slug
    out_dir.mkdir(parents=True, exist_ok=True)

    nb_duration = probe_duration(video)

    # Intro narration introduces THIS video, then hands to the deep dive.
    ch_phrase = f"Chapter {num}" if num else "this chapter"
    intro_narration = (
        f"Medhavy A-I — intelligent learning systems. "
        f"In this deep dive, we unpack {short_title}, {ch_phrase} of {args.book_title}. "
        f"Let's get into it."
    )
    outro_narration = (
        "That was a Medhavy deep dive. "
        "Medhavy — A-I-powered intelligent learning systems. "
        "On YouTube at Medhavy A-I. Medhavy dot com. Subscribe for the next chapter."
    )

    sheet = {
        "metadata": {
            "title": args.title,
            "slug": slug,
            "topic": short_title,
            "audience": "MEDHAVY",
            "voice_kokoro": "am_onyx",
            "voice": "MEDHAVY",
            "register": "Wonder",
            "palette": "medhavy",
            "style_preset": "medhavy",
            "source_chapter": str(chapter.relative_to(chapter.parents[1]))
                if len(chapter.parents) >= 2 else chapter.name,
            "chapter_number": num,
            "chapter_title": short_title,
            "book_title": args.book_title,
            "playlist": args.playlist,
            "notebooklm_video": str(video),
            "notebooklm_duration_s": nb_duration,
            "note": "B00/B99 are Medhavy Remotion bookends with TTS; B50 is the raw "
                    "NotebookLM mp4 used as-is. Run generate_audio_kokoro.py --only B00 B99.",
        },
        "beats": [
            {
                "beat_id": "B00",
                "act": "MEDHAVY INTRO",
                "narration_text": intro_narration,
                "shot": {
                    "type": "GRAPHIC", "source": "remotion", "motion": "fade",
                    "remotion": {
                        "pattern": "MedhavyOpen", "provenance": "reel-local", "version": "1",
                        "props": {
                            "topic": short_title.upper(),
                            "lines": [
                                "Medhavy AI",
                                f"{args.book_title} — {ch_phrase}",
                                short_title,
                                "A NotebookLM deep dive.",
                            ],
                        },
                        "rendered": {"out": "media/B00.mp4", "at": ""},
                    },
                },
                "estimated_duration_s": 11.0,
                "audio_file": "mp3/beat-B00.mp3",
            },
            {
                "beat_id": "B50",
                "act": "NOTEBOOKLM",
                "narration_text": None,
                "raw_video": str(video),
                "shot": {"type": "RAW", "source": "notebooklm", "motion": "none"},
                "estimated_duration_s": nb_duration,
            },
            {
                "beat_id": "B99",
                "act": "MEDHAVY OUTRO",
                "narration_text": outro_narration,
                "shot": {
                    "type": "GRAPHIC", "source": "remotion", "motion": "fade",
                    "remotion": {
                        "pattern": "MedhavyOutro", "provenance": "reel-local", "version": "1",
                        "props": {
                            "brand": "Medhavy",
                            "tagline": "AI-powered intelligent learning systems",
                            "handle": "@MedhavyAI",
                            "url": "medhavy.com",
                        },
                        "rendered": {"out": "media/B99.mp4", "at": ""},
                    },
                },
                "estimated_duration_s": 9.0,
                "audio_file": "mp3/beat-B99.mp3",
            },
        ],
    }

    out = out_dir / "beat_sheet.json"
    out.write_text(json.dumps(sheet, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"[beatsheet] chapter {num}: {short_title}")
    print(f"[beatsheet] NotebookLM body = {nb_duration:.1f}s")
    print(f"[beatsheet] wrote {out}")
    print(f"[beatsheet] folder = {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
