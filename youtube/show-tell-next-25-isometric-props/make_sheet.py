"""Candidate batch 25–49: actual vector demonstrations, not product claims."""
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent;SLUG=HERE.name
TITLE='Show-Tell: 25 More Props for Design and Learning'
# id, label, verb, narration, visible action, word cue
DATA=[
('prompt-suggestion','Suggestion','Choose','A suggestion offers a starting point. Move the proposed instruction toward the arrow, then leave room to revise it. Suggested does not mean required.','Suggestion slip approaches the arrow','Move'),
('question-exchange','Clarification','Ask back','Clarification sends a question back before work continues. Separate the two directions. Use this when missing context matters more than producing an immediate answer.','Upper and lower arrows separate around the question','Separate'),
('token','Token','Allocate','A token can stand for a unit in a budget. Separate one segment from the rest. This is a teaching metaphor, not a literal drawing of language tokenization.','One segment leaves the token ring','Separate'),
('filter','Filter','Narrow','A filter narrows a collection according to a rule. Move a record past successive levels. The rule must be stated; filtering alone does not make information trustworthy.','One record passes three filtering levels','Move'),
('sort','Sort','Reorder','Sorting changes order without changing the collection. Swap the short and long bars. Name the ordering rule before interpreting whichever item ends up first.','Short and long bars swap vertical positions','Swap'),
('dynamic-form','Adaptive form','Reveal','An adaptive form asks a follow-up question only when it applies. Reveal the second field after the first choice. More fields are not automatically more useful.','Second field appears after an initial choice','Reveal'),
('responsive-layout','Responsive design','Reflow','Responsive design preserves the task across different screens. Separate the desktop, tablet, and phone. The layout can change while the essential decision stays available.','Three screen silhouettes spread apart','Separate'),
('sliders','Adjustment','Tune','A slider makes a range adjustable. Move the handle along its track. Name what changes and provide a way to understand the selected value without guessing from position.','Handle travels on the isometric rail','Move'),
('toggle-on','Explicit choice','Switch','A toggle expresses a two-state choice. Move it from one end to the other. For a consequential action, make the current state clear before anything happens.','Knob moves from off position to on position','Move'),
('settings-accessibility','Accessibility','Support','Accessibility is support for completing a task, not a decorative badge. Bring the support into place beneath the figure. Then test the real experience with its users.','Support platform arrives beneath the figure','Bring'),
('highlight-keyboard-focus','Keyboard focus','Advance','Keyboard focus shows where the next action will land. Move the focus marker between controls. A visible ring should track navigation, not remain around the first item.','Focus marker travels between two control targets','Move'),
('data-alert','Data warning','Investigate','A data warning interrupts an assumption. Reveal the warning, then pull out the affected record. The next step is investigation, not turning the warning into a reassuring check.','Warning appears before a record separates','Reveal'),
('sync-problem','Sync failure','Stop','A failed exchange should stop the next handoff. Bring the outgoing record to the broken connection and hold it. Do not show movement that suggests delivery succeeded.','Outgoing slip stops at the broken connection','Bring'),
('undo','Undo','Reverse','Undo returns from a recent action to its earlier state. Move the same record back. Keep it distinct from restoring an older backup, which may replace more work.','Record moves out and returns along the same route','Move'),
('settings-backup-restore','Restore','Recover','Restore recovers a saved state. Bring the snapshot back into the recovery ring. Name which snapshot you used, and verify what changed after the restoration.','Saved snapshot returns to the recovery ring','Bring'),
('deployed-code-history','Release history','Inspect','Release history connects a deployed package to earlier decisions. Move the clock beside the package, then reveal a record. A timestamp alone cannot explain why the release changed.','Clock and record become visible beside package','Move'),
('view-kanbab','Work board','Advance','A work board makes status visible. Move one task between columns. Define what the destination means; arriving in a done column is not evidence that the work passed review.','One task changes columns on the board','Move'),
('timeline','Timeline','Trace','A timeline preserves sequence. Follow the events in order. This schematic has no time scale, so the distances between events do not claim how long anything took.','Marker follows four ordered events','Follow'),
('query-stats','Metric inquiry','Inspect','A metric needs a question. Move the lens toward the change in this illustrative trend. Ask what was measured and what evidence could support a different interpretation.','Lens approaches a bend in a schematic trend','Move'),
('data-table','Table','Inspect row','A table keeps records comparable. Pull one row aside while the other rows remain. Use this when the lesson depends on inspecting an individual case within a collection.','Middle row separates from the table','Pull'),
('quiz','Retrieval practice','Attempt','A quiz asks the learner to try before seeing the answer. Move the question aside and reveal a response card. The teaching value comes from the attempt and feedback.','Question yields to a response card after a pause','Move'),
('local-library','Reference reading','Open','Reference reading connects a person to material they can inspect. Open the two pages around the reader. Show the source itself when the lesson turns on its exact wording.','Book pages separate beneath reader','Open'),
('lab-research','Experiment','Test','An experiment changes something so its consequences can be examined. Lower the instrument toward the sample. This prop represents a test; it does not provide a test result.','Instrument approaches the sample stage','Lower'),
('map','Orientation','Unfold','A map reveals relationships that one isolated location cannot show. Unfold the three panels. For a workflow map, label the places people actually need to find.','Three folded map panels separate','Unfold'),
('flag','Milestone','Mark','A milestone marks a condition worth checking. Raise the flag after the work reaches that point. Keep the milestone separate from a claim that the whole project is complete.','Flag rises on pole and a record arrives','Raise')]
SPARSE={'sparse_by_design':True,'sparse_reason':'Show-tell: one large vector prop with two clear labels; deliberate negative space.'}
def card(bid,narr,pattern,props,**extra):
 return dict(beat_id=bid,act='bookend',lane='bookend',proof_gate='SHOW',narration_text=narr,estimated_duration_s=len(narr.split())/2.5,
 voice='am_onyx',engine='kokoro',qc=SPARSE.copy(),shot={'type':'REMOTION','source':'own','show':[{'at':.1,'event':'Bookend settles'}],'remotion':{'pattern':pattern,'props':props}},**extra)
