"""
iso_kit.py — the show-tell drawing kit. PASTE this block at the top of a reel's scenes.py;
do not import it (Gate A copies only scenes.py into its sandbox).

Drawn isometric objects in the Claude palette: cardboard boxes (closed, open, taped), dark
MCP blocks with ports, flat skill pages, server stacks with lights, checks, a cursor, pills.
Pacing helpers read the reel's beat_sheet.json so scenes wait for their spoken phrase.

Every rule in ../SKILL.md "DRAWING LAWS" is already obeyed by these primitives; keep it that
way when you add one (label beside, never inside; terracotta never under text; dim greys
with gaps for chart blocks; type floor 32).
"""
from manim import *
import numpy as np
import json as _json, os as _os

# ═════════════════════════════ ISO KIT (show-tell) ═════════════════════════════
STAGE = "#F2F0E9"; INK = "#3D3929"; TERRA = "#D97757"; DIM = "#8B8F96"; GHOST = "#D9D4C7"; CARD = "#FAF9F5"
BOX_TOP, BOX_L, BOX_R = "#F3E9D8", "#DCC9AA", "#C7AE86"          # kraft cardboard: top, left face, right face (deep enough for Gate V contrast)
BOX_IN1, BOX_IN2, BOX_FLOOR = "#CDB894", "#BFA67E", "#B39A72"     # inside walls + floor
DARK_TOP, DARK_L, DARK_R = "#3A3530", "#26221F", "#1E1B18"        # MCP / server blocks
PAGE_TOP, PAGE_L, PAGE_R = "#FFFFFF", "#ECE7DF", "#E2DCD2"         # skill pages
BAR1, BAR2, BAR3 = "#8B8F96", "#B4AFA6", "#D9D4C7"                # chart segments, dim to ghost
SERIF = "EB Garamond"
C30 = 0.8660254
config.background_color = STAGE


def T(s, size=36, color=INK, bold=False):
    return Text(s, font=SERIF, color=color, font_size=size, weight="BOLD" if bold else "NORMAL")


class Iso:
    """Isometric projection: x runs right-up, y runs left-up, z runs up. (ox, oy) is where (0,0,0) lands."""
    def __init__(self, ox=0.0, oy=0.0, s=1.0):
        self.ox, self.oy, self.s = ox, oy, s

    def p(self, x, y, z=0.0):
        return np.array([self.ox + (x - y) * C30 * self.s, self.oy + (x + y) * 0.5 * self.s + z * self.s, 0.0])

    def v(self, dx, dy, dz=0.0):
        return self.p(dx, dy, dz) - self.p(0, 0, 0)

    def quad(self, pts, fill, stroke=INK, sw=4):
        return Polygon(*[self.p(*q) for q in pts], fill_color=fill, fill_opacity=1, stroke_color=stroke, stroke_width=sw)

    def box(self, x0, y0, z0, w, d, h, top=BOX_TOP, left=BOX_L, right=BOX_R, sw=4):
        """Closed box: the two front faces (x = x0 and y = y0) plus the top."""
        x1, y1, z1 = x0 + w, y0 + d, z0 + h
        return VGroup(
            self.quad([(x0, y0, z0), (x0, y1, z0), (x0, y1, z1), (x0, y0, z1)], left, sw=sw),
            self.quad([(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)], right, sw=sw),
            self.quad([(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)], top, sw=sw))

    def open_box(self, x0, y0, z0, w, d, h):
        """(back, front): floor + inner back walls, then the front walls. Put contents between them."""
        x1, y1, z1 = x0 + w, y0 + d, z0 + h
        back = VGroup(
            self.quad([(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0)], BOX_FLOOR),
            self.quad([(x1, y0, z0), (x1, y1, z0), (x1, y1, z1), (x1, y0, z1)], BOX_IN1),
            self.quad([(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)], BOX_IN2))
        front = VGroup(
            self.quad([(x0, y0, z0), (x0, y1, z0), (x0, y1, z1), (x0, y0, z1)], BOX_L),
            self.quad([(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)], BOX_R))
        back.set_z_index(0); front.set_z_index(2)
        return back, front

    def tape(self, x0, y0, z1, w, d, drop=0.35, t=0.22):
        """Terracotta tape across the top (along x) and down the left front face."""
        ym = y0 + d / 2
        return VGroup(
            self.quad([(x0, ym - t, z1), (x0 + w, ym - t, z1), (x0 + w, ym + t, z1), (x0, ym + t, z1)], TERRA, sw=0),
            self.quad([(x0, ym - t, z1), (x0, ym + t, z1), (x0, ym + t, z1 - drop), (x0, ym - t, z1 - drop)], TERRA, sw=0))

    def mcp(self, x0, y0, z0, w=1.3, d=1.3, h=0.7):
        """Dark MCP block with two light ports on its right front face."""
        body = self.box(x0, y0, z0, w, d, h, DARK_TOP, DARK_L, DARK_R)
        ports = VGroup(*[self.box(x0 + w * f, y0 - 0.18, z0 + h * 0.3, w * 0.16, 0.18, h * 0.3, GHOST, BOX_IN1, BOX_IN2, sw=1)
                         for f in (0.22, 0.58)])
        return VGroup(body, ports)

    def page(self, x0, y0, z0, w=1.1, d=1.4):
        """A skill page lying flat: white slab, three ghost text lines, one terracotta dot."""
        slab = self.box(x0, y0, z0, w, d, 0.06, PAGE_TOP, PAGE_L, PAGE_R, sw=1.5)
        zt = z0 + 0.06
        lines = VGroup(*[Line(self.p(x0 + 0.2, y0 + d * f, zt), self.p(x0 + w - 0.2, y0 + d * f, zt), color=GHOST, stroke_width=4)
                         for f in (0.3, 0.5, 0.7)])
        dot = Dot(self.p(x0 + 0.2, y0 + d * 0.86, zt), radius=0.06, color=TERRA)
        return VGroup(slab, lines, dot)

    def server(self, x0, y0, z0, w=1.4, d=1.4, slab=0.42, n=3):
        """A stack of dark server slabs; returns (stack, lights) — lights start ghost, turn terracotta."""
        stack = VGroup(*[self.box(x0, y0, z0 + i * (slab + 0.04), w, d, slab, DARK_TOP, DARK_L, DARK_R) for i in range(n)])
        lights = VGroup(*[Dot(self.p(x0 + 0.25, y0, z0 + i * (slab + 0.04) + slab / 2), radius=0.06, color=GHOST) for i in range(n)])
        return stack, lights


def ease_in(t):
    """Quadratic ease-in (things dropping into a box). Local: Gate A's stub has no ease_in_quad."""
    return t * t


