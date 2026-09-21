# type-spec — the encodable typography rules (GATE T reference)

Everything here is a value or procedure the checker asserts. Numbers are the
defaults for the CLAUDE brutalist brand; tune in one place, not per beat.
Primary sources are cited so the rules trace to specs, not folklore — verify
platform safe areas directly, they drift.

## 1. Type scale — per aspect ratio, frame-height-relative

Font size is `vh`-relative (share of frame HEIGHT), resolved per aspect ratio
from a lookup — NOT one size scaled proportionally across ratios.

| Role        | 16:9   | 9:16   | 1:1    | Notes |
|-------------|--------|--------|--------|-------|
| Title/H1    | 6.0vh  | 5.5vh  | 5.5vh  | display; tightens tracking |
| Act card    | 7.0vh  | 6.0vh  | 6.0vh  | the ACT I / segment card |
| H2 / label  | 3.8vh  | 4.0vh  | 3.8vh  | |
| Body        | 3.5vh  | 4.0vh  | 3.6vh  | vertical needs larger relative body |
| Caption/LT  | 2.6vh  | 3.0vh  | 2.6vh  | lower-third, kicker |
| Data label  | 2.4vh  | 2.8vh  | 2.4vh  | D3; tabular-nums on |

- **Hard floor:** no body/label text below **3.2% of frame height**. Below
  that = FAIL. (Broadcast legibility rule of thumb: size as % of frame height,
  not px.)
- **Stroke floor:** no rendered stroke thinner than ~2px @1080p — thin strokes
  are the first thing platform re-encode destroys.
- **Motion tax:** any text that moves/scales/appears in a transition gets one
  step larger minimum size and a longer min on-screen dwell than static text.

## 2. Safe area — asserted per ratio

- Title-safe **90%**, action-safe **93%**, inset from each edge (SMPTE/EBU
  heritage; still the working convention).
- 9:16: **bottom inset larger** than a proportional scale suggests — platform
  UI (captions, like/share, progress bar) eats the bottom asymmetrically. Use
  ~14% bottom / ~8% top as the default safe inset for vertical.
- Assertion: every text run's rendered bbox ⊂ safe box. Overflow = FAIL.

## 3. Tracking (letter-spacing) as a function of size

Tracking tightens as size grows, loosens as it shrinks — never a global
constant. Default curve (em):

| Size band            | letter-spacing |
|----------------------|----------------|
| Display ≥ 5vh        | −0.015em       |
| Title 3.8–5vh        | −0.005em       |
| Body 3.2–3.8vh       | 0em            |
| Caption ≤ 3.2vh      | +0.02em        |
| ALL-CAPS (any size)  | base + 0.04em  |

- Programmatic uppercase ALWAYS adds the +0.04em (fonts are kerned for mixed
  case; caps without compensation collide).
- CSS control surface (Remotion/Chromium): `font-kerning: normal` for body;
  `text-rendering: optimizeLegibility` on titles (enables kerning+ligatures,
  costs perf) / `optimizeSpeed` on long scrolling labels. (CSS Text Module L4.)

## 4. Auto-fit — binary-search shrink-to-fit (measure real glyphs)

Fit variable-length strings by measuring **rendered kerned width** on an
offscreen canvas; never `char_count × avg_advance`, never `overflow:hidden`.

```javascript
function fitFontSize(text, maxWidthPx, fontFamily, minPx = 24, maxPx = 120) {
  const ctx = document.createElement('canvas').getContext('2d');
  const widthAt = (px) => { ctx.font = `${px}px ${fontFamily}`; return ctx.measureText(text).width; };
  let lo = minPx, hi = maxPx, best = minPx;
  while (lo <= hi) {
    const mid = (lo + hi) >> 1;
    if (widthAt(mid) <= maxWidthPx) { best = mid; lo = mid + 1; } else { hi = mid - 1; }
  }
  return best;
}
```

- Run **after** `document.fonts.ready` — fitting against a fallback then
  swapping the real font is a classic invisible headless bug.
- Multi-line (captions): greedy line-break to width, then shrink-and-retry if
  line count exceeds the box's max lines.
- `minPx` must map to ≥ the frame-height floor (§1) at the target resolution —
  if a string can't fit at the floor, that's a content problem (shorten the
  string / de-wordify), not a size problem.

## 5. Headless Chromium (Remotion) pitfalls the checker guards

- **Font-load race:** gate capture on `document.fonts.ready`; for
  `@remotion/google-fonts` or self-hosted, `await font.load()` before the
  composition mounts. Frames captured mid-load rasterize wrong-metric fallback.
- **Determinism:** pin the render environment (same Docker image / Chromium
  build, same font-smoothing/GPU flags). Bit-identical output is required for
  the golden-string diff to mean anything.
- **Fallback stack:** always specify an explicit fallback; a silent system-font
  substitution in CI is the #1 "why did this run look different" bug — and a
  FAIL here, not a nit (§ SKILL hard rule 4).

## 6. Manim text rules

