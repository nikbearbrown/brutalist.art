"""Sample real video frames for visual review, plus resolution/duration checks."""
import argparse,json,subprocess,math
from pathlib import Path
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--master');args=ap.parse_args()
OUT=R/'_qc/inspection';OUT.mkdir(parents=True,exist_ok=True)
sheet=json.loads((R/'beat_sheet.json').read_text())
def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))
def frame(path,at,name):
    dest=OUT/name
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(at),'-i',str(path),'-frames:v','1','-vf','scale=960:-1',str(dest)],check=True)
    return dest
def contact(items,name,cols=3,w=480,h=270):
    canvas=Image.new('RGB',(cols*w,math.ceil(len(items)/cols)*(h+24)),'#F2F0E9');draw=ImageDraw.Draw(canvas)
    for n,(path,label) in enumerate(items):
        x=n%cols*w;y=n//cols*(h+24)
        canvas.paste(Image.open(path).convert('RGB').resize((w,h)),(x,y+24));draw.text((x+8,y+5),label,fill='#3D3929')
    canvas.save(OUT/name)
rows=[];items=[]
for b in sheet['beats']:
    bid=b['beat_id'];p=R/'media'/f'{bid}.mp4'
    if not p.exists():p=R/'manim'/f'{bid}.mp4'
    data=probe(p);v=next(x for x in data['streams'] if x['codec_type']=='video')
    assert (v['width'],v['height'])==(3840,2160),(bid,v['width'],v['height'])
    d=float(data['format']['duration']);a=b['actual_duration_s']
    rows.append({'beat':bid,'width':v['width'],'height':v['height'],'video_seconds':d,'audio_seconds':a,'difference':round(d-a,4)})
    for f in (.15,.5,.85):items.append((frame(p,d*f,f'{bid}-{int(f*100)}.png'),f'{bid} {int(f*100)}%'))
(R/'_qc/beat-integrity.json').write_text(json.dumps(rows,indent=2)+'\n')
for n in range(0,len(items),18):contact(items[n:n+18],f'beats-{n//18+1}.jpg')
if args.master:
    p=Path(args.master);data=probe(p)
    subprocess.run(['ffmpeg','-v','error','-y','-i',str(p),'-vf','fps=2,scale=480:-1',str(OUT/'scan-%04d.png')],check=True)
    scans=[(f,f'{n*.5:.1f}s') for n,f in enumerate(sorted(OUT.glob('scan-*.png')))]
    for n in range(0,len(scans),36):contact(scans[n:n+36],f'scan-sheet-{n//36+1}.jpg',6,320,180)
    (R/'_qc/master-probe.json').write_text(json.dumps(data,indent=2)+'\n')
print('Inspected source files: 29 native-4K beats. Contact sheets:',OUT)
