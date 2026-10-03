"""Film actions. build_reel.py pastes this AFTER both shared vector kits."""

try:
    _WORDS=_json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),'mp3','words.json')))['beats']
except (OSError,KeyError):
    _WORDS={}

def _cue(scene,word):
    bid=type(scene).__name__.split('_')[0]
    for token in _WORDS.get(bid,[]):
        if token['text'].strip('.,:;!?').lower()==word.lower():
            gap=token['startFrame']/24-_elapsed(scene)-.08
            if gap>0:scene.wait(gap)
            break

def _done(scene):
    bid=type(scene).__name__.split('_')[0]
    gap=_TARGET.get(bid,10)-_elapsed(scene)-.10
    if gap>0:scene.wait(gap)

def _play(scene,*animations,run_time=.8):
    bid=type(scene).__name__.split('_')[0]
    midpoint=_TARGET.get(bid,10)/2
    now=_elapsed(scene)
    if now<midpoint+.25 and now+run_time>midpoint-.25:
        scene.wait(max(.01,midpoint+.3-now))
    scene.play(*animations,run_time=run_time)

def _prop_demo(scene,name,title,verb):
    hero=make_prop(name,x=-.4,y=0,scale=1.4 if name in ('layers','deployed-code') else 1.65)
    p=hero.parts
    # Prepare initial states BEFORE the first rendered frame. No teleporting a
    # settled prop into an action's starting pose, and no checks appearing early.
    if name=='dataset-linked':p['link'].shift(RIGHT*2)
    if name=='deployed-code':VGroup(p['package'],p['brackets']).shift(UP*.65)
    if name=='person-raised-hand':VGroup(p['arm'],p['hand']).shift(DOWN*.45)
    if name=='handshake':
        p['left'].shift(LEFT*.65);p['right'].shift(RIGHT*.65)
    if name=='partner-exchange':p['handoff'].move_to([-2.3,-1.2,0])
    hidden={'linked-services':['connector'],'person-check':['check'],
        'data-check-double':['checks'],'search-check-2':['check'],
        'track-changes':['revision'],'receipt':['row0','row1','row2'],
        'account-tree':['edges']}
    for part in hidden.get(name,[]):hero.remove(p[part])
    title_obj=T(title,64).move_to([0,2.85,0])
    verb_obj=T(verb,56).move_to([0,-2.8,0])
    scene.add(hero,title_obj,verb_obj,_brand_bug())
    # New membership after the first play also makes Gate A distinguish action
    # from motion-only wallpaper. This quiet marker is an activity indicator.
    scene.wait(.2)
    pulse=Dot([4.7,-2.75,0],radius=.1,color=TERRA)
    _play(scene,FadeIn(pulse),run_time=.25)
    scene.wait(.35)
    cues=['Lift','Join','Lift','Pull','Watch','Draw','Lower','Follow','Raise','Bring','Bring','Move',
          'Let','Keep','Send','Move','Cross-check','Move','Separate','Add','Draw','Split','Move','Move']
    _cue(scene,cues[PROP_IDS.index(name)])
    if name=='dataset':
        part=p['cells'][1]
        _play(scene,part.animate.move_to([3.5,.3,0]),run_time=1.25)
        _play(scene,Create(check(3.5,-.9,.27)),run_time=.65)
    elif name=='dataset-linked':
        link=p['link']
        _play(scene,link.animate.shift(LEFT*2),run_time=1.5)
        _play(scene,Create(check(3.4,0,.27)),run_time=.5)
    elif name=='layers':
        _play(scene,p['layer2'].animate.shift(UP*.65+RIGHT*.8),run_time=1.35)
        _play(scene,FadeIn(_slip(3.9,0)),run_time=.6)
    elif name=='quick-reference':
        _play(scene,p['bookmark'].animate.shift(RIGHT*2.3),run_time=1.2)
        _play(scene,FadeIn(_slip(3.6,-.5)),run_time=.6)
    elif name=='terminal':
        req=_slip(-4,0);res=_slip(3.8,0)
        _play(scene,FadeIn(req),run_time=.5)
        _play(scene,req.animate.move_to([-2,0,0]),run_time=.9)
        scene.remove(req)
        _play(scene,FadeIn(res,shift=RIGHT*.8),run_time=.9)
    elif name=='linked-services':
        link=p['connector'];hero.remove(link)
        _play(scene,Create(link),run_time=.8)
        dot=Dot(link.get_start(),radius=.12,color=TERRA)
        scene.remove(pulse);_play(scene,FadeIn(dot),run_time=.3)
        _play(scene,dot.animate.move_to(link.get_end()),run_time=1.5)
    elif name=='deployed-code':
        package=VGroup(p['package'],p['brackets'])
        _play(scene,package.animate.shift(DOWN*.65),run_time=1.2)
        _play(scene,Create(check(3.6,.15,.3)),run_time=.6)
    elif name=='network-node':
        nodes=p['nodes'];dot=Dot(nodes[0].get_center(),radius=.13,color=TERRA)
        scene.remove(pulse);_play(scene,FadeIn(dot),run_time=.4)
        _play(scene,dot.animate.move_to(nodes[2].get_center()),run_time=1)
        _play(scene,dot.animate.move_to(nodes[1].get_center()),run_time=1)
    elif name=='person-raised-hand':
        arm=VGroup(p['arm'],p['hand'])
        req=_slip(3.8,-.15)
        _play(scene,FadeIn(req),run_time=.5)
        _play(scene,arm.animate.shift(UP*.45),run_time=.9)
        _play(scene,Create(Line([2.55,-.65,0],[2.55,.65,0],color=INK,stroke_width=7)),run_time=.6)
    elif name=='person-check':
        approval=p['check'];hero.remove(approval)
        req=_slip(4,0)
        _play(scene,FadeIn(req),run_time=.4)
        _play(scene,req.animate.move_to([2.3,-.3,0]),run_time=1)
        _play(scene,Create(approval),run_time=.7)
    elif name=='handshake':
        _play(scene,p['left'].animate.shift(RIGHT*.65),p['right'].animate.shift(LEFT*.65),run_time=1.4)
        _play(scene,Create(check(3.8,.1,.3)),run_time=.6)
    elif name=='partner-exchange':
        slip=p['handoff']
        _play(scene,slip.animate.move_to([1.3,-.15,0]),run_time=1.8)
        _play(scene,Create(check(3.5,0,.3)),run_time=.6)
    elif name=='policy':
        req=_slip(4.1,0)
        _play(scene,FadeIn(req),run_time=.4)
        _play(scene,req.animate.move_to([2.55,0,0]),run_time=.9)
        scene.wait(.35)
        _play(scene,req.animate.move_to([4.1,0,0]),run_time=.9)
    elif name=='shield-lock':
        req=_slip(-3.8,-1.2)
        _play(scene,FadeIn(req),run_time=.4)
        _cue(scene,'open')
        _play(scene,p['shackle'].animate.shift(UP*.35),run_time=.4)
        _play(scene,req.animate.move_to([3.7,-1.2,0]),run_time=1.5)
    elif name=='shield-question':
        req=_slip(2.25,-.75)
        _play(scene,FadeIn(req),run_time=.5)
        _play(scene,req.animate.move_to([4.1,1.05,0]),run_time=1.3)
        _play(scene,Create(Line([3.35,-.6,0],[4.8,-.6,0],color=DIM,stroke_width=7)),run_time=.5)
    elif name=='vpn-key':
        gate=Line([3,-1.1,0],[3,1.1,0],color=INK,stroke_width=8)
        _play(scene,Create(gate),run_time=.5)
        _play(scene,hero.animate.shift(RIGHT*1.05),run_time=1)
        _play(scene,gate.animate.shift(RIGHT*.8+UP*.8),run_time=.8)
    elif name=='data-check-double':
        checks=p['checks'];hero.remove(checks)
        _play(scene,Indicate(p['records'],color=INK,scale_factor=1.04),run_time=.8)
        _play(scene,Create(checks[0]),run_time=.5)
        _play(scene,Create(checks[1]),run_time=.5)
    elif name=='search-check-2':
        result=p['check'];hero.remove(result)
        _play(scene,p['lens'].animate.shift(LEFT*.65),run_time=.6)
        _play(scene,p['lens'].animate.shift(RIGHT*1.05),run_time=1)
        _play(scene,Create(result),run_time=.6)
    elif name=='track-changes':
        revision=p['revision'];hero.remove(revision)
        _play(scene,p['before'].animate.move_to([-3,0,0]),p['after'].animate.move_to([2.3,0,0]),run_time=1.1)
        revision.move_to([2.3,.12,0])
        _play(scene,Create(revision),run_time=.7)
    elif name=='receipt':
        rows=[p['row'+str(n)] for n in range(3)]
        hero.remove(*rows)
        for row in rows:_play(scene,Create(row),run_time=.65)
    elif name=='account-tree':
        edges=p['edges'];hero.remove(edges)
        _play(scene,Create(edges),run_time=.8)
        dot=Dot(p['nodes'][0].get_center(),radius=.12,color=TERRA)
        scene.remove(pulse);_play(scene,FadeIn(dot),run_time=.3)
        _play(scene,dot.animate.move_to(p['nodes'][1].get_center()),run_time=.9)
        dot2=Dot(p['nodes'][0].get_center(),radius=.12,color=INK)
        _play(scene,FadeIn(dot2),run_time=.3)
        _play(scene,dot2.animate.move_to(p['nodes'][2].get_center()),run_time=.9)
    elif name=='arrow-split':
        dot=Dot([-.4,-1.35,0],radius=.15,color=TERRA)
        scene.remove(pulse);_play(scene,FadeIn(dot),run_time=.3)
        _play(scene,dot.animate.move_to([-.4,0,0]),run_time=.7)
        other=Dot([-.4,0,0],radius=.15,color=INK)
        _play(scene,FadeIn(other),run_time=.2)
        _play(scene,dot.animate.move_to([1.25,1.4,0]),other.animate.move_to([-1.65,.55,0]),run_time=1)
    elif name=='rebase':
        _play(scene,p['branch'].animate.shift(UP*.72),run_time=1.5)
        _play(scene,Create(check(3.6,0,.3)),run_time=.6)
    elif name=='conveyor-belt':
        _play(scene,p['cargo'].animate.shift(RIGHT*2.15+UP*1.24),run_time=1.8)
        _play(scene,Create(Line([3.4,-.4,0],[3.4,1.1,0],color=INK,stroke_width=7)),run_time=.5)
    _done(scene)

class BCREDIT_Attribution(Scene):
    def construct(self):
        hero=make_prop('layers',scale=1.5)
        self.add(hero,_brand_bug(),T('Isocons',64).move_to([-3.7,2.6,0]),T('CC BY 4.0',60).move_to([3.3,2.6,0]),T('Adapted',56).move_to([0,-2.6,0]))
        _play(self,hero.parts['layer2'].animate.shift(UP*.5),run_time=1)
        _play(self,Create(check(3.8,-.2,.35)),run_time=.6)
        _done(self)
