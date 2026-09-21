---
name: kerning
description: >
  Deterministic typography gate for the brutalist video pipeline — the
  TYPE-LOCK LAW. Encodes font-size and kerning/tracking as testable rules (not
  taste) and asserts them against every rendered frame before a cut ships:
  per-aspect-ratio type scale, a hard minimum legible size as a share of frame
  height, tracking-as-a-function-of-size, safe-area insets, WCAG contrast, and
  bounding-box overflow. Also enforces the NO-WORDY-CARD (SHOW-DON'T-TELL-HARD)
  law: a Remotion beat may never be a two-sentence text slide — wordy text
  beats are rebuilt as a SHOW visual (Manim process diagram or Remotion
  animation). ALWAYS-RUN, like factcheck: no reel reaches its review or final
  cut until the type gate passes. Use when the user types `kerning`,
  `type-lock`, `typecheck`, `typography`, `font size`, `de-wordify`, or asks to
  fix kerning/tracking, fix wordy slides, or run the type gate against beat
  sheets. Never publishes.
---

> **ALWAYS-RUN GATE.** This skill is to the LOOK what factcheck is to the
> CLAIMS. Every explainer builder (`ai-explainer`, `cli-explainer`,
> `deep-explainer`) runs GATE T (type-lock) before its review cut AND again
> before `./art final`. A reel that has never passed GATE T is unfinished, the
> same way a reel without FACTCHECK.md is unfinished. There is no "skip for
> now" — a failing type assertion blocks the cut.

# kerning — the TYPE-LOCK LAW (typography as a deterministic gate)

Nobody eyeballs every frame in a schema-first pipeline. Remotion rasterizes
through headless Chromium, Manim shapes text through Pango/LaTeX, D3 delegates
to the browser — and whatever they emit ships. So every typographic decision
is a RULE the pipeline asserts, never a judgment call made by a human who
isn't looking. This skill is that rule set plus the check that enforces it.

Two failure families this gate exists to kill, both visible in real cuts:

1. **Broken kerning/tracking** — the gappy-letter look from Manim's Pango
   `Text` path (letters spaced like `w a v e s   t h r o u g h`), Chromium
   font-load races that rasterize a fallback font with wrong metrics, and
   programmatic all-caps rendered without compensating tracking.
2. **Font-size failure** — text legible on a 27" dev monitor that turns to
   mush after platform re-compression, is unreadable in a 9:16 feed, or
   overflows its safe area because an auto-generated string was longer than the
   box.

And one CONTENT failure this gate also owns, because it reads as a typography
problem but is really a beat-design problem:

3. **Wordy cards** — a Remotion beat that is two sentences of prose on a plate
   (the "Committee Question" anti-pattern). The fix is never smaller type. The
   fix is to SHOW it — rebuild the beat as a Manim process diagram or a
   Remotion animation. See the NO-WORDY-CARD LAW below.

The full encodable spec — the per-ratio type scale table, tracking curve,
auto-fit algorithm, headless-Chromium gotchas, Manim `Text` vs `Tex` rule, D3
tabular-nums, and the golden-string set — lives in `reference/type-spec.md`.
This file governs the LAWS and the GATE; the reference governs the NUMBERS.

## The NO-WORDY-CARD LAW (SHOW-DON'T-TELL, hard form)

The parent explainer's SHOW-DON'T-TELL LAW says "illustrate the concept." This
is its enforced, testable form for text beats:

- A Remotion beat may carry **at most one line of display text plus one short
  label/kicker**. A pull-quote of ≤ 12 words, seated as a designed quote card,
  is legal. Two sentences of body prose on a plate is NOT — it is a wordy card
  and it FAILS the gate.
- A beat whose narration teaches a **relationship, process, contrast, or
  sequence** must be a SHOW visual: a Manim process diagram (nodes, arrows,
  the flow), a Remotion build-on, or a D3 chart — not the sentences describing
  it. The "Testable vs Untestable Handoff" diagram is the target; the
  "Committee Question" two-column text card is the anti-pattern.
- **De-wordify procedure** (what the gate does when it flags a wordy card):
  1. Read the beat's narration. Name the underlying structure (contrast /
     pipeline / branching / accumulation / part-to-whole).
  2. Rebuild it in the lane that shows that structure — Manim process diagram
     for pipelines and branching, Remotion for rhetorical/build-on, D3 for
     quantities. Keep on-screen words to labels only.
  3. Recompile that slot; re-run GATE T on the new frame.
