"""Native Manim adapter, not raster imports. Requires build.py beside this file.

For isolated Gate A scenes, paste build.py's geometry definitions (through
make_props) and this factory into scenes.py; omit export-only imports/main.
"""
def make_original(prop_id, height=3.2):
    from manim import VGroup, Polygon, VMobject, Circle
    from build import make_props, bounds
    import numpy as np
    props={p.name.lower().replace(' ','-'):p for p in make_props()}
    p=props[prop_id]
    x0,y0,x1,y1=bounds(p)
    scale=min(height/(y1-y0),4.8/(x1-x0))
    cx,cy=(x0+x1)/2,(y0+y1)/2
    def point(x,y):return np.array([(x-cx)*scale,-(y-cy)*scale,0])
    rig=VGroup();rig.parts={};rig.action_vectors={}
    for name,shapes in p.parts.items():
        part=VGroup()
        for s in shapes:
            if s['kind']=='circle':
                mob=Circle(radius=s['r']*scale).move_to(point(s['cx'],s['cy']))
            elif s['kind']=='polygon':
                mob=Polygon(*[point(x,y) for x,y in s['pts']])
            else:
                mob=VMobject().set_points_as_corners([point(x,y) for x,y in s['pts']])
            mob.set_fill(s['fill'] if s['fill']!='none' else '#FFFFFF',opacity=0 if s['fill']=='none' else 1)
            mob.set_stroke(s['stroke'] if s['stroke']!='none' else '#FFFFFF',width=s['width']*100,opacity=0 if s['stroke']=='none' else 1)
            part.add(mob)
        rig.parts[name]=part;rig.add(part)
        if name in p.moves:
            dx,dy=p.moves[name];rig.action_vectors[name]=np.array([dx*scale,-dy*scale,0])
    return rig
