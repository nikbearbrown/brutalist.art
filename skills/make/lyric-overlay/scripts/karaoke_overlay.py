#!/usr/bin/env python3
"""karaoke_overlay.py — burn synced karaoke captions onto an ALREADY-FINISHED
video, without regenerating the underlying performance and without
re-encoding its audio.

This is the dot-tree adaptation of the musinique/brutalist-art `lyric-overlay`
skill (skills/make/lyric-overlay/, hyphen tree). The hyphen skill's own
pipeline builds a full Remotion project (OffthreadVideo background +
AudioVisualizer + LyricLayer) rendered through headless Chromium — the right
tool when a waveform visualizer matters. For these three spoken-word masters
(silent-bookended, multi-minute, 4K) a full Chromium frame-by-frame
re-composite of the entire body was judged not worth the render time
(realistically hours per file at 4K) against what it buys over a direct
image-overlay burn: the same synced, styled, word-highlight captions over
untouched footage, in minutes.

TWO ADDITIONAL DEVIATIONS FROM THE HYPHEN PATTERN, both forced by this
machine's actual ffmpeg build (verified with `ffmpeg -filters` /
`ffmpeg -version`):
  - No libass: this ffmpeg has no `ass`/`subtitles` filter (not compiled
    with --enable-libass). An ASS karaoke burn (the obvious approach) is
    therefore not available. Captions are instead rasterized frame-by-frame
    with Pillow (word-level color state: upcoming/active/sung) onto a
    transparent RGBA strip, held for its exact on-screen duration via an
    ffmpeg concat image list (one PNG per contiguous state, not per frame —
    a few hundred images for a multi-minute track, not tens of thousands),
    encoded to a `qtrle` (lossless, alpha-capable) intermediate, then
    composited onto the source with the plain `overlay` filter (in every
    ffmpeg build; no extra library needed).
  - This means captions are NOT Remotion-rendered for these three karaoke
    outputs. musinique-bookend's two cards (Task 1) ARE real Remotion
    components rendered via runtime/scripts/remotion_scenes.py, the
    toolkit's only lawful Remotion render path — that path was followed
    exactly where it applied. This script is a plain Python+ffmpeg
    compositor for the reasons above, styled with the same Musinique tokens
    (INK/CREAM/TEAL, Inter) by hand instead of importing tokens/musinique.ts.

THE GROUND-TRUTH LAW (kept from lyric-overlay): the audio comes from the
video itself, never a separate file — extract, transcribe, and leave the
ORIGINAL audio stream untouched (`-c:a copy`) in the output.

Pipeline:
  1. ffprobe the source for width/height/fps (the caption strip is sized to
     match the source exactly).
  2. ffmpeg-extract a 16kHz mono wav for Whisper (a scratch file only —
     the video's own audio stream is what ends up in the output, copied).
  3. faster-whisper, word_timestamps=True -> real per-word start/end times
     locked to the actual performance (never a beat-grid guess).
  4. Correct wording against a plain-text reference (the known
     poem/song/rhyme) ONLY where a whisper word is a close string match to a
     reference word — fixes proper nouns/archaic spelling/punctuation
     without overwriting genuine ad-libs/extensions/repeats (the actual
     performances here run longer than their base texts, confirmed on all
     three). Low-confidence words with no reference match are flagged
     `unclear: true` in the JSON sidecar (never invented, never silently
     dropped) but keep their whisper timing/text on the burned track —
     pulling a word off the burn would break the sync.
  5. Group corrected words into caption lines by pause-gap + a max
     words/line cap (the performance's own phrasing, not the reference's
     line breaks — an extended/ad-libbed performance does not track the
     base text line-for-line).
  6. Rasterize the karaoke strip (Pillow, Inter, Musinique tokens) and
     composite it onto the source (`overlay` filter; video re-encoded,
     audio stream-copied).

Usage:
  python3 skills/make/lyric-overlay/scripts/karaoke_overlay.py \\
      <musinique-master.mp4> --reference <reference.txt> \\
      --lang en [--model small] [--out <path>] [--keep-workdir]

Requires: pip install faster-whisper (already a toolkit dependency
elsewhere — skills/upload/youtube-publisher/scripts/transcribe.py is the
reference pattern this script follows for the transcription step), Pillow,
and ffmpeg (qtrle + overlay filter — both in any standard ffmpeg build).
"""
import argparse
import difflib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

FFPROBE = shutil.which("ffprobe") or "ffprobe"
FFMPEG = shutil.which("ffmpeg") or "ffmpeg"

