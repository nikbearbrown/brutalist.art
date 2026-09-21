#!/usr/bin/env python3
"""seis_composite.py — the seis-composite skill's engine (skills/make/seis-composite).

  python3 seis_composite.py plan.json --out film.mp4
plan.json (the editing brief's timeline as data):
  {"open": {"eyebrow": "SEIS · Alumni", "lines": ["Look what our people", "have gone on to do."], "seconds": 4},
   "sections": [{"eyebrow": "Who they are now", "lines": [...optional card...], "seconds": 2.5, "clips": ["clips/jay-01.mp4", ...]}, ...],
   "stat": {"eyebrow": "SEIS", "lines": ["112 spotlight stories", "…"], "emphasis": 0, "seconds": 4},          # optional, before the closing beat
   "bridge": {"lines": ["The name is changing.", "The mission isn’t."], "emphasis": 1, "seconds": 3, "dark": true},
   "end_seconds": 10, "music": "path/to/bed.mp3", "music_gain": 0.12}
Clips are the seis-extract outputs (or any mp4). Warns on any clip > 15 s. Composition SeisFilm. Never publishes.
"""
import argparse, json, math, shutil, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent; TOOLKIT = HERE.parent.parent
REM = TOOLKIT / 'runtime' / 'remotion'; PUB = REM / 'public' / 'seis-film'; FPS = 30

def dur(p): return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(p)], capture_output=True, text=True).stdout.strip())
def card(c, default_s=2.5, dark=False):
    return {'kind': 'card', 'frames': int(math.ceil(c.get('seconds', default_s) * FPS)), 'src': '', 'eyebrow': c.get('eyebrow', ''), 'lines': c.get('lines', []), 'emphasis': c.get('emphasis', -1), 'dark': c.get('dark', dark)}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('plan'); ap.add_argument('--out', required=True); a = ap.parse_args()
    plan = json.loads(Path(a.plan).read_text()); base = Path(a.plan).parent; PUB.mkdir(parents=True, exist_ok=True)
    items = []
    if plan.get('open'): items.append(card(plan['open'], 4))
    for sec in plan.get('sections', []):
        if sec.get('lines'): items.append(card(sec))
        for c in sec.get('clips', []):
            src = (base / c) if not Path(c).is_absolute() else Path(c); d = dur(src)
            if d > 15.5 + 6: print(f"  ! {src.name}: {d:.1f}s total — answer likely over the brief's 15 s cap")
            dst = PUB / src.name; shutil.copy2(src, dst)
            items.append({'kind': 'clip', 'frames': int(math.floor(d * FPS)), 'src': f'seis-film/{dst.name}', 'eyebrow': '', 'lines': [], 'emphasis': -1, 'dark': False})
    if plan.get('stat'): items.append(card(plan['stat'], 4))
    if plan.get('bridge'): items.append(card(plan['bridge'], 3, dark=True))
    items.append({'kind': 'end', 'frames': int(plan.get('end_seconds', 10) * FPS), 'src': '', 'eyebrow': '', 'lines': [], 'emphasis': -1, 'dark': False})
    music = ''
    if plan.get('music'):
        m = Path(plan['music']); dst = PUB / m.name; shutil.copy2(m, dst); music = f'seis-film/{dst.name}'
    props = {'items': items, 'music': music, 'musicGain': plan.get('music_gain', 0.12)}
    pj = Path(a.out).with_suffix('.props.json'); pj.write_text(json.dumps(props, ensure_ascii=False))
    total = sum(i['frames'] for i in items); print(f"{len(items)} items · {total/FPS:.1f}s")
    r = subprocess.run(['npx', 'remotion', 'render', 'src/index.ts', 'SeisFilm', str(Path(a.out).resolve()), f'--props={pj.resolve()}', '--codec=h264', '--crf=18', '--concurrency=4', '--log=error'], cwd=str(REM), capture_output=True, text=True)
    if r.returncode != 0: sys.exit(r.stderr[-1500:])
    print('wrote', a.out, f'({dur(a.out):.1f}s)')

if __name__ == '__main__': main()
