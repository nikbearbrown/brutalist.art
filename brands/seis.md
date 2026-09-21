---
name: seis
description: >
  SEIS (Software Engineering and Information Systems, Northeastern College of
  Engineering) brand spec — a UNIT variant of the `neu` brand. Same NEU palette
  (NU red / black / white / gold, Lato), same NEU brand laws, plus the SEIS
  spotlight bookends (SeisSpotlightOpen · SeisProfileCredit · SeisOutro) and the
  Spotlight register. Used by `brand_variant.py [reel] seis` and by the first-class
  `seis-profile` skill (one reel per COE spotlight story) and `seis-ai` (the
  unit's AI explainer) — different flows, one skin.
---

# seis — SEIS unit spec (child of `neu`)

SEIS is not a new brand. It is Northeastern's brand (`brands/neu.md`, tokens
`runtime/remotion/src/tokens/neu.ts`, Manim `ART_PALETTE=neu`) worn by one unit.
Everything `neu` locks stays locked here — `brands/neu.md` (palette, type, logos, laws), `runtime/design/NEU-DESIGN.md` (the constitution from brand.northeastern.edu) and `runtime/remotion/src/tokens/neu.ts` (the values). This file adds only the unit deltas.

## Inherits from `neu` — verbatim, not restated
Palette (white ground, NU black, NU red `#C8102E` as brand/emphasis ONLY — never
state, never "bad"), NU gold rare + large-area only, Lato throughout with
regular-weight headings and sentence case, no gradients / drop shadows /
categorical rainbow, every asset contains red. Logo clear-space and minimum-size
rules. Read `brands/neu.md` and the NEU visual constitution before touching a scene.

## Deltas

| Slot | Value |
|---|---|
| Brand key | `seis` (`brand_variant.py` AUD entry; `beat_sheet.seis.json` when forked from a reel — a fresh spotlight reel authors `beat_sheet.json` directly with this metadata) |
| Audience | Prospective + current SEIS students, alumni, faculty, industry partners — watching on SEIS's own channel, not Bear's |
| Register | **Spotlight** — the profile modifier's "celebratory-but-honest" warmth (ai-explainer §profile, rules 2–7) in Northeastern brand voice: sentence case, no hype, no superlatives the article didn't earn. Third person. Liam names himself once (B00) and signs off (BOUT); never "in for Bear" — this is an institutional channel |
| Voice | **Liam** — Kokoro `am_onyx` (free), in his own persona, third person ABOUT the subject. Greeting pattern (channel-convert, org channel): B00 opens "This is Liam, for SEIS.", BOUT signs "Liam, for SEIS." — never "in for Bear" (Bear is not the host on SEIS's channel). ElevenLabs override `ELEVENLABS_VOICE_LIAM`, opt-in only. ONE voice for the whole series |
| Interviewer voice | **Bella** — Kokoro `af_bella` — asks the questions in `seis-extract` alumni Q&A clips (the SEIS interviewer). Liam stays the narrator. Free |
| `channel_title` | `SEIS · Northeastern` until Erin Macri confirms the YouTube handle (`_confirm.youtube_handle`). Known socials from the SEIS announcement card: **`@nu_seis`** (LinkedIn, Instagram), **`@northeastern.seis`** (Facebook) — the outro carries `@nu_seis` |
| Logo | Two SEIS unit marks ship in `logos/seis/unit/` and `runtime/remotion/public/seis/` (from Bear, 2026-09-19): **`seis-button-logo.jpg`** — the tile "button", S·E·I·S on black, 160×160 — the top-right bug on every SEIS frame; **`seis-logo.png`** — the lockup, NU "N" + "Northeastern University / Software Engineering and Information Systems", 463×149 transparent — under the name in lower thirds and on the end slide. Scenes take `logo: 'seis/seis-button-logo.jpg'`, `lockup: 'seis/seis-logo.png'` (`SeisQA`, `SeisFilm`, `SeisLogoTechnique`); the spotlight bookends default to the official NU marks (`northeastern/official/monogram-red.svg` open, `primary-logo-red-black.svg` outro) per `logos/seis/README.md`. Both unit marks are low-res rasters (fine at 1080p, soft at 4K) — ask SEIS for SVG. NU brand law forbids re-drawing any mark. Clear space = the height of the "N"; never on a photo without a scrim; never red-on-red |
| Bookends | `SeisSpotlightOpen` (B00) · body · `SeisCard` recap (BVDT) · `SeisProfileCredit` (BHTF — replaces YOUR TURN; the handoff is the person's own links + "read the full story") · `SeisOutro` (BOUT). Claude composer scenes NEVER appear — the Claude UI is not the subject (ILLUSTRATE LAW) |
| Body cards | `SeisCard` (NEU Form A: white, Lato, one red rule) — the only text card. Manim fragments render under `ART_PALETTE=neu`. Claude-toned Remotion illustrations need a NEU retint logged as a decision before use |
| Outro CTA | The article's own URL ("Read the full story") — verified, never invented. Handle line only once confirmed |
| Music | None by default. Northeastern's channel is not the place for the NBB jingle family; the outro is silent unless SEIS supplies a licensed cue |

## Photo rule (the one place a lifted image is allowed)
The article's hero image may appear ONCE, on `SeisSpotlightOpen`, exactly as COE
published it (no filter, no duotone, no crop below the shoulders), credited in
`RIGHTS.md` with the article's own credit line ("Photo sourced from LinkedIn" /
"Courtesy photo"). Every other beat is REBUILT (REBUILD LAW). Re-publication of
these photos on YouTube is SEIS's call, not ours — the ledger carries a
per-reel rights row and the batch does not publish.