- Two paths, different kerning: `Tex`/`MathTex` (LaTeX — excellent for math,
  constrained fonts) vs `Text`/`MarkupText` (Pango — arbitrary installed fonts,
  shaping quality depends on the font's kern tables). Pick **one canonical path
  for narration-synced labels** (`Text`/`MarkupText`) and reserve `Tex` for
  actual notation. Don't switch by scene aesthetic.
- **The gappy-letter bug** (`w a v e s   t h r o u g h`) is almost always: (a)
  the named font isn't installed so Pango falls back and shapes with wrong
  tracking, or (b) letters were animated per-glyph (`Write`/`AddTextLetterByLetter`)
  at large scale leaving residual spacing. Fixes: name an **installed** font
  exactly (EB Garamond for CLAUDE brand — confirm `fc-list | grep -i garamond`);
  prefer `MarkupText` for controlled spacing; avoid per-glyph animation on
  display text; render a frame and assert inter-glyph advance (§8.4).
- `font_size` is scene-unit-relative — size in scene units, let the camera map
  to px; don't reverse-engineer a px-equivalent per resolution.

## 7. D3 text rules

- `font-variant-numeric: tabular-nums` on every numeric tick/label — otherwise
  proportional digits jitter horizontally frame-to-frame in animated charts
  (reads as a bug though the kerning is "correct").
- Collision = font-size problem: shrink font in fixed steps or rotate labels
  algorithmically until no bounding boxes intersect; don't nudge after.
- Small dense ticks (10–12px): `font-kerning: none` + fixed positive tracking
  often beats metric kerning at that size.

## 8. GATE T assertions (what `scripts/type_check.py` checks per frame)

   **Detection mask (§8.1, §8.2, §8.6b):** pixel-level checks use the union of
   INK (#3D3929) and MUTE (#5D584F) masks on light-polarity frames (tolerance 48
   in Euclidean RGB distance), and a luminance threshold on dark-polarity frames.
   INK-only detection is a known blind spot: Manim scene files use MUTE for the
   majority of diagram labels, annotations, and supporting text. Any checker that
   reads only INK will silently miss all MUTE labels — overlaps, overflows, and
   min-size violations all become invisible. Both colors must be in the union.

1. **Min-size:** every text run ≥ frame-height floor for its role (§1). Source
   the role→size from the beat's lane + the §1 table. Detection mask: INK ∪ MUTE
   (see above) — a MUTE label below the floor is a FAIL, same as an INK one.
2. **Overflow:** Remotion — headless `getBoundingClientRect` per text node ⊂
   safe box (§2); Manim/D3 — rendered-glyph bbox (INK ∪ MUTE union mask) ⊂ safe
   box.
3. **Contrast:** sample text ink vs backing plate on the rendered frame; assert
   ≥ 4.5:1 (WCAG 2.x body-text). Backgrounds are variable/generated, so read
   pixels.
4. **Kerning sanity:** for a text run, measure mean inter-glyph advance; FAIL if
   it exceeds the font's expected advance for that size by the gap threshold
   (default 1.6×) — catches Pango fallback + per-glyph residue.
5. **No-wordy-card:** Remotion beat text payload ≤ 1 display line + 1 label, OR
   a ≤12-word designed pull-quote. More prose = FAIL → de-wordify.
6. **Golden strings:** run every title/label template through `fitFontSize` +
   overflow against the adversarial set below; any overflow/floor breach = FAIL.
6b. **Bbox-overlap:** no two text-run bboxes (from the INK ∪ MUTE union mask)
    may intersect by more than 10% of the smaller element's area. Catches the
    stacked-label bug where two elements share coordinates and print glyphs on top
    of each other, becoming unreadable. Threshold: intersection / min(area_i, area_j)
    < 0.10. Box borders that enclose labels are excluded via an explicit allowlist
    (`BBOX_OVERLAP_EXEMPT_PATTERNS` in `type_check.py`) — only genuine text-run
    blobs trigger this check.

### Golden-string set (adversarial, run in CI)

```
LONGEST   : the single longest string the template can emit (worst real case)
ALLCAPS   : THE COMMITTEE QUESTION AND THEN SOME MORE WORDS
NARROW    : illillillillill Illilli littil
WIDE      : WMMWWMMW MMWWMM WWMMWW
ONEWORD   : Untestable
NUMERIC   : 1,234,567.89  0.001  −18.3s   (tabular-nums check)
```

## Sources
- CSS Text Module Level 4 (W3C) — `font-kerning`, `letter-spacing`, `text-rendering`.
- WCAG 2.x — 4.5:1 body-text contrast.
- Remotion docs — `@remotion/google-fonts`, font-loading, Puppeteer/Playwright render internals.
- Manim Community docs — `Tex`/`MathTex` vs `Text`/`MarkupText` (Pango), `font_size` scene units.
- D3 docs + label-collision utilities — tabular-nums, collision-by-font-size.
- SMPTE/EBU title-safe/action-safe heritage — 90%/93%; verify per-platform (YouTube/TikTok/IG) safe areas directly, they differ and aren't governed by one current standard.