B=[card('BIDEA','Bonjour. This is Liam, in for Bear. Here are twenty-five more candidate props. Each one shows a design choice, a recovery step, or a learning action. Judge what the motion explains, not just how the icon looks.',
 'BrutalistHesitantWriter',dict(text='Choose a prop for\nhow it looks.',triggerWords='how it looks',replacementWords='what it explains',fontSize=78,charMs=22,hesitateBetween=6,hesitateWithin=1,mistakeRate=2,jitter=20,seed=SLUG,banner=''),lead_silence_s=.8),
 card('BDEFS','Three terms. A control changes a setting. Recovery returns work to a usable state. Evidence supports a judgment. These drawings are teaching examples, not reports of tests we have run.',
 'ClaudeDefinitions',dict(title='Terms In This Film',terms=[dict(term='control',meaning='Changes a setting'),dict(term='recovery',meaning='Returns to a usable state'),dict(term='evidence',meaning='Supports a judgment')],folderLabel='@NikBearBrown'))]
for n,(slug,label,verb,narr,event,cue) in enumerate(DATA):
 bid=f'B{n:02}'
 B.append(dict(beat_id=bid,act='show-tell',lane='manim',proof_gate='SHOW',narration_text=narr,estimated_duration_s=len(narr.split())/2.5,
 voice='am_onyx',engine='kokoro',qc=SPARSE.copy(),shot={'type':'GRAPHIC','source':'own','visual_intent':event,'motion_claim':event,'show':[{'at':.05,'event':label+' appears'},{'at':cue,'event':event}],'manim':{'class':bid+'_Prop'},'prop_id':slug}))
B.append(dict(beat_id='BCREDIT',act='credit',lane='manim',proof_gate='SHOW',narration_text='These twenty-five candidates are simplified adaptations of Isocons, under Creative Commons Attribution four point zero. Geometry, colors, and motion have changed. They are awaiting library selection; keep the source credit when reusing them.',estimated_duration_s=13,voice='am_onyx',engine='kokoro',qc=SPARSE.copy(),shot={'type':'GRAPHIC','source':'own','show':[{'at':.2,'event':'Three map panels separate while the license stays visible'}],'manim':{'class':'BCREDIT_Attribution'}}))
PROMPT='Use Show-Tell to explain a task I teach. Choose three props. Show a learner action, a possible failure, and the evidence needed to continue.'
B.extend([card('BHTF','Your turn. Paste this into Claude: '+PROMPT+' Review the result. Can you follow the action without reading a paragraph? Does the film distinguish a symbol from evidence?',
 'ClaudeComposerAsk',dict(greeting='Your turn.',topic='CLAUDE · YOUR TURN',segment='Choose What Explains',command=PROMPT,runningText='paste this into Claude…',output=['Check: the action is visible.','Check: symbols are not evidence.'],folderLabel='@NikBearBrown',modelLabel='Claude',effortLabel='High',largeText=True)),
 card('BOUT',TITLE+'. At Nik Bear Brown.','ClaudeTitleOutro',dict(title=TITLE,slug=SLUG,handle='@NikBearBrown',subline=''),kind='outro_voice',tail_silence_s=1.)])
dest=HERE/'beat_sheet.json';old={b['beat_id']:b for b in json.loads(dest.read_text())['beats']} if dest.exists() else {}
for b in B:
 prev=old.get(b['beat_id'],{})
 if prev.get('narration_text')==b['narration_text']:
  for key in ('audio_file','actual_duration_s'):
   if key in prev:b[key]=prev[key]
 if b['beat_id']=='BDEFS' and 'actual_duration_s' in b:b['shot']['remotion']['props']['durationSeconds']=b['actual_duration_s']
metadata=dict(slug=SLUG,title=TITLE,topic='CLAUDE · SHOW-TELL',skill='show-tell',style_preset='show-tell',channel='claude-liam',persona='Liam (in for Bear)',voice='am_onyx',voice_kokoro='am_onyx',engine='kokoro',clock='narration',palette='claude',register='Teardown',fps=24,aspect_ratio='16:9',width=3840,height=2160,caption_policy='none',playlist='Claude',chapter_number=2,bookend_exempt=['cold-open','bvdt'],bookend_exempt_reason='Show-Tell uses hesitant writer, definitions, Your Turn and locked spoken outro; no verdict.',tags=['Show-Tell','Isometric Icons','Conducting AI','Computational Skepticism','Educational AI'])
dest.write_text(json.dumps(dict(metadata=metadata,beats=B),indent=2)+'\n')
print(len(B),'beats; audio still determines actual duration')
