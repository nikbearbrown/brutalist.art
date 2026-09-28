# Sectioning — cutting written material into learning sections

`tldr <source>` starts here, never at a beat sheet. The source — a chapter,
a report, a long post, a pasted document — is read WHOLE and cut into
**learning sections**: the units a viewer can learn in one sitting. Each
section is a candidate film. The human picks (GATE S); then each pick builds
on the spine in `../SKILL.md`.

## The section test

A passage is a learning section when ALL of these can be written in one
line each:

1. **The question** — as a viewer would ask it, in their words.
2. **The key case** — one concrete puzzle, computation, anomaly or
   before/after contrast that motivates the whole section (pedagogy §1.1).
3. **The naive attempt** — the obvious approach and where it breaks or bloats.
4. **The representation** — the one arrangement in which the answer becomes
   visible (pedagogy §10).
5. **The abstraction it earns** — the statement, definition or equation that
   arrives last, as the name for what was watched.
6. **The boundary** — what the section will NOT teach; the transfer exercise.

If line 4 cannot be written, the passage is not ready to be a film — it is a
*reading*, and the honest move is to log it `not-yet-sectionable` with the
reason (usually: the source states the abstraction without a case, so the
case must be invented and then fact-checked as our own).

If lines 2–5 need TWO answers, the passage is two sections.

## What a chapter usually yields

- A textbook chapter: 2–5 sections. Its "key terms" list is a *hint* at
  section boundaries, not the boundaries themselves — terms cluster around
  the abstraction each section earns.
- A research report or long post: 1–3 sections. Its executive summary is
  the TL;DR candidate; its figures are the representation candidates (every
  figure is REBUILT as Manim, never lifted — REBUILD LAW).
- Front matter, prefaces, summaries and exercise lists are never sections
  (books/ rule 5: chapters only, no stubs).

## The card format

Written to `<book>/youtube/tldr-sections-<source-slug>.md` (a report with no
book: `<report-folder>/youtube/…`). Append on re-runs; never overwrite a card
the human has marked.

```markdown
# tldr sections — <source title>

Source: <path or URL> · read <YYYY-MM-DD> · <N> sections · <M> deferred

## S1 · <Section title, Title Case>                      tier: single-insight
- question:        Why does the order you multiply two matrices in change the answer?
- key case:        two 2×2 matrices — a rotation and a shear — applied both ways to the same arrow
- naive:           "just multiply the numbers" — works, gives two different boxes, explains nothing
- representation:  the grid: a matrix is where the two basis arrows land; composing = following them
- abstraction:     AB ≠ BA because composition of transformations is not commutative
- boundary:        when it IS commutative (same-axis scalings, rotations in 2-D) → YOUR TURN
- terms (prereq):  vector, basis vector, matrix (row/column read)      ← TERMS beat, or "none"
- equations:       (AB)v = A(Bv)                                       ← each fires a TANGENT
- source span:     §2.3–2.4, figures 2.6–2.8
- status:          pick | deferred | built → tldr-matrix-order

## S2 · …
```

`tier` comes from the length procedure (pedagogy §5) run on the card's arc
counts. `status` is the human's column.

## One film per section — the default and its exception

**Default: one film per section.** Sanderson's stated advice is *be niche*
(pedagogy §0); a section is a film-sized topic, and a 3–6 minute film that
lands one aha outperforms a 12-minute film that lands three half-ahas.

**Exception — the multi-act film (2–3 sections in one reel):** only when the
later sections *re-use the earlier section's key case* — the same objects
stay on screen and the second section's HOOK is the first section's
BOUNDARY. Then the film is one continuous lesson with section cards
(FormACard, Title Case) at the joins, and the plan must say in one line why
the sections cannot stand alone. Multi-act needs the human's explicit
approval at GATE S; `all` does not grant it.

## GATE S

Present the cards, ranked by how well line 4 (the representation) is
already visible in the source (a source with a strong figure or worked
example sections more safely than one that only asserts). Then wait.

- `pick S1 S3` → build those, one reel folder each, in that order.
- `all` → every card with `status: pick`, one film each.
- `S1+S2` → the multi-act exception for those two, with the reason logged.
- A card the human declines is set `deferred` with a reason, never deleted.

Nothing builds before a pick — in `--silent` mode too. The sections file is
the one artifact `--silent` still stops on.

## After GATE S

Per chosen section, the SKILL.md workflow from step 2 (`plan`). The card's
six lines seed the plan directly: question → B01's corrected text; key case
→ HOOK; naive → NAIVE; representation → SHIFT; abstraction → ABSTRACTION (+
TANGENT per equation); boundary → BHTF; terms → B02 or "none, because…".
The TL;DR lines are written LAST, from the finished plan — the gist of an
argument is known only once the argument exists.
