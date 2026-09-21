---
name: deep-explainer
description: >
  Build multi-act, in-depth documentary explainers with Claude bookends
  and Liam's Teardown narration (free local Kokoro am_onyx). Use for
  deep-explainer, deep reel, or an in-depth Claude-bookended film request.
  Depth determines runtime; executed examples and diagrams are preferred,
  with pantry stills only when the source artifact is necessary. No still
  quota. Explicit tool-evaluation requests activate audit mode. Audio-first,
  phase-gated, with a full review cut and a sourcing list only for genuine
  outstanding assets. Never publishes.
---

# deep-explainer — the long-form Claude-bookended documentary cut

A sibling of `ai-explainer` and `cli-explainer` on the same shared skeleton:
Claude bookends, different MIDDLE. Here the middle is a 5–10 minute
documentary-register body built from executed examples, data and diagrams.
Use human-supplied or archival stills in `pantry/` only when the artifact itself
is necessary evidence, not to decorate a computation. Where
`ai-explainer` makes a tight reel, deep-explainer makes an episode.

## Lineage — what governs when

Math in every beat follows [MATH-TYPESETTING.md](../../../docs/MATH-TYPESETTING.md).
A generic text-card reroute is not a valid substitute for typeset equations,
even when ordinary typography checks pass. Verify algebra and rendered notation.

This skill EXTENDS `ai-explainer`, which extends `explainer`. Nothing below
repeals a parent law; this file only adds the genre's own contracts.

- **Bookends, brand, laws** → `../ai-explainer/SKILL.md` governs: COLD OPEN
  LAW (B00 is `ClaudeComposerAsk`, ask lands answered),
  **EXECUTIVE-SUMMARY LAW** (B01 is `BrutalistHesitantWriter` — the overview of
  what the film is about, typed and corrected on screen; at this length the
  advance organizer matters more, not less, and its ≥ 9s window is a floor, not a
  target), ASK→RESULT LAW,
  ILLUSTRATE LAW, SHOW-DON'T-TELL LAW, SPARK-LINE LAW, REBUILD LAW,
  DOUBLE-CHECK LAW, FILL-THE-CANVAS, LOGO LAW, VISUAL QC LAW, HANDOFF LAW,
  OUTRO LAW, the channels table, IN-FOR-BEAR LAW, and
  **DOODLE-BANNED LAW** (DoodleScene/DoodleChart permanently cut from this
  register; replace with clean Manim/Remotion; §8.0 checker enforces).
- **Closing block** → the `your-turn` skill's three-beat standard: VERDICT
  recap (`ClaudeVerdictArtifact`) → YOUR TURN prompt Liam reads in full
  (`ClaudeComposerAsk`, greeting `Your turn.`) → TITLE re-read
  (`ClaudeTitleOutro`). **@NikBearBrown outro card is locked** — exact title restate, hardcoded `@NikBearBrown` handle, one of the 18 crisp-safe mascots (slug-seeded), NO subline; spoken not scored (Liam: title, then "At Nik Bear Brown"; no jingle); claude-liam reels only. See `OUTRO-LOCK.md`.
- **How graphics are MADE** → `../explainer/` doctrine: MOTION.md,
  EQUATIONS.md (equation tangents), REMOTION.md, the two-axis shot system,
  the slot contract, the pantry law, the slate system, `manim/animated_graphics.py`.
- **Pacing** → `../duration-planner/` doctrine: duration is an OUTPUT.
  The 5–10 min band is the genre's natural landing zone for a multi-act
  concept, never a target to pad toward. If the arc lands at 4:40, ship 4:40.
- **This file** governs: evidence-based beat routing, the vox-beat treatment on the
  Claude stage, the vox-run continuity contract, the shopping-list gate, and
  the deep act structure.

## When this skill (and when not)

Use deep-explainer when the concept is **multi-act** — several linked
mechanisms that each need their own instances and evidence (the source is a
long research doc, a chapter, a framework with 4+ parts). If the source is one
insight, it's an `ai-explainer`; if it's mostly math, it's a `math-explainer`;
if it's mostly a build, it's a `cli-explainer`.

## The `audit` modifier (opt-in — NOT the default)

Arms when the video **evaluates** a tool or method for a subject domain
rather than teaching the subject (e.g. "what can Manim do for physics?",
"is D3 useful for bio?", "capability audit of the simulation pipeline").
Trigger phrases: `audit`, `evaluate the tool`, `what can X do`,
`capability audit`, `is X useful for`. Full doctrine: `AUDIT-MODE.md`
at the toolkit root — read it before building an audit reel.

