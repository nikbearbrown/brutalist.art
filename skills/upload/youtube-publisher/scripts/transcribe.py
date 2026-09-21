#!/usr/bin/env python3
"""
transcribe.py — Whisper transcript (with timestamps) for a NotebookLM .mp4.

Extracts the audio with ffmpeg, runs faster-whisper, and writes two files next
to the source video:

  <name>.transcript.json   {"video": "...mp4", "duration_s": 512.3,
                            "segments": [{"start": 0.0, "end": 4.2, "text": "..."}, ...],
                            "text": "full transcript ..."}
  <name>.transcript.txt    plain full transcript

The JSON segments are GROUND TRUTH for two later steps: chapter-marker
timestamps in the YouTube description, and matching the video to a book chapter.

Requires:  pip install faster-whisper   (and ffmpeg on PATH)

Usage:
    python transcribe.py path/to/Video.mp4
    python transcribe.py path/to/Video.mp4 --model small --language en
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path


def extract_audio(mp4: Path, wav: Path) -> None:
    # 16 kHz mono is what Whisper wants; keeps the temp file tiny.
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(mp4), "-vn", "-ac", "1", "-ar", "16000",
         "-f", "wav", str(wav)],
        check=True, capture_output=True,
    )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("video", help="path to the NotebookLM .mp4")
    ap.add_argument("--model", default="small",
                    help="faster-whisper model size (tiny|base|small|medium|large-v3). "
                         "small is a good speed/quality balance for clear narration.")
    ap.add_argument("--language", default="en", help="force a language (default en)")
    ap.add_argument("--compute-type", default="int8",
                    help="int8 (CPU, fast) | float16 (GPU) | float32")
    args = ap.parse_args()

    mp4 = Path(args.video).expanduser().resolve()
    if not mp4.exists():
        sys.exit(f"[transcribe] no such file: {mp4}")

    stem = mp4.with_suffix("")  # drop .mp4
    out_json = Path(f"{stem}.transcript.json")
    out_txt = Path(f"{stem}.transcript.txt")

    try:
        from faster_whisper import WhisperModel
    except ImportError:
        sys.exit("[transcribe] missing dependency: pip install faster-whisper")

    with tempfile.TemporaryDirectory() as td:
        wav = Path(td) / "audio.wav"
        print(f"[transcribe] extracting audio → {wav.name}")
        extract_audio(mp4, wav)

        print(f"[transcribe] loading model '{args.model}' ({args.compute_type})…")
        model = WhisperModel(args.model, device="cpu", compute_type=args.compute_type)

        print("[transcribe] transcribing (this can take a few minutes)…")
        segments, info = model.transcribe(
            str(wav), language=args.language, vad_filter=True,
            vad_parameters=dict(min_silence_duration_ms=500),
        )

        segs = []
        pieces = []
        for s in segments:
            text = s.text.strip()
            if not text:
                continue
            segs.append({"start": round(s.start, 2), "end": round(s.end, 2), "text": text})
            pieces.append(text)
            # live progress so a long file doesn't look hung
            print(f"  [{s.start:7.1f}s] {text[:80]}")

    duration = round(segs[-1]["end"], 2) if segs else round(getattr(info, "duration", 0.0), 2)
    full = " ".join(pieces)

    out_json.write_text(json.dumps(
        {"video": mp4.name, "duration_s": duration, "language": args.language,
         "segments": segs, "text": full},
        ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    out_txt.write_text(full + "\n", encoding="utf-8")

    print(f"\n[transcribe] {len(segs)} segments, {duration:.1f}s")
    print(f"[transcribe] wrote {out_json.name} and {out_txt.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
