"""Deterministic assembly of the self-contained scene file and production records."""
from pathlib import Path
import json, runpy, shutil
R=Path(__file__).resolve().parent
ART=R.parents[1]
ns=runpy.run_path(str(R/'make_sheet.py'))
kit=ART/'skills/make/show-tell'
from manim import SVGMobject
logo=SVGMobject(str(ART/'runtime/remotion/public/logo-outro/bear-brown/bear-brown-logo-1.svg'))
logo.set_width(.65).move_to([5.7,-3.05,0])
logo_data=[m.get_points().round(6).tolist() for m in logo.family_members_with_points() if m.get_fill_opacity()>.5]
logo_code='\nNBB_LOGO_DATA='+repr(logo_data)+'''\ndef _brand_bug():
    return VGroup(*[VMobject(fill_color=DIM,fill_opacity=.55,stroke_width=0).set_points(np.array(points)) for points in NBB_LOGO_DATA])
'''
code=(kit/'templates/iso_kit.py').read_text()+'\n'+(kit/'templates/iso_props_24.py').read_text()+logo_code+'\n'+(R/'scene_body.py').read_text()
for n,(slug,label,verb,*_) in enumerate(ns['DATA']):
    code+=f'\nclass B{n:02}_Prop(Scene):\n    def construct(self):\n        _prop_demo(self,{slug!r},{label!r},{verb!r})\n'
(R/'scenes.py').write_text(code)
rows=['# Shot list','', '| Beat | Prop | Motion |','|---|---|---|']
facts=['# Fact check','','Status: checked by Codex, 2026-09-30. No human sign-off claimed. All examples are designed illustrations, not executed product integrations.','',
       '| # | Beat | Claim | Verdict | Source | Fix |','|---|---|---|---|---|---|']
for n,entry in enumerate(ns['DATA']):
    slug,label,verb,narr,event=entry
    rows.append(f'| B{n:02} | {slug} | {event} |')
    facts.append(f'| {n+1} | B{n:02} | Designed example: {event}. Teaching recommendation, not an empirical result. | EXEMPT | scene_body.py and templates/iso_props_24.py; {slug} in archived Isocons references | Explicit illustrative framing; no security or correctness guarantee |')
facts.extend(['| 25 | BIDEA | The pack contains 24 distinct props. | PASS | PROP_IDS and assets/isocons-24/manifest.json; build_prop_assets.py checks all assets | None |',
'| 26 | BDEFS BHTF | Definitions and viewer exercise are the film’s own teaching conventions. | EXEMPT | Show-Tell skill and this storyboard | None |',
'| 27 | BCREDIT | Adapted from Isocons under CC BY 4.0; geometry and animation modified. | PASS | Archived license-panel.txt; https://creativecommons.org/licenses/by/4.0/ ; original and adapted SVGs | Credit retained; no endorsement implied |',
'| 28 | BOUT | Title restatement and channel identity. | EXEMPT | beat_sheet.json metadata | None |'])
(R/'SHOTLIST.md').write_text('\n'.join(rows)+'\n')
(R/'FACTCHECK.md').write_text('\n'.join(facts)+'\n')
(R/'PROMPTS.md').write_text('# Prompts\n\nNo generation prompts. All illustrations are native vector code. Free local Kokoro narration.\nUser request: “start with 24 carefully adapted props and make a show and tell film showing them”.\n')
(R/'SOURCES.md').write_text('# Sources\n\n- https://www.isocons.app/ — 24 selected icon references and CC BY 4.0 license panel, captured 2026-09-30.\n- https://creativecommons.org/licenses/by/4.0/ — adaptation and attribution terms.\n- ../../skills/make/show-tell/assets/isocons-24/manifest.json — source names, original hashes, adapted hashes, named layers.\n- ../../skills/make/show-tell/assets/isocons-24/ATTRIBUTION.md — full attribution.\n\nThe props are simplified redraws, not an unchanged import. The film demonstrates designed teaching metaphors; it does not claim to test an agent, measure a model, or establish software security.\n')
(R/'CHECKS-REPORT.md').write_text('# Authoring check\n\n25 body/credit SHOW beats; 4 explanatory bookends; 0 PUNTs.\nFramework: prop/state/action. Worked examples: 24 actual vector rigs. Falsifiability: a check mark does not prove correctness and a shield does not prove security. Scaffolded task and four Show-Tell bookends present. Rendering and pixel QC recorded separately after execution.\n')
(R/'description.txt').write_text('Twenty-four reusable isometric props for explaining AI workflows: context, tools, human judgment, permissions, evidence, and process. Each drawing demonstrates a meaningful action.\n\nIcons adapted from Isocons (https://www.isocons.app/), CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). Simplified geometry, colors, strokes, and animation modified for Brutalist Show-Tell.\n\nCreators linked by Isocons: https://x.com/leyeConnect and https://x.com/meandchimso. Source notice: Isometric Icons ©2026. No endorsement implied.\n\nNarration: Liam, in for Bear. @NikBearBrown\n')
print('Self-contained scenes and paperwork written.')
