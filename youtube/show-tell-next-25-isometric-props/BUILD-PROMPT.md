# Rebuild the candidate showcase

Read the Show-Tell skill and inherited production rules. Work from the
brutalist.art root. Do not publish, stage, promote library assets, or push.

1. Inspect existing 4K media and reuse verified unchanged clips.
2. Edit props_25.py and scene_body.py; run build_reel.py only before rebuilds.
3. Generate missing narration with runtime/scripts/generate_audio_kokoro.py;
   use --only for revisions. Run finish_audio.py and runtime/scripts/align.py.
4. Run preflight.py, inspect every still, and fix sources before 4K rendering.
5. Run ./art run youtube/show-tell-next-25-isometric-props --height 2160.
6. Fix all gates, then ./art final youtube/show-tell-next-25-isometric-props
   --height 2160 --out youtube/show-tell-next-25-isometric-props/exports/landscape.
7. Run inspect_frames.py on the master: inspect the 2fps scan and three samples
   per beat. Record defects and corrections. Run make_captions.py after conform.
8. Verify master and every beat native 4K, silent outro tail, clean markers,
   hash, caption coverage, and zero unresolved major/blocker visual findings.
9. Package candidate-props with editable SVGs and vector rig sources. Keep the
   batch separate: Bear chooses what is added to the shared library.
