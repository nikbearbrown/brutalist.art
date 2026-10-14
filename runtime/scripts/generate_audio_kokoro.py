#!/usr/bin/env python3
"""
generate_audio_kokoro.py — the FREE voice engine (Kokoro-82M via kokoro-onnx).

Kokoro is FREE — a local 82M-parameter Apache-2.0 model with ~28 NAMED preset
voices (Bella, Sarah, Adam, Michael, Emma, George, Puck, Santa, …). No API,
no meter, no quota; near-real-time on an M1's CPU. The catch: no cloning —
none of these voices is yours. Best uses: audio previz (free draft narration),
volume work where the voice isn't the brand, and multi-voice cast pieces.

THE INTERFACE IS THE HOUSE INTERFACE — identical to generate_audio.py:
  <folder>/mp3/beat-<ID>.mp3       one mp3 per beat
  <folder>/mp3/timings.json        {"B00": 3.1, ...}
  beat_sheet.json                  actual_duration_s + audio_file written back
Durations are GROUND TRUTH for all downstream timing. Downstream never knows
which engine spoke.

PRONUNCIATION — the G2P reads spelling, so it will mispronounce brand names.
Two layers, applied in this order:
  1. runtime/pronunciation/<persona>.json — voice-only TEXT respellings
     (see liam.json); the on-screen text is untouched.
  2. metadata["pronounce"] = {"Medhavy": "mɛdˈhɑːviː"} — a word → IPA lexicon.
     The line is phonemized normally, the listed words are substituted, and the
     whole line is synthesized as phonemes. Espeak gives "Medhavy" as
     /mˈɛdhævi/ — med-HAV-ee, rhyming with savvy — when the name is
     meh-DHAA-vee. Get the starting IPA from --phonemize, then edit the one
     word. A lexicon key matches the text AFTER layer 1, so key it on the
     respelled form if layer 1 rewrites that word.

PACE:
  beat["speed"] or --speed. 1.0 is Kokoro's default and reads brisk; a brand
  line wants ~0.94. Below ~0.85 Kokoro smears the vowels.

VOICE SELECTION (mixed-engine sheets supported):
  - beat["voice"] = "af_bella" | "am_adam" | …  → that Kokoro voice
  - metadata["voice_kokoro"] or metadata["voice"] → folder default (must agree)
  - beat["engine"] = "nbb" (or any non-"kokoro" value) → SKIPPED here;
    run generate_audio_nbb.py --only <those beats> for them. A sheet can mix
    nbb body beats with kokoro bookends.

MODEL FILES (one-time, ~330MB total, no account needed):
  $ART_HOME/runtime/models/kokoro/kokoro-v1.0.onnx
  $ART_HOME/runtime/models/kokoro/voices-v1.0.bin
  (override with $KOKORO_MODEL / $KOKORO_VOICES)
  mkdir -p runtime/models/kokoro && cd runtime/models/kokoro
  curl -LO https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
  curl -LO https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin

Install:  pip install kokoro-onnx        (and ffmpeg on PATH)

Usage:
    python3 generate_audio_kokoro.py path/to/<slug>              # human approval gates apply
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
import tempfile
import wave
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_safety import (BuildError, atomic_json, default_voice, is_source_report,
                          intentional_silence, validate_project, validate_approvals, writable_path)
# Spoken-form safety net. Inlined on purpose: the sandbox kept this in
# generate_audio.py alongside the PAID ElevenLabs engine, which is excluded from
# this cut by design — so importing from it left the FREE default engine unable
# to start (caught 2026-08-31). The toolkit is self-contained; this table has no
# business living in a file that only exists to hold a paid API client.
SYMBOLS = {
    "\u03c8": "psi", "\u03a8": "Psi", "\u210f": "h-bar", "|\u03c8|\u00b2": "psi squared",
    "\u222b": "integral of", "\u2192": "goes to", "\u2265": "greater than or equal to",
    "\u2264": "less than or equal to", "\u0394x": "delta x", "\u0394p": "delta p",
    "\u0394E": "delta E", "\u221e": "infinity", "E\u2080": "E sub zero", "E\u2081": "E sub one",
    "\u00b7": " times ", "\u00b2": " squared", "\u00bd": "one half", "\u2014": ", ",
}


def normalize_for_tts(text: str, voice: str = None) -> str:
    for sym, spoken in SYMBOLS.items():
        text = text.replace(sym, spoken)
    if voice:
        from pronunciation import apply as _pron   # runtime/pronunciation/<persona>.json, voice-only rewrites
        text = _pron(text, voice)
    return text


FFMPEG = shutil.which("ffmpeg") or "ffmpeg"
FFPROBE = shutil.which("ffprobe") or "ffprobe"
DEFAULT_VOICE = "am_onyx"   # Non-fellows fallback; fellows require an approved choice.


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
    from espeak_fallback import use_system_espeak
    use_system_espeak()
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
    """Copy-on-write output: never follow a Short's legacy link into its parent."""
    ints = [max(-32768, min(32767, int(s * 32767))) for s in samples]
    with tempfile.TemporaryDirectory(prefix='.tts-', dir=out_mp3.parent) as scratch:
        tmp = Path(scratch) / 'audio.wav'
        encoded = Path(scratch) / 'audio.mp3'
        with wave.open(str(tmp), "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(sample_rate)
            w.writeframes(struct.pack(f"<{len(ints)}h", *ints))
        subprocess.run([FFMPEG, "-y", "-v", "error", "-i", str(tmp),
                        "-c:a", "libmp3lame", "-q:a", "2", str(encoded)], check=True)
        os.replace(encoded, out_mp3)


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
    ap.add_argument("--no-gate", action="store_true",
                    help="deprecated; cannot bypass human approvals")
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
    sheet_path = writable_path(folder, a.sheet)
    sheet = json.loads(sheet_path.read_text())
    # Schema normalisation: v1 uses "id"; v2 uses "beat_id". Accept both.
    for _b in sheet.get("beats", []):
        if "beat_id" not in _b and "id" in _b:
            _b["beat_id"] = _b["id"]
        if "narration_text" not in _b and "narration" in _b:
            _b["narration_text"] = _b["narration"]
        if "actual_duration_s" not in _b:
            for _k in ("est_s", "estimated_duration_s"):
                if _k in _b:
                    _b["actual_duration_s"] = float(_b[_k])
                    break
    md = sheet["metadata"]
    validate_project(sheet)
    validate_approvals(folder, sheet)
    selected_voice = default_voice(sheet)
    lexicon = md.get("pronounce", {})

    todo = []
    for b in sheet["beats"]:
        bid = b["beat_id"]
        if is_source_report(b, sheet) or intentional_silence(b):
            print(f"[kokoro] {bid} SKIPPED — source audio / intentional silence")
            continue
        text = (b.get("narration_text") or "").strip()
        if not text:
            continue
        if text.startswith(("⚠", "[LOST]", "[PLACEHOLDER]")):
            # A sentinel is a note to humans, not a script. Voicing one ships
            # "narration lost" as narration (incident 2026-08-27). Hard skip.
            print(f"[kokoro] {bid}  SKIPPED — narration_text is a sentinel, not narration")
            continue
        if a.only is not None and bid not in a.only:
            continue
        engine = str(b.get("engine", "kokoro")).lower()
        if engine != "kokoro":
            print(f"[kokoro] {bid}  engine={engine} — skipped (run its own "
                  f"generator, e.g. generate_audio.py --only {bid})")
            continue
        voice = b.get("voice") or selected_voice
        todo.append((b, voice, text))

    if a.dry_run:
        for b, voice, text in todo:
            print(f"[kokoro] (dry-run) {b['beat_id']}  voice={voice}  "
                  f"{len(text)} chars")
        print(f"[kokoro] {len(todo)} beat(s) would generate — cost: $0.00")
        return 0

    if not todo:
        print('[kokoro] no narration to generate')
        return 0
    k = load_engine()
    known = set(k.get_voices())
    bad = sorted({v for _, v, _ in todo} - known)
    if bad:
        sys.exit(f"[kokoro] unknown voice(s): {', '.join(bad)} — "
                 f"see --list-voices")

    writable_path(folder, 'mp3/timings.json').parent.mkdir(exist_ok=True)
    timings_path = writable_path(folder, 'mp3/timings.json')
    timings = json.loads(timings_path.read_text()) if timings_path.exists() else {}
    for b, voice, text in todo:
        bid = b["beat_id"]
        lang = lang_for(voice)
        speed = float(b.get("speed", a.speed))
        spoken = normalize_for_tts(text, voice)
        if lexicon:
            spoken = apply_lexicon(spoken, lexicon, lang)
        samples, sr = k.create(spoken, voice=voice, speed=speed, lang=lang,
                               is_phonemes=bool(lexicon))
        out = writable_path(folder, f"mp3/beat-{bid}.mp3")
        write_mp3(samples, sr, out)
        dur = measure(out)
        b["audio_file"] = f"mp3/beat-{bid}.mp3"
        b["actual_duration_s"] = round(dur, 2)
        timings[bid] = round(dur, 2)
        print(f"[kokoro] beat-{bid}.mp3  {dur:.2f}s  voice={voice}  "
              f"speed={speed}")
    atomic_json(sheet_path, sheet)
    atomic_json(timings_path, timings)
    print(f"[kokoro] {len(todo)} beat(s) generated · cost $0.00 · durations "
          f"are GROUND TRUTH, same as generate_audio.py")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BuildError as exc:
        raise SystemExit(f'[kokoro] REFUSED: {exc}')
