"""Original Show-Tell props. No third-party icon geometry or images.

Geometry follows the house Iso projection and exact iso_kit.py face colors.
Run: python3 icons/show-tell-originals/build.py
"""
from pathlib import Path
import math, json, html, hashlib, zipfile
import xml.etree.ElementTree as ET
import cairosvg
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
STAGE, INK, TERRA = '#F2F0E9', '#3D3929', '#D97757'
KRAFT = ('#F3E9D8', '#DCC9AA', '#C7AE86')
DARK = ('#3A3530', '#26221F', '#1E1B18')
PAPER = ('#FFFFFF', '#ECE7DF', '#E2DCD2')
GREY = ('#D9D4C7', '#B4AFA6', '#8B8F96')

def project(q):
    x,y,z = q
    return ((x-y)*math.sqrt(3)/2, -(x+y)*.5-z)

class Prop:
    def __init__(self, name, action):
        self.name, self.action, self.parts = name, action, {}
        self.moves = {}
    def poly(self, part, pts, fill, stroke=INK, width=.035):
        self.parts.setdefault(part, []).append(dict(kind='polygon', pts=[project(q) for q in pts], fill=fill, stroke=stroke, width=width))
    def line(self, part, pts, color='#8B8F96', width=.045):
        self.parts.setdefault(part, []).append(dict(kind='polyline', pts=[project(q) for q in pts], fill='none', stroke=color, width=width))
    def dot(self, part, q, r=.07, color=TERRA):
        x,y=project(q)
        self.parts.setdefault(part, []).append(dict(kind='circle', cx=x, cy=y, r=r, fill=color, stroke='none', width=0))
    def box(self, part, x,y,z,w,d,h, colors=KRAFT):
        top,left,right=colors; X,Y,Z=x+w,y+d,z+h
        self.poly(part,[(x,y,z),(x,Y,z),(x,Y,Z),(x,y,Z)],left)
        self.poly(part,[(x,y,z),(X,y,z),(X,y,Z),(x,y,Z)],right)
        self.poly(part,[(x,y,Z),(X,y,Z),(X,Y,Z),(x,Y,Z)],top)
    def page(self, part,x,y,z,w=1.5,d=1.8):
        self.box(part,x,y,z,w,d,.07,PAPER)
        for t in [.35,.65,.95]:
            self.line(part,[(x+.2,y+t,z+.075),(x+w-.2,y+t,z+.075)],'#D9D4C7',.04)
        self.dot(part,(x+.23,y+d-.27,z+.08),.055)
    def tray_back(self,part,x,y,z,w,d,h):
        self.box(part,x,y,z,w,d,.13)
        self.box(part,x+w-.12,y,z,.12,d,h)
        self.box(part,x,y+d-.12,z,w,.12,h)
    def tray_front(self,part,x,y,z,w,d,h):
        self.box(part,x,y,z,.12,d,h)
        self.box(part,x,y,z,w,.12,h)
    def move(self,part,delta):
        self.moves[part]=project(delta)

