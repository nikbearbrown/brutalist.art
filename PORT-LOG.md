# PORT-LOG.md — curated ports from `brutalist-art/` (sandbox) into this public cut

The sandbox is bloated (67 skills, 583 scenes, 102 root docs, 417 reels, 58 GB).
This cut is deliberately curated: **15 skills, free-by-default, no publishing
machinery** (CLAUDE.md rule 5). Ports are therefore *selective* — only what makes
the retained skills correct. This file records what came across and what did not.

---

## Batch 1 — 2026-08-30 · correctness: the two accepted card forms

**Why:** this cut shipped `SlateCard` — the DESIGN-PRINCIPLES §1 **banned** card
(eyebrow/kicker + bold sans headline + rule + decorative circle) — and did **not**
ship either accepted replacement. Across the wider tree `FormBCard` is used by
3,147 reels and `FormACard` by 1,347; both were absent here.

| Action | File |
|---|---|
| DELETED | `runtime/remotion/src/scenes/SlateCard.tsx` (+ Root.tsx import/composition) |
| added | `scenes/FormACard.tsx`, `FormBCard.tsx`, `FormACard916.tsx`, `FormBCard916.tsx` |
| added | `DESIGN-PRINCIPLES.md` — the doc that *defines* the two accepted forms |
| updated | `runtime/scripts/fill_slates.py` — now stamps **FormACard**, not SlateCard |
| updated | `runtime/scripts/generate_audio_kokoro.py` — hard-skips `⚠` / `[LOST]` / `[PLACEHOLDER]` narration sentinels (a batch build voiced one as narration, 2026-08-27) |

## Batch 2 — 2026-08-30 · components this cut's own skills already name

Of 49 reusable components (used by >1 reel) absent here, **10 were named by this
cut's own SKILL.md / docs** — i.e. already referenced but not shippable. Ported
those, minus one:

`ClaudeMascotGrid` · `ClaudeMascotScene` · `DoodleChart` · `DoodleScene` ·
`GitHubSectionRail` · `GitHubStructureMap` · `ShellSession`

Dependencies pulled in to make them build: `tokens/shell.ts`,
`doodle/{handFont.ts,PaperGrain.tsx,roughen.ts}`, `vendor/` (rough.js + LICENSE).

**NOT ported — `FlowDiagram.tsx`.** Its sandbox original has 2 real zod type errors
(a `"⚠ SET IN BEAT SHEET"` sentinel used as the default of an enum field). The
sandbox tree currently has **28 TypeScript errors**; this cut has **0**, and that is
worth protecting. Port it after the schema is fixed upstream.

**Verification:** `node_modules/.bin/tsc --noEmit` → **0 errors**.
`./art scene-index` → 601 renderable compositions.

---

## Deliberately NOT ported (bloat, or contrary to this cut's charter)

| Not ported | Why |
|---|---|
| Publishing lane — `post`, `youtube-publisher`, `video-inventory`, `post.py`, `stage_publish.py` | CLAUDE.md rule 5: "Never publish. There is no publishing machinery here." Excluded **by design**, not missing. |
| 49 × `CLAUDE-CODE-*.md` one-off prompts | Bear's private one-off runbooks; not toolkit doctrine. |
| 417 reel folders in sandbox `youtube/` (14 GB) | Content, not toolkit. Rule 3: videos travel with their book. |
| 39 reusable components not referenced by any skill here | No consumer in this cut. Port on demand, with its skill. |
| 43 single-reel souvenir components + 44 zero-reference components | Bloat by definition. |
| Paid-tier skills beyond the documented tiering | Rule 6/7: free by default; never escalate a fellow into a paid tier. |
| `.env`, `.fuse_hidden*`, `*.bak`, `*.pre-*` | Junk / secrets. |

## Drift the other way — do not clobber

Five skills exist ONLY here and are real work: `anthropics`, `finance`, `guests`,
`logo-motion`, `screen-clean`. Any future sync must merge, never overwrite.

## Open

