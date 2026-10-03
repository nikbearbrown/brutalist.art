"""Export the candidate pack, with provenance and named editable SVG groups."""
from pathlib import Path
import json, hashlib, html, math, runpy
from PIL import Image,ImageDraw,ImageFont
import cairosvg
R=Path(__file__).resolve().parent;ART=R.parents[1];OUT=R/'candidate-props'
export=runpy.run_path(str(ART/'skills/make/show-tell/scripts/build_prop_assets.py'))['svg_part']
def main():
 manifest=json.loads((OUT/'manifest.json').read_text());adapt=(R/'props_25.py').exists()
 if adapt:
  ns={'__file__':str(R/'scenes.py')}
  for f in [ART/'skills/make/show-tell/templates/iso_kit.py',ART/'skills/make/show-tell/templates/iso_props_24.py',R/'props_25.py']:exec(f.read_text(),ns)
  (OUT/'svg').mkdir(exist_ok=True)
 (OUT/'previews').mkdir(exist_ok=True)
 font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Georgia.ttf',20)
 for variant in (('source','adapted') if adapt else ('source',)):
  sheet=Image.new('RGB',(1600,math.ceil(len(manifest['props'])/4)*335),'#F2F0E9');draw=ImageDraw.Draw(sheet)
  for n,r in enumerate(manifest['props']):
   if variant=='source':
    raw=(OUT/'references'/f'{r["id"]}.svg').read_text().replace('fill="none"','fill="#FAF9F5"',1).replace('stroke="black"','stroke="#3D3929"')
   else:
    prop=ns['make_candidate'](r['id']);assert prop.width<4.5 and prop.height<4.5,(r['id'],prop.width,prop.height)
    raw='<svg xmlns="http://www.w3.org/2000/svg" viewBox="-2.3 -2.3 4.6 4.6" width="640" height="640"><title>'+html.escape(r['source_name'])+'</title><metadata>Adapted from Isocons; CC BY 4.0. Geometry, palette and animation modified. Candidate for review.</metadata>'+''.join(export(k,g) for k,g in prop.parts.items())+'</svg>\n'
    target=OUT/'svg'/f'{r["id"]}.svg';target.write_text(raw)
    r.update(parts=list(prop.parts),svg='svg/'+r['id']+'.svg',adapted_sha256=hashlib.sha256(target.read_bytes()).hexdigest())
   preview=OUT/'previews'/f'{variant}-{r["id"]}.png'
   cairosvg.svg2png(bytestring=raw.encode(),write_to=str(preview),output_width=280,output_height=280,background_color='#F2F0E9')
   im=Image.open(preview).convert('RGB');x=n%4*400;y=n//4*335;sheet.paste(im,(x+60,y))
   draw.text((x+12,y+293),f'{n+25:02}  {r["source_name"]}',font=font,fill='#3D3929')
  sheet.save(OUT/f'{variant}-contact.png')
 if adapt:(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
if __name__=='__main__':main()