def check(x, y, s=0.2, color=INK, w=7):
    return VGroup(Line([x - s, y, 0], [x - s * 0.3, y - s * 0.75, 0], color=color, stroke_width=w),
                  Line([x - s * 0.3, y - s * 0.75, 0], [x + s * 1.1, y + s * 0.85, 0], color=color, stroke_width=w))


def cursor(x, y, s=0.45):
    return Polygon([x, y, 0], [x, y - s, 0], [x + s * 0.28, y - s * 0.72, 0], [x + s * 0.62, y - s * 0.66, 0],
                   fill_color=INK, fill_opacity=1, stroke_color=CARD, stroke_width=2)


def pill(x, y, w, h=0.62, fill="#FFFFFF"):
    return RoundedRectangle(width=w, height=h, corner_radius=h / 2, fill_color=fill, fill_opacity=1, stroke_width=0).move_to([x, y, 0])


# ═════════════════════════════ pacing (narration is the clock) ═════════════════════════════
try:
    _SHEET = _json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "beat_sheet.json")))
    _TARGET = {b["beat_id"]: float(b.get("actual_duration_s") or b.get("estimated_duration_s") or 0) for b in _SHEET["beats"]}
    _NARR = {b["beat_id"]: b["narration_text"] for b in _SHEET["beats"]}
except Exception:
    _TARGET, _NARR = {}, {}


def _elapsed(self):
    rt = getattr(getattr(self, "renderer", None), "time", None)
    return float(rt) if isinstance(rt, (int, float)) else 0.0


def until(self, phrase, lead=0.25):
    """Wait until `phrase` is spoken (its character share of the narration × the measured audio)."""
    bid = type(self).__name__.split("_")[0]
    n, target = _NARR.get(bid, ""), _TARGET.get(bid, 0)
    if not n or not target or phrase not in n:
        return
    gap = target * n.index(phrase) / len(n) - lead - _elapsed(self)
    if gap > 0.05:
        self.wait(gap)


def finish(self):
    target = _TARGET.get(type(self).__name__.split("_")[0], 0)
    self.wait(max(0.3, target - _elapsed(self)) if target else 2.0)

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

"""25 candidate redraws, not installed in the shared Show-Tell library.

Paste after the existing iso_kit and iso_props_24 helpers. Every part is native
vector geometry. Isocons silhouettes are simplified; controls gain movable parts.
"""
CANDIDATE_IDS=('prompt-suggestion','question-exchange','token','filter','sort',
 'dynamic-form','responsive-layout','sliders','toggle-on','settings-accessibility',
 'highlight-keyboard-focus','data-alert','sync-problem','undo','settings-backup-restore',
 'deployed-code-history','view-kanbab','timeline','query-stats','data-table','quiz',
 'local-library','lab-research','map','flag')

def _plate(w=1.7,h=1.5,fill=BOX_TOP):
    return _front([(-w/2,-h/2),(w/2,-h/2),(w/2,h/2),(-w/2,h/2)],.2,fill)

def _hook_arrow():
    return _front([(-.7,.9),(-1,.9),(-1,-.05),(-.7,-.35),(.48,-.35),(.15,-.68),
        (.38,-.9),(1,-.24),(.38,.42),(.15,.18),(.48,-.1),(-.55,-.1),(-.7,.05)],.18)

def _question():
    return VGroup(_front_line([(-.3,.35),(-.14,.55),(.13,.55),(.3,.34),(.23,.12),(0,-.02),(0,-.2)],INK,6),
        Dot(Iso().p(0,-.02,-.42),radius=.075,color=INK))

def _ring_arrow():
    angles=np.linspace(.4,5.8,44)
    points=[(np.cos(t),np.sin(t)) for t in angles]+[(.68*np.cos(t),.68*np.sin(t)) for t in angles[::-1]]
    ring=_front(points,.16)
    tip=_front([(.65,-.7),(1.12,-.66),(.94,-.18)],.16)
    return VGroup(ring,tip)

def _lens():
    return VGroup(Circle(radius=.46,stroke_color=INK,stroke_width=6),
        Line([.32,-.32,0],[.77,-.77,0],color=INK,stroke_width=8))

