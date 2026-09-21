#!/usr/bin/env python3
"""brand_variant.py — scaffold an audience variant beat sheet from the canonical one.

BRUTALIST (pared-down) EDITION: three brands only — claude-liam, nbb, hai —
and Kokoro is the ONLY engine. Two voices ship with the toolkit:
  am_onyx  "Onyx"  → claude-liam (Liam in for Bear) and nbb
  af_bella "Bella" → hai

Every reel starts with beat_sheet.json (the canonical cut). A variant is written
as beat_sheet.<suffix>.json inside a new <suffix>- directory. The canonical
beat_sheet.json is NEVER modified.

This script does the DETERMINISTIC half — audience metadata (engine, kokoro
voice, palette, register). The creative half — rewriting each beat's narration
into the register, the signature exercise beat, the audience outro — is done by
Claude, guided by skills/make/nbb/SKILL.md or skills/make/hai/SKILL.md.

Directory convention (source never modified):
  <book>/youtube/<slug>/              →  <book>/youtube/<suffix>-<slug>/
  <book>/lectures/<chapter>-lecture/  →  <book>/<suffix>-lectures/<chapter>-lecture/

Usage:
  python3 scripts/brand_variant.py <REEL_OR_LECTURE> {claude-liam|nbb|hai}
"""
import argparse, json, shutil, sys
from pathlib import Path

AUD = {
    "claude-liam": {"suffix": "claude-liam", "audience": "Claude",
                    "palette": "claude", "register": "Teardown",
                    "charter": "CLAUDE-BRAND.md", "author_section": "NikBearBrown",
                    "engine": "kokoro", "voice_kokoro": "am_onyx", "use_dir": True},
    "nbb": {"suffix": "nbb", "audience": "NikBearBrown",
            "palette": "teardown", "register": "Teardown",
            "charter": "brands/nbb.md", "author_section": "NikBearBrown",
            "engine": "kokoro", "voice_kokoro": "am_onyx", "use_dir": True},
    "seis": {"suffix": "seis", "audience": "SEIS", "voice_env": "ELEVENLABS_VOICE_LIAM",
            "voice_fallback_env": "ELEVENLABS_VOICE_NEU",
            "palette": "neu", "register": "Spotlight", "charter": "brands/seis.md",
            "author_section": "SEIS", "persona": "Liam, for SEIS",
            "engine": "kokoro", "voice_kokoro": "am_onyx"},
    "hai": {"suffix": "hai", "audience": "HAI",
            "palette": "humanitarians", "register": "Plain",
            "charter": "brands/hai.md", "author_section": "Humanitarians AI",
            "engine": "kokoro", "voice_kokoro": "af_bella", "use_dir": True},
}


def get_brand_dir(reel: Path, suffix: str) -> Path:
    parts = list(reel.parts)
    if 'lectures' in parts:
        idx = parts.index('lectures')
        book_dir = Path(*parts[:idx])
        return book_dir / f'{suffix}-lectures' / reel.name
    return reel.parent / f'{suffix}-{reel.name}'


