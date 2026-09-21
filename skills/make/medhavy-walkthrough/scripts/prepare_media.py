#!/usr/bin/env python3
"""Cut footage beats frame-exact from a capture, pad narration to the action
clock, and pad the spoken outro (title + "At Nik Bear Brown") with a 1 s tail. Never retimes footage.

  prepare_media.py REEL [--fps 30]

Reads beat_sheet.json: beats with `source_capture` + `source_seconds` [start,end]
become media/<id>.mp4 (silent) and audio/<id>.wav (narration apad to the clip).
Narration longer than the clip is an error: rewrite narration, never stretch action.
The OUTRO beat is spoken (kind outro_voice): Kokoro take + 1.0 s silent tail. No jingle.
"""
import argparse, hashlib, json, math, shutil, subprocess, sys
from pathlib import Path

def sha(p):
    with open(p, 'rb') as f: return hashlib.file_digest(f, 'sha256').hexdigest()
def seconds(p):
    return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(p)]))
def nframes(p):
    return int(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-count_frames','-show_entries','stream=nb_read_frames','-of','default=nw=1:nk=1',str(p)]))

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('reel', type=Path); ap.add_argument('--fps', type=int, default=30)
    a = ap.parse_args(); reel = a.reel.resolve(); fps = a.fps
    art_home = Path(__file__).resolve().parents[4]
    sheet_p = reel / 'beat_sheet.json'; sheet = json.loads(sheet_p.read_text())
    cov = json.loads((reel / 'coverage.json').read_text())
    (reel / 'media').mkdir(exist_ok=True); (reel / 'audio').mkdir(exist_ok=True)
    manifest = []
    for b in sheet['beats']:
        bid = b['beat_id']
        if 'source_seconds' in b:
            cap = cov['captures'][b['source_capture']]; src = reel / cap['path']
            assert sha(src) == cap['sha256'], f'{bid}: capture hash mismatch'
            s0, s1 = b['source_seconds']; f0 = round(s0 * fps); n = round((s1 - s0) * fps); dur = n / fps
            out = reel / 'media' / f'{bid}.mp4'
            subprocess.run(['ffmpeg','-v','error','-y','-i',str(src),'-vf',f'select=gte(n\\,{f0}),setpts=PTS-STARTPTS','-frames:v',str(n),
                            '-c:v','libx264','-preset','medium','-crf','14','-pix_fmt','yuv420p','-r',str(fps),'-an',str(out)], check=True)
            assert nframes(out) == n, f'{bid}: frame count mismatch'
            narr = reel / 'mp3' / f'beat-{bid}.mp3'; nd = seconds(narr)  # always the Kokoro take, never the padded output
            assert nd <= dur + 0.02, f'{bid}: narration {nd:.2f}s exceeds clip {dur:.2f}s; rewrite narration, never stretch action'
            wav = reel / 'audio' / f'{bid}.wav'
            subprocess.run(['ffmpeg','-v','error','-y','-i',str(narr),'-af',f'aresample=48000,apad,atrim=duration={dur:.6f}','-ar','48000','-ac','2',str(wav)], check=True)
            assert abs(seconds(wav) - dur) < 0.02
            b.update(audio_file=f'audio/{bid}.wav', actual_duration_s=dur, render_duration_s=dur, source_frames=[f0, f0 + n], source_fps=fps,
                     narration_duration_s=round(nd, 2), hold_note=f'narration {nd:.2f}s padded with silence to the {dur:.2f}s action clock; no retiming')
            manifest.append(dict(beat_id=bid, path=f'media/{bid}.mp4', sha256=sha(out), source_capture=b['source_capture'], source_frames=[f0, f0+n], fps=fps, duration_s=dur, retiming=False))
            print(f'{bid}: {dur:.2f}s clip from {s0}s, narration {nd:.2f}s', flush=True)
        elif b.get('kind') in ('outro_jingle', 'outro_voice') or b.get('act') == 'OUTRO':
            # OUTRO-LOCK §Voice (2026-09-18): spoken, never scored. Liam's take + 1.0 s silent tail hold.
            narr = reel / 'mp3' / f'beat-{bid}.mp3'; assert narr.exists(), f'{bid}: outro narration missing; narration_text must be "<title>. At Nik Bear Brown."'
            nd = seconds(narr); dur = math.ceil((nd + 1.0) * fps - 1e-8) / fps
            wav = reel / 'audio' / f'{bid}.wav'
            subprocess.run(['ffmpeg','-v','error','-y','-i',str(narr),'-af',f'aresample=48000,apad,atrim=duration={dur:.6f}','-ar','48000','-ac','2',str(wav)], check=True)
            for k in ('jingle_source', 'jingle_sha256'): b.pop(k, None)
            b.update(kind='outro_voice', audio_file=f'audio/{bid}.wav', actual_duration_s=dur, render_duration_s=dur, narration_duration_s=round(nd, 2),
                     hold_note=f'spoken outro {nd:.2f}s + 1.0s silent tail; no jingle (OUTRO-LOCK §Voice)')
            b['shot']['remotion']['props']['durationSeconds'] = dur
            print(f'{bid}: spoken outro {nd:.2f}s + tail = {dur:.2f}s', flush=True)
        else:
            d = b.get('actual_duration_s'); assert d, f'{bid}: no measured audio'
            b['render_duration_s'] = math.ceil(d * fps - 1e-8) / fps
    sheet_p.write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + '\n')
    (reel / 'capture' / 'clip-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print('total timeline', round(sum(b['render_duration_s'] for b in sheet['beats']), 2), 's')

if __name__ == '__main__':
    sys.exit(main())
