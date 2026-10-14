---
name: fellows
description: >
  Fellow-showcase reels for Humanitarians AI — wrap a fellow's OWN video
  report (a .mov/.mp4 they recorded) in the Claude-branded bookends and ship
  it as an episode on @HumanitariansAI. The fellow-selected narrator asks
  Claude "I wonder what Humanitarians AI fellow [name] has been working on
  lately…", then
  summarizes the work in 2–3 beats (from the faster-whisper transcript +
  frames pulled from the report), the fellow's video then PLAYS AS IS, and the narrator
  reads Professor Bear's notes (feedback + next steps — human-signed, GATE N),
  a "Your turn" handoff invites the viewer to dig deeper with a prompt, and
  the standard Humanitarians AI outro closes. Use when the user types
  `fellows [video|folder]`, `fellow report`, `fellow showcase`, or drops a
  fellow's report video and asks to wrap/publish-prep it. Sibling of
  ai-explainer (same skeleton, different middle: the middle IS the fellow's
  video). Audio-first except the report beat (the report's own runtime is
  that beat's clock). The fellow chooses one persistent Kokoro voice. Never publishes.
---

# fellows — the Humanitarians AI fellow-showcase reel

A fellows video answers one question — *what has this fellow been building?* —
and lets the fellow answer most of it themselves. The reel is a frame around
their own report: the selected narrator sets it up, the report plays untouched, Professor Bear
responds, the viewer gets a prompt to go deeper. The skill's job is the frame,
never a re-edit of the fellow's work.

For the weekly two-video/four-file requirement and browser-only GitHub/Drive
handoff, follow [FELLOWS-SUBMISSION.md](../../../docs/FELLOWS-SUBMISSION.md).
Runtime approval records and safe-export commands are specified in
[PIPELINE-SAFETY.md](../../../docs/PIPELINE-SAFETY.md). This fellows workflow does
not generate or deliver captions. Research transcription is text, not a CC track.

## The shared skeleton (a sibling of ai-explainer / cli-explainer)

Same Claude-branded bookends as the siblings; the MIDDLE is the fellow's own
video plus commentary around it:

1. **Beat 0 — the Claude composer** (`ClaudeComposerAsk`, COLD OPEN LAW).
2. **Middle — what differs:** 2–3 summary beats → the report AS IS → Professor
   Bear's notes.
3. **Second-to-last — "Your Turn"** (`greeting: "Your turn."`).
4. **Last — the STANDARD HUMANITARIANS AI OUTRO** (deliberate deviation from
   the siblings' title-restate outro — see OUTRO, below).

## GATE L — library-first (ask the library before you author a beat)

Before a beat is authored, routed to Manim, slated, or written up as a request
card, ASK WHAT ALREADY EXISTS:

```bash
./art scenes "what the beat needs, in plain words"
./art scenes --check <ComponentName>     # is that name actually renderable?
```

The library is bigger than any session can hold in its head — which is exactly
how a reel ends up with beats slated while a purpose-built component sits unused
two directories away. A hit is a **LEAD**, not a verdict: read the desc and the
props before trusting it. A candidate tagged `[derived text — open the file]`
has no header of its own; the search text was assembled from file evidence.

A genuine miss is a **PUNT**, and a punt is a design card: build the component
and the next reel finds it forever. The search logs the miss to
`TEMPLATE-MISSES.md` by itself (`--reel <path>` records who needed it). **A miss
is never a licence to slate.**

After adding a component, run `./art scene-index` — a component that is not in
the index cannot be found by anyone, including you next week.

## Trigger

```
fellows [video-file | fellow-folder] [--fellow "Full Name"] [--project "Project Name"] [--out dir]
```

Also: "fellow report", "fellow showcase", "wrap [video] for Humanitarians".
Input is typically a raw recording dropped into `fellows/` (e.g.
`fellows/Causal Couture Phase 3 Report.mov`). If `--fellow` is not given and
the name is not in the filename or spoken in the transcript, ASK the human —
never guess a person's name (HONESTY, sharpened for people, per the
ai-explainer profile modifier).

## Persistent fellow voice

Each fellow chooses one Kokoro voice before the first report is generated and
keeps it across the whole report series. Store the choice in the fellow-level
README or profile and repeat the same `engine: "kokoro"` and voice ID in every
episode's metadata and narration beats.

When the fellow has not supplied a preference, use the name only as a starting
heuristic: female-coded names receive an `af_*` suggestion and male-coded names
receive an `am_*` suggestion. This is not an identity claim. The fellow's
explicit preference always overrides the heuristic. A later voice change is a
documented re-voice decision for the series, never a silent per-episode choice.

## Brand facts

| Slot | Value |
|---|---|
| Channel | `@HumanitariansAI` — folder chip and HAI logo bug on every beat (LOGO LAW; full-size on the outro). |
| Persona / voice | **Fellow-selected narrator** — one persistent Kokoro voice per fellow. The fellow's explicit choice and human approval are required; a suggestion is not approval. Record `voice_policy`, the selected voice ID, and the fingerprint-bound `metadata.approvals.voice` record. |
| Skin | Claude fidelity skin for the composer bookends (`tokens/claude.ts` — never retint); RESULT/notes graphics render in the **humanitarians palette** (`tokens/humanitarians.ts`) per ASK→RESULT LAW. |
| Register | Teardown-warm, celebratory-but-honest (the profile-modifier rule): make the fellow's invisible work visible; any skepticism points at the problem space, never at the fellow. Professor Bear's notes are the honest-feedback beat — that's where critique lives, and it is constructive by construction. |
| Output | `fellows/[first-name-last-initial]/[YYYY-MM-DD-short-weekly-description]/` — all lowercase kebab-case. |

## The required beat spine

```
B00  INTRO       ClaudeComposerAsk cold open. command = "I wonder what
                 Humanitarians AI fellow [Name] has been working on lately…"
                 — the ask lands ANSWERED (output lines: project name, phase,
                 one-line what-it-is). greeting: `Fellows, [Name]` (the
                 profile-modifier pattern — the subject takes the persona
                 slot; overrides the world-language hello). Narration: the selected narrator
                 introduces the report and fellow. For weekly submissions, the
                 opening narration follows the required "Hi, I am [your name]
                 and this video is about [summary of the topic]" line; branded
                 bookends do not displace it. Disclose AI narration clearly.
B01–B03  THE WORK   2–3 beats. The selected narrator summarizes what the fellow built — from
                 the transcript, one idea per beat. Visuals: frames pulled
                 from the report (Ken Burns; FELLOW'S-WORK carve-out, below)
                 and/or rebuilt graphics in the humanitarians palette.
                 SPARK-LINE LAW binds where composer chrome appears.
B04  THE REPORT  The fellow's video PLAYS AS IS — pass-through beat.
                 media/B04.mp4 is the transcoded report; its OWN audio and
                 OWN runtime are kept. No trimming, no retiming, no voiceover
                 (THE REPORT IS THE CLOCK, below). Brand bug stays (LOGO LAW).
B05–B06  PROFESSOR BEAR'S NOTES   The selected narrator reads Bear's notes — one beat of
                 feedback (what's strong, what to tighten), one of NEXT
                 STEPS. Notes-card visuals, humanitarians palette. The
                 narration frames it explicitly: "Professor Bear's notes —"
                 GATE N governs (below).
B07  YOUR TURN   HANDOFF LAW unchanged: ClaudeComposerAsk, greeting
                 "Your turn.", runningText "paste this into Claude…",
                 command = a prompt that digs into the fellow's topic, repo,
                 or method — read ALOUD and discussed, never just typed.
B08  OUTRO       The STANDARD Humanitarians AI outro (OutroSeries / OutroCTA,
                 humanitarians palette, content from AUTHOR.MD's
                 Humanitarians AI section). The selected narrator signs off consistently.
                 **NOT** the @NikBearBrown outro — fellows is a HAI channel reel;
                 `ClaudeTitleOutro` and its lock (OUTRO-LOCK.md) do NOT apply here.
```

A **FELLOW CREDIT card** is required near the outro (on or beside B06): the
fellow's name, program/cohort, project name, and their public links VERBATIM
(GitHub, LinkedIn — only links that actually exist; never invent one).

## The transcript (whisper first, everything hangs off it)

Before any beat is authored, transcribe the report with **faster-whisper** for
research. Do not run the caption-delivery pipeline:

```bash
ffmpeg -i "[report].mov" -vn -ac 1 -ar 16000 transcript/report.wav
python3 -c "from faster_whisper import WhisperModel; ..."   # research transcription only
```

Write `transcript/report.txt`, retaining timestamps where useful for checking
claims. It feeds the summary beats, the draft of Professor Bear's notes and
`description.txt`. No `.srt`, caption burn-in or caption upload is required.

**Screenshots:** pull stills for the summary beats with
`ffmpeg -ss [t] -i "[report].mov" -frames:v 1 media/B01.png` — pick frames
that show the WORK (the demo, the chart, the interface), not the fellow's
face mid-sentence.

## Laws — inherited, plus three of this skill's own

All ai-explainer house laws bind (LOGO, SHOW-DON'T-TELL, FILL-THE-CANVAS,
DOUBLE-CHECK, VISUAL QC, SPARK-LINE, COLD OPEN, ASK→RESULT, HANDOFF,
never-publish). The fellows-specific law set:

- **THE REPORT IS THE CLOCK (the one exception to audio-first).** Everywhere
  else narration MP3s are the master clock. The report beat's clock is the
  report's own measured runtime; its own audio remains on the timeline. Transcode
  container/resolution to the reel spec (3840×2160 landscape or 2160×3840 vertical,
  h264/AAC, contain/letterbox — never
  crop or stretch), but never retime, trim, speed up, or talk over it. If the
  human wants a trimmed cut, that is an explicit request logged in
  BUILD-LOG.md — never the skill's own call.
- **SOUND REPAIR (the carve-out inside the carve-out).** "As is" protects the
  fellow's CONTENT and TIMING, not bad audio. If the report's sound is poor —
  quiet, clipped, hummy, roomy, wildly uneven — FIX IT in the transcode step,
  timing untouched: loudness-normalize to the narration (below), denoise
  (`afftdn`, or `arnndn` for stubborn hiss), high-pass the rumble/hum
  (`highpass=f=80`, plus a notch at 60/50 Hz if needed), and de-ess/limit
  clipping peaks. The MATCH rule is the point: the fellow's segment must sit
  at the same perceived loudness as the selected narrator's narration — a viewer should never
  reach for the volume knob at the splice.
  **The target is the narration's measured loudness, not a fixed number.** The
  pipeline does not normalize Kokoro narration (it lands around −21 LUFS), and
  staged masters must sit in GATE LOUDNESS's −28 to −18 LUFS window
  (`runtime/scripts/loudness_check.py`), so a fixed −16 would leave the report
  ~5 LU hot at the splice and can push a report-heavy reel over the ceiling.
  After step 4, measure the narration, then two-pass `loudnorm` the report to it
  with `linear=true` (gain only; no dynamics, no timing change):
  ```bash
  N=$(ffmpeg -hide_banner -i "concat:$(ls mp3/beat-*.mp3 | paste -sd'|' -)" \
        -af loudnorm=print_format=summary -f null - 2>&1 | awk '/Input Integrated/{print $3}')
  # pass 1: ffmpeg -i report.mov -af loudnorm=I=$N:TP=-1.5:LRA=11:print_format=json -f null -
  # pass 2: loudnorm=I=$N:TP=-1.5:LRA=11:measured_I=…:measured_TP=…:measured_LRA=…:measured_thresh=…:offset=…:linear=true
  ```
  If `N` itself falls outside −28 to −18 LUFS, stop and flag it: the narration,
  not the report, needs attention. Log `N`, both passes' measurements and the
  final filter in BUILD-LOG.md. Never pitch-shift, never
  time-stretch, never re-voice. Every filter applied is logged in
  BUILD-LOG.md; if the audio is beyond repair (unintelligible passages),
  flag it to the human with timestamps instead of shipping a bad segment.
- **FELLOW'S-WORK carve-out (of REBUILD LAW).** Frames and clips from the
  fellow's own report play as THEMSELVES — like the ACTUAL-CODE LAW in
  cli-explainer, the fellow's artifact is the receipt; rebuilding it would
  falsify it. Everything that is NOT the fellow's own material (context
  diagrams, comparison charts, the notes cards) is rebuilt native, REBUILD
  LAW unchanged.
