#!/usr/bin/env python3
"""musinique_bookend.py — wrap a finished standalone film in silent Musinique
intro/outro cards, output at the source's own 4K resolution.

THE SILENCE LAW: the bookends carry no audible content, ever. No <Audio> tag
exists in either Remotion composition (MusiniqueIntroCard / MusiniqueOutroCard),
and this script never synthesizes narration or a jingle over them — only a
silent placeholder audio stream when the source film HAS an audio track (so
ffmpeg's concat filter has matching stream counts on every segment).

THE ARTIST-LINKS LAW: outro text (artist name + links) comes ONLY from
../artists.json, resolved by --artist <slug>. Never invented, never guessed.

THE 4K-MATCH LAW: this script ffprobes the input film for width/height/fps/
audio params and renders both bookends to match EXACTLY — whatever the
source's real resolution and frame rate are, not a hardcoded 3840x2160.

What one run does:
  1. ffprobe the input film (width, height, fps, audio codec/rate/channels).
  2. Resolve --artist against artists.json (KeyError-hard-stop if unknown).
  3. Write a scratch beat_sheet.json with two REMOTION beats
     (MusiniqueIntroCard, MusiniqueOutroCard), props carrying the source's
     exact canvas (halved — see NOTE below) + fps + the resolved title/artist.
  4. Render both via runtime/scripts/remotion_scenes.py, foreground — the
     ONLY lawful Remotion render path in this toolkit. Never hand-rolls
     `npx remotion render`.
  5. Concatenates intro + source + outro into one 4K output file via
     ffmpeg's concat FILTER (re-encode), not stream-copy concat — see
     "Why the concat filter" below.
  6. Writes the result next to the source film.

NOTE — why the composition renders at HALF the source's pixel dimensions:
remotion_scenes.py's render_beat() unconditionally passes `--scale=2` to
`npx remotion render` (house convention for supersampled/anti-aliased text —
see LogoOutro, which authors at 1080p and relies on this same doubling for
its 4K masters). This script therefore hands the composition's
calculateMetadata HALF of the source's width/height, so scale=2 lands back
on the source's exact pixel count. The concat step below still forcibly
scales every segment to the source's exact WxH as a defensive second check —
so a future change to remotion_scenes.py's scale factor degrades render
sharpness, never correctness.

Why the concat filter, not stream-copy concat: the three known
spoken-word sources disagree on fps (25 vs 30) and audio sample rate
(48000 vs 44100 Hz), and the Remotion renders start from a totally
independent encode. Stream-copy concat (the `concat` DEMUXER) requires
byte-identical codec parameters across every segment — fragile here, and it
would silently produce a broken or unplayable file on any mismatch. The
concat FILTER re-encodes every segment through one filter graph
(scale+fps-normalize the video, matching-profile silent audio for the
bookends), so segments never need to agree ahead of time. Cost: one
re-encode pass. Given these are ~2.5s bookends around a ~2-3 minute film,
the trade is obviously worth it for a script meant to run unattended.

Usage:
  python3 skills/make/musinique-bookend/scripts/musinique_bookend.py \\
      <film_path> --title "<title text>" --artist <artist-slug> \\
      [--out <path>] [--intro-seconds 2.5] [--outro-seconds 3.0] \\
      [--keep-render]

Free/local only: Remotion render (Kokoro-free, no audio synthesis at all)
+ ffmpeg/ffprobe. Never touches a paid API/tool — there is no paid path in
this skill to touch.
"""
import argparse, json, shutil, subprocess, sys, tempfile
from pathlib import Path

FFPROBE = shutil.which("ffprobe") or "ffprobe"
FFMPEG = shutil.which("ffmpeg") or "ffmpeg"

# skills/make/musinique-bookend/scripts/musinique_bookend.py -> ART_HOME
ART_HOME = Path(__file__).resolve().parents[4]
SKILL_DIR = Path(__file__).resolve().parents[1]
ARTISTS_JSON = SKILL_DIR / "artists.json"

LINK_LABELS = {
    "spotify": "Spotify",
    "apple_music": "Apple Music",
    "musinique": "Musinique",
    "website": "Website",
}