**Chassis routing note:** choose depth by the teaching problem, not the media
mix. A multi-act audit can use only executed examples and rendered artifacts.
There is no VOX quota; when nothing needs sourcing, record zero outstanding
requests instead of inventing a shopping list.

Three-line summary (read AUDIT-MODE.md for the full rules):

- **Showing ≠ teaching.** The deliverable is a lane verdict — which tool
  fits the domain and where it fails — not a lesson in the domain itself.
- **Exhibits not filler.** Every body visual is a REAL rendered artifact
  under evaluation. Zero AI-generated stills, zero pantry shopping list,
  no asking the human to supply media. If a beat needs connective tissue,
  use a deterministic Remotion eval card (cream, EB Garamond, terracotta).
- **Exhibit gate — hard stop.** If the exhibits don't exist yet, STOP.
  Building the exhibit library is a separate gated step before the audit.

## The spine (fixed)

```
B00 cold open (ClaudeComposerAsk, ask answered, Liam signs in)
B01 hesitant-writer overview (BrutalistHesitantWriter) — the BLUF, typed and corrected
  ACT I   … ACT N        the documentary body (this skill's subject)
VERDICT recap (ClaudeVerdictArtifact)
YOUR TURN (ClaudeComposerAsk, prompt read aloud + discussed)
TITLE re-read outro (ClaudeTitleOutro)
```

Acts are 4–8 beats each. Every act opens with a one-line segment card or a
spark-line beat naming the act (Title Case serif) — the viewer always knows
where they are in a 5–10 minute film.

## THE BEAT MIX — no quota (VOX LAW governs)

**The vox percentage is dead** (2026-09-02). It used to say ~20–25% of body
beats should be pantry stills, with a WARN outside 15–30%. That target produced
films that shopped for atmosphere to hit a number.

**`VOX LAW` in `../explainer/SKILL.md` replaces it:** a still is used when the
still IS the evidence — the actual record, the real document the narration makes
a claim about — and never as texture. A deep-explainer whose evidence is text,
code, or data correctly has **zero** vox beats. That is not a skipped pantry.

| Lane | When | What it is |
|---|---|---|
| **VOX** | the still is the evidence, and nothing else can be | A pantry still animated in the vox cutout grammar (below). `shot.type: STILL` or `COMPOSITE`, `shot.source: archive` or `ai`. |
| **MANIM** | there is an equation, a simulation, or a quantity that moves | Fragments from `animated_graphics.py`: isotype grids, state cards, quote cards, equation tangents. `shot.source: own`. |
| **REMOTION** | the idea has a shape — a comparison, a ledger, a structure | C2 rhetorical patterns, C3 concept illustrations, Onda `code-block` for anything code, segment cards. `shot.source: own`. |
| **CARD** | the act needs naming, or the film needs a breath | Act cards, kicker, sources card. |

What survives from the old lint: **more than 2 consecutive beats sharing a
visual scheme is a WARN** (except inside a vox run, where sameness is the
point). That check is about monotony and still earns its place. The percentages
do not — report the histogram at the plan gate as information, never as a gate.

**Rhythm.** Denser than the parent explainer's ~28-word vox rhythm, lighter
than a lecture: ~7–14 s per beat, narration ~25–45 words. A 5–10 min episode
lands around 30–50 beats. The parent's 45–70-word budget applies only to the
exempt bookend beats (the ask, the verdict recap, the handoff
read-and-discuss). Estimate at ~2.9 words/second for planning; the measured
audio is the only clock that counts.

## GATE L — library-first (ask the library before you author a beat)

Before a beat is authored, routed to Manim, slated, or written up as a request
card, ASK WHAT ALREADY EXISTS:

```bash
./art scenes "what the beat needs, in plain words"
./art scenes --check <ComponentName>     # is that name actually renderable?
```

The library is bigger than any session can hold in its head — which is exactly
how a reel ends up with beats slated while a purpose-built component sits unused
two directories away. A hit is a **LEAD**, not a verdict: read the desc and the
props before trusting it. A candidate tagged `[derived text — open the file]`
has no header of its own; the search text was assembled from file evidence.

A genuine miss is a **PUNT**, and a punt is a design card: build the component
and the next reel finds it forever. The search logs the miss to
`TEMPLATE-MISSES.md` by itself (`--reel <path>` records who needed it). **A miss
is never a licence to slate.**

After adding a component, run `./art scene-index` — a component that is not in
the index cannot be found by anyone, including you next week.

## PROOF GATE — beat-sheet authoring exit condition

