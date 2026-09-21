---
name: cli-explainer
description: >
  Build a CLI video — a Teardown-voice reel that shows an AI-CLI session and
  shows the OUTPUT as a moving vox-explainer beat: a Manim / Remotion / d3
  animation, or a slate you fill later. Defaults: Liam persona (claude-liam,
  Kokoro am_onyx, free) and the CLAUDE skin (cream composer, warm ink,
  terracotta spark — ClaudeComposerAsk for prompts, ClaudeCodeBeat for code);
  the tool flag swaps the interface skin (claude, onda, codex) and the persona
  flag swaps the voice (liam, bear). The ask drives the story; the output is
  always motion, never a still. The reel reconstructs how the artifact was
  BUILT with the tool: show the prompt, show the ACTUAL code, show the output.
  Use when the user types cli, cli-explainer, or claude-cli followed by a
  concept, chapter, or idea, or asks for a CLI video or Claude-build video
  (legacy names: terminal-screencast, Onda video). Register: Teardown
  (NikBearBrown). Output: beat_sheet.json for vox_run.sh.
---

# cli-explainer — the CLI-video style (composer in, animated output out)

## Evidence and mathematical notation

Read [EXECUTABLE-EVIDENCE.md](../../../docs/EXECUTABLE-EVIDENCE.md) before
authoring code/output beats and [MATH-TYPESETTING.md](../../../docs/MATH-TYPESETTING.md)
for equations. Run the source and preserve its actual outputs; plausible-looking
terminal text is not an execution receipt. A teaching reconstruction must be
labeled, and an excerpt must not change the result. Do not request pantry
photographs of code, tests, tables or flow diagrams that can be generated locally.
Show what the code does, not code card after code card. Typeset explanatory
math structurally; literal source code stays literal code.

> Renamed from `terminal-screencast` (which was itself the renamed `cli`
> skill). The old names — `terminal-screencast`, "Onda video" — still resolve
> to this skill; `cli` and `claude-cli` remain the trigger words.

## The shared skeleton (claude-explainer AND claude-cli are siblings)

Both skills produce the SAME Claude-branded bookends; only the MIDDLE differs.

1. **Beat 1 — the Claude terminal, `[Hello], [Name]`** (`ClaudeComposerAsk`:
   world-language hello + persona). Always beat 0.
2. **Middle — the ONLY part that differs:**
   - **claude-explainer** → a **vox-style explainer**: any media that fits the
     concept (archival, isotype, Manim, illustrations — and terminals/code where
     they earn the beat). The bookends frame it; the middle teaches.
   - **claude-cli** → the **build-with-Claude loop**, each step discussed: CLI
     prompt (Claude template) + *why this prompt* → show code + discuss → show
     output + discuss; at least one revision.
3. **Second-to-last — "Your Turn"**: the composer with a suggested prompt typed in
   for the viewer to explore (`greeting: "Your turn."`).
4. **Last — the channel brand card**: `@NikBearBrown` / `@Medhavy` / `@Musinique`
   … (title restate + channel handle).

