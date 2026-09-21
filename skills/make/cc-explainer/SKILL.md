---
name: cc-explainer
description: >
  Build a CC video — Liam, in for Bear, opens Claude Code and SHOWS what he is doing.
  The interface is the subject, so the body lives in the CC kit (CCSession,
  CCPromptBar, CCStatusVerb, CCToolCall, CCDiff, CCPlanCard, CCThemePicker,
  CCWebHome, CCPlainShell for outside-the-session shells); a card, diagram, or Manim fragment appears only when a concept
  cannot be shown in the terminal. The spine: a CC cold open, THE IDEA
  (BrutalistHesitantWriter typing what this film is about), a DEFINITIONS card
  (CCDefinitions — the jargon the film cannot avoid, one plain line each), the
  product's real loop (PROMPT → THINK → TOOLS → CHANGE → VERIFY), then — on
  films that BUILD something — THE BUILD, SHOWN (BFLOW: the flow and any other
  diagram the build needs; BSHOW: what the output actually looks like), then TWO
  closing-block beats before the recap — CONDUCT (the Boondoggle Score: who did
  what, with handoff conditions) and HUMAN (what the human MUST/SHOULD do, what
  the AI CAN/SHOULD do) — then the your-turn standard: VERDICT → YOUR TURN →
  the locked @NikBearBrown outro. Audience: smart people who use the chat
  window and may not know the technical words. Use when the user types `cc`, `cc-explainer`, `claude code video`,
  `show me in claude code`, or asks for a Claude Code 101 / walkthrough /
  terminal-first explainer. Register: Teardown. Liam (Kokoro `am_onyx`),
  "in for Bear", is at the keyboard AND owns the closing block — LIAM LAW,
  no other operator persona. Never publishes.
---

# cc-explainer — an expert opens the terminal and shows you

> Sibling of `ai-explainer` (cream composer, concept-illustrated middle) and
> `cli-explainer` (prompt → code → moving output). Same bookend chassis, same
> laws. What is different here: **the terminal is not a skin over the body —
> it IS the body.** A CC video reconstructs a real Claude Code session the way
> a shop video reconstructs a repair: the camera is over his shoulder, and the
> thing on the bench is the interface.

## Lineage — what governs when

- **Bookends, brand, laws** → `../ai-explainer/SKILL.md`: LOGO LAW, REBUILD
  LAW, FILL-THE-CANVAS, SHOW-DON'T-TELL, DOUBLE-CHECK, VISUAL QC, SPARK-LINE,
  HANDOFF, OUTRO, PIXEL-ART, DOODLE-BANNED, the channel roster.
- **The closing three** → `../your-turn/SKILL.md`: VERDICT
  (`ClaudeVerdictArtifact`) → YOUR TURN (`ClaudeComposerAsk`, greeting
  `Your turn.`, prompt read in full) → TITLE re-read (`ClaudeTitleOutro`).
  Liam owns all three. `OUTRO-LOCK.md` binds: exact title restate, hardcoded
  `@NikBearBrown`, slug-seeded mascot, no subline.
- **The interface kit and its editorial law** →
  `runtime/remotion/src/scenes/CC-TEMPLATES.md`. Read it whole. Product mode
  strings, keybindings, and status verbs are **verbatim** product strings
  (`tokens/claudecode.ts` → `VERBS`); never paraphrase them.
- **Library-first, proof gate, type-lock** → GATE L (`./art scenes`), the
  PROOF GATE and `CHECKS-REPORT.md` (`../nopunt/SKILL.md`), GATE T
  (`../kerning/SKILL.md`, `scripts/type_check.py`) — exactly as in
  `cli-explainer`. Not repeated here; they bind unchanged.
- **This file** governs: the operator persona, the TERMINAL-FIRST law, the
  session-fidelity laws, the beat spine, and the three closing-block beats
  with their doctrine and component contracts.

## The operator — who is at the keyboard

