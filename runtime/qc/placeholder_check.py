#!/usr/bin/env python3
"""
placeholder_check.py — HOLD vs PUNT classifier for unfilled STILL/archive beats.

For every beat whose shot.type is STILL (or COMPOSITE) with source=archive and
whose media slot is not yet filled, this script decides:

  HOLD  — the beat genuinely requires a human:
             a real archival photograph, government document, specific named
             person's blog/paper screenshot, or a judgment only Bear can make.
             Kept as a placeholder; logged in the report with the reason.

  PUNT  — the machine can author this itself:
             a diagram, chart, table, code/terminal illustration, or any
             generatable figure. Remaining as STILL when the system could
             build it is a defect (exit code 1 — warning, never a hard block).

Exit codes
----------
  0   all STILL placeholders are HOLD (or there are none) — clean
  1   at least one PUNT placeholder remains unfilled — defect, non-blocking

The script NEVER exits with code ≥ 2. It must not block art run.

Usage
-----
  python3 placeholder_check.py <reel_dir>            # prints table to stdout
  python3 placeholder_check.py <reel_dir> --md       # also writes PLACEHOLDER.md
"""

import json
import os
import re
import sys
from pathlib import Path

# ── HOLD heuristics ──────────────────────────────────────────────────────────
# If ANY of these patterns match the beat's prompt/description, classify HOLD.

HOLD_PATTERNS = [
    # Government / official sources (real screenshots needed for credibility)
    # NOTE: only a HOLD if the beat genuinely needs the DOCUMENT VISUAL (screenshot).
    # Beats that illustrate a FACT about a document (e.g. "disclosed vs not") are PUNT.
    r"\bnist\.gov\b",
    r"\baisi\.gov\b",
    r"\.gov\b",
    r"\bpress release\b",
    r"\bofficial website\b",
    r"\bgovernment\b",
    # Named real-person content (fabricating would misrepresent)
    r"\bsimonwillison\.net\b",
    r"\bwillison\b",
    r"\bsubstack\b",
    r"\barxiv\.org\b",
    r"\bnature\.com\b",
    # Tier 2 shopping (real archival screenshot explicitly required)
    r"\btier 2\b",
    # PDF page extractions (file must exist in pantry)
    r"pdftopdf",
    r"render from pdf",
]

# ── PUNT heuristics ──────────────────────────────────────────────────────────
# If NO HOLD pattern matches AND any PUNT pattern matches, classify PUNT.
# If neither matches, default to PUNT (machine can usually make a diagram).
#
# KEY RULE: The ONLY archive HOLD is a genuine photograph of a real, existing
# person/place/event/document. For ai-explainer data/concept reels, expect
# ~zero archive stills. A body full of "drop a historical image" asks for
# data/stats/concepts is a laziness signal — flag all of them as PUNTs.
#
# "extract from *.mp4" and "ffmpeg *.mp4" requests for promo/demo video frames
# are PUNT: the machine can author the concept/stat as a clean Manim diagram.
# (Genuine documentary extracts that are in pantry are skipped via _slot_filled.)

PUNT_PATTERNS = [
    r"\btier 1\b",
    r"\bany diagram\b",
    r"\bany chart\b",
    r"\bany screenshot\b",
    r"\bconceptual\b",
    r"\barchitecture diagram\b",
    r"\bterminal\b",
    r"\bci output\b",
    r"\bcode\b",
    r"\btable\b",
    r"\bflow diagram\b",
    r"\bbar chart\b",
    r"\bmanim\b",
    r"\bno real person\b",
    r"\brepresents? the concept\b",
    r"\brepresents? \w+ concept\b",
    # Data/stat/concept beats — machine can make a clean diagram
    r"\bstat card\b",
    r"\blower.?bound\b",
    r"\beval number\b",
    r"\bdisclosure\b",
    r"\bdisclosed\b",
    r"\bcoherent\b.*\b(story|pattern|picture)\b",
    # Promo/demo video frame extracts — not genuine archival photographs
    r"extract from.*\.mp4",
    r"ffmpeg.*\.mp4",
    r"promo(tional)? video",
    r"\bdemo.{0,10}video\b",
    r"kimi.*demo",
    r"open.world.*\.mp4",
    # Generic "drop a historical image" asks for concept content
    r"drop.*historical.*image",
    r"historical.*image",
    r"drop.*an? image",
]


def _match_any(text: str, patterns: list[str]) -> str | None:
    """Return first matching pattern label, or None."""
    low = text.lower()
    for p in patterns:
        m = re.search(p, low)
        if m:
            return p
    return None


def _slot_filled(beat: dict, reel_dir: Path) -> bool:
    """True only if the beat has been filled with real (non-slate) media.

    Pantry assets (human-dropped PNGs/MP4s) always count as filled even if the
    pipeline hasn't yet converted them to a final clip. Clips from the pipeline
    are only counted if build.status is not SLATE.
    """
    bid = beat.get("beat_id") or beat.get("id", "")

    # Pantry: human-dropped files always count as filled
    pantry = reel_dir / "pantry"
    if pantry.exists():
        for f in pantry.iterdir():
            stem = f.stem
            if (stem.startswith(bid + "-") or stem == bid) and not f.is_dir():
                return True

    # Build stamp: MANIM/VIDEO/STILL etc. mean genuinely filled by the pipeline
    build = beat.get("build") or {}
    status = build.get("status", "")
    if status and status != "SLATE":
        return True

    # No build stamp and no pantry file → unfilled
    # (clips/ is always machine-generated slates, not counted)
    return False


