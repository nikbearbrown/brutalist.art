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
