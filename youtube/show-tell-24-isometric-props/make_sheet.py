"""Author the 24-prop demonstration; preserve existing audio when text is unchanged."""
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
SLUG=HERE.name
TITLE='Show-Tell: 24 Props That Explain'
# Prop, display label, action label, narration, visual event. Demonstrations are
# designed examples, not claims about a running Claude integration or benchmark.
DATA=[
('dataset','Dataset','Select',"Start with a dataset. Lift one record out of the collection. The motion distinguishes the evidence we actually inspect from everything we could inspect.","One cell leaves the dataset"),
('dataset-linked','Linked data','Connect',"Linked data adds a relationship. Join the connector to the records. A link tells us where material connects, not whether that material is reliable.","Separate chain joins the record plate"),
('layers','Layers','Separate',"Layers separate responsibilities. Lift the top layer while the others stay put. Use this to distinguish the interface, the agent, and the underlying service.","Top plane lifts away from two lower planes"),
('quick-reference','Reference','Retrieve',"A reference gives the worker a procedure when it is needed. Pull out the marked section. Keep instructions visually distinct from evidence about the world.","Bookmark pulls away from the reference"),
('terminal','Terminal','Run',"The terminal takes a request and returns a result. Watch the evidence slip enter, then a different slip emerge. An action has an observable consequence.","Request enters terminal and a separate result emerges"),
('linked-services','Services','Exchange',"Connected services exchange something specific. Draw the connection, then send a packet across it. Do not use a cable to imply unlimited access.","Connector draws and packet crosses between service blocks"),
('deployed-code','Deployment','Release',"Deployment moves a package into its operating position. Lower the code onto its platform. This shows delivery, not a guarantee that the software works correctly.","Code package lowers onto its platform"),
('network-node','Network','Route',"A network offers more than one route. Follow one packet through the nodes. Showing the chosen path is clearer than lighting up every connection at once.","One packet takes two edges in sequence"),
('person-raised-hand','Human review','Pause',"The raised hand means stop and ask. Raise it before the action continues. Human intervention belongs inside the workflow, not in a disclaimer after it.","Hand and arm rise while a request waits"),
('person-check','Reviewer','Approve',"A reviewer inspects a proposed result before approving it. Bring the evidence to the person, then add the check. Approval is a decision, not decoration.","Evidence arrives before the approval check"),
('handshake','Agreement','Accept',"Agreement needs two sides. Bring the hands together only after both are present. Use this for accepted terms or a shared task boundary, not automatic trust.","Two separated hands meet"),
('partner-exchange','Handoff','Transfer',"A handoff transfers responsibility. Move the same evidence slip from one person to another. The object persists, so the viewer can follow what changed hands.","Evidence slip moves from one person to another"),
('policy','Policy','Block',"A policy is a constraint that changes behavior. Let a request approach the boundary and stop. If the rule never affects the action, the picture teaches nothing.","Request hits a rule boundary and returns"),
('shield-lock','Permission','Unlock',"Permission is a gate. Keep the lock closed until access is granted, then open it. The shield represents this boundary, not proof that a system is secure.","Shackle lifts before a request passes"),
('shield-question','Uncertainty','Escalate',"Uncertainty should change the route. Send the unresolved case away for review. A question mark is useful only when the workflow does something about it.","Unresolved evidence moves away from the shield for review"),
('vpn-key','Access key','Authorize',"A key grants a particular capability. Move it to the access point. In your own lesson, name what it unlocks and what remains outside its scope.","Key reaches a closed access point, which then opens"),
('data-check-double','Cross-check','Compare',"Cross-check two records before adding either check mark. These symbols show the comparison step. They cannot tell us whether the underlying sources are independent or correct.","Two records remain visible before two checks appear"),
('search-check-2','Inspection','Find',"Inspection is an active search. Move the lens across the source, then mark the selected finding. Finding a passage and verifying its claim are different jobs.","Lens sweeps the source before finding is marked"),
('track-changes','Revision','Compare',"Revision needs a before and an after. Separate the versions and reveal the changed line. Keep enough history to explain why the new version is better.","Overlapping versions separate and a revision line appears"),
('receipt','Process record','Record',"A process record accumulates as work happens. Add each row in order. Record the action, the evidence, and the decision, not just the finished artifact.","Three record rows arrive sequentially"),
('account-tree','Delegation','Assign',"Delegation starts with a responsible owner. Draw the branches, then send work to each destination. Different workers need explicit tasks, not merely different boxes.","Edges draw from parent, then task packets reach two workers"),
('arrow-split','Decision','Branch',"A decision changes the path. Split the moving token into two possible routes. In a real workflow, state the condition that selects one route rather than both.","One incoming token becomes two explicitly illustrative alternatives"),
('rebase','Rebase','Move base',"Rebase is a code-history metaphor. Move the branch to a later base. This is a simplified illustration of changing its starting point, not a complete Git tutorial.","Side branch moves to a later point on the trunk"),
('conveyor-belt','Workflow','Advance',"A conveyor makes progress visible. Move the package along the belt, then stop it for review. Finishing the motion is not the same as passing the check.","Package advances and stops before the belt ends"),
]
SPARSE={'sparse_by_design':True,'sparse_reason':'Show-tell: one large native-vector prop and two readable labels. Only underfill and clustering waived.'}
def card(bid,narr,pattern,props,**extra):
    return dict(beat_id=bid,act='bookend',lane='bookend',proof_gate='SHOW',narration_text=narr,
        estimated_duration_s=round(len(narr.split())/2.5,2),voice='am_onyx',engine='kokoro',qc=SPARSE.copy(),
        shot={'type':'REMOTION','source':'own','show':[{'at':.1,'event':'Bookend content appears and settles'}],
              'remotion':{'pattern':pattern,'props':props}},**extra)
