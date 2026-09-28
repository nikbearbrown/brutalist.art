---
name: tldr
description: >
  Build a TL;DR film from a book chapter or any written report — Liam, in for
  Bear, gives the whole point up front, then EARNS it in one or more LEARN
  sections written on the 3Blue1Brown pedagogical template (concrete before
  abstract, a mystery not a syllabus, the natural wrong turn shown and
  corrected, ONE revealing representation, transform-don't-cut Manim, the
  abstraction arriving as the answer), and closes on the your-turn standard.
  Fixed spine: B00 TL;DR·WHAT (ClaudeTldrWhat — what this film is about) → B01
  TL;DR·WHY (ClaudeTldrWhy — why you should care, the relevance) — two cards on
  the TL;DR page, never the composer → B02 THE QUESTION (BrutalistHesitantWriter
  — the naive question corrected into the real one) → B03 TERMS
  (ClaudeDefinitions — only if there is jargon) → LEARN
  section(s), pure Manim → BVDT recap → BHTF your turn → BOUT locked
  @NikBearBrown outro. A source is first cut into learning sections
  (SECTIONS.md, one candidate film per section, human picks), then each film
  builds. Use when the user types `tldr`, `tl;dr`, `tldr <chapter | report |
  path | paste>`, or asks for a TL;DR film, a chapter explainer, or a
  3Blue1Brown-style walkthrough of written material. Register: Teardown with
  the discovery voice. Kokoro `am_onyx`, free. Never publishes.
---

# tldr — the point first, then earned

> Sibling of `ai-explainer` (one insight, illustrated), `deep-explainer`
> (multi-act documentary) and `cc-explainer` (terminal-first). Same Claude
> bookends, same laws. What is different here: **the body is a lesson, not an
> argument.** A tldr film takes written material a reader would skim — a
> chapter, a report, a long post — states its point in the first breath, and
> then teaches that point the way 3Blue1Brown teaches: a concrete case the
> viewer can hold, a question they want answered, the obvious attempt and
> where it breaks, one representation that makes the answer visible, and the
> general statement arriving last, as the name for what they just watched.

Spec set by Bear 2026-09-22, in his words: *"first beat is a tldr of the film,
Liam, the same Liam in for Bear … second beat is the question the film is
asking using hesitant writer … summarizes any key terms in the third beat
like cc explainer does … the outro is the same as the ai explainers with
recap, your turn and the branding beat … the intent is to go through book
chapters or other written reports, break into one or more learning sections
(topics for a film) and make the film … the learning content beats are pure
3Blue1Brown template: pedagogy and structure."*

## Lineage — what governs when

EXTENDS `../ai-explainer/` (which extends `../explainer/`). Nothing here
repeals a parent law; this file adds the genre's own contracts.

- **Bookends, brand, laws** → `../ai-explainer/SKILL.md`: COLD OPEN LAW,
  EXECUTIVE-SUMMARY LAW (satisfied here by B00 — see the TL;DR contract),
  ASK→RESULT, ILLUSTRATE, SHOW-DON'T-TELL, SPARK-LINE, REBUILD, DOUBLE-CHECK,
  FILL-THE-CANVAS, LOGO, VISUAL QC, HANDOFF, OUTRO, PIXEL-ART, DOODLE-BANNED,
  IN-FOR-BEAR, GATE L (library-first), the PROOF GATE, GATE T.
- **The closing three** → `../your-turn/SKILL.md`: VERDICT
  (`ClaudeVerdictArtifact`, BVDT) → YOUR TURN (`ClaudeComposerAsk`, BHTF,
  greeting `Your turn.`, prompt read in full) → TITLE re-read
  (`ClaudeTitleOutro`, BOUT). `OUTRO-LOCK.md` binds: exact title restate,
  hardcoded `@NikBearBrown`, slug-seeded mascot, no subline, spoken not scored.
- **THE QUESTION and TERMS** are the tldr forms of cc-explainer's THE IDEA
  and DEFINITIONS (`../cc-explainer/SKILL.md`) — same pedagogy (the one
  corrected phrase IS the misconception; terms only when unavoidable, one
  plain line each), Claude cream stage instead of the CC terminal.
