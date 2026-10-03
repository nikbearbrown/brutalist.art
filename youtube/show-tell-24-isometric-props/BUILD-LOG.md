# Build record — 2026-09-30

User requested 24 adapted isometric props and a Show-Tell film demonstrating
them. No publishing, staging, Git commit, or push was requested for this film.

## Artwork and provenance

- Captured exactly 24 selected Isocons SVG references and its CC BY 4.0 license
  panel. The library manifest retains original and adapted SHA-256 hashes.
- Made simplified native-vector redraws, not a claim of unchanged imports.
  Warm cream/kraft/ink palette, restrained terracotta, editable named layers.
- Added a reusable Manim factory and 24 standalone SVGs. Pack tests confirm
  distinct assets, named groups, bounds, movable parts, and no embedded rasters.
- Updated the Show-Tell skill with a focused link to the prop reference.
  Shortened its existing oversized discovery description to pass skill validation
  while preserving the relevant triggers and production rules.
- Pack includes attribution, original references, contact sheet, and templates.

## Film

- 29 beats: four house bookends, 24 prop demonstrations, one attribution beat.
- Free local Kokoro `am_onyx` (Liam in for Bear). No paid generation.
- Audio master clock measured; 0.8-second opening lead and one-second outro
  tail. Word alignment completed for all 29 beats without fallback.
- Whisper opening check recognized the greeting and “Liam in for Bear,” plus
  the full introduction. No erroneous product/version names in this narration.
- Manim props rendered natively at 3840×2160, 24 fps; Remotion bookends rendered
  with the shared foreground wrapper. No raster upscaling or Topaz.

## Corrections made before final

- Merged extrusion side fills to remove unnecessary segment seams on circles.
- Enlarged spacing between cross-check records and between revision versions;
  this resolved the first Gate T pass's two graphic-bounding-box failures.
- Set hidden checks, detached connectors, and separated parts before the first
  frame, removing initial-pose jumps and premature approvals.
- Timed actions to aligned narration words. Preserved stable midpoint holds.
- Reduced the initially raised deployment package to clear the title; the
  strict layout gate caught its overlap before the clip could be slotted.
- Reduced the layer-stack demo scale to keep the lifted plane below its label.
- Kept the first-pass clips and cache under `_superseded/first-pass/`.

## Verification before master export

- Static, independent contrast/margin, and rendered layout gates passed.
- Review-cut visual gate: 58 sampled frames, zero BLOCKER, zero MAJOR.
- Gate T: all 29 beats pass, zero failures.
- All 29 source clips are 3840×2160; no body scene overruns its narration.
- Fact-check records and four Show-Tell bookends pass their checkers.
- Complete word-aligned sidecar captions: 113 cues, zero SRT errors; every
  narration word retained. Captions are not burned into the film.
- Three samples per beat inspected for states and transitions. Final assembled
  master inspection is recorded in `_qc/REPORT.md` after export.

## Completed local deliverables

- Clean master: `exports/landscape/show-tell-24-isometric-props.mp4`;
  272.542 seconds, native 3840×2160 at 24 fps, narrated, no review markers.
- Final whole-film visual scan completed across 16 contact sheets at 2 fps;
  no unresolved blocker or major defects. Gate T and master checks pass.
- Master SHA256: `e0186f347a6a6b11de43dd265658e074e711011b86d985750cef9c69e46ea806`.
- Reusable 24-prop SVG/Manim pack and attribution are installed under the
  Show-Tell skill's `assets/isocons-24/`, with a distributable ZIP beside it.
- Local creation only: not staged, uploaded, committed, or pushed.
