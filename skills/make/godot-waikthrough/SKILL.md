---
name: godot-waikthrough
description: Play a Godot game, capture every implemented feature, use riff for on-screen Liam commentary, and render a 4K walkthrough with the regular outro. The walker modifier adds the Claude GDD prompt opening, a second-beat built-result summary, Verdict, and Your Turn. Also accepts godot-walkthrough. Does not build a game or publish it.
---

# godot-waikthrough — play the features, riff, render

`godot-waikthrough` is the requested command spelling; `godot-walkthrough` is an
alias. This is an **agent-driven builder** like `ai-explainer`, not a shell
command that invents a play route without reading the project.

```text
godot-waikthrough /path/to/game
godot-waikthrough walker /path/to/walker-jumpman
```

Use the existing Godot project, its brief/GDD, controls, and test evidence.
Resolve the actual `project.godot` (often in a `godot/` child). If more than one
unrelated candidate exists, ask which game. Output belongs in the game's
own `youtube/claude-liam-<game>-walkthrough/`, or the user's chosen reel folder.
Read [riff](../riff/SKILL.md), [capture-and-coverage.md](references/capture-and-coverage.md),
[RENDER-TARGETS.md](../../../RENDER-TARGETS.md), and
[PIPELINE-SAFETY.md](../../../docs/PIPELINE-SAFETY.md) before production.

## 1. Identify the playable build

Inventory **implemented** features from source plus a real run. Compare with the
GDD; explicitly distinguish built, planned, and broken. Include controls,
menus, failure/recovery, completion/replay, and settings where they exist—not
just the successful path. Group related features naturally; no fixed beat count.
Do not promise every theoretical edge case. For an enormous game, report the
coverage size before silently reducing “every feature” to a highlights reel.

Record the game revision/content hash, engine version, feature checklist, input
route, and capture method. Work on an isolated copy for harness/config changes;
preserve the original game's code, assets, saves, and currently open instance.
Do not secretly fix the game to make a demonstration succeed. If it cannot run,
report the exact blocker; no fake gameplay in place of an engine run.

## 2. Play and capture, then riff

Drive the game through its **normal input path**, manually or with an explicit
deterministic input driver. Capture the real rendered viewport. A driver may
observe position/state to choose inputs, but must not teleport, set completion,
disable collisions, or call test-only gameplay shortcuts to claim a played result.
Clearly label scripted-input captures as such; they are not human playtests.

Show the precondition, input, and visible outcome of each implemented feature.
Include a genuine failure and recovery where supported. For a timing-sensitive
feature, show the sequence and use input/tick evidence; a still is insufficient.
Write `coverage.json` using the reference contract. Any unshown implemented
feature prevents the **complete walkthrough** claim.

Invoke **riff** on these captures. Inspect first; narrate what is happening on
screen, the mechanism, and a useful trade-off. Use Liam in for Bear, local Kokoro
`am_onyx`, not a game character. Source-code facts and untested judgments must
be identified as such. The human judges feel/fun; AI plays, records, explains,
and checks. Keep gameplay visually recognizable; do not retint or recreate it
as a Claude-style mock game.

## 3. Assemble the film

Read [ai-explainer](../ai-explainer/SKILL.md) for the render/voice chassis and
reusable Claude components. This skill owns the middle: **real gameplay** takes
precedence over that skill's rebuilt-visual or no-screen-recording rules.
Do not force a prompt/code/revision loop onto a game walkthrough.

- **Standard mode:** open on the game and its objective, with Liam's brief
  introduction; then play/riff through the feature coverage. No obligatory
  Walker/GDD or Claude prompt opening.
- **`walker` mode:** use the AI-explainer bookends in this exact order:
  1. **B00 — ClaudeComposerAsk.** Prompt begins “Please use Walker to convert my
     game design document about …” and describes this game's actual idea, then
     asks for a playable Godot project. No literal `X` placeholder. Identify a
     reconstructed prompt as an illustrative reconstruction; never pretend it
     is a historical transcript. No fictional live build/progress receipts.
  2. **B01 — what was built.** Summarize the actual result in plain language,
     e.g. “Level one of walker-jumpman: two gaps, a spike, and a finish flag.”
     State the slice's limits, not unbuilt GDD promises. Use the existing
     hesitant-writer overview with a meaningful correction and sufficient
     measured time, rather than a generic “what is Walker?” lesson.
  3. **Gameplay body.** The actual feature walkthrough and synchronized riffs.
  4. **Verdict → Your Turn → regular outro.** Verdict separates observed working
     features from defects, untested claims, and planned work. Your Turn shows
     a relevant Walker prompt, reads/discusses it, and invites one concrete
     experiment. Liam signs off here, before the final card.

Both modes close with a verdict and actionable Your Turn, then the **regular
outro**. Read [OUTRO-LOCK.md](../../../OUTRO-LOCK.md): `ClaudeTitleOutro`, exact
episode title, `@NikBearBrown`, one crisp-safe mascot below the handle, no
subline. The card is **spoken, never scored**: Liam re-reads the exact title,
then "At Nik Bear Brown", over a 1 s tail hold. No jingle, no gameplay audio,
no invented character voice, chiptune, victory sound, or game-themed music on
that final card. This lock wins over older parent outro instructions.

## 4. Render and verify, don't stop at a beat sheet

Capture evidence first, then author `beat_sheet.json`, `RIFF.md`, `SHOTLIST.md`,
`FACTCHECK.md`, `PROMPTS.md`, and `BUILD-PROMPT.md`. Generate and measure Kokoro
audio; synchronize genuine action to the words. Follow the reference's
no-retiming rules. Use the approved `runtime/scripts/remotion_scenes.py` path
for bookends, then the regular compositor, not a second rendering system.

```bash
# From brutalist.art; replace REEL with the resolved reel path.
./art godot-waikthrough --check REEL
python3 runtime/scripts/generate_audio_kokoro.py REEL
# Render the authored bookends using remotion_scenes.py's current --help.
./art final REEL --height 2160 --fps 30 --out REEL/exports/landscape
./art godot-waikthrough --check REEL
```

The check validates the coverage contract, clip hashes, dimensions, time ranges,
input-log presence, and beat references; it cannot judge truth or completeness
of the inventory. Inspect the actual film against the checklist as well.
Retain all existing fact, approval, frame, and audio gates—never fabricate human
signatures. Check native 4K gameplay and final 3840×2160 output, the opening and
closing sequence, sync, failure/recovery, every feature, and clean regular-outro
audio. No burned captions by default. Sidecar SRT only if requested.

For 30 fps captures, preserve exact frame-fraction durations (e.g. `320/30`),
not six-decimal upward-rounded probe strings that can add a frame and cause
unintended retiming. Verify each gameplay slot's compositor ratio rounds to
`1.000000`; extend a labeled final-frame hold if additional narration time is
needed, not the action. If a game's dimming scrim triggers the flat-card contrast
heuristic, inspect the actual pixels. A beat may declare named normalized
`qc.contrast_regions` (`label`, `box: [x0,y0,x1,y1]`) plus a written
`qc.contrast_reason` to test its essential text locally. Every region must pass;
all other checks remain. Never relabel gameplay as a source report or suppress
all frame checks to obtain a pass. Manually inspect menu text and game content.

Deliver the MP4's absolute path, a quoted `open` command, feature coverage,
limitations, and QC results. No upload, publish, or Git push is implied. Do not
make a Short unless asked; a requested Short is a separate native 9:16 high-level
cut **strictly under 180 seconds**, not this whole walkthrough cropped vertically.