# Musinique house tokens (runtime/remotion/src/tokens/musinique.ts), applied
# by hand since this is a plain Pillow/ffmpeg compositor, not a Remotion
# component — see the libass deviation note above.
MUSINIQUE_INK = (17, 24, 39)        # #111827 — near-black; scrim + outline
MUSINIQUE_TEAL = (37, 99, 235)      # #2563eb — the one accent; active word
MUSINIQUE_CREAM = (255, 255, 255)   # #ffffff — sung word (recede but legible)
MUSINIQUE_SLATE = (156, 163, 175)   # lighter gray-400 — upcoming word (dim, still readable on scrim)

FONT_CANDIDATES = [
    "/Users/bear/Library/Fonts/Inter_28pt-Bold.ttf",
    "/Users/bear/Library/Fonts/Inter_24pt-Bold.ttf",
    "/Users/bear/Library/Fonts/Inter-VariableFont_opsz,wght.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
]


def run(cmd, **kw):
    print("[karaoke]", "$", " ".join(str(c) for c in cmd))
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        sys.exit(f"[karaoke] command failed (exit {r.returncode}): {cmd[0]}\n{r.stderr[-1500:]}")
    return r


def ffprobe_video(path: Path) -> dict:
    r = subprocess.run(
        [FFPROBE, "-v", "error", "-print_format", "json", "-show_format", "-show_streams", str(path)],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        sys.exit(f"[karaoke] ffprobe failed on {path}:\n{r.stderr[-800:]}")
    info = json.loads(r.stdout)
    vs = next(s for s in info["streams"] if s["codec_type"] == "video")
    num, den = (vs.get("r_frame_rate") or "30/1").split("/")
    fps = float(num) / float(den or 1)
    return {
        "width": int(vs["width"]), "height": int(vs["height"]), "fps": fps,
        "duration": float(info["format"].get("duration") or vs.get("duration") or 0.0),
    }


def extract_wav(video: Path, wav: Path):
    run([FFMPEG, "-y", "-i", str(video), "-vn", "-ac", "1", "-ar", "16000", "-f", "wav", str(wav)])


def transcribe_words(wav: Path, model_size: str, language):
    from faster_whisper import WhisperModel
    print(f"[karaoke] loading faster-whisper model '{model_size}' (cpu, int8) ...")
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    print("[karaoke] transcribing with word timestamps (this can take a while on a multi-minute 4K master) ...")
    segments, info = model.transcribe(
        str(wav), language=language, word_timestamps=True,
        vad_filter=True, vad_parameters=dict(min_silence_duration_ms=400),
    )
    words = []
    seg_records = []
    for seg in segments:
        seg_records.append({"start": round(seg.start, 2), "end": round(seg.end, 2), "text": seg.text.strip()})
        print(f"  [{seg.start:7.1f}s] {seg.text.strip()[:90]}")
        if not seg.words:
            continue
        for w in seg.words:
            token = w.word.strip()
            if not token:
                continue
            words.append({
                "word": token, "start": round(w.start, 3), "end": round(w.end, 3),
                "probability": round(float(getattr(w, "probability", 1.0)), 3),
            })
    detected_lang = getattr(info, "language", language or "unknown")
    return words, seg_records, detected_lang


_WORD_RE = re.compile(r"[A-Za-z']+")


def normalize(token: str) -> str:
    return re.sub(r"[^a-z']", "", token.lower())


def load_reference_tokens(ref_path: Path) -> list:
    """Flat list of normalized reference words (English-alphabet tokens only —
    the Goosey reference is bilingual English/Punjabi; the Gurmukhi lines
    simply never match and are correctly left to whisper's own transcription
    of that stretch, since only the English lines are meant to correct
    wording here)."""
    text = ref_path.read_text(encoding="utf-8")
    return [normalize(t) for t in _WORD_RE.findall(text) if normalize(t)]


def best_reference_match(token: str, ref_tokens: list, ref_set: set):
    """Exact matches (safe: only fixes casing) are always accepted. Fuzzy
    matches (whisper misheard a word) are restricted to tokens of 5+ chars —
    short words ('not'/'no', 'is'/'in') collide too easily on edit-distance
    alone and a false correction on a common function word is worse than no
    correction (the FRUMP false-positive 'not' -> 'No' caught in review is
    exactly this failure mode; length + a stricter cutoff for short words
    closes it without losing the archaic/proper-noun corrections this exists
    for — 'sinew', 'impostors', 'Kipling'-length words are all >= 5)."""
    norm = normalize(token)
    if not norm:
        return None, 0.0
    if norm in ref_set:
        return norm, 1.0
    if len(norm) < 5:
        return None, 0.0
    close = difflib.get_close_matches(norm, ref_tokens, n=1, cutoff=0.82)
    if close and close[0][:1] == norm[:1]:
        ratio = difflib.SequenceMatcher(None, norm, close[0]).ratio()
        return close[0], ratio
    return None, 0.0


def find_original_casing(ref_path: Path, normalized_token: str):
    text = ref_path.read_text(encoding="utf-8")
    for tok in _WORD_RE.findall(text):
        if normalize(tok) == normalized_token:
            return tok
    return None


def correct_words(words: list, ref_tokens: list, ref_path: Path) -> list:
    ref_set = set(ref_tokens)
    out = []
    for w in words:
        match, ratio = best_reference_match(w["word"], ref_tokens, ref_set)
        corrected = dict(w)
        corrected["reference_match"] = match
        corrected["match_ratio"] = round(ratio, 3)
        corrected["unclear"] = bool(w["probability"] < 0.45 and match is None)
        if match and ratio >= 0.72:
            corrected["display"] = find_original_casing(ref_path, match) or w["word"]
        else:
            corrected["display"] = w["word"]
        out.append(corrected)
    return out


def group_lines(words: list, max_gap_s: float = 0.6, max_words: int = 7) -> list:
    lines = []
    cur = []
    prev_end = None
    for w in words:
        if cur and (w["start"] - prev_end > max_gap_s or len(cur) >= max_words):
            lines.append(cur)
            cur = []
        cur.append(w)
        prev_end = w["end"]
    if cur:
        lines.append(cur)
    return lines


# ── Pillow caption-strip rendering ──────────────────────────────────────────

def load_font(size: int):
    from PIL import ImageFont
    for path in FONT_CANDIDATES:
        if Path(path).exists():
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    return ImageFont.load_default()


def word_color(word: dict, t: float):
    if t < word["start"]:
        return MUSINIQUE_SLATE
    if t < word["end"]:
        return MUSINIQUE_TEAL
    return MUSINIQUE_CREAM


def render_line_frame(line: list, t: float, width: int, height: int, font):
    from PIL import Image, ImageDraw
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    display_words = [w["display"] for w in line]
    spacer = " "
    gaps = [draw.textlength(spacer, font=font) for _ in line]
    widths = [draw.textlength(w, font=font) for w in display_words]
    total_w = sum(widths) + sum(gaps[:-1]) if len(line) > 1 else (widths[0] if widths else 0)

    pad_x, pad_y = 36, 20
    box_w = min(width - 40, total_w + pad_x * 2)
    box_h = font.size + pad_y * 2
    box_x0 = (width - box_w) / 2
    box_y0 = (height - box_h) / 2
    scrim = Image.new("RGBA", (int(box_w), int(box_h)), (*MUSINIQUE_INK, 178))
    _round_mask_paste(img, scrim, int(box_x0), int(box_y0), radius=18)

    x = (width - total_w) / 2
    y = (height - font.size) / 2 - pad_y * 0.15
    for i, w in enumerate(line):
        color = word_color(w, t)
        draw.text((x, y), display_words[i], font=font, fill=(*color, 255))
        x += widths[i] + (gaps[i] if i < len(line) - 1 else 0)
    return img


def _round_mask_paste(base, patch, x, y, radius=16):
    from PIL import Image, ImageDraw
    mask = Image.new("L", patch.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, patch.size[0], patch.size[1]], radius=radius, fill=255)
    base.paste(patch, (x, y), mask)


