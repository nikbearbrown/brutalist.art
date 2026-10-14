#!/usr/bin/env python3
"""setup_smoke_whisper.py — setup's captions gate.

Writes a one-second 440 Hz test tone with ffmpeg and decodes it through
faster-whisper's own file loader (faster_whisper.audio.decode_audio, the path
every transcription takes). Exit 0 only if that returns about one second of
non-silent 16 kHz audio — not just "the import worked." No model is loaded,
so nothing is downloaded. Catches av/faster-whisper breaks such as av 19
dropping av.open(metadata_errors=...).
Prints one stderr line on success/failure; setup's check() discards output
either way and reports its own MISS message.
"""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SR = 16000


def fail(msg: str) -> int:
    print(f"[smoke] {msg}", file=sys.stderr)
    return 1


def main() -> int:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        return fail("ffmpeg not on PATH")
    try:
        from faster_whisper.audio import decode_audio
    except ImportError:
        return fail("faster_whisper not importable")

    fd, wav_path = tempfile.mkstemp(suffix=".wav")
    os.close(fd)
    try:
        out = subprocess.run([ffmpeg, "-loglevel", "error", "-y", "-f", "lavfi",
                              "-i", "sine=frequency=440:duration=1", "-ac", "1",
                              "-ar", str(SR), wav_path], capture_output=True, text=True)
        if out.returncode != 0:
            return fail(f"ffmpeg could not write the test tone: {out.stderr.strip()}")
        try:
            audio = decode_audio(wav_path, sampling_rate=SR)
        except Exception as e:
            return fail(f"faster-whisper could not decode a WAV file: {e!r}")
        seconds = len(audio) / SR
        peak = float(abs(audio).max()) if len(audio) else 0.0
        if not 0.9 <= seconds <= 1.1:
            return fail(f"decoded {seconds:.2f} s of audio from a 1 s tone")
        if peak < 0.05:
            return fail(f"decoded audio is silent (peak {peak:.3f})")
        print(f"[smoke] whisper decode OK — {seconds:.2f} s, peak {peak:.2f}", file=sys.stderr)
        return 0
    finally:
        Path(wav_path).unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
