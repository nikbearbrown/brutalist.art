#!/usr/bin/env python3
"""seis_profile.py — scaffold + ledger for SEIS spotlight reels (skills/make/seis-profile).

One scraped COE spotlight story folder (story.md + meta.json + images, as written by
the seis scraper into books/seis/<slug>/) → one reel folder books/seis/youtube/seis-<slug>/
on the NEU skin (brands/seis.md). Deterministic, no LLM, no spend. The AUTHORING
pass (Claude Code following skills/make/seis/SKILL.md) fills profile.json, the
narration, the shots and FACTCHECK.md; this script only lays the table.

  python3 seis_profile.py <slug>            scaffold one story
  python3 seis_profile.py --all             scaffold every story under --src
  python3 seis_profile.py --ledger          write books/seis/youtube/REVIEW.md
  --src  books/seis (default)   --out books/seis/youtube (default)   --force  overwrite

Never overwrites an existing beat_sheet.json unless --force (authoring is precious).
"""
import argparse, json, os, re, shutil, sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLKIT = HERE.parent.parent                      # brutalist.art/
PUBLIC = TOOLKIT / "runtime" / "remotion" / "public" / "seis"
# Story corpus root: $SEIS_BOOKS if set, else the folder that contains this toolkit
# (Bear's layout is books/brutalist.art + books/seis; a SEIS clone sets SEIS_BOOKS
# or passes --src / --out explicitly). Never a laptop-specific absolute path.
BOOKS = Path(os.environ.get("SEIS_BOOKS", TOOLKIT.parent)).expanduser().resolve()
UNIT = "Software Engineering and Information Systems"
SCHOOL = "Northeastern University · College of Engineering"
CHANNEL_TITLE = "SEIS · Northeastern"             # until the YouTube handle is confirmed
LOGO_OPEN = "northeastern/official/monogram-red.svg"                  # the N alone reads at bug size (logos/seis/README.md)
LOGO_OUTRO = "northeastern/official/primary-logo-red-black.svg"     # monogram + wordmark, full size on the outro; SEIS lockup pending
TODAY = date.today().isoformat()

BODY_ACTS = [  # the spotlight arc — the author trims/merges, never pads (duration is an OUTPUT)
    ("B02", "before", "Where they came from — the foundation before Northeastern"),
    ("B03", "why-seis", "Why this program — the specific reason the article gives"),
    ("B04", "project-1", "First project / co-op — REBUILT as a concept illustration (REBUILD LAW)"),
    ("B05", "project-2", "Second project / co-op / research — REBUILT"),
    ("B06", "human", "The human detail the article offers (dance, a prior career, a hobby) — only if present"),
    ("B07", "next", "What's next — the aspiration, in the article's own scope"),
]


def slate_beat(bid, act, intent):
    return {
        "beat_id": bid, "act": act, "estimated_duration_s": 12,
        "narration_text": "", "audio_file": f"mp3/beat-{bid}.mp3",
        "new_visual_element": intent,
        "shot": {"type": "REMOTION", "source": "own", "visual_intent": intent,
                 "remotion": {"pattern": "SeisCard",
                              "props": {"label": "", "lines": [], "emphasis": -1}}},
        "_todo": "narration + shot (SHOW/HOLD/CARD per nopunt) — or delete this beat",
    }


def remotion_beat(bid, act, pattern, props, intent, est=8):
    return {"beat_id": bid, "act": act, "estimated_duration_s": est, "narration_text": "",
            "audio_file": f"mp3/beat-{bid}.mp3", "new_visual_element": intent,
            "shot": {"type": "REMOTION", "source": "own", "visual_intent": intent,
                     "remotion": {"pattern": pattern, "props": props}}}


