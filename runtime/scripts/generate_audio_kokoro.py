#!/usr/bin/env python3
"""
generate_audio_kokoro.py — the ONLY voice engine in the brutalist toolkit
(Kokoro-82M via kokoro-onnx — free, local, Apache-2.0, no API, no meter).

THE HOUSE VOICES — exactly two, both Kokoro:
  am_onyx   "Onyx"  — the nbb persona / Liam-in-for-Bear default
  af_bella  "Bella" — the hai persona default
Any other voice code is rejected. There is no ElevenLabs, no Suno, no paid
engine anywhere in this toolkit.

THE INTERFACE IS THE HOUSE INTERFACE:
  <folder>/mp3/beat-<ID>.mp3       one mp3 per beat
  <folder>/mp3/timings.json        {"B00": 3.1, ...}
  beat_sheet.json                  actual_duration_s + audio_file written back
Durations are GROUND TRUTH for all downstream timing.

PRONUNCIATION — the G2P reads spelling, so it will mispronounce brand names:
  metadata["pronounce"] = {"Medhavy": "mɛdˈhɑːviː"}
  A word → IPA lexicon. The line is phonemized normally, the listed words are
  substituted, and the whole line is synthesized as phonemes. Espeak gives
  "Medhavy" as /mˈɛdhævi/ — med-HAV-ee, rhyming with savvy — when the name is
  meh-DHAA-vee. Get the starting IPA from --phonemize, then edit the one word.

PACE:
  beat["speed"] or --speed. 1.0 is Kokoro's default and reads brisk; a brand
  line wants ~0.94. Below ~0.85 Kokoro smears the vowels.

VOICE SELECTION:
  - beat["voice"] = "af_bella" | "am_onyx"  → that voice for that beat
  - metadata["voice_kokoro"]                → folder default (else am_onyx)

MODEL FILES (one-time, ~330MB total, no account needed):
  $ART_HOME/runtime/models/kokoro/kokoro-v1.0.onnx
  $ART_HOME/runtime/models/kokoro/voices-v1.0.bin
  (override with $KOKORO_MODEL / $KOKORO_VOICES)
  mkdir -p runtime/models/kokoro && cd runtime/models/kokoro
  curl -LO https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
  curl -LO https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin

Install:  pip install kokoro-onnx        (and ffmpeg on PATH)

Usage:
    python3 generate_audio_kokoro.py path/to/<slug>              # generates immediately — no gate
    python3 generate_audio_kokoro.py path/to/<slug> --dry-run
    python3 generate_audio_kokoro.py path/to/<slug> --only B03 B08
    python3 generate_audio_kokoro.py --list-voices
    python3 generate_audio_kokoro.py --phonemize "Medhavy AI."
"""
import argparse
import json
import os
import re
import shutil
import struct
import subprocess
import sys
import wave
from pathlib import Path

FFMPEG = shutil.which("ffmpeg") or "ffmpeg"
FFPROBE = shutil.which("ffprobe") or "ffprobe"
DEFAULT_VOICE = "am_onyx"    # Onyx — the house default (nbb / Liam-in-for-Bear)
ALLOWED_VOICES = {"am_onyx", "af_bella"}   # the only two voices in this toolkit

# Math/symbol → spoken form. Applied as a safety net even if the beat sheet
# already carries tts_normalized_text. (Inlined from the legacy generate_audio.py.)
SYMBOLS = {
    "ψ": "psi", "Ψ": "Psi", "ℏ": "h-bar", "|ψ|²": "psi squared",
    "∫": "integral of", "→": "goes to", "≥": "greater than or equal to",
    "≤": "less than or equal to", "Δx": "delta x", "Δp": "delta p",
    "ΔE": "delta E", "∞": "infinity", "E₀": "E sub zero", "E₁": "E sub one",
    "·": " times ", "²": " squared", "½": "one half", "—": ", ",
}


