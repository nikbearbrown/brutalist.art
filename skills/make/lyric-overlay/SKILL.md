---
name: lyric-overlay
description: >
  Add synced karaoke captions (word-level highlight, timed to the real
  vocal/performance audio) on top of an EXISTING finished video — without
  regenerating or re-rendering the underlying footage, and without
  re-encoding its audio. Use when the user has a finished .mp4 and wants
  "the karaoke version", "add synced lyrics to this video", "put captions
  timed to the speech on this", or types `overlay`. Input: a finished
  video + a plain-text reference (for wording correction only, never
  timing). Output: `<video-stem>-karaoke.mp4` beside the source, plus a
  `<same-stem>.lyrics.json` sidecar with every word's real timestamp,
  reference-corrected spelling, and an `unclear` flag where neither
  whisper nor the reference could resolve a word.
metadata:
  tags: karaoke, captions, overlay, faster-whisper, transcription, musinique
---

# lyric-overlay — synced karaoke captions over an already-finished video

Dot-tree port of the hyphen-tree `lyric-overlay` skill (originally named
`muzak-overlay`, sibling of `music-video`/`muzak`). Read
`REMOTION-STANDARDS.md` before touching anything under
`runtime/remotion/src/scenes/` — this skill, as adapted here, does **not**
add a new Remotion component (see the deviation note below), but the rule
still governs any future work that brings this pattern back into Remotion.

## What changed in the port, and why

The hyphen skill (`skills/make/lyric-overlay/scripts/overlay_new.py`) builds
a full Remotion project: `VideoBackground.tsx` (OffthreadVideo background +
scrim), `AudioVisualizer.tsx` (oscilloscope waveform), `LyricLayer.tsx`
(karaoke captions), all rendered through headless Chromium. It also depends
on a **sibling `muzak` skill's** scripts (`analyze_audio.py` for librosa beat
analysis, `align_lyrics.py`/`align_lyrics_audio.py` for lyric timing) which
do not exist in this toolkit — `music-video`/`muzak` was never ported to
`brutalist.art/`.

For the three spoken-word masters this skill was built to karaoke
(`spoken-word/{frump,goosey,if}/*-musinique.mp4` — 4K, 1.5–3.5 minutes each),
neither piece of that machinery was worth porting as-is:

- **No waveform visualizer needed** — these are spoken-word recitations
  wrapped in silent Musinique bookends, not music videos; the ask was
  captions only.
- **No beat-grid needed** — `align_lyrics.py`'s even-spacing seed is a worse
  starting point than real ASR timestamps. `faster-whisper` with
  `word_timestamps=True` gives genuine per-word timing off the actual
  audio directly — no beat analysis step required at all.
- **Full-length Chromium compositing of a multi-minute 4K video was judged
  too expensive** for what it would buy here (realistically well over an
  hour of headless-Chromium OffthreadVideo decode+re-encode per file) versus
  a plain image-overlay burn that produces the identical visible result —
  synced word-highlight captions over untouched footage — in minutes.
- **This machine's ffmpeg has no libass** (`ffmpeg -filters` has no
  `ass`/`subtitles` entry — confirmed, not assumed), which rules out the
  other obvious non-Remotion path (an ASS karaoke burn).

So `scripts/karaoke_overlay.py` does it a third way: Pillow rasterizes a
transparent RGBA caption strip frame **once per contiguous on-screen state**
(a word's highlight changing is a state change; a silent gap is one blank
state) — a few hundred images for a multi-minute track, not one per output
frame — held for its exact duration via an ffmpeg concat image list, encoded
losslessly with alpha (`qtrle`), then composited onto the source with the
plain `overlay` filter (in every ffmpeg build, no extra library). Colors and
type come from `runtime/remotion/src/tokens/musinique.ts`'s values, applied
by hand (INK `#111827`, TEAL `#2563eb`, CREAM `#ffffff`, Inter) since this
is a Python/ffmpeg compositor, not a Remotion component.

**This is the documented REMOTION-STANDARDS deviation for this pattern.**
Task 1's `musinique-bookend` cards are real Remotion components rendered
via `runtime/scripts/remotion_scenes.py` (the toolkit's only lawful Remotion
render path) — that path was used exactly where it applied. This skill's
karaoke layer is not a Remotion component at all, for the reasons above.
Porting a real `LyricLayer`-equivalent Remotion scene remains open work if a
future song needs the waveform visualizer too (see "Next phase" below).