B=[card('BIDEA',"Hallo. This is Liam, in for Bear. Better teaching pictures do more than decorate. These twenty-four isometric props make actions visible: selecting evidence, granting permission, handing off work, and recording decisions.",
    'BrutalistHesitantWriter',{'text':'Teaching pictures should\ndecorate the explanation.','triggerWords':'decorate the explanation','replacementWords':'make the action visible',
    'fontSize':78,'charMs':22,'hesitateBetween':6,'hesitateWithin':1,'mistakeRate':2,'jitter':20,'seed':SLUG,'banner':''},lead_silence_s=.8),
   card('BDEFS',"Three terms. A prop is a reusable drawing. A state tells us what condition it is in. An action changes that condition. The picture shows the change; the voice explains why it matters.",
    'ClaudeDefinitions',{'title':'Terms In This Film','terms':[{'term':'prop','meaning':'A reusable drawing'},{'term':'state','meaning':'Its current condition'},{'term':'action','meaning':'A meaningful change'}],'folderLabel':'@NikBearBrown'})]
for n,(slug,label,action,narr,show) in enumerate(DATA):
    bid=f'B{n:02}'
    B.append(dict(beat_id=bid,act='show-tell',lane='manim',proof_gate='SHOW',narration_text=narr,
        estimated_duration_s=round(len(narr.split())/2.5,2),voice='am_onyx',engine='kokoro',qc=SPARSE.copy(),
        shot={'type':'GRAPHIC','source':'own','visual_intent':show,'motion_claim':show,
        'show':[{'at':.05,'event':label+' prop establishes the example'},{'at':.25,'event':show}],
        'manim':{'class':bid+'_Prop'},'prop_id':slug}))
B.append(dict(beat_id='BCREDIT',act='credit',lane='manim',proof_gate='SHOW',narration_text="These props are simplified redraws adapted from Isocons under Creative Commons Attribution four point zero. The shapes, colors, and animation have changed. Keep the source and license credit when you reuse them.",estimated_duration_s=13,voice='am_onyx',engine='kokoro',qc=SPARSE.copy(),shot={'type':'GRAPHIC','source':'own','visual_intent':'A reference sheet becomes a layered reusable prop; source and license remain visible','show':[{'at':.2,'event':'Layers separate, attribution stays'}],'manim':{'class':'BCREDIT_Attribution'}}))
PROMPT='Use Show-Tell to explain my workflow with three props. Show one human decision and one check of the evidence.'
B.extend([card('BHTF','Your turn. Paste this into Claude: '+PROMPT+' Then check the film yourself. Does every motion explain a change? Can you tell what the human decided?',
    'ClaudeComposerAsk',{'greeting':'Your turn.','topic':'CLAUDE · YOUR TURN','segment':'Make the Action Visible','command':PROMPT,'runningText':'paste this into Claude…',
    'output':['Check: every motion explains a change.','Check: the human decision is visible.'],'folderLabel':'@NikBearBrown','modelLabel':'Claude','effortLabel':'High','largeText':True}),
    card('BOUT',TITLE+'. At Nik Bear Brown.','ClaudeTitleOutro',{'title':TITLE,'slug':SLUG,'handle':'@NikBearBrown','subline':''},kind='outro_voice',tail_silence_s=1.)])
dest=HERE/'beat_sheet.json'
old={b['beat_id']:b for b in json.loads(dest.read_text())['beats']} if dest.exists() else {}
for b in B:
    prev=old.get(b['beat_id'],{})
    if prev.get('narration_text')==b['narration_text']:
        for key in ('audio_file','actual_duration_s'):
            if key in prev:b[key]=prev[key]
    if b['beat_id']=='BDEFS' and 'actual_duration_s' in b:b['shot']['remotion']['props']['durationSeconds']=b['actual_duration_s']
metadata=dict(slug=SLUG,title=TITLE,topic='CLAUDE · SHOW-TELL',skill='show-tell',style_preset='show-tell',channel='claude-liam',
    persona='Liam (in for Bear)',voice='am_onyx',voice_kokoro='am_onyx',engine='kokoro',clock='narration',palette='claude',register='Teardown',
    fps=24,aspect_ratio='16:9',width=3840,height=2160,caption_policy='none',playlist='Claude',chapter_number=1,
    bookend_exempt=['cold-open','bvdt'],bookend_exempt_reason='Show-tell opens with hesitant writer and definitions; no verdict. Your Turn and locked spoken outro retained.',
    source_doc='SOURCES.md; Isocons selected references and local native vector rig',tags=['Show-Tell','Isometric Icons','Conducting AI','Computational Skepticism','Claude'])
dest.write_text(json.dumps({'metadata':metadata,'beats':B},indent=2)+'\n')
print(len(B),'beats; estimated',round(sum(b['estimated_duration_s'] for b in B)),'seconds')
