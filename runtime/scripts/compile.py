#!/usr/bin/env python3
"""compile.py — the explainer slot compiler + assembler.

Every beat on the timeline is a conformed per-beat mp4 in clips/.
Slot precedence:  media/<beat>.mp4  >  manim/<beat>.(mp4|mov)  >
                  media/<beat>.png (animated per shot.motion)  >  slate.
Rebuild recompiles ONLY slots whose input changed (sha1 manifest), then
re-concats and muxes the master audio. Every compile STAMPS the beat sheet:
each beat gets a `build` record (status/src/filled_by/needs) and metadata.build
summarizes the cut — the sheet is a build record, not just an intent document.
A skin lint warns when the sheet claims a brand contract its beats don't
request (e.g. palette=claude with no ClaudeComposerAsk cold open, or a sheet
with zero machine-renderable beats). Annotations/captions are NOT this
script's job — they belong to the Remotion assembly plane. The --review flag
burns global timecode + per-beat id/status at assembly only; clips/ stay clean.

Text rendering is PORTABLE: slates and review labels are drawn with Pillow and
overlaid as PNGs, so this works on ffmpeg builds without the drawtext filter
(e.g. Homebrew's freetype-less bottle). If drawtext exists, a running global
timecode is added too; if not, each review label carries its time range.

Usage:
  python3 scripts/compile.py reels/<slug> [--review] [--fps 24]
         [--height 720] [--audio path/to/master.(mp3|wav)] [--force]

Free/local. No API calls. ffmpeg + Pillow + Python stdlib.
"""
import argparse, hashlib, json, os, shutil, subprocess, sys, tempfile, re, copy, math
from datetime import datetime, timezone
from collections import Counter
from pathlib import Path
from build_safety import (BuildError, ApprovalError, atomic_json, file_digest,
                          is_source_report, intentional_silence, positive_duration,
                          require_paperwork, validate_approvals, validate_project,
                          writable_path, record_failure, require_short_duration)

FFMPEG = shutil.which("ffmpeg") or "ffmpeg"
FFPROBE = shutil.which("ffprobe") or "ffprobe"
INK_RGB = (47, 42, 38)        # #2F2A26
CREAM_RGB = (243, 235, 221)   # #F3EBDD
LADDER_RETIME = 0.05          # retime silently within ±5%
LADDER_REFUSE = 0.15          # >15% short → loud warning (still freeze-padded)

