---
name: post
description: >
  Publish-STAGING step for a finished brutalist reel — never an upload. `post`
  guarantees a clean broadcast master and stages it for YouTube: it makes SURE
  every beat is true 4K (2160p; re-renders any sub-4K beat), compiles the CLEAN
  final with NO review/beat markers or QC burn-in, generates the YouTube
  description as a sibling `.md` (same basename as the mp4, timestamped
  chapters from measured beat offsets), MOVES the hi-res 4K master + its `.md`
  into the TOPOST staging folder, runs a Topaz Video AI CLI pass to create a
  FURTHER-upscaled version that also lands in TOPOST, and records every staged
  video — files, resolution, duration, dates, meta — in a tracking JSON
  (`TOPOST/staged.json`). Use when the user types `post`, `stage`, `topost`,
  `publish-prep`, `stage for youtube`, or asks to 4K-finalize / upscale / stage
  a reel for upload. Staging only — the human does the actual upload.
---

> **STAGES, NEVER UPLOADS.** `post` is the bridge between a finished reel and
> the human's upload. It moves a clean 4K master (plus a Topaz-upscaled variant
> and a YouTube description) into the TOPOST folder and logs it. Putting the
> file on YouTube stays a human action. This preserves the toolkit's
> never-publish law while giving the human an upload-ready pile.

# post — clean 4K, no markers, staged to TOPOST

Default staging root:
`/Users/bear/Documents/CoWork/bear-textbooks/books/youtube/TOPOST`
(override with `--to <dir>`). Everything `post` emits for a reel lands there:
the 4K master, the Topaz-upscaled master, the `<slug>.md` YouTube description,
and an updated `staged.json` manifest.

## Preconditions (post refuses a reel that isn't done)

1. The reel is complete — zero slates, every beat real motion.
2. **GATE T (type-lock) is green** — `TYPECHECK.md` exists with no FAIL (the
   `kerning` skill). A reel with broken type does not get staged.
3. Audio is locked; the beat sheet measures out to the master clock.

If any precondition fails, `post` STOPS and says which — it does not stage a
half-finished or type-broken reel.

## The four guarantees `post` enforces

### 1. Every beat is true 4K (2160p)

