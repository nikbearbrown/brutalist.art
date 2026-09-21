---
name: seis-composite
description: >
  Assemble seis-extract clips into the SEIS alumni impact film per the editing brief: opening
  "who they are now" spotlight beat → the turning point → what that became → facing forward →
  the closing beat → a bridge card ("The name is changing. The mission isn't.") → the static SEIS
  end slide. Kinetic NEU-brand text cards between sections, an optional stat card before the
  close, an optional music bed ducked under speech, ~2:00 target. Input is a plan.json that IS the
  brief's timeline as data; output is one mp4 via the `SeisFilm` composition. Use when the user
  types `seis composite`, `seis compose`, `assemble the alumni video`, or points at a folder of
  seis-extract clips + a brief. Never publishes.
---

# seis-composite — clips → the alumni film

## The brief's timeline, as data
```json
{"open":   {"eyebrow": "SEIS · Alumni", "lines": ["Look what our people", "have gone on to do."], "seconds": 4},
 "sections": [
   {"eyebrow": "Who they are now",   "clips": ["clips/jay-01.mp4", "clips/jainil-01.mp4", "clips/hemant-01.mp4"]},
   {"eyebrow": "The turning point",  "lines": ["A course. A professor.", "A co-op through the program."], "clips": ["…"]},
   {"eyebrow": "What that became",   "clips": ["…"]},
   {"eyebrow": "Facing forward",     "clips": ["…"]},
   {"eyebrow": "",                   "clips": ["clips/jainil-ceo.mp4"]}],
 "stat":   {"eyebrow": "SEIS", "lines": ["112 spotlight stories", "…"], "emphasis": 0, "seconds": 4},
 "bridge": {"lines": ["The name is changing.", "The mission isn’t.", "This is SEIS."], "emphasis": 2, "seconds": 4, "dark": true},
 "end_seconds": 10, "music": "bed.mp3", "music_gain": 0.12}
```
```
python3 runtime/scripts/seis_composite.py plan.json --out alumni-impact-rough.mp4
```

## Editing laws (from the brief)
- **Open on impact, not backstory** — `now` clips first; the first thing heard is a role/company/team size.
- **Speed-up moment** — in *What that became* / *Facing forward*, stack 3–4 punchy fact-clips back
  to back (one per alum, no lingering). seis-extract makes these short by cutting `in`/`out` tight.
- **The closing slide is earned** — put the single most emotionally full line immediately before the
  bridge (Jainil's "Nokia CEO" is the brief's candidate).
- **Stat card only with a REAL number** (alumni count, companies, placement rate) — never invented.
- **Music subtle and steady**, voices lead; a slight lift into the close, no swell.
- **Department over institution** on every card: the eyebrow names SEIS / the program.
- **Bridge + end slide**: ~2–4 s text card, then ~10 s static SEIS slide (primary logo, "This is
  SEIS." — swap in the approved tagline if SEIS supplies one).
- **≤ 15 s per clip**, ~2:00 total; the script prints the total so you cut before rendering.

## What it refuses
- Re-cutting inside a clip (the extract sidecar is the audit trail; change the pull instead).
- A stat with no source. A tagline SEIS hasn't approved. Any publish step.