def make_candidate(name,x=0,y=0,scale=1):
    if name not in CANDIDATE_IDS:raise ValueError(name)
    p={};i=Iso()
    if name=='prompt-suggestion':
        p['arrow']=_hook_arrow();p['suggestion']=_slip(1.5,-.9).scale(.65)
    elif name=='question-exchange':
        p['upper']=_hook_arrow().scale(.6).move_to([0,.85,0])
        p['lower']=_hook_arrow().rotate(PI).scale(.6).move_to([0,-.85,0])
        p['question']=_question().scale(.7)
    elif name=='token':
        for n in range(4):
            a=n*PI/2+.18;b=(n+1)*PI/2-.18
            pts=[(r*np.cos(t),r*np.sin(t)) for r,ts in [(1,np.linspace(a,b,9)),(.4,np.linspace(b,a,9))] for t in ts]
            p['segment'+str(n)]=_front(pts,.25)
    elif name in ('filter','sort'):
        for n,w in enumerate((2,1.35,.7)):
            xx=-w/2 if name=='filter' else -1
            p['bar'+str(n)]=_front([(xx,.8-n*.6),(xx+w,.8-n*.6),(xx+w,1.02-n*.6),(xx,1.02-n*.6)],.22)
    elif name=='dynamic-form':
        p['row0']=_plate(1.4,.5).move_to([-.3,.65,0]);p['row1']=_plate(1.4,.5).move_to([-.3,-.3,0])
        p['branch']=_front([(.6,.8),(1,.8),(.8,.1),(1.1,.1),(.55,-1),(.7,-.2),(.4,-.2)],.15)
    elif name=='responsive-layout':
        p['desktop']=_plate(1.55,1.2).move_to([-.7,.45,0])
        p['tablet']=_plate(.85,1.3).move_to([.7,.1,0])
        p['phone']=_plate(.48,1).move_to([1.5,-.55,0])
    elif name=='sliders':
        p['rail']=_front([(-1.3,-.12),(1.3,-.12),(1.3,.12),(-1.3,.12)],.2)
        p['knob']=_plate(.32,.55,fill=BAR1).move_to([.55,.4,0])
    elif name=='toggle-on':
        pts=[(-.5+.6*np.cos(t),.6*np.sin(t)) for t in np.linspace(PI/2,3*PI/2,20)]
        pts +=[(.5+.6*np.cos(t),.6*np.sin(t)) for t in np.linspace(-PI/2,PI/2,20)]
        p['track']=_front(pts,.25)
        p['knob']=_front(_ellipse_points(.48,0,.32,.32),.05,fill=BAR1)
    elif name=='settings-accessibility':
        p['body']=_front([(-1,.48),(1,.48),(1,.2),(.3,.2),(.3,-1),(.08,-1),(0,-.25),(-.08,-1),(-.3,-1),(-.3,.2),(-1,.2)],.18)
        p['head']=_front(_ellipse_points(0,.92,.23,.23),.15)
        p['support']=VGroup(*[i.box(-.5,.3,-1.3+n*.12,1,.25,.06).shift(DOWN*.2*n) for n in range(2)])
    elif name=='highlight-keyboard-focus':
        p['disc']=_front(_ellipse_points(0,0,.9,.9),.2)
        p['caret']=_front_line([(0,-.38),(0,.38)],INK,10)
    elif name=='data-alert':
        for n in range(3):p['row'+str(n)]=_plate(1.7,.23).move_to([-.3,.65-n*.6,0])
        p['alert']=VGroup(_front_line([(0,.25),(0,-.25)],INK,9),Dot(Iso().p(0,0,-.52),radius=.09,color=INK)).move_to([1.25,.25,0])
    elif name=='sync-problem':
        p['upper']=_hook_arrow().scale(.7).move_to([-.3,.6,0]);p['lower']=_hook_arrow().rotate(PI).scale(.7).move_to([.3,-.65,0])
        p['warning']=Line([0,-.28,0],[0,.28,0],color=DIM,stroke_width=10)
    elif name=='undo':p['arrow']=_hook_arrow().rotate(PI)
    elif name=='settings-backup-restore':
        p['ring']=_ring_arrow();p['snapshot']=_front(_ellipse_points(0,0,.25,.25),.1,fill=BAR1)
    elif name=='deployed-code-history':
        p['package']=i.box(-.65,-.5,0,1.3,1,.8)
        p['clock']=Circle(radius=.48,fill_color=STAGE,fill_opacity=1,stroke_color=INK,stroke_width=5).move_to([1,-.8,0])
        p['hands']=VGroup(Line([1,-.8,0],[1,-.49,0],color=DIM,stroke_width=6),Line([1,-.8,0],[1.22,-.93,0],color=DIM,stroke_width=6))
    elif name=='view-kanbab':
        p['board']=_plate(2.15,1.7)
        for n,h in enumerate((.9,.5,1.15)):
            p['column'+str(n)]=_front([(-.78+n*.62,-.45),(-.45+n*.62,-.45),(-.45+n*.62,-.45+h),(-.78+n*.62,-.45+h)],.02,fill=BAR2)
        p['card']=i.box(0,0,0,.3,.3,.08).move_to([-.62,.1,0])
    elif name=='timeline':
        p['path']=_front_line([(-1,-.2),(-.4,.35),(.3,-.35),(1,.35)],INK,9)
        for n,(xx,zz) in enumerate([(-1,-.2),(-.4,.35),(.3,-.35),(1,.35)]):p['event'+str(n)]=_front(_ellipse_points(xx,zz,.12,.12),.1)
    elif name=='query-stats':
        p['trend']=_front_line([(-1,.1),(-.45,.8),(.1,.25),(.8,.95)],INK,9)
        p['lens']=_lens().move_to([.35,-.7,0])
    elif name=='data-table':
        for n in range(3):
            p['row'+str(n)]=_plate(1.8,.28).move_to([0,.8-n*.8,0])
            p['cell'+str(n)]=_front_line([(-.55,-.08),(-.55,.08)],DIM,6).shift(UP*(.8-n*.8))
    elif name=='quiz':
        p['back']=_plate(1.55,1.6).move_to([-.3,-.18,0]);p['page']=_plate(1.55,1.6)
        p['question']=_question()
    elif name=='local-library':
        p['left']=_front([(-1,-.55),(0,-.9),(0,.1),(-1,.45)],.2)
        p['right']=_front([(0,-.9),(1,-.55),(1,.45),(0,.1)],.2)
        p['reader']=_front(_ellipse_points(0,.9,.32,.32),.2)
    elif name=='lab-research':
        p['base']=i.box(-.9,-.4,-1,1.8,.8,.15)
        p['arm']=_front([(-.7,-.7),(-.35,-.7),(-.35,.8),(.3,.8),(.3,1.08),(-.7,1.08)],.2)
        p['lens']=_front([(-.18,.7),(.55,.7),(.55,.36),(-.18,.36)],.2,fill=BAR2)
        p['stage']=i.box(-.4,-.2,-.35,.95,.5,.06)
    elif name=='map':
        p['left']=_front([(-1,-.75),(-.33,-1),(-.33,.7),(-1,1)],.16)
        p['middle']=_front([(-.33,-1),(.33,-.75),(.33,1),(-.33,.7)],.16,fill=BOX_L)
        p['right']=_front([(.33,-.75),(1,-1),(1,.7),(.33,1)],.16)
    elif name=='flag':
        p['pole']=_front([(-.85,-1),(-.66,-1),(-.66,1),(-.85,1)],.16)
        p['flag']=_front([(-.66,.94),(.2,.94),(.35,.6),(1,.6),(1,-.1),(.18,-.1),(0,.15),(-.66,.15)],.16)
    g=VGroup(*p.values());g.move_to([0,0,0]);g.scale(scale);g.move_to([x,y,0]);g.parts=p
    return g

