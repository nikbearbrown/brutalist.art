#!/usr/bin/env python3
"""
build_description.py — assemble the YouTube description in Medhavy house style.

Produces two files in the video folder:
  <slug>-youtube.md   editable, human-readable draft (title, hook, learn, physics,
                      chapters, footer) — this is where a human refines wording.
  description.txt     the EXACT text uploaded as the YouTube description
                      (everything except the title), rebuilt from the .md.

It fills what it can automatically — chapter line, timestamp list (from chapters.json),
brand footer, hashtags — and seeds the hook / "What you'll learn" / "The physics"
from the matched chapter. Treat those seeded paragraphs and the chapter LABELS as a
DRAFT: the chapter's first paragraph rarely doubles as a good YouTube hook, and the
timestamp labels come in as "<rewrite me>". Edit the .md, then re-run with --refresh
to regenerate description.txt from your edited .md.

Usage:
    python build_description.py <folder> --chapter path/to/NN-*.md          # first pass
    python build_description.py <folder> --refresh                          # after editing .md
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

FOOTER = (
    "Medhavy · AI-powered intelligent learning systems · @MedhavyAI · medhavy.com\n"
    "A NotebookLM deep dive, bookended and published by Medhavy."
)
HASHTAGS = ("#QuantumMechanics #Physics #NotebookLM #Medhavy #QuantumPhysics "
            "#PhysicsExplained #DeepDive #ScienceEducation")


def chapter_headings(chapter: Path, limit: int = 8) -> list[str]:
    heads = []
    for line in chapter.read_text(encoding="utf-8", errors="ignore").splitlines():
        m = re.match(r"^#{2,3}\s+(.*)", line)
        if m:
            h = m.group(1).strip()
            if h and not h.lower().startswith(("exercise", "problem", "summary")):
                heads.append(h)
    return heads[:limit]


def first_para(chapter: Path) -> str:
    for line in chapter.read_text(encoding="utf-8", errors="ignore").splitlines():
        s = line.strip()
        if s and not s.startswith(("#", "!", "|", "-", "*", ">", "`")):
            return s
    return ""


def timestamp_block(folder: Path) -> str:
    cj = folder / "chapters.json"
    if not cj.exists():
        return "0:00 Intro"
    markers = json.loads(cj.read_text())
    lines = []
    for m in markers:
        label = m["label"]
        if label == "<rewrite me>":
            label = (m.get("snippet") or "…").rstrip(".") + "  <-- rewrite"
        lines.append(f"{m['t']} {label}")
    return "\n".join(lines)


def build_md(folder: Path, chapter: Path) -> str:
    sheet = json.loads((folder / "beat_sheet.json").read_text())
    md = sheet["metadata"]
    num = md.get("chapter_number")
    ch_line = (f"Quantum Mechanics Vol. 1 · Chapter {num} — {md.get('chapter_title','')}"
               if num else md.get("chapter_title", ""))
    heads = chapter_headings(chapter)
    learn = "; ".join(heads[:5]) if heads else "the core ideas of this chapter"

    return f"""**Title:** {md['title']}

{first_para(chapter)}

**What you'll learn:** This NotebookLM deep dive walks through {learn}. \
Edit this line into a punchy 1–2 sentence hook aimed at a curious viewer.

**The physics:** {md.get('chapter_title','')} — summarise the key result(s) in 2–3 \
sentences drawn from the chapter. Keep the real numbers and equations.

**Chapters:**
{timestamp_block(folder)}

**From:** {ch_line}

---
Physics deep dives, narrated by AI. This episode is a NotebookLM conversation on \
Chapter {num if num else ''}, with a Medhavy intro and outro.
{FOOTER}

{HASHTAGS}
"""


def md_to_description(md_text: str) -> str:
    """Flatten the editable .md into the plain description.txt YouTube expects:
    drop the **Title:** line and markdown bold, keep everything else verbatim."""
    out = []
    for line in md_text.splitlines():
        if line.startswith("**Title:**"):
            continue
        line = re.sub(r"\*\*(.+?)\*\*", r"\1", line)   # unbold
        out.append(line)
    text = "\n".join(out).strip()
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("folder")
    ap.add_argument("--chapter", help="matched chapter .md (required on first pass)")
    ap.add_argument("--refresh", action="store_true",
                    help="regenerate description.txt from the already-edited <slug>-youtube.md")
    args = ap.parse_args()

    folder = Path(args.folder).expanduser().resolve()
    sheet = json.loads((folder / "beat_sheet.json").read_text())
    slug = sheet["metadata"]["slug"]
    md_path = folder / f"{slug}-youtube.md"

    if args.refresh:
        if not md_path.exists():
            raise SystemExit(f"[desc] {md_path} not found; run the first pass with --chapter first")
        md_text = md_path.read_text()
    else:
        if not args.chapter:
            raise SystemExit("[desc] first pass needs --chapter path/to/NN-*.md")
        md_text = build_md(folder, Path(args.chapter).expanduser().resolve())
        md_path.write_text(md_text, encoding="utf-8")

    (folder / "description.txt").write_text(md_to_description(md_text), encoding="utf-8")
    print(f"[desc] wrote {md_path.name} and description.txt")
    if not args.refresh:
        print("[desc] NEXT: edit the hook, the 'What you'll learn' line, 'The physics', "
              "and the chapter labels in the .md, then run again with --refresh.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
