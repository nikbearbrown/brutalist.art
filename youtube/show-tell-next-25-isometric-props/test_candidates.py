"""Verify source fidelity records, editable layers, 25 new IDs, and rig movement."""
from pathlib import Path
import json,hashlib,xml.etree.ElementTree as ET
import numpy as np
R=Path(__file__).resolve().parent;ART=R.parents[1];OUT=R/'candidate-props'
ns={'__file__':str(R/'scenes.py')}
for f in (ART/'skills/make/show-tell/templates/iso_kit.py',ART/'skills/make/show-tell/templates/iso_props_24.py',R/'props_25.py'):exec(f.read_text(),ns)
m=json.loads((OUT/'manifest.json').read_text());ids=[p['id'] for p in m['props']]
assert len(ids)==len(set(ids))==25
assert not set(ids)&set(ns['PROP_IDS'])
assert m['status']=='candidate-review'
for p in m['props']:
 for rel,key in [('references/'+p['id']+'.svg','reference_sha256'),(p['svg'],'adapted_sha256')]:
  assert hashlib.sha256((OUT/rel).read_bytes()).hexdigest()==p[key],(p['id'],key)
 svg=ET.parse(OUT/p['svg']).getroot()
 assert not svg.findall('.//{http://www.w3.org/2000/svg}image')
 layers=[g.attrib['id'] for g in svg.findall('{http://www.w3.org/2000/svg}g')]
 assert layers==p['parts'],p['id']
 g=ns['make_candidate'](p['id']);assert g.width<4.5 and g.height<4.5
 part=next(iter(g.parts.values()));before=np.array(part.get_center());part.shift(np.array([.3,.2,0]))
 assert np.allclose(np.array(part.get_center())-before,[.3,.2,0])
print('PASS: 25 distinct new candidate IDs; hashes; named SVG layers; native vectors; movable parts; bounds.')