Governs **authoring**, not rendering. Slates compile regardless (SLATE-RULE is
unaffected). The loop won't call a beat or a sheet "done" while it's punting.
Classification rules and the whole-sheet checklist live in
`skills/make/nopunt/SKILL.md` — the loop reads them there; this section does
not duplicate them.

**Per-beat exit condition.** A beat is DONE when it classifies as SHOW, HOLD,
or CARD (§ "SHOW / HOLD / CARD" in nopunt). If the narration makes a
factual/structural claim OR names a visual ("the routing diagram", "the wheel",
"the table"), the beat MUST be SHOW or a justified HOLD — never a bare CARD,
never a PUNT. Route every PUNT to its catalog row in nopunt before marking the
beat done. This applies to all lane types — VOX, MANIM, REMOTION, and CARD
beats all pass the same per-beat classification before the beat is closed.

**Legibility contract** on every SHOW/HOLD claim beat:
- Names its on-screen artifact in `shot.show` or `shot.visual_intent`.
- ~15–35% negative space.
- Un-highlighted elements never faded below ~40% opacity.
- Comparisons shown side-by-side, held ≥2s.

**Whole-sheet exit condition.** The sheet is DONE when (1) every beat
classifies SHOW, HOLD, or CARD with no unresolved PUNTs, and (2) the
teaching-arc checklist in nopunt (§ "Whole-sheet teaching-arc checklist")
passes — framework beat before examples, worked example, falsifiability beat,
scaffolded viewer task, four bookends, no-source-no-verdict rule.

**CHECKS-REPORT — write before the slate, not after.** Before Gate D1 (the
previz compile), write `CHECKS-REPORT.md` in the reel folder:

  N SHOW / N justified-HOLD / N PUNT-flagged
  Teaching arc: FRAMEWORK ✓/✗ | WORKED EXAMPLE ✓/✗ | FALSIFIABILITY ✓/✗
                SCAFFOLDED TASK ✓/✗ | BOOKENDS ✓/✗ | NO-SOURCE-NO-VERDICT ✓/✗

A PUNT-flagged beat or a failing arc item is a **violation**. The loop resolves
it or the author explicitly justifies it in `BUILD-LOG.md`. Neither is ever
silently passed.

## VOX BEATS — pantry stills, machine-animated

First apply [EXECUTABLE-EVIDENCE.md](../../../docs/EXECUTABLE-EVIDENCE.md).
Use pantry only when the artifact itself is needed. Run Python for a Python
result; compute data for a chart. A notebook/index-card photograph is not
necessary evidence for a constructed example or a locally runnable experiment.

A vox beat does not generate its own media. It **expects a static image** —
`pantry/[BID].png` → intake to `media/[BID].png` — and the compiler animates
it. That's the whole deal: the human supplies the plate, the machine supplies
the motion.

**Sourcing pantry stills — free first.** The default source is Smithsonian Open
Access (CC0, no rights escalation):

```bash
python3 runtime/scripts/smithsonian_fetch.py "<visual terms>" \
    --copy <reel> --beat <BID>
```

This resolves, downloads, optionally Topaz-upscales, and drops the image into
`pantry/<BID>-<slug>.png` with a provenance sidecar — ready for pantry intake.
Run `./art todo <reel>` to see which beats still need stills. Other free sources
(NASA, Wellcome, NLM) are available via `image_fetch.py --source smithsonian|nasa|wellcome|nlm_ihm`.
Higgsfield-generated stills are the opt-in upgrade (three-way contract in
`../explainer/SKILL.md`); absent CLI = Smithsonian/archive path silently.

**Treatment — the vox laundering function on the CLAUDE stage.** This is a
FIDELITY brand (parent law), so vox beats do NOT import the newsprint ground.
The treatment is: desaturate ~80%, contrast ~1.15, seated on the Claude cream
stage (`#F2F0E9`), subtle film-grain overlay (screen/overlay blend, low
opacity), warm-ink vignette. Terracotta `#D97757` remains the ONE accent —
a hand-drawn ring, an underline, a highlight bar. One editor's-pen voice per
beat. Serif labels with hairline underlines, per the parent design tokens.
The result must still read as the Claude brand wearing a documentary texture,
not as a Vox clone dropped into a Claude reel.

**Motion menu per vox beat** (`shot.motion`):

- `kenburns` — the workhorse. Ease-out bias (`Easing.out(Easing.cubic)` —
  documentary, not bouncy). Set `shot.focus: [fx, fy]` toward the sentence's
  subject.
- `cutout` — the transparent-background subject rises/settles onto the stage
  with a spring (pop-in, damped); background layer holds or drifts. Requires
  a cut-out PNG (alpha) in the pantry; the shopping list says so.