- 8 pre-existing uncommitted edits were in this tree before these ports
  (`package.json`, `Root.tsx`, `scenes.json`, `capture_sim.py`, two SKILL.md,
  plus untracked `art.pre-scene-search` and `BrutalistHesitantWriter.tsx`).
  `capture_sim.py` is byte-identical to the sandbox; the two SKILL.md differ.
  Resolve before committing.
- Rule-owner docs still only in the sandbox and arguably worth porting:
  `REMOTION-STANDARDS.md` (component-authoring contract — this cut's rule 8
  already assumes it), `SHOT-FORM-SYSTEM.md`, `SHOTS.md`, `GLOSSARY.md`,
  `VOICE-LOCK.md`, `BRAND-LOCKS.md`, `TEMPLATE-MISSES.md`, `CAPABILITIES.md`.

## Batch — 2026-09-22 · the `tldr` skill and its TERMS card

**Why:** Bear's new skill (chapter/report → learning sections → per-section film on
the 3Blue1Brown template). It needed the retired tree's Brown Blue pedagogy and a
cream-stage definitions card; neither existed here.

| Action | File |
|---|---|
| added | `skills/make/tldr/SKILL.md` (+ `reference/pedagogy.md`, `reference/sectioning.md`, `reference/example-tldr-beat_sheet.json`) |
| ported (rewritten) | `brutalist-art/skills/make/math-explainer/reference/pedagogy.md` → `skills/make/tldr/reference/pedagogy.md` — the 3b1b gates, extended with the seven-stage template, the scene-level unit, the three learning checks |
| added | `runtime/remotion/src/scenes/ClaudeDefinitions.tsx` (+ Root.tsx import/composition) — the Claude-register port of the sandbox's `CCDefinitions` (dark CC shell, NOT ported: the CC kit and `tokens/claudecode.ts` are absent here, so `cc-explainer` in this tree still references a card it cannot render) |
| updated | `art` (`--list` row), `CLAUDE.md` (ADVANCED table), `skills/TIERS.md` |

**NOT ported:** the CC kit (`CCSession`, `CCShell`, `CCDefinitions`, …) and the
math-explainer scripts (`silent_run.py`, `burn_captions.py`, …) — tldr runs on the
shared `run.sh` / `compile.py` belt like every other builder here.


## Fix — 2026-09-22 · hesitant writer phrase triggers; ClaudeDefinitions GATE T sizes

| Action | File |
|---|---|
| fixed | `runtime/remotion/src/scenes/BrutalistHesitantWriter.tsx` — multi-word `triggerWords` ("can do", "why not just") now merge into one token and replace as a phrase; previously only single words matched, so every phrase trigger silently never fired (ai-explainer doctrine tells authors to use phrases). Single-word sheets render identically. |
| updated | `runtime/remotion/src/scenes/ClaudeDefinitions.tsx` — meaning 48, title 54 @ 0.06em, chip 32: GATE T measures lowercase runs at x-height and tracked titles as single glyphs; 40/36/24 failed the 41px floor at 4K. |

## Added — 2026-09-22 · the two TL;DR cards (tldr cold open)

Bear: "TLDR intro beat needs a NEW template, not the Claude.ai interface" → then "TLDR needs two beats: 1. what is this film about? 2. why should you care?"

| Action | File |
|---|---|
| added | `runtime/remotion/src/scenes/ClaudeTldrWhat.tsx` — TL;DR page, card one: wordmark "TL;DR." (terracotta period), greeting + course line, heading "What This Film Is About", the question writes on word by word, numbered lines land on `cues` (seconds), active numeral terracotta |
| added | `runtime/remotion/src/scenes/ClaudeTldrWhy.tsx` — card two: same header (page turn), heading "Why You Should Care", the stake writes on, dashed consequence lines land on cues |
| updated | `Root.tsx` (two compositions, `durationSeconds` → calculateMetadata), `runtime/scripts/bookend_check.py` (`metadata.skill == "tldr"` accepts `ClaudeTldrWhat` as the cold open), `scenes.json` via `./art scene-index` |
| GATE T sizes | heading 50 · course line 50 · greeting 52 · question 64 · lines 48 · numerals 60 · chip 32 — every lowercase run is measured at x-height at 4K (41px floor); headings in INK, never terracotta (2.74:1 on cream) |

