# DESIGN.md — Northeastern University Visual Constitution

> Source: brand.northeastern.edu — the authoritative reference for all decisions in this document.
> When this file and the Brand Center conflict, the Brand Center wins. Update this file, then proceed.
> Load on-demand before any Generate phase session that touches visual output.

---

## Who this governs

Any creative or digital output produced under the Northeastern University brand:
course materials, data visualizations, slide decks, reports, web components, print collateral.
Applies to the Boston campus and all global campuses unless a campus-specific override is documented below.

---

## Color system

Northeastern's palette is intentionally minimal. Three working colors, one accent. Hierarchy is enforced.

### Primary palette

| Role | Name | HEX | RGB | CMYK | Pantone | Usage target |
|------|------|-----|-----|------|---------|--------------|
| Brand primary | NU Red | `#C8102E` | 200, 16, 46 | 0, 100, 80, 5 | 186 U | 27% |
| Structure | Black | `#000000` | 0, 0, 0 | 0, 0, 0, 100 | — | 35% |
| Structure | White | `#FFFFFF` | 255, 255, 255 | 0, 0, 0, 0 | — | 35% |
| Accent | Gold | `#A4804A` | 164, 128, 74 | 33, 46, 80, 10 | 871 Metallic C | 3% |

**The hierarchy is not optional.** Red reinforces the brand; it is not a general-purpose highlight color. Every piece of collateral must contain red. Gold appears rarely — ceremonial contexts, metallic print applications, and approved premium materials only. It is never a substitute for red as the brand signal.

### Color rules that do not bend

- Do not introduce colors outside the four above without brand review approval.
- Red on black and red on white are both approved. Red on red is never permitted.
- Gold is metallic in print (Pantone 871). In digital, `#A4804A` is the approved screen approximation — do not substitute a brighter yellow or a warmer brown.
- White backgrounds are standard. Off-white, cream, or gray backgrounds require approval and are not defaults.
- Do not use red as an alarm or error color in data visualization contexts where the data itself is not alarming — red encodes the brand, not the state of the data. Use a neutral indicator for errors in UI.

### Accessibility

| Pair | Contrast ratio | WCAG AA (text) | WCAG AA (large text) |
|------|---------------|----------------|----------------------|
| Black on White | 21:1 | ✓ Pass | ✓ Pass |
| White on Black | 21:1 | ✓ Pass | ✓ Pass |
| White on Red (`#C8102E`) | 4.6:1 | ✓ Pass | ✓ Pass |
| Black on Red (`#C8102E`) | 4.5:1 | ✓ Pass (borderline) | ✓ Pass |
| Gold on White (`#A4804A`) | 3.0:1 | ✗ Fail | ✓ Pass (large only) |

**Gold fails WCAG AA for body text on white.** Do not use gold for text smaller than 18px regular or 14px bold. Gold is acceptable for decorative rules, borders, and large display text only.

---

## Typography

### Brand typeface

**Lato** is the Northeastern system typeface. It is used across all digital and most print contexts.

| Style | Weight | Size | Line-height | Use |
|-------|--------|------|-------------|-----|
| H1 | 400 (Regular) | 48px | 48px | Page titles only |
| H2 | 400 (Regular) | 36px | 40px | Section headers |
| H3 | 400 (Regular) | 30px | 36px | Subsections |
| H4 | 700 (Bold) | 20px | 28px | Component headers |
| H5–H6 | 700 (Bold) | 16px | 24px | Labels, callouts |
| Body | 400 (Regular) | 16px | 24px | Running text |
| Small / caption | 400 (Regular) | 13px | 18px | Footnotes, captions, source lines |
| Eyebrow | 400 (Regular) | 11px | 16px | Category labels above headings |

**Notable:** Northeastern headings are regular weight (400), not bold. Bold is reserved for H4 and below. This is a deliberate brand choice — do not "improve" headings by bolding them.

### Rules

- Sentence case for all headings and UI labels. Title Case for proper nouns and official program names only.
- No ALL-CAPS except for eyebrow labels (short category labels above headlines), which are set in all-caps at 11px.
- Do not substitute Arial, Helvetica, or system-ui for Lato. Load from Google Fonts or the approved CDN.
- Minimum body size: 16px digital, 9pt print.

---

## Logo system

### The marks