- The screen carries the *evidence*; the narration carries the *sentence*.
  If a viewer could read the slide instead of listening, the slide is doing
  the narration's job — cut the words, show the mechanism.

## The TYPE-LOCK LAW (font size + kerning, as assertions)

Every value below is stated fully in `reference/type-spec.md`; the law is that
these are **asserted per rendered frame**, not trusted from the source.

- **Size is frame-relative, never fixed px.** Type scale is a lookup keyed by
  aspect ratio (`16:9`, `9:16`, `1:1`) — a separate scale per ratio, not one
  size scaled proportionally, because safe-area geometry isn't proportional.
  Hard floor: no body text below **3.2% of frame height**; no stroke thinner
  than ~2px at 1080p (compression eats it).
- **Safe area is asserted.** Title-safe 90% / action-safe 93%, with larger
  bottom inset on 9:16 (platform UI eats the bottom). Rendered text bounding
  boxes must sit inside the safe box — checked, not assumed.
- **Tracking is a function of size, not a constant.** Display sizes tighten
  (slightly negative `letter-spacing`); small/caption sizes loosen (positive).
  A title and a lower-third never share a `letter-spacing` even in the same
  face. Programmatic all-caps ALWAYS gets compensating positive tracking.
- **Kerning is explicit.** Body: `font-kerning: normal`. Display: verify no
  visible pair gaps; if the face misbehaves, set optical tracking rather than
  trusting metric pairs. Very small dense labels (10–12px D3 ticks) often read
  better with `font-kerning: none` + fixed positive tracking.
- **Auto-fit measures real glyphs.** Variable-length strings (titles, data
  labels, captions) are fit with a binary-search shrink-to-fit that measures
  *rendered kerned width* on an offscreen canvas — never `chars × avg_width`,
  and never `overflow: hidden` (silent truncation is a shipped bug). Fit runs
  **after** `document.fonts.ready`.
- **One canonical face per surface.** CLAUDE brand: EB Garamond serif for
  display/body, the UI sans for kickers/labels; terracotta `#D97757` is the one
  accent. Manim `Text` and Remotion must name the **same installed font** — a
  fallback substitution is the root cause of the gappy-letter bug.

## GATE T — the deterministic type check (what "always run" means)

GATE T runs the checker (`scripts/type_check.py`, spec in
`reference/type-spec.md`) over the reel's rendered frames and writes
`TYPECHECK.md` (row per beat: beat | lane | worst finding | PASS/FAIL | fix).
It asserts, per frame:

1. **Min-size** — every text run ≥ the frame-relative floor for its role.
2. **Overflow** — every text bounding box (headless `getBoundingClientRect`
   for Remotion; rendered-glyph bbox for Manim/D3) inside the safe-area box.
3. **Contrast** — text vs its actual backing plate ≥ WCAG 4.5:1 (backgrounds
   may be generated/variable, so assert on the frame, not the design).
4. **Kerning sanity** — no run whose measured inter-glyph advance exceeds the
   font's expected tracking by the gap threshold (catches the Pango gappy-letter
   failure and fallback-font metrics).
