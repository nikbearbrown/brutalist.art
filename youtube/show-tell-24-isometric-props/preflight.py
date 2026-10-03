"""Run the same isolated static checks as production, then last-frame previews."""
import json,subprocess,tempfile,shutil
from pathlib import Path
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent;ART=R.parents[1]
sheet=json.loads((R/'beat_sheet.json').read_text())
classes=[b['shot']['manim']['class'] for b in sheet['beats'] if 'manim' in b['shot']]
scratch=Path(tempfile.mkdtemp(prefix='show-tell-props-audit-'))
shutil.copy2(R/'scenes.py',scratch/'scenes.py')
for cls in classes:
    subprocess.run(['python3',str(ART/'runtime/qc/static_scene_check.py'),str(scratch/'scenes.py'),'--class',cls,'--quiet'],check=True)
    subprocess.run(['python3',str(ART/'runtime/qc/manim_layout_audit.py'),str(R/'scenes.py'),'--class',cls,'--curve-strict'],check=True)
media=R/'_qc/preview'
subprocess.run(['manim','-ql','-s','--media_dir',str(media),str(R/'scenes.py'),*classes],check=True)
images=sorted((media/'images/scenes').glob('*.png'))
for offset in range(0,len(images),9):
    group=images[offset:offset+9]
    canvas=Image.new('RGB',(1440,3*296),'#F2F0E9');d=ImageDraw.Draw(canvas)
    for n,f in enumerate(group):
        x=n%3*480;y=n//3*296
        im=Image.open(f).convert('RGB').resize((480,270));canvas.paste(im,(x,y+26));d.text((x+8,y+5),f.stem,fill='#3D3929')
    canvas.save(R/f'_qc/preview-{offset//9+1}.jpg')
print('Preflight and previews complete; scratch:',scratch)
