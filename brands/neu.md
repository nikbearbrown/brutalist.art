---
name: neu
description: >
  Northeastern University brand spec for Brutalist reels — the palette, type,
  logos and laws every NEU-skinned scene obeys. Parent of `brands/seis.md`.
  Tokens: `runtime/remotion/src/tokens/neu.ts`; Manim `ART_PALETTE=neu`;
  constitution: `runtime/design/NEU-DESIGN.md` (from brand.northeastern.edu).
---

# neu — Northeastern University brand spec

**What this is.** The one page a designer or student needs to make a reel that
passes Northeastern brand review, with every value in this repo so a fresh
clone of `brutalist.art` is self-contained. When this file and
brand.northeastern.edu disagree, the Brand Center wins; fix this file, then proceed.
The long form is `runtime/design/NEU-DESIGN.md`.

## Palette (`tokens/neu.ts`)

| Role | Hex | Rule |
|---|---|---|
| Ground | `#FFFFFF` | White only. No cream, no off-white, no dark mode. |
| Ink / marks | `#000000` | NU black for all text and structure. |
| **NU Red** | **`#C8102E`** | Brand and emphasis ONLY. Never a state color, never "bad", never a warning. |
| Neutral | `#545454` | Secondary text, structure, "lost / bad" (the label carries meaning, not the hue). |
| Gridline | `#E3E3E3` | Hairlines only. |
| NU Gold | `#A4804A` | Ceremonial. Rare, large-area only; fails AA at small sizes. |
| Data series | `#C8102E` `#000000` `#545454` `#787878` `#C4C4C4` | Primary series is NU Red, the rest are greys. The categorical rainbow is forbidden. |

Every asset contains red somewhere. Red is never paired with green as good/bad.
No gradients, no drop shadows, no glows, no photo filters.

## Type

| Slot | Face | File |
|---|---|---|
| Everything | **Lato** | `runtime/remotion/public/fonts/Lato-Regular.ttf`, `Lato-Bold.ttf`; Manim copy `runtime/manim/fonts/Lato-Regular.ttf`; license `Lato-OFL.txt` (SIL OFL 1.1) |
| Data numbers, math | PT Mono | `runtime/fonts/PT_Mono/` |

Headings are regular weight, sentence case. Bold is for emphasis inside a line,
not for headings. Lato is bundled but must be loaded per scene with `useLato()`
(`tokens/lato.ts`), otherwise Chrome silently substitutes Helvetica.

## Logos

Official marks (Northeastern Primary Marks, trademark, never re-drawn) live in
`logos/seis/primary-marks/` (eps, png, svg; PMS, CMYK, RGB) with clean RGB SVG
copies in `runtime/remotion/public/northeastern/official/` for `staticFile()`.
The map from clean name to source file is in `logos/seis/README.md`.

| Use | File |
|---|---|
| Corner bug, opens | `northeastern/official/monogram-red.svg` (the N alone) |
| Outro, full size | `northeastern/official/primary-logo-red-black.svg` |
| On black or NU-red grounds | the `-white` variants |

Clear space equals the height of the N. The N is never smaller than 12 px.
Never red on red. Never on a photo without a scrim. The Wikimedia Commons
wordmarks in `logos/northeastern/` are superseded by the official set.

## Layout and motion

- Grid, whitespace and one red rule per card (NEU Form A: white, Lato, one red rule).
- Motion must carry the claim: a still frame of any beat should show what it is about.
- Charts: white ground, `#E3E3E3` gridlines, NU Red primary series, greys after.
- Photos appear as published, uncropped below the shoulders, credited; every other beat is rebuilt.

## Voice on NEU-branded channels

Sentence case, no hype, no superlatives the source did not earn. Third person.
The narrator names himself once at the open and signs off at the close.

## Children

- `brands/seis.md` — the SEIS unit variant (Software Engineering and Information Systems): adds the unit marks, the Spotlight register and the SEIS bookends.