- **How graphics are MADE** → `../explainer/` doctrine: MOTION.md,
  EQUATIONS.md (the equation tangent), `manim/animated_graphics.py`
  conventions, the slot contract; `docs/MATH-TYPESETTING.md` for any math.
- **Pacing** → `../duration-planner/`: duration is an OUTPUT. The
  pedagogy's length procedure (`reference/pedagogy.md` §5) derives it.
- **This file** governs: the spine, the TL;DR / QUESTION / TERMS contracts,
  sectioning (how written material becomes films), the LEARN pedagogy and
  its gates, the Manim laws for LEARN beats, and the output contract.

## Who narrates

**LIAM LAW.** Liam, in for Bear, narrates every beat — TL;DR, body and the
closing three. Kokoro `am_onyx`, free. He says so in B00 ("This is Liam, in
for Bear.") and the outro card speaks the title then "At Nik Bear Brown". No
other persona, no clone of Bear's delivery (IN-FOR-BEAR LAW).

**Register.** Teardown for the bookends (the verdict names what the source
gets right and where it over-reaches). Inside the LEARN sections the voice is
the **discovery voice** (`reference/pedagogy.md` §3): "what if we tried—",
"notice what just happened", "you'd guess … and you'd be almost right". Never
"it can be shown that". The narration REACTS to what moves on screen
(SHOW-DON'T-TELL); it does not read a chapter over wallpaper.

## The spine (fixed)

```
B00  TL;DR · WHAT   ClaudeTldrWhat — the TL;DR PAGE, card one. NOT the
                    composer (Bear, 2026-09-22). Wordmark "TL;DR." with the
                    terracotta period; "[hello], Liam" (world-language
                    rotation; Wagwan stays Bear's) + the course/topic line;
                    heading "What This Film Is About"; the QUESTION writes on
                    word by word; 2–3 numbered lines land one per spoken
                    clause, the just-landed numeral in terracotta. Liam signs
                    in and SAYS what the film is about.
B01  TL;DR · WHY    ClaudeTldrWhy — the TL;DR PAGE, card two: the RELEVANCE.
                    Same header (a page turn, not a cut to something new);
                    heading "Why You Should Care"; the STAKE writes on in one
                    sentence; 2–3 consequence lines land on their clauses,
                    marked by terracotta dashes (numerals belong to card one).
                    Liam answers "why should you care?" in plain words.
B03  TERMS          ClaudeDefinitions — ONLY if the film has jargon the viewer
                    arrives needing. 2–5 rows, one plain line each, in order
                    of first use. Never the term the film exists to EARN.
                    Skip the beat (and say so in CHECKS-REPORT.md) otherwise.
     ─── LEARN section 1  (beats B10–B19) ───
     [B10 SECTION]  FormACard, Title Case — only when the film has ≥ 2 sections
     HOOK           the key case, unsolved, on screen
     INSTANCE ×2+   concrete, parametrized, SHOWN MOVING (vary, replay)
     NAIVE          the obvious attempt; where it breaks, on screen
     SHIFT          the revealing representation arrives
     TRANSFORM      the same objects morph — the aha; narration slows
     ABSTRACTION    the general statement / the name — arrives LAST
     [TANGENT]      fires after any ABSTRACTION that lands an equation
     PAYOFF         the HOOK's object back on screen, resolved
     [BOUNDARY]     what this section did NOT teach (one line; often folded
                    into the next section's HOOK or into BHTF)
     ─── LEARN section 2  (beats B20–B29) … only when SECTIONS.md says so ───
     ─── your-turn standard (beat ids checked by GATE BOOKEND) ───
BVDT VERDICT        ClaudeVerdictArtifact. "Let's recap with Claude." then the
                    TL;DR restated in the film's own nouns — now earned.
BHTF YOUR TURN      ClaudeComposerAsk, greeting "Your turn.", topic carries
                    "YOUR TURN". The prompt is the TRANSFER exercise: a changed
                    instance the viewer predicts and explains with Claude.
                    Read aloud in full, then discussed.
BOUT OUTRO          ClaudeTitleOutro — OUTRO-LOCK. narration_text =
                    "<exact title>. At Nik Bear Brown." kind: outro_voice,
                    1.0 s silent tail, no jingle.
```

**Beat ids are positional on purpose.** Section *k* owns `Bk0`–`Bk9`; the
Manim scene for beat `B23` is `class B23_<Name>` in `scenes.py` and the
pacing block keys the scene to its narration by that id. A section that needs
more than nine body beats is two sections (density rule, pedagogy §6), not a
tenth beat.

**GATE BOOKEND** (`runtime/scripts/bookend_check.py`) knows this skill:
with `metadata.skill: "tldr"` the cold open may be `ClaudeTldrWhat` (the
composer is still accepted). BVDT/BHTF/BOUT carry their ids unchanged.
Setting `metadata.skill` is therefore required, not optional.

## The four opening contracts

Two TL;DR cards, then the question, then the terms (Bear, 2026-09-22: "TLDR
needs two beats: 1. what is this film about? and 2. why should you care? What
is the relevance — then the hesitant writer beat and the rest"). Both cards
live on the same TL;DR page — **never the Claude composer** — so B00→B01 reads
as a page turn. Together they are the EXECUTIVE-SUMMARY LAW's one legal
exception ("a reel whose cold open ALREADY is the whole idea") used
deliberately, so that B02 is free to hold the question.

### B00 — TL;DR · WHAT (`ClaudeTldrWhat`)

```ts
// ClaudeTldrWhat — runtime/remotion/src/scenes/ClaudeTldrWhat.tsx
{ eyebrow?: string,           // 'TL;DR' — the wordmark; the period is the terracotta
  heading?: string,           // 'What This Film Is About'
  greeting: string,           // '[hello], Liam' — world-language rotation (lexicon in ../ai-explainer/SKILL.md)
  topic?: string,             // course / subject line, plain Title Case (course films: 'INFO 7375 · … · Chapter N')
  question: string,           // the question this film answers, in the viewer's words; writes on word by word
  lines: string[],            // the TL;DR, 2–3 lines: (1) the answer; (2) what you will see or be able to do; (3) the trap
  cues?: number[],            // seconds into the beat: question, then each line — set them ON the spoken clauses
  durationSeconds: number,    // = the beat's measured audio (rewrite after any re-narration)
  folderLabel?: string }      // '@NikBearBrown'
```

Motion is the contract: the wordmark lands, the question writes on, each
line lands as Liam reaches its clause and its numeral takes the one
terracotta while the previous settles to ink. A B00 whose lines are all on
screen from frame one is a slide (SHOW-DON'T-TELL). Write `cues` from the
narration's word positions; verify on a frame at ~50% that only the lines
already spoken are visible.

Narration: `"<Hello>. This is Liam, in for Bear[, with <course>]. This film is
about <one sentence>. <line 1>. <line 2>. <the trap>."` — 45–70 words. The
TL;DR is the gist, not the
mechanism: it names the shape of the answer and the stakes and leaves the
representation, the instances and the aha for the body. **The TL;DR paradox
rule:** giving away the conclusion does not spend the reveal, because the
reveal in a 3Blue1Brown lesson is *seeing why*, not *hearing what*. If the
TL;DR line already explains the mechanism, it is too long — cut it back to
the claim.

### B01 — TL;DR · WHY (`ClaudeTldrWhy`)

The relevance: why the viewer should care, before any mechanism. Same page
header as card one (the wordmark holds; the greeting drops; the course line
stays), a new heading, and a different body — a STAKE and its consequences.

```ts
// ClaudeTldrWhy — runtime/remotion/src/scenes/ClaudeTldrWhy.tsx
{ eyebrow?: string,           // 'TL;DR'
  heading?: string,           // 'Why You Should Care'
  topic?: string,             // same course / subject line as card one
  lead: string,               // the stake in ONE sentence; writes on word by word
  lines: string[],            // 2–3 consequences: what goes wrong without this, what it unlocks
  cues?: number[],            // seconds: lead, then each line — on the spoken clauses
  durationSeconds: number,    // = measured audio
  folderLabel?: string }
```

Write the relevance for THIS viewer (the sectioning card's audience): where
this idea shows up in their work, what misreading it costs, what having it
unlocks. Never "this is important" — name the consequence. Narration: `"Why
should you care? <stake>. <consequence 1>. <consequence 2>. <what it
unlocks>."` — 45–65 words. The mark is a dash, not a numeral, so the two
cards never look like one list continued.

### B02 — THE QUESTION (`BrutalistHesitantWriter`)

The question the film is asking, written in front of the viewer, and
corrected once. The correction is the pedagogy: the writer first types the
question a viewer would arrive with (the naive framing — the trap door,
pedagogy §2), then replaces the phrase that makes it the wrong question.

- `text` — 2–4 short lines (`\n`), ending on the film's real question. Read
  back with the replacements applied, it must be exactly the question the
  LEARN section answers.
- `triggerWords` / `replacementWords` — the ONE phrase (a whole phrase when
  the misconception lives in a phrase — never a lone noun that leaves the
  sentence wrong). Worked example: "Why is matrix multiplication *so hard to
  compute*?" → "…*order-dependent*?" — the naive question is about effort,
  the real one is about geometry.
- Palette — the component's cream defaults (`CLAUDE.PAGE` / `CLAUDE.INK` /
  `CLAUDE.SPARK`); pass nothing. `face` serif; `fontSize` 60–78 by length.
- Pace — `charMs` 22–32, `hesitateBetween` 6–8, `hesitateWithin` 1,
  `mistakeRate` 5, `jitter` 20; `seed` = the slug (never the shipped default).
- Narration — Liam reads the CORRECTED question, then one breath on why the
  first version is the trap. 20–35 words, `lead_silence_s: 0.8`, audio window
  ≥ 9 s. Verify after render that the correction is on screen before the cut.

### B03 — TERMS (`ClaudeDefinitions`)

Only when the film has jargon the viewer *arrives* needing. The audience is a
smart person who has not read the chapter: define each term at a high level,
one plain line, no lecture. **DEFINITIONS-ARE-ENDPOINTS still binds** (pedagogy
§1.4): TERMS holds *prerequisite* vocabulary the LEARN section will use
without stopping — never the concept the film exists to earn. If the word
being defined is the film's answer, it does not belong here; it belongs in
the ABSTRACTION beat, arriving last.

```ts
// ClaudeDefinitions — runtime/remotion/src/scenes/ClaudeDefinitions.tsx
{ title?: string,                       // default 'Terms In This Film' (Title Case)
  terms: [{ term: string,               // ≤ 22 chars, as written on screen
            meaning: string }],         // ≤ ~80 chars, wraps to two lines max
  durationSeconds: number,              // = the beat's measured audio (set after audio lock)
  startCue?: number, rowGap?: number,   // frames; default: rows land across 12–70% of the beat
  dark?: boolean,                       // charcoal polarity; off by default
  folderLabel?: string }                // '@NikBearBrown'
```

Rows land one at a time in the order Liam reads them; the row that has just
landed carries the one terracotta, earlier rows settle to ink. Liam reads
each line once. 2–5 terms; the beat runs 10–20 s.

## Sectioning — how written material becomes films

`tldr <source>` never starts with a beat sheet. It starts by reading the
WHOLE source and cutting it into **learning sections**: the units a viewer
can learn in one sitting, each with one key case and one revealing
representation. Full procedure and card format: `reference/sectioning.md`.

- Output: `<book>/youtube/tldr-sections-<source-slug>.md` (for a report with
  no book, `<report-folder>/youtube/…`). One card per section: the question,
  the key case, the naive attempt, the representation, the abstraction it
  earns, the boundary, the prerequisite terms, and an estimated tier.
- **Default: one film per section.** Sanderson's stated advice is *be niche*;
  a section is a film-sized topic. A film carries 2–3 sections only when they
  share one key case that the later sections re-use (multi-act tier, needs
  the human's explicit approval at GATE S).
- **GATE S (sections).** The human picks which cards become films, or says
  `all`. Nothing builds before a pick. A card the human declines is logged
  `deferred` on the sections file, never silently dropped.
- Then, per chosen section: the build workflow below, one reel folder each.

## The LEARN pedagogy — the 3Blue1Brown template as gates

Read `reference/pedagogy.md` before every plan. It is the ported Brown Blue
constitution (`brutalist-art/skills/make/math-explainer/reference/pedagogy.md`,
retired tree) plus the seven-stage template and the scene-level unit from
Bear's 2026-09-22 research notes, all as enforceable checks. The short form:

1. **Concrete before abstract — enforced.** Two moving INSTANCE beats before
   any ABSTRACTION beat for that abstraction, or the plan fails Gate 1.
2. **Mystery, not syllabus.** The HOOK is the key case, unsolved. "Today
   we'll cover…" is banned as an opener. The gap between what the rules
   predict and what happens is the section.
3. **The natural wrong turn, shown.** NAIVE is the attempt the viewer would
   make; it is walked, on screen, to where it breaks or bloats. Not a straw
   man — the attempt that *almost* works.
4. **One representation, chosen before any animation.** SHIFT introduces the
   arrangement in which the relationship becomes visible (a grid that moves,
   a signal wound on a circle, layers of equal distance). If a rough sketch of
   it does not reveal the relationship, the explanation is not ready — fix
   the model, not the motion.
5. **Exactly one collision.** TRANSFORM is the aha: two threads the film set
   up separately meet, as one continuous morph of persistent objects. One per
   section. Three diluted ahas is a plan failure.
6. **Definitions are endpoints.** ABSTRACTION names what the viewer has been
   pointing at for a minute. Test: would "this thing deserves a name" feel
   overdue? If not, it is too early.
7. **Every landed equation fires the tangent** (`../explainer/EQUATIONS.md`,
   ~30–45 s, five zones, explain never derive), on the split stage: equation
   persists on the MAIN side, zones write into the SIDE band.
8. **Predict before the reveal.** At least one hold before TRANSFORM where
   Liam asks the viewer to commit ("Before it moves — where does the red
   arrow land?"), then it moves.
9. **Boundary, not completeness.** Nothing "for completeness". What was not
   taught is named in one line and becomes the transfer exercise in BHTF.
10. **Length is derived** (pedagogy §5): count the arc, add the holds, report
    the tier at Gate 1. Single-insight films land at roughly 3–6 minutes with
    bookends; never pad, never rush — cut scope instead.

**The scene-level unit.** Every LEARN beat is authored as
QUESTION → ACTION → OBSERVATION → INFERENCE → NEXT QUESTION (pedagogy §9),
recorded in the beat's `learn` block. A beat whose `next_question` is empty
is the section's last beat or a defect.

## Manim laws for LEARN beats

LEARN beats are `shot.type: "GRAPHIC"`, `shot.manim.class: "Bk#_Name"`, one
`Scene` each in the reel's `scenes.py` (the run.sh contract; exemplar:
`examples/deep-explainer/claude-liam-fluency-trap/scenes.py`). No Remotion
cards inside a LEARN section except the optional section card; no pantry, no
stills, no shopping list — everything in a lesson is drawable.

- **Transform, don't cut.** Within a section, state changes are morphs of
  persistent objects (`Transform`, `ReplacementTransform`,
  `.animate.apply_matrix`, `ValueTracker` sweeps). Objects keep their identity
  across beats: the HOOK's arrow is the PAYOFF's arrow. A hard cut is legal
  only at a section boundary. Because run.sh renders one scene per beat, a
  section's scenes share a module-level *state factory* (the same objects
  rebuilt at the previous beat's end state) so the join reads as continuous —
  the last frame of `B12` is the first frame of `B13`. Write the factory
  once; assert it in each scene's first line.
- **Palette — the Claude stage, one accent.** Cream `#F2F0E9`, ink `#3D3929`,
  terracotta `#D97757` as THE accent, `#8B8F96` dim for the before-state /
  foil, `#D9D4C7` ghost for scaffolding. Color roles, mapped from the 3b1b
  grammar: the OBJECT under study is ink; the FOIL / before-state is dim; the
  HIGHLIGHT — the element the narration points at *right now* — is
  terracotta, and it moves with the sentence and fades when the sentence
  ends. One terracotta moment per beat. `metadata.learn_canvas: "dark"` flips
  the whole film's LEARN sections to the dark canvas (`#1F1E1B` ground,
  `#F2F0E9` ink, same accent) — per film, never per beat; the bookends stay
  cream. DESIGN-PRINCIPLES.md: dark-canvas Manim exhibits are dark by
  nature, not by the polarity roll.
- **Type.** EB Garamond for every label (`font="EB Garamond"`), `MathTex` for
  every equation (MATH-TYPESETTING.md — never a formula as a text string),
  type floor 32 (titles 40), no `slant=ITALIC` on multi-word text (Pango
  collapses spaces). GATE T reads a thin terracotta horizontal shape as
  accent text — draw underlines in ink or dim.
- **Motion carries the claim.** Every LEARN scene changes a non-text shape
  before its final play (Gate A/B); a scene that only writes text is a card,
  and a card inside a LEARN section is a defect. Reveals land on the spoken
  word (`show` events at fractions of the beat; `sub_beats` when a move must
  hit mid-sentence). Easing: Manim's default `smooth`; no bounce, no
  scale-on-mount, no decorative motion (Mayer's coherence principle, parent
  MOTION.md).
- **Preserve identity, change one thing.** Hold the example steady and vary
  one parameter per INSTANCE; keep labels attached to their objects as they
  move; map every symbol back to the object it names, beside it, when it
  first appears (ABSTRACTION beat).
- **Mark simplifications on screen.** A projection, an idealization, a
  2-D stand-in for an n-D object gets one small dim caption naming what is
  omitted, once per section.
- **Pacing block.** Each scene stretches to its beat's measured narration via
  the `_TARGET` pacing pattern (see the exemplar); a TRANSFORM beat's
  narration is deliberately short so the morph gets the seconds — write ≤ 1
  sentence and let `run_time` fill the audio. Silence over a finished
  picture is teaching; a HOLD is written as narration that stops describing,
  never as an empty beat.

## Workflow (each gate is the human's)

1. **`tldr <source>`** — read the WHOLE source; write the sections file
   (`reference/sectioning.md`). Present the cards. **GATE S: pick.**
2. **`plan <section>`** — for one chosen section: the TL;DR lines, THE
   QUESTION's text + corrected phrase, TERMS (or "none, because…"), the LEARN
   beats with roles and `learn` blocks, `show` blocks (SHOW-DON'T-TELL binds
   at authoring), the representation named in one sentence, the equation(s)
   that will land and their tangents, the length procedure and tier, the
   Gate-1 audit table (pedagogy §8) filled. GATE L per beat
   (`./art scenes …`). Write `CHECKS-REPORT.md` (PROOF GATE) and the sheet.
   **GATE: approve the plan.**
3. **`factcheck`** — every claim, number and worked value against the source
   and by independent computation (every instance's numbers are recomputed,
   every equation's algebra is verified separately from its typography);
   strip the datable; `FACTCHECK.md`. **GATE: claims hold.**
4. **Audio** — `runtime/scripts/generate_audio_kokoro.py <reel>` (Liam,
   `am_onyx`, free). Measured mp3s are the clock. Then write each Remotion
   beat's `durationSeconds` (B02) from `actual_duration_s`, and the BOUT tail
   (`tail_silence_s: 1.0`).
5. **`scenes.py`** — one Scene per LEARN beat, the state factory per section,
   the pacing block. `./art run <reel> --height 2160` → Gate A/B → Gate V →
   GATE T → GATE BOOKEND → **read the frames** (`_qc/`, `qc-sheet.png`; every
   equation at its revealed states and at 15/50/85% of its beat). Fix at the
   source, re-run. **GATE: watch the cut.**
6. **`./art final <reel> --height 2160`** → the master, in the reel folder.
   `BUILD-PROMPT.md` ships beside it. **STOP.** Never stage, never publish
   without Bear's word.

`--silent` (`skills/SILENT-MODE.md`) removes the human from steps 2–5, never
from GATE S and never from the stop line.

## Output contract

```
<book>/youtube/tldr-sections-<source-slug>.md    the section cards (GATE S)
<book>/youtube/tldr-<concept>/
  beat_sheet.json     metadata.skill "tldr"; beats carry role / section / learn
  scenes.py           one Scene per LEARN beat; state factory per section
  BUILD-PROMPT.md     paste-ready end-to-end rebuild
  BUILD-LOG.md        decisions, MISSING: lines, gate signatures
  FACTCHECK.md        claim | verdict | source or derivation | fix
  CHECKS-REPORT.md    SHOW/HOLD/CARD tally + the teaching arc + the Gate-1 table
  SOURCES.md          the source (path, section, date read), corrections, seeds
  TYPECHECK.md        GATE T (written by the run)
  mp3/  manim/  media/  mp4/  _qc/
```

Slug convention `tldr-<concept>` (`tldr-matrix-order`); one folder per film;
built INTO the owning book's `youtube/`, never into the toolkit.
`metadata.skill: "tldr"`, `metadata.style_preset: "tldr"`, `channel`
`claude-liam`, `engine` `kokoro`, `voice` `am_onyx`, `register` `Teardown`,
`palette` `claude`, `learn_canvas` `cream` | `dark`. Skeleton with every
bookend and one section: `reference/example-tldr-beat_sheet.json`.

Beat fields this genre adds (all read by the plan audit, none by the
renderer): `role` (HOOK · INSTANCE · NAIVE · SHIFT · TRANSFORM · ABSTRACTION ·
TANGENT · PAYOFF · BOUNDARY · SECTION), `section` (int), `learn`
(`{question, action, observation, inference, next_question}`), and on the
one predict beat `predict: true`.

## Hard rules (this genre's own — parents' rules all still bind)

1. **THE POINT FIRST, THEN THE RELEVANCE.** B00 says what the film is about
   and shows it on the TL;DR page; B01 says why the viewer should care. A tldr
   film that opens on a tease is not a tldr; one that skips the relevance is a
   summary.
2. **TWO TL;DR CARDS (WHAT, then WHY), THEN THE QUESTION; TERMS ONLY WHEN NEEDED.** The
   hesitant writer's correction is the film's misconception. TERMS never
   holds the term the film earns.
3. **SECTIONS BEFORE SHEETS.** No beat sheet before the sections file and a
   human pick (GATE S). One film per section by default.
4. **CONCRETE BEFORE ABSTRACT — GATED.** ≥ 2 moving instances before each
   abstraction; definitions arrive as endpoints; the HOOK is unsolved and
   mystery-framed. Failing any of these fails the plan gate.
5. **ONE REPRESENTATION, ONE COLLISION.** The SHIFT names it; the TRANSFORM
   lands it; once per section.
6. **PURE MANIM IN THE LESSON.** LEARN beats are Manim scenes on the Claude
   stage; transform-don't-cut inside a section; no cards, no stills, no
   pantry, no shopping list, no AI video, ever.
7. **BOOKLOOP LAW.** The film teaches the idea standalone: the book, chapter
   and course are not named on screen or in narration ("the chapter I'm
   reading" at most) — EXCEPT course films (INFO 7375 and siblings), which
   carry the course credit. SOURCES.md always names the source in full.
8. **FACTCHECK + GATE T + GATE BOOKEND, ALWAYS.** `FACTCHECK.md` with every
   instance recomputed; `TYPECHECK.md` with no FAIL; the four bookends in
   order. A run or final that reports success without them is not done.
9. **DURATION IS DERIVED.** Report the tier at the plan gate; never pad to a
   length, never cut an INSTANCE to hit one — cut scope.
10. **NEVER PUBLISH.** The master stays in the reel folder. Staging is the
    `post` skill on Bear's word; public is a manual Studio flip.

## Reference files (this folder)

- `reference/pedagogy.md` — the 3Blue1Brown template as gates: sequencing
  checklist, mystery framing, discovery narration, beat roles and the Gate-2
  audit, length procedure, density rule, the boundary, the seven-stage
  template, the scene-level unit, the representation checklist, the
  animation-carries-reasoning table, the three learning checks, sources.
- `reference/sectioning.md` — cutting a chapter or report into learning
  sections: the section test, the card format, the one-film-per-section
  default and its exception, GATE S.
- `reference/example-tldr-beat_sheet.json` — a skeleton sheet: every bookend
  plus one complete LEARN section, ready to copy and fill.
