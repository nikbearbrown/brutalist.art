"""Export editable, named-layer SVGs and inspectable contact sheets from the rig."""
from pathlib import Path
import json, hashlib, html
from PIL import Image, ImageDraw, ImageFont
import cairosvg

ROOT=Path(__file__).resolve().parents[1]
ns={'__file__':str(ROOT/'templates/iso_kit.py')}
exec((ROOT/'templates/iso_kit.py').read_text(),ns)
exec((ROOT/'templates/iso_props_24.py').read_text(),ns)
OUT=ROOT/'assets/isocons-24'

def svg_part(name,group):
    paths=[]
    for m in group.family_members_with_points():
        curves=m.get_cubic_bezier_tuples()
        if len(curves)==0:continue
        d=[];last=None
        for c in curves:
            if last is None or sum((c[0]-last)**2)>1e-10:
                d.append(f'M {c[0][0]:.5f} {-c[0][1]:.5f}')
            d.append('C '+' '.join(f'{q[0]:.5f} {-q[1]:.5f}' for q in c[1:]))
            last=c[-1]
        paths.append(f'<path d="{" ".join(d)}" fill="{m.get_fill_color().to_hex()}" fill-opacity="{m.get_fill_opacity()}" stroke="{m.get_stroke_color().to_hex()}" stroke-width="{float(m.get_stroke_width())*.008}" stroke-opacity="{m.get_stroke_opacity()}" stroke-linejoin="round" stroke-linecap="round"/>')
    return f'<g id="{name}">{"".join(paths)}</g>'

def main():
    manifest=json.loads((OUT/'manifest.json').read_text())
    (OUT/'svg').mkdir(exist_ok=True);(OUT/'previews').mkdir(exist_ok=True)
    for r in manifest['props']:
        prop=ns['make_prop'](r['id'])
        assert len(prop.parts)>=1
        assert prop.width<4.5 and prop.height<4.5,(r['id'],prop.width,prop.height)
        body=''.join(svg_part(n,g) for n,g in prop.parts.items())
        svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-2.3 -2.3 4.6 4.6" width="640" height="640"><title>{html.escape(r["source_name"])}</title><metadata>Adapted and simplified from Isocons, https://www.isocons.app/ ; CC BY 4.0 https://creativecommons.org/licenses/by/4.0/ . Geometry, colors, strokes and rig modified.</metadata>{body}</svg>'
        target=OUT/'svg'/f'{r["id"]}.svg';target.write_text(svg+'\n')
        cairosvg.svg2png(bytestring=svg.encode(),write_to=str(OUT/'previews'/f'{r["id"]}.png'),background_color='#F2F0E9')
        r['parts']=list(prop.parts);r['svg']='svg/'+r['id']+'.svg';r['adapted_sha256']=hashlib.sha256(target.read_bytes()).hexdigest()
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Georgia.ttf',24)
    for variant in ('adapted','source'):
        sheet=Image.new('RGB',(1600,6*335),'#F2F0E9');draw=ImageDraw.Draw(sheet)
        for n,r in enumerate(manifest['props']):
            if variant=='source':
                raw=(OUT/'references'/f'{r["id"]}.svg').read_text().replace('fill="none"','fill="#FAF9F5"',1)
                raw=raw.replace('stroke="black"','stroke="#3D3929"')
                preview=OUT/'previews'/f'source-{r["id"]}.png'
                cairosvg.svg2png(bytestring=raw.encode(),write_to=str(preview),output_width=260,output_height=260,background_color='#F2F0E9')
            else:preview=OUT/'previews'/f'{r["id"]}.png'
            im=Image.open(preview).convert('RGB');im.thumbnail((290,290))
            x=(n%4)*400;y=(n//4)*335
            sheet.paste(im,(x+(400-im.width)//2,y))
            draw.text((x+16,y+293),f'{n+1:02}  {r["source_name"]}',font=font,fill='#3D3929')
        sheet.save(OUT/f'{variant}-contact.png')
    print('24 SVGs, named parts, SHA-256 manifest, source and adapted contact sheets.')

if __name__=='__main__':main()
