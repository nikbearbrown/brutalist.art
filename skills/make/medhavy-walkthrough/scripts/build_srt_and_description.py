#!/usr/bin/env python3
"""Full-text SRT (cues split within each beat, timed over the measured narration)
and a YouTube description with exact chapter offsets from the beat clocks.

  build_srt_and_description.py REEL [--to TOPOST_DIR] [--chapters "B00=Intro,B02=Admin overview,..."]
"""
import argparse, json, re, subprocess, textwrap
from pathlib import Path

def dur(p): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(p)]))
def ts(s):
    ms=int(round(s*1000)); h,ms=divmod(ms,3600000); m,ms=divmod(ms,60000); sec,ms=divmod(ms,1000); return f'{h:02d}:{m:02d}:{sec:02d},{ms:03d}'
def mmss(s): return f'{int(s)//60}:{int(s)%60:02d}'

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('reel',type=Path); ap.add_argument('--to',type=Path); ap.add_argument('--chapters',default='')
    a=ap.parse_args(); reel=a.reel.resolve(); sheet=json.loads((reel/'beat_sheet.json').read_text()); slug=sheet['metadata']['slug']
    chap={k:v for k,v in (x.split('=',1) for x in a.chapters.split(',') if '=' in x)}
    cues=[]; t0=0.0; offsets={}
    for b in sheet['beats']:
        bid=b['beat_id']; rd=float(b['render_duration_s']); offsets[bid]=t0
        text=(b.get('narration_text') or '').strip()
        if text:
            narr=reel/'mp3'/f'beat-{bid}.mp3'; nd=dur(narr) if narr.exists() else rd
            nd=min(nd, rd)
            sents=re.split(r'(?<=[.!?])\s+', text); chunks=[]
            for s in sents:
                for piece in textwrap.wrap(s, 84) if len(s)>84 else [s]:
                    if chunks and len(chunks[-1])+1+len(piece)<=84: chunks[-1]+=' '+piece
                    else: chunks.append(piece)
            total=sum(len(c) for c in chunks); cur=t0
            for i,c in enumerate(chunks):
                d=nd*len(c)/total; end=cur+d-(0.05 if i<len(chunks)-1 else 0)
                cues.append((cur,end,'\n'.join(textwrap.wrap(c,42))))
                cur+=d
        t0+=rd
    srt='\n'.join(f'{i+1}\n{ts(s)} --> {ts(e)}\n{txt}\n' for i,(s,e,txt) in enumerate(cues))
    (reel/f'{slug}.srt').write_text(srt)
    # description
    md=sheet['metadata']; title=md['title']
    beats={b['beat_id']:b for b in sheet['beats']}
    by_act={b.get('act'):b for b in sheet['beats']}
    hook=by_act.get('OVERVIEW',sheet['beats'][1])['narration_text']; verdict=by_act['VERDICT']['narration_text']; yt=by_act['NEXT STEPS']['shot']['remotion']['props']['command']
    lines=[f'# {title}','',hook,'',verdict,'','---','','## Chapters','']
    for bid,label in chap.items():
        if bid in offsets: lines.append(f'{mmss(offsets[bid])} {label}')
    lines+=['','---','','## YOUR TURN','','Paste into Claude Code from the medhavi-hub repo:','','```',yt,'```','',
            'One book, one student, one comparison. Then ask a person to use it.','','---','',
            'Real screen capture of the live Medhavy Hub admin, driven by a scripted browser. Every student name, email and invite code was masked in the page before recording. Narration: Liam, in for Bear (Kokoro). Built with the brutalist.art `medhavy-walkthrough` skill; no paid generation.','',
            '**@NikBearBrown**','','#MedhavyHub #OpenTextbooks #EdTech #Clerk #Supabase #NextJS #Claude #ClaudeCode #NikBearBrown','','---','',
            '*Sources: the medhavi-hub repository (README, DEVELOPER.md, docs/) at commit efcc3f5; see the reel\'s SOURCES.md.*']
    desc='\n'.join(lines)+'\n'
    (reel/f'{slug}-youtube.md').write_text(desc)
    if a.to: (a.to/f'{slug}.srt').write_text(srt); (a.to/f'{slug}.md').write_text(desc)
    print(f'{len(cues)} cues; chapters: '+', '.join(f'{mmss(offsets[b])} {l}' for b,l in chap.items() if b in offsets)); print(f'description {len(desc.encode())} bytes')
if __name__=='__main__': main()