def make_props():
    out=[]
    def new(name,action):
        p=Prop(name,action);out.append(p);return p
    p=new('Context crate','Lift the lid; reveal the contents.')
    p.tray_back('crate-back',0,0,0,2.6,2.4,1.1)
    p.page('context',.4,.4,.2,1.7,1.5)
    p.tray_front('crate-front',0,0,0,2.6,2.4,1.1)
    p.box('lid',-.06,-.06,1.16,2.72,2.52,.18)
    p.line('lid',[(1.3,0,1.35),(1.3,2.4,1.35)],'#8B8F96',.18)
    p.move('lid',(0,0,1.0))

    p=new('Skill stack','Pull one instruction page from the stack.')
    for i in range(3):p.page('pages',.12*i,.09*i,.14*i,2,2.4)
    p.page('selected-page',.36,.27,.5,2,2.4);p.move('selected-page',(1.1,0,.6))

    p=new('Tool block','Remove the tool cartridge from its dock.')
    p.box('dock',-.2,-.2,0,2.6,2.3,.2,GREY)
    p.box('tool',0,0,.23,2.2,1.9,1.15,DARK)
    for x in [.35,1.25]:p.box('tool',x,-.16,.55,.45,.17,.3,GREY)
    p.dot('tool',(1.85,.5,1.39));p.move('tool',(0,0,.9))

    p=new('Connector pair','Move the plug into the receiving socket.')
    p.box('socket',1.3,.4,0,1.5,1.6,.8,DARK)
    p.box('socket',1.7,.18,.23,.65,.23,.3,GREY)
    p.box('plug',1.15,-.65,.16,.8,.5,.45,DARK)
    for x in [1.28,1.65]:p.box('plug',x,-.13,.26,.13,.3,.13,GREY)
    p.move('plug',(.42,.32,0))

    p=new('Server tower','Lift one node out of the stack.')
    for i in range(3):
        part='node' if i==2 else 'rack'
        p.box(part,0,0,i*.65,2,1.9,.52,DARK)
        p.dot(part,(.3,-.02,i*.65+.25),.06,TERRA if i==2 else '#D9D4C7')
        p.line(part,[(.7,-.015,i*.65+.25),(1.6,-.015,i*.65+.25)],'#8B8F96',.06)
    p.move('node',(0,0,.65))

    p=new('Memory drawers','Open a drawer to retrieve a saved record.')
    p.box('cabinet',0,0,0,2,1.6,2)
    for i in range(3):
        part='drawer' if i==1 else f'fixed-drawer-{i}'
        p.box(part,.13,-.1,.15+i*.6,1.74,1.3,.46,GREY)
        p.box(part,.65,-.24,.31+i*.6,.65,.15,.09,DARK)
    p.box('cabinet-top',0,0,1.96,2,1.6,.12,KRAFT)
    p.move('drawer',(0,-.9,0))

    p=new('Context inbox','Lift the newest page out of the tray.')
    p.tray_back('tray-back',0,0,0,2.6,2.6,.45)
    p.page('records',.3,.3,.17,2,2)
    p.page('new-page',.3,.3,.34,2,2)
    p.tray_front('tray-front',0,0,0,2.6,2.6,.45)
    p.move('new-page',(0,0,1.1))

    p=new('Agent workstation','Pull a tool block beside the work surface.')
    p.box('foot',.4,.6,0,1.9,1.1,.15,GREY)
    p.box('stand',1.1,1,.16,.3,.3,.6,DARK)
    p.box('screen',0,1,.76,2.7,.2,1.65,DARK)
    p.poly('screen',[(.14,.99,.94),(2.56,.99,.94),(2.56,.99,2.25),(.14,.99,2.25)],'#FAF9F5')
    for z in [1.2,1.5,1.8]:p.line('screen',[(.4,.97,z),(1.8,.97,z)],'#8B8F96',.06)
    p.box('tool',2.7,-.3,0,.85,.8,.55,DARK);p.dot('tool',(3.1,-.32,.28))
    p.move('tool',(-.85,-.3,0))

    p=new('Review desk','Slide the evidence onto the reviewer’s desk.')
    for x,y in [(0,0),(2.5,0),(0,1.65),(2.5,1.65)]:p.box('legs',x,y,0,.16,.16,1.2,DARK)
    p.box('desktop',-.1,-.1,1.2,2.9,2,.16)
    p.page('evidence',.55,.1,1.4,1.5,1.5)
    p.move('evidence',(.3,-1,.15))

    p=new('Permission gate','Raise the barrier before work proceeds.')
    p.box('base',-.1,-.1,0,3.1,1.5,.13,GREY)
    for x in [0,2.5]:p.box('posts',x,.6,.13,.28,.35,1.7,DARK)
    p.box('barrier',.2,.48,1,2.3,.16,.27)
    p.dot('posts',(.14,.58,1.6));p.move('barrier',(0,0,.95))

    p=new('Approval stamp','Press the stamp onto the document.')
    p.page('document',0,0,0,2.3,2.5)
    p.box('stamp',.65,.65,.6,1.1,1.1,.2,DARK)
    p.box('stamp',1.05,1.05,.8,.3,.3,.6)
    p.box('stamp',.75,.75,1.4,.9,.9,.17)
    p.move('stamp',(0,0,-.5))

    p=new('Secure vault','Slide the locking bar away from the door.')
    p.box('body',0,0,0,2.3,1.8,2,DARK)
    p.box('door',.17,-.12,.18,1.96,.15,1.64,GREY)
    p.box('lock-bar',.35,-.3,.9,1.6,.18,.18,KRAFT)
    p.box('lock-bar',1.4,-.36,.72,.2,.18,.55,DARK)
    p.move('lock-bar',(.65,0,0))

    p=new('Conveyor','Carry the parcel along the conveyor.')
    p.box('frame',0,0,0,4,1.5,.4,DARK)
    for i in range(8):p.box('rollers',.13+i*.48,.07,.4,.3,1.36,.08,GREY)
    p.box('parcel',.45,.24,.53,1,1,.75)
    p.dot('parcel',(.92,.7,1.3),.07);p.move('parcel',(1.8,0,0))

    p=new('Branch junction','Move a work packet onto one of two routes.')
    p.box('inbound',0,0,0,1.3,1.1,.15,GREY)
    p.box('route-a',1.5,0,0,1.8,.45,.15,GREY)
    p.box('route-b',1.5,.8,0,.45,1.8,.15,GREY)
    p.box('packet',.15,.22,.2,.7,.65,.45,DARK)
    p.move('packet',(1.85,-.1,0))

    p=new('Checkpoint scanner','Move a parcel through the inspection arch.')
    p.box('track',-.1,-.4,0,2.9,2.3,.15,GREY)
    p.box('arch',2.3,.65,.15,.3,.45,2,DARK)
    p.box('arch',0,.65,2.15,2.6,.45,.25,DARK)
    p.dot('arch',(1.3,.63,2.26),.07)
    p.box('parcel',.7,-.3,.2,1.1,1.1,.7)
    p.box('near-post',0,.65,.15,.3,.45,2,DARK)
    p.move('parcel',(0,1.25,0))

    p=new('Evidence binder','Lift the cover to inspect the records.')
    p.box('back-cover',0,0,0,2.4,2.8,.12,DARK)
    for i in range(3):p.page('records',.25,.15,.14+i*.12,1.95,2.45)
    p.box('spine',0,0,.12,.18,2.8,.65,DARK)
    p.box('cover',.19,0,.58,2.2,2.8,.12,KRAFT)
    p.move('cover',(0,0,.9))

    p=new('Inspection lamp','Bring the light head closer to the evidence.')
    p.box('base',.1,.1,0,1,1,.18,DARK)
    p.box('upright',.43,.43,.18,.2,.2,2.1,GREY)
    p.box('lamp-head',.43,.43,2.28,1.7,.2,.16,GREY)
    p.box('lamp-head',1.75,.17,1.9,.85,.75,.43,DARK)
    p.poly('lamp-head',[(1.85,.16,1.95),(2.48,.16,1.95),(2.48,.16,2.08),(1.85,.16,2.08)],'#FFFFFF','none')
    p.page('evidence',1.35,-.1,.02,1.5,1.6)
    p.move('lamp-head',(0,0,-.5))

    p=new('Experiment bench','Place a test sample in the fixture.')
    p.box('base',0,0,0,3,2.2,.25,GREY)
    for x in [.2,2.5]:p.box('fixture',x,.5,.25,.25,1.1,.9,DARK)
    p.box('sample',1.1,.7,.3,.75,.75,.7)
    p.box('control',.3,-.15,.4,.65,.3,.45,DARK);p.dot('control',(.63,-.17,.63))
    p.move('sample',(0,0,1))

    p=new('Version shelves','Pull the selected version from its shelf.')
    p.box('back',0,1.8,0,2.8,.15,2.2,KRAFT)
    for x in [0,2.65]:p.box('supports',x,.1,0,.15,.15,2.1,DARK)
    for z in [.05,.75,1.45]:p.box('shelves',0,0,z,2.8,1.9,.1,GREY)
    for i in range(3):
        name='selected-version' if i==1 else 'versions'
        p.page(name,.35,.15,.2+i*.7,2,1.5)
    p.move('selected-version',(0,-1,.2))

    p=new('Comparison trays','Lift one sample to compare two alternatives.')
    for x in [0,2.1]:
        p.tray_back('trays',x,0,0,1.8,1.9,.35)
        p.box('sample-b' if x else 'sample-a',x+.4,.45,.2,.9,.9,.6,DARK if x else KRAFT)
        p.tray_front('rims',x,0,0,1.8,1.9,.35)
    p.move('sample-b',(0,0,.9))

    p=new('Human handoff','Transfer a work packet across a shared counter.')
    p.box('counter',0,0,0,3.7,1.9,.22,KRAFT)
    p.box('human-side',.2,1.1,.24,.75,.55,.55,GREY)
    p.box('agent-side',2.7,1.1,.24,.75,.55,.55,DARK)
    p.dot('agent-side',(3.08,1.08,.54))
    p.page('packet',.3,.1,.27,1.05,.8);p.move('packet',(2.05,0,0))

    p=new('Task queue','Pull the first work item out of the queue.')
    p.box('rail',0,0,0,3.6,1.5,.15,GREY)
    for i in range(3):
        part='next-task' if i==0 else 'waiting-tasks'
        p.box(part,.2+i*1.12,.2,.2,.85,1.05,.9,KRAFT)
        p.page(part,.28+i*1.12,.32,1.11,.66,.78)
    p.move('next-task',(-.75,-.6,.35))

    p=new('Budget slots','Lift one token from a finite set of slots.')
    p.box('tray',0,0,0,3.6,1.8,.3,DARK)
    for i in range(4):
        part='allocated-token' if i==3 else 'available-tokens'
        p.box(part,.15+i*.85,.27,.31,.65,1.25,.25,KRAFT)
    p.move('allocated-token',(.3,0,.85))

    p=new('Recovery dock','Return a removed module to its docking rails.')
    p.box('base',0,0,0,2.8,2.4,.15,GREY)
    for x in [.25,2.15]:p.box('rails',x,.2,.15,.3,2,.25,DARK)
    p.box('module',.65,.45,1.1,1.4,1.5,.6,KRAFT)
    p.dot('module',(1.35,.43,1.4));p.move('module',(0,0,-.68))

    p=new('Release parcel','Separate the lid from a packaged delivery.')
    p.box('package',0,0,0,2.5,2.4,1.25,KRAFT)
    p.box('lid',-.07,-.07,1.3,2.64,2.54,.2,KRAFT)
    p.line('lid',[(1.25,0,1.51),(1.25,2.4,1.51)],'#8B8F96',.22)
    p.dot('lid',(1.25,1.1,1.53),.1)
    p.page('packing-slip',2.8,.15,.03,1,1.3)
    p.move('lid',(0,0,.8))
    return out