def scaffold(slug, src, out, force=False):
    sdir = src / slug
    meta = json.loads((sdir / "meta.json").read_text())
    rdir = out / f"seis-{slug}"
    rdir.mkdir(parents=True, exist_ok=True)
    (rdir / "mp3").mkdir(exist_ok=True); (rdir / "media").mkdir(exist_ok=True)
    title, url, dt = meta["title"], meta["url"], meta.get("date", "")

    # hero photo → remotion/public/seis/<slug>.<ext> (as published; RIGHTS.md carries the credit)
    photo_rel, photo_credit = "", ""
    imgs = meta.get("image_details") or []
    if imgs and imgs[0].get("file"):
        srcimg = sdir / imgs[0]["file"]
        if srcimg.exists():
            PUBLIC.mkdir(parents=True, exist_ok=True)
            dest = PUBLIC / f"{slug}{srcimg.suffix}"
            if not dest.exists() or force: shutil.copy2(srcimg, dest)
            photo_rel = f"seis/{dest.name}"
            photo_credit = imgs[0].get("alt", "") or ""
    # the article's own photo credit line, if it printed one
    body = (sdir / "story.md").read_text()
    m = re.search(r"(Photo[^.\n]*?(?:sourced|courtesy)[^.\n]*\.|Courtesy photo\.)", body, re.I)
    if m: photo_credit = m.group(1).strip()

    # profile.json — the extraction record; null until the authoring pass fills it
    prof = rdir / "profile.json"
    if not prof.exists() or force:
        prof.write_text(json.dumps({
            "slug": slug, "title": title, "url": url, "date": dt,
            "student_name": None, "program": None, "term": None, "status": None,
            "thesis": None, "background_before_neu": None, "why_this_program": None,
            "projects": [], "personal_detail": None, "career_aspiration": None,
            "faculty_named": [], "employers_named": [], "public_links": [],
            "theme_tags": [], "photo": photo_rel, "photo_credit": photo_credit,
            "_rule": "every field paraphrased from story.md ONLY — never invented; null when absent",
        }, indent=2, ensure_ascii=False) + "\n")

    # Manim components + Lato ride along (scenes.py imports seis_graphics locally; run.sh renders from the reel dir)
    gfx = TOOLKIT / "runtime" / "manim" / "seis_graphics.py"
    if gfx.exists(): shutil.copy2(gfx, rdir / "seis_graphics.py")
    lato = TOOLKIT / "runtime" / "fonts" / "Lato" / "static" / "Lato-Regular.ttf"
    if lato.exists():
        (rdir / "fonts").mkdir(exist_ok=True); shutil.copy2(lato, rdir / "fonts" / "Lato-Regular.ttf")
    bs = rdir / "beat_sheet.json"
    if bs.exists() and not force:
        return f"exists  {rdir.name}"
    beats = [
        remotion_beat("B00", "open", "SeisSpotlightOpen", {
            "eyebrow": "Student spotlight", "name": "TODO name", "program": "TODO program",
            "term": "", "unit": UNIT, "school": SCHOOL, "photo": photo_rel, "photoCredit": photo_credit, "logo": LOGO_OPEN,
        }, "Spotlight open — name, program, the article's hero photo as published", est=10),
        remotion_beat("B01", "bluf", "SeisCard", {"label": "TODO name", "lines": [], "emphasis": -1},
                      "BLUF — the ONE idea this person's story lands (EXECUTIVE-SUMMARY LAW)", est=10),
    ] + [slate_beat(*a) for a in BODY_ACTS] + [
        remotion_beat("BVDT", "recap", "SeisCard", {"label": "TODO name", "lines": [], "emphasis": -1},
                      "Recap — the ONE idea restated, name on the card", est=8),
        remotion_beat("BHTF", "credit", "SeisProfileCredit", {
            "name": "TODO name", "role": "TODO program", "links": [],
            "storyUrl": url, "storyDate": dt, "storyAuthor": "",
        }, "PERSON CREDIT — links verbatim from the article only; read the full story", est=8),
        remotion_beat("BOUT", "outro", "SeisOutro", {
            "unit": UNIT, "school": SCHOOL, "series": "SEIS student spotlights", "handle": "@nu_seis", "url": url, "logo": LOGO_OUTRO,
        }, "SEIS outro — unit, school, series line; handle only once confirmed", est=6),
    ]
    sheet = {"metadata": {
        "slug": f"seis-{slug}", "title": title, "topic": "SEIS · STUDENT SPOTLIGHT",
        "purpose": f"SEIS spotlight reel of the COE story “{title}” ({dt}) for SEIS's YouTube.",
        "audience": "SEIS", "brand": "seis", "palette": "neu", "register": "Spotlight",
        "engine": "kokoro", "voice": "am_onyx", "voice_kokoro": "am_onyx", "persona": "Liam, for SEIS",
        "channel_title": CHANNEL_TITLE, "clock": "narration",
        "source": {"url": url, "date": dt, "scraped": meta.get("scraped", ""), "story_md": str(sdir / "story.md")},
        "_confirm": {"youtube_handle": None, "logo_lockup": None, "photo_rights": None},
    }, "beats": beats}
    bs.write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + "\n")

    (rdir / "SOURCES.md").write_text(
        f"# SOURCES — seis-{slug}\n\n- Article: {url}\n- Published: {dt}\n- Author: (COE — byline not printed on the page)\n"
        f"- Scraped: {meta.get('scraped','')} → `{sdir/'story.md'}`\n- Photo: {photo_rel or '(none)'} — credit: {photo_credit or '(none printed)'}\n\n"
        "Every narration claim traces to the article. No other source is permitted for facts about the person.\n")
    (rdir / "RIGHTS.md").write_text(
        f"# RIGHTS — seis-{slug}\n\n| Asset | As published by COE | Credit line | Re-use on YouTube |\n|---|---|---|---|\n"
        f"| {photo_rel or '(no photo)'} | {url} | {photo_credit or '(none printed)'} | CONFIRM with SEIS (Erin Macri) |\n\n"
        "The article text is COE's; the reel paraphrases it under SEIS's own request. Photos credited "
        "\"sourced from LinkedIn\" are the student's — SEIS confirms re-use before publish. Never published by this pipeline.\n")
    (rdir / "FACTCHECK.md").write_text(
        f"# FACTCHECK — seis-{slug}\n\nStatus: **GATE F NOT SIGNED — authoring pass pending.**\n"
        f"Single source: {url} (scraped copy in SOURCES.md). Every row's Source column names the paragraph.\n\n"
        "| # | Beat | Claim (as spoken / shown) | Verdict | Source / derivation | Fix if needed |\n|---|---|---|---|---|---|\n")
    (rdir / "SHOTLIST.md").write_text(
        f"# SHOTLIST — seis-{slug}\n\nTyped work order per beat (filled by the authoring pass).\n\n"
        "| Beat | Type (SHOW/HOLD/CARD) | Source (SeisCard / Manim neu / illustration) | What the viewer watches |\n|---|---|---|---|\n")
    (rdir / "PROMPTS.md").write_text(f"# PROMPTS — seis-{slug}\n\nNo generative media in this reel by default (REBUILD LAW; NEU imagery law). Log any Manim/illustration prompt here.\n")
    (rdir / "BUILD-PROMPT.md").write_text(
        f"# BUILD — seis-{slug}\n\nPaste into Claude Code from `brutalist.art/`:\n\n```\n"
        f"seis-profile author {slug}   # fill profile.json + narration + shots + FACTCHECK (skills/make/seis-profile/SKILL.md)\n"
        f"seis-profile build {slug}    # kokoro audio (am_onyx — Liam) → ART_PALETTE=neu render → compile → visual QC\n"
        "```\n\nNever publishes. The master lands as `seis-" + slug + "-cut.mp4` after `./art final`.\n")
    return f"scaffold {rdir.name}"