5. **No-wordy-card** — no Remotion beat exceeds the one-line-plus-label budget
   (word-count + line-count assertion on the beat's text payload).
6. **Golden strings** — every title/label template is fit-tested against the
   adversarial set (longest expected, all-caps, narrowest `illi`, widest
   `WMMW`, single word) so overflow/kern bugs are caught on strings that
   haven't occurred in real content yet.

A FAIL blocks the cut. The builder fixes the flagged beat (de-wordify, refit,
retrack, reface, or re-render the frame) and re-runs GATE T until green.
Determinism requires a pinned render environment (same Chromium build / Docker
image) — antialiasing and hinting drift otherwise, and "green locally, broken
in CI" is exactly the bug class this gate exists to prevent.

## Running against existing beat sheets (batch)

`kerning sweep <youtube-dir>` — for every reel folder with a `beat_sheet.json`:
run GATE T on its current frames, write `TYPECHECK.md`, and produce a worklist.
Then, per reel and in two passes (see below), apply fixes and re-gate. This is
how the whole back-catalog gets brought up to the type standard without a human
eyeballing every frame — the golden-string + bbox + contrast assertions do the
looking.

**Two passes, always in this order:**

- **PASS 1 — de-wordify (content).** Find every wordy Remotion text card and
  rebuild it as a SHOW visual (Manim process diagram / Remotion build-on / D3).
  This changes *what* is on screen; do it first, because the type gate on a
  card you're about to delete is wasted work.
- **PASS 2 — type-lock (form).** With the beat lanes settled, run GATE T on
  every frame and fix every kerning/size/overflow/contrast failure: reface to
  the canonical font, refit variable strings, retrack display vs small, fix
  Manim Pango shaping (name the installed font, avoid per-glyph `Write`
  artifacts, prefer `MarkupText` for controlled spacing), enforce safe area.
  Recompile only changed slots; re-gate until green.

## Manim, Remotion, D3 — the per-engine rules (summary; full in reference)

- **Manim:** one canonical text path for narration-synced labels (`Text` /
  `MarkupText`, Pango) and `Tex`/`MathTex` reserved for actual math — never
  mixed by scene-aesthetic whim, because the two paths kern differently and
  the mix reads as a mistake. Name the exact installed font; a missing font is
  the gappy-letter bug. `font_size` is scene-unit-relative — size in scene
  units and let the camera map to pixels; don't reverse-engineer px per
  resolution.
- **Remotion (headless Chromium):** gate frame capture on `document.fonts.ready`
  and `await font.load()` before mount; specify an explicit fallback stack;
  `text-rendering: optimizeLegibility` on titles, `optimizeSpeed` on long
  scrolling labels; pin the render environment for subpixel stability.
- **D3:** `font-variant-numeric: tabular-nums` on every numeric axis tick and
  data label (proportional digits jitter frame-to-frame in animation);
  overlap is solved by shrinking font size / rotating labels algorithmically,
  not by nudging after the fact; small dense ticks prefer fixed tracking over
  metric kerning.

## Hard rules

1. **Always run.** GATE T is mandatory before review cut and before final,
   for every explainer. No skip flag.
2. **Assert on the frame, not the source.** Backgrounds and string lengths are
   variable and un-reviewed; the check reads rendered pixels/bboxes.
3. **Smaller type is never the fix for a wordy card.** De-wordify first.
4. **One canonical face per surface.** A fallback substitution is a FAIL, not
   a cosmetic nit — it breaks every fit calculation done before the swap.
5. **Golden strings run in CI.** Every text template is adversarially fit-tested
   before it can ship, not after a bad string appears in real content.
6. **Never publish.** GATE T green means the master may sit in the reel folder;
   putting it in front of an audience stays a human decision.

## Output contract

```
<reel>/
  TYPECHECK.md         GATE T ledger: beat | lane | finding | PASS/FAIL | fix
  BUILD-LOG.md         (append) de-wordify + type-fix decisions per beat
scripts/type_check.py  the deterministic checker (see reference/type-spec.md)
reference/
  type-spec.md         the encodable numbers: scale table, tracking curve,
                       auto-fit, headless gotchas, per-engine rules, golden set
```
