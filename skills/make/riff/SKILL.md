---
name: riff
description: Render or inspect a visual artifact and riff on what visibly happens, its mechanism, trade-offs, and educational usefulness. Use for riff requests about clips, gameplay, Remotion or Manim scenes, or as the commentary pass inside a walkthrough. Default narrator is Liam in for Bear. Never publishes.
---

# riff — show it, then judge the design

Inputs: a local clip, scene, or small related collection. The output is commentary
grounded in visible evidence, paired with the rendered artifact—not a generic
review written from a filename. This is the public toolkit adaptation of the
legacy `component-showcase` riff workflow; no sibling repository is required.

## Look before writing

- For a clip, probe it and inspect representative frames **and the event sequence**.
  Keep timecodes. A frame can show a state; it cannot establish response time,
  motion, or causality. Listen to existing audio when it bears on the claim.
- For a Remotion/Manim scene, find the existing renderer with `./art scenes`,
  inspect its props/source, then render one small, clearly labeled educational
  fixture. Verify this pilot before batching. Record seeds and inputs.
- For gameplay, use the actual engine capture supplied by
  [godot-waikthrough](../godot-waikthrough/SKILL.md). Do not substitute a fixture,
  animation, screenshot slideshow, or imagined success for a played feature.

Write each riff around **what changed → why that matters → the trade-off**.
Point to the event as it occurs. Let the footage carry the evidence and the
voice carry the interpretation. A useful riff may name a limitation or an
experiment for the viewer; it need not manufacture a criticism for every beat.

Example, **only if the capture shows it**: “The spike sends us straight back to
the start. That's a cheap retry: I can test another jump immediately. It doesn't
yet tell us whether a first-time player saw the danger.” Never call a scripted
route a human playtest or infer fun, fairness, or accessibility from it.

Record `RIFF.md`: artifact + time range | visible observation | interpretation
and its source, if needed | narration | suggested next experiment. Separate
observations from source-code explanations and hypotheses. Missing or failed
renders stay in the report; do not silently omit them. Humans decide what is
fun, useful, publishable, or worth promoting.

## Voice and rendering

Default: **Liam, in for Bear**, Teardown register, local Kokoro `am_onyx`.
No voice cloning, character impressions, invented dialogue, paid TTS, or added
game sounds. Concise, conversational reactions beat continuous chatter.

Inside another builder, return the riffs and evidence mapping to that builder;
do not add a second intro, captions, jingle, or outro to every clip. Generate
measured narration, then synchronize its phrases to the observed actions.
Never change apparent gameplay speed to make a sentence fit.

When the user asks for a standalone riff **film**, use
[ai-explainer](../ai-explainer/SKILL.md) for its bookends and render chassis;
real clips remain evidence, not Claude UI wallpaper. Follow
[OUTRO-LOCK.md](../../../OUTRO-LOCK.md): standard title/handle/mascot card,
Liam re-reads the title then says "At Nik Bear Brown"; no jingle or music on that card. Do not manufacture
a scene-themed ending. No burned-in captions unless explicitly requested.
For a critique-only request, inspect and report; do not launch a film build.

Deliver the rendered film when requested, `RIFF.md`, and actual validation
results. A drafted script is not a rendered film. Never publish or push merely
because a riff was requested.
