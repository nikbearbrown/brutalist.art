# Approved original Show-Tell props

Bear approved these 25 original objects for the skill on 2026-10-01. They use
the original `iso_kit.py` projection and palette, not Isocons geometry. Keep
their physical vocabulary: kraft containers, dark hardware, paper layers,
visible connectors, and small terracotta signals. Use objects for actions,
not as decorative symbols or proof that a system is safe or correct.

## Select and reuse

- Inspect `../assets/originals-25/contact-sheet.png`; action endpoints are in
  `action-contact-sheet.png` beside it.
- Editable transparent SVGs: `assets/originals-25/svg/`. Matching endpoint
  SVGs: `assets/originals-25/action-svg/`. Named groups remain editable.
- Geometry, action vectors, and hashes: `assets/originals-25/manifest.json`.
- Native Manim: paste `templates/iso_originals_25.py` into `scenes.py`, after
  `iso_kit.py` if using its labels/pacing. The new template is self-contained:
  no sibling imports, manifest reads, raster assets, CairoSVG, or Pillow.

```python
rig = make_original('context-crate', height=3.2, x=0, y=-0.2)
self.add(rig)
self.play(rig.parts['lid'].animate.shift(rig.action_vectors['lid']))
```

Set size with `height` at construction; horizontal extent is capped at 4.8
units. Action vectors include this scale. If you subsequently scale or rotate
the group, transform its action vectors too. Translation needs no adjustment.
The factory bounds both endpoints, not just the resting object. Moving parts
retain painter order; inspect occlusion when composing multiple objects.

This is a rig example, not a complete gated scene. Add a short label beside
the prop and a meaningful new shape after the first frame; coordinate motion
with narration. Test actual scene composition at Gate A, layout, V, and T.
Asset approval is not a blanket film gate pass. Use SVG or native geometry for
4K; never enlarge a raster preview into a master.

## Catalog

| ID | Moving part | Teaching action |
|---|---|---|
| context-crate | lid | Reveal context |
| skill-stack | selected-page | Retrieve instructions |
| tool-block | tool | Undock a tool |
| connector-pair | plug | Connect to a socket |
| server-tower | node | Isolate a node |
| memory-drawers | drawer | Retrieve a saved record |
| context-inbox | new-page | Take the latest input |
| agent-workstation | tool | Bring a tool to the workspace |
| review-desk | evidence | Bring evidence to review |
| permission-gate | barrier | Permit passage |
| approval-stamp | stamp | Record a decision |
| secure-vault | lock-bar | Release a locking bar |
| conveyor | parcel | Move work along a pipeline |
| branch-junction | packet | Choose a route |
| checkpoint-scanner | parcel | Inspect a passing item |
| evidence-binder | cover | Inspect the records |
| inspection-lamp | lamp-head | Focus inspection |
| experiment-bench | sample | Insert or remove a test sample |
| version-shelves | selected-version | Retrieve a revision |
| comparison-trays | sample-b | Compare alternatives |
| human-handoff | packet | Transfer responsibility |
| task-queue | next-task | Take the next work item |
| budget-slots | allocated-token | Allocate finite capacity |
| recovery-dock | module | Restore a component |
| release-parcel | lid | Open a delivery |

## Maintenance

The skill-local manifest and SVGs are the promoted snapshot. Run
`python3 skills/make/show-tell/scripts/build_original_props.py` from the
toolkit root to regenerate its standalone Manim template and portable ZIP;
run `scripts/test_original_props.py` from this skill to verify all 25 rigs.
No source-site fetch is needed. The exploratory originals and previous films
are preserved outside this promoted set; rebuilding them does not silently
replace the skill's assets.
