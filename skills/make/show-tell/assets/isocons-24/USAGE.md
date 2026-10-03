# Using the 24-prop pack

Open `adapted-contact.png` to choose an object. Import individual files from
`svg/` into Figma or another SVG editor. Each file has a transparent background
and named groups; it contains no embedded raster image.

For Manim, paste the toolkit's `templates/iso_kit.py` followed by
`templates/iso_props_24.py` into your scene source. The downloadable ZIP includes
both files under `templates/`. For example:

```python
prop = make_prop('shield-lock', x=-1, y=0, scale=1.6)
self.add(prop)
self.play(prop.parts['shackle'].animate.shift(UP * 0.35))
```

`manifest.json` lists every ID and its movable parts. Choose the starting state
before the first frame: remove an approval check from the group, then create it
only after the review action. Keep labels upright and outside object outlines.

Use a small cast in an ordinary film; the accompanying showcase uses all 24
because the prop library is its subject. Motion should explain a change, not
merely decorate narration. A security symbol is not proof of security.

Read and retain `ATTRIBUTION.md`. These are simplified redraws adapted from
Isocons, not an official or unchanged Isocons release.
