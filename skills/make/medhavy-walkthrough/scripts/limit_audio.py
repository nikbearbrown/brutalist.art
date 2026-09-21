#!/usr/bin/env python3
"""True-peak limit every per-beat track to audio/<id>-lim.wav (-1.5 dBTP, length unchanged)
and point the beat sheet at them. Run before `art final`; the stage loudness gate has no bypass.
Always reads the un-limited source (mp3/beat-<id>.mp3 for bookends, audio/<id>.wav for padded
footage narration and the spoken outro), so it is safe to re-run."""
import json, subprocess, sys
from pathlib import Path
reel = Path(sys.argv[1]).resolve(); sp = reel / 'beat_sheet.json'; sheet = json.loads(sp.read_text())
def dur(p): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(p)]))
for b in sheet['beats']:
    bid = b['beat_id']; af = b.get('audio_file', '')
    if af.endswith(f'{bid}-lim.wav'):
        src = (reel/'audio'/f'{bid}.wav') if (reel/'audio'/f'{bid}.wav').exists() else (reel/'mp3'/f'beat-{bid}.mp3')
    else:
        src = reel / af
    out = reel/'audio'/f'{bid}-lim.wav'
    subprocess.run(['ffmpeg','-v','error','-y','-i',str(src),'-af','aresample=48000,alimiter=limit=0.841:attack=5:release=50:level=false','-ar','48000','-ac','2',str(out)], check=True)
    assert abs(dur(src)-dur(out)) < 0.03, (bid, dur(src), dur(out))
    b['audio_file'] = f'audio/{bid}-lim.wav'; print(f'{bid}: {src.name} -> {out.name}')
sp.write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + '\n')