- **GATE N — Professor Bear's notes are BEAR'S words.** The skill DRAFTS
  `NOTES.md` (feedback + next steps) from the transcript, in Bear's plain
  register, as a starting point — but the notes beats never go to audio until
  Bear has edited or signed `NOTES.md`. The selected narrator reads them AS Bear's notes
  ("Professor Bear's notes—"), so shipping an unsigned draft is
  impersonation, not a shortcut. GATE N is logged in BUILD-LOG.md and bound to
  the notes and exact spoken text in `metadata.approvals.professor_notes`.
  The runtime blocks pending or stale records; `--no-gate` is not a bypass.
  Never have an AI sign a human's approval record.
- **HONESTY (people-sharpened, from the profile modifier).** Only claims the
  fellow's own report makes — never invent an accomplishment, metric, quote,
  credential, or link. Soft attributions stay soft. Log the source video
  filename, duration, and transcription date in SOURCES.md.

## Flow

1. **Transcribe** (free): faster-whisper → `transcript/`; pull candidate
   stills; measure the report's duration.
2. **Author** `beat_sheet.json` in the spine above + draft `NOTES.md` +
   `description.txt`. Metadata: `audience: "Humanitarians AI"`,
   `palette: "claude"` bookends / `humanitarians` results, `engine: "kokoro"`,
   `voice: "[fellow-persistent-kokoro-id]"`, `voice_policy:
   "persistent-fellow-selected"`, `profile: "fellow-report"`,
   `register: "Teardown-warm"`. B04 declares `kind: "source_report"`,
   `clock: "source"`, `audio_policy: "preserve"`.
