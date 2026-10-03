"""Build self-contained sources and records. Does not promote library candidates."""
from pathlib import Path
import json,runpy
from manim import SVGMobject
R=Path(__file__).resolve().parent;ART=R.parents[1];kit=ART/'skills/make/show-tell'
ns=runpy.run_path(str(R/'make_sheet.py'))
logo=SVGMobject(str(ART/'runtime/remotion/public/logo-outro/bear-brown/bear-brown-logo-1.svg'))
logo.set_width(.65).move_to([5.7,-3.05,0])
points=[m.get_points().round(6).tolist() for m in logo.family_members_with_points() if m.get_fill_opacity()>.5]
bug='\nNBB_LOGO_DATA='+repr(points)+'''\ndef _brand_bug():
    return VGroup(*[VMobject(fill_color=DIM,fill_opacity=.55,stroke_width=0).set_points(np.array(points)) for points in NBB_LOGO_DATA])
'''
code='\n'.join(f.read_text() for f in (kit/'templates/iso_kit.py',kit/'templates/iso_props_24.py',R/'props_25.py'))+bug+'\n'+(R/'scene_body.py').read_text()
for n,(slug,label,verb,narr,event,cue) in enumerate(ns['DATA']):
 code+=f'\nclass B{n:02}_Prop(Scene):\n    def construct(self):\n        _prop_demo(self,{slug!r},{label!r},{verb!r},{cue!r})\n'
(R/'scenes.py').write_text(code)
rows=['# Shot list','','| Beat | Candidate | Motion |','|---|---|---|']
facts=['# Fact check','','Status: agent-reviewed by Codex, 2026-09-30; illustrative claims and source-license records checked. This new batch has no human sign-off yet.','','These are designed teaching metaphors, not executed integration tests or measured outcomes.','','| # | Beat | Claim | Verdict | Source | Fix |','|---|---|---|---|---|---|']
for n,(slug,label,verb,narr,event,cue) in enumerate(ns['DATA']):
 rows.append(f'| B{n:02} | {slug} | {event} |')
 facts.append(f'| {n+1} | B{n:02} | Designed illustration: {event}. Recommendations, not measured results. | EXEMPT | props_25.py; scene_body.py; archived Isocons source | Symbols explicitly distinguished from evidence; no fabricated data |')
facts.extend(['| 26 | BIDEA | 25 new candidate props. | PASS | manifest.json count and 25 unique IDs, none in first pack | Library selection remains with Bear |','| 27 | BDEFS BHTF | Teaching definitions and exercise. | EXEMPT | Storyboard conventions | None |','| 28 | BCREDIT | Isocons CC BY 4.0 adaptations; candidate status. | PASS | candidate-props/references/license-panel.txt; https://creativecommons.org/licenses/by/4.0/ | Attribution retained |','| 29 | BOUT | Title and channel. | EXEMPT | Metadata | None |'])
for name,lines in [('SHOTLIST.md',rows),('FACTCHECK.md',facts)]: (R/name).write_text('\n'.join(lines)+'\n')
(R/'PROMPTS.md').write_text('# Prompts\n\nNo generation prompts. Native vector construction and free local Kokoro narration. User requested the next 25 props and a film, with library selection deferred.\n')
(R/'SOURCES.md').write_text('# Sources\n\n- https://www.isocons.app/ — 25 selected source SVGs and license, archived in candidate-props/references/.\n- https://creativecommons.org/licenses/by/4.0/ — attribution and adaptation terms.\n- candidate-props/manifest.json — source names, hashes, named parts.\n- props_25.py and scene_body.py — actual native-vector demonstrations.\n\nSimplified adaptations, not unchanged SVG conversion. The trend and timeline have no empirical data or numerical scale. Token is a symbolic allocation unit, not literal language tokenization. No product integration, security guarantee, or test result is claimed.\n')
(R/'CHECKS-REPORT.md').write_text('# Authoring check\n\n26 body/credit SHOW beats, four bookends, zero PUNTs. Framework: control/recovery/evidence. Worked examples: 25 candidate rigs. Falsifiability: symbols do not establish delivery, correctness, or test success. Scaffolded task and all four Show-Tell bookends retained. Candidate library status stated aloud. Pixel verification follows rendering.\n')
credit='Icons adapted from Isocons (https://www.isocons.app/), CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). Source notice: Isometric Icons ©2026. Creators linked by the site: https://x.com/leyeConnect and https://x.com/meandchimso. Geometry, palette, strokes, layers, and motion modified. No endorsement implied.'
(R/'description.txt').write_text('Twenty-five more Show-Tell prop candidates for design, recovery, evaluation, and learning. Each performs one meaningful action. These are illustrations, not reports of empirical tests. Library selection remains pending.\n\n'+credit+'\n\nLiam, in for Bear. @NikBearBrown\n')
(R/'candidate-props/ATTRIBUTION.md').write_text('# Candidate pack 25–49\n\n'+credit+'\n\nSimplified native-vector redraws, not verbatim conversions. The adapted SVG artwork is distributed under CC BY 4.0. Keep this notice with redistribution. No library promotion has been approved.\n')
print('Scenes and records written; candidate status preserved.')
