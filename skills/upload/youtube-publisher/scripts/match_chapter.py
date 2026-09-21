#!/usr/bin/env python3
"""
match_chapter.py — match a NotebookLM transcript to a book chapter.

Compares the transcript text against every chapter markdown file in a chapters/
directory using TF-IDF cosine similarity (pure stdlib, no extra deps) and prints
a ranked list. The top match is almost always right for these deep-dive videos,
but the ranking lets a human confirm — the chapter number sets the playlist order,
so a wrong match reorders the playlist.

Usage:
    python match_chapter.py path/to/Video.transcript.json --chapters path/to/chapters
    python match_chapter.py path/to/Video.transcript.json --chapters ../chapters --json

Outputs (with --json): {"video": "...", "best": {"file": "05-...md", "number": 5,
                        "title": "...", "score": 0.42}, "ranking": [...]}
"""
from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter
from pathlib import Path

STOP = set("""a an the and or of to in on for is are was were be been being this that these those
it its as at by with from into over under about above below then than so such no not can will would
you your we our they their he she his her i me my mine ours vs via if but each per most more less
one two into onto within without between across during after before now here there what which who whom
whose how why when where all any both few many other some own same only very just also into out up down""".split())


def tokens(text: str) -> list[str]:
    return [w for w in re.findall(r"[a-z][a-z0-9\-']+", text.lower()) if w not in STOP and len(w) > 2]


def chapter_number(path: Path) -> int | None:
    m = re.match(r"(\d+)", path.stem)
    return int(m.group(1)) if m else None


def chapter_title(path: Path) -> str:
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("transcript", help="the .transcript.json produced by transcribe.py")
    ap.add_argument("--chapters", required=True, help="directory of NN-*.md chapter files")
    ap.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    ap.add_argument("--skip", default="00,99",
                    help="comma-separated chapter-number prefixes to ignore (front/back matter)")
    args = ap.parse_args()

    t = json.loads(Path(args.transcript).read_text())
    q_tokens = tokens(t["text"])

    ch_dir = Path(args.chapters).expanduser().resolve()
    skip = {s.strip() for s in args.skip.split(",") if s.strip()}
    chapters = [p for p in sorted(ch_dir.glob("*.md"))
                if not any(p.stem.startswith(s) for s in skip)]
    if not chapters:
        raise SystemExit(f"[match] no chapter .md files under {ch_dir}")

    # Build document token lists and document frequencies for IDF.
    docs = {p: tokens(p.read_text(encoding="utf-8", errors="ignore")) for p in chapters}
    df = Counter()
    for toks in docs.values():
        for w in set(toks):
            df[w] += 1
    N = len(docs)
    idf = {w: math.log((N + 1) / (df[w] + 1)) + 1 for w in df}

    def vec(toks):
        tf = Counter(toks)
        return {w: (tf[w] / len(toks)) * idf.get(w, 0.0) for w in tf if w in idf}

    qv = vec(q_tokens)

    def cosine(a, b):
        common = set(a) & set(b)
        num = sum(a[w] * b[w] for w in common)
        na = math.sqrt(sum(v * v for v in a.values()))
        nb = math.sqrt(sum(v * v for v in b.values()))
        return num / (na * nb) if na and nb else 0.0

    ranking = []
    for p, toks in docs.items():
        ranking.append({
            "file": p.name, "number": chapter_number(p),
            "title": chapter_title(p), "score": round(cosine(qv, vec(toks)), 4),
        })
    ranking.sort(key=lambda r: r["score"], reverse=True)

    if args.json:
        print(json.dumps({"video": t.get("video"), "best": ranking[0], "ranking": ranking},
                         ensure_ascii=False, indent=1))
    else:
        print(f"\nVideo: {t.get('video')}")
        print("Ranked chapter matches (higher = closer):")
        for r in ranking:
            mark = "  <= best" if r is ranking[0] else ""
            print(f"  {r['score']:.4f}  ch{r['number']:>2}  {r['title']}{mark}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
