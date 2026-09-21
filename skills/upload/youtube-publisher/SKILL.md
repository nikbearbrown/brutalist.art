---
name: youtube-publisher
description: >-
  Turn NotebookLM video downloads into published, chapter-ordered YouTube episodes on
  the @MedhavyAI channel. Use this whenever the user has NotebookLM .mp4 files (e.g. in a
  notebooklm/ folder) they want posted to YouTube, mentions "NotebookLM video", "post to
  Medhavy", "Quantum Mechanics NotebookLM playlist", wants a Whisper transcript + timestamped
  YouTube description for a video, wants a Medhavy Remotion intro/outro wrapped around a
  NotebookLM deep dive, or wants videos matched to book chapters and added to a playlist in
  chapter order. Trigger even if they only say "publish these deep dives" or "sandwich this
  with the Medhavy bookends" — this skill owns that whole pipeline.
---

# NotebookLM → YouTube (Medhavy)

NotebookLM produces a finished narrated video. This skill does **not** re-explain the
content — it treats the NotebookLM `.mp4` as the body of the episode and does the
publishing work around it: transcribe it, match it to a book chapter (which sets its
place in the playlist), write a real YouTube description with timestamped topics, wrap
it in a narrated Medhavy Remotion intro and outro, and post it to **@MedhavyAI** into a
named playlist **in chapter order**.

The heavy pieces already exist elsewhere in the repo and are **reused, not rebuilt**:
Kokoro or nbb narration (`generate_audio_kokoro.py` / `generate_audio_nbb.py`), the `MedhavyOpen` / `MedhavyOutro` Remotion scenes,
and the YouTube OAuth pattern. This skill only adds the NotebookLM-specific glue.

## When you're done, the video looks like this

```
[ Medhavy intro beat  B00 ]  Remotion MedhavyOpen  + AI narration  (~11s)
[ NotebookLM deep dive B50 ]  the raw .mp4, untouched, its own audio  (N min)
[ Medhavy outro beat   B99 ]  Remotion MedhavyOutro + AI narration  (~9s)
```

One folder per video, named by slug, holding `beat_sheet.json`, `mp3/`, `media/`,
`mp4/[slug].mp4` (the upload master), `chapters.json`, `description.txt`, and
`[slug]-youtube.md`.

> **Voice selection is governed by `VOICE-LOCK.md` (repo root).** Bookend narration uses Kokoro `am_onyx` (free, `generate_audio_kokoro.py`) or nbb for Bear's voice (free, `generate_audio_nbb.py`). No ElevenLabs. No audio spend gate.

## Before you start — dependencies and secrets

These run on a machine with network access (not the sandbox). Confirm/install:

- `pip install faster-whisper mutagen requests google-api-python-client google-auth-oauthlib google-auth-httplib2`
- `ffmpeg`/`ffprobe` on PATH; `node`/`npx` for Remotion; the Remotion project's `node_modules` installed (`npm ci` in the remotion dir once).
- `NBB_CKPT (or SSH alias aicr)` in the environment (for the intro/outro voice).
- YouTube OAuth: `client_secret.json` + a first-run consent that mints `youtube_token.json`. **This is the one thing only the user can provide** — walk them through `references/youtube-setup.md` if it's not set up. Never invent credentials.

Reused-tool locations default to the repo layout; override with `--scripts-dir` /
`--remotion-dir` or the env vars `MEDHAVY_SCRIPTS_DIR` / `MEDHAVY_REMOTION_DIR`:

- generate_audio.py → `skills/make/sketch-explainer/scripts/`
- Remotion project → `runtime/remotion/` (has `src/index.ts`, `MedhavyOpen`, `MedhavyOutro`)

The Medhavy voice, palette, and brand strings are fixed constants — see
`references/medhavy-brand.md`. Don't guess them.

## The pipeline

Per video, run the orchestrator — it chains all build steps and stops before upload:

```bash
python scripts/pipeline.py path/to/Video.mp4 --chapters path/to/chapters
```

That is the fast path. Below is what each step does and where **a human must decide**,
because two steps produce drafts that should not be posted unread.

### 1. Transcribe (`transcribe.py`)
faster-whisper → `Video.transcript.json` (segments with timestamps) + `.txt`. The `small`
model is a good default for clear NotebookLM narration; bump to `medium` if accuracy matters.

### 2. Match to a chapter — HUMAN GATE (`match_chapter.py`)
TF-IDF ranks every chapter; the top hit sets the **chapter number**, which sets the
**playlist position**. The auto-match is usually right and well-separated, but show the
user the ranking and confirm before continuing — a wrong match silently reorders the
playlist. Override with `--chapter path/to/NN-*.md`.

### 3. Beat sheet (`build_beatsheet.py`)
Writes `beat_sheet.json` with B00 (MedhavyOpen intro), B50 (the raw NotebookLM video),
B99 (MedhavyOutro). The intro narration names the video + chapter; the outro is the
standard Medhavy sign-off. Only B00/B99 ever get TTS.