The body is narrated **in first person, present tense, by the person whose
session it is.** He is not explaining Claude Code; he is using it, and
saying what he is doing and why while he does it. "I'm going to put it in
plan mode before it touches anything, because I don't know this codebase yet"
— not "Plan mode lets users review changes before execution."

**LIAM LAW (Bear, 2026-09-08: "Liam persona ALWAYS. Liam in for Bear").**
The operator is **Liam, in for Bear** — on every cc-explainer, body and
closing block alike. There is no Ada, no second persona, no `--persona`
switch. The first reel (`cc-vibecoders-welcome`) was built with an "Ada"
operator and re-narrated the same day; do not repeat it.

| Field | Value | Notes |
|---|---|---|
| `metadata.operator.name` | `Liam` | Says "This is Liam, in for Bear" in the cold open. |
| `metadata.operator.voice` | Kokoro `am_onyx` | Free, local. The same voice carries the body and the closing block. |
| Closing block | Liam, `am_onyx` | your-turn's rule: the recap voice owns VERDICT, YOUR TURN, OUTRO. Handoff line into the recap: `Let's recap with Claude.` (no "Thanks, …" — there is nobody to thank). |

IN-FOR-BEAR LAW is satisfied twice — in the cold open and on the outro
("Liam, in for Bear"). Liam never imitates Bear and never claims to be him.

**Voice register.** Teardown — he names the design choice and what it cost:
"Claude picked `Explore` over reading the file directly. That's the right
call on a repo this size, and it's why the first answer took twelve seconds."
Forbidden phrases per `voices/teardown/VOICE.md`. He is allowed to be wrong
on camera and to say so — the VERIFY steps exist precisely so he can be.

## TERMINAL-FIRST LAW (this genre's ILLUSTRATE LAW, inverted)

In `ai-explainer`, the Claude UI must earn its beats and the default is an
illustration. Here it is the reverse. **The default surface for every body
beat is `CCSession`.** A beat leaves the terminal only when it can name the
concept the terminal cannot show — and it must name it, in
`shot.leaves_terminal_because`. Legal reasons:

- a **diagram** of structure the session only implies (the hook lifecycle,
  the context window filling, a subagent's separate context) → C2/C3 pattern
  or Manim fragment;
- a **quantity that moves** (tokens per turn, cost over a session) → Manim;
- a **concept card** for a term he just used and the viewer may not know
  (what a worktree is) → one card, ≤12 words, back to the terminal.

Two consecutive non-terminal beats is a build failure unless both name a
reason. A concept card that could have been a `CCSession` text block is a
punt.

## Session fidelity — the laws that make it a receipt

- **REAL-SESSION LAW.** Tool names, arguments, file paths, diff lines, and
  the plan card come from a session that **actually ran**. The reel is a
  reconstruction, not a dramatization. Keep the session transcript in the
  reel folder as `SESSION.md` (paste of the real run, trimmed) — it is the
  source every `CCSession` block is checked against. An invented tool result
  is a DOUBLE-CHECK LAW violation.
- **TYPES-NOT-NARRATES LAW.** A `prompt` block contains **what he typed**.
  It is never his narration. (Defect on record: the shipped
  `claude-liam-plan-mode-interruption` sheet pastes the voiceover into the
  prompt block — a session in which someone typed a paragraph of exposition
  at Claude. The narration says *why* he typed it; the block shows *what*.)
  A prompt block longer than ~2 lines is a smell; a prompt block that reads
  like a sentence about Claude Code is a bug.
- **VERBATIM-STRINGS LAW.** `accept edits on`, `plan mode on`,
  `shift+tab to cycle`, `esc to interrupt`, `ctrl+o to expand`, `◐ medium ·
  /effort`, and every status verb are product strings. The kit renders them;
  the sheet does not restyle them.
- **ONE LOOP PER CYCLE.** Each body cycle shows the product's actual loop —
  `PROMPT → THINK → TOOLS → CHANGE → VERIFY` — and the VERIFY step is **him
  running something**, not Claude saying it is done. Claude's ✓ is a claim.
  His command is the evidence. (This is where the film's skepticism lives.)
- **Clawd is punctuation.** `mascot: 'auto'` on `CCSession` follows the
  cued block; anything else is off. One mascot per shot, posed by what the
  session is doing. PIXEL-ART LAW binds.

## The spine (fixed)

```
B00  COLD OPEN     the terminal opens. CCSession, mode from the story.
                   CCPromptBar types the real ask; CCStatusVerb lands; the
                   first tool call returns. Liam says who he is and what he
                   is about to do. (CCWebHome is the alternative cold open
                   for a first-run / install / IDE episode.)