Four primary wordmark configurations exist. Use in this order of preference:

1. **Primary Wordmark** — N + "Northeastern University" stacked. First choice for all applications.
2. **Secondary Logo** — N monogram + motto lockup. Use for increased visual interest; best in print and larger formats only. Motto must be legible — do not use below minimum size.
3. **Horizontal Wordmark** — N + "Northeastern University" side by side. Use when vertical space is constrained.
4. **Stacked Wordmark** — Alternative stacked configuration. Available for experimental or editorial uses; can run vertically.

### Approved color versions

| Background | Logo color |
|-----------|-----------|
| White | Red (`#C8102E`) — preferred |
| White | Black |
| Black / dark | White |
| Red | White only |

Never place the red logo on a red background. Never place any logo on a patterned or photographic background without a legibility scrim.

### Clear space

Clear space around all wordmarks equals the height and width of the "N" in "Northeastern" on all four sides. No type, graphic elements, or other marks enter this zone.

### Minimum size

Digital: the "N" in "Northeastern" must be at least 12px tall.
Print: the "N" in "Northeastern" must be at least 1/8 inch tall.
The Secondary Logo (with motto) must meet these minimums with the motto remaining legible — at small sizes, revert to the Primary Wordmark.

### What the logo never does

- Changes color outside the approved versions above
- Gains a drop shadow, gradient, outline, or special effect
- Gets warped, stretched, skewed, rotated, or distorted
- Gets combined with other elements inside the clear space
- Gets its proportions, composition, or orientation altered
- Appears as a reversed-color or outlined version

---

## Imagery

**Photography style:** Authentic, warm, and active. Students and faculty in real learning and research contexts. Natural light preferred. Avoid staged, stock-photo-looking imagery.

**Color treatment:** Photography can appear in full color or with a red duotone treatment for brand-forward applications. Black-and-white is used sparingly for editorial or historical contexts.

**Gradient overlays:** Permitted on photography for legibility (black-to-transparent), not as decoration.

**No gradients as decoration.** No glassmorphism. No drop shadows on type.

---

## Animation and interaction (digital)

- Hover on links: `color: #C8102E` — the red underline/color shift is the primary interactive signal
- Hover on buttons: background darkens; red hover state `#C8102E` on white buttons is approved
- Transitions: `0.3s ease` is the system default (per brand.northeastern.edu CSS)
- No bounce, no parallax, no scroll-jacking
- Focus states: visible, high-contrast, 2px solid — never removed

---

## Data visualization within the NEU brand

When producing charts, graphs, or data displays under the NEU brand, the color system constrains the standard Brutalist palette. Apply these substitutions:

| Brutalist default role | NEU substitution | Notes |
|----------------------|-----------------|-------|
| Primary series color | `#C8102E` NU Red | First and most important series only |
| Secondary series | `#000000` Black | Or dark gray `#2D2926` for softer contrast |
| Tertiary series | `#A4804A` Gold | Use sparingly; fails AA for body text |
| Additional series | Grays: `#404040`, `#787878`, `#C4C4C4` | Neutral expansion beyond the 3-color palette |
| Chart background | `#FFFFFF` White | Per brand standard |
| Gridlines | `#E3E3E3` | Neutral-1 from brand CSS |
| Primary text | `#000000` | |
| Secondary text / axis | `#545454` | Neutral-5 from brand CSS |
| Alarm / alert | `#000000` or `#545454` | Do not use red for data alerts — red is brand, not state |

**Critical constraint:** Red encodes the brand, not the data. If you are making a chart where red would naturally mean "negative" or "danger," you must use a different encoding for that meaning. Using NU Red for negative values is prohibited — it corrupts the brand signal.

---

## Brand review requirement

Northeastern has a strict brand governance policy. All media plans and creative assets require review and approval before going to market. This applies to externally-facing outputs and any materials produced on behalf of the university.

Submit for review at: [brand.northeastern.edu/brand-reviews](https://brand.northeastern.edu/brand-reviews/)

When in doubt, submit. The cost of an unapproved asset reaching external audiences is higher than the cost of review.

---

*Source: brand.northeastern.edu — Primary Logos, Color, Typography pages.*
*Last reconciled against Brand Center: May 2026.*
*Next reconciliation: before any major production run or when brand.northeastern.edu signals an update.*
