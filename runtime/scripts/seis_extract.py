#!/usr/bin/env python3
"""seis_extract.py — the seis-extract skill's engine (skills/make/seis-extract).

  transcribe <video.mp4> [--model small]            → <stem>.transcript.json + .md (word timestamps; pick pulls against the brief)
  cut <video.mp4> --pulls pulls.json --out <dir>     → one branded Q&A clip per pull: Bella asks (Kokoro af_bella, question typed on
                                                       the SEIS page) → the alum answers (segment, lower third naming the PROGRAM,
                                                       burned captions from the transcript). Sidecar <id>.json per clip for seis-composite.
pulls.json:
  {"alum": {"name": "...", "program": "MS Information Systems · SEIS", "gradYear": "2024", "title": "...", "company": "..."},
   "pulls": [{"id": "dhan-01", "section": "now", "question": "What do you do today?", "in": "0:19", "out": "0:34"}, ...]}
Optional top-level "frame": {"zoom": 1.3, "cx": 0.37, "cy": 0.5} reframes a Teams/Zoom recording onto the speaker (crops out side tiles);
in/out may also be "~a phrase from the transcript" — resolved to the word timings (in = phrase start, out = phrase end).
optional "corrections": {"Dhunvardini Rajendra": "Dhanvardini Rajendran", "SAIS": "SEIS"} fixes whisper's proper nouns in the burned captions.
Sections: now · turning-point · became · forward · closing (the editing brief's timeline). No answer clip over 15 s (warned).
Free, local: faster-whisper + kokoro-onnx + ffmpeg + Remotion (composition SeisQA). Never publishes.
"""
import argparse, json, math, subprocess, sys, os, re
from pathlib import Path
HERE = Path(__file__).resolve().parent; TOOLKIT = HERE.parent.parent
CORR = {}   # the active pulls.json corrections map (set in cut) — phrase anchors try both spellings
REM = TOOLKIT / 'runtime' / 'remotion'; PUB = REM / 'public' / 'seis-qa'
KOKORO = TOOLKIT / 'runtime' / 'models' / 'kokoro'
FPS = 30

def tsec(v, transcript=None, side='in'):
    """seconds from a number, "m:ss", or "~phrase" (resolved against the transcript's words — first match after any earlier pull is the author's job)."""
    if isinstance(v, (int, float)): return float(v)
    if isinstance(v, str) and v.startswith('~') and transcript is not None:
        from difflib import SequenceMatcher
        words = [w for seg in transcript['segments'] for w in seg['words']]
        # try the phrase as written AND with every correction reversed (Teams spelling → whisper spelling),
        # so an anchor copied from the .docx still lands on whisper's "Dhunvardini" / "Karl Bugraura"
        variants = {v[1:].lower()}
        for wrong, right in (CORR or {}).items():
            variants |= {x.replace(right.lower(), wrong.lower()) for x in list(variants) if right.lower() in x}
        best, bi, bn = 0.0, 0, 1
        for ph in variants:
            target = re.findall(r"[a-z0-9']+", ph); n = len(target)
            for i in range(0, max(1, len(words) - n + 1)):
                cand = [re.sub(r"[^a-z0-9']", '', w['w'].lower()) for w in words[i:i+n]]
                r = SequenceMatcher(None, target, cand).ratio()
                if r > best: best, bi, bn = r, i, n
        if best < 0.6: sys.exit(f"phrase not found in transcript: {v!r} (best match {best:.2f}) — anchor to whisper's words in <stem>.transcript.md")
        return words[bi]['s'] - 0.15 if side == 'in' else words[min(len(words)-1, bi + bn - 1)]['e'] + 0.25
    p = [float(x) for x in str(v).split(':')]
    return p[0] * 60 + p[1] if len(p) == 2 else p[0] * 3600 + p[1] * 60 + p[2] if len(p) == 3 else p[0]