def normalize_for_tts(text: str) -> str:
    for sym, spoken in SYMBOLS.items():
        text = text.replace(sym, spoken)
    return text


def phonemize(text: str, lang: str = "en-us") -> str:
    """The G2P Kokoro runs internally, exposed so a wrong guess is visible."""
    from kokoro_onnx.tokenizer import Tokenizer
    return Tokenizer().phonemize(text, lang=lang)


def apply_lexicon(text: str, lexicon: dict, lang: str = "en-us") -> str:
    """text + {word: IPA} -> one phoneme string for the whole line.

    The listed words are cut out of the text first and the surviving chunks are
    phonemized in context, so the rest of the line keeps its sentence-level
    prosody (espeak reduces "An" to /ɐn/ only when it can see the sentence).
    Phonemizing word by word and concatenating loses that.
    """
    if not lexicon:
        return phonemize(text, lang)
    pattern = re.compile(
        r"\b(" + "|".join(re.escape(w) for w in
                          sorted(lexicon, key=len, reverse=True)) + r")\b",
        re.IGNORECASE)
    out, hits = [], []
    for i, chunk in enumerate(pattern.split(text)):
        if i % 2:                       # odd chunks are the matched words
            key = next(k for k in lexicon if k.lower() == chunk.lower())
            out.append(lexicon[key].strip())
            hits.append(chunk)
        elif chunk.strip():
            out.append(phonemize(chunk, lang).strip())
    if hits:
        print(f"[kokoro] pronounce: {', '.join(hits)}")
    return " ".join(out)


def model_paths():
    home = Path(os.environ.get("ART_HOME") or Path(__file__).resolve().parents[2])
    base = home / "runtime" / "models" / "kokoro"
    model = Path(os.environ.get("KOKORO_MODEL") or base / "kokoro-v1.0.onnx")
    voices = Path(os.environ.get("KOKORO_VOICES") or base / "voices-v1.0.bin")
    return model, voices


def load_engine():
    model, voices = model_paths()
    if not (model.exists() and voices.exists()):
        sys.exit(
            f"[kokoro] model files missing. One-time download (~330MB, free):\n"
            f"  mkdir -p {model.parent}\n"
            f"  cd {model.parent}\n"
            f"  curl -LO https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx\n"
            f"  curl -LO https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin")
    try:
        from kokoro_onnx import Kokoro
    except ImportError:
        sys.exit("[kokoro] pip install kokoro-onnx   (free, local — no key)")
    return Kokoro(str(model), str(voices))


LANG_BY_PREFIX = {
    "a": "en-us",   # American English
    "b": "en-gb",   # British English
    "j": "ja",      # Japanese
    "z": "cmn",     # Mandarin Chinese
    "e": "es",      # Spanish
    "f": "fr-fr",   # French
    "h": "hi",      # Hindi
    "i": "it",      # Italian
    "p": "pt-br",   # Brazilian Portuguese
}


def lang_for(voice: str) -> str:
    """G2P language from the voice code's first letter (af_→en-us, zf_→cmn, …).
    Narration text for a non-English voice must be IN that language."""
    return LANG_BY_PREFIX.get(voice[:1], "en-us")


def write_mp3(samples, sample_rate, out_mp3: Path):
    """numpy float samples → wav (stdlib) → mp3 (ffmpeg). No soundfile dep."""
    tmp = out_mp3.with_suffix(".tmp.wav")
    ints = [max(-32768, min(32767, int(s * 32767))) for s in samples]
    with wave.open(str(tmp), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sample_rate)
        w.writeframes(struct.pack(f"<{len(ints)}h", *ints))
    subprocess.run([FFMPEG, "-y", "-v", "error", "-i", str(tmp),
                    "-c:a", "libmp3lame", "-q:a", "2", str(out_mp3)], check=True)
    tmp.unlink()


