#!/usr/bin/env python3
"""stage_publish.py — stage a reel for youtube_publish.py.

Writes, in the reel folder, exactly what the publisher expects:
  mp4/<slug>.mp4          -> symlink to the clean 16:9 master (<slug>.mp4 at reel root)
  mp4/<slug>-short.mp4    -> symlink to the clean 9:16 master (short/*-short-cut.mp4)
  <slug>.srt              captions from the 16:9 beat sheet (SOURCE text on
                          measured beat windows — 'E = hν' on screen while the
                          voice says 'h nu'; never a transcription pass)
  <slug>-short.srt        captions from the short's own sheet (own timing)
  <slug>-youtube.md       description: blurb, chapters (from metadata.chapters),
                          sources/fact-check line, credits + AI DISCLOSURE from
                          media/*.source.txt sidecars, hashtags

Then publish (per-playlist drip: next slot = max(now+15m, last in playlist+2h)):
  python3 ../skills/make/sketch-explainer/scripts/youtube_publish.py <reel> \\
      --no-pairs --schedule-scope playlist --interval-hours 2 \\
      --client ... --token ... --ledger ...
"""
import argparse, json, sys, textwrap
from pathlib import Path


def ts(sec):
    h, rem = divmod(int(sec), 3600)
    m, s = divmod(rem, 60)
    ms = int(round((sec - int(sec)) * 1000))
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def chapter_ts(sec):
    m, s = divmod(int(sec), 60)
    return f"{m}:{s:02}"


def write_srt(sheet, out):
    cues, t, n = [], 0.0, 0
    for b in sheet["beats"]:
        dur = float(b.get("actual_duration_s") or 0)
        text = (b.get("narration_text") or "").strip()
        if text:
            n += 1
            lines = textwrap.wrap(text, 42)[:3]
            cues.append(f"{n}\n{ts(t)} --> {ts(t + dur - 0.05)}\n" + "\n".join(lines))
        t += dur
    out.write_text("\n\n".join(cues) + "\n")
    return n, t


def credits_block(folder):
    """Credits + disclosure from media/*.source.txt sidecars."""
    credits, disclosures = [], []
    for sc in sorted((folder / "media").glob("*.source.txt")):
        body = sc.read_text()
        bid = sc.name.split(".")[0]
        first = next((l.strip() for l in body.splitlines() if l.strip()), "")
        if "AI-GENERATED" in body or "synthetic" in body.lower():
            disclosures.append(bid)
            if first and "FILL-IN" not in first and not first.startswith("AI-GENERATED"):
                credits.append(f"{bid}: {first}")
        elif first and "FILL-IN" not in first:
            credits.append(f"{bid}: {first}")
    lines = []
    if credits:
        lines.append("Archival sources:")
        lines += [f"  {c}" for c in credits]
    if disclosures:
        lines.append(f"AI disclosure: motion in beats {', '.join(sorted(set(disclosures)))} "
                     "is AI-generated (Higgsfield), seeded from or standing in for "
                     "archival material. Details per shot in the repository.")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder", type=Path)
    a = ap.parse_args()
    folder = a.folder.resolve()
    sheet = json.loads((folder / "beat_sheet.json").read_text())
    m = sheet["metadata"]
    slug = m.get("slug", folder.name)
    title = m.get("title", slug)

    # mp4 staging (symlinks; the publisher follows them)
    mp4 = folder / "mp4"
    mp4.mkdir(exist_ok=True)
    land_src = folder / f"{slug}.mp4"
    short_src = folder / "short" / f"{slug}-short-cut.mp4"
    for src, name in ((land_src, f"{slug}.mp4"), (short_src, f"{slug}-short.mp4")):
        dst = mp4 / name
        if not src.exists():
            print(f"[emit] MISSING master: {src.name} — compile the clean cut first")
            continue
        if dst.is_symlink() or dst.exists():
            dst.unlink()
        dst.symlink_to(Path("..") / src.relative_to(folder))
        print(f"[emit] mp4/{name} -> {src.relative_to(folder)}")

    # captions, per surface, from the sheets
    n, total = write_srt(sheet, folder / f"{slug}.srt")
    print(f"[emit] {slug}.srt  ({n} cues, {total:.0f}s)")
    short_sheet_p = folder / "short" / "beat_sheet.json"
    if short_sheet_p.exists():
        ns, ts_ = write_srt(json.loads(short_sheet_p.read_text()),
                            folder / f"{slug}-short.srt")
        print(f"[emit] {slug}-short.srt  ({ns} cues, {ts_:.0f}s)")

    # description
    blurb = m.get("description_blurb") or next(
        (b["narration_text"] for b in sheet["beats"]
         if b.get("shot", {}).get("type") == "CARD"), "")
    chapters = ""
    if m.get("chapters"):
        t, at = 0.0, {}
        for b in sheet["beats"]:
            at[b["beat_id"]] = t
            t += float(b.get("actual_duration_s") or 0)
        rows = [(0.0 if i == 0 else at.get(bid, 0.0), label)
                for i, (bid, label) in enumerate(m["chapters"])]
        chapters = "\n".join(f"{chapter_ts(t)} {label}" for t, label in rows)
    # No topical default: a stale default ships the WRONG tags on every reel that
    # forgets its own (an MHS/robotics film went out tagged #physics #quantum
    # #sciencehistory, 2026-08-31). Reels set metadata.hashtags; absent that we
    # emit only the channel tag, which is true of every reel.
    tags = m.get("hashtags") or ["NikBearBrown"]
    src_chapter = m.get("source_chapter", "")
    parts = [title, "", blurb, ""]
    if chapters:
        parts += ["Chapters:", chapters, ""]
    # BOOKLOOP LAW: films teach the IDEA standalone and never name the book,
    # chapter, or course — the manuscripts are unpublished. This line used to be
    # unconditional and named "the source chapter" in EVERY description, including
    # reels with no chapter at all (2026-08-31). The claim we can always make is
    # the one about primary sources.
    parts += ["Every factual claim in this video was checked against primary "
              "sources before rendering.", ""]
    cb = credits_block(folder)
    if cb:
        parts += [cb, ""]
    parts += [" ".join("#"+t.lstrip("#") for t in tags), "", "youtube.com/@NikBearBrown"]
    md = folder / f"{slug}-youtube.md"
    md.write_text("\n".join(p for p in parts if p is not None))
    print(f"[emit] {md.name}")
    print(f"[emit] playlist: {m.get('playlist')!r} · shorts: {m.get('playlist_short')!r}")
    print("[emit] staged. Publish with youtube_publish.py "
          "--no-pairs --schedule-scope playlist --interval-hours 2")


if __name__ == "__main__":
    main()
