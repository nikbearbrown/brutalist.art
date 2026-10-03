"""Structural, source, bounds, transparency and native-rig checks."""
from pathlib import Path
import json, hashlib, xml.etree.ElementTree as ET
import numpy as np
from PIL import Image
from build import make_props, bounds, svg
from manim_props import make_original

root=Path(__file__).resolve().parent
manifest=json.loads((root/'manifest.json').read_text())
props=make_props();assert len(props)==25
assert len({p.name for p in props})==25
for p,record in zip(props,manifest['props']):
    slug=record['id'];raw=(root/'svg'/f'{slug}.svg').read_bytes()
    assert hashlib.sha256(raw).hexdigest()==record['sha256']
    tree=ET.fromstring(raw)
    assert not tree.findall('.//{*}image') and not tree.findall('.//{*}text')
    groups={e.attrib['id'] for e in tree.findall('.//{*}g') if 'id' in e.attrib}
    assert groups==set(p.parts)
    assert set(p.moves)<=groups
    assert svg(p)!=svg(p,1)
    im=Image.open(root/'png'/f'{slug}.png')
    assert im.mode=='RGBA' and im.getpixel((0,0))[3]==0
    assert all(np.isfinite(bounds(p)))
    rig=make_original(slug)
    assert rig.width<5 and rig.height<3.3
    for name,vector in rig.action_vectors.items():
        before=rig.parts[name].get_center().copy()
        rig.parts[name].shift(vector)
        assert np.linalg.norm(rig.parts[name].get_center()-before)>.1
    assert rig.width<5 and rig.height<3.3
print('PASS: 25 unique original props; SVG groups, hashes, transparency, finite geometry, native Manim parts and action bounds.')