def measure(path: Path) -> float:
    out = subprocess.run([FFPROBE, "-v", "error", "-show_entries",
                          "format=duration", "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder", type=Path, nargs="?")
    ap.add_argument("--only", nargs="*", default=None, help="beat ids to (re)generate")
    ap.add_argument("--speed", type=float, default=1.0)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--list-voices", action="store_true")
    ap.add_argument("--phonemize", metavar="TEXT", default=None,
                    help="print the G2P's IPA for TEXT and exit — the first step "
                         "in fixing a mispronounced name")
    ap.add_argument("--sheet", default="beat_sheet.json",
                    help="beat sheet filename to read/write (default: beat_sheet.json)")
    a = ap.parse_args()

    if a.phonemize:
        print(phonemize(a.phonemize))
        return 0
    if a.list_voices:
        k = load_engine()
        for v in sorted(k.get_voices()):
            print(v)
        return 0
    if not a.folder:
        sys.exit("[kokoro] need a video folder (or --list-voices)")

    folder = a.folder.resolve()
    sheet_path = folder / a.sheet
    sheet = json.loads(sheet_path.read_text())
    md = sheet["metadata"]
    default_voice = md.get("voice_kokoro", DEFAULT_VOICE)
    lexicon = md.get("pronounce", {})

    todo = []
    for b in sheet["beats"]:
        bid = b["beat_id"]
        text = (b.get("narration_text") or "").strip()
        if not text:
            continue
        if a.only is not None and bid not in a.only:
            continue
        engine = str(b.get("engine", "kokoro")).lower()
        if engine != "kokoro":
            print(f"[kokoro] {bid}  engine={engine} — skipped (this toolkit is "
                  f"Kokoro-only; set engine to 'kokoro' to voice this beat)")
            continue
        voice = b.get("voice") or default_voice
        if voice not in ALLOWED_VOICES:
            sys.exit(f"[kokoro] {bid} asks for voice '{voice}' — this toolkit "
                     f"ships exactly two voices: am_onyx (Onyx) and af_bella "
                     f"(Bella). Fix the beat sheet.")
        todo.append((b, voice, text))

    if a.dry_run:
        for b, voice, text in todo:
            print(f"[kokoro] (dry-run) {b['beat_id']}  voice={voice}  "
                  f"{len(text)} chars")
        print(f"[kokoro] {len(todo)} beat(s) would generate — cost: $0.00")
        return 0

    k = load_engine()
    known = set(k.get_voices())
    bad = sorted({v for _, v, _ in todo} - known)
    if bad:
        sys.exit(f"[kokoro] unknown voice(s): {', '.join(bad)} — "
                 f"see --list-voices")

    (folder / "mp3").mkdir(exist_ok=True)
    timings_path = folder / "mp3" / "timings.json"
    timings = json.loads(timings_path.read_text()) if timings_path.exists() else {}
    for b, voice, text in todo:
        bid = b["beat_id"]
        lang = lang_for(voice)
        speed = float(b.get("speed", a.speed))
        spoken = normalize_for_tts(text)
        if lexicon:
            spoken = apply_lexicon(spoken, lexicon, lang)
        samples, sr = k.create(spoken, voice=voice, speed=speed, lang=lang,
                               is_phonemes=bool(lexicon))
        out = folder / "mp3" / f"beat-{bid}.mp3"
        write_mp3(samples, sr, out)
        dur = measure(out)
        b["audio_file"] = f"mp3/beat-{bid}.mp3"
        b["actual_duration_s"] = round(dur, 2)
        timings[bid] = round(dur, 2)
        print(f"[kokoro] beat-{bid}.mp3  {dur:.2f}s  voice={voice}  "
              f"speed={speed}")
    sheet_path.write_text(json.dumps(sheet, indent=1, ensure_ascii=False))
    timings_path.write_text(json.dumps(timings, indent=1))
    print(f"[kokoro] {len(todo)} beat(s) generated · cost $0.00 · durations "
          f"are GROUND TRUTH, same as generate_audio.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
