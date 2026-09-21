---
name: seis-extract
description: >
  Turn a SEIS alumni interview recording (Teams/Zoom mp4) into branded Q&A clips: for each pull in
  a brief, Bella (Kokoro af_bella — the SEIS interviewer's voice) asks the question while it types
  onto a SEIS page (NEU brand, Lato), then the alum answers — the interview segment full-frame with
  a slow reframe, a lower third that names the PROGRAM explicitly (name · program · grad year ·
  title · company) and burned captions from the transcript's word timings. Two steps:
  `transcribe` (faster-whisper, word timestamps → a timestamped transcript to choose pulls against
  the editing brief) and `cut` (pulls.json → clips + sidecars). Answer clips are capped at ~15 s.
  Many interviews, one grammar. Use when the user types `seis extract`, `seis extractor`,
  `extract clips from <interview>`, or drops an alumni interview + a brief. Sibling of
  `seis-composite` (assembles the clips into the film). Free, local. Never publishes.
---

# seis-extract — interview → branded Q&A clips

## Why a question first
An interview answer lifted cold is a talking head. The same answer after a typed question on the
SEIS page is a *story beat*: the viewer knows what was asked, the program's name is on screen
before the alum speaks, and every clip shares one grammar so `seis-composite` can cut them together
at pace. Bella asks; the alum answers; the program is named. That's the whole skill.

## Inputs
- The recording (`*.mp4`, any resolution — letterboxed to 1920×1080).
- The editing brief (Erin's "Alumni Impact Video — Editing Brief" or its successor) — it decides
  WHICH lines are worth pulling. Its laws are restated below because they govern pull selection.
- `pulls.json` — what you write after reading the transcript against the brief:
  ```json
  {"alum": {"name": "Dhanvardini Rajendran", "program": "MS Information Systems · SEIS", "gradYear": "2025", "title": "…", "company": "…"},
   "pulls": [
     {"id": "dhan-01", "section": "now",           "question": "What do you do today?",                     "in": "0:19", "out": "0:33"},
     {"id": "dhan-02", "section": "turning-point", "question": "Which course or professor changed things?", "in": "3:19", "out": "3:33"}]}
  ```
  `section` ∈ now · turning-point · became · forward · closing (the brief's timeline). `in`/`out`
  are the ANSWER bounds in the recording. The question is yours to write — short, spoken-natural,
  in Bella's voice (she is the interviewer, not a narrator).

## Anchoring pulls without hand-timing
`in`/`out` may be `"~a phrase"`: the extractor finds it in whisper's word timings (in = phrase start,
out = phrase end + 0.25 s). Whisper mis-hears names (Dhunvardini, Karl Bugraura, Tejas Parik) — put every
such name in `corrections` (it fixes the burned captions) and the anchor matcher then tries both spellings,
so you can copy phrases from the Teams .docx transcript. If a phrase still misses, read `<stem>.transcript.md`
and anchor on whisper's words. Choose anchors that bound ≤ 15 s of speech — slow talkers need tight phrases.
Teams .docx transcripts (speaker-labelled, correct names) are the better source for CHOOSING pulls;
whisper is only the clock.

## Flow
```
python3 runtime/scripts/seis_extract.py transcribe "<interview>.mp4"          # → <stem>.transcript.md (+ .json)
# read the transcript against the brief; write pulls.json
python3 runtime/scripts/seis_extract.py cut "<interview>.mp4" --pulls pulls.json --out clips/
```
Per pull: Bella's mp3 (Kokoro af_bella) → the question card typed to her clock → the segment cut
(ffmpeg, 1080p30) → captions chunked from the transcript's words (≤ 6 words / ≤ 2.4 s per chunk) →
Remotion `SeisQA` renders `clips/<id>.mp4` + `clips/<id>.json` (section, alum, seconds, source).

## Pull-selection laws (from the brief — these decide what gets cut)
1. **Department over institution.** Pull the line that names a course, a professor, a co-op through
   the program, a project, an award. A line that only proves "Northeastern is good" is too broad.
2. **Specificity over sentiment.** "Won a global hackathon with four teammates from the program"
   beats "it was a great experience". Fact-lines forward.
3. **Celebrate the person.** Every alum gets at least one pull that is clearly *their* moment
   (`section: now` with the most impressive fact first — role, company, team size).
4. **≤ 15 s per answer.** It's a highlight reel. The script warns; the compositor warns again.
5. **The program is named on screen.** The lower third reads `MS Information Systems · SEIS`
   (or the alum's actual SEIS program), never just "Northeastern".
6. **One clear beat per section per alum.** Don't force every alum into every section.
7. **Honesty.** The question must be one the answer actually answers; never re-cut an answer to
   imply something the alum didn't say. Sidecars keep `in`/`out` and the source file for audit.

## Voice
Bella — Kokoro `af_bella` — is the SEIS interviewer's voice for questions ONLY (Liam `am_onyx`
remains the narrator on SEIS reels). Both free. Recorded in `brands/seis.md`.

## Output contract (what seis-composite reads)
`clips/<id>.mp4` (question + answer, 1080p30, captions burned, lower third) and `clips/<id>.json`.
Clips are self-contained; the compositor never re-cuts inside them.
