# Rebuild this film

From `/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art`, use the
Show-Tell skill to rebuild `youtube/show-tell-24-isometric-props`. Read the
skill and source records. Preserve unrelated work; do not publish or push.

1. Inspect existing 4K media before rerendering. Reuse verified unchanged clips.
2. If authoring changed, run the reel's `build_reel.py` to inline both shared
   vector kits. This regenerates paperwork and the beat sheet, preserving
   measured audio only where narration is unchanged. Do not run it after
   final assembly unless rebuilding intentionally.
3. Generate only missing/changed narration using the shared Kokoro script.
   Run `finish_audio.py` to pad bookends and lock measured durations. When
   replacing bookend narration, archive the corresponding old unpad file first.
4. Run `preflight.py` and inspect every preview. Use `runtime/scripts/align.py`
   for word timing and check the greeting transcription.
5. Run `./art run youtube/show-tell-24-isometric-props --height 2160`.
   Resolve all gates in scene source; never weaken a checker or ship placeholders.
6. Run `./art final youtube/show-tell-24-isometric-props --height 2160 --out
   youtube/show-tell-24-isometric-props/exports/landscape`.
7. Inspect actual frames at 2 fps and 15/50/85% of each beat. Record results in
   `_qc/REPORT.md`. Verify every beat and the final master are 3840×2160,
   retain the silent outro tail, compute SHA-256, and deliver the full path.

Attribution is in `description.txt` and the asset pack's `ATTRIBUTION.md`.
Never stage or upload without a new user request.
