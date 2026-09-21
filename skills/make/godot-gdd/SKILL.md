---
name: godot-gdd
description: Create a Liam-narrated game design document explainer film for an existing Godot game or design package. Walk through the entire GDD's intent, mechanics, scope, risks and acceptance evidence; use existing game scenes to illustrate it. The walker modifier adds Claude/Walker bookends. Keep proposed design, implementation, tests and human judgments distinct.
---

# godot-gdd — explain the design contract

```text
godot-gdd /path/to/game-package [path/to/GDD.md]
godot-gdd walker /path/to/walker-game [path/to/GDD.md]
```

An agent-driven film builder, not a GDD generator or a line-by-line reading.
Resolve the GDD and playable project (often `godot/`) inside the package.
If there are competing GDDs and no authoritative selection, ask which to use.
Output to `<game-package>/youtube/claude-liam-<game>-gdd/`. Preserve the game,
design documents, approval records, previous films and user edits. Creating a
film does not authorize changing the design, building features or publishing.

Read [ai-explainer](../ai-explainer/SKILL.md), [riff](../riff/SKILL.md),
[RENDER-TARGETS.md](../../../RENDER-TARGETS.md),
[PIPELINE-SAFETY.md](../../../docs/PIPELINE-SAFETY.md),
[OUTRO-LOCK.md](../../../OUTRO-LOCK.md), and
[design-evidence.md](references/design-evidence.md) before authoring.

## Read before explaining

Read the entire GDD, including appendices, revision history, open questions and
acceptance criteria. Read the brief and relevant build/test/asset records. Inspect
current source and scenes before describing something as implemented. This skill
usually runs after some game work exists, but a build is not required: missing
features are valid material, not an invitation to invent footage.

Map every substantive top-level section to a narrated beat or an explicit,
reasoned exclusion. Group related sections where that makes a better explanation.
Explain the design's causal chain: player experience → rule → system owner →
visible feedback → acceptance test. Walk through vision, pillars, loops,
mechanics, world/level/narrative/roles, scope, technical and asset constraints,
risks, tests, open decisions and revisions where the document contains them.
Do not manufacture lore, characters, accessibility features or asset pipelines
just to fill a template. Explain why an intentionally empty category is empty.

## A proposal is not a passing test

Label material as **proposed**, **implemented**, **observed/tested**, or **human
decision pending**. A feature can be implemented while its player-experience
hypothesis remains untested. A later build can supersede an old “not built” note
without approving the full design. State the document version and evidence date;
reconcile these differences explicitly rather than silently editing the GDD.

Use short exact document excerpts with section/requirement IDs. Explain what the
rule buys, what it costs, and how someone could reject it. Distinguish theoretical
calculations from measured physics. Keep automated route reachability separate
from a new player's completion time, accessibility and fun. Report actual failed
iterations as well as current passes; do not reinterpret tests as human approval.

## Visualize the GDD with the game

Search `./art scenes "document design requirements scope loop evidence"` before
authoring. Reuse suitable shared components; add one only for a missing teaching
need. A readable document/evidence board is preferable to a fake code editor for
prose. Show a requirement beside the relevant real game image, behavior, level
diagram, ownership flow or measured result. Diagrams must encode real relations,
not just decorate narration. Highlight requirements as their phrases are spoken.

Reconstructed document/editor views and proposed maps are labeled. Do not present
a proposed three-zone course as a screenshot of an implemented one-room slice.
Actual same-build engine images and captures may be reused with hashes, capture
method and source-build evidence. New captures follow
[the Godot capture contract](../godot-waikthrough/references/capture-and-coverage.md).
Never silently change the game, teleport a fixture and call it normal play, or
retime action to fit narration. Label staged views and held frames.

## Liam and Walker structure

Default: Liam in for Bear, Teardown register, local Kokoro `am_onyx`.
Explain the design's choices, not every implementation line; that is
`godot-gamedev`'s job. Riff only on inspected evidence. Duration follows coverage
and measured speech, not a fixed target. No captions unless requested.

`walker` adds:

1. Claude composer, explicitly reconstructed/suggested: “Please use Walker to
   convert my game design document about …” with this game's actual description.
2. Hesitant-writer summary of what was built, what remains proposed, and why the
   film is returning to the GDD. Use a working single-word correction.
3. The design walkthrough, connecting document intent to existing game evidence.
4. Verdict → Your Turn → regular locked outro. AI organizes requirements, traces
   source and runs checks; humans own purpose, scope approval, rights, fairness,
   accessibility and whether the experience is worth playing. Your Turn reads a
   bounded prompt to revise one design hypothesis and specify its test.

Both modes end with `ClaudeTitleOutro`: exact title, @NikBearBrown, one slug-seeded
mascot, no subline, Liam re-reading the title then "At Nik Bear Brown" (no jingle, ever). Liam signs off in Your Turn.
No narration, game sounds or themed voices on the final card.

## Evidence, rendering and handoff

Write `beat_sheet.json`, `GDD-COVERAGE.md`, `gdd-evidence.json`, `SHOTLIST.md`,
`FACTCHECK.md`, `SOURCES.md`, `RIFF.md`, `PROMPTS.md`, and `BUILD-PROMPT.md`.
Run `./art godot-gdd --check REEL --gdd GDD.md` before rendering and at handoff.
It checks the source hash, section coverage, exact excerpts, evidence files and
beat references; it cannot certify explanatory truth, fun or human approval.

Generate and measure narration; bind highlights to its actual word timing. Pilot
new visual components, inspect them, then render through
`runtime/scripts/remotion_scenes.py` only. Assemble with
`./art final REEL --height 2160 --fps 30 --out REEL/exports/landscape`.
Preserve approval, audio and failure gates. Inspect the actual master, document
readability, status labels, proposal diagrams, game evidence and regular outro.
Record checks and remaining limitations honestly. Deliver the rendered 4K film,
full path and quoted `open` command; do not stop at the script when a film is asked
for. Shorts, game changes, Git pushes and publication need separate requests.
