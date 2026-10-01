"""Check promoted assets and exercise the template with no companion files."""
from pathlib import Path
import json, hashlib, tempfile, subprocess, sys, shutil
import xml.etree.ElementTree as ET

root=Path(__file__).resolve().parents[1]
assets=root/'assets/originals-25'
manifest=json.loads((assets/'manifest.json').read_text())
assert manifest['status']=='approved-for-show-tell'
assert len(manifest['props'])==25
for p in manifest['props']:
    raw=(assets/'svg'/f'{p["id"]}.svg').read_bytes()
    assert hashlib.sha256(raw).hexdigest()==p['sha256']
    svg=ET.fromstring(raw)
    assert not svg.findall('.//{*}image')
    assert set(p['parts'])=={g.attrib['id'] for g in svg.findall('.//{*}g') if 'id' in g.attrib}
with tempfile.TemporaryDirectory(prefix='show-tell-originals-test-') as scratch:
    shutil.copy2(root/'templates/iso_originals_25.py',Path(scratch)/'scenes.py')
    code='''
import runpy, numpy as np
ns=runpy.run_path('scenes.py')
for name, spec in ns['_ST_ORIGINALS_25'].items():
    for height in [1.6,3.2]:
        rig=ns['make_original'](name,height=height,x=.4,y=-.2)
        assert set(rig.parts)==set(spec['parts'])
        assert rig.width<5 and rig.height<3.3
        for part, vector in rig.action_vectors.items():
            before=rig.parts[part].get_center().copy()
            rig.parts[part].shift(vector)
            assert np.linalg.norm(rig.parts[part].get_center()-before)>.05
        assert rig.width<5 and rig.height<3.3
print('PASS: 25 native rigs at two scales, isolated scenes.py, all actions and bounds.')
'''
    subprocess.run([sys.executable,'-c',code],cwd=scratch,check=True)
print('PASS: promoted SVG hashes, named groups, native geometry, approval metadata.')
