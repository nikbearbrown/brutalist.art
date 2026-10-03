"""Isocons-inspired Show-Tell props: simplified, layered, native-vector redraws.

Paste AFTER iso_kit.py into scenes.py. make_prop returns a VGroup with named
parts (prop.parts), not a baked image. Coordinates use the kit's projection.
Source and license: ../assets/isocons-24/ATTRIBUTION.md.
"""

PROP_IDS = (
    'dataset','dataset-linked','layers','quick-reference','terminal','linked-services',
    'deployed-code','network-node','person-raised-hand','person-check','handshake',
    'partner-exchange','policy','shield-lock','shield-question','vpn-key',
    'data-check-double','search-check-2','track-changes','receipt','account-tree',
    'arrow-split','rebase','conveyor-belt')

def _front(points, depth=.22, fill=BOX_TOP):
    """Extrude a front silhouette; named layers keep the prop editable."""
    iso=Iso()
    sides=VGroup(iso.quad([(x,depth,z) for x,z in points],BOX_R,sw=3))
    for a,b in zip(points,points[1:]+points[:1]):
        if a==b: continue
        sides.add(iso.quad([(a[0],0,a[1]),(b[0],0,b[1]),(b[0],depth,b[1]),(a[0],depth,a[1])],BOX_R,sw=0))
    face=iso.quad([(x,0,z) for x,z in points],fill,sw=4)
    return VGroup(sides,face)

def _ellipse_points(x,z,rx,rz,n=40):
    return [(x+rx*np.cos(t),z+rz*np.sin(t)) for t in np.linspace(0,2*np.pi,n,endpoint=False)]

def _front_line(points,color=DIM,sw=5):
    iso=Iso()
    return VMobject(stroke_color=color,stroke_width=sw).set_points_as_corners([iso.p(x,-.015,z) for x,z in points])

def _slip(x=0,y=0):
    """A recurring evidence slip; grey internals avoid fused ink outlines."""
    i=Iso()
    g=i.box(-.48,-.43,0,.96,.86,.08,sw=3)
    g.add(Line(i.p(-.27,-.1,.085),i.p(.27,-.1,.085),color=DIM,stroke_width=5))
    return g.move_to([x,y,0])

def _person(x=0):
    head=_front(_ellipse_points(x,.62,.27,.29),.16)
    torso=_front([(x-.47,-.7),(x+.47,-.7),(x+.39,.08),(x-.39,.08)],.2)
    return VGroup(torso,head)

def _shield():
    return _front([(-.85,.85),(0,1.1),(.85,.85),(.72,-.4),(0,-1.1),(-.72,-.4)],.25)