def _prompt_text(beat: dict) -> str:
    """Collect all free-text fields that might describe what media is needed."""
    parts = []
    for key in ("prompt", "description", "graphic", "pantry", "shopping"):
        v = beat.get(key, "")
        if isinstance(v, str):
            parts.append(v)
        elif isinstance(v, dict):
            parts.append(str(v))
    # also include intent + narration_text for context
    for key in ("intent", "narration_text", "narration"):
        v = beat.get(key, "")
        if isinstance(v, str):
            parts.append(v)
    return " ".join(parts)


def classify_beat(beat: dict) -> tuple[str, str]:
    """Returns (label, reason): label='HOLD'|'PUNT', reason=short string."""
    text = _prompt_text(beat)
    hold_match = _match_any(text, HOLD_PATTERNS)
    if hold_match:
        # Derive a human-readable reason from which pattern matched
        reasons = {
            r"\bnist\.gov\b": "real government document (NIST)",
            r"\baisi\.gov\b": "real government document (AISI)",
            r"\.gov\b": "real government document",
            r"\bpress release\b": "official press release — fabricating it is deceptive",
            r"\bofficial website\b": "official website screenshot needed",
            r"\bgovernment\b": "government source — real screenshot required",
            r"\bsimonwillison\.net\b": "Simon Willison's blog post — real screenshot for citation credibility",
            r"\bwillison\b": "named person's content — real screenshot for citation credibility",
            r"\bsubstack\b": "named Substack post — real screenshot for source credibility",
            r"\barxiv\.org\b": "arxiv paper screenshot — real document needed",
            r"\bnature\.com\b": "Nature article screenshot — real document needed",
            r"\btier 2\b": "Tier 2 shopping: real archival screenshot explicitly required",
            r"ffmpeg.*\.mp4": "specific video frame extraction — file must be in pantry",
            r"extract from.*\.mp4": "specific video frame extraction — file must be in pantry",
            r"pdftopdf": "PDF page extraction — real PDF must be in pantry",
            r"render from pdf": "PDF page extraction — real PDF must be in pantry",
        }
        return "HOLD", reasons.get(hold_match, f"matched HOLD pattern: {hold_match}")
    # No HOLD markers — this is a PUNT
    punt_match = _match_any(text, PUNT_PATTERNS)
    if punt_match:
        return "PUNT", f"generatable ({punt_match.strip()})"
    # Default: if it's a plain STILL with no markers, assume PUNT (machine can diagram it)
    return "PUNT", "no HOLD markers — diagram or chart can be authored by the pipeline"


def run(reel_dir: Path, write_md: bool = False) -> int:
    bs_path = reel_dir / "beat_sheet.json"
    if not bs_path.exists():
        print(f"[placeholder] no beat_sheet.json at {reel_dir}")
        return 0

    with open(bs_path) as f:
        bs = json.load(f)

    rows = []
    for beat in bs["beats"]:
        bid = beat.get("beat_id") or beat.get("id", "?")
        sh = beat.get("shot", {})
        shot_type = sh.get("type", "")
        source = sh.get("source", "")

        # Only classify unfilled STILL/archive beats
        if shot_type not in ("STILL", "COMPOSITE"):
            continue
        if source not in ("archive", ""):
            continue
        if _slot_filled(beat, reel_dir):
            continue  # already provided by human — skip

        label, reason = classify_beat(beat)
        rows.append((bid, label, reason))

    if not rows:
        if write_md:
            _write_md(reel_dir, rows)
        return 0

    # Print table
    reel_name = reel_dir.name
    print(f"\n[placeholder] {reel_name} — {len(rows)} unfilled STILL/archive beat(s)")
    punts = [r for r in rows if r[1] == "PUNT"]
    holds = [r for r in rows if r[1] == "HOLD"]

    print(f"  HOLD: {len(holds)}   PUNT: {len(punts)}")
    for bid, label, reason in rows:
        flag = "⚠" if label == "PUNT" else "—"
        print(f"  {flag} {bid:6s}  {label:4s}  {reason}")

    if punts:
        print(f"\n[placeholder] DEFECT: {len(punts)} PUNT beat(s) remain as STILL placeholders.")
        print(f"[placeholder] The pipeline can author these — add Manim/Remotion scenes and re-run.")

    if write_md:
        _write_md(reel_dir, rows)

    return 1 if punts else 0


def _write_md(reel_dir: Path, rows: list) -> None:
    lines = ["# PLACEHOLDER.md — HOLD vs PUNT audit\n"]
    if not rows:
        lines.append("*No unfilled STILL/archive placeholders.*\n")
    else:
        lines.append("| Beat | Class | Reason |\n")
        lines.append("|------|-------|--------|\n")
        for bid, label, reason in rows:
            lines.append(f"| {bid} | **{label}** | {reason} |\n")
        punts = [r for r in rows if r[1] == "PUNT"]
        if punts:
            lines.append(f"\n> **{len(punts)} PUNT beat(s)** — the pipeline can author these. "
                          f"Add a Manim scene or Remotion beat and re-run.\n")
    with open(reel_dir / "PLACEHOLDER.md", "w") as f:
        f.writelines(lines)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("reel_dir")
    ap.add_argument("--md", action="store_true", help="also write PLACEHOLDER.md")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    reel = Path(args.reel_dir)
    rc = run(reel, write_md=args.md)
    sys.exit(rc)