- `parallax` — 2–3 layers (background plate, midground subject, foreground
  detail) drifting at different rates. Requires the layers as separate pantry
  files (`[BID]-bg.png`, `[BID]-mid.png`, `[BID]-fg.png`).
- `drawon` / `annotate` — the still holds; the terracotta ring/underline/X
  draws on, keyed to the spoken word.
- `hold` — legal for a portrait kicker; never twice in a row.

Reveals land ON the spoken word (parent MOTION.md doctrine; word clock from
the align step). Constant velocity for documentary moves; easing only for
elements that feel like UI.

**Provenance.** Parent rules bind unchanged: `archive` slots need the
`.source.txt` sidecar (URL, license, credit → auto-credits); generated media
of real people gets `source: ai` + the disclosure sidecar. Real people/events
→ real archives first.

## CONTINUITY — the vox-run contract (and its deliberate limit)

The documentary "one continuous shot" feel is scoped to **vox runs only**: a
run is 2–3 consecutive vox beats authored as one camera move. Everywhere else
— any boundary where the lane changes (vox→Manim, Remotion→vox, etc.) — is a
hard cut. Never attempt frame-continuity across the whole episode: chaining
40+ beats through prose prompts is exactly the fragility this rule exists to
kill.

Inside a run, continuity is a **serialized contract, not narrative trust**.
The run's beats share a `vox_run` id, and each beat but the last carries a
`handoff` block that the next beat's first frame MUST reproduce:

```jsonc
"shot": {
  "type": "STILL", "source": "archive", "motion": "kenburns",
  "vox_run": "R2",                    // same id across the run's beats
  "handoff": {                        // this beat's LAST frame, serialized
    "camera": { "x": 0.62, "y": 0.40, "scale": 1.8 },   // 0–1 frame coords
    "objects": [
      { "id": "portrait-hume", "x": 0.5, "y": 0.45, "scale": 1.0, "opacity": 1 }
    ]
  }
}
```

Rules: the run's beats render as ONE composition internally (one camera
spline, beat boundaries = narration boundaries), OR as separate clips whose
first/last frames are pinned to the handoff values — either implementation is
legal, but the handoff block is authored at plan time either way, so the
continuity survives any re-render. A run never crosses an act boundary. Max
run length 3 beats. Runs are where the pantry earns drama: zoom out from the
detail (beat 1) to reveal the whole plate (beat 2), pan to the consequence
(beat 3).

## THE TWO HARD GATES (beyond the parents')

### Gate D1 — the slate previz IS the first deliverable

The first compile is always a **full-length watchable previz**: every vox
beat renders as a slate (beat id + narration line + terracotta pipeline
pointer), Manim/Remotion beats render for real (they're free), audio is real
(generated immediately after narration is authored). This is honest by design — at this genre's scale the pantry is
the bottleneck, and the previz is what the human reviews for pacing while
sourcing stills. Never present a previz as a finished cut.

### Gate D2 — the shopping list (duration-locked, tier-tagged)

`SHOPPING.md` is written **after audio lock** (never before — a card written
before the beat's real length is known can't state its duration requirement,
and conform is left stretching instead of trimming). One entry per missing
pantry asset. The review cut does not proceed while SHOPPING.md entries sit
unresolved without an explicit human "ship with slates" override.

Entry format and the sourcing tiers: `reference/shopping-list.md`.
The short version:

- **Tier 0 — the local library, FIRST.** Before an entry is written, search
  the toolkit's still stock (`svg/svg/images/`, ~1,500 PNGs, indexed in
  `svg/svg/icons.json`): `python3 runtime/scripts/pantry_search.py "<terms>"`.
  LOOK at the candidates; a real match is copied to `pantry/<BID>-<id>.png`
  (`--copy <reel> --beat <BID>`) and its SHOPPING.md entry is written
  pre-checked with the library id. No good match → the entry stands and the
  human searches. Tier 2/3 rights law still applies to whatever the still
  depicts — the library is a source, not a rights clear.
- **Tier 1 — generic/illustrative** (no real referent): AI-generate or stock;
  no rights escalation.
- **Tier 2 — specific real object** (named building, document, artifact):
  prefer the real image; verify THE ITEM's stated rights, not the hosting
  institution's reputation; AI fallback is labeled.