"4K master" is a lie if a beat was rendered at 1080 and stretched. `post`
audits **per-beat source resolution** and re-renders any beat below 2160p at
2160p before the final compile — Manim and Remotion both render at 2160
natively; a beat's clip must be born 4K, not upscaled into the composite.
- Audit: probe each beat's rendered clip (`ffprobe` height). Any `< 2160` →
  re-render that beat at 2160 (its lane's render path), recompile only changed
  slots.
- The final compile is `./art final <slug>` (defaults to `--height 2160`) — the
  clean master path, NOT `./art run` and NEVER `--review`.

### 2. No beat markers / no burn-in

The review cut carries burn-in labels (beat id, lane, timing — e.g.
`A2M MANIM 94.4s +18.3s`, `A1C CARD VIDEO 22.6s`) and any QC overlay. The
staged master must have NONE.
- Use only `./art final` (review burn-in is a `--review`-only feature).
- **Assert it:** sample frames from the compiled master and confirm no
  bottom-corner marker band / debug overlay survives. A frame with a marker =
  FAIL, re-compile clean. Never stage a marked master.

### 3. A YouTube description travels with the video

Emit `<slug>.md` (same basename as the mp4, `.md` not `.mp4`) beside the master
in TOPOST. If the reel already has a description, refresh it; otherwise generate
from the beat sheet:
- **Title** (the reel's title).
- **Description** — 2–4 sentence hook from the cold open + verdict.
- **Chapters** — timestamped list built from MEASURED beat offsets (act cards
  become chapter marks: `0:00 Intro`, `1:12 The Two Teams`, …). YouTube needs
  the first stamp at `0:00`.
- **YOUR TURN** prompt (the reel's handoff), the channel line
  (@NikBearBrown / Liam-in-for-Bear), sources/credits, hashtags.

### 4. A Topaz CLI upscale produces a further-upscaled variant

After the clean 4K master exists, run **Topaz Video AI via the command line**
to produce a further-upscaled version that ALSO sits in TOPOST
(`<slug>-topaz.mp4`, or `<slug>-8k.mp4` if scaling to 4320p).
- Invoke Topaz's bundled `ffmpeg` with a `tvai_up` filter, e.g. (macOS, adjust
  to the installed Topaz version/model):

  ```bash
  export TVAI_MODEL_DIR="/Applications/Topaz Video AI.app/Contents/Resources/models"
  export TVAI_MODEL_DATA_DIR="$TVAI_MODEL_DIR"
  TOPAZ_FFMPEG="/Applications/Topaz Video AI.app/Contents/MacOS/ffmpeg"
  "$TOPAZ_FFMPEG" -i "<slug>.mp4" \
    -vf "tvai_up=model=prob-3:scale=0:w=7680:h=4320" \
    -c:v hevc_videotoolbox -profile:v main -b:v 120M -tag:v hvc1 \
    -c:a copy "<slug>-topaz.mp4"
  ```

- **Detect first.** If the Topaz ffmpeg binary isn't found, LOG it and stage
  without the Topaz variant (record `topaz.ran = false`, `reason`) — a missing
  Topaz install is not a reason to fail the whole stage. Do not substitute a
  plain ffmpeg scale and call it "Topaz."
- Model/scale are config (`--topaz-model`, `--topaz-height`); default to a
  high-fidelity model at 4320p. State the model + output resolution in the log.

## The move + the manifest

1. **MOVE** (not copy) the clean 4K master into TOPOST, alongside `<slug>.md`.
   The reel folder keeps its `beat_sheet.json` and build paperwork, so the reel
   stays rebuildable; the shippable mp4 now lives in TOPOST.
2. Place the Topaz variant in TOPOST too.
3. **Update `TOPOST/staged.json`** — append or update (by `slug`) one entry.
   Never overwrite unrelated entries; the manifest is additive/idempotent.

```jsonc
{
  "videos": [
    {
      "slug": "claude-liam-deep-08-agentic-ai",
      "title": "Agentic AI, Overpromised?",
      "source_reel": "books/computational-skepticism-for-ai/youtube/claude-liam-deep-08-agentic-ai/",
      "staged_at": "2026-07-24T14:05:00-04:00",   // date + time, America/New_York
      "files": {
        "master_4k": "claude-liam-deep-08-agentic-ai.mp4",
        "topaz_upscale": "claude-liam-deep-08-agentic-ai-topaz.mp4",
        "description_md": "claude-liam-deep-08-agentic-ai.md"
      },
      "resolution": "3840x2160",
      "duration_s": 372.4,
      "beat_count": 34,
      "all_beats_4k": true,
      "markers_clean": true,
      "gate_t": "pass",
      "topaz": { "ran": true, "model": "prob-3", "output_res": "7680x4320" },
      "status": "staged"          // human flips to "uploaded" after upload
    }
  ]
}
```

## Workflow

1. **check** — verify preconditions (complete, GATE T green, audio locked).
2. **4k-audit** — probe every beat; re-render any sub-4K beat at 2160; recompile.
3. **final** — `./art final <slug>`; frame-assert no markers/burn-in.
4. **describe** — write/refresh `<slug>.md` (timestamped chapters from measured
   offsets + boilerplate).
5. **move** — move master + `.md` into TOPOST.
6. **topaz** — detect Topaz ffmpeg; upscale into TOPOST (or log-and-skip).
7. **log** — upsert the `staged.json` entry (files, res, duration, dates, meta).
8. Report the TOPOST contents and the manifest row. STOP — the human uploads.

## Batch

`post sweep <youtube-dir>` — stage every complete + GATE-T-green reel under a
folder, one at a time; skip (and list) any reel not ready with the reason.
Unattended-safe: on a single reel's failure, log it, continue, report at the end.

## Hard rules

0. **HARD GLOBAL RULE — post to YouTube ONLY from TOPOST, never from any other
   directory.** A YouTube upload is permitted only for a hi-res staged master
   physically in `/Users/bear/Documents/CoWork/bear-textbooks/books/youtube/TOPOST/`
   with a matching `staged.json` entry. Never upload from a reel's
   `<book>/youtube/<slug>/`, from `mp4/`, or anywhere else. Staging via `post`
   is the ONLY thing that makes a reel uploadable. No exception, no override.
1. **Never upload.** Staging to TOPOST is the end of `post`.
2. **No stretched 4K.** Every beat is born 2160p or gets re-rendered; the
   composite is never upscaled to fake 4K (the Topaz pass is a SEPARATE,
   labeled further-upscale of the true master).
3. **No markers ship.** Clean `./art final` only; frame-assert it.
4. **Type gate first.** No GATE-T-failing reel is staged.
5. **Manifest is additive.** Update by slug; never clobber other entries.
6. **Move means move.** The shippable master lives in TOPOST after `post`; the
   reel folder retains the beat sheet for rebuilds.

## Output contract

```
books/youtube/TOPOST/
  <slug>.mp4            clean 4K master (moved here)
  <slug>-topaz.mp4      Topaz further-upscaled variant
  <slug>.md             YouTube description (timestamped chapters + boilerplate)
  staged.json           tracking manifest (meta + dates), additive
```
