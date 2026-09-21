---
name: musinique-bookend
description: >
  Wrap an already-finished standalone film — a music video, a spoken-word
  recitation, any raw video file that is NOT a beat-sheet-driven reel — in a
  silent Musinique intro card (title text) and a silent Musinique outro card
  (@Musinique handle + the performing artist's name and links), output at the
  source's own 4K resolution and frame rate. Use when the user types
  `musinique bookend <film>`, `wrap this in musinique bookends`, or asks to
  add a Musinique open/close to a finished song or spoken-word video.
---

# musinique-bookend — silent open/close for a finished film

One command: ffprobe the source, render two silent Remotion cards to match it
exactly, concatenate. No narration, no jingle, no register — the whole point
is silence.

## The one command

```bash
python3 skills/make/musinique-bookend/scripts/musinique_bookend.py \
    <film_path> --title "<title text>" --artist <artist-slug> [--out <path>]
```

That single run: ffprobes `<film_path>` for width/height/fps/audio params,
renders `MusiniqueIntroCard` and `MusiniqueOutroCard` via
`runtime/scripts/remotion_scenes.py` (foreground — the only lawful Remotion
path) with props matched to the source's exact canvas, concatenates
intro + source + outro with ffmpeg, and writes the result beside the source
film. Nothing else to do.

## The laws

| Law | What it means |
|---|---|
| **SILENCE LAW** | No audible content enters either bookend, ever. Neither `MusiniqueIntroCard.tsx` nor `MusiniqueOutroCard.tsx` has an `<Audio>` tag — not muted, not present. The only audio the script ever adds is a synthesized `anullsrc` silence, matched to the source's own sample rate/channel layout, purely so ffmpeg's concat filter has matching stream shapes. No TTS, no jingle, no register — never. |
| **ARTIST-LINKS LAW** | The outro's artist name and every link come from `artists.json` in this skill's own folder, resolved by `--artist <slug>`. Never invented, never guessed, never filled in from memory. An unknown slug is a hard stop that prints the known slugs. |
| **4K-MATCH LAW** | Bookends always render at the source's exact resolution and fps — ffprobe'd at runtime, never hardcoded. All three known spoken-word sources happen to be 3840x2160, but the script does not assume that; it reads whatever the file actually is. |
| **MUSINIQUE-NATIVE LAW** | Both cards use `runtime/remotion/src/tokens/musinique.ts` — monochrome editorial (white ground, near-black ink, the one blue accent), Inter throughout, no serif. This is a musinique-native piece per `MUSINIQUE.md`'s "Video grammar" section — never the Claude UI skin. |
| **NO-GUESS LAW** | The script never picks which artist performs a film. `--artist` is a required, explicit flag; there is no default. |

## The artist registry

`skills/make/musinique-bookend/artists.json` — 13 artists, each a kebab-case
slug with whatever links Bear actually gave (some have 2, some have 3; never
padded to match). Look up a slug's exact links there before calling
`--artist`; the script's own error message on an unknown slug lists every
known one.

**Known data issue, flagged not fixed:** `jingle-yankel`'s `apple_music` and
`musinique` links are byte-identical to `mayfield-king`'s in Bear's source
list — almost certainly a copy-paste slip upstream, not corrected here. See
`artists.json`'s `_flags` field. Confirm the real links with Bear before
trusting `jingle-yankel`'s outro card.

## Why the concat filter, not stream-copy

The known sources disagree on fps (25 vs 30) and audio sample rate (48000 vs
44100 Hz), and the Remotion renders are an independent encode from the
source. Stream-copy concat (the `concat` demuxer) needs byte-identical codec
parameters on every segment — fragile here, and a mismatch fails silently or
produces an unplayable file. `musinique_bookend.py` instead builds one
`ffmpeg -filter_complex` graph: every video segment is force-scaled/fps-
normalized to the source's exact canvas, and (when the source has audio)
each bookend gets a silent `anullsrc` companion trimmed to its own rendered
duration so audio and video stay in lock-step across the concat. One
re-encode pass, in exchange for never depending on the source and the
renders already agreeing.

## Flags

| flag | effect |
|---|---|
| `--title "<text>"` | required — the intro card's on-screen title |
| `--artist <slug>` | required — resolves the outro's name + links from `artists.json` |
| `--out <path>` | override the output path (default below) |
| `--intro-seconds 2.5` | intro duration, 1.5–4s (default 2.5) |
| `--outro-seconds 3.0` | outro duration, 1.5–4s (default 3.0) |
| `--keep-render` | keep the scratch Remotion render workdir for inspection instead of deleting it |

## Output convention

`spoken-word/` (and any sibling tree this skill is pointed at) has no
`youtube/<slug>/` substructure — a finished film just sits in its own named
folder next to nothing else that would collide with a bookended copy. So the
default output is the source's containing folder name, reused as the
filename:

```
spoken-word/<song>/<song>-musinique.mp4
```

e.g. `spoken-word/frump/Man Lip Syncing to Camera_5_ddv3.mp4` →
`spoken-word/frump/frump-musinique.mp4`. `--out` overrides when a different
location is wanted.

## Moving parts

- `skills/make/musinique-bookend/scripts/musinique_bookend.py` — this
  skill's one script
- `skills/make/musinique-bookend/artists.json` — the artist registry (13
  entries, see above)
- `runtime/remotion/src/scenes/MusiniqueIntroCard.tsx` — the front card:
  the musinique-logo-2 mark springs on, then the title sets in; a `*Demo`
  twin ships alongside with filled preview props
- `runtime/remotion/src/scenes/MusiniqueOutroCard.tsx` — the back card:
  the mark, `@Musinique`, the artist name, and the link list stagger in;
  a `*Demo` twin ships alongside
- both registered in `Root.tsx` under the `claude-musinique season 1`
  block, with `calculateMetadata` deriving `width`/`height`/`fps`/
  `durationInFrames` straight from props — that's what lets the render
  match any source canvas without touching the component
- `runtime/remotion/src/musinique-logo-2-path.ts` — the reused mark path
  data (73-subpath SVG, already vendored for the existing Musinique logo
  showcases); this skill draws on it rather than re-deriving the mark

## Smoke-tested, not production-rendered

This skill was verified end to end on a synthetic 6s, 3840x2160, 25fps,
48kHz-stereo clip (`ffmpeg -f lavfi color=... + sine=...`), never on a real
spoken-word film — those are multi-minute 4K masters and Bear has not yet
said which artist performs which one. Confirm the artist-to-film pairing
with Bear before running this on `spoken-word/frump/`, `spoken-word/goosey/`,
or `spoken-word/if/`.

## Example invocations

```bash
# smoke test — a synthetic clip, safe to run anytime
python3 skills/make/musinique-bookend/scripts/musinique_bookend.py \
    /tmp/smoke-source.mp4 --title "Smoke Test Song" --artist nik-bear-brown \
    --out /tmp/smoke-source-musinique.mp4

# real films — DO NOT RUN until Bear confirms the artist for each
python3 skills/make/musinique-bookend/scripts/musinique_bookend.py \
    "spoken-word/frump/Man Lip Syncing to Camera_5_ddv3.mp4" \
    --title "Frump" --artist <slug-bear-confirms>

python3 skills/make/musinique-bookend/scripts/musinique_bookend.py \
    "spoken-word/goosey/goosey-seedance_1_ddv3.mp4" \
    --title "Goosey" --artist <slug-bear-confirms>

python3 skills/make/musinique-bookend/scripts/musinique_bookend.py \
    "spoken-word/if/Man Singing to Camera_1_ddv3.mp4" \
    --title "If" --artist <slug-bear-confirms>
```