def sh(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        raise BuildError(f"[art] command failed:\n{' '.join(map(str, cmd))}\n{r.stderr[-1200:]}")
    return r

def probe_dur(path):
    r = subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return None

def probe_wh(path):
    r = subprocess.run([FFPROBE, "-v", "error", "-select_streams", "v:0",
                        "-show_entries", "stream=width,height", "-of", "csv=p=0",
                        str(path)], capture_output=True, text=True)
    try:
        vals = r.stdout.strip().splitlines()[0].split(",")
        return int(vals[0]), int(vals[1])
    except (ValueError, IndexError):
        return None, None

def sha1(path, extra=""):
    h = hashlib.sha1(); h.update(extra.encode())
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def has_drawtext():
    import os
    if os.environ.get("ART_NO_DRAWTEXT"):
        return False
    r = subprocess.run([FFMPEG, "-hide_banner", "-filters"],
                       capture_output=True, text=True)
    return " drawtext " in r.stdout

def find_font():
    # prefer the workspace-bundled house serif (EB Garamond) so slate/burn-in
    # text is on-brand and machine-independent; then fall back to system serifs.
    _root = Path(__file__).resolve().parents[1]          # runtime/
    bundled = (_root / "fonts/EB_Garamond/static/EBGaramond-Regular.ttf",
               _root / "fonts/Inter/static/Inter_28pt-Regular.ttf")
    for p in (*bundled,
              "/System/Library/Fonts/Supplemental/Georgia.ttf",
              "/Library/Fonts/Georgia.ttf",
              "/System/Library/Fonts/Supplemental/Times New Roman.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
              "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"):
        if Path(p).exists():
            return str(p)
    return None

# ------------------------------------------------------------- PIL text

def _pil_font(font_path, size):
    from PIL import ImageFont
    try:
        return ImageFont.truetype(font_path, size)
    except Exception:
        return ImageFont.load_default()

def make_slate_png(out, w, h, bid, label, owner, font_path, prompt_line=None):
    """A slate is a REQUEST CARD: what this beat needs and from whom.
    Line 4 (optional) is the suggested generation prompt / search terms,
    wrapped, so the human can act on the card without opening the sheet."""
    from PIL import Image, ImageDraw
    img = Image.new("RGB", (w, h), INK_RGB)
    d = ImageDraw.Draw(img)
    f1 = _pil_font(font_path, int(h * 0.12))
    f2 = _pil_font(font_path, int(h * 0.045))
    f3 = _pil_font(font_path, int(h * 0.038))
    d.text((w / 2, h * 0.34), bid, font=f1, fill=CREAM_RGB, anchor="mm")
    d.text((w / 2, h * 0.50), label[:80], font=f2, fill=CREAM_RGB, anchor="mm")
    d.text((w / 2, h * 0.60), owner[:90], font=f3, fill=(211, 95, 67), anchor="mm")
    if prompt_line:
        f4 = _pil_font(font_path, int(h * 0.030))
        words, lines, cur = prompt_line.split(), [], ""
        for wd in words:
            if len(cur) + len(wd) + 1 > 84 and cur:
                lines.append(cur); cur = wd
            else:
                cur = (cur + " " + wd).strip()
        if cur: lines.append(cur)
        for i, ln in enumerate(lines[:3]):
            d.text((w / 2, h * (0.70 + 0.045 * i)), ln,
                   font=f4, fill=(180, 168, 150), anchor="mm")
    img.save(out)

def make_label_png(out, text, font_path, size):
    from PIL import Image, ImageDraw
    f = _pil_font(font_path, size)
    tmp = Image.new("RGBA", (4, 4)); tw = ImageDraw.Draw(tmp).textbbox((0, 0), text, font=f)
    w, h = tw[2] - tw[0] + 24, tw[3] - tw[1] + 16
    img = Image.new("RGBA", (w, h), (0, 0, 0, 150))
    ImageDraw.Draw(img).text((12, 8 - tw[1]), text, font=f, fill=(255, 255, 255, 255))
    img.save(out)

def make_teardown_label_png(out, bid, font_path, size):
    """Compact teardown beat-ID chip: solid ink (#2A1A0E) background, white text.
    Intentional — for Brutalist finals where keep_review_labels is true.
    The viewer sees it; B00B narration says 'the little label in the corner'."""
    from PIL import Image, ImageDraw
    INK = (42, 26, 14)    # #2A1A0E
    WHITE = (255, 255, 255, 255)
    f = _pil_font(font_path, size)
    tmp = Image.new("RGBA", (4, 4))
    tw = ImageDraw.Draw(tmp).textbbox((0, 0), bid, font=f)
    pad_x, pad_y = 10, 6
    w = tw[2] - tw[0] + pad_x * 2
    h = tw[3] - tw[1] + pad_y * 2
    img = Image.new("RGBA", (w, h), (*INK, 255))
    ImageDraw.Draw(img).text((pad_x, pad_y - tw[1]), bid, font=f, fill=WHITE)
    img.save(out)

def make_channel_title_png(out, text, font_path, size):
    """Centered channel handle for the first beat only.
    Ink text on a fully transparent ground — no pill, no box. Blends naturally
    with the first beat's cream background. Set metadata.channel_title in the
    beat sheet; compile.py shows it only during the first beat's duration."""
    from PIL import Image, ImageDraw
    f = _pil_font(font_path, size)
    tmp = Image.new("RGBA", (4, 4))
    tw = ImageDraw.Draw(tmp).textbbox((0, 0), text, font=f)
    pad_x, pad_y = 4, 4
    img_w = tw[2] - tw[0] + pad_x * 2
    img_h = tw[3] - tw[1] + pad_y * 2
    img = Image.new("RGBA", (img_w, img_h), (0, 0, 0, 0))
    ImageDraw.Draw(img).text((pad_x, pad_y - tw[1]), text, font=f,
                             fill=(*INK_RGB, 255))
    img.save(out)

# ------------------------------------------------------------- slots

def resolve_slot(folder, bid):
    for rel, status in ((f"media/{bid}.mp4", "VIDEO"), (f"manim/{bid}.mp4", "MANIM"),
                        (f"manim/{bid}.mov", "MANIM"), (f"media/{bid}.png", "STILL"),
                        (f"media/{bid}.jpg", "STILL")):
        p = folder / rel
        if p.exists():
            return p, status
    return None, "SLATE"

def vf_fit(w, h, fit="crop"):
    if fit == "pad":        # letterbox on the newsprint ground (shorts wrap)
        return (f"scale={w}:{h}:force_original_aspect_ratio=decrease,"
                f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:color=0xF3EBDD")
    return f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}"

def vf_treatment(source, override=None):
    """The laundering function: desaturate + printed contrast for photographic
    sources. Manim fragments and design-system beats pass through untouched.
    Per-beat override (shot.treatment): 'none' = as generated (the one loud
    element); 'light' = keep the color, seat it in the collage — for beats
    whose color IS the information (a forge glow the narration names)."""
    if override == "none":
        return None
    if override == "light":
        return "hue=s=0.8,eq=contrast=1.06:brightness=0.005"
    if source in ("archive", "ai"):
        return "hue=s=0.25,eq=contrast=1.12:brightness=0.01"
    return None

def _log_replace(folder, bid, msg):
    """Append a replacement note to <reel>/replace_log.md (dedup by line)."""
    log = Path(folder) / "replace_log.md"
    line = f"- {bid}: {msg}"
    prev = log.read_text() if log.exists() else "# REPLACE LOG — slots needing better media\n"
    if line not in prev:
        log.write_text(prev.rstrip() + "\n" + line + "\n")
        print(f"[art] {bid}: logged for replacement -> {log.name}")


def compile_clip(folder, beat, out, w, h, fps, font, work, fit="crop"):
    # A failed rebuild must leave the previous cache entry intact.
    with tempfile.TemporaryDirectory(prefix='.clip-', dir=out.parent) as scratch:
        candidate = Path(scratch) / 'clip.mp4'
        result = _compile_clip(folder, beat, candidate, w, h, fps, font, work, fit)
        os.replace(candidate, out)
        return result


def _compile_clip(folder, beat, out, w, h, fps, font, work, fit="crop"):
    bid = beat["beat_id"]
    dur = beat_duration(beat)
    shot = beat.get("shot", {})
    src, status = resolve_slot(folder, bid)
    # Per-clip normalize: near-visually-lossless so this pass is NOT a real
    # generation of loss (medium/crf12). The one meaningful lossy encode is the
    # final concat below (slow/crf16).
    # The timeline is frame-aligned. Decimal -t rounding plus tpad can otherwise
    # add a duplicate frame (e.g. 601/24 -> 25.042 seconds -> 602 frames).
    enc = ["-frames:v", str(round(dur * fps)),
           "-c:v", "libx264", "-preset", "medium", "-crf", "12",
           "-pix_fmt", "yuv420p", "-r", str(fps), "-an", str(out)]
    treat = vf_treatment(shot.get("source", "own"), shot.get("treatment"))

    if is_source_report(beat):
        if status != 'VIDEO':
            raise BuildError(f'{bid}: source report video is missing')
        # Embedded audio joins the master separately. Never retime, center-cut,
        # stylize or crop the fellow's evidence to fit a narration estimate.
        cmd = [FFMPEG, '-y', '-i', src, '-vf', vf_fit(w, h, 'pad') + f',tpad=stop_mode=clone:stop_duration={1/fps}',
               '-t', f'{dur:.6f}'] + enc
    elif status in ("VIDEO", "MANIM"):
        d = probe_dur(src) or dur
        vf = [vf_fit(w, h, fit)]
        if treat and status == "VIDEO":
            vf.append(treat)
        delta = (d - dur) / dur
        seek = []
        if abs(delta) <= LADDER_RETIME and d > 0:          # retime to exact
            vf.append(f"setpts=PTS*{dur / d:.6f}")
        elif d < dur and d > 0:                             # slow to fit — never freeze
            ratio = dur / d
            if ratio > 3.0:
                print(f"[art] WARNING {bid}: clip {d:.1f}s slowed {ratio:.1f}x "
                      f"into {dur:.1f}s beat — extreme slow-mo, consider a longer generation")
                _log_replace(folder, bid, f"clip {d:.1f}s slowed {ratio:.1f}x into "
                             f"{dur:.1f}s beat — extreme slow-mo; replace with a "
                             f"longer generation (pantry, {Path(src).name})")
            else:
                print(f"[art] {bid}: clip {d:.1f}s slowed {ratio:.2f}x to fill {dur:.1f}s beat")
            vf.append(f"setpts=PTS*{ratio:.6f}")
        else:                                               # longer -> CENTER cut
            off = max(0.0, (d - dur) / 2.0)
            if off > 0.05:
                seek = ["-ss", f"{off:.3f}"]
                print(f"[art] {bid}: clip {d:.1f}s center-cut to {dur:.1f}s (skip {off:.1f}s head/tail)")
        # freeze-pad any sub-frame shortfall so clip totals match audio totals
        vf.append(f"tpad=stop_mode=clone:stop_duration={dur:.3f}")
        cmd = [FFMPEG, "-y"] + seek + ["-i", src, "-vf", ",".join(vf), "-t", f"{dur + 0.5 / fps:.6f}"] + enc
    elif status == "STILL":
        motion = shot.get("motion", "kenburns")
        iw, ih = probe_wh(src)
        if iw and (iw < w or ih < h):
            print(f"[art] WARNING {bid}: still {iw}x{ih} under output {w}x{h} — "
                  f"the move will reveal upscale artifacts (MOTION.md §1)")
        vf = [vf_fit(w * 2, h * 2, fit)]                   # oversample against zoompan shimmer
        if treat:
            vf.append(treat)
        # MOTION.md §1: motivated direction. shot.focus = [fx, fy] in 0–1
        # image coords; default 0.5,0.5 reproduces the old center move.
        f_xy = shot.get("focus") or [0.5, 0.5]
        fx = min(max(float(f_xy[0]), 0.0), 1.0)
        fy = min(max(float(f_xy[1]), 0.0), 1.0)
        frames = max(2, int(round(dur * fps)))
        if motion == "hold":
            vf.append(f"scale={w}:{h}")
        elif motion == "pan":                              # pan OR zoom, never both
            ltr = int(hashlib.sha1(bid.encode()).hexdigest(), 16) % 2 == 0
            prog = (f"on/{frames - 1}" if ltr else f"(1-on/{frames - 1})")
            vf.append(f"zoompan=z='1.10':x='(iw-iw/zoom)*({prog})'"
                      f":y='(ih-ih/zoom)*{fy:.4f}':d={frames}:s={w}x{h}:fps={fps}")
        else:                                               # ken burns toward the focus
            zin = int(hashlib.sha1(bid.encode()).hexdigest(), 16) % 2 == 0
            z = (f"zoom+{0.08/frames:.6f}" if zin else f"1.08-{0.08/frames:.6f}*on")
            vf.append(f"zoompan=z='{z}':x='(iw-iw/zoom)*{fx:.4f}'"
                      f":y='(ih-ih/zoom)*{fy:.4f}':d={frames}:s={w}x{h}:fps={fps}")
        cmd = [FFMPEG, "-y", "-loop", "1", "-i", src, "-vf", ",".join(vf),
               "-t", f"{dur + 0.5 / fps:.6f}"] + enc
    else:                                                   # slate (PIL — no drawtext needed)
        label = (beat.get("new_visual_element") or beat.get("narration_text", ""))[:80]
        from beat_plan import owner_line
        owner, prompt_line = owner_line(beat)
        # TWO placeholder types (hardening rule 4): a VOX-ANIM placeholder is a
        # beat that would otherwise be a single-sentence Remotion slide. It asks
        # for pantry media that will be ANIMATED vox-style with Remotion — a
        # distinct request from the STILL/COMPOSITE "drop an image" slate.
        if shot.get("placeholder") == "vox-anim" or shot.get("scene_type") == "vox-anim":
            label = ("VOX-ANIM · " + label)[:80]
            owner = f"YOU -> pantry media, animated vox-style with Remotion (as {bid}.mp4)"
        png = work / f"slate-{bid}.png"
        make_slate_png(png, w, h, bid, label, owner, font, prompt_line)
        cmd = [FFMPEG, "-y", "-loop", "1", "-i", png, "-t", f"{dur + 0.5 / fps:.6f}"] + enc
    sh(cmd)
    return src, status

def make_qc_sheet(folder, beats, clips, work, font):
    """Contact sheet: mid-frame of every beat clip, tiled + labeled. The cheap
    visual QC pass — review this one image for overflow/clipping/layout bugs."""
    from PIL import Image, ImageDraw
    tiles, tw, th = [], 480, 270
    for b in beats:
        bid = b["beat_id"]
        dur = beat_duration(b)
        clip = clips / f"{bid}.mp4"
        frame = work / f"qc-{bid}.png"
        subprocess.run([FFMPEG, "-y", "-ss", f"{dur / 2:.2f}", "-i", str(clip),
                        "-frames:v", "1", "-vf", f"scale={tw}:{th}", str(frame)],
                       capture_output=True)
        if frame.exists():
            img = Image.open(frame).convert("RGB")
            d = ImageDraw.Draw(img)
            d.rectangle([0, th - 26, 150, th], fill=(0, 0, 0))
            d.text((8, th - 23), f"{bid} {b.get('shot', {}).get('type', '')}",
                   font=_pil_font(font, 16), fill=(255, 255, 255))
            tiles.append(img)
    if not tiles:
        return None
    cols = 4
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw, rows * th), (30, 27, 24))
    for i, img in enumerate(tiles):
        sheet.paste(img, ((i % cols) * tw, (i // cols) * th))
    out = folder / "qc-sheet.png"
    sheet.save(out)
    return out


def concat_line(path):
    return "file '" + str(Path(path).resolve()).replace("'", "'\\''") + "'\n"


def probe_streams(path):
    r = sh([FFPROBE, '-v', 'error', '-show_streams', '-show_format', '-of', 'json', path])
    return json.loads(r.stdout)


def require_audible(path, label):
    r = sh([FFMPEG, '-hide_banner', '-i', path, '-vn', '-af', 'volumedetect', '-f', 'null', '-'])
    m = re.search(r'max_volume:\s*([-\w.]+) dB', r.stderr)
    if not m or float(m.group(1)) <= -80:
        raise BuildError(f'{label}: required audio is silent; declare audio_policy=silence only if intentional')


def beat_duration(beat):
    return positive_duration(beat.get('render_duration_s') or beat.get('actual_duration_s')
                             or beat.get('estimated_duration_s'), beat['beat_id'])


def prepare_timeline(folder, sheet, fps):
    for beat in sheet['beats']:
        if is_source_report(beat, sheet):
            src, status = resolve_slot(folder, beat['beat_id'])
            if status != 'VIDEO':
                raise BuildError(f"{beat['beat_id']}: source report must exist at media/<beat_id>.mp4")
            beat['kind'] = 'source_report'
            beat['clock'] = 'source'
            beat.setdefault('audio_policy', 'preserve')
            beat['actual_duration_s'] = positive_duration(probe_dur(src), beat['beat_id'])
        measured = positive_duration(beat.get('actual_duration_s') or beat.get('estimated_duration_s'), beat['beat_id'])
        # Pad, never truncate, the sub-frame tail. Audio and video now share
        # exactly the same frame boundaries without accumulating concat drift.
        beat['render_duration_s'] = math.ceil(measured * fps - 1e-8) / fps


def build_master_audio(folder, beats, cli_audio, tmp):
    """Assemble a complete clocked audio timeline; a missing track is an error."""
    total = sum(beat_duration(b) for b in beats)
    if cli_audio:
        if any(is_source_report(b) for b in beats):
            raise BuildError('--audio cannot replace the embedded soundtrack of a source report')
        path = Path(cli_audio)
        if not path.is_file() or abs((probe_dur(path) or 0) - total) > 0.15:
            raise BuildError('--audio must exist and match the complete timeline duration')
        require_audible(path, 'Master track')
        return path, 'explicit master track'
    wavs = []
    for b in beats:
        bid = b['beat_id']
        dur = beat_duration(b)
        wav = tmp / f'audio-{bid}.wav'
        if intentional_silence(b):
            inputs = ['-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo']
        else:
            src = resolve_slot(folder, bid)[0] if is_source_report(b) else (
                folder / (b.get('audio_file') or f'audio/{bid}.mp3'))
            if src is None or not src.is_file():
                raise BuildError(f'{bid}: missing required audio ({src}); no silent fallback')
            streams = probe_streams(src)['streams']
            if not any(s.get('codec_type') == 'audio' for s in streams):
                raise BuildError(f'{bid}: source has no audio stream')
            require_audible(src, bid)
            if not is_source_report(b) and abs((probe_dur(src) or 0) - dur) > 0.15:
                raise BuildError(f'{bid}: narration duration disagrees with the beat; regenerate/measure audio')
            inputs = ['-i', src]
        # Separate PCM segments avoid MP3 concat padding/drift; explicit padding
        # only fills the segment's remaining tail, never shifts following beats.
        sh([FFMPEG, '-y', '-v', 'error'] + inputs + ['-map', '0:a:0', '-vn',
            '-af', 'apad', '-t', f'{dur:.6f}', '-ar', '48000', '-ac', '2', '-c:a', 'pcm_s16le', wav])
        wavs.append(wav)
    lst = tmp / 'audio.txt'
    lst.write_text(''.join(concat_line(p) for p in wavs))
    out = tmp / 'master.wav'
    sh([FFMPEG, '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', lst,
        '-c:a', 'pcm_s16le', out])
    return out, 'per-beat timeline (source audio preserved)'


def verify_output(path, total, fps, audible, short=False):
    probe = probe_streams(path)
    kinds = {s.get('codec_type') for s in probe['streams']}
    if not {'audio', 'video'} <= kinds:
        raise BuildError('Final must contain decodable video and audio streams')
    duration = positive_duration(probe.get('format', {}).get('duration'), 'Output')
    if short:
        require_short_duration(duration, 'Encoded Short container')
        for stream in probe['streams']:
            if stream.get('codec_type') in ('video', 'audio') and stream.get('duration') is not None:
                require_short_duration(stream['duration'], 'Encoded Short ' + stream['codec_type'])
    if abs(duration - total) > max(0.15, 2 / fps):
        raise BuildError(f'Output duration {duration:.3f}s does not match timeline {total:.3f}s')
    sh([FFMPEG, '-v', 'error', '-xerror', '-i', path, '-f', 'null', '-'])
    if audible:
        require_audible(path, 'Compiled output')


def final_preflight(folder, sheet, sheet_name):
    require_paperwork(folder)
    for name in ('beat_lint.py', 'gate_shape.py'):
        gate = Path(__file__).resolve().parents[1] / 'qc' / name
        if not gate.is_file():
            raise BuildError(f'Missing required final gate: {gate.name}')
        sh([sys.executable, gate, folder / sheet_name])
    md = sheet.get('metadata') or {}
    if md.get('kind') == 'short':
        if md.get('short_validation', {}).get('status') != 'ready':
            raise BuildError('Short needs a ready portrait plan before final export')
        # Related-video selection and channel-wide spacing happen at scheduling
        # time in the separate publishing workflow, not while rendering files.

def _filled_by(beat, status):
    """Name the thing that actually filled this slot, for the build stamp."""
    shot = beat.get("shot") or {}
    rem = shot.get("remotion") or {}
    if status == "MANIM":
        scene = (shot.get("manim") or {}).get("scene_class") or ""
        return f"manim:{scene}" if scene else "manim"
    if status == "VIDEO" and rem.get("pattern") and (rem.get("rendered") or {}).get("at"):
        return f"remotion:{rem['pattern']}"
    if status == "VIDEO":
        return "media"          # capture / human drop / build-script copy
    if status == "STILL":
        return "still"
    return None                  # SLATE


def lint_skin(sheet):
    """Machine-check the brand contract the sheet CLAIMS. Prose instructions
    to an authoring agent don't survive; this does. Warning-only for now."""
    warns = []
    meta = sheet.get("metadata", {})
    beats = sheet.get("beats") or []
    if not beats:
        return warns

    def pat(b):
        return ((b.get("shot") or {}).get("remotion") or {}).get("pattern") or ""

    # A sheet with ZERO machine-fillable beats was authored blind — every
    # slot falls to a human request card and the pipeline renders nothing.
    from beat_plan import fill_plan
    machine = [b["beat_id"] for b in beats
               if fill_plan(b).get("responsible") == "pipeline"]
    if not machine:
        warns.append("NO RENDERABLE BEATS: no beat carries a shot.remotion.pattern "
                     "or Manim annotation — the pipeline will render NOTHING and "
                     "every slot becomes a YOU-slate. The sheet was authored "
                     "without the scene contract.")

    # SPARK-LINE LAW: an inner ClaudeComposerAsk beat must carry a spark line
    # (its `greeting`) — never a lonely asterisk. B00 (cold open) and the handoff
    # ("Your turn.") are the only composer beats allowed their own greetings; every
    # other composer beat that is empty is a lonely-asterisk bug (e.g. a CHANGE beat).
    for i, b in enumerate(beats):
        if pat(b) != "ClaudeComposerAsk":
            continue
        g = ((b.get("shot") or {}).get("remotion") or {}).get("props", {}).get("greeting", "")
        if i == 0:
            continue  # cold open owns the hello
        if str(g).strip().lower() in ("your turn.", "your turn"):
            continue  # the handoff
        if not str(g).strip():
            warns.append(f"{b['beat_id']}: composer beat has an empty spark line — "
                         f"SPARK-LINE LAW wants a short serif cue (e.g. \"The change,\").")

    if str(meta.get("palette", "")).lower() == "claude":
        p0, pN = pat(beats[0]), pat(beats[-1])
        if p0 != "ClaudeComposerAsk":
            warns.append(f"{beats[0]['beat_id']}: palette=claude but the cold open "
                         f"is '{p0 or 'un-annotated'}' — COLD OPEN LAW wants "
                         f"ClaudeComposerAsk")
        if pN != "ClaudeTitleOutro":
            warns.append(f"{beats[-1]['beat_id']}: palette=claude but the outro "
                         f"is '{pN or 'un-annotated'}' — OUTRO LAW wants "
                         f"ClaudeTitleOutro")
    return warns


def stamp_sheet(folder, sheet, report, cut, sheet_name="beat_sheet.json"):
    """Write what THIS compile actually did back into beat_sheet.json.

    Every beat gets a `build` record alongside its `shot` intent:
      status    VIDEO | MANIM | STILL | SLATE   (resolve_slot's verdict)
      src       reel-relative file that filled the slot, or null
      filled_by 'remotion:<pattern>' | 'manim:<scene>' | 'media' | 'still' | null
      needs     (SLATE only) the owner line — who owes this file
      suggested (SLATE only) the request card's prompt line, if any
      at        ISO timestamp of this compile

    metadata.build summarizes the cut: counts, slate list, skin warnings.
    Intent is never modified — build is a parallel record, so a reviewer can
    diff what was ASKED against what actually RENDERED. Failure to stamp
    never kills a compile.
    """
    try:
        from datetime import datetime
        from beat_plan import owner_line
        now = datetime.now().isoformat(timespec="seconds")
        status_by = {bid: status for bid, _, _, status, _ in report}
        slates = []
        for b in sheet["beats"]:
            bid = b["beat_id"]
            if bid not in status_by:
                continue
            status = status_by[bid]
            src, _ = resolve_slot(folder, bid)
            rec = {"status": status,
                   "src": str(src.relative_to(folder)) if src else None,
                   "filled_by": _filled_by(b, status),
                   "at": now}
            if status == "SLATE":
                owner, prompt_line = owner_line(b)
                rec["needs"] = owner
                if prompt_line:
                    rec["suggested"] = prompt_line
                slates.append(bid)
                rem = (b.get("shot") or {}).get("remotion") or {}
                if rem.get("pattern"):
                    print(f"[art] WARNING {bid}: sheet asks for Remotion "
                          f"'{rem['pattern']}' but nothing rendered — run "
                          f"remotion_scenes.py, then recompile")
            b["build"] = rec
        warns = lint_skin(sheet)
        for wmsg in warns:
            print(f"[art] SKIN LINT: {wmsg}")
        sheet.setdefault("metadata", {})["build"] = {
            "at": now, "cut": cut,
            "filled": len(report) - len(slates), "of": len(report),
            "slates": slates, "skin_warnings": warns,
        }
        atomic_json(writable_path(folder, sheet_name), sheet)
        print(f"[art] build stamp → {sheet_name} "
              f"({len(report) - len(slates)}/{len(report)} filled)")
    except Exception as e:                                  # never fatal
        print(f"[art] WARNING: build stamp failed: {e}", file=sys.stderr)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder", type=Path)
    ap.add_argument("--review", action="store_true")
    ap.add_argument("--fps", type=int, default=24)
    ap.add_argument("--height", type=int, default=720)
    ap.add_argument("--audio", help="master audio file (music bed / narration mix)")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--allow-slates", action="store_true",
                    help="legacy review-only option; final masters always reject slates")
    ap.add_argument("--out", type=Path, default=None, metavar="DIR",
                    help="directory to write the master into — any folder, including a "
                         "Google Drive mount. Explicit --out always wins. Without it, a "
                         "clean 4K final goes to $ART_OUT if set, else BRUTALIST_HOME/renders/; "
                         "a --review cut always stays beside the reel.")
    ap.add_argument("--sheet", default="beat_sheet.json",
                    help="beat sheet filename (default: beat_sheet.json)")
    a = ap.parse_args()
    try:
        return compile_reel(a)
    except (BuildError, OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as exc:
        if a.folder.is_dir():
            record_failure(a.folder, exc, 'blocked' if isinstance(exc, ApprovalError) else 'failed')
        print(f'[art] REFUSED: {exc}', file=sys.stderr)
        return 2


def compile_reel(a):
    folder = a.folder.resolve()
    sheet = json.loads(writable_path(folder, a.sheet).read_text())
    original_sheet = copy.deepcopy(sheet)
    validate_project(sheet)
    atomic_json(writable_path(folder, 'build-state.json'), {'status': 'planned'})
    validate_approvals(folder, sheet)
    if not a.review:
        if a.allow_slates:
            raise BuildError('--allow-slates is review-only; a final cannot contain missing visuals')
        final_preflight(folder, sheet, a.sheet)
    if a.fps <= 0:
        raise BuildError('FPS must be positive')
    prepare_timeline(folder, sheet, a.fps)
    beats = sheet["beats"]
    inputs = set()
    for b in beats:
        source, _ = resolve_slot(folder, b['beat_id'])
        if source:
            inputs.add(source.resolve())
        if not is_source_report(b) and not intentional_silence(b):
            inputs.add((folder / (b.get('audio_file') or f"mp3/beat-{b['beat_id']}.mp3")).resolve())
    if a.audio:
        inputs.add(Path(a.audio).resolve())
        # A supplied master replaces ordinary per-beat narration requirements.
        inputs = {p for p in inputs if p.is_file()}
    for p in inputs:
        if not p.is_file():
            raise BuildError(f'missing required audio or media: {p}')
    input_hashes = {str(p): file_digest(p) for p in sorted(inputs)}
    if sheet.get('metadata', {}).get('kind') == 'short':
        require_short_duration(sum(beat_duration(b) for b in beats), 'Measured Short timeline')
    ar = sheet.get("metadata", {}).get("aspect_ratio", "16:9")
    num, den = (int(x) for x in ar.split(":"))
    if a.height <= 0 or a.height % 2 or a.fps <= 0 or num <= 0 or den <= 0:
        raise BuildError('Height must be positive/even; FPS and aspect ratio must be positive')
    h = a.height; w = int(round(h * num / den / 2) * 2)
    fps, font = a.fps, find_font()
    drawtext = has_drawtext()
    clips = writable_path(folder, 'clips/manifest.json').parent; clips.mkdir(exist_ok=True)
    work = writable_path(folder, 'clips/_work/.check').parent; work.mkdir(exist_ok=True)
    writable_path(folder, '_qc/.check').parent.mkdir(exist_ok=True)
    writable_path(folder, 'media/.check').parent.mkdir(exist_ok=True)
    man_path = clips / "manifest.json"
    manifest = json.loads(man_path.read_text()) if man_path.exists() else {}
    # Validate/assemble all sound before spending time on visual renders.
    audio, akind = build_master_audio(folder, beats, a.audio, work)
    atomic_json(writable_path(folder, 'build-state.json'), {'status': 'rendering'})

    report, t0 = [], 0.0
    for b in beats:
        bid = b["beat_id"]
        dur = beat_duration(b)
        out = writable_path(folder, f"clips/{bid}.mp4")
        src, status = resolve_slot(folder, bid)
        bshot = b.get("shot", {})
        key = (f"L4|{w}x{h}@{fps}|{sheet.get('metadata', {}).get('fit', 'crop')}|report={is_source_report(b)}"
               f"|{dur:.3f}|{bshot.get('motion', '')}"
               f"|{bshot.get('focus', '')}|{bshot.get('treatment', '')}|"
               + (sha1(src) if src else "slate"))
        if a.force or manifest.get(bid) != key or not out.exists():
            src, status = compile_clip(folder, b, out, w, h, fps, font, work,
                                       fit=sheet.get("metadata", {}).get("fit", "crop"))
            manifest[bid] = key
            atomic_json(man_path, manifest)
            print(f"[art] compiled {bid}  {status:6}  {dur:5.1f}s" +
                  (f"  ← {src.name}" if src else ""), flush=True)
        report.append((bid, t0, dur, status, b.get("shot", {}).get("type", "?")))
        t0 += dur
    atomic_json(man_path, manifest)

    # THE MASTER LAW: no slates in a clean master. Review cuts show slates as
    # information; a master with a slate is an unfinished film shipping.
    slated = [bid for bid, _, _, status, _ in report if status == "SLATE"]
    if slated and not a.review and not a.allow_slates:
        raise BuildError(f"[art] REFUSED: clean master would carry {len(slated)} slate(s): "
                 f"{' '.join(slated)} — run run.sh to render/fill them "
                 f"(use --review to inspect unfinished work)")

    # Descriptive inventory, not a sourcing quota. A renderer is not a visual
    # language; executed evidence may correctly use one renderer throughout.
    def _eff_motion(b):
        s = b.get("shot", {})
        return (s.get("motion")
                or ("kenburns" if s.get("type") == "STILL"
                    else (s.get("type") or "?").lower()))
    hist = Counter(_eff_motion(b) for b in beats)
    print("[art] motion histogram: "
          + "  ".join(f"{k}:{n}" for k, n in hist.most_common()))

    lst = clips / "concat.txt"
    lst.write_text(''.join(concat_line(clips / (b['beat_id'] + '.mp4')) for b in beats))
    total = sum(beat_duration(b) for b in beats)

    slug = sheet.get("metadata", {}).get("slug", folder.name)

    # ── RENDER TARGET ────────────────────────────────────────────────────────
    # brutalist.art RENDERS; it does not publish. A finished 4K master may land
    # in any folder — a local dir, a shared drive, a Google Drive mount. Staging
    # and uploading are somebody else's job, outside this toolkit.
    #   1. --out DIR        explicit, always wins
    #   2. $ART_OUT         the downloader's configured render folder (.env)
    #   3. <toolkit>/renders/   built-in default, so it works with zero config
    # A --review cut is a working artifact and always stays beside the reel.
    if a.review:
        out_dir = folder
    elif a.out:
        out_dir = a.out
    else:
        env_out = os.environ.get("ART_OUT", "").strip()
        out_dir = Path(env_out).expanduser() if env_out \
            else Path(__file__).resolve().parents[2] / "renders"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / (f"{slug}-slate.mp4" if a.review else f"{slug}.mp4")

    # --- label overlay: review cuts only — never in clean finals
    meta_flags = sheet.get("metadata", {})
    keep_labels = bool(meta_flags.get("keep_review_labels"))
    label_pngs = []   # list of (png_path, ts, dur)
    if a.review:
        for bid, ts, dur, status, stype in report:
            png = work / f"lbl-{bid}.png"
            make_label_png(png, f"{bid} {stype} {status} {ts:6.1f}s +{dur:.1f}s",
                           font, int(h * 0.032))
            label_pngs.append((png, ts, dur))
    elif keep_labels:
        # Compact teardown chips — just the beat ID, ink on white, intentional on-screen.
        # B00B tells the viewer: "the little label in the corner of each beat — B00, B04 …"
        for bid, ts, dur, status, stype in report:
            png = work / f"tdl-{bid}.png"
            make_teardown_label_png(png, bid, font, int(h * 0.020))
            label_pngs.append((png, ts, dur))

    # --- channel title: ink text centered at the bottom of the FIRST BEAT ONLY.
    # Set metadata.channel_title in beat_sheet.json (e.g. "@HumanitariansAI").
    # Renders in the serif house font, no background, same palette as the beat card.
    channel_title = meta_flags.get("channel_title", "")
    title_png = None
    first_beat_dur = float(beats[0].get("actual_duration_s")
                           or beats[0].get("estimated_duration_s") or 6.0) if beats else 0.0
    if channel_title and font:
        title_png = work / "channel_title.png"
        make_channel_title_png(title_png, channel_title, font, int(h * 0.030))

    cmd = [FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", lst]
    cmd += (["-i", str(audio)] if audio else
            ["-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo"])
    for png, ts, dur in label_pngs:
        cmd += ["-i", str(png)]
    if title_png:
        cmd += ["-i", str(title_png)]

    fc = []
    n_label_inputs = 2 + len(label_pngs)   # 0=video, 1=audio, 2..=labels
    if label_pngs or title_png:
        prev = "0:v"
        for i, (png, ts, dur) in enumerate(label_pngs):
            nxt = f"v{i}"
            fc.append(f"[{prev}][{i + 2}:v]overlay=16:H-h-16:"
                      f"enable='between(t,{ts:.3f},{ts + dur:.3f})'[{nxt}]")
            prev = nxt
        if title_png:
            fc.append(f"[{prev}][{n_label_inputs}:v]"
                      f"overlay=(W-w)/2:H-h-40"
                      f":enable='between(t,0,{first_beat_dur:.3f})'[vtitle]")
            prev = "vtitle"
        if a.review and drawtext:
            fc.append(f"[{prev}]drawtext=fontfile={font}:text='%{{pts\\:hms}}'"
                      f":fontcolor=white:fontsize={int(h*0.04)}:box=1"
                      f":boxcolor=black@0.55:boxborderw=8:x=w-text_w-16:y=16[vout]")
        else:
            fc.append(f"[{prev}]null[vout]")
    if fc:
        cmd += ["-filter_complex", ";".join(fc), "-map", "[vout]", "-map", "1:a"]
    else:
        cmd += ["-map", "0:v", "-map", "1:a"]
    cmd += ["-c:v", "libx264", "-preset", "slow", "-crf", "16",
            "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest",
            "-t", f"{total:.3f}", str(out)]
    # Encode to a candidate. A previous verified final remains untouched if any
    # encode, approval re-check, media inspection or required QC gate fails.
    with tempfile.TemporaryDirectory(prefix=f'.{slug}-candidate-', dir=out_dir) as scratch:
        candidate = Path(scratch) / 'candidate.mp4'
        cmd[-1] = str(candidate)
        sh(cmd)
        verify_output(candidate, total, fps, bool(a.audio) or any(not intentional_silence(b) for b in beats),
                      short=sheet.get('metadata', {}).get('kind') == 'short')
        if not a.review:
            atomic_json(writable_path(folder, 'build-state.json'), {'status': 'verifying'})
            gate = Path(__file__).resolve().parents[1] / 'qc' / 'final_frame_check.py'
            if not gate.is_file():
                raise BuildError('Missing required final-frame checker')
            # Use the resolved source-clock sheet, not stale authored estimates.
            timeline = work / 'resolved-sheet.json'
            atomic_json(timeline, sheet)
            sh([sys.executable, gate, folder, '--mp4', candidate, '--sheet', timeline])
            latest = json.loads((folder / a.sheet).read_text())
            validate_approvals(folder, latest)
            # No approval or source edit during an encode may authorize this cut.
            if latest != original_sheet:
                raise BuildError('Beat sheet changed during rendering; rebuild the new revision')
            if any(not Path(p).is_file() or file_digest(p) != value for p, value in input_hashes.items()):
                raise BuildError('Source media or narration changed during rendering; rebuild the new revision')
        os.replace(candidate, out)
    stamp_sheet(folder, sheet, report, cut=('review' if a.review else 'master'), sheet_name=a.sheet)
    state = {'status': 'review' if a.review else 'ready', 'output': str(out.resolve()),
             'sha256': file_digest(out), 'duration_s': total,
             'input_sha256': input_hashes,
             'at': datetime.now(timezone.utc).isoformat()}
    if not a.review:
        atomic_json(out.with_suffix('.verified.json'), state)
    atomic_json(writable_path(folder, 'build-state.json'), state)

    n_slate = sum(1 for r in report if r[3] == "SLATE")
    if a.review:
        qc = make_qc_sheet(folder, beats, clips, work, font)
        if qc:
            print(f"[art] QC contact sheet → {qc}")
    print(f"[art] wrote {out}  ({total:.1f}s, audio: {akind}, "
          f"drawtext: {'yes' if drawtext else 'no — PIL overlays'})")
    print(f"[art] slots: {len(report) - n_slate}/{len(report)} filled — " +
          " ".join(f"{bid}:{st}" for bid, _, _, st, _ in report))

if __name__ == "__main__":
    raise SystemExit(main())