BIDEA THE IDEA     BrutalistHesitantWriter, CC palette (bg CC.PAGE, ink
                   CC.INK, accent CC.SPARK). The writer types what this film
                   is about in 2–4 short lines and corrects ONE word — the
                   misconception the film exists to fix. Liam says the idea
                   of the film in plain words over the typing. ≥ 12 s.
BDEFS DEFINITIONS  CCDefinitions — only if the film has critical jargon.
                   2–5 terms the viewer will hear or see, each defined in one
                   plain line at a high level. Liam reads them, no more.
                   Skip the beat (and say so in CHECKS-REPORT) if the film
                   has no jargon a chat-window user would trip on.
     ─── cycle 1 ───
     PROMPT        CCSession · prompt block (what he typed) + status verb
     THINK/TOOLS   CCSession · tool tree, live → done; he reads the tree
                   aloud and says what Claude chose to look at and why
     CHANGE        CCSession · diff block; he reads the diff, not the summary
     VERIFY        CCSession · HIS command (test, run, grep, git diff --stat),
                   its real output; the ✓ becomes evidence or doesn't
     [CONCEPT]     ≤1 non-terminal beat per cycle, only with a named reason
     ─── cycle 2 = the correction (16:9) ───
                   Something the verify step showed. He re-prompts. Same loop.
                   REVISION LAW from cli-explainer binds.
     ─── THE BUILD, SHOWN (build films only — BUILD-SHOW LAW, below) ───
     BFLOW         the flow of what was built, and any other diagram the
                   build needs to be understood (data flow, call sequence,
                   state, file layout). 1–3 beats. Library-first
                   (FlowDiagram / FlowDiagramClaude / PipelineFlow /
                   SkillTeardownPipeline / CCHarnessMap) or a Manim fragment.
     BSHOW         what the output LOOKS like — the real thing, running:
                   terminal output on CCPlainShell, a figure re-rendered by
                   the reel, a captured recording of the real page / app.
                   1–2 beats. Never a mock, never a description of output.
     ─── the two closing-block beats ───
     CONDUCT       the Boondoggle Score — see below
     HUMAN         the ledger: MUST/SHOULD human · CAN/SHOULD AI — see below
     ─── your-turn standard (beat ids are checked by GATE BOOKEND) ───
     BVDT          ClaudeVerdictArtifact, Liam; handoff line first
     BHTF          ClaudeComposerAsk, greeting "Your turn.", topic carries
                   "YOUR TURN", prompt read aloud
     BOUT          ClaudeTitleOutro — OUTRO-LOCK; props carry
                   handle "@NikBearBrown" and subline "" (the gate reads them
                   from the sheet even though the component hardcodes them)