NBB_LOGO_DATA=[[[5.580421, -3.191236, 0.0], [5.576099, -3.188691, 0.0], [5.573047, -3.18361, 0.0], [5.573047, -3.179033, 0.0], [5.573047, -3.179033, 0.0], [5.573047, -3.17064, 0.0], [5.597456, -3.116739, 0.0], [5.620339, -3.074785, 0.0], [5.620339, -3.074785, 0.0], [5.628984, -3.059022, 0.0], [5.64907, -3.02546, -0.0], [5.657715, -3.012238, -0.0], [5.657715, -3.012238, -0.0], [5.662546, -3.005121, -0.0], [5.663564, -3.002832, -0.0], [5.663564, -2.999017, -0.0], [5.663564, -2.999017, -0.0], [5.663564, -2.99266, -0.0], [5.667886, -2.985795, -0.0], [5.676785, -2.977406, -0.0], [5.676785, -2.977406, -0.0], [5.685684, -2.96927, -0.0], [5.69687, -2.962149, -0.0], [5.71594, -2.95249, -0.0], [5.71594, -2.95249, -0.0], [5.740857, -2.94003, -0.0], [5.742128, -2.939776, -0.0], [5.758654, -2.939776, -0.0], [5.758654, -2.939776, -0.0], [5.776452, -2.93952, -0.0], [5.778995, -2.94079, -0.0], [5.768571, -2.944097, -0.0], [5.768571, -2.944097, -0.0], [5.726873, -2.957827, -0.0], [5.682886, -2.983001, -0.0], [5.675767, -2.997236, -0.0], [5.675767, -2.997236, -0.0], [5.674496, -2.999782, -0.0], [5.67297, -3.002322, -0.0], [5.672462, -3.00334, -0.0], [5.672462, -3.00334, -0.0], [5.670682, -3.005881, -0.0], [5.671953, -3.006899, -0.0], [5.687972, -3.015287, -0.0], [5.687972, -3.015287, -0.0], [5.700685, -3.022153, -0.0], [5.705515, -3.025712, -0.0], [5.703735, -3.027239, -0.0], [5.703735, -3.027239, -0.0], [5.702718, -3.028257, -0.0], [5.6867, -3.024441, -0.0], [5.679073, -3.021391, -0.0], [5.679073, -3.021391, -0.0], [5.67475, -3.019612, -0.0], [5.670682, -3.017067, -0.0], [5.669156, -3.015287, -0.0], [5.669156, -3.015287, -0.0], [5.668309, -3.014271, -0.0], [5.667461, -3.013254, -0.0], [5.666613, -3.012238, -0.0], [5.666613, -3.012238, -0.0], [5.664071, -3.016052, -0.0], [5.661528, -3.019866, -0.0], [5.658986, -3.02368, -0.0], [5.658986, -3.02368, -0.0], [5.643222, -3.047835, -0.0], [5.620339, -3.090294, 0.0], [5.609152, -3.116485, 0.0], [5.609152, -3.116485, 0.0], [5.603812, -3.128689, 0.0], [5.594659, -3.151826, 0.0], [5.587286, -3.17191, 0.0], [5.587286, -3.17191, 0.0], [5.586268, -3.174623, 0.0], [5.585251, -3.177336, 0.0], [5.584234, -3.180049, 0.0], [5.584234, -3.180049, 0.0], [5.585336, -3.179964, 0.0], [5.586438, -3.179878, 0.0], [5.58754, -3.179793, 0.0], [5.58754, -3.179793, 0.0], [5.59059, -3.179541, 0.0], [5.590845, -3.179793, 0.0], [5.591099, -3.183861, 0.0], [5.591099, -3.183861, 0.0], [5.591353, -3.18742, 0.0], [5.590845, -3.18869, 0.0], [5.588811, -3.190727, 0.0], [5.588811, -3.190727, 0.0], [5.585759, -3.193777, 0.0], [5.584743, -3.194033, 0.0], [5.58042, -3.191235, 0.0], [5.58042, -3.191235, 0.0], [5.58042, -3.191235, 0.0], [5.58042, -3.191235, 0.0], [5.58042, -3.191235, 0.0], [5.58042, -3.191235, 0.0], [5.58042, -3.191236, 0.0], [5.580421, -3.191236, 0.0], [5.580421, -3.191236, 0.0], [5.624408, -3.157927, 0.0], [5.620086, -3.155895, 0.0], [5.617543, -3.151827, 0.0], [5.617034, -3.146741, 0.0], [5.617034, -3.146741, 0.0], [5.616864, -3.145046, 0.0], [5.616695, -3.14335, 0.0], [5.616525, -3.141655, 0.0], [5.616525, -3.141655, 0.0], [5.618814, -3.139283, 0.0], [5.621102, -3.13691, 0.0], [5.62339, -3.134537, 0.0], [5.62339, -3.134537, 0.0], [5.638645, -3.11928, 0.0], [5.677039, -3.097417, 0.0], [5.726873, -3.07555, 0.0], [5.726873, -3.07555, 0.0], [5.735772, -3.071735, 0.0], [5.74289, -3.068176, 0.0], [5.743145, -3.067667, 0.0], [5.743145, -3.067667, 0.0], [5.743145, -3.067158, 0.0], [5.74162, -3.065888, 0.0], [5.73984, -3.064869, 0.0], [5.73984, -3.064869, 0.0], [5.735009, -3.06182, 0.0], [5.721533, -3.061563, 0.0], [5.708566, -3.063599, 0.0], [5.708566, -3.063599, 0.0], [5.689751, -3.066905, 0.0], [5.666868, -3.073514, 0.0], [5.652376, -3.079871, 0.0], [5.652376, -3.079871, 0.0], [5.645765, -3.08292, 0.0], [5.643477, -3.08292, 0.0], [5.642205, -3.079109, 0.0], [5.642205, -3.079109, 0.0], [5.639917, -3.072753, 0.0], [5.639917, -3.070207, 0.0], [5.642968, -3.067414, 0.0], [5.642968, -3.067414, 0.0], [5.646528, -3.064108, 0.0], [5.669411, -3.051394, 0.0], [5.697125, -3.037664, -0.0], [5.697125, -3.037664, -0.0], [5.724839, -3.023933, -0.0], [5.742383, -3.014018, -0.0], [5.759673, -3.002575, -0.0], [5.759673, -3.002575, -0.0], [5.791709, -2.981474, -0.0], [5.812557, -2.962149, -0.0], [5.816118, -2.950201, -0.0], [5.816118, -2.950201, -0.0], [5.817389, -2.946385, -0.0], [5.817134, -2.945876, -0.0], [5.814846, -2.943588, -0.0], [5.814846, -2.943588, -0.0], [5.811541, -2.939776, -0.0], [5.803659, -2.93647, -0.0], [5.79298, -2.934434, -0.0], [5.79298, -2.934434, -0.0], [5.780522, -2.931893, -0.0], [5.743909, -2.931893, -0.0], [5.724586, -2.934434, -0.0], [5.724586, -2.934434, -0.0], [5.643224, -2.945115, -0.0], [5.556268, -2.976898, -0.0], [5.4955, -3.017577, -0.0], [5.4955, -3.017577, -0.0], [5.468041, -3.035885, -0.0], [5.445411, -3.059022, 0.0], [5.436767, -3.07733, 0.0], [5.436767, -3.07733, 0.0], [5.434479, -3.082159, 0.0], [5.434225, -3.084448, 0.0], [5.434225, -3.091823, 0.0], [5.434225, -3.091823, 0.0], [5.434225, -3.099959, 0.0], [5.434479, -3.100976, 0.0], [5.437276, -3.105045, 0.0], [5.437276, -3.105045, 0.0], [5.441344, -3.111144, 0.0], [5.451006, -3.117248, 0.0], [5.461176, -3.120555, 0.0], [5.461176, -3.120555, 0.0], [5.472109, -3.123857, 0.0], [5.477957, -3.124876, 0.0], [5.49245, -3.126146, 0.0], [5.49245, -3.126146, 0.0], [5.503892, -3.127165, 0.0], [5.505926, -3.127925, 0.0], [5.505926, -3.131232, 0.0], [5.505926, -3.131232, 0.0], [5.505926, -3.133268, 0.0], [5.473381, -3.131994, 0.0], [5.464482, -3.129961, 0.0], [5.464482, -3.129961, 0.0], [5.440836, -3.124114, 0.0], [5.424309, -3.104536, 0.0], [5.425834, -3.08394, 0.0], [5.425834, -3.08394, 0.0], [5.427106, -3.061059, 0.0], [5.448463, -3.036647, -0.0], [5.492196, -3.00741, -0.0], [5.492196, -3.00741, -0.0], [5.527029, -2.984273, -0.0], [5.566947, -2.965204, -0.0], [5.61373, -2.949185, -0.0], [5.61373, -2.949185, -0.0], [5.673481, -2.928845, -0.0], [5.741113, -2.91715, -0.0], [5.778489, -2.92071, -0.0], [5.778489, -2.92071, -0.0], [5.796541, -2.922489, -0.0], [5.793999, -2.922741, -0.0], [5.812559, -2.918421, -0.0], [5.812559, -2.918421, -0.0], [5.879937, -2.903163, -0.0], [5.936128, -2.902911, -0.0], [5.958756, -2.917912, -0.0], [5.958756, -2.917912, -0.0], [5.969435, -2.924778, -0.0], [5.974011, -2.933423, -0.0], [5.974266, -2.945626, -0.0], [5.974266, -2.945626, -0.0], [5.974266, -2.953001, -0.0], [5.973757, -2.95478, -0.0], [5.970707, -2.960881, -0.0], [5.970707, -2.960881, -0.0], [5.962825, -2.976648, -0.0], [5.943247, -2.99241, -0.0], [5.906125, -3.01275, -0.0], [5.906125, -3.01275, -0.0], [5.894176, -3.019106, -0.0], [5.884259, -3.023683, -0.0], [5.84968, -3.039446, -0.0], [5.84968, -3.039446, -0.0], [5.847646, -3.040464, -0.0], [5.849934, -3.040716, -0.0], [5.861376, -3.040716, -0.0], [5.861376, -3.040716, -0.0], [5.883242, -3.040973, -0.0], [5.893921, -3.042752, -0.0], [5.90104, -3.047582, -0.0], [5.90104, -3.047582, -0.0], [5.902311, -3.04843, -0.0], [5.903582, -3.049279, -0.0], [5.904853, -3.050127, 0.0], [5.904853, -3.050127, 0.0], [5.907989, -3.049364, -0.0], [5.911125, -3.048601, -0.0], [5.914261, -3.047839, -0.0], [5.914261, -3.047839, -0.0], [5.9196, -3.046568, -0.0], [5.924177, -3.045803, -0.0], [5.924431, -3.046059, -0.0], [5.924431, -3.046059, -0.0], [5.925448, -3.047073, -0.0], [5.922906, -3.049871, -0.0], [5.921126, -3.049871, -0.0], [5.921126, -3.049871, -0.0], [5.920109, -3.049871, -0.0], [5.916295, -3.050889, 0.0], [5.912481, -3.05216, 0.0], [5.912481, -3.05216, 0.0], [5.910192, -3.052838, 0.0], [5.907904, -3.053517, 0.0], [5.905616, -3.054196, 0.0], [5.905616, -3.054196, 0.0], [5.905616, -3.055721, 0.0], [5.905616, -3.057247, 0.0], [5.905616, -3.058772, 0.0], [5.905616, -3.058772, 0.0], [5.905616, -3.064872, 0.0], [5.903328, -3.069449, 0.0], [5.897226, -3.075553, 0.0], [5.897226, -3.075553, 0.0], [5.884512, -3.088266, 0.0], [5.854256, -3.104028, 0.0], [5.82222, -3.114705, 0.0], [5.82222, -3.114705, 0.0], [5.811033, -3.11852, 0.0], [5.80671, -3.119539, 0.0], [5.799337, -3.119791, 0.0], [5.799337, -3.119791, 0.0], [5.790438, -3.1203, 0.0], [5.78993, -3.1203, 0.0], [5.787642, -3.117759, 0.0], [5.787642, -3.117759, 0.0], [5.785099, -3.114961, 0.0], [5.784591, -3.109622, 0.0], [5.78637, -3.106059, 0.0], [5.78637, -3.106059, 0.0], [5.789421, -3.100469, 0.0], [5.803914, -3.090044, 0.0], [5.821712, -3.080634, 0.0], [5.821712, -3.080634, 0.0], [5.836205, -3.072754, 0.0], [5.865444, -3.061565, 0.0], [5.88909, -3.054956, 0.0], [5.88909, -3.054956, 0.0], [5.891378, -3.054194, 0.0], [5.893412, -3.053429, 0.0], [5.893412, -3.052923, 0.0], [5.893412, -3.052923, 0.0], [5.893412, -3.049617, -0.0], [5.854257, -3.048599, -0.0], [5.828831, -3.051396, 0.0], [5.828831, -3.051396, 0.0], [5.821203, -3.052158, 0.0], [5.814084, -3.052667, 0.0], [5.813321, -3.052415, 0.0], [5.813321, -3.052415, 0.0], [5.811541, -3.051649, 0.0], [5.809507, -3.044531, -0.0], [5.810524, -3.04199, -0.0], [5.810524, -3.04199, -0.0], [5.811287, -3.039445, -0.0], [5.813575, -3.038427, -0.0], [5.83595, -3.030039, -0.0], [5.83595, -3.030039, -0.0], [5.882987, -3.012497, -0.0], [5.92977, -2.987832, -0.0], [5.95367, -2.968254, -0.0], [5.95367, -2.968254, -0.0], [5.966637, -2.957321, -0.0], [5.971722, -2.945879, -0.0], [5.966383, -2.937999, -0.0], [5.966383, -2.937999, -0.0], [5.961806, -2.931133, -0.0], [5.950365, -2.925286, -0.0], [5.935109, -2.921979, -0.0], [5.935109, -2.921979, -0.0], [5.922905, -2.919438, -0.0], [5.882732, -2.919691, -0.0], [5.860866, -2.922741, -0.0], [5.860866, -2.922741, -0.0], [5.845356, -2.924777, -0.0], [5.818151, -2.929607, -0.0], [5.817134, -2.930624, -0.0], [5.817134, -2.930624, -0.0], [5.81688, -2.930877, -0.0], [5.817897, -2.932656, -0.0], [5.819422, -2.934693, -0.0], [5.819422, -2.934693, -0.0], [5.823237, -2.940288, -0.0], [5.824762, -2.948933, -0.0], [5.823237, -2.955793, -0.0], [5.823237, -2.955793, -0.0], [5.820948, -2.965713, -0.0], [5.816372, -2.973083, -0.0], [5.806201, -2.984016, -0.0], [5.806201, -2.984016, -0.0], [5.787386, -3.003342, -0.0], [5.765011, -3.018595, -0.0], [5.70577, -3.052157, 0.0], [5.70577, -3.052157, 0.0], [5.704075, -3.05309, 0.0], [5.70238, -3.054022, 0.0], [5.700685, -3.054955, 0.0], [5.700685, -3.054955, 0.0], [5.705431, -3.054701, 0.0], [5.710177, -3.054447, 0.0], [5.714923, -3.054193, 0.0], [5.714923, -3.054193, 0.0], [5.734501, -3.053428, 0.0], [5.741366, -3.055716, 0.0], [5.746959, -3.064108, 0.0], [5.746959, -3.064108, 0.0], [5.747468, -3.064871, 0.0], [5.747976, -3.065634, 0.0], [5.748485, -3.066397, 0.0], [5.748485, -3.066397, 0.0], [5.750943, -3.065634, 0.0], [5.753401, -3.064871, 0.0], [5.755858, -3.064108, 0.0], [5.755858, -3.064108, 0.0], [5.762977, -3.062073, 0.0], [5.767809, -3.062073, 0.0], [5.767045, -3.064617, 0.0], [5.767045, -3.064617, 0.0], [5.766537, -3.065888, 0.0], [5.763486, -3.067415, 0.0], [5.755604, -3.070465, 0.0], [5.755604, -3.070465, 0.0], [5.75357, -3.071228, 0.0], [5.751535, -3.071991, 0.0], [5.749501, -3.072753, 0.0], [5.749501, -3.072753, 0.0], [5.749247, -3.074449, 0.0], [5.748993, -3.076144, 0.0], [5.748739, -3.077839, 0.0], [5.748739, -3.077839, 0.0], [5.746451, -3.097922, 0.0], [5.719499, -3.122843, 0.0], [5.680089, -3.142165, 0.0], [5.680089, -3.142165, 0.0], [5.655173, -3.154368, 0.0], [5.631272, -3.160982, 0.0], [5.624407, -3.157928, 0.0], [5.624407, -3.157928, 0.0], [5.624407, -3.157928, 0.0], [5.624407, -3.157928, 0.0], [5.624407, -3.157928, 0.0], [5.624407, -3.157928, 0.0], [5.624407, -3.157927, 0.0], [5.624407, -3.157927, 0.0], [5.624408, -3.157927, 0.0], [5.635595, -3.142165, 0.0], [5.651867, -3.138097, 0.0], [5.675767, -3.128691, 0.0], [5.69204, -3.120046, 0.0], [5.69204, -3.120046, 0.0], [5.714414, -3.108094, 0.0], [5.73628, -3.090296, 0.0], [5.74162, -3.079618, 0.0], [5.74162, -3.079618, 0.0], [5.742383, -3.078177, 0.0], [5.743145, -3.076735, 0.0], [5.743908, -3.075294, 0.0], [5.743908, -3.075294, 0.0], [5.742298, -3.075972, 0.0], [5.740687, -3.076651, 0.0], [5.739077, -3.077329, 0.0], [5.739077, -3.077329, 0.0], [5.710092, -3.088772, 0.0], [5.671191, -3.108855, 0.0], [5.649833, -3.123604, 0.0], [5.649833, -3.123604, 0.0], [5.640171, -3.130213, 0.0], [5.623899, -3.144962, 0.0], [5.627458, -3.144196, 0.0], [5.627458, -3.144196, 0.0], [5.628476, -3.143944, 0.0], [5.632289, -3.142926, 0.0], [5.635595, -3.142164, 0.0], [5.635595, -3.142164, 0.0], [5.635595, -3.142164, 0.0], [5.635595, -3.142164, 0.0], [5.635595, -3.142164, 0.0], [5.635595, -3.142164, 0.0], [5.635595, -3.142164, 0.0], [5.635595, -3.142165, 0.0], [5.635595, -3.142165, 0.0], [5.805438, -3.109364, 0.0], [5.827304, -3.103008, 0.0], [5.864171, -3.086483, 0.0], [5.880697, -3.07555, 0.0], [5.880697, -3.07555, 0.0], [5.890359, -3.069194, 0.0], [5.900529, -3.060039, 0.0], [5.900529, -3.057495, 0.0], [5.900529, -3.057495, 0.0], [5.900529, -3.055463, 0.0], [5.900021, -3.055463, 0.0], [5.886546, -3.060293, 0.0], [5.886546, -3.060293, 0.0], [5.858577, -3.069956, 0.0], [5.823744, -3.085718, 0.0], [5.808488, -3.095633, 0.0], [5.808488, -3.095633, 0.0], [5.799336, -3.101737, 0.0], [5.790945, -3.108347, 0.0], [5.790182, -3.110635, 0.0], [5.790182, -3.110635, 0.0], [5.789419, -3.112923, 0.0], [5.795267, -3.112414, 0.0], [5.805438, -3.109364, 0.0], [5.805438, -3.109364, 0.0], [5.805438, -3.109364, 0.0], [5.805438, -3.109364, 0.0], [5.805438, -3.109364, 0.0], [5.759672, -3.130213, 0.0], [5.756366, -3.128433, 0.0], [5.754078, -3.124874, 0.0], [5.754078, -3.122076, 0.0], [5.754078, -3.122076, 0.0], [5.753824, -3.1114, 0.0], [5.798065, -3.025459, -0.0], [5.822728, -2.988083, -0.0], [5.822728, -2.988083, -0.0], [5.830864, -2.975879, -0.0], [5.832643, -2.974861, -0.0], [5.835186, -2.979946, -0.0], [5.835186, -2.979946, -0.0], [5.836458, -2.982492, -0.0], [5.836203, -2.983001, -0.0], [5.832898, -2.987321, -0.0], [5.832898, -2.987321, -0.0], [5.82349, -2.999781, -0.0], [5.797048, -3.049614, -0.0], [5.782301, -3.082919, 0.0], [5.782301, -3.082919, 0.0], [5.771368, -3.107584, 0.0], [5.768572, -3.114958, 0.0], [5.770097, -3.115976, 0.0], [5.770097, -3.115976, 0.0], [5.771622, -3.11699, 0.0], [5.772131, -3.121315, 0.0], [5.771113, -3.123603, 0.0], [5.771113, -3.123603, 0.0], [5.769333, -3.126909, 0.0], [5.765011, -3.131229, 0.0], [5.763232, -3.131229, 0.0], [5.763232, -3.131229, 0.0], [5.762469, -3.131229, 0.0], [5.760689, -3.13072, 0.0], [5.759673, -3.130211, 0.0], [5.759673, -3.130211, 0.0], [5.759673, -3.130211, 0.0], [5.759673, -3.130211, 0.0], [5.759673, -3.130211, 0.0], [5.759673, -3.130211, 0.0], [5.759672, -3.130211, 0.0], [5.759672, -3.130212, 0.0], [5.759672, -3.130213, 0.0]]]
def _brand_bug():
    return VGroup(*[VMobject(fill_color=DIM,fill_opacity=.55,stroke_width=0).set_points(np.array(points)) for points in NBB_LOGO_DATA])

