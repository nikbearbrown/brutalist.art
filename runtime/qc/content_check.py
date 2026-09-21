#!/usr/bin/env python3
"""
content_check.py — GATE CONTENT: placeholder, missing-prop, and cross-reel contamination check.

Three failure classes (all block — not warnings):

  PLACEHOLDER     — a rendered string equals a known filler sentinel or generic placeholder.
                    Caught: "Key point one/two/three", "Lorem", "Topic", "⚠ SET * IN BEAT SHEET",
                    and any item label matching the "Key point N" pattern.

  MISSING-PROP    — a required content prop is absent from a beat's remotion.props, causing the
                    component to render its compiled-in default. For ClaudeComposerAsk, the
                    dangerous missing props are: segment (defaults to "Photoelectric Effect"
                    in the unfixed component) and command.

  FOREIGN-DEFAULT — a prop value matches a known component default that carries content from
                    another reel (e.g. segment="Photoelectric Effect" in a non-photoelectric reel).
                    After the fix, sentinel values make this class redundant, but it still catches
                    the pre-fix state and explicit copy-paste contamination.

Exit: 2 if any failure, 0 if clean.

Usage:
  python3 content_check.py <reel_dir>
  python3 content_check.py <reel_dir> --sheet beat_sheet.json
"""
import argparse, json, re, sys
from pathlib import Path

# ── Placeholder sentinel prefix (post-fix standard) ──────────────────────────
SENTINEL_PREFIX = "⚠ SET"

# ── Known generic filler strings (case-insensitive) ──────────────────────────
_FILLER = {
    "lorem", "lorem ipsum", "topic", "title here", "placeholder",
    "your title here", "add text here", "tbd", "to be determined",
    "sample text", "example text", "insert text", "enter text here",
    "key point one", "key point two", "key point three", "key point four",
    "key point 1",  "key point 2",   "key point 3",    "key point 4",
}

# ── "Key point N" pattern ─────────────────────────────────────────────────────
_KEY_POINT_RE = re.compile(r'^key\s+point\s+\w+$', re.IGNORECASE)

# ── Known dangerous component defaults (pre-fix; must still be caught) ───────
# Maps (pattern, prop) → dangerous_default_value
_DANGEROUS_DEFAULTS = {
    ("ClaudeComposerAsk", "segment"):     "Photoelectric Effect",
    ("ClaudeComposerAsk", "command"):     'claude "write a Manim scene: photoelectric effect"',
    ("ClaudeComposerAsk", "topic"):       "CLAUDE CODE · MANIM",
    ("ClaudeComposerAsk", "greeting"):    "Hola, Bear",
    ("ClaudeComposerAsk", "runningText"): "running simulation…",
}

# ── Required props for key components ────────────────────────────────────────
# Any beat using this pattern that is MISSING these props will render the
# compiled-in default (often a foreign reel's content).
_REQUIRED_PROPS = {
    "ClaudeComposerAsk": ["segment", "command"],
}


def is_placeholder(s: str) -> bool:
    """True if s is a sentinel or known filler."""
    if not s:
        return False
    low = s.strip().lower()
    if low.startswith(SENTINEL_PREFIX.lower()):
        return True
    if low in _FILLER:
        return True
    if _KEY_POINT_RE.match(low):
        return True
    return False


def check_props_recursive(bid: str, pattern: str, props: dict,
                          path: str = "") -> list:
    """Walk all string values in props recursively and flag placeholders."""
    failures = []
    for k, v in props.items():
        current_path = f"{path}.{k}" if path else k
        if isinstance(v, str):
            if is_placeholder(v):
                failures.append((
                    "PLACEHOLDER", f"{pattern}.props.{current_path}",
                    f"value is a placeholder or sentinel: {v!r}"
                ))
        elif isinstance(v, list):
            for i, item in enumerate(v):
                if isinstance(item, str):
                    if is_placeholder(item):
                        failures.append((
                            "PLACEHOLDER",
                            f"{pattern}.props.{current_path}[{i}]",
                            f"value is a placeholder or sentinel: {item!r}"
                        ))
                elif isinstance(item, dict):
                    failures.extend(
                        check_props_recursive(bid, pattern, item,
                                              f"{current_path}[{i}]"))
        elif isinstance(v, dict):
            failures.extend(
                check_props_recursive(bid, pattern, v, current_path))
    return failures


def check_missing_required(bid: str, pattern: str, props: dict) -> list:
    """Flag required props missing from ClaudeComposerAsk (and similar) beats."""
    failures = []
    required = _REQUIRED_PROPS.get(pattern, [])
    for prop in required:
        if prop not in props:
            danger = _DANGEROUS_DEFAULTS.get((pattern, prop))
            detail = (f" — will render component default {danger!r} "
                      f"(foreign reel content)" if danger else
                      " — will render compiled-in default (unknown content)")
            failures.append((
                "MISSING-PROP", f"{pattern}.props.{prop}",
                f"required prop {prop!r} absent{detail}"
            ))
    return failures


def check_foreign_defaults(bid: str, pattern: str, props: dict,
                            slug: str) -> list:
    """Flag prop values that are known-foreign compiled-in defaults."""
    failures = []
    for (pat, prop), danger_val in _DANGEROUS_DEFAULTS.items():
        if pat != pattern:
            continue
        if prop not in props:
            continue  # missing props caught by check_missing_required
        actual = props[prop]
        if actual == danger_val:
            failures.append((
                "FOREIGN-DEFAULT", f"{pattern}.props.{prop}",
                f"value {actual!r} is a compiled-in component default "
                f"that carries content from another reel"
            ))
    return failures


def check_beat(beat: dict, slug: str) -> list:
    bid   = beat.get("beat_id") or beat.get("id") or "?"
    shot  = beat.get("shot") or {}
    rem   = shot.get("remotion") or beat.get("remotion") or {}
    pat   = str(rem.get("pattern") or "")
    props = rem.get("props") or {}

    failures = []
    if not pat or not props:
        return failures

    failures += check_props_recursive(bid, pat, props)
    failures += check_missing_required(bid, pat, props)
    failures += check_foreign_defaults(bid, pat, props, slug)
    return [(bid, sev, kind, msg) for sev, kind, msg in failures]


def main():
    ap = argparse.ArgumentParser(description="Placeholder / missing-prop / contamination gate")
    ap.add_argument("reel", type=Path)
    ap.add_argument("--sheet", default="beat_sheet.json")
    a = ap.parse_args()

    sheet_path = a.reel / a.sheet
    if not sheet_path.exists():
        sys.exit(f"[content-check] ERROR: no {a.sheet} at {sheet_path}")

    sheet = json.loads(sheet_path.read_text())
    beats = sheet.get("beats") or []
    slug  = (sheet.get("metadata") or {}).get("slug", a.reel.name)

    print(f"[content-check] {slug}  beats={len(beats)}")

    all_failures = []
    for b in beats:
        for bid, sev, kind, msg in check_beat(b, slug):
            all_failures.append((bid, sev, kind, msg))
            print(f"[content-check] FAIL {bid}: [{sev}] {kind} — {msg}")

    if all_failures:
        print(f"\n[content-check] FAILED — {len(all_failures)} content violation(s). "
              f"Fix placeholders and missing props before compiling.")
        sys.exit(2)
    else:
        print(f"[content-check] PASS — {len(beats)} beats checked, no violations.")
        sys.exit(0)


if __name__ == "__main__":
    main()