```

**Retired (Bear, 2026-09-08):** the SKEPTIC beat (`CCSkepticAudit`, the four
moves Descartes / Hume / Popper / Plato). "Hume, Plato etc is just confusing."
The component stays in the kit; no cc-explainer uses it. The skepticism is not
gone — it lives in every VERIFY step (his command, not Claude's ✓) and in the
verdict's falsifiable line.

**GATE BOOKEND.** `runtime/scripts/bookend_check.py` enforces the four
bookends. It knows this skill: with `metadata.skill: "cc-explainer"` the cold
open may be a CC surface (`CCSession`, `CCWebHome`, `CCShell`,
`CCPromptBar`). The recap / your-turn / outro rules are unchanged — use the
ids above or the gate blocks the run. Set `metadata.skill` or the override
does not arm.

A 16:9 CC video missing THE IDEA, a VERIFY step in every cycle, a correction
cycle, or either closing-block beat is not done; a build film (`metadata.build`)
missing BFLOW or BSHOW is not done. Duration is an
output (`../duration-planner/`); the loop plus the three beats lands most
episodes at 4–8 minutes. Shorts (9:16) ship one cycle and drop CONDUCT, keeping
HUMAN compressed to one beat; THE IDEA and DEFINITIONS stay.

## THE BUILD, SHOWN — BFLOW and BSHOW (build films only)

**BUILD-SHOW LAW (Bear, 2026-09-09: "when used to show how to build something
with Claude Code it should show any relevant flow and other diagrams and what
the output looks like right before the Boondoggle score beat").** A cc-explainer
whose ask is *build / make / wire up / ship X* — the cli-scout BUILD lane, any
film where the loop ends with a thing that runs — carries two slots between the
last correction cycle and CONDUCT. The Boondoggle Score then scores a build the
viewer has just SEEN, not one they were told about.

**Arming.** Set `metadata.build: true` (the author script asserts it when the
ask verb is build-shaped). Concept films — the Claude Code 101 tiers that
explain a feature rather than build with it — leave it unset and skip both
slots; say so in `CHECKS-REPORT.md` ("BUILD-SHOW: not armed — concept film").
A build film that skips them is not done.

### BFLOW — the flow, and the other diagrams (1–3 beats)

What the session only implied, drawn: how the thing that was built fits
together and what moves through it. Pick the diagrams the BUILD needs, in
this order of preference, and stop when the viewer can predict the output:

| Need | Draw | Library lead (GATE L first) |
|---|---|---|
| the pipeline / request path / what calls what | flow diagram, boxes and arrows, the build's real names on the boxes | `FlowDiagram`, `FlowDiagramClaude` (nodes/edges), `PipelineFlow`, `SkillTeardownPipeline` |
| where it sits in Claude Code (hook, skill, MCP server, subagent) | the harness map with the built piece lit | `CCHarnessMap` |
| a quantity the build changes (tokens, latency, rows) | Manim bars / counter | reel-local `scenes.py` |
| the files it created or touched | file tree, rows landing on the spoken names | `CoworkFolderTree`, `CCPlanCard` (≤7 rows) |
| a state machine or sequence | Manim fragment | reel-local |

Rules: every node label is a name from `SESSION.md` (REAL-SESSION LAW —
no invented modules); one accent per beat; the diagram BUILDS in narration
order (a still frame must not carry it — MOTION test); each beat names
`shot.leaves_terminal_because` = "BFLOW: <what the terminal could not show>".
Two BFLOW beats are the norm; three is the ceiling.

### BSHOW — what the output looks like (1–2 beats)

The built thing, doing its job, on screen. This is the receipt for the whole
film, and it is subject to REBUILD LAW and DOUBLE-CHECK LAW like everything
else — so the surface is chosen by what the output IS:

| The output is… | Show it as | Provenance |
|---|---|---|
| terminal / log / test output | `CCPlainShell` (`$ ` command, real lines, `# ` comments) or a `CCSession` VERIFY-style block | the lines are in `SESSION.md` |
| a file (config, CLAUDE.md, JSON, CSV) | `CoworkMarkdownFile` / `CCDiff` on the real file, scrolled to the part that matters | the file is in the reel folder |
| a figure, chart, plot the build produced | re-rendered by the reel from the build's own data (Manim / Remotion) — never a screenshot of the plot | data file in the reel folder, cited in FACTCHECK |
| a web page, app, dashboard, game | a **captured recording of the real thing running** (the `viz-riff` capture precedent): `clips/BSHOW.mp4`, `shot.source: "own"`, `media/BSHOW.source.txt` naming the command that launched it and the capture date | the capture is the evidence; a mock-up of the page is a PUNT |
| a generated artifact (image, audio, video) | the artifact itself, held, with its generation command shown first | disclosure sidecar if AI-generated |