- **Tier 3 — specific named real person**: archival photo first (the
  PHOTOGRAPH's rights govern — photographer's term, not the subject's);
  the rights check itself escalates to the human, every time.
- Motion assets state their minimum duration and ask for MORE than needed —
  conform trims (lossless) rather than stretches (lossy).

## Workflow (each gate is the human's)

1. **`plan`** — read the WHOLE source; act structure → beats (~20–35 words),
   lane per beat (the mix contract), vox runs + handoff blocks, `show` blocks
   (SHOW-DON'T-TELL binds at authoring time), viz data, equation tangents
   marked. Present the lane histogram + the act map. **GATE: approve.**
2. **`factcheck`** — parent explainer Gate F, sharpened for this genre:
   long sources are where fabricated-but-fluent claims hide. Verify every
   number and named claim against the source; strip what will date the
   episode (tool names, versions, "as of [month]"); anything the source
   itself flags as unverified either dies or is presented AS unverified.
   `FACTCHECK.md` in the reel folder. **GATE: claims hold.**
3. **Audio** — generate_audio_kokoro.py (Kokoro, free, the default). Measured mp3s become the clock.
4. **Audio lock** — measured mp3s become the clock; align writes the word
   clock.
5. **Gate D2** — tier-0 library pass (`pantry_search.py` per vox still; copy
   real matches into `pantry/`), then write `SHOPPING.md` from the locked
   durations — matched entries pre-checked, the rest handed over.
6. **Gate D1 previz** — `./art run [reel]`: full compile, slates in vox
   slots, Manim/Remotion rendered, `--review` burn-in. **GATE: watch it.**
7. **Pantry fill** — human drops stills into `pantry/`; the parent pantry
   law (`pantry` command word) intakes, treats, renames; set `shot.focus`;
   fill sidecars. Rerun — only changed slots recompile.
8. **Review cut → VISUAL QC LAW pass → `./art final`.** The closing block is
   the `your-turn` standard. `BUILD-PROMPT.md` ships in the folder (parent
   rule: a reel without its build prompt is unfinished).

## Output contract

```
[book]/youtube/[slug]/
  beat_sheet.json      the heart (schema: runtime/schema/beat_sheet.schema.json
                       + vox_run/handoff + the lane annotations above)
  BUILD-PROMPT.md      paste-ready end-to-end build prompt
  BUILD-LOG.md         decisions, MISSING: lines, gate signatures
  FACTCHECK.md         claim | verdict | source | fix
  SHOPPING.md          Gate D2 manifest (after audio lock)
  SOURCES.md           source doc(s), corrections, seeds, credits
  pantry/  media/  manim/  clips/  mp3/   (parent slot contract)
```

Slug convention: `[channel]-[concept]` (default `claude-liam-…`), built into
the OWNING BOOK's `youtube/` — never into the toolkit.

## Hard rules (the genre's own — parents' rules all still bind)

1. **VOX is evidence, never texture** (`../explainer/SKILL.md` → VOX LAW).
   A still earns its beat only when it IS the claim — the actual record, the
   real document. Zero vox beats is a correct outcome for a film whose evidence
   is text. What separates this genre from `ai-explainer` is the ACT STRUCTURE
   and the 5–10 minute arc, not a pantry percentage.
2. **No whole-film continuity.** The vox-run contract is the ONLY
   frame-continuity mechanism. A plan that chains runs across act boundaries
   or beyond 3 beats fails the plan gate.
3. **SHOPPING.md only after audio lock.** A shopping list with estimated
   durations is a defect, not a head start.
4. **Strip the datable.** This genre's episodes are long-lived; vendor tool
   lists, model names, and "as of" claims from sources are compressed to
   generic mechanisms or cut (DOUBLE-CHECK LAW, sharpened).
5. **Unverified-source caution.** When the source doc itself mixes verified
   and fabricated material (research-pass output often does), FACTCHECK.md
   must mark which claims were independently checked — inheriting the
   source's own confidence is the exact failure mode this genre's episodes
   tend to be ABOUT.
6. **Never publish.** Master stays in the reel folder; public is a human
   Studio flip.
7. **GATE T (type-lock) — ALWAYS RUN**, like factcheck. After every compile,
   `scripts/type_check.py` runs per rendered frame and writes `TYPECHECK.md`
   (§8.1 min-size · §8.2 overflow · §8.3 contrast · §8.4 kerning / Pango catch ·
   §8.5 no-wordy-card · §8.6 golden strings). A FAIL blocks both `./art run`
   (wired after GATE V in `run.sh`) and `./art final` (wired as pre-flight in
   `art`). See `skills/make/kerning/SKILL.md` and `reference/type-spec.md`.

## Reference files (this folder)

- `reference/vox-beats.md` — the cutout grammar in implementation terms:
  easing, springs, grain, screen-blend keying, layer compositing; what's
  verified vs. what to re-check.
- `reference/shopping-list.md` — the Gate D2 manifest format + tier law.
- `reference/continuity.md` — the vox-run handoff contract, worked example.