## Ported — 2026-09-26 · the Claude Code (CC) scene kit

Bear approved porting the CC Remotion kit from `brutalist-art/` (the retired sandbox) into this toolkit, so `skills/make/cc-explainer` has the components it names.

| Action | File |
|---|---|
| added | `runtime/remotion/src/scenes/CC*.tsx` (16): CCBoondoggleScore, CCDefinitions, CCDiff, CCHarnessMap, CCHumanLedger, CCPlainShell, CCPlanCard, CCPromptBar, CCSession, CCShell, CCSkepticAudit, CCStatusVerb, CCThemePicker, CCToolCall, CCWalkthroughDemo, CCWebHome |
| added | `runtime/remotion/src/scenes/CC-TEMPLATES.md`, `runtime/remotion/src/tokens/claudecode.ts` |
| added | `runtime/remotion/src/scenes/CursorLayer.tsx`: the anchor registry that CCShell, CCSession and others import. It was missing here |
| reused | `ClaudeMascotScene.tsx` (same as the sandbox copy), `GitHubCodeDiff.tsx` (only the default `caption` differs; `diffLineSchema` is the same) |
| updated | `Root.tsx`: the `CursorLayer` composition, plus a `<Folder name="CC">` with all 31 CC compositions (16 components + 15 Demos). Ids, durations, schemas and defaultProps match the sandbox Root.tsx. `scenes.json` was rebuilt with `./art scene-index` |

## Added — 2026-09-27 · show-tell CARD family (`ShowTellCard`)

Bear, with a reference sheet of sixteen interface motion studies: "For the show-tell skill keep all typography and colors but add more stop motion cards beyond just the isometric graphics ... the skill should never force but more choices can add".

| Action | File |
|---|---|
| added | `runtime/remotion/src/scenes/ShowTellCard.tsx` — one composition, 16 `kind`s: player, search, workspace, tabs, chart, dashboard, stack, dock, masked, elastic, layout, reveal, perspective, focus, paths, particles. Claude palette + iso_kit kraft, EB Garamond / UI sans / mono, shot on twos (`onTwos`, default true), solid kraft offset shadows, no blur or gradients. Motion done by ~70% of `durationSeconds`; type settled by 45% (GATE T samples the midpoint) |
| updated | `Root.tsx` (composition `ShowTellCard`, calculateMetadata from `durationSeconds`), `scenes.json` via `./art scene-index` |
| updated | `skills/make/show-tell/SKILL.md` — new **Card family — optional** section (menu, not a quota; kind → when-to-use table; props; card laws; beat-sheet shape `lane: "card"`, `shot.remotion.pattern: "ShowTellCard"`); law 1 and the BODY rule now allow a card per beat |
| film | `youtube/brutalist/claude-liam-brutalist-show-tell-cards/` — "Show-Tell: Drawings and Cards", three drawn beats + eight card kinds |

## Updated — 2026-09-27 · show-tell: no length cap + the card test

Bear: "there's no hard cap on the show tell length it's as long as it should be but it should just be to the point no bullshit ... use these new cards only if they actually make sense no using a card just for using a card".

| Action | File |
|---|---|
| removed | length caps: frontmatter "Short, 60–180 s", Spine "6–10 drawn beats of 5–12 s", batch brief "6–9 beats / Target 100–160 s" (`anthropics/youtube/SHOW-TELL-BATCH.md`) |
| added | SKILL.md law 9 AS LONG AS IT NEEDS, NO LONGER; a **Length** paragraph (the content sets the length; split beats past ~15 s; cut repeats and padding) |
| added | SKILL.md **THE CARD TEST** (three questions, any "no" means a drawing; real numbers only; a "why a card" column in SHOTLIST.md; re-check if more than a third of the body is cards); law 1 and the Card laws rewritten to match; the "all cards" option removed |
| updated | `art --list` line, `CLAUDE.md`, and books/CLAUDE.md show-tell rows |
