# Candidate props 25–49

Status: **for Bear's review, not added to the shared library**.

Each SVG is editable, transparent, and contains named groups matching the
Manim rig's `.parts` dictionary. The manifest records source and adapted
hashes, source names, license, and the groups available for animation.

For native Manim rendering, paste `iso_kit.py`, `iso_props_24.py` (shared
geometry helpers), then `props_25.py` from `templates/` into the scene file.
Use `make_candidate('sliders', scale=1.5)`, then animate
`hero.parts['knob']`. The factory itself does not mutate a scene. The older
24-prop helper is a dependency, not another set of candidates in this pack.

Prepare initial states before the first rendered frame. Hide checks or
results until the represented action happens. Labels belong beside the
object; keep the illustration and voice focused on one change.

## Review list

| Number | Prop | Teaching action |
|---|---|---|
| 25 | Prompt suggestion | Choose a starting instruction |
| 26 | Question exchange | Ask for missing context |
| 27 | Token | Allocate a symbolic budget unit |
| 28 | Filter | Narrow a collection |
| 29 | Sort | Change order, not membership |
| 30 | Dynamic form | Reveal a relevant follow-up |
| 31 | Responsive layout | Preserve tasks across screens |
| 32 | Sliders | Adjust a range |
| 33 | Toggle on | Make a two-state choice |
| 34 | Settings Accessibility | Provide task support |
| 35 | Highlight keyboard focus | Show where input lands |
| 36 | Data alert | Investigate a record |
| 37 | Sync Problem | Stop a failed handoff |
| 38 | Undo | Reverse a recent action |
| 39 | Settings backup restore | Recover a saved state |
| 40 | Deployed code history | Inspect release history |
| 41 | View Kanbab (source spelling) | Move a task between states |
| 42 | Timeline | Follow an event sequence |
| 43 | Query Stats | Investigate a metric |
| 44 | Data table | Inspect one comparable row |
| 45 | Quiz | Attempt before seeing a response |
| 46 | Local library | Open source material |
| 47 | Lab research | Approach a sample for testing |
| 48 | Map | Reveal relationships |
| 49 | Flag | Mark a milestone |

These are simplified adaptations, not unchanged imports. See ATTRIBUTION.md
and keep it with any reused or redistributed artwork. A symbol is not proof:
the chart is schematic, the token is a metaphor, and the experiment has no
invented result. Library selection remains a human decision.
