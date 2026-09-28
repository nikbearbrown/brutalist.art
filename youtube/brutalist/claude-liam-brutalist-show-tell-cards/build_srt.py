#!/usr/bin/env python3
"""build_srt.py — full-text caption track for this reel.
The generic emitter (stage_publish.py) writes ONE cue per beat and truncates the
narration. This keeps the emitter's beat windows (already on the compiled clock)
and splits each beat's FULL narration_text into ≤ ~84-char cues, proportional by
word count. Run AFTER stage_publish.py, BEFORE ./art post.
"""
import json, re, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
slug = HERE.name
srt_path = HERE / f"{slug}.srt"
sheet = json.load(open(HERE / "beat_sheet.json"))
TS = re.compile(r"(\d{2}):(\d{2}):(\d{2}),(\d{3})")
def t2s(m): h, mi, s, ms = map(int, m.groups()); return h*3600 + mi*60 + s + ms/1000
def s2t(x):
    ms = int(round(x*1000)); h, ms = divmod(ms, 3600000); mi, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02d}:{mi:02d}:{s:02d},{ms:03d}"
blocks = [b for b in srt_path.read_text().strip().split("\n\n") if b.strip()]
windows = []
for b in blocks:
    lines = b.split("\n"); a, z = TS.findall(lines[1])[:2]
    windows.append((t2s(TS.match(":".join(a[:3]) + "," + a[3])), t2s(TS.match(":".join(z[:3]) + "," + z[3]))))
beats = [b for b in sheet["beats"] if b.get("narration_text")]
assert len(beats) == len(windows), (len(beats), len(windows))
MAX = 84
out, n = [], 0
for (t0, t1), beat in zip(windows, beats):
    words = beat["narration_text"].split()
    chunks, cur = [], []
    for w in words:
        if cur and len(" ".join(cur + [w])) > MAX and (cur[-1][-1] in ".,;:?!" or len(" ".join(cur)) > MAX * 0.7):
            chunks.append(" ".join(cur)); cur = [w]
        else:
            cur.append(w)
    if cur: chunks.append(" ".join(cur))
    total = sum(len(c.split()) for c in chunks); t = t0
    for c in chunks:
        d = (t1 - t0) * len(c.split()) / total; n += 1
        out.append(f"{n}\n{s2t(t)} --> {s2t(min(t + d, t1) - 0.02)}\n{c}\n"); t += d
srt_path.write_text("\n".join(out))
print(f"[srt] {n} cues → {srt_path.name}")
