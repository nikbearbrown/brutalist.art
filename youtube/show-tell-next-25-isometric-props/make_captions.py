"""Full-text word-aligned SRT on actual conformed clip offsets. No staging."""
import json,subprocess,textwrap
from pathlib import Path
R=Path(__file__).resolve().parent
sheet=json.loads((R/'beat_sheet.json').read_text());words=json.loads((R/'mp3/words.json').read_text())
fps=words['fps'];offsets={};t=0
for b in sheet['beats']:
    bid=b['beat_id'];offsets[bid]=t
    t+=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(R/'clips'/f'{bid}.mp4')]))
def stamp(s):
    ms=round(s*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);sec,ms=divmod(ms,1000)
    return f'{h:02}:{m:02}:{sec:02},{ms:03}'
cues=[];previous=0;emitted=[]
for b in sheet['beats']:
    ws=words['beats'][b['beat_id']];j=0
    while j<len(ws):
        group=[]
        while j<len(ws) and len(group)<9:
            group.append(ws[j]);j+=1
            if len(' '.join(w['text'] for w in group))>=60 or (len(group)>=4 and group[-1]['text'].endswith(('.', '?', '!'))):break
        start=max(previous,offsets[b['beat_id']]+group[0]['startFrame']/fps)
        end=max(start+.08,offsets[b['beat_id']]+group[-1]['endFrame']/fps)
        previous=end;emitted.extend(w['text'] for w in group)
        cues.append(f'{len(cues)+1}\n{stamp(start)} --> {stamp(end)}\n'+textwrap.fill(' '.join(w['text'] for w in group),42))
assert ' '.join(emitted)==' '.join(b['narration_text'] for b in sheet['beats'])
(R/f'{R.name}.srt').write_text('\n\n'.join(cues)+'\n')
print(len(cues),'cues; all narration retained; timeline',round(t,3),'seconds')
