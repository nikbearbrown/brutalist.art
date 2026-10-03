"""Make a portable review pack, without installing any shared skill assets."""
from pathlib import Path
import shutil,zipfile
R=Path(__file__).resolve().parent;ART=R.parents[1];OUT=R/'candidate-props'
templates=OUT/'templates';templates.mkdir(exist_ok=True)
for name in ('iso_kit.py','iso_props_24.py'):
 shutil.copy2(ART/'skills/make/show-tell/templates'/name,templates/name)
shutil.copy2(R/'props_25.py',templates/'props_25.py')
dest=R/'show-tell-candidate-props-25-49.zip'
with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED) as z:
 for f in sorted(OUT.rglob('*')):
  if f.is_file() and 'previews' not in f.parts:z.write(f,Path('candidate-props-25-49')/f.relative_to(OUT))
with zipfile.ZipFile(dest) as z:
 assert z.testzip() is None
 assert sum('/svg/' in n and n.endswith('.svg') for n in z.namelist())==25
print(dest,dest.stat().st_size,'bytes; 25 SVGs; CRC pass')