"""Meaningful actions on the 25 candidate rigs; narrated word timing."""
try:_WORDS=_json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),'mp3','words.json')))['beats']
except (OSError,KeyError):_WORDS={}
def _cue(scene,word):
    bid=type(scene).__name__.split('_')[0]
    for token in _WORDS.get(bid,[]):
        if token['text'].strip('.,:;!?').lower()==word.lower():
            gap=token['startFrame']/24-_elapsed(scene)-.08
            if gap>0:scene.wait(gap)
            break
def _done(scene):
    bid=type(scene).__name__.split('_')[0];gap=_TARGET.get(bid,10)-_elapsed(scene)-.1
    if gap>0:scene.wait(gap)
def _play(scene,*animations,run_time=.8):
    bid=type(scene).__name__.split('_')[0];mid=_TARGET.get(bid,10)/2;now=_elapsed(scene)
    if now<mid+.25 and now+run_time>mid-.25:scene.wait(max(.01,mid+.3-now))
    scene.play(*animations,run_time=run_time)
def _prop_demo(scene,name,title,verb,cue):
    hero=make_candidate(name,scale=1.5);p=hero.parts
    hidden={'dynamic-form':['row1'],'data-alert':['alert'],'settings-accessibility':['support']}
    for part in hidden.get(name,[]):hero.remove(p[part])
    if name=='toggle-on':p['knob'].shift(Iso().v(-.96,0,0)*1.5)
    if name=='sliders':p['knob'].shift(Iso().v(-1.25,0,0)*1.5)
    if name=='settings-backup-restore':p['snapshot'].move_to([3.7,-.2,0])
    if name=='flag':p['flag'].shift(DOWN*.65)
    if name=='highlight-keyboard-focus':
        hero.shift(LEFT*1.6);p['caret'].set_z_index(2)
    scene.add(hero,T(title,64).move_to([0,2.9,0]),T(verb,56).move_to([0,-2.8,0]),_brand_bug())
    scene.wait(.2);pulse=Dot([4.7,-2.75,0],radius=.1,color=TERRA)
    _play(scene,FadeIn(pulse),run_time=.25);scene.wait(.3);_cue(scene,cue)
    if name=='prompt-suggestion':
        _play(scene,p['suggestion'].animate.shift(LEFT*1.15+UP*.25),run_time=1.2)
        _play(scene,Create(Line([2.6,-1.4,0],[4,-1.4,0],color=DIM,stroke_width=5)),run_time=.6)
    elif name=='question-exchange':
        _play(scene,p['upper'].animate.shift(RIGHT*.65),p['lower'].animate.shift(LEFT*.65),run_time=1.4)
        _play(scene,FadeIn(_slip(3.6,-.5)),run_time=.5)
    elif name=='token':
        _play(scene,p['segment0'].animate.shift(RIGHT*1.3),run_time=1.3)
        _play(scene,Create(Line([3,-1.1,0],[4.1,-1.1,0],color=DIM,stroke_width=6)),run_time=.5)
    elif name=='filter':
        slip=_slip(3.4,1.25).scale(.7);_play(scene,FadeIn(slip),run_time=.3)
        for yy in (.25,-.65,-1.5):_play(scene,slip.animate.move_to([3.4,yy,0]),run_time=.55)
    elif name=='sort':
        a=np.array(p['bar0'].get_center());b=np.array(p['bar2'].get_center())
        _play(scene,p['bar0'].animate.move_to(b),p['bar2'].animate.move_to(a),run_time=1.4)
        _play(scene,FadeIn(_slip(3.5,0).scale(.7)),run_time=.5)
    elif name=='dynamic-form':
        _play(scene,FadeIn(p['row1'],shift=DOWN*.3),run_time=1)
        _play(scene,FadeIn(_slip(3.5,-.2)),run_time=.6)
    elif name=='responsive-layout':
        _play(scene,p['desktop'].animate.shift(LEFT*.7),p['phone'].animate.shift(RIGHT*.55),run_time=1.3)
        _play(scene,Create(Line([-3,-2.15,0],[3,-2.15,0],color=DIM,stroke_width=5)),run_time=.7)
    elif name=='sliders':
        _play(scene,p['knob'].animate.shift(Iso().v(1.55,0,0)*1.5),run_time=1.5)
        _play(scene,FadeIn(_slip(3.8,-.5).scale(.6)),run_time=.5)
    elif name=='toggle-on':
        _play(scene,p['knob'].animate.shift(Iso().v(.96,0,0)*1.5),run_time=1.2)
        _play(scene,Create(Line([3,-.9,0],[4.2,-.9,0],color=DIM,stroke_width=5)),run_time=.6)
    elif name=='settings-accessibility':
        _play(scene,FadeIn(p['support'],shift=LEFT*1.5),run_time=1.4)
        _play(scene,FadeIn(_slip(3.6,-.4)),run_time=.6)
    elif name=='highlight-keyboard-focus':
        target=p['disc'].copy().shift(RIGHT*3.2)
        _play(scene,FadeIn(target),run_time=.5)
        _play(scene,p['caret'].animate.shift(RIGHT*3.2),run_time=1.3)
    elif name=='data-alert':
        _play(scene,Create(p['alert']),run_time=.7)
        _play(scene,p['row1'].animate.move_to([-3.5,-1.1,0]),run_time=1.3)
    elif name=='sync-problem':
        slip=_slip(-3.7,-1.1).scale(.7);_play(scene,FadeIn(slip),run_time=.4)
        _play(scene,slip.animate.move_to([-1.65,-1.1,0]),run_time=1.3)
        _play(scene,Create(Line([-1.1,-1.7,0],[-1.1,-.6,0],color=DIM,stroke_width=7)),run_time=.5)
    elif name=='undo':
        slip=_slip(-3.5,-1.25).scale(.8);_play(scene,FadeIn(slip),run_time=.4)
        _play(scene,slip.animate.move_to([3.5,-1.25,0]),run_time=1)
        _play(scene,slip.animate.move_to([-3.5,-1.25,0]),run_time=1)
    elif name=='settings-backup-restore':
        _play(scene,p['snapshot'].animate.move_to(p['ring'].get_center()),run_time=1.4)
        _play(scene,FadeIn(_slip(3.7,-1)),run_time=.5)
    elif name=='deployed-code-history':
        _play(scene,VGroup(p['clock'],p['hands']).animate.shift(RIGHT*.65),run_time=.8)
        _play(scene,FadeIn(_slip(-3.6,-.75)),run_time=.7)
    elif name=='view-kanbab':
        _play(scene,p['card'].animate.shift(Iso().v(.65,0,0)*1.5),run_time=1.3)
        _play(scene,FadeIn(_slip(3.6,-.4)),run_time=.7)
    elif name=='timeline':
        dot=Dot(p['event0'].get_center(),radius=.14,color=TERRA);scene.remove(pulse)
        _play(scene,FadeIn(dot),run_time=.3)
        for n in (1,2,3):_play(scene,dot.animate.move_to(p['event'+str(n)].get_center()),run_time=.65)
    elif name=='query-stats':
        _play(scene,p['lens'].animate.shift(LEFT*.75+UP*.65),run_time=1.3)
        _play(scene,FadeIn(_slip(3.6,-.6)),run_time=.6)
    elif name=='data-table':
        _play(scene,VGroup(p['row1'],p['cell1']).animate.move_to([3,-.1,0]),run_time=1.3)
        _play(scene,Create(Line([3.1,-1.7,0],[4.4,-1.7,0],color=DIM,stroke_width=6)),run_time=.5)
    elif name=='quiz':
        _play(scene,p['question'].animate.move_to([-3.6,.2,0]),run_time=1)
        _play(scene,FadeIn(_slip(3.5,0)),run_time=.8)
    elif name=='local-library':
        _play(scene,p['left'].animate.shift(LEFT*.7),p['right'].animate.shift(RIGHT*.7),run_time=1.4)
        _play(scene,FadeIn(_slip(3.7,-.7)),run_time=.6)
    elif name=='lab-research':
        _play(scene,p['lens'].animate.shift(DOWN*.45),run_time=1.3)
        _play(scene,FadeIn(_slip(3.6,-.7)),run_time=.6)
    elif name=='map':
        _play(scene,p['left'].animate.shift(LEFT*.75),p['right'].animate.shift(RIGHT*.75),run_time=1.4)
        _play(scene,FadeIn(_slip(3.6,-.75)),run_time=.6)
    elif name=='flag':
        _play(scene,p['flag'].animate.shift(UP*.65),run_time=1.3)
        _play(scene,FadeIn(_slip(3.6,-.75)),run_time=.6)
    _done(scene)