def ledger(out):
    rows = []
    for rdir in sorted(p for p in out.iterdir() if p.is_dir() and p.name.startswith("seis-")):
        bs = rdir / "beat_sheet.json"
        if not bs.exists(): continue
        d = json.loads(bs.read_text()); beats = d["beats"]
        todo = sum(1 for b in beats if b.get("_todo") or "TODO" in json.dumps(b.get("shot", {})))
        narr = sum(1 for b in beats if b.get("narration_text", "").strip())
        mp3 = sum(1 for b in beats if (rdir / b.get("audio_file", "")).exists())
        media = sum(1 for b in beats if (rdir / "media" / f"{b['beat_id']}.mp4").exists())
        master = any(rdir.glob("*-cut.mp4"))
        slate = any(rdir.glob("*-slate.mp4")) or any(rdir.glob("*review*.mp4"))
        fc = (rdir / "FACTCHECK.md").read_text()
        signed = "SIGNED" in fc.split("\n", 3)[2].upper() if fc.count("\n") > 2 else False
        conf = d.get("metadata", d).get("_confirm", {}); unconfirmed = [k for k, v in conf.items() if not v]
        stage = ("MASTER" if master else "SLATE" if slate else "RENDERED" if media == len(beats) else "AUDIO" if mp3 == len(beats)
                 else "AUTHORED" if narr == len(beats) and todo == 0 else "SCAFFOLD")
        rows.append((rdir.name, stage, f"{narr}/{len(beats)}", f"{mp3}/{len(beats)}", f"{media}/{len(beats)}",
                     "✓" if signed else "—", ", ".join(unconfirmed) or "—"))
    md = [f"# REVIEW — SEIS spotlight reels · {TODAY}\n", f"{len(rows)} reels. Stages: SCAFFOLD → AUTHORED → AUDIO → RENDERED → SLATE (review cut) → MASTER (./art final). Nothing here publishes.\n",
          "| Reel | Stage | Narration | Audio | Media | Gate F | Unconfirmed |", "|---|---|---|---|---|---|---|"]
    md += [f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]} | {r[6]} |" for r in rows]
    from collections import Counter
    c = Counter(r[1] for r in rows)
    md.insert(2, "  ".join(f"{k}: {v}" for k, v in sorted(c.items())) + "\n")
    (out / "REVIEW.md").write_text("\n".join(md) + "\n")
    return f"REVIEW.md — {len(rows)} reels: " + "  ".join(f"{k} {v}" for k, v in sorted(c.items()))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug", nargs="?"); ap.add_argument("--all", action="store_true")
    ap.add_argument("--ledger", action="store_true"); ap.add_argument("--force", action="store_true")
    ap.add_argument("--src", default=str(BOOKS / "seis")); ap.add_argument("--out", default=str(BOOKS / "seis" / "youtube"))
    a = ap.parse_args(); src, out = Path(a.src), Path(a.out)
    if a.ledger: print(ledger(out)); return
    slugs = [a.slug] if a.slug else ([p.name for p in sorted(src.iterdir()) if (p / "meta.json").exists()] if a.all else [])
    if not slugs: ap.error("give a slug, --all, or --ledger")
    for s in slugs: print(scaffold(s, src, out, a.force))
    print(ledger(out))


if __name__ == "__main__":
    main()