def ffprobe_json(path: Path) -> dict:
    r = subprocess.run(
        [FFPROBE, "-v", "error", "-print_format", "json",
         "-show_format", "-show_streams", str(path)],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        sys.exit(f"[musinique-bookend] ffprobe failed on {path}:\n{r.stderr[-800:]}")
    return json.loads(r.stdout)


def probe_source(path: Path) -> dict:
    info = ffprobe_json(path)
    vstream = next((s for s in info["streams"] if s.get("codec_type") == "video"), None)
    astream = next((s for s in info["streams"] if s.get("codec_type") == "audio"), None)
    if not vstream:
        sys.exit(f"[musinique-bookend] {path} has no video stream — not a film")

    width = int(vstream["width"])
    height = int(vstream["height"])
    num, den = (vstream.get("r_frame_rate") or "30/1").split("/")
    fps = float(num) / float(den or 1)
    duration = float(info["format"].get("duration") or vstream.get("duration") or 0.0)

    out = {
        "width": width, "height": height, "fps": fps, "duration": duration,
        "vcodec": vstream.get("codec_name"),
        "has_audio": astream is not None,
    }
    if astream:
        out["acodec"] = astream.get("codec_name")
        out["sample_rate"] = int(astream.get("sample_rate") or 48000)
        out["channels"] = int(astream.get("channels") or 2)
    return out


def even(n: int) -> int:
    n = int(round(n))
    return n if n % 2 == 0 else n + 1


def load_artist(slug: str) -> dict:
    if not ARTISTS_JSON.exists():
        sys.exit(f"[musinique-bookend] missing registry: {ARTISTS_JSON}")
    reg = json.loads(ARTISTS_JSON.read_text())
    artists = reg.get("artists", {})
    if slug not in artists:
        known = ", ".join(sorted(artists))
        sys.exit(f"[musinique-bookend] unknown --artist '{slug}'. Known slugs: {known}\n"
                  f"(the artists.json registry is the ONLY source — never invent one)")
    a = artists[slug]
    links = [{"label": LINK_LABELS.get(k, k.title()), "url": u}
              for k, u in a.get("links", {}).items()]
    return {"name": a["name"], "links": links}


def run(cmd, **kw):
    print("[musinique-bookend] $", " ".join(str(c) for c in cmd))
    r = subprocess.run(cmd, **kw)
    if r.returncode != 0:
        sys.exit(f"[musinique-bookend] command failed (exit {r.returncode}): {cmd[0]}")
    return r


def render_bookends(workdir: Path, src: dict, title: str, artist: dict,
                     intro_s: float, outro_s: float) -> tuple[Path, Path]:
    half_w, half_h = even(src["width"] / 2), even(src["height"] / 2)
    fps = src["fps"]

    beat_sheet = {
        "metadata": {"slug": "musinique-bookend-scratch"},
        "beats": [
            {
                "beat_id": "B01",
                "act": "intro",
                "narration_text": "",
                "shot": {"type": "REMOTION", "source": "own", "remotion": {
                    "pattern": "MusiniqueIntroCard",
                    "props": {
                        "title": title,
                        "durationS": intro_s,
                        "width": half_w, "height": half_h, "fps": fps,
                    },
                }},
                "actual_duration_s": intro_s,
            },
            {
                "beat_id": "B02",
                "act": "outro",
                "narration_text": "",
                "shot": {"type": "REMOTION", "source": "own", "remotion": {
                    "pattern": "MusiniqueOutroCard",
                    "props": {
                        "artistName": artist["name"],
                        "links": artist["links"],
                        "durationS": outro_s,
                        "width": half_w, "height": half_h, "fps": fps,
                    },
                }},
                "actual_duration_s": outro_s,
            },
        ],
    }
    (workdir / "beat_sheet.json").write_text(json.dumps(beat_sheet, indent=1))

    scenes_py = ART_HOME / "runtime" / "scripts" / "remotion_scenes.py"
    for bid in ("B01", "B02"):
        run([sys.executable, str(scenes_py), str(workdir), "--only", bid, "--force"])

    intro_mp4 = workdir / "media" / "B01.mp4"
    outro_mp4 = workdir / "media" / "B02.mp4"
    for p in (intro_mp4, outro_mp4):
        if not p.exists():
            sys.exit(f"[musinique-bookend] expected render missing: {p}")
    return intro_mp4, outro_mp4


def concat_with_filter(intro: Path, source: Path, outro: Path, out: Path, src: dict,
                        intro_s: float, outro_s: float):
    """Concatenate intro + source + outro via the ffmpeg concat FILTER
    (re-encode). See the module docstring 'Why the concat filter' for why
    this is preferred over stream-copy concat for this skill.

    Every video segment is force-scaled/fps-normalized to the source's exact
    WxH/fps (the defensive second check on the 4K-MATCH LAW). When the source
    has audio, each bookend gets a silent `anullsrc` companion trimmed to
    that bookend's own exact rendered duration (intro_s/outro_s — the same
    duration remotion_scenes.py already froze the clip to), so the concat
    filter's audio segments stay in lock-step with its video segments; the
    source's own audio is only reformatted (sample rate/layout), never
    replaced. THE SILENCE LAW: the synthesized audio is anullsrc — literally
    silence, never a jingle or narration.
    """
    w, h, fps = src["width"], src["height"], src["fps"]
    has_audio = src["has_audio"]
    sr = src.get("sample_rate", 48000)
    ch = src.get("channels", 2)
    layout = "mono" if ch == 1 else "stereo"

    if has_audio:
        cmd = [FFMPEG, "-y",
               "-i", str(intro),
               "-f", "lavfi", "-t", f"{intro_s:.3f}",
               "-i", f"anullsrc=channel_layout={layout}:sample_rate={sr}",
               "-i", str(source),
               "-i", str(outro),
               "-f", "lavfi", "-t", f"{outro_s:.3f}",
               "-i", f"anullsrc=channel_layout={layout}:sample_rate={sr}",
               "-filter_complex",
               ";".join([
                   f"[0:v]scale={w}:{h},fps={fps},setsar=1,format=yuv420p[v0]",
                   f"[2:v]scale={w}:{h},fps={fps},setsar=1,format=yuv420p[v1]",
                   f"[3:v]scale={w}:{h},fps={fps},setsar=1,format=yuv420p[v2]",
                   f"[1:a]aformat=sample_rates={sr}:channel_layouts={layout}[a0]",
                   f"[2:a]aformat=sample_rates={sr}:channel_layouts={layout}[a1]",
                   f"[4:a]aformat=sample_rates={sr}:channel_layouts={layout}[a2]",
                   "[v0][a0][v1][a1][v2][a2]concat=n=3:v=1:a=1[outv][outa]",
               ]),
               "-map", "[outv]", "-map", "[outa]",
               "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p",
               "-c:a", "aac", "-b:a", "192k", "-ar", str(sr),
               "-r", str(fps),
               str(out)]
    else:
        cmd = [FFMPEG, "-y", "-i", str(intro), "-i", str(source), "-i", str(outro),
               "-filter_complex",
               ";".join([
                   f"[0:v]scale={w}:{h},fps={fps},setsar=1,format=yuv420p[v0]",
                   f"[1:v]scale={w}:{h},fps={fps},setsar=1,format=yuv420p[v1]",
                   f"[2:v]scale={w}:{h},fps={fps},setsar=1,format=yuv420p[v2]",
                   "[v0][v1][v2]concat=n=3:v=1:a=0[outv]",
               ]),
               "-map", "[outv]",
               "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p",
               "-r", str(fps),
               str(out)]

    run(cmd)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("film", type=Path, help="path to the finished standalone film")
    ap.add_argument("--title", required=True, help="film/song title — rendered in the intro")
    ap.add_argument("--artist", required=True,
                     help="artist slug from artists.json — resolves the outro's name+links")
    ap.add_argument("--out", type=Path, default=None,
                     help="output path (default: <film-dir>/<film-dir-name>-musinique.mp4)")
    ap.add_argument("--intro-seconds", type=float, default=2.5,
                     help="intro bookend duration, 1.5-4s (default 2.5)")
    ap.add_argument("--outro-seconds", type=float, default=3.0,
                     help="outro bookend duration, 1.5-4s (default 3.0)")
    ap.add_argument("--keep-render", action="store_true",
                     help="keep the scratch render workdir for inspection instead of deleting it")
    a = ap.parse_args()

    film = a.film.resolve()
    if not film.exists():
        sys.exit(f"[musinique-bookend] no such film: {film}")

    src = probe_source(film)
    print(f"[musinique-bookend] source: {src['width']}x{src['height']} "
          f"@ {src['fps']:.3f}fps, audio={'yes' if src['has_audio'] else 'no'} "
          f"({film.name}, {src['duration']:.1f}s)")

    artist = load_artist(a.artist)
    print(f"[musinique-bookend] artist: {artist['name']} — "
          f"{len(artist['links'])} link(s): "
          f"{', '.join(l['label'] for l in artist['links'])}")

    out = a.out.resolve() if a.out else film.parent / f"{film.parent.name}-musinique.mp4"
    out.parent.mkdir(parents=True, exist_ok=True)

    workdir = Path(tempfile.mkdtemp(prefix="musinique-bookend-"))
    try:
        intro_mp4, outro_mp4 = render_bookends(
            workdir, src, a.title, artist, a.intro_seconds, a.outro_seconds)

        for label, clip in (("intro", intro_mp4), ("outro", outro_mp4)):
            got = ffprobe_json(clip)
            vs = next(s for s in got["streams"] if s["codec_type"] == "video")
            print(f"[musinique-bookend] rendered {label}: "
                  f"{vs['width']}x{vs['height']} -> will be scaled to "
                  f"{src['width']}x{src['height']} at concat time")

        concat_with_filter(intro_mp4, film, outro_mp4, out, src,
                            a.intro_seconds, a.outro_seconds)
    finally:
        if a.keep_render:
            print(f"[musinique-bookend] kept render workdir: {workdir}")
        else:
            shutil.rmtree(workdir, ignore_errors=True)

    final = ffprobe_json(out)
    vs = next(s for s in final["streams"] if s["codec_type"] == "video")
    dur = float(final["format"]["duration"])
    print(f"[musinique-bookend] wrote {out}  ({vs['width']}x{vs['height']}, {dur:.1f}s)")


if __name__ == "__main__":
    main()