class BCREDIT_Attribution(Scene):
    def construct(self):
        hero=make_candidate('map',scale=1.3)
        self.add(hero,_brand_bug(),T('Isocons',64).move_to([-3.7,2.6,0]),T('CC BY 4.0',60).move_to([3.3,2.6,0]),T('Candidates',56).move_to([0,-2.6,0]))
        _play(self,hero.parts['right'].animate.shift(RIGHT*.6),run_time=1)
        _play(self,FadeIn(_slip(3.8,-.3)),run_time=.6);_done(self)

class B00_Prop(Scene):
    def construct(self):
        _prop_demo(self,'prompt-suggestion','Suggestion','Choose','Move')

class B01_Prop(Scene):
    def construct(self):
        _prop_demo(self,'question-exchange','Clarification','Ask back','Separate')

class B02_Prop(Scene):
    def construct(self):
        _prop_demo(self,'token','Token','Allocate','Separate')

class B03_Prop(Scene):
    def construct(self):
        _prop_demo(self,'filter','Filter','Narrow','Move')

class B04_Prop(Scene):
    def construct(self):
        _prop_demo(self,'sort','Sort','Reorder','Swap')

class B05_Prop(Scene):
    def construct(self):
        _prop_demo(self,'dynamic-form','Adaptive form','Reveal','Reveal')