### 4. Bookend audio (`generate_audio_kokoro.py --only B00 B99`)
Kokoro (or nbb for Bear's voice) generates the intro and outro narration and writes real durations back. **B50 is never
sent to TTS** — the NotebookLM audio is already there.

### 5. Render bookends (`render_bookends.py`)
Renders `MedhavyOpen`/`MedhavyOutro` via Remotion, lays the narration on each, freezing
the last frame so the voice never clips → `media/B00.mp4`, `media/B99.mp4`.

### 6. Sandwich (`sandwich.py`)
Normalizes all three segments to one canonical format (1920×1080, 30 fps, h264, AAC) —
this matters because Remotion and NotebookLM outputs differ and ffmpeg's concat corrupts
mismatched inputs — then concatenates → `mp4/[slug].mp4`, the upload master.

### 7. Chapter markers (`chapter_markers.py`)
Proposes YouTube timestamped chapters from the transcript, **offset by the real intro
length** (so the timestamps point at the right place in the final video). Labels come in
as `[rewrite me]` with a snippet — they are placeholders.

### 8. Description — HUMAN GATE (`build_description.py`)
Seeds `[slug]-youtube.md` in the Medhavy house style (hook, "What you'll learn", "The
physics", timestamped chapters, brand footer, hashtags). The seeded hook is the chapter's
first paragraph and the chapter labels are raw snippets — **rewrite them**. Turn each
`[rewrite me]` into a real topic title, sharpen the hook, and fill "The physics" with the
chapter's key result and numbers. Then flatten to the upload text:

```bash
python scripts/build_description.py [folder] --refresh
```

### 9. Publish in chapter order — HUMAN GATE (`publish_playlist.py`)
Uploads every folder not yet posted and adds each to
**"Quantum Mechanics Volume 1 (NotebookLM)"** at its chapter position, so the playlist
reads in chapter order no matter what order you built things in.

```bash
# preview — no upload, no quota spent:
python scripts/publish_playlist.py --root path/to/notebooklm-videos --dry-run
# real:
python scripts/publish_playlist.py --root path/to/notebooklm-videos
```

Uploads default to **unlisted** (a fresh YouTube API project can't publish `public` until
Google approves an audit — see the setup reference). Confirm with the user before flipping
`--privacy public`, and confirm the chapter order printed in the dry-run first.

## Batch flow (many videos)

1. Run `pipeline.py` on each `.mp4` (they can share `--chapters`). Confirm each chapter match.
2. Refine each `-youtube.md`, run `build_description.py --refresh` on each.
3. One `publish_playlist.py --root [parent]` posts them all in chapter order.

Two NotebookLM videos can map to the same chapter (e.g. Ch 1 blackbody + Ch 1
photoelectric). That's fine — they'll sit adjacent in the playlist; order them by tweaking
titles or by uploading in the intended order.

## Notes on judgment

- The transcript and chapter match are cheap to redo; the upload is not. Treat steps 2, 8,
  and 9 as the places to slow down.
- If `chapter_markers.py` yields fewer than 3 markers, lower `--min-gap` or add markers by
  hand — YouTube needs ≥3 to render a chapter list.
- Keep the NotebookLM body untouched. The value of this skill is that it *doesn't* re-encode
  or re-narrate the deep dive; it only bookends and publishes it.

See `references/medhavy-brand.md` for the fixed brand constants and
`references/youtube-setup.md` for the one-time OAuth setup.

## Credentials (per channel)

OAuth credentials live in `youtube/credentials/[channel]/` (gitignored), each holding
`client_secret.json`, `youtube_token.json`, and `youtube_publish_ledger.json`. Choose the channel
with `ART_YOUTUBE_CHANNEL` (default `nikbearbrown`) or `publish_playlist.py --channel [name]`.
Most people have one channel; add more folders for multiple. `./art keys` validates the selected
channel's OAuth for free.

## Series cross-links (default ON)

The whole series funnels to one intro video and one master playlist. When publishing, the description
is automatically appended with a cross-link — no manual editing:

- **Short** (`--kind short`, or any `short/` subfolder — auto-detected) → points to the intro **video**
  "What is Brutalist?" (`ART_ANCHOR_VIDEO_URL`).
- **Long** (default) → points to the series **playlist** "Brutalist" (`ART_ANCHOR_PLAYLIST_URL`), and
  the video is also added to that playlist.

Both anchors are set in `.env` (`ART_ANCHOR_VIDEO_URL`, `ART_ANCHOR_PLAYLIST_URL`); blank either to
disable it, or pass `--no-anchor` to skip both. The append is idempotent — re-running won't duplicate
the link.

**Native Shorts "Related video" chip:** the YouTube Data API cannot set the native related-video link
that appears on a Short; that's a YouTube Studio / mobile-app action. The description link above is the
automatable funnel; set the native chip manually in Studio if you want it in addition.

**Credentials resolution:** the publisher now resolves `youtube/credentials/[channel]/` from the repo
root automatically (fixed a `parents[]` bug), so you no longer need `ART_HOME` set or `--client`/
`--token`/`--ledger` passed when running the script directly from the repo root.
