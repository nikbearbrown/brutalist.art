---
name: godot-gamedev
description: Make a Liam-narrated Godot development film pairing each focused code excerpt with the visible game result it produces. Explains components, scenes, assets, art and tests using source-backed editor reconstructions and actual engine evidence. Use walker for Claude/GDD bookends. Does not build or publish a game.
---

# godot-gamedev — take the game apart

```text
godot-gamedev /path/to/game
godot-gamedev walker /path/to/walker-game
```

This is an agent-driven film builder, not an unattended generic code summarizer.
Resolve the actual `project.godot`; the game package may contain a `godot/` child.
Keep outputs in `<game-package>/youtube/claude-liam-<game>-gamedev/`, separate
from any gameplay walkthrough. Preserve the game, saves, existing films and
user edits. No game change, paid call, Git push or publication is implied.

Read [ai-explainer](../ai-explainer/SKILL.md) for the bookend/voice chassis,
[riff](../riff/SKILL.md) for evidence-led commentary,
[RENDER-TARGETS.md](../../../RENDER-TARGETS.md),
[PIPELINE-SAFETY.md](../../../docs/PIPELINE-SAFETY.md), and
[OUTRO-LOCK.md](../../../OUTRO-LOCK.md). This skill owns the middle: real
source and Godot editor anatomy replace generic Claude prompt/result loops.
Real engine images/footage are evidence, not placeholders to redraw.

## Code → visible result is the teaching unit

Show one focused, readable excerpt, then immediately show what those lines do
in this game before introducing another excerpt. Narration points from the
named line/property to the specific event, shape, control or state on screen.
Do not accumulate code-only beats and defer all gameplay to the end. A filename,
verbal description, or another code panel is not a visible result.

Use real motion for movement, collisions, camera tracking and state changes.
For drawing/asset code, a real engine preview can establish appearance; label
staged poses and diagnostic collider overlays. For configuration or tests,
show the running consequence or recorded tool output and explain its limits.
A split view is useful when it remains readable, but must still have a clear
read-the-code phase followed by a watch-the-result phase. Don't make gameplay
tiny to retain an entire editor around it.

Record a `teaching_contract: "code-then-result-v1"` and `code_result_pairs` in
new evidence ledgers (see the reference). The checker verifies adjacency and
hash-bound result media, not whether the footage actually proves the claim;
that requires viewing the event sequence. Older ledgers remain readable but
do not certify this new teaching contract.

For an assignment-focused film, lead with a short, verified setup and the
actual assignment requirements. Connect each result to a bounded student
change, prediction or check. Distinguish the untouched starter from a completed
student extension; reuse same-build footage honestly and preserve prior films.

## Read the whole playable system

Inventory runtime code, scenes, resources, configuration, input bindings,
levels, UI, art/audio, import settings, tests and export setup. Read every
runtime file; group related components into teachable units rather than
reading every line aloud. Trace ownership and dependencies, not just filenames.
Read the brief/GDD to distinguish built, proposed and missing features.
Read [evidence.md](references/evidence.md) before producing the source ledger.

For each implemented component, show where it lives, what data enters, the
important lines or properties, what changes, and what the player sees. Explain
why that design was chosen and one practical trade-off. Where a number matters,
derive it from the current code or a recorded test; do not substitute a familiar
tutorial's values. Show at least one complete input → state → output trace.
Give tests their own treatment, including what test-only shortcuts cannot prove.

Art is code/data too: inspect actual textures, sprite sheets, palettes, fonts,
animation tracks, drawing functions, meshes/materials and sound sources where
they exist. If all art is procedural, demonstrate the drawing commands and the
real rendered result. Do not invent a sprites folder, TileMap, animation player,
soundtrack or import workflow that this project does not use. Distinguish
visual silhouettes from collision geometry and source defaults from overrides.

## Show it as a developer would find it in Godot