class B06_Prop(Scene):
    def construct(self):
        _prop_demo(self,'responsive-layout','Responsive design','Reflow','Separate')

class B07_Prop(Scene):
    def construct(self):
        _prop_demo(self,'sliders','Adjustment','Tune','Move')

class B08_Prop(Scene):
    def construct(self):
        _prop_demo(self,'toggle-on','Explicit choice','Switch','Move')

class B09_Prop(Scene):
    def construct(self):
        _prop_demo(self,'settings-accessibility','Accessibility','Support','Bring')

class B10_Prop(Scene):
    def construct(self):
        _prop_demo(self,'highlight-keyboard-focus','Keyboard focus','Advance','Move')

class B11_Prop(Scene):
    def construct(self):
        _prop_demo(self,'data-alert','Data warning','Investigate','Reveal')

class B12_Prop(Scene):
    def construct(self):
        _prop_demo(self,'sync-problem','Sync failure','Stop','Bring')

class B13_Prop(Scene):
    def construct(self):
        _prop_demo(self,'undo','Undo','Reverse','Move')

class B14_Prop(Scene):
    def construct(self):
        _prop_demo(self,'settings-backup-restore','Restore','Recover','Bring')

class B15_Prop(Scene):
    def construct(self):
        _prop_demo(self,'deployed-code-history','Release history','Inspect','Move')

class B16_Prop(Scene):
    def construct(self):
        _prop_demo(self,'view-kanbab','Work board','Advance','Move')

class B17_Prop(Scene):
    def construct(self):
        _prop_demo(self,'timeline','Timeline','Trace','Follow')

class B18_Prop(Scene):
    def construct(self):
        _prop_demo(self,'query-stats','Metric inquiry','Inspect','Move')

class B19_Prop(Scene):
    def construct(self):
        _prop_demo(self,'data-table','Table','Inspect row','Pull')

class B20_Prop(Scene):
    def construct(self):
        _prop_demo(self,'quiz','Retrieval practice','Attempt','Move')

class B21_Prop(Scene):
    def construct(self):
        _prop_demo(self,'local-library','Reference reading','Open','Open')

class B22_Prop(Scene):
    def construct(self):
        _prop_demo(self,'lab-research','Experiment','Test','Lower')

class B23_Prop(Scene):
    def construct(self):
        _prop_demo(self,'map','Orientation','Unfold','Unfold')

class B24_Prop(Scene):
    def construct(self):
        _prop_demo(self,'flag','Milestone','Mark','Raise')