Rules: Liam's narration on BSHOW is *what to look at*, not *what it does*
("there — the third row is the one the hook rejected"); the launch command
appears before the output (ASK→RESULT LAW, inverted for output); the beat
holds long enough to read (≥ 6 s on a page capture); Clawd `off`. If the
output cannot be shown honestly — it needs credentials, it is not
deterministic, it did not actually run — the film says so on screen
(`CCPlainShell` with the error, and the CONDUCT beat scores that step
`[IJ]`) rather than showing a stand-in.

**Why here, not earlier.** The VERIFY steps inside the cycles show single
commands proving single claims. BFLOW/BSHOW step back: the whole build,
drawn, then running. CONDUCT immediately after scores who built it; HUMAN
says which of that was the human's. The order is the argument.

## THE IDEA and DEFINITIONS (the two beats before the loop)

### BIDEA — THE IDEA (`BrutalistHesitantWriter`)

Beat two, always. The writer types the idea of the film — the sentence a
smart chat-window user would say back to a friend — and corrects one word.
Author it per reel:

- `text` — 2–4 short lines (`\n` breaks), ending on the film's real claim.
- `triggerWords` / `replacementWords` — ONE word, the misconception the film
  fixes ("better" → "different": Claude Code is not a better model). Never a
  random word; the correction is the pedagogy.
- Palette — CC, not the component's cream defaults: `bg` `#1F1E1B`, `ink`
  `#F2F0E9`, `accent` `#D97757`; `face` serif; `fontSize` ~78; `seed` = slug.
- Pace — the component's defaults (`charMs` 50, `hesitateBetween` 20) type
  four lines in ~25 s and get cut mid-sentence by a 15–19 s narration. Use
  `charMs` 22, `hesitateBetween` 6, `hesitateWithin` 1, `mistakeRate` 5,
  `jitter` 20: four lines land in ~15 s (measured). Keep the text ≤ 4 lines,
  ≤ ~150 characters.
- Narration — Liam says what the film is about, in plain words, over the
  typing. No jargon here; that is the next beat's job.

### BDEFS — DEFINITIONS (`CCDefinitions`)

Only when the film has critical jargon. The audience is smart people who use
the web interface and may be unclear on the technical words: define each at a
high level, one plain line, no lecture. 2–5 terms, in the order the film uses
them. Liam reads each line once.

```ts
// CCDefinitions
{ title?: string,                      // default 'TERMS IN THIS FILM'
  terms: [{ term: string,              // ≤ 18 chars, as written on screen
            meaning: string }],        // ≤ ~70 chars, wraps to two lines max
  startCue?: number, rowGap?: number } // rows land one at a time
```

## The two closing-block beats

These turn the film on its own session: who actually did what, and which of
that work was the human's to do. Doctrine is distilled in
`reference/three-beats.md` (its SKEPTIC section is retired); the beat
contracts are here.

### CONDUCT — the Boondoggle Score (`info-7375-conducting-ai`, Gru)

Programming as conducting. He scores the session he just ran: each step,
who did it, which supervisory capacity the human exercised, and the handoff
condition between steps — the thing that had to be true before the next
step was allowed to begin.

| Label | Capacity | What it looked like in this session |
|---|---|---|
| `[PF]` | Problem Formulation | the one-sentence ask he wrote before Claude saw anything |
| `[TO]` | Tool Orchestration | plan mode first; the subagent for the search; `--effort` |
| `[PA]` | Plausibility Auditing | he read the diff and heard the wrong note before running it |
| `[IJ]` | Interpretive Judgment | he decided the passing test was testing the wrong thing |
| `[EI]` | Executive Integration | he held the two threads (the fix and the migration) to one goal |