def sh(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0: sys.exit(f"FAILED: {' '.join(str(c) for c in cmd[:6])}…\n{r.stderr[-1200:]}")
    return r

def transcribe(video: Path, model='small'):
    from faster_whisper import WhisperModel
    wav = video.with_suffix('.16k.wav'); sh(['ffmpeg', '-loglevel', 'error', '-y', '-i', str(video), '-ac', '1', '-ar', '16000', str(wav)])
    m = WhisperModel(model, device='cpu', compute_type='int8')
    segs, info = m.transcribe(str(wav), word_timestamps=True, vad_filter=True)
    out, lines = [], []
    for s in segs:
        out.append({'start': s.start, 'end': s.end, 'text': s.text.strip(), 'words': [{'w': w.word.strip(), 's': w.start, 'e': w.end} for w in (s.words or [])]})
        lines.append(f"[{int(s.start)//60}:{int(s.start)%60:02d}] {s.text.strip()}")
    tj = video.with_suffix('.transcript.json'); tm = video.with_suffix('.transcript.md')
    tj.write_text(json.dumps({'source': video.name, 'duration': info.duration, 'segments': out}, indent=1, ensure_ascii=False))
    tm.write_text(f"# Transcript — {video.name}\n\n" + '\n'.join(lines) + '\n'); wav.unlink(missing_ok=True)
    print(f"{tm}  ({len(out)} segments, {info.duration:.0f}s)")

def bella(text: str, out_mp3: Path):
    import numpy as np, soundfile as sf
    from kokoro_onnx import Kokoro
    k = Kokoro(str(KOKORO / 'kokoro-v1.0.onnx'), str(KOKORO / 'voices-v1.0.bin'))
    a, sr = k.create(text, voice='af_bella', speed=1.0, lang='en-us')
    wav = out_mp3.with_suffix('.wav'); sf.write(str(wav), a, sr)
    sh(['ffmpeg', '-loglevel', 'error', '-y', '-i', str(wav), '-codec:a', 'libmp3lame', '-q:a', '3', str(out_mp3)]); wav.unlink()
    return len(a) / sr

def captions_for(transcript, t0, t1, max_words=6, max_s=2.4, corrections=None):
    words = [w for seg in transcript['segments'] for w in seg['words'] if w['s'] >= t0 - 0.05 and w['e'] <= t1 + 0.05]
    chunks, cur = [], []
    for w in words:
        if cur and (len(cur) >= max_words or w['e'] - cur[0]['s'] > max_s or re.search(r'[.?!]$', cur[-1]['w'])):
            chunks.append(cur); cur = []
        cur.append(w)
    if cur: chunks.append(cur)
    def fix(t):
        for a, b in (corrections or {}).items(): t = re.sub(re.escape(a), b, t, flags=re.I)
        return t
    return [{'t': fix(' '.join(w['w'] for w in c)), 's': int((c[0]['s'] - t0) * FPS), 'e': int((c[-1]['e'] - t0 + 0.35) * FPS)} for c in chunks]

def cut(video: Path, pulls_path: Path, out: Path):
    plan = json.loads(pulls_path.read_text()); default = plan.get('alum', {}); fr = plan.get('frame') or {}; corr = plan.get('corrections') or {}
    global CORR; CORR = corr
    tj = video.with_suffix('.transcript.json')
    if not tj.exists(): transcribe(video)
    transcript = json.loads(tj.read_text()); PUB.mkdir(parents=True, exist_ok=True); out.mkdir(parents=True, exist_ok=True)
    for p in plan['pulls']:
        pid = p['id']; t0, t1 = tsec(p['in'], transcript, 'in'), tsec(p['out'], transcript, 'out'); alum = dict(default, **p.get('alum', {}))
        if t1 - t0 > 15.5: print(f"  ! {pid}: answer is {t1-t0:.1f}s — the brief caps clips at ~15 s")
        qmp3 = PUB / f'{pid}-q.mp3'; qdur = bella(p['question'], qmp3)
        clip = PUB / f'{pid}.mp4'
        z = float(fr.get('zoom', 1.0)); cx, cy = float(fr.get('cx', 0.5)), float(fr.get('cy', 0.5))
        crop = f"crop=iw/{z}:ih/{z}:iw*{cx}-iw/{z}/2:ih*{cy}-ih/{z}/2," if z > 1.0 else ''
        sh(['ffmpeg', '-loglevel', 'error', '-y', '-ss', f'{t0:.3f}', '-to', f'{t1:.3f}', '-i', str(video), '-vf', crop + 'scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=30',
            '-c:v', 'libx264', '-crf', '18', '-preset', 'fast', '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', str(clip)])
        props = {'question': p['question'], 'questionAudio': f'seis-qa/{qmp3.name}', 'questionFrames': int(math.ceil((qdur + 0.7) * FPS)),
                 'clip': f'seis-qa/{clip.name}', 'clipFrames': int(math.ceil((t1 - t0) * FPS)),
                 'name': alum.get('name', ''), 'program': alum.get('program', 'SEIS'), 'gradYear': str(alum.get('gradYear', '')), 'title': alum.get('title', ''), 'company': alum.get('company', ''),
                 'captions': captions_for(transcript, t0, t1, corrections=corr), 'logo': 'seis/seis-button-logo.jpg', 'lockup': 'seis/seis-logo.png'}
        pj = out / f'{pid}.props.json'; pj.write_text(json.dumps(props, ensure_ascii=False))
        final = out / f'{pid}.mp4'
        sh(['npx', 'remotion', 'render', 'src/index.ts', 'SeisQA', str(final), f'--props={pj.resolve()}', '--codec=h264', '--crf=18', '--concurrency=4', '--log=error'], cwd=str(REM))
        side = {'id': pid, 'section': p.get('section', ''), 'question': p['question'], 'in': t0, 'out': t1, 'alum': alum,
                'frames': props['questionFrames'] + props['clipFrames'], 'seconds': round((props['questionFrames'] + props['clipFrames']) / FPS, 2), 'file': str(final), 'source': video.name}
        (out / f'{pid}.json').write_text(json.dumps(side, indent=1, ensure_ascii=False))
        print(f"  ✓ {pid}  [{p.get('section','')}]  Q {qdur:.1f}s + A {t1-t0:.1f}s → {final.name}")

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest='cmd', required=True)
    a = sub.add_parser('transcribe'); a.add_argument('video'); a.add_argument('--model', default='small')
    c = sub.add_parser('cut'); c.add_argument('video'); c.add_argument('--pulls', required=True); c.add_argument('--out', required=True)
    args = ap.parse_args()
    if args.cmd == 'transcribe': transcribe(Path(args.video), args.model)
    else: cut(Path(args.video), Path(args.pulls), Path(args.out))