def copy_build_scripts(src: Path, dst: Path) -> list:
    copied = []
    for p in (list(src.glob('build_deck.py')) + list(src.glob('render.py'))
              + list(src.glob('make_audio*.py'))):
        shutil.copy2(p, dst / p.name)
        copied.append(p.name)
    return copied


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("reel", type=Path)
    ap.add_argument("audience", choices=list(AUD))
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    cfg = AUD[a.audience]
    reel = a.reel.resolve()

    src = reel / "beat_sheet.json"
    if not src.exists():
        sys.exit(f"[variant] no beat_sheet.json in {reel}")

    out_dir = get_brand_dir(reel, cfg["suffix"])
    out = out_dir / f"beat_sheet.{cfg['suffix']}.json"
    if out.exists() and not a.force:
        sys.exit(f"[variant] {out} already exists (use --force to reset it from canonical)")
    out_dir.mkdir(parents=True, exist_ok=True)

    sheet = json.loads(src.read_text())
    meta = sheet.setdefault("metadata", {})

    meta["audience"] = cfg["audience"]
    meta["derived_from"] = "beat_sheet.json"
    meta["register"] = cfg["register"]
    meta["palette"] = cfg["palette"]
    meta["outro_source"] = f"AUTHOR.MD :: {cfg['author_section']}"
    meta["engine"] = cfg["engine"]
    meta["voice_kokoro"] = cfg["voice_kokoro"]
    meta.pop("voice_id", None)          # no paid engines in this toolkit
    if a.audience == "hai":
        meta["typography"] = {"serif": "EB Garamond", "sans": "Montserrat"}
        meta["channel_title"] = "@HumanitariansAI"
    elif a.audience == "nbb":
        meta["typography"] = {"display": "Montserrat", "serif": "EB Garamond", "mono": "PT Mono"}

    if a.audience == "hai":
        meta["_variant_todo"] = [
            "rewrite every beat narration_text/text in the Plain register "
            "(runtime/prose/plain/PROSE.md + brands/hai.md) — method, when to use, "
            "when NOT to/where it fails; voice only, facts unchanged",
            "optional: add ONE Irreducibly-Human tangent beat (0-1 per video, ONLY on a clear opportunity)",
            "add CLI worked exercise as the SECOND-TO-LAST beat "
            "(paste-ready ASK→OUTPUT→CHANGE→OUTPUT, NEXT STEP; see skills/make/hai/SKILL.md §Step 4)",
            f"add/replace outro with Humanitarians AI outro from {meta['outro_source']} (LAST beat)",
            "verify ending order: body → [tangent] → [CLI exercise] → [outro]",
            "then build: generate_audio_kokoro.py (voice af_bella) → palette=humanitarians → compile",
        ]
    elif a.audience == "nbb":
        meta["_variant_todo"] = [
            "rewrite every beat narration_text/text in the Teardown register "
            "(runtime/prose/teardown/PROSE.md + brands/nbb.md) — take it apart, explain how "
            "each piece works, judge the design choices; voice only, facts unchanged",
            "add LLM exercise as the SECOND-TO-LAST beat "
            "(paste-ready prompt for Claude/ChatGPT/Gemini + dig-deeper follow-up; "
            "see skills/make/nbb/SKILL.md §Step 3)",
            f"add/replace outro with NikBearBrown outro from {meta['outro_source']} (LAST beat)",
            "verify ending order: body → [LLM exercise] → [outro]",
            "build: generate_audio_kokoro.py (voice am_onyx) → palette=teardown → compile",
        ]
    else:
        meta["_variant_todo"] = [
            "rewrite every beat narration_text in the Teardown register — voice only, facts unchanged",
            "B00 says '…this is Liam, in for Bear.' and the outro signs off the same way (IN-FOR-BEAR LAW)",
            "then build: generate_audio_kokoro.py (voice am_onyx) → palette=claude → compile",
        ]

    # durations change with the rewrite; drop stale render stamps so they recompute
    for b in sheet.get("beats", []):
        b.pop("actual_duration_s", None)
        b.get("shot", {}).pop("rendered", None) if isinstance(b.get("shot"), dict) else None
    for seg in sheet.get("segments", []):
        for b in seg.get("beats", []):
            b.pop("actual_duration_s", None)

    out.write_text(json.dumps(sheet, indent=1, ensure_ascii=False))
    copied = copy_build_scripts(reel, out_dir)
    if copied:
        print(f"[variant] copied build scripts: {', '.join(sorted(copied))}")
    beat_count = len(sheet.get("beats", []))
    seg_count = len(sheet.get("segments", []))
    content_note = (f"{beat_count} beats" if beat_count else f"{seg_count} segments")
    print(f"[variant] wrote {out}  audience={cfg['audience']}  register={cfg['register']}  "
          f"palette={cfg['palette']}  engine=kokoro  voice={cfg['voice_kokoro']}")
    print(f"[variant] {content_note} to rewrite in {cfg['register']} — "
          f"next: follow skills/make/{a.audience if a.audience in ('nbb','hai') else 'ai-explainer'}/SKILL.md")


if __name__ == "__main__":
    main()
