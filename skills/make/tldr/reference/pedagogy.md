# The 3Blue1Brown template, as gates — the tldr pedagogical constitution

Ported 2026-09-22 from the retired Brown Blue constitution
(`brutalist-art/skills/make/math-explainer/reference/pedagogy.md`, hyphen
tree, read-only) and extended with the seven-stage template, the scene-level
unit and the learning checks from Bear's 2026-09-22 research notes on
Sanderson's method. This file is the reason the tldr skill exists; the look
is downstream of it.

**Provenance discipline.** Three kinds of claim are mixed below and are
labelled where it matters: (S) Sanderson's *stated* advice — his site's
creator FAQ and the Summer of Math Exposition writeups; (L) patterns *read
off* his published lessons; (H) *house synthesis* — our operationalization.
Never present (H) as Sanderson's rule.

## §0 The problem this template solves (S)

Most technical explanation presents the general framework first and then
populates it with examples. Sanderson's stated position is that this is
backwards for anyone who does not already understand the material: the
limiting factor is *motivation*, not explanation quality. Nothing made the
learner want to hold the idea long enough for it to click. So the order is
inverted — concrete example → tension → the abstraction, arriving as the
thing that resolves the tension. This is a narrative insight borrowed from
fiction (stakes, a mystery, a climax where two ideas collide), not a
visual-effects insight; Manim is downstream of it.

His stated principles, verbatim in spirit (S): *concrete before abstract*;
*open with the key exercise, don't save it for the end*; *topic choice
matters more than production quality*; *be niche*; *just start and iterate
publicly*. His SoME judging criteria (S): clarity, motivation legible in the
first ~30 seconds, novelty of the experience (not of the topic).

## §1 The sequencing checklist (Gate 1 — hard requirements)

A plan fails Gate 1 unless all five hold:

1. **The key case is identified and named** in one line at the top of the
   plan (not in the film): the concrete puzzle, computation, anomaly or
   before/after contrast that motivates everything. Problem topics supply
   their own key exercise; expository topics need a key *case* — a
   representative event, an anomaly, a fact that should predict but doesn't.
2. **The section opens with it, unsolved** (the HOOK). No vocabulary, no
   notation, no "today we'll cover" before the viewer has felt the problem.
   (In a tldr film the TL;DR beat has already named the *answer's shape*;
   the HOOK still opens the section on the unsolved case — see the TL;DR
   paradox rule in SKILL.md.)
3. **Concrete instances precede every abstraction.** At least two
   parametrized instances of the phenomenon are *shown moving* before the
   general statement. Manim makes instances cheap: vary the parameter,
   replay the transformation.
4. **Definitions are endpoints.** A term or symbol is introduced only after
   the viewer has enough structure to *want* a name for it. Test: could the
   narration say "this thing we keep pointing at deserves a name" and have
   it feel overdue? If not, the definition is too early. (The TERMS beat is
   not an exception: it holds *prerequisite* vocabulary only.)
5. **No premature completeness.** Nothing is included "for completeness".
   Edge cases, generalizations and caveats that do not serve THIS section's
   one insight are cut or deferred (logged under `deferred` in the plan).

## §2 Mystery framing, not utility framing (Gate 1)

The HOOK is **mystery-framed**: a specific tension the viewer needs
resolved. Utility framing is banned as an opener.

- Utility (banned as opener): "Understanding X is critical for Y. Today
  we'll see how X works."
- Mystery (required): state the fact that *should* predict an outcome, then
  the case where it doesn't. "Same two matrices. Multiply them this way, you
  get a rotation. Multiply them the other way — a shear."

The generalizable move (H): **find the gap between what the rules predict
and what actually happens.** That gap is the section.

## §3 Discovery narration ("inventing math") (S/L)

Narrate as re-invention, not transmission. The viewer should feel walked
through reasoning that *could plausibly have led* to the discovery — not
handed the polished, discovery-erased final form.

- Voice moves: "what if we tried—", "notice what just happened", "so we're
  stuck — unless—", "you'd guess … and you'd be almost right."