## The one rule everything else serves

**The audio is ground truth, and it comes from the video itself.** The
script extracts a scratch 16kHz mono wav from the source `.mp4` purely for
Whisper to transcribe; the OUTPUT's audio stream is the source's own,
stream-copied (`-c:a copy`) — never re-encoded, never replaced.

## The one command

```bash
python3 skills/make/lyric-overlay/scripts/karaoke_overlay.py \
    <finished-master.mp4> --reference <reference.txt> \
    [--lang en|auto] [--model small] [--out <path>] [--keep-workdir]
```

That single run: extracts audio -> `faster-whisper` word-level transcription
-> reference-based wording correction -> line grouping by pause-gap ->
Pillow caption-strip rasterization -> ffmpeg `overlay` composite. Writes
`<video-stem>-karaoke.mp4` and `<video-stem>-karaoke.lyrics.json` beside the
source (or wherever `--out` points, with the sidecar taking the same stem).

## The laws

| Law | What it means |
|---|---|
| **GROUND-TRUTH LAW** | Audio for transcription is extracted from the video itself, never a separate file; the output's audio track is the source's own, byte-identical (`-c:a copy`). |
| **REAL-TIMESTAMPS LAW** | Every word's on-screen timing comes from `faster-whisper`'s `word_timestamps=True` against the actual performance — never a beat-grid guess, never hand-typed. |
| **REFERENCE-IS-WORDING-ONLY LAW** | A plain-text reference (the known poem/song/rhyme) may correct a word's *spelling/casing*, never its *timing*, and only when the whisper word is a close string match (`difflib`, same first letter, ratio ≥ 0.72). An ad-libbed/extended passage with no close match is left exactly as whisper heard it — never forced onto the reference text. |
| **NO-GUESS LAW** | A low-confidence word (`probability < 0.45`) with no reference corroboration is flagged `unclear: true` in the `.lyrics.json` sidecar. It is never invented and never silently dropped from the burned track (removing it would break the sync) — the flag is the record of doubt. |
| **NO-FOOTAGE-REGEN LAW** | The source video's picture content is never regenerated or re-cut — only composited with a caption layer on top. Video pixels are necessarily re-encoded to burn that layer in (unavoidable — compositing changes pixels); audio is not. |

## Pipeline detail

1. **ffprobe** the source for width/height/fps — the caption strip matches
   exactly, no rescale.
2. **Extract** `audio.wav` (16kHz mono, scratch only).
3. **Transcribe** (`faster-whisper`, `word_timestamps=True`, `vad_filter=True`)
   -> a flat word list with real start/end/probability.
4. **Correct wording** against `--reference` (normalize + `difflib` closest
   match); flag `unclear` where neither source resolves a word.
5. **Group into lines** by a 0.6s pause-gap or a 7-word cap — the
   performance's own phrasing, not the reference's line breaks.
6. **Rasterize + composite**: one Pillow RGBA frame per contiguous
   highlight-state (blank / a line with one particular word active), held
   via an ffmpeg concat image list, `qtrle`-encoded for alpha, then
   `overlay`'d onto the source; audio stream-copied.

## Known references used so far

- `references/if-kipling.txt` — Rudyard Kipling, "If—" (1910), public domain.
- `references/frump-mother-goose.txt` — traditional "Young Roger and Dolly"
  (the short base text; Bear's actual performance runs longer — extension/
  repetition, confirmed by whisper's own timing vs. the base text length).
- Goosey uses `books/musinique/distrokid/guusii-guusii-gainddr-goosey-goosey-gander/lyrics.txt`
  directly (bilingual English/Punjabi) — not copied into this skill; pass
  its path as `--reference`. The Gurmukhi lines never match (English-token
  matching only) and are correctly left to whisper's own transcription of
  that stretch.

## Next phase

If a future song needs the waveform visualizer too, port `muzak`'s
`analyze_audio.py` (librosa) and build a real `LyricLayer`-equivalent
Remotion scene (schema + demo twin + Root.tsx registration + scene-index
regen, per REMOTION-STANDARDS §6) instead of extending this ffmpeg/Pillow
compositor — the compositor is scoped to "captions only, no re-render",
which is what every request so far has actually needed.
