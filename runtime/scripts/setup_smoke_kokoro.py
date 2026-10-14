#!/usr/bin/env python3
"""setup_smoke_kokoro.py — setup's audio gate.

Synthesizes one throwaway phrase with Kokoro and decodes it with ffmpeg's
volumedetect filter. Exit 0 only if the render is real audio (mean_volume
> -40 dB) — not just "the model files exist" or "the import worked."
Prints nothing on success/failure beyond a one-line stderr note; setup's
check() discards output either way and reports its own MISS message.
"""
import os
import shutil
import struct
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODEL = ROOT / "runtime" / "models" / "kokoro" / "kokoro-v1.0.onnx"
VOICES = ROOT / "runtime" / "models" / "kokoro" / "voices-v1.0.bin"
THRESHOLD_DB = -40.0


def fail(msg: str) -> int:
    print(f"[smoke] {msg}", file=sys.stderr)
    return 1


def main() -> int:
    if not (MODEL.exists() and VOICES.exists()):
        return fail("Kokoro model files missing")
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        return fail("ffmpeg not on PATH")
    from espeak_fallback import use_system_espeak
    use_system_espeak()
    try:
        from kokoro_onnx import Kokoro
    except ImportError:
        return fail("kokoro_onnx not importable")

    try:
        k = Kokoro(str(MODEL), str(VOICES))
        samples, sr = k.create("This is a setup smoke test.", voice="af_bella",
                                speed=1.0, lang="en-us")
    except Exception as e:
        return fail(f"synthesis raised {e!r}")

    ints = [max(-32768, min(32767, int(s * 32767))) for s in samples]
    fd, wav_path = tempfile.mkstemp(suffix=".wav")
    os.close(fd)
    try:
        with wave.open(wav_path, "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(sr)
            w.writeframes(struct.pack(f"<{len(ints)}h", *ints))

        out = subprocess.run([ffmpeg, "-i", wav_path, "-af", "volumedetect",
                               "-f", "null", "-"],
                              capture_output=True, text=True)
        mean_db = None
        for line in out.stderr.splitlines():
            if "mean_volume" in line:
                mean_db = float(line.split(":")[1].strip().split(" ")[0])
        if mean_db is None:
            return fail("ffmpeg volumedetect produced no mean_volume reading")
        if mean_db <= THRESHOLD_DB:
            return fail(f"synthesized audio too quiet ({mean_db} dB <= {THRESHOLD_DB} dB)")
        print(f"[smoke] kokoro synth OK — mean_volume {mean_db} dB", file=sys.stderr)
        return 0
    finally:
        Path(wav_path).unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
