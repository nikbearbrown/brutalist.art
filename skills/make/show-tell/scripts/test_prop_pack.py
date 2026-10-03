"""Check actual asset invariants, not exact prose or implementation wording."""
from pathlib import Path
import hashlib,json,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1];PACK=ROOT/'assets/isocons-24'
manifest=json.loads((PACK/'manifest.json').read_text())
ns={'__file__':str(ROOT/'templates/iso_kit.py')}
exec((ROOT/'templates/iso_kit.py').read_text(),ns)
exec((ROOT/'templates/iso_props_24.py').read_text(),ns)
assert manifest['count']==len(manifest['props'])==len(ns['PROP_IDS'])==24
assert set(ns['PROP_IDS'])=={r['id'] for r in manifest['props']}
assert len({r['adapted_sha256'] for r in manifest['props']})==24
for r in manifest['props']:
    target=PACK/r['svg'];xml=ET.parse(target)
    assert hashlib.sha256(target.read_bytes()).hexdigest()==r['adapted_sha256']
    assert hashlib.sha256((PACK/'references'/f'{r["id"]}.svg').read_bytes()).hexdigest()==r['reference_sha256']
    assert not xml.findall('.//{http://www.w3.org/2000/svg}image')
    groups=xml.findall('./{http://www.w3.org/2000/svg}g')
    assert {g.get('id') for g in groups}==set(r['parts'])
    prop=ns['make_prop'](r['id'])
    assert 0<prop.width<4.5 and 0<prop.height<4.5
    part=next(iter(prop.parts.values()));before=part.get_center().copy()
    part.shift(ns['RIGHT']*.25)
    assert abs(part.get_center()[0]-before[0]-.25)<1e-6
print('PASS: 24 unique vector props; original/adapted hashes; named SVG layers; usable movable Manim parts; bounds; no embedded raster assets.')
