# Capture and coverage

## Capture choices

Use an existing trusted recording mechanism or an input-driven Godot capture.
Do not require unavailable OS automation. First inspect `godot --help` and the
project's existing tests. Godot's [Movie Maker](https://docs.godotengine.org/en/stable/tutorials/animation/creating_movies.html)
can record a deterministic engine run using `--write-movie`, `--fixed-fps`, and
bounded `--quit-after`. It is offline rendering, **not evidence of real-time FPS**.
Check the [command-line reference](https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html)
for the installed version. Record version and settings in `CAPTURE.md`.

For example, on an isolated project copy with a game-specific input driver:

```bash
godot --path "$CAPTURE_PROJECT" --script res://capture_driver.gd \
  --write-movie "$REEL/capture/run.avi" --fixed-fps 60 --quit-after 1800
```

Those variables are explicitly resolved task paths, not guessed locations.
The driver must instantiate the real main scene and use `Input.action_press` /
`Input.action_release` or input events. Log actions against game ticks; release
held keys between runs. Assert the expected result, and quit nonzero on failure.
Merely exhausting `--quit-after` is not success. Review scripts before executing
them; a copy does not isolate network access or `user://` saves automatically.
Give the capture copy a separate user-data directory when the game writes saves.

Record **native rendered 3840×2160**, not a 720p recording scaled to a 4K container.
Window dimensions can be display-clamped; test the project's stretch mode and
actual output. A SubViewport capture or Movie Maker setting may be necessary.
For pixel art, disclose logical resolution separately: crisp scaling of the
game's intended logical canvas is different from enlarging a recorded video.
Do not change level bounds or gameplay merely to fill a frame. Probe and inspect
one short capture before a full run. Use bounded takes: AVI has a size limit;
PNG/WAV sequences can consume substantial disk space. Stop cleanly so headers
finalize. Keep original captures until their final evidence has been verified.

For walker-jumpman, inspect its **current** scene, input bindings, first-level
data, and tests. Existing unit tests may teleport or seed coyote/buffer state;
those are useful mechanical checks, not walkthrough footage. Write an input-only
route for menu/start, movement/jump, hazard/fall retry, pause/resume, manual retry,
completion/replay, and any other actually implemented feature. Do not add
cherries, sound, or settings claims merely because the full GDD proposes them.

## Timing and audio contract

Keep the real precondition → input → result interval at normal simulation speed.
Split long explanations, shorten narration, or show **labeled** replays/holds
outside that interval. A replay must not look like a second independent test.
Do not use `pantry` intake on the captures: its stripping/retiming behavior is
not an evidence-preserving gameplay edit.

The stock compiler's ordinary footage path can center-cut and slow video to fit.
Therefore pre-trim each `media/Bxx.mp4` deliberately and conform the narration
window to the whole selected action, rather than feeding arbitrary-length raw
captures to it. Align `render_duration_s` and clip duration at the film frame rate,
padding narration with silence when necessary. Inspect compiled clips for
retiming/trim notices and verify event timing against the original; a prose
claim that timing was preserved is not a check. Do not mislabel gameplay as a
fellow's `SOURCE_REPORT` to evade this issue or the approval system.

Liam narration is the primary audio. If the game has meaningful audio, explicitly
decide whether to retain it quietly under narration; use the supported audio
inputs, not an untested mux assumption. Document any muting. A silent game needs
no fabricated sound effects. All gameplay audio stops before the regular outro;
only Liam's spoken title and "At Nik Bear Brown" play on that final card (no jingle).

## `coverage.json` contract

Author this in the reel folder. The validator is read-only. Hash the actual
capture bytes after recording; changing a capture invalidates its evidence.
Use a content hash of the source snapshot for `build_id` (64 hex characters);
record the hash method and source list in `CAPTURE.md`. Include any GDD omissions
as `planned`, with a reason. An implemented-but-broken/unshown feature remains
`implemented` with empty evidence: the check must fail until shown or the human
explicitly agrees to a partial walkthrough. Don't relabel it `planned` to pass.

```json
{
  "schema_version": 1,
  "game": {"name": "walker-jumpman", "build_id": "<source-snapshot-sha256>"},
  "captures": {
    "run-01": {
      "path": "capture/run-01.mp4",
      "sha256": "<capture-file-sha256>",
      "build_id": "<same-source-snapshot-sha256>",
      "method": "scripted-input",
      "input_log": "capture/run-01-inputs.jsonl"
    }
  },
  "features": [
    {
      "id": "jump", "status": "implemented",
      "evidence": [{
        "capture": "run-01", "beat_id": "B02",
        "start_s": 3.0, "action_s": 3.5, "end_s": 5.0,
        "observation": "Player leaves the ground and lands on the next step.",
        "riff": "Name the visible decision and its trade-off, after inspecting this take."
      }]
    },
    {"id": "cherries", "status": "planned", "reason": "GDD only; not built.", "evidence": []}
  ]
}
```

The schema example is **not evidence**. Replace all sample times, hashes, and
observations with measured ones. `method` is `scripted-input` or `human-input`;
both require a nonempty input log (structured notes/timecodes suffice for human
input). All paths are relative to and contained in the reel, including resolved
symlinks. Referenced `beat_id`s must exist in `beat_sheet.json` and have narration.

Run `./art godot-waikthrough --check REEL` before final assembly and after changes.
`--min-height 720` is available on the Python checker **only for a pilot/test**;
the public command defaults to native 4K and a low-resolution pilot is not a
finished 4K film. Machine checks do not certify that a described action occurs,
that an input log is truthful, or that source inspection found every feature.
Those require actual visual/source review, recorded in `_qc/REPORT.md`.