def build_state_segments(lines: list, duration: float):
    """One (representative_time, start, end) tuple per contiguous on-screen
    state: a blank gap, or a line with one particular word-highlight state.
    Far fewer entries than frames — an image is rendered once per segment,
    not once per frame."""
    segments = []
    cursor = 0.0
    for line in lines:
        line_start = line[0]["start"]
        line_end = line[-1]["end"]
        if line_start > cursor:
            segments.append((None, cursor, line_start))  # blank gap
        boundaries = {line_start, line_end}
        for w in line:
            boundaries.add(w["start"])
            boundaries.add(w["end"])
        bts = sorted(t for t in boundaries if line_start <= t <= line_end)
        for i in range(len(bts) - 1):
            t0, t1 = bts[i], bts[i + 1]
            if t1 - t0 <= 0.001:
                continue
            segments.append((line, t0, t1))
        cursor = line_end
    if duration > cursor:
        segments.append((None, cursor, duration))
    return segments


def render_caption_layer(lines: list, duration: float, width: int, strip_h: int, workdir: Path) -> Path:
    font = load_font(max(28, round(strip_h * 0.30)))
    segments = build_state_segments(lines, duration)
    frames_dir = workdir / "caption_frames"
    frames_dir.mkdir(parents=True, exist_ok=True)

    blank = None
    concat_lines = ["ffconcat version 1.0"]
    last_path = None
    for i, (line, t0, t1) in enumerate(segments):
        dur = t1 - t0
        if line is None:
            if blank is None:
                from PIL import Image
                blank = frames_dir / "blank.png"
                Image.new("RGBA", (width, strip_h), (0, 0, 0, 0)).save(blank)
            path = blank
        else:
            mid_t = (t0 + t1) / 2
            img = render_line_frame(line, mid_t, width, strip_h, font)
            path = frames_dir / f"seg{i:05d}.png"
            img.save(path)
        concat_lines.append(f"file '{path.name}'")
        concat_lines.append(f"duration {dur:.3f}")
        last_path = path
    if last_path is not None:
        concat_lines.append(f"file '{last_path.name}'")  # concat-demuxer image quirk: repeat final entry

    list_path = frames_dir / "list.ffconcat"
    list_path.write_text("\n".join(concat_lines) + "\n", encoding="utf-8")
    print(f"[karaoke] rendered {len(segments)} caption-state images -> {frames_dir.name}/")

    overlay_mov = workdir / "caption_overlay.mov"
    run([
        FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", str(list_path),
        "-pix_fmt", "argb", "-c:v", "qtrle",
        str(overlay_mov),
    ])
    return overlay_mov