**Scout → builder routing (the idea's SOURCE picks the skill):**
- `cli-ideas.md` (cli-scout) and `simulation-ideas.md` (sim-scout) cards → **claude-cli**
- video-idea cards (`vids/` scouts, `media-scout` video cards) → **claude-explainer**

Both are audio-first, phase-gated, fill-in-first, and
output `[slug].mp4` + `[slug]-slate.mp4`. See `docs/how-to-create-a-claude-explainer.md`.


A **CLI video** shows two things in alternation: **a simulated Claude session**
(the Claude skin — someone typing a prompt into the composer and reading what it
makes) and **what the prompt produced** (an output beat — a *moving*
visualization). Two differences from the `simulation` aspect: the output is not
Manim-only (it is any animation or a slate), and every CLI video carries a
**fixed narrative spine** so it teaches, not just demonstrates.

The core logic is unchanged from the terminal days: **show prompt → show code →
show output**. What changed is the skin: the reel reconstructs how you'd build
the artifact *with Claude*, so the input beats wear the Claude look
(`tokens/claude.ts` — cream `#FAF9F5`, warm ink `#3D3929`, one terracotta
`#D97757` accent) by default; `--tool onda` uses the generic dark terminal
skin instead (see Skins, below).

`vox_compile.py` already resolves an output slot by precedence
`media/[BID].mp4 > manim/[BID].(mp4|mov) > media/[BID].png > slate` — so the output
beat plays whatever motion you drop in, and un-filled beats ship as labeled slates.

## Trigger
`cli [concept | chapter | idea] [--tool claude|onda|codex] [--persona liam|bear] [--out [dir]]`
Aliases: `cli-explainer […]` · `claude-cli […]`. Also: "make a CLI video",
"Claude-build video of X", "show the prompt then the output". (Legacy names —
`terminal-screencast`, "Onda video" — still mean this skill.)

**`--tool` picks the interface skin. Default is `claude`.** Plain `cli`,
`cli-explainer`, and `claude-cli` all produce the Claude look; `--tool onda`
gives the generic dark terminal; `--tool codex` gives the Codex interface
(real components — see Skins); `--tool github` gives the GitHub dark skin
(diegetic subject surface — repo hero, section rail, code viewer, diff, and four
evidence patterns); `--tool shell` gives the dark macOS terminal skin (prompt →
command → output, terracotta sigil). New CLI tools slot in here as one more skin.

**`--persona` picks the voice. Default is `liam`.** `liam` = the claude-liam
channel (Liam in for Bear, Kokoro `am_onyx`, free — IN-FOR-BEAR LAW applies);
`--persona bear` = Bear's Kokoro am_onyx voice, same as the default channel.
The persona also names the `[Hello], [Name]` greeting in B00.
New personas slot in as channel voices the same way new tools slot in as skins.

## The required beat spine (EVERY CLI video — not optional)
```
B00  INTRO        cold open on the interface (ClaudeComposerAsk by default;
                  the --tool skin's composer otherwise — ask lands answered; COLD
                  OPEN LAW, per claude-explainer).
     PROBLEM      what is the problem, why are we solving it, the context, why the
                  viewer should care — the stakes, stated BEFORE the build begins.
                  No prompt yet: this is the "why" that earns the build.
     ─── cycle 1 ───
     CLI          the prompt typed into the CLI — SHOW AND DISCUSS the prompt.
     CODE         the generated code — the CRITICAL OUTPUT of the prompt; SHOW
                  AND DISCUSS it (ClaudeCodeBeat). Required every cycle.
     OUTPUT       the run's result — a MOVING visualization (Manim/Remotion/d3),
                  a screen capture, or a slate.
     ─── cycle 2 = the revision (16:9 only) ───
     CLI          check the output, type the REVISED prompt (runningText
                  "updating…") — show and discuss what changed.
     CODE         the revised code — show and discuss the diff that matters.
     OUTPUT       the BETTER output — the change made visible.
                  (more cycles if the story needs them; see THE REVISION LAW.)
     ─── close ───
     SUMMARY      what we built and what the output showed — the lesson, in one beat.
     NEXT STEPS   HANDOFF — ClaudeComposerAsk with a suggested prompt typed in,
                  greeting "Your turn." (HANDOFF LAW, per claude-explainer).
     OUTRO        title-restate outro (Remotion: ClaudeTitleOutro — poster serif,
                  terracotta period, handle beneath; CodexTitleOutro under
                  --tool codex) — the LAST beat.
```
Mandatory in the 16:9 cut: (1) the **PROBLEM** beat after the intro and before
the CLI loop; (2) **at least one revision** — a second CLI → CODE → better
OUTPUT cycle; (3) the **SUMMARY** and **NEXT STEPS** beats before the outro. A
16:9 CLI video missing any of these is not done.

**THE REVISION LAW.** The 16:9 video ALWAYS contains at least one revision
cycle (CLI → CODE → better OUTPUT) — a CLI video without a check-and-change is
incomplete. The ONE exception is the 9:16 / Shorts cut: to fit the 3:00 cap it
ships a SINGLE cycle — CLI → CODE → OUTPUT, no revision — and points the viewer
to the 16:9 for the complete example. Revision is a 16:9 requirement, not a
9:16 one.

The through-line is *problem → build → run → check → change → what it means → what's
next* — Teardown-voiced and output-agnostic.

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
beat done. For CLI videos: every OUTPUT beat is SHOW by definition (the beat
spine already requires motion, never a still) — a static or unclassified output
slot is automatically a PUNT.

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

**CHECKS-REPORT — write before the slate, not after.** Before the first slate
compiles, write `CHECKS-REPORT.md` in the reel folder:

  N SHOW / N justified-HOLD / N PUNT-flagged
  Teaching arc: FRAMEWORK ✓/✗ | WORKED EXAMPLE ✓/✗ | FALSIFIABILITY ✓/✗
                SCAFFOLDED TASK ✓/✗ | BOOKENDS ✓/✗ | NO-SOURCE-NO-VERDICT ✓/✗

A PUNT-flagged beat or a failing arc item is a **violation**. The loop resolves
it or the author explicitly justifies it in `BUILD-LOG.md`. Neither is ever
silently passed.

## Input beats — the Claude Remotion template
Reuse the Claude fidelity scenes (`runtime/remotion/src/scenes/`, tokens in
`runtime/remotion/src/tokens/claude.ts` — a FIDELITY palette: never retint):
- **INTRO** → `ClaudeComposerAsk` · cold open, ask shown answered · props:
  `command`, `topic`, `segment`, `greeting` (`[hello], [persona]` — world-language
  hello, rotate per reel), `runningText`, `output` (result lines).
- **ASK** → `ClaudeComposerAsk` · props: `command` (the actual generation prompt),
  `topic`, `segment`, `runningText` matching the action (`building the sim…`,
  `rendering Manim…`). Same prop contract as the legacy TerminalAsk — old beat
  sheets convert by renaming the scene.
- **CODE** → `ClaudeCodeBeat` · props: `title` (filename), `code`, `sparkLine`
  (≤4-word serif compression of the beat's point).
- **CHANGE** → `ClaudeComposerAsk` with the revision prompt + `runningText: "updating…"`.
  **SPARK-LINE LAW:** every inner composer beat carries a spark line (its
  `greeting`) — never a lonely asterisk. ASK = `"The ask,"`, CHANGE = `"The change,"`
  (or `"The revision,"`). Only B00 (the hello) and the handoff (`"Your turn."`) get
  their own greetings; an empty greeting on any other composer beat is a bug.
- **NEXT STEPS / HANDOFF** → `ClaudeComposerAsk` with `greeting: "Your turn."`,
  `runningText: "paste this into Claude…"`, `command` = the suggested prompt.
- **OUTRO** → `ClaudeTitleOutro` · prop: `title` (exact episode title), `slug` (reel folder name, seeds mascot + polarity).
  **@NikBearBrown outro card is locked** — exact title restate, hardcoded `@NikBearBrown` handle, one of the 18 crisp-safe mascots (slug-seeded), NO subline; spoken not scored (Liam: title, then "At Nik Bear Brown"; no jingle); claude-liam reels only. See `OUTRO-LOCK.md`.

**THE ACTUAL-CODE LAW.** The CODE beat shows the REAL source of the artifact —
the sim's own JS, the generated `scenes.py`, the script that actually ran —
trimmed to the lines that teach (the physics, the mapping, the one denominator
that matters), never pseudocode, never prose restyled as code. The reel is a
reconstruction of how the artifact was built with Claude: the ASK prompt must
plausibly generate the code shown, and the code shown must plausibly produce
the OUTPUT beat. Prompt → code → output is one receipt, in the Claude look.

**Skins — chosen by `--tool` (default `claude`).** The body logic and the
bookends above are IDENTICAL for every tool; they differ only in the interface
skin of the input beats:
- **`claude`** (DEFAULT — plain `cli` and `claude-cli` both use it) → the CLAUDE
  interface: `ClaudeComposerAsk` / `ClaudeCodeBeat`, Claude fidelity palette
  (cream `#FAF9F5`, ink `#3D3929`, one terracotta `#D97757`).
- **`onda`** → the GENERIC dark terminal skin: `NikBearBrownTerminalAsk` /
  `NikBearBrownCodeBlock` (the darker Onda/terminal look). Same props, same
  spine, same bookends.
- **`codex`** → the CODEX interface — REAL, not reserved. Written by Codex
  itself; registered in Remotion Studio under `Codex-Templates`:
  `CodexComposerAsk` (task + typing + execution checklist), `CodexCodeBeat`
  (code + verification command + status), `CodexTitleOutro` (end card), plus
  `CodexWindow` (task report / diff surface) and `CodexCallout` (annotated
  frame for Teardown judgments). Tokens: `tokens/codex.ts` — a FIDELITY
  palette like Claude's: never retint. Editorial law in
  `runtime/remotion/src/scenes/CODEX-TEMPLATES.md`: the Codex loop is
  TASK → INSPECT → CHANGE → VERIFY → REPORT, and when two products appear in
  one script, name the owner of every interface judgment.
- **`github`** → the GITHUB dark skin — diegetic subject surface (a cutaway to
  a real GitHub page). Tokens: `tokens/github.ts` (bg `#010409`, panel
  `#0d1117`, blue accent `#2f81f7`). Interface components:
  - `GitHubRepoHero({name, kind, headline, starLabel, repo, handle, tagline})` —
    hero frame: octo mark + pill + headline + star widget.
  - `GitHubSectionRail({kicker, headline, body, chip})` — full-height section
    with blue accent rail, watermark octo.
  - `GitHubCodeViewer({path[], branch, lang, lines[], caption})` — file viewer
    with breadcrumb, line numbers, and syntax-aware coloring.
  - `GitHubCodeDiff({file, badge, lines[{gutter, text, kind}], caption})` — diff
    view with add/del row backgrounds.
  Evidence beat types (select by beat `shot.remotion.pattern`):
  - `GitHubCallChain({nodes[{k, d, hi}], caption})` — vertical call chain.
  - `GitHubBucketList({buckets[{title, items[], hi}], caption})` — dependency
    buckets.
  - `GitHubStructureMap({rows[{name, loc, hi}], max, caption})` — horizontal
    LOC bar chart.
  - `GitHubChurn({years[{label, count, peak, frozen}], max, caption})` — git
    churn bar chart with peak/frozen states.
- **`shell`** → the SHELL dark terminal skin — diegetic macOS terminal. Tokens:
  `tokens/shell.ts` (stage `#06070a`, terracotta sigil `#d97757`). Components:
  - `ShellSession({path, command, out[{text, cls}], caret, title, host})` —
    terminal window with traffic-light dots, typing animation, staggered output.
    `cls` on each output line: `''` (default), `'dim'`, or `'hi'` (terracotta
    wash on the "money" evidence line).
Converting a sheet between skins is a scene rename (props carry over):
`ClaudeComposerAsk ↔ NikBearBrownTerminalAsk ↔ CodexComposerAsk`,
`ClaudeCodeBeat ↔ NikBearBrownCodeBlock ↔ CodexCodeBeat`,
`ClaudeTitleOutro ↔ CodexTitleOutro` (`title ↔ filename`, keep `code`, keep
the `sparkLine`). One Codex nuance: `CodexComposerAsk` has no `greeting` prop —
fold the spark line into `segment` and keep the persona hello in the narration.
The `github`/`shell` skins are subject surfaces (cutaways to real tools) — the
light Claude narrator skin (B00, NEXT STEPS, OUTRO) is always the bookend.

## Output beats — a MOVING slot (never a still)
The output beat is a **video**, never a static image. Set `shot.source` to null and
fill it ONE of these ways:
1. **Manim** → `shot.source:"manim"`, add the scene to `scenes.py` → `manim/[BID].mp4`.
   Best for a parametric/data animation (a curve drawing, a value snapping onto a grid).
2. **Remotion** → `shot.remotion.pattern` → `media/[BID].mp4`. Typographic/UI motion.
3. **d3 (animated)** → render a d3 animation to mp4, drop as `media/[BID].mp4`.
4. **screen-recording mp4** → `media/[BID].mp4` — a capture of the real run.
5. **nothing → slate** → `vox_run.sh` emits a labeled slate for you to fill with one
   of the above. Every output beat is a slate until the motion is dropped in.
**No static png.** If one frame seems to be the artifact, animate its reveal/transform
or make it a slate. Record the intended motion in the beat's `visual_intent`.

Output beats follow the ASK → RESULT LAW (claude-explainer): the Claude UI is
never decoration — every composer beat is immediately followed by what it
produced, and result graphics render in the episode's channel palette.

## House laws (shared with claude-explainer — all bind here)

CLI videos ride the same chassis, palette, channel roster, and 16:9 → 9:16
pipeline as claude-explainer, so every House law in
`skills/make/ai-explainer/SKILL.md` applies here too. Canonical text lives
there; the CLI-specific application:

- **DEFAULT CHANNEL: claude-liam.** Unless the human names a channel or
  passes `--persona bear`, build on claude-liam
  (Kokoro `am_onyx`, free; IN-FOR-BEAR LAW — "this is Liam, in for Bear" in
  B00 and the outro). `--persona` is the explicit switch; the channel roster
  is the extension point for new voices.
- **LOGO LAW.** The channel brand bug (NBB for @NikBearBrown) rides EVERY beat
  — input and output alike — as a low-opacity lower-right corner mark inside
  the safe area, and full-size on the OUTRO title card. Never skip it.
- **REBUILD LAW.** Any source figure/chart is rebuilt as native animation,
  never a screenshot. The CODE beat is the deliberate exception the
  ACTUAL-CODE LAW carves out — real source shown as itself; everything else is
  rebuilt. Only source-verifiable numbers appear on screen.
- **SHOW-DON'T-TELL LAW.** Already the spine's core for OUTPUT beats (always
  moving, never a still) — extend it to EVERY beat: if a PROBLEM or SUMMARY
  line describes something that can move, show it moving, synced to the
  voiceover, not a static card.
- **FILL-THE-CANVAS / TYPESIZE LAW.** Use the whole 1920×1080. Code and output
  beats especially: size type to fill `SAFE`, never a timid font in the top
  third over dead space. The ~24px legibility floor is a floor, not a target.
- **DOUBLE-CHECK LAW.** Beyond NO FABRICATION: fact-check the source, strip
  anything that dates the video (model version numbers, drifting counts), and
  rewrite in Teardown — never parrot. Corrections logged in SOURCES.md.
- **VISUAL QC LAW.** Every build ends with the frame-level QC pass (sample
  frames, 9-point rubric incl. canvas fill, `SAFE`/`SAFE916` insets, zero
  BLOCKER/MAJOR) — the mp4 probe is a file check, never QC. Full spec:
  `CLAUDE-CODE-VISUAL-QC-CHECK.md` at repo root.
- **HANDOFF LAW (read & discuss).** The NEXT STEPS beat's suggested prompt is
  an INTERESTING prompt that extends the build into the viewer's own work, and
  the narration READS it aloud and DISCUSSES why it's worth running — a prompt
  that only appears on screen is a defect.

(COLD OPEN, SPARK-LINE, ASK→RESULT, OUTRO, one-terracotta, never-publish,
and **DOODLE-BANNED LAW** — DoodleScene/DoodleChart permanently cut
from this register; §8.0 checker in type_check.py enforces; validators
enforce locks, never loosen them to pass a cut style — cited inline above,
bind unchanged.)

**GATE T (type-lock) — ALWAYS RUN**, like factcheck. After every compile,
`scripts/type_check.py` runs per rendered frame and writes `TYPECHECK.md`
(§8.1 min-size · §8.2 overflow · §8.3 contrast · §8.4 kerning / Pango catch ·
§8.5 no-wordy-card · §8.6 golden strings). A FAIL blocks both `./art run` and
`./art final`. See `skills/make/kerning/SKILL.md` for the full type-lock law.

## Voice — Teardown (NikBearBrown)
Narration reads the session like a teardown: the problem and stakes (PROBLEM beat),
what the prompt does, what to *verify* in the code and the output, the design
choice the run exposes, then the lesson and the next move. Strip jargon; explain
the machinery; NO FABRICATION. Forbidden phrases per `prose/teardown/PROSE.md`.

## Build & render (reuses the vox pipeline unchanged)
1. Emit `beat_sheet.json` in the required spine above — INTRO, PROBLEM, the CLI loop
   with ≥1 revision, SUMMARY, NEXT STEPS, OUTRO. Add `scenes.py` for Manim outputs.
2. `python3 runtime/scripts/generate_audio_kokoro.py [reel]` — Teardown-voice narration (free, local).
3. `bash scripts/vox_run.sh [reel]` — renders composer/code/brand beats, renders
   Manim outputs, leaves un-filled output beats as slates, compiles the review cut.
   (Batch D3 lane: `runtime/scripts/build_cli_d3_reels.py` does the same spine
   end-to-end and renders the Claude beats via `remotion_scenes.py`.)
4. Fill each output slate with a Manim/Remotion/d3/mp4 as it's ready; re-run `vox_run.sh`.

## Reference
`reference/example-cli-beat_sheet.json` — a worked CLI video in the full required
spine (INTRO → PROBLEM → ASK → CODE → OUTPUT → CHANGE → OUTPUT → SUMMARY → NEXT STEPS
→ OUTRO), Claude-skin input beats, output beats as animated slots.
