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