- Wrong turns are valuable when they are the *natural* wrong turn (the one
  the viewer would take), shown briefly and corrected on screen — this is
  the NAIVE beat, and "empathy for the misconception" is its whole point.
- Never "it can be shown that." If it can be shown, show it; if showing is
  out of scope, say so plainly and point to the BOUNDARY.
- Sanderson's own note (S, Dwarkesh interview): understanding something does
  not preserve your memory of being confused by it. Plan the sequence of
  *changes in the viewer's understanding* before the sequence of facts.

## §4 Beat roles (Gate 2 — the beat sheet is audited against this arc)

Every LEARN beat carries a `role`; the roles appear in this partial order
within a section:

```
HOOK         the key case, unsolved (opens the section)
INSTANCE     a concrete parametrized example, shown moving   (≥ 2 before any ABSTRACTION)
NAIVE        the obvious attempt, walked to where it breaks or bloats
SHIFT        the revealing representation arrives — the reframe
TRANSFORM    the same objects morphing — the collision, the aha (exactly one per section)
ABSTRACTION  the general statement / definition / equation — arrives as an ENDPOINT
TANGENT      unpacks a landed equation — fires after any ABSTRACTION that is an equation
PAYOFF       the HOOK resolved by the abstraction; optionally one scale-shift
BOUNDARY     what this section did NOT teach + the transfer exercise (often fused into BHTF)
```

Audit rules (H), walked top to bottom:
- An `ABSTRACTION` with fewer than two prior `INSTANCE` beats *for that
  abstraction* is a Gate-2 rejection.
- A section with zero `TRANSFORM` beats, or more than one, is a rejection.
- The `PAYOFF` must put the HOOK's object back on screen — the same
  persistent object, not a re-draw.
- Any `ABSTRACTION` that lands an equation must be followed by a `TANGENT`
  (`../../explainer/EQUATIONS.md`: five zones, ≤ ~45 s, explain never
  derive). The tangent explains the symbols; the derivation, if any, was the
  ABSTRACTION's arrival.
- `NAIVE` and `SHIFT` are required unless the plan justifies their absence in
  one line (a pure-puzzle section may go INSTANCE → TRANSFORM directly).
- At least one beat before the `TRANSFORM` carries `predict: true` — Liam
  asks the viewer to commit before the reveal (§10).

## §5 The length procedure (run at plan, report at Gate 1)

Length is **derived**, never chosen (`../duration-planner/`). Compute it:

1. Count the arc: 1 HOOK + N INSTANCEs (2–4 per abstraction) + NAIVE + SHIFT
   + 1 TRANSFORM + A ABSTRACTIONs (usually 1) + tangents + 1 PAYOFF (+
   BOUNDARY), per section.
2. A LEARN beat is 20–60 words of narration ≈ 8–25 s at Liam's pace; a
   TRANSFORM beat is deliberately short-spoken and long-shown.
3. Add hold time: a built-up idea gets the seconds it needs to be looked at.
4. Add the bookends: TL;DR (~15 s), QUESTION (~12 s), TERMS (10–20 s if
   present), VERDICT (~25 s), YOUR TURN (~35 s), OUTRO (~6 s).

Tiers this produces:

| Tier | Arc | Typical runtime |
|---|---|---|
| **Single-insight** | 1 section, 1 abstraction, 2–3 instances | 3–6 min |
| **Standard** | 1 section with 2 abstractions, or 2 short sections sharing a key case | 6–9 min |
| **Multi-act** | 2–3 sections, each with its own HOOK | 9–14 min — needs explicit approval at GATE S |

Two prohibitions: **never pad** (no filler beats to reach a "good YouTube
length") and **never rush** (no cutting an INSTANCE to hit a duration — cut
scope: fewer abstractions, a deferred section).

## §6 The density rule (applies at plan, again at scenes)

Err toward more detail *in the plan*, then cut **during planning, never
during animation**. For every anticipated viewer question, three options:

1. Answer it inline if the answer fits in ≤ 2 beats and serves the one insight.
2. Defer it — name it in the BOUNDARY ("why this holds in three dimensions is
   its own film").
3. Cut it silently.

If a detour needs > 2 beats, it is by definition a deferral or a cut. The
Gate-1 audit table lists every detour and which of the three it got. A
section that needs more than nine body beats is two sections.

## §7 The boundary — explain, don't educate (S/H)

An explainer is the intuition half. It does not replace practice, assessment
or procedural fluency, and must not pretend to. Sanderson himself stresses
doing the calculations as part of developing intuition (S).

- Every section ends with a **BOUNDARY**: one sentence naming what was
  deliberately not taught, and **one concrete exercise the viewer can do**
  with what they now have. In a tldr film the exercise becomes the YOUR TURN
  prompt (BHTF) — the handoff from explanation to instruction.
- Never claim the film "teaches you X." It shows why X is true and what it
  feels like; the viewer still has to go do X.

## §8 The seven-stage template (H — a planning aid, not Sanderson's pacing)

A synthesis of what the lessons actually do (L), sized for one section. The
shares are a planning aid for the length procedure, never targets.

| Stage | Share | What the viewer experiences | What you produce | Role |
|---|---:|---|---|---|
| 1. Present the question | 0–10% | "I understand the problem and want an answer." | a specific example, puzzle or observable phenomenon | HOOK |
| 2. Establish the objects and rules | 10–20% | "I know what I'm looking at and what can change." | a small example with explicit assumptions and visible labels | INSTANCE |
| 3. Try a natural approach | 20–35% | "That seems reasonable. Where does it lead?" | a plausible attempt that reveals structure or a genuine limitation | NAIVE (+ INSTANCE) |
| 4. Introduce the revealing representation | 35–55% | "Now I can see something I couldn't before." | the central diagram, transformation, decomposition or comparison | SHIFT → TRANSFORM |
| 5. Develop the insight | 55–70% | "I can anticipate what happens next." | varied examples; what stays invariant | INSTANCE (post-shift) |
| 6. Formalize | 70–85% | "The terminology and formula describe what we just did." | definitions and notation connected to the model | ABSTRACTION (+ TANGENT) |
| 7. Resolve and extend | 85–100% | "I can answer the original question and see where this applies." | the opening example again, a changed case, a boundary | PAYOFF → BOUNDARY |

Stage 3 does not require a contrived mistake — sometimes the natural
approach works and simply needs refinement; its purpose is to make the next
step intelligible. Formalization may happen in small increments through the
section; not every term must wait for stage 6.

**The one non-negotiable across the lessons read (L):** each new concept
answers a question the explanation has already made meaningful.

## §9 The scene-level unit (H)

Every LEARN beat is authored as five lines, recorded in the beat's `learn`
block. It prevents a script from becoming a succession of facts connected
only by "next".

1. **Question** — what uncertainty is active?
2. **Action** — what do we manipulate or compare?
3. **Observation** — what can the viewer now notice?
4. **Inference** — what does that observation justify?
5. **Next question** — what still needs explaining? (empty only on the
   section's last beat)

Worked example (a search-algorithms section):
- Q: How do we find the fewest moves through this maze?
- A: Expand every reachable square one move away, then two.
- O: The search advances in layers of equal distance.
- I: With equal-cost moves, first discovery reaches a square in the fewest moves.
- Next: What changes if some moves cost more than others?

## §10 The representation — the most important design decision (H)

Much of the explanatory power comes from selecting a representation in
which the desired relationship becomes *visible*. Ask, before any animation:
**what could I put on screen that would let the viewer infer the next step?**

Useful families: a spatial arrangement that exposes a relationship · a
process shown one state at a time · a decomposition into simpler parts · two
cases differing in exactly one meaningful respect · a quantity that stays
unchanged while everything around it moves.

Choose it before committing to elaborate animation. If a rough sketch cannot
convey the relationship, the explanatory model needs work, not the motion.

## §11 Making animation carry the reasoning (L/H)

| Design choice | Pedagogical purpose | Practical implementation |
|---|---|---|
| Preserve object identity | follow the same quantity across representations | labels and visual cues stay attached as objects move or become symbols |
| Change one feature at a time | make comparisons interpretable | hold the example steady while varying one parameter |
| Make motion correspond to an operation | show what a transformation *does* | animate the rotation, accumulation, sorting or redistribution when that action IS the concept |
| Coordinate narration and change | make the relevant relationship easy to locate | name an object when highlighting or manipulating it; the terracotta moves with the sentence |
| Map symbols back to objects | give notation a concrete referent | introduce each term beside the quantity or operation it represents |
| Mark simplifications | prevent the visual from suggesting a false claim | one dim caption naming what is omitted, projected, approximated or idealized |

Two lessons show this deliberately (L): the transformer lesson colour-codes
model weights vs. the data flowing through and states its simplifications
of tokens and embeddings; the Fourier lesson refines its "centre of mass"
picture into the actual integral and explains the scaling difference. The
visual model is developed and *corrected* as precision increases.

## §12 The three learning checks (H, with one cited support)

An explanation can create a strong feeling of understanding without
establishing independent skill. Build these in:

- **Prediction** — before the TRANSFORM, ask what happens next (`predict: true`).
- **Explanation** — after the PAYOFF, ask *why* the observed result follows
  (Liam poses it; the VERDICT answers it in one line).
- **Transfer** — change the example and ask whether the same reasoning
  applies (the YOUR TURN prompt).

Independent support for inserting retrieval checks into video lectures:
Szpunar, Khan & Schacter (PNAS 2013) found reduced mind-wandering and
better learning with interpolated tests. That supports the checks; it does
not validate this whole template, and it says nothing about 3Blue1Brown
specifically.

## §13 The Gate-1 audit table (the plan shows this, filled)

| Check | Ref | Pass? |
|---|---|---|
| Key case named | §1.1 | |
| Section opens unsolved; zero vocabulary before the felt problem | §1.2, §2 | |
| ≥ 2 moving instances before each abstraction | §1.3 | |
| Every definition arrives as an endpoint; TERMS holds prerequisites only | §1.4 | |
| Natural wrong turn shown (NAIVE) or its absence justified | §3, §4 | |
| One representation named in one sentence (SHIFT) | §10 | |
| Exactly one TRANSFORM per section | §4 | |
| Every landed equation followed by a TANGENT | §4, EQUATIONS.md | |
| PAYOFF returns the HOOK's persistent object | §4 | |
| Nothing "for completeness"; deferrals logged | §1.5, §6 | |
| Mystery-framed opener; utility framing absent | §2 | |
| Discovery voice; no "it can be shown that" | §3 | |
| Every beat has a `learn` block; next_question chains | §9 | |
| One `predict: true` beat before the TRANSFORM | §12 | |
| Boundary: not-taught + transfer exercise → BHTF | §7 | |
| Length derived + tier reported; no pad, no rush | §5 | |

## §14 Pre-build review checklist (read once before `./art run`)

- Can the intended viewer understand the opening question?
- Does each abstraction have a motivating example?
- Does the central visual reveal a relationship (not decorate a claim)?
- Can the viewer connect each important symbol to its meaning?
- Does every major transition answer a question already raised?
- Are assumptions and limits explicit on screen?
- Does the ending resolve the opening problem with the same object?
- Could a viewer solve or explain a changed case without replaying the film?

## Sources

- 3Blue1Brown, About / creator FAQ (concrete before abstract; open with the
  exercise; topic > production; be niche) — https://www.3blue1brown.com/about/
- 3Blue1Brown, Summer of Math Exposition (judging criteria: clarity,
  motivation, novelty) — https://www.3blue1brown.com/blog/some1/
- Dwarkesh Patel, interview with Grant Sanderson (storytelling; planning the
  viewer's changes of understanding; exercises) — https://www.dwarkesh.com/p/grant-sanderson
- Stanford Daily, 2020-01-24 (characters, stakes, the "climax" analogy)
- Lessons read for §8/§11: Essence of Calculus; Linear transformations and
  matrices; Fourier transform; Transformers — https://www.3blue1brown.com/lessons/
- Szpunar, Khan & Schacter, "Interpolated memory tests reduce mind wandering
  and improve learning of online lectures", PNAS 110(16), 2013 —
  https://www.pnas.org/doi/10.1073/pnas.1221764110