Component: `CCBoondoggleScore` (contract below): a two-column score —
MINION PART (Claude's steps, with the prompt that drove each) and GRU PART
(his steps, capacity-labelled) — populating in dependency order, each Claude
step followed by its **handoff condition** in the Gru voice ("not 'looks
good' — every foreign key references a documented entity"). The narration
names the **dangerous middle** explicitly: the step where Claude produced
something plausible from an incomplete spec and only his audit stood between
it and the codebase. If a capacity appears zero times, he says so — a
session with no `[PA]` is a session that assumed Claude was right.

### HUMAN — the ledger (`info-7375-irreducibly-human`, Tier 4)

Two columns, filled from the session, not from principle:

```
THE HUMAN                              THE AI
MUST    decide what "done" means       CAN     generate the scaffold from a spec
        sign the diff                  CAN     draft the tests from the criteria
        catch the confident error      CAN     find every call site in 4 s
SHOULD  read the tree before the diff  SHOULD  run in plan mode on a new repo
        write the failure case first   SHOULD  hand back a plan, not a change
```

The Tier 4 frame governs the narration: the machine cannot reliably report
its own uncertainty, so the metacognitive burden — how sure should I be, in
this domain, about this output — is the human's and cannot be lent. The
verdict is **supervise**, not "don't use". Verification is not the leftover
work; it is the part with consequence in it, and it is the part that does not
speed up when the solver does. He ends the beat on one sentence about what
he would not delegate next time, and why.

Component: `CCHumanLedger` (contract below). MUST rows are terracotta-ruled;
SHOULD rows are ink; the AI column fills first, the human column lands
second and holds — the order is the argument.

## Component contracts (built; kept for reference)

`./art scenes` finds no purpose-built scene for any of the three. The
nearest hits, checked by rendering: `BrandBoondoggleScore` hardcodes its
steps and takes only a `score` number — a demo, not a component;
`MedhavyTwoColumnCard` has the right prop shape for the ledger
(`leftHeader/leftItems/rightHeader/rightItems`) but renders a small cream
Medhavy card at ~25% fill — a **layout lead** for `CCHumanLedger`, not an
interim. **Until these exist, all three beats render on
`ClaudeVerdictArtifact`** with the line formats below, and `BUILD-LOG.md`
records the interim.

Kit gotchas found while validating the reference sheet (both bite silently):
`CCSession` `text` blocks occupy **one row each** — a long line does not
truncate, it **wraps and overprints the blocks beneath it** (seen on
`cc-vibecoders-welcome` B05: a 130-character sentence printed over the two
`Write` calls that followed). Keep every text block under **~44 characters** at
the kit's type size (measured: a 45th character wraps) and split Claude's sentences at clause boundaries, one
block per line, wording untouched; newlines inside a block also collapse.
`CCHumanLedger` rows **ellipsize past ~30 characters** (proportional type: measured, "say 'unverified' instead of guessing" fits at 36 while "run the commands, quote the outputs" clips at 35) (two columns at the kit's
40px type) — write every MUST/SHOULD/CAN row to fit; `CCBoondoggleScore`'s
`system` header wraps past ~28 characters. A body beat that runs a command the
session's fence blocked, or a shell loop around several sessions, renders on
**`CCPlainShell`** (a dark plain terminal, no Claude chrome, `$ ` commands and
`# ` comments) — never on `BrutalistAdaptCLI` (cream page, a hardcoded
"adapt this template" title, type under the GATE T floor; failed §8.1 on
`cc-five-claudes-explained` B03). The one diagram a cc-explainer leaves the
terminal for is **`CCHarnessMap`** (model → prompt → context → harness → your
loop, rings landing inside out) — built for `cc-agentic-harness`.
**Never edit `beat_sheet.json` while `art run` is alive** — the run writes its
build stamps back from its own in-memory copy at the end and silently reverts
any prop edit made meanwhile (`cc-agentic-harness` pass 2: a chip fix vanished
and the beat rendered clipped). To re-render one beat: with no run alive, set
its `shot.remotion.rendered` to `{"out":"","at":""}`, drop `build`, delete
`media/<id>.mp4`, then run. And when stopping a run, kill `run.sh` /
`remotion_scenes.py` / `ffmpeg` for that reel (`pkill -f <slug>`), not just the
`art` wrapper — a survivor holds `.render.lock` and keeps rendering.
`ClaudeVerdictArtifact` (BVDT) paginates its lines two per page; give it **4 or 6
lines**, never 5 — a one-line last page reads as low-contrast to Gate V's 85 %
sample (`cc-claude-md-length`).
`CCSession` status blocks and `CCStatusVerb` **prepend the `↓` themselves** — write
`tokens: "1.2k tokens"`, never `"↓ 1.2k tokens"`, or the line renders `↓ ↓`
(shipped that way on the first three films).
`CCPlanCard` **clips** past about seven rows under the footer band (GATE T
§8.13 catches it) — the plan card is a summary, keep it to what fits.
`mascot: 'auto'` on a beat whose block stack reaches the bottom of the shell
puts Clawd **on top of the last rows** (B04's diff): set `mascot: 'off'` on
any full-height beat. Register the real ones in `Root.tsx`
under the `CC` folder and re-run `./art scene-index`.

```ts
// CCSkepticAudit — RETIRED 2026-09-08; kept in the kit, unused by this skill
{ claim: string,                       // Claude's completion line, verbatim
  moves: [{ name: 'Descartes'|'Hume'|'Popper'|'Plato',
            question: string,          // ≤ 12 words, what he asks aloud
            command: string,           // what he runs
            result: 'pass'|'fail'|'pending',
            cue: number }],            // frame the stamp lands
  verdict?: string }                   // ≤ 12 words, lands last

// CCBoondoggleScore — the CONDUCT beat
{ system: string,
  steps: [{ n: number, phase: 'F'|'C'|'I'|'B'|'H'|'R',
            labor: 'claude'|'human',
            text: string,              // the prompt (claude) or the action (human)
            capacity?: 'PA'|'PF'|'TO'|'IJ'|'EI',   // human steps only
            handoff?: string,          // claude steps only; testable, ≤ 20 words
            dependsOn?: number[] }],
  dangerousMiddle?: number,            // step n to ring in terracotta
  distribution?: boolean }             // show the capacity tally at the end

// CCHumanLedger — the HUMAN beat
{ human: [{ tier: 'MUST'|'SHOULD', text: string }],
  ai:    [{ tier: 'CAN'|'SHOULD',  text: string }],
  closing?: string }                   // ≤ 14 words; what he would not delegate

// Interim on ClaudeVerdictArtifact — one line per row, prefix carries the semantics:
//   CONDUCT:  "3 · CLAUDE · draft migration → handoff: every FK names a documented entity"
//             "4 · HUMAN [PA] · read the diff; caught the dropped index"
//   HUMAN:    "MUST — decide what done means"   "AI CAN — find every call site"
```

## Workflow

1. **Run the session.** For real. Save the transcript to `SESSION.md`. The
   reel cannot be authored from imagination — REAL-SESSION LAW.
2. **`plan`** — from `SESSION.md`, cut the loop into cycles; one `CCSession`
   beat per loop step; mark the correction; write THE IDEA's lines and its one corrected word; list the jargon the
   film cannot avoid for DEFINITIONS; on a build film, list the BFLOW
   diagrams (from the session's real names) and decide the BSHOW surface from
   what the output IS — and capture the output NOW, while the build still
   runs (`clips/BSHOW.mp4` + sidecar); draft CONDUCT and HUMAN from what
   actually happened (the CONDUCT steps are the real prompts; the HUMAN
   ledger names what he did). GATE L per beat. Present the spine. **GATE: approve.**
3. **`factcheck`** — every tool name, path, diff line and output in the sheet
   is in `SESSION.md`; every product string is verbatim; nothing datable
   (model names, version numbers, "as of"). `FACTCHECK.md`.
4. **Audio** — Liam (`am_onyx`) for every beat, body and closing three
   (`generate_audio_kokoro.py` honours per-beat `voice`). Measured mp3s are
   the clock.
5. **`CHECKS-REPORT.md`** before the first compile — SHOW/HOLD/CARD, the
   teaching arc (the VERDICT's falsifiable line is the falsifiability beat; the HUMAN beat
   is the scaffolded-task setup for YOUR TURN).
6. **`./art run`** → Gate V → GATE T → read frames → **`./art final`**.
   `BUILD-PROMPT.md` ships in the folder.

## Output contract

```
[book]/youtube/[slug]/
  SESSION.md          the real transcript this reel reconstructs — the source
  beat_sheet.json     spine above; body beats carry shot.remotion.pattern = CCSession
                      and, off-terminal, shot.leaves_terminal_because
  FACTCHECK.md  CHECKS-REPORT.md  BUILD-LOG.md  BUILD-PROMPT.md  SOURCES.md
  mp3/  media/  mp4/
  clips/BSHOW.mp4 + media/BSHOW.source.txt     build films: the captured output
```

Slug convention `cc-[concept]`; `metadata.skill` must be `cc-explainer` (e.g. `cc-init-your-first-claude-md`). Builds
into the OWNING BOOK's `youtube/` — for the 101 series that is
`anthropics/claude-code-101/` per its `INDEX.md` tiers.

## Hard rules (this genre's own — parents' rules all still bind)

1. **TERMINAL-FIRST.** Body beats default to `CCSession`; leaving the terminal
   requires a named reason; two consecutive unreasoned card beats fail.
2. **REAL-SESSION.** Every block traces to `SESSION.md`. No invented output.
3. **TYPES-NOT-NARRATES.** Prompt blocks are what he typed, never what he
   said.
4. **VERIFY IS A COMMAND.** Every cycle ends with him running something.
   Claude's ✓ is a claim; his output is the evidence.
5. **IDEA, DEFINITIONS, THEN THE LOOP; CONDUCT AND HUMAN BEFORE THE RECAP.**
   THE IDEA is beat two on every film; DEFINITIONS follows when there is
   jargon; CONDUCT and HUMAN close the body, each grounded in this session,
   each with its source book named in `SOURCES.md`.
6. **VERBATIM PRODUCT STRINGS.** Modes, keybindings, verbs from the kit and
   its tokens. Never restyled, never paraphrased.
7. **OUTRO-LOCK.** `ClaudeTitleOutro`, `@NikBearBrown`, exact title, no
   subline. Liam re-reads the title then says "At Nik Bear Brown"; no jingle,
   no music on the card.
8. **BUILD-SHOW.** On a build film (`metadata.build: true`), BFLOW (the flow
   and any other diagram the build needs, real names only) and BSHOW (the
   output, real and running, never a mock) sit immediately before CONDUCT.
   Concept films skip both and say so in CHECKS-REPORT.
9. **Never publish.** Master stays in the reel folder; TOPOST via `post`.

## Port note

The CC kit (`CC*` scenes, `tokens/claudecode.ts`) exists in **this tree
only**. The public cut `brutalist.art` carries `ClaudeCodeBeat` and
`ShellSession` and none of the kit; this skill cannot run there until it is
ported. Recorded in `PORT-LOG.md` when it is.

## Reference files (this folder)

- `reference/three-beats.md` — the doctrine behind CONDUCT / HUMAN (SKEPTIC retired),
  distilled from the three courses with chapter pointers; its BUILD-SHOWN note
  says why the score follows the shown build.
- `reference/example-cc-beat_sheet.json` — a worked spine for the first
  missing 101 episode, `/init` and your first CLAUDE.md, with real
  `CCSession` block shapes.