def bounds(p):
    pts=[]
    for name, shapes in p.parts.items():
        dx,dy=p.moves.get(name,(0,0))
        for shape in shapes:
            q=shape.get('pts') or [(shape['cx']-shape['r'],shape['cy']-shape['r']),(shape['cx']+shape['r'],shape['cy']+shape['r'])]
            pts.extend(q);pts.extend((x+dx,y+dy) for x,y in q)
    return min(x for x,y in pts),min(y for x,y in pts),max(x for x,y in pts),max(y for x,y in pts)

def svg(p,state=0):
    x0,y0,x1,y1=bounds(p);scale=min(490/(x1-x0),490/(y1-y0),110)
    tx,ty=320-(x0+x1)*scale/2,320-(y0+y1)*scale/2
    bits=[f'<svg xmlns="http://www.w3.org/2000/svg" width="640" height="640" viewBox="0 0 640 640"><title>{html.escape(p.name)}</title><desc>{html.escape(p.action)} Original geometry in the Show-Tell house style.</desc><g transform="translate({tx} {ty}) scale({scale})" stroke-linejoin="round" stroke-linecap="round">']
    for name,shapes in p.parts.items():
        dx,dy=p.moves.get(name,(0,0));bits.append(f'<g id="{name}" data-dx="{dx}" data-dy="{dy}" transform="translate({dx*state} {dy*state})">')
        for s in shapes:
            attrs=f'fill="{s["fill"]}" stroke="{s["stroke"]}" stroke-width="{s["width"]}"'
            if s['kind']=='circle':bits.append(f'<circle cx="{s["cx"]}" cy="{s["cy"]}" r="{s["r"]}" {attrs}/>')
            else:
                points=' '.join(f'{x:.5f},{y:.5f}' for x,y in s['pts'])
                bits.append(f'<{s["kind"]} points="{points}" {attrs}/>')
        bits.append('</g>')
    return ''.join(bits)+'</g></svg>'