Run `./art scenes "Godot editor code scene tree inspector assets"` before
authoring. Reuse `GodotDevWorkbench` when its props fit; extend the shared
component only for a real missing teaching need. Read its source/props first.
Preserve Godot's recognizable Scene/FileSystem, Script/2D, Inspector and Output
layout and syntax colors. Large readable excerpts outrank a pixel-perfect tiny
desktop replica. Native portrait variants must reflow, not crop.

Label reconstructed editor views **“Godot editor reconstruction”** and provide
source path/line numbers. They are teaching views, not recordings of a live
editing session. Never invent a debugger success line or a property value.
Extract displayed code verbatim from hashed files. Use separate annotation
panels for explanations; clearly label pseudocode if it is needed.

Distinguish the saved/local scene from runtime/remote nodes. Code-created nodes
do not magically appear in a saved `.tscn`; inspect a running instance on an
isolated copy and record its tree when that distinction matters. Likewise,
ordinary script variables are not exported Inspector fields. Show only real
exported/resource properties, or label a separate data panel as a source or
runtime inspection. Asset previews must correspond to actual files or actual
engine output, with provenance. Do not silently repair the game for the film.

## Narration and structure

Liam, in for Bear; Teardown register; local Kokoro `am_onyx`. The voice explains
the mechanism while source lines, nodes, properties and results are highlighted.
Write the visible sequence before the narration. Riff on inspected output, not
imagined play. Keep code readable long enough to follow; split dense components
into several beats. Duration follows the depth and measured audio, not a preset
film length. Diagram beats, focused code views, art previews and real runs should
each earn their place. A file list with voiceover is not a component explanation.

Standard mode opens on the game/architecture and proceeds into development.
`walker` adds these bookends in order:

1. Claude composer with a suggested/reconstructed prompt beginning “Please use
   Walker to convert my game design document about …”; describe this actual game.
2. Hesitant-writer summary of what was built and what this teardown will explain.
   Use a working single-word correction and enough measured time to complete it.
3. Development body: component-by-component mechanism and evidence.
4. Verdict → Your Turn → regular outro. The verdict separates implemented work,
   limitations and human judgment. Your Turn reads a useful Walker prompt aloud
   and invites one bounded code change plus prediction/test, not blind copying.

Both modes end with the locked `ClaudeTitleOutro`: exact title, @NikBearBrown,
one slug-seeded crisp mascot, no subline, Liam re-reading the title then "At Nik Bear Brown" (no jingle, ever). Liam signs
off in Your Turn. No narration, game SFX or themed voices on the final card.

## Build and finish

Write `beat_sheet.json`, `COMPONENTS.md`, `gamedev-evidence.json`, `SHOTLIST.md`,
`FACTCHECK.md`, `SOURCES.md`, `RIFF.md`, `PROMPTS.md` and `BUILD-PROMPT.md`.
Generate/measure narration, then bind highlights to its phrases. Render a pilot
of any new component through `runtime/scripts/remotion_scenes.py`; inspect it
before batching. Use that wrapper for the rest, then `./art final REEL --height
2160 --fps 30 --out REEL/exports/landscape`. Preserve all approval/audio/QC gates.

Run `./art godot-gamedev --check REEL --game GODOT_PROJECT` before rendering and
at handoff. It checks file coverage, hashes, source lines and beat references,
not explanatory truth or visual quality. Run relevant existing game tests on an
isolated copy. Existing same-build gameplay captures may be reused with hashes
and disclosure. New captures follow godot-waikthrough's capture contract; no
test-fixture teleporting presented as played gameplay. No silent action retiming.

Inspect the actual master, code at reading size, highlights, art/collision
comparison, editor disclosure, clock/sound, and the regular outro. Record real
test and visual outcomes, including corrections. No captions unless requested.
Deliver the 4K MP4, absolute path and quoted `open` command, component coverage
and limitations. Do not stop at a skill, script or beat sheet when a film was asked
for. Do not make a Short or publish unless separately requested.
