# Medhavy brand constants

These are fixed. Copy them verbatim; do not invent variants.

## Channel
- Handle: **@MedhavyAI**
- URL: **medhavy.com**
- Tagline: **AI-powered intelligent learning systems**
- Name meaning (for intro copy): "Medhavy" / मेधावी — Sanskrit for *intelligent* or
  *intellectually brilliant*.

## Voice (Kokoro)
- Engine: Kokoro, voice `af_kore` (free, local).
- Generate via `generate_audio_kokoro.py` with `metadata.voice_kokoro: "af_kore"`.
- Pronunciation: send the literal word "Medhavy" to TTS. In narration text, spell out
  "A-I" (not "AI") so it's read as letters, and "dot com" (not ".com").

## Remotion bookends (project: runtime/remotion, src/index.ts)
- **MedhavyOpen** (intro). Props:
  - `topic`: string (short, upper-case topic line)
  - `lines`: string[] (brand + video/chapter lines)
- **MedhavyOutro** (outro). Props:
  - `brand`: "Medhavy"
  - `tagline`: "AI-powered intelligent learning systems"
  - `handle`: "@MedhavyAI"
  - `url`: "medhavy.com"

## Palette (Okabe–Ito, colorblind-safe)
- ground / cream: `#F0EAD6`
- data / allowed / energy: teal `#009E73`
- annotation / ratio: crimson `#D55E00`
- highlighter: `#F0E442`
- All body text: ink (near-black).

## Description footer (goes at the bottom of every description)
```
Medhavy · AI-powered intelligent learning systems · @MedhavyAI · medhavy.com
A NotebookLM deep dive, bookended and published by Medhavy.
```

## Default hashtags
```
#QuantumMechanics #Physics #NotebookLM #Medhavy #QuantumPhysics #PhysicsExplained #DeepDive #ScienceEducation
```

## YouTube defaults
- Category: 27 (Education)
- Default privacy: `unlisted` until the channel's API project passes Google's audit,
  then `public`.
- Playlist: **Quantum Mechanics Volume 1 (NotebookLM)** (created if missing).
