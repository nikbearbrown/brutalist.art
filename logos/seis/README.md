# logos/seis — marks for SEIS reels

## `primary-marks/` — Northeastern's OFFICIAL primary marks (Bear dropped `Primary Marks.zip`, 2026-09-15)
University-level marks in PMSu / PMSc / CMYK / RGB (eps + png + svg): Primary Logo (monogram + wordmark),
Secondary Logo (monogram + motto), Notched-N wordmark, Notched-N motto, Monogram, Wordmark horizontal /
stacked — each in red+black, red+white, black, white. `rights: trademark`. Never re-draw; clear space = the
height of the N; N ≥ 12px; never red-on-red; never on a photo without a scrim (NEU-DESIGN.md § Logo).

RGB SVGs copied with clean names to `runtime/remotion/public/northeastern/official/` for `staticFile()`:

| clean name | source |
|---|---|
| primary-logo-red-black.svg | primary-logo-red-black/Primary Logo Red+Black/4_RGB/Monogram Wordmark_RGB_186+K.svg |
| primary-logo-red-white.svg | primary-logo-red-white/Primary Logo Red+White/4_RGB/Monogram Wordmark_RGB_186+KO.svg |
| primary-logo-black.svg | primary-logo-black/Primary Logo Black/Monogram Wordmark_K.svg |
| primary-logo-white.svg | primary-logo-white/Primary Logo White/Monogram Wordmark_KO.svg |
| secondary-logo-red-black.svg | secondary-logo-red-black/Secondary Logo Red+Black/4_RGB/N-Motto Wordmark_RGB_186+K.svg |
| secondary-logo-black.svg | secondary-logo-black/Secondary Logo Black/N-Motto Wordmark_K.svg |
| secondary-logo-white.svg | secondary-logo-white/Secondary Logo White/N-Motto Wordmark_KO.svg |
| notched-n-wordmark-red-black.svg | notched-n-northeastern-red-black/Notched N Northeastern Red+Black/4_RGB/NU_RGB_Notched-N_wordmark_RB.svg |
| notched-n-wordmark-red-white.svg | notched-n-northeastern-red-white/Notched N Northeastern Red+White/4_RGB/NU_RGB_Notched-N_wordmark_RW.svg |
| notched-n-wordmark-black.svg | notched-n-northeastern-black/Notched N Northeastern Black/NU_Notched-N_wordmark_K.svg |
| notched-n-wordmark-white.svg | notched-n-northeastern-white/Notched N Northeastern White/NU_KO_Notched-N_wordmark.svg |
| notched-n-motto-red-black.svg | notched-n-motto-red-black/Notched N Motto Red+Black/4_RGB/NU_RGB_Notched-N_motto_RB.svg |
| monogram-red.svg | monogram-red/Monogram Red/4_RGB/NU_RGB_monogram_R.svg |
| monogram-black.svg | monogram-black/Monogram Black/NU_monogram_K.svg |
| monogram-white.svg | monogram-white/Monogram White/NU_monogram_KO.svg |
| wordmark-horizontal-black.svg | nu-wordmark-horizontal-black/NU Wordmark Horizontal Black/NU_K_wordmark_h.svg |
| wordmark-horizontal-white.svg | nu-wordmark-horizontal-white/NU Wordmark Horizontal White/NU_KO_wordmark_h.svg |
| wordmark-stacked-black.svg | nu-wordmark-stacked-black/NU Wordmark Stacked Black/NU_wordmark_v_K.svg |
| wordmark-stacked-white.svg | nu-wordmark-stacked-white/NU Wordmark Stacked White/NU_wordmark_v_KO.svg |

**Default for SEIS reels:** `monogram-red.svg` (the N alone) as the open bug, `primary-logo-red-black.svg` full-size on the outro;
`monogram-red.svg` as the small corner bug (LOGO LAW). Use `-white` variants only on black / NU-red grounds.

## SEIS-unit marks — now in `unit/` (see below; SVG / high-res versions still wanted from SEIS)
Seen in chat 2026-09-15, not in the zip: the **SEIS tile mark** (four white rounded tiles, red serif S·E·I·S,
"Northeastern University" beneath, black ground) and the **N + "Software Engineering and Information Systems"**
lockup (white on NU red). Shipped as `unit/seis-button-logo.jpg` (tile) and `unit/seis-logo.png` (lockup); SVG versions would drop in beside them. Handles on the SEIS
announcement card: @nu_seis (LinkedIn, Instagram), @northeastern.seis (Facebook). YouTube handle: CONFIRM.
`../northeastern/` holds the Wikimedia Commons copies of the wordmarks (superseded by primary-marks/).

## `unit/` — the SEIS unit marks (from Bear, 2026-09-19; source `books/seis/logos/`)
- `seis-logo.png` — the lockup: N + "Northeastern University / Software Engineering and Information Systems" (463×149, transparent). Under the name in lower thirds; the end slide.
- `seis-button-logo.jpg` — the tile "button": S·E·I·S on black (160×160). Top-right bug on every SEIS frame.
Both are low-res rasters — fine at 1080p, soft at 4K. Ask SEIS for SVG/high-res when convenient. Copied to `runtime/remotion/public/seis/`.