def composite(video: Path, overlay_mov: Path, out_path: Path, src: dict, strip_h: int):
    y_offset = src["height"] - strip_h - round(src["height"] * 0.05)
    cmd = [
        FFMPEG, "-y", "-i", str(video), "-i", str(overlay_mov),
        "-filter_complex", f"[0:v][1:v]overlay=x=0:y={y_offset}:format=auto[outv]",
        "-map", "[outv]", "-map", "0:a",
        "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p",
        "-r", str(src["fps"]),
        "-c:a", "copy",  # source audio stream untouched — never re-encoded
        str(out_path),
    ]
    run(cmd)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video", type=Path, help="the finished Musinique master (already has its bookends)")
    ap.add_argument("--reference", type=Path, required=True,
                     help="plain-text reference lyrics/poem used ONLY to correct wording, never timing")
    ap.add_argument("--lang", default="en", help="whisper language hint ('auto'/'' for bilingual sources)")
    ap.add_argument("--model", default="small", help="faster-whisper model size (tiny/base/small/medium)")
    ap.add_argument("--out", type=Path, default=None,
                     help="output path (default: <video-stem-without-musinique>-musinique-karaoke.mp4)")
    ap.add_argument("--keep-workdir", action="store_true")
    a = ap.parse_args()

    video = a.video.resolve()
    if not video.exists():
        sys.exit(f"[karaoke] no such file: {video}")
    ref = a.reference.resolve()
    if not ref.exists():
        sys.exit(f"[karaoke] no such reference file: {ref}")

    src = ffprobe_video(video)
    print(f"[karaoke] source: {src['width']}x{src['height']} @ {src['fps']:.3f}fps, {src['duration']:.1f}s")

    out = a.out.resolve() if a.out else video.with_name(video.stem + "-karaoke.mp4")

    workdir = Path(tempfile.mkdtemp(prefix="lyric-overlay-"))
    wav = workdir / "audio.wav"
    try:
        print("[karaoke] extracting audio (ground-truth law: from the video itself) ...")
        extract_wav(video, wav)

        lang = None if a.lang.lower() in ("", "auto") else a.lang
        words, segments, detected_lang = transcribe_words(wav, a.model, lang)
        if not words:
            sys.exit("[karaoke] whisper returned no words — refusing to burn an empty track")

        ref_tokens = load_reference_tokens(ref)
        words = correct_words(words, ref_tokens, ref)
        lines = group_lines(words)
        unclear_count = sum(1 for w in words if w["unclear"])

        sidecar = out.with_suffix(".lyrics.json")
        sidecar.write_text(json.dumps({
            "version": 1,
            "video": video.name,
            "fps": src["fps"],
            "detected_language": detected_lang,
            "reference": ref.name,
            "model": a.model,
            "word_count": len(words),
            "unclear_count": unclear_count,
            "segments": segments,
            "lines": [
                {
                    "index": i,
                    "start": ln[0]["start"], "end": ln[-1]["end"],
                    "text": " ".join(w["display"] for w in ln),
                    "words": ln,
                }
                for i, ln in enumerate(lines)
            ],
        }, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"[karaoke] wrote sidecar {sidecar} ({len(words)} words, {unclear_count} flagged unclear)")

        strip_h = max(160, round(src["height"] * 0.16))
        overlay_mov = render_caption_layer(lines, src["duration"], src["width"], strip_h, workdir)

        print("[karaoke] compositing captions (video re-encoded; audio stream-copied untouched) ...")
        composite(video, overlay_mov, out, src, strip_h)
    finally:
        if a.keep_workdir:
            print(f"[karaoke] kept workdir: {workdir}")
        else:
            shutil.rmtree(workdir, ignore_errors=True)

    final = ffprobe_video(out)
    print(f"[karaoke] wrote {out}  ({final['width']}x{final['height']}, {final['duration']:.1f}s)")


if __name__ == "__main__":
    main()
