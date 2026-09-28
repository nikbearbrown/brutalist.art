# TYPECHECK.md — GATE T

Reel: `claude-liam-brutalist-show-tell-cards`  |  Checked: 2026-09-27T14:03  |  Overall: PASS  |  Beats checked: 15  |  FAILs: 0

Spec: `skills/make/kerning/reference/type-spec.md` §8.  Floor: 1.9% frame-height.  Contrast: 4.5:1 WCAG.  Kern threshold: 3.5× expected advance.  Wordy budget: 2 elements.

> **§8.10 REDUNDANCY (advisory — does not block cut):**
> Narration should DISCUSS on-screen text, not recite it.
> Exception: LITERAL beats (viewer types/copies/runs the text) are exempt.

> - §8.10 [B03] narration recites the card (1.00) — discuss it, don't read it
> - §8.10 [B08] narration recites the card (1.00) — discuss it, don't read it

| beat | lane | polarity | worst finding | status | fix |
|------|------|----------|---------------|--------|-----|
| BIDEA | bookend | light | min-size §8.1: min text-run height 61px >= floor 41px | PASS | — |
| BDEFS | bookend | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B00 | manim | light | min-size §8.1: min text-run height 940px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B01 | manim | light | min-size §8.1: min text-run height 63px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B02 | card | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B03 | card | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B04 | card | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B05 | card | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B06 | card | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B07 | card | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B08 | card | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B09 | card | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B10 | manim | light | min-size §8.1: min text-run height 63px >= floor 41px | PASS | — |
| BHTF | bookend | light | min-size §8.1: hand-drawn pattern (ClaudeComposerAsk) — §8.1 hachure/crossbar fragments ar… | PASS | — |
| BOUT | bookend | dark | min-size §8.1: min text-run height 66px >= floor 41px | PASS | — |

---

## Failures requiring action before cut

*None — GATE T PASS.*
---

## Check summary

| Check | Beats checked | FAILs |
|-------|---------------|-------|
| no-wordy-card §8.5 | 9 | 0 |
| min-size §8.1 | 15 | 0 |
| overflow §8.2 | 15 | 0 |
| contrast §8.3 | 15 | 0 |
| contrast-local §8.3b | 15 | 0 |
| bbox-overlap §8.6b | 15 | 0 |
| card-clip §8.13 | 15 | 0 |
| kerning §8.4 | 3 | 0 |
| redundancy §8.10 (advisory) | 5 | 2 (advisory — no exit effect) |

---

*GATE T: any FAIL blocks `./art run` and `./art final`. Fix the flagged beats and re-run `scripts/type_check.py` until green.*