3. **Human gates** — the fellow approves the persistent voice; Bear reviews
   `NOTES.md` and its exact spoken wording. Inspect `art approvals [reel]
   --fingerprints` and record only real sign-offs as described in PIPELINE-SAFETY.
4. **Audio**: `python3 runtime/scripts/generate_audio_kokoro.py [reel]` — narration
   beats only; B04 is pass-through.
5. **Transcode the report** into `media/B04.mp4` (letterboxed, own audio) —
   applying SOUND REPAIR here if the report's audio needs it (loudness matched to
   the narration measured from step 4's MP3s; denoise/high-pass as required; log
   filters in BUILD-LOG.md).
6. **Render + assemble**: Remotion beats via
   `runtime/scripts/remotion_scenes.py [reel]` (foreground), then
   `art run [reel]` — review only; conform to audio everywhere and the report's
   runtime on B04. `art vertical [reel]` prepares a separate full-length portrait
   sheet; finish its native portrait graphics and render it independently.
7. **QC**: the frame-level VISUAL QC LAW pass (sample frames, 9-point rubric,
   `_qc/REPORT.md`) — check the letterbox, the bug placement over the
   fellow's footage, visual legibility and sound continuity across the splice.
   `art final [reel]` requires the final gates; use height 2160 for landscape and
   height 3840 for the 9:16 master. Failed checks must not be presented as a final.
8. Ship `BUILD-PROMPT.md` beside the beat sheet, as every reel does. Human
   reviews. Source and small documents go to GitHub; videos and large media go
   to Drive. Notify the PM with both links. PM-approved review uploads go to the
   Q playlist; Professors Brown and Nina decide publication. No toolkit command
   uploads, schedules or publishes. See FELLOWS-SUBMISSION for the complete gates.

## Naming

Fellow folder: lowercase `first-name-last-initial`, for example `maya-r`.
Episode folder: `YYYY-MM-DD-short-description-of-that-weeks-work`, for example
`2026-07-10-building-the-verified-data-gate`. Title pattern:
`What's [Name] Building? — [Weekly Work]` (or the report's own title if it is
better).
