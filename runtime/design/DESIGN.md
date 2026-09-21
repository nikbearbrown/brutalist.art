# DESIGN.md — the Vox-explainer design constitution

The visual language for vox-explainer slate cuts. This is a **reference doc, not a
pipeline dependency** — the live values are the tokens in
`aspects/explainer/vox-explainer/manim/vox_graphics.py` and the Remotion token
sets; this file is what they must match, and what you point at when reviewing
("make the red hotter").

**Lineage, stated plainly:** the *motion-graphics grammar* (mixed media, the
two-axis shot system, newsprint collage) is a homage to Vox's explainer videos.
The **palette and type here are Bear's own**, NOT Vox's brand kit. Blue has been
intentionally removed from every palette here.

---

## Palette is a registry, keyed by `metadata.palette`

There is no single global palette anymore. Palette is one axis of the audience
system (see `AUDIENCES.md`) — a named token set the render imports. Every palette
fills the **same six role keys** (`CREAM`=ground, `INK`=text, `TEAL`=good/kept,
`CRIMSON`=bad/lost, `SLATE`=structure, `GOLD`=highlighter) with its own values,
so a scene retints by swapping the set, never by editing the scene.

| `metadata.palette` | look | ground | good/bad grammar | type | where it lives |
|---|---|---|---|---|---|
| **`teardown`** *(default)* | direct, minimalist | white | **red-vs-ink + label** | Montserrat / EB Garamond / PT Mono | below + `vox_graphics.py` |
| **`newsprint`** | warm editorial | cream | two hues (teal/crimson) | same | below |
| **`neu`** | Northeastern brand | white | **label + position only** (red is brand, never state) | **Lato** | below + `neu.ts` |
| `medhavy` | colorblind-safe | eggshell | two hues (Okabe-Ito) | same | `AUDIENCES.md` · `medhavy.ts` |
| `humanitarians` | muted editorial | cream | two hues (warm/cool) | same | `AUDIENCES.md` · `humanitarians.ts` |
| `musinique` | monochrome / SaaS-clean | white | **blue (#2563eb) as good; gray-700 as bad; label + position carry** | **Inter (humanist sans)** | `musinique-palette.md` · `musinique.ts` · `animated_graphics.py` |

**Default flipped (2026-07):** the house default was `newsprint` (cream / teal /
crimson / gold). It is now **`teardown`** — direct and minimalist, the NikBearBrown
brand. `newsprint` is preserved verbatim as an opt-in palette; nothing about it
changed except that it is no longer the default.

---

## `teardown` — the default (minimalist)

One accent. It is red. Nothing else on the plane gets a color — red earns its
place *because* it is the only color on the slide.

| role key | token | hex | role | on white (WCAG) |
|---|---|---|---|---|
| ground | `CREAM` | `#FFFFFF` | flat white plane — never cream, never warm paper | — |
| text | `INK` | `#2A1A0E` | all text + marks; warm near-black | ~16.8:1 · AAA |
| bad / lost / broken / "skip" | `CRIMSON` | `#C8102E` | the one accent — the mark under scrutiny | 5.9:1 · AA |
| good / kept / true / "apply" | `TEAL` | `#2A1A0E` | **plain ink** — good is not a second color; the label + side carry it | ~16.8:1 · AAA |
| structure | `SLATE` | `#545454` | entity cards, neutral scaffolding, axes | 7.6:1 · AAA |
| highlighter, fill only | `GOLD` | `#C8102E` @ ~14% (composited `#F6D8DC`) | the editor's-pen sweep — a wash of the one accent, behind serif emphasis | ink-on-tint stays AAA |
| hairline | *(added)* | `#D4D4D4` | dividers, card borders — not a text color | — |

### `teardown` color laws
1. **One accent, and it is red.** Red = the mark under scrutiny / the emphasis /
   the primary series. Do not introduce a second hue to mean "good."
2. **Good/bad is red-vs-ink, carried by label + position.** "Good/kept" renders in
   plain `INK`; "bad/lost" renders in red. The distinction is legible in grayscale
   and under any colorblindness because a **KEPT/LOST (or ✓/✗) label and left/right
   placement** carry it — color only points.
3. **Highlighter is a wash of the one accent**, used at most once per graphic,
   behind serif emphasis. No yellow. No second decorative color.
4. **`SLATE` gray is structure, not an accent.** Keep it out of the good/bad story.
5. Warm near-black `INK`, never pure black, never blue-black.

---

## `newsprint` — opt-in (the former default, preserved)

Warm editorial. The only palette that keeps a distinct positive *color*.

| role key | token | hex | role | on cream (WCAG) |
|---|---|---|---|---|
| ground | `CREAM` | `#F3EBDD` | the newsprint ground, full plane | — |
| text | `INK` | `#2F2A26` | all body/serif text, marks; warm near-black | 11.99:1 · AAA |
| good / kept / true | `TEAL` | `#1F6F5C` | the positive data accent | 5.09:1 · AA |
| bad / lost / broken | `CRIMSON` | `#BF3339` | the negative data accent | 4.73:1 · AA |
| structure | `SLATE` | `#3E5559` | entity cards (white text), neutrals | 6.70:1 · AA |
| highlighter, fill only | `GOLD` | `#F5D061` | editor's-pen sweep — NEVER text | 1.26:1 · fails by design |

Color laws for `newsprint` are the original two-accent rules: TEAL=good / CRIMSON=bad,
never swapped mid-film; gold is a highlighter, never text; pair color with position +
label; slate is structure. (Retired here too: `NAVY`, `DUSTY-BLUE`, `TERRACOTTA`.)

---

## `neu` — Northeastern brand (for NEU class videos)

Governed by Northeastern brand law (`runtime/design/NEU-DESIGN.md`). **Red = brand,
never state.** Because red cannot encode "bad," NEU carries good/bad by **label +
position only** — no color-coding of state at all. Typeface is **Lato** (required),
not EB Garamond/Montserrat.

| role key | token | NEU value | hex |
|---|---|---|---|
| ground | `CREAM` | white | `#FFFFFF` |
| text | `INK` | black (NEU mandates pure black) | `#000000` |
| good / kept | `TEAL` | black — label carries it | `#000000` |
| bad / lost | `CRIMSON` | gray — label carries it (**never red**) | `#545454` |
| structure | `SLATE` | gray | `#545454` |
| highlighter, fill only | `GOLD` | NU gold — rare, large-area only (fails AA small) | `#A4804A` |
| brand / emphasis / primary series | *(added)* | NU Red | `#C8102E` |
| gridlines | *(added)* | neutral-1 | `#E3E3E3` |

**NEU laws:** every asset must contain NU Red, but only as brand/emphasis/primary
series — never for negative values or alerts. Gold is ceremonial, large-text only.
Headings are regular weight (400), sentence case. No gradients, glassmorphism, or
drop shadows on type. White ground only.

---

## Data-visualization palette — separate from the brand palette

The brand palettes above govern **general text, Manim marks, and Remotion chrome** —
the *look*. They are deliberately too small for a chart with many series (`teardown`
is one accent; you cannot color five lines with "red"). So **multi-series data
visualization draws from a dedicated categorical palette that is NOT the brand
palette.**

**House data-viz standard: Okabe-Ito** (colorblind-safe — the gold standard). Chosen
because the whole system is accessibility-first, it scales to 8 series, it is
functional rather than decorative (brutalist-compatible), and its `#000000` sits with
`teardown` ink.

```
#000000 black     #E69F00 orange   #56B4E9 sky blue   #009E73 bluish green
#F0E442 yellow    #0072B2 blue     #D55E00 vermillion #CC79A7 reddish purple
```

**Data-viz laws**
1. **1–2 series still use the brand grammar** — red-vs-ink (`teardown`), teal/crimson
   (`newsprint`). Reach for the categorical set only at **3+ series**.
2. **Assign in listed order**, first series first; don't cherry-pick for prettiness.
3. **Position + label still carry meaning** — the categorical set points, it doesn't
   encode alone.

**Exceptions**
- **`neu`** — Northeastern brand law forbids non-brand chart colors. NEU charts use
  **NU Red for the primary series + grays** (`#000000` · `#545454` · `#787878` ·
  `#C4C4C4`) with `#E3E3E3` gridlines — never the categorical rainbow, never red for
  a negative value.
- **`medhavy`** already *is* Okabe-Ito, and **`humanitarians`** already *is* muted
  editorial — their charts use their own audience set (see `AUDIENCES.md`).

**Runner-up / fallback:** muted editorial (`#1F4E5F #E4572E #29335C #F3A712 #A8C686`)
— more minimalist to look at, but caps at 5 series and is CVD-decent, not gold. Tableau
10 was considered and rejected: too saturated and "designed" for the teardown aesthetic.

---

## Typography — four fonts, four jobs (shared by all palettes except `neu`)

| token | family | used for |
|---|---|---|
| `DISPLAY` | **Montserrat** (geometric sans) | titles, big display lines, section cards, **label chips** (`LabelChip` — white tracked caps on the accent block) |
| `SANS` | **Inter** (neutral sans) | **reserved** — no live component role since the 2026-07 amendment; available for a future dense-UI graphic |
| `SERIF` | **EB Garamond** | editorial / newsprint serif moments — quote cards, pull-quotes, attributions, and the underlined annotation labels (`SerifLabel`, italic) |
| `MONO` | **PT Mono** | math + data numbers only — never running text, never the equation body |

**`neu` override:** NEU class videos set **all** type in **Lato** (regular-weight
headings, sentence case) per Northeastern brand law. Lato is a Google Font (OFL) —
bundle the TTFs in `fonts/Lato/`; the CDN `<link>` does not reach Manim.

**Serif rule (non-neu):** the newsprint soul rides on serif — keep EB Garamond for
the places that *are* editorial (quotes, endcard attribution, marginalia). Structural
motion graphics are Montserrat. Don't set a whole graphic in serif out of habit.

### Amendment 2026-07-08 — Inter retired from the frame
`SerifLabel` → EB Garamond *italic* (was Inter bold); `LabelChip` → Montserrat MEDIUM
tracked-caps (was Inter mixed case); `SANS` (Inter) stays defined for backward compat
with no live role. Existing reels pick up the new type on their next re-render.

### Fonts are bundled in `runtime/fonts/`
```
fonts/EB_Garamond/   fonts/Inter/   fonts/Montserrat/   fonts/PT_Mono/   fonts/Lato/  (add for neu)
```
**Bundled ≠ visible to the renderer.** Manim/Pango resolves by *family name* via
fontconfig — a TTF in a folder is not found until registered. One-time on the Mac:
```
cp fonts/*/static/*.ttf fonts/PT_Mono/*.ttf ~/Library/Fonts/     # then re-log or `atsutil`
```
Verify: `fc-list | grep -iE 'garamond|inter|montserrat|pt mono|lato'` should list all.
If a family is missing, Pango silently substitutes and the render looks wrong.

---

## What implementing the default flip changes
- **`vox_graphics.py`** and the Remotion token sets: the default set becomes
  `teardown` (white / ink / red-only). `newsprint` moves to its own named set.
  Add `neu.ts` (+ Manim parallel) for the NEU palette.
- **`wcag_margin_check.py` (Gate W):** its `HEX` lock currently hard-codes the old
  default palette — make it **palette-aware** (read the active palette's tokens), or
  it flags every `teardown` reel as off-palette.
- **`compile.py` `find_font()`:** prefer bundled `runtime/fonts/…`; add Lato.
- **Re-renders every reel** (color + default change). Cheap per reel — but all of them.

**Open choice:** the `teardown` highlighter is a wash of the one accent (red @ ~14%).
If a neutral graphite sweep reads cleaner on video, swap `GOLD` to `#E8E6E1` — a
one-line change, still zero new hues.