def make_prop(name, x=0, y=0, scale=1):
    """Create one of 24 props. Stable named parts support scene-specific actions.

    The caller animates parts; the factory performs no scene mutations.
    Large labels belong beside this object, never inside its silhouette.
    """
    if name not in PROP_IDS: raise ValueError(name)
    p={}; i=Iso()
    if name in ('dataset','dataset-linked'):
        p['body']=_front([(-.85,-.9),(.85,-.9),(.85,.9),(-.85,.9)])
        p['cells']=VGroup(*[_front([(a,b),(a+.38,b),(a+.38,b+.38),(a,b+.38)],.04,fill=BAR2)
            for a,b in [(-.57,-.52),(.15,-.52),(-.57,.19),(.15,.19)]])
        if name.endswith('linked'):
            p['link']=VGroup(*[RoundedRectangle(width=.65,height=.38,corner_radius=.15,stroke_color=INK,stroke_width=5)
                .rotate(-PI/6).move_to([a,-.95,0]) for a in (.55,.97)])
    elif name=='layers':
        for n in range(3): p['layer'+str(n)]=i.box(-.85,-.65,n*.45,1.7,1.3,.08,sw=3)
    elif name=='quick-reference':
        p['body']=_front([(-.75,-.95),(.65,-.95),(.9,-.7),(.9,.95),(-.75,.95)])
        p['lines']=VGroup(*[_front_line([(-.48,z),(.42,z)],sw=5) for z in (-.45,-.05,.35)])
        p['bookmark']=_front([(.55,.95),(.82,.95),(.82,.24),(.685,.38),(.55,.24)],.06,fill=BAR2)
    elif name=='terminal':
        p['body']=_front([(-1.1,-.7),(1.1,-.7),(1.1,.8),(-1.1,.8)],.25,fill=BAR2)
        p['prompt']=_front_line([(-.7,.42),(-.38,.15),(-.7,-.12)],color=INK,sw=7)
        p['cursor']=_front_line([(-.12,-.16),(.55,-.16)],color=INK,sw=7)
    elif name=='linked-services':
        p['left']=i.box(-1.6,0,0,.85,.85,.55,sw=3)
        p['right']=i.box(.65,0,0,.85,.85,.55,sw=3)
        p['connector']=Line(i.p(-.5,.25,.2),i.p(.5,.25,.2),color=DIM,stroke_width=9)
    elif name=='deployed-code':
        p['platform']=i.box(-1,-.75,-.45,2,1.5,.2,top=BAR2,left=BAR1,right=BAR1)
        p['package']=i.box(-.48,-.48,.1,.96,.96,.8)
        p['brackets']=VGroup(_front_line([(-.35,.63),(-.48,.5),(-.35,.37)],INK,4),
                              _front_line([(.15,.63),(.28,.5),(.15,.37)],INK,4))
    elif name=='network-node':
        positions=[(-1.1,-.4),(1.1,-.4),(0,1.05)]
        p['edges']=VGroup(*[Line([*positions[a],0],[*positions[b],0],color=DIM,stroke_width=5) for a,b in [(0,1),(0,2),(1,2)]])
        p['nodes']=VGroup(*[i.box(0,0,0,.45,.45,.4).move_to([a,b,0]) for a,b in positions])
    elif name in ('person-raised-hand','person-check'):
        p['person']=_person(-.2)
        if name.endswith('hand'):
            p['arm']=_front([(.15,-.05),(.5,-.05),(.87,.7),(.65,.82),(.38,.23)],.16)
            p['hand']=_front(_ellipse_points(.79,.93,.16,.23),.12)
        else: p['check']=check(.8,-.2,.27,color=INK,w=6)
    elif name=='handshake':
        p['left']=_front([(-1.5,-.32),(-.55,-.32),(.08,.04),(-.13,.36),(-.67,.17),(-1.5,.17)],.22)
        p['right']=_front([(1.5,.24),(.55,.24),(-.08,-.12),(.13,-.44),(.67,-.25),(1.5,-.25)],.22,fill=BOX_L)
    elif name=='partner-exchange':
        p['left']=_person(-1.25).scale(.7)
        p['right']=_person(1.25).scale(.7)
        p['handoff']=_slip(0,-.8).scale(.5)
    elif name=='policy':
        p['body']=_front([(-.75,-1),(.75,-1),(.75,1),(-.75,1)])
        p['rules']=VGroup(*[_front_line([(-.45,z),(.45,z)],sw=6) for z in (-.45,0,.45)])
        p['gate']=Line([1.1,-.85,0],[1.1,.9,0],color=INK,stroke_width=9)
    elif name in ('shield-lock','shield-question'):
        p['shield']=_shield()
        if name.endswith('lock'):
            p['shackle']=Arc(radius=.3,start_angle=0,angle=PI,stroke_color=INK,stroke_width=6).move_to([0,.38,0])
            p['lock']=RoundedRectangle(width=.7,height=.5,corner_radius=.05,fill_color=BAR1,fill_opacity=1,stroke_width=0).move_to([0,0,0])
        else:
            p['question']=_front_line([(-.28,.45),(-.12,.66),(.16,.64),(.31,.43),(.25,.2),(0,0),(0,-.13)],INK,6)
            p['dot']=Dot(i.p(0,-.02,-.38),radius=.08,color=INK)
    elif name=='vpn-key':
        p['bow']=VGroup(_front(_ellipse_points(-.68,.12,.44,.44),.17),
            _front(_ellipse_points(-.68,.12,.2,.2),.01,fill=STAGE))
        p['shaft']=_front([(-.28,-.01),(1,-.01),(1,-.38),(.73,-.38),(.73,-.23),(.43,-.23),(.43,.19),(-.28,.19)],.17)
    elif name=='data-check-double':
        p['records']=VGroup(i.box(0,0,0,.8,1,.08).move_to([-.95,0,0]),
                            i.box(0,0,0,.8,1,.08).move_to([.95,0,0]))
        p['checks']=VGroup(check(-.95,1,.22),check(.95,1,.22))
    elif name=='search-check-2':
        p['source']=i.box(-.8,-.7,0,1.6,1.4,.08)
        p['lens']=VGroup(Circle(radius=.51,stroke_color=INK,stroke_width=6),
                        Line([.35,-.35,0],[.82,-.82,0],color=INK,stroke_width=9)).move_to([.15,.7,0])
        p['check']=check(1.35,-.6,.22)
    elif name=='track-changes':
        p['before']=i.box(-1,-.8,0,1.5,1.5,.08)
        p['after']=i.box(-.15,-.2,.22,1.5,1.5,.08)
        p['revision']=Line(i.p(.12,.5,.32),i.p(.96,.5,.32),color=DIM,stroke_width=8)
    elif name=='receipt':
        p['paper']=_front([(-.7,1),(.7,1),(.7,-.8),(.42,-1),(.14,-.8),(-.14,-1),(-.42,-.8),(-.7,-1)],.12)
        for n,z in enumerate((.55,.1,-.35)):
            p['row'+str(n)]=_front_line([(-.4,z),(.4,z)],DIM,6)
    elif name=='account-tree':
        p['edges']=VGroup(Line([0,.7,0],[0,0,0],color=DIM,stroke_width=5),
            Line([-1,-.6,0],[-1,0,0],color=DIM,stroke_width=5),Line([1,-.6,0],[1,0,0],color=DIM,stroke_width=5),
            Line([-1,0,0],[1,0,0],color=DIM,stroke_width=5))
        p['nodes']=VGroup(*[i.box(0,0,0,.6,.45,.3).move_to([x,y,0]) for x,y in [(0,.95),(-1,-.75),(1,-.75)]])
    elif name=='arrow-split':
        p['stem']=_front([(-.13,-1),(.13,-1),(.13,-.13),(.75,.49),(.94,.3),(1.02,.94),(.38,.86),(.57,.67),(0,.1),(-.57,.67),(-.38,.86),(-1.02,.94),(-.94,.3),(-.75,.49),(-.13,-.13)],.2)
    elif name=='rebase':
        p['trunk']=Line([-.55,-1,0],[-.55,1,0],color=DIM,stroke_width=7)
        p['branch']=VGroup(Line([-.55,-.55,0],[.7,.2,0],color=DIM,stroke_width=6),
            Circle(radius=.18,fill_color=BOX_R,fill_opacity=1,stroke_color=INK,stroke_width=4).move_to([.7,.2,0]))
        p['commits']=VGroup(*[Circle(radius=.18,fill_color=BOX_TOP,fill_opacity=1,stroke_color=INK,stroke_width=4).move_to([-.55,z,0]) for z in (-.85,.2,.9)])
    elif name=='conveyor-belt':
        p['belt']=i.box(-1.55,-.45,-.15,3.1,.9,.18,top=BAR2,left=BAR1,right=BAR1)
        p['feet']=VGroup(*[i.box(a,-.15,-.75,.15,.2,.55,sw=3) for a in (-1.1,1.1)])
        p['cargo']=i.box(-.95,-.25,.13,.5,.5,.4)
    g=VGroup(*p.values())
    g.move_to([0,0,0]);g.scale(scale);g.move_to([x,y,0]);g.parts=p
    return g
