# Original Show-Tell props

25 original procedural illustrations, created 2026-10-01 after Bear rejected
the adapted icon packs. No third-party SVGs, silhouettes, or traced images are
used. The house `skills/make/show-tell/templates/iso_kit.py` supplies the visual
reference: 30-degree projection, kraft faces, warm-ink outlines, dark hardware,
white paper layers, grey detail and small terracotta signals.

These are physical teaching objects, not extruded flat pictograms. Each has a
named movable component. Labels belong beside the object in a film, not baked
into the artwork. The catalog demonstrates component motion; it is not a
render-verified film. Each eventual film still requires its own layout and
Gate T checks.

## Review

- `index.html`: local interactive catalog; Show action / Reset per object.
- `contact-sheet.png`: assembled set.
- `action-contact-sheet.png`: action endpoints.
- `svg/`: transparent, editable vector artwork with named groups.
- `action-svg/`: endpoint variants with the same coordinate system.
- `png/`: transparent 640-pixel previews; use SVG/native geometry for 4K.
- `manifest.json`: explicit geometry, part names, action vectors and hashes.

## Rebuild and reuse

Run `python3 build.py`, then `python3 test_props.py` in this directory.
Export requires CairoSVG and Pillow; native-rig tests also require Manim.

`manim_props.py` exposes `make_original('context-crate')`, returning a native
VGroup with `.parts` and `.action_vectors`. Animate the selected component:

```python
rig = make_original('context-crate')
self.add(rig)
self.play(rig.parts['lid'].animate.shift(rig.action_vectors['lid']))
```

For a Gate A-isolated scene, inline the geometry definitions and factory;
do not depend on companion files surviving the isolated scene copy. Follow
Show-Tell's timing, new-shape and type rules when writing film scenes.

The two earlier adaptation packs and their films are preserved. This original
set is separate and awaits Bear's visual selection; nothing is automatically
promoted, published, or substituted into existing films.