def main():
    props=make_props();assert len(props)==25
    for folder in ['svg','action-svg','png']: (ROOT/folder).mkdir(exist_ok=True)
    sheet=Image.new('RGB',(2000,2250),STAGE);draw=ImageDraw.Draw(sheet)
    action_sheet=Image.new('RGB',(2000,2250),STAGE);action_draw=ImageDraw.Draw(action_sheet)
    font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Georgia.ttf',23)
    small=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',17)
    manifest=[];cards=[]
    for i,p in enumerate(props):
        slug=p.name.lower().replace(' ','-');assert p.moves and all(k in p.parts for k in p.moves)
        raw=svg(p);ET.fromstring(raw)
        (ROOT/'svg'/f'{slug}.svg').write_text(raw)
        (ROOT/'action-svg'/f'{slug}.svg').write_text(svg(p,1))
        cairosvg.svg2png(bytestring=raw.encode(),write_to=str(ROOT/'png'/f'{slug}.png'),output_width=640,output_height=640)
        preview=Image.open(ROOT/'png'/f'{slug}.png').convert('RGBA').resize((380,380))
        x,y=(i%5)*400,(i//5)*450;sheet.paste(preview,(x+10,y),preview)
        draw.text((x+18,y+380),f'{i+1:02}  {p.name}',font=font,fill=INK)
        draw.text((x+18,y+416),' / '.join(p.moves),font=small,fill=INK)
        action_raw=svg(p,1)
        cairosvg.svg2png(bytestring=action_raw.encode(),write_to=str(ROOT/'png'/f'{slug}-action.png'),output_width=640,output_height=640)
        preview_action=Image.open(ROOT/'png'/f'{slug}-action.png').convert('RGBA').resize((380,380))
        action_sheet.paste(preview_action,(x+10,y),preview_action)
        action_draw.text((x+18,y+380),f'{i+1:02}  {p.name}',font=font,fill=INK)
        action_draw.text((x+18,y+416),' / '.join(p.moves),font=small,fill=INK)
        manifest.append(dict(id=slug,name=p.name,action=p.action,parts=p.parts,moves=p.moves,sha256=hashlib.sha256(raw.encode()).hexdigest()))
        cards.append(f'<article><div class="drawing">{raw}</div><h2>{i+1:02} {p.name}</h2><p>{html.escape(p.action)}</p><button type="button" aria-pressed="false">Show action</button><a href="svg/{slug}.svg" download>SVG</a></article>')
    sheet.save(ROOT/'contact-sheet.png')
    action_sheet.save(ROOT/'action-contact-sheet.png')
    (ROOT/'manifest.json').write_text(json.dumps(dict(status='original-candidates',source='Original procedural geometry; house iso_kit.py projection and palette only. No Isocons source.',props=manifest),indent=2)+'\n')
    page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Original Show-Tell Props</title><style>
    *{box-sizing:border-box}body{margin:0;background:#F2F0E9;color:#3D3929;font:18px Georgia,serif}header{padding:40px;max-width:1100px}h1{font-size:42px;margin:0 0 16px}header p{line-height:1.5}main{padding:0 30px 40px;display:grid;grid-template-columns:repeat(auto-fit,minmax(290px,1fr));gap:22px}article{border:1px solid #D9D4C7;padding:16px;background:#FAF9F5}.drawing svg{width:100%;height:auto}h2{font-size:23px;margin:0 0 12px}p{min-height:48px;font-size:17px}button,a{font:16px Arial;color:#3D3929}button{background:#F3E9D8;border:1px solid #3D3929;padding:10px;cursor:pointer;margin-right:20px}button:focus-visible,a:focus-visible{outline:3px solid #D97757;outline-offset:4px}svg g[data-dx]{transition:transform .8s ease-in-out}@media(prefers-reduced-motion:reduce){svg g[data-dx]{transition:none}}
    </style><header><h1>Original Show-Tell props</h1><p>25 physical objects drawn from scratch using the house projection, kraft faces, warm ink, dark hardware, white pages and small terracotta signals. No borrowed icon silhouettes. Each button demonstrates a named part—not a generic whole-icon bounce.</p><p>Candidate set for review. No existing films or libraries have been overwritten.</p></header><main>'''+''.join(cards)+'''</main><script>document.querySelectorAll('button').forEach(b=>b.onclick=()=>{const on=b.getAttribute('aria-pressed')!=='true';b.setAttribute('aria-pressed',String(on));b.textContent=on?'Reset':'Show action';b.closest('article').querySelectorAll('g[data-dx]').forEach(g=>g.setAttribute('transform',`translate(${on?g.dataset.dx:0} ${on?g.dataset.dy:0})`))});</script></html>'''
    (ROOT/'index.html').write_text(page)
    print('Built 25 original props: SVGs, action states, transparent PNGs, manifest and interactive catalog.')

if __name__=='__main__':main()
