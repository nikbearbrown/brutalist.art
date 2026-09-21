#!/usr/bin/env python3
"""
frame_check.py — GATE FRAME: analytical layout and WCAG contrast check.

Derives expected text positions from beat-sheet prop values and known
component layout constants. No rendering required — violations are caught
from the JSON before expensive compilation begins.

Failures (always block — no --lenient):
  COLLISION  — two text layers share a y range (kicker bleeds into title)
  EDGE-BLEED — computed text box reaches a canvas or card edge
  CONTRAST   — text/bg combination fails WCAG AA (4.5:1 normal, 3.0:1 large)

Exit: 2 if any failure, 0 if clean.

Usage:
  python3 frame_check.py <reel_dir>
  python3 frame_check.py <reel_dir> --height 2160
"""
import argparse, json, sys
from pathlib import Path

# ── Canvas defaults (4K — compile.py 4K LAW) ─────────────────────────────────
DEFAULT_H = 2160

# ── CLAUDE palette (mirrors runtime/remotion/src/tokens/claude.ts) ────────────
CLAUDE_PAGE     = (243, 235, 221)   # #F3EBDD cream
CLAUDE_INK      = (47,  42,  38)    # #2F2A26 dark ink
CLAUDE_INK_SOFT = (110, 102, 92)    # approximate INK at 0.75 opacity on PAGE
CLAUDE_CARD     = (255, 253, 249)   # near-white card background

# ── ClaudeComposerAsk layout constants (mirrors ClaudeComposerAsk.tsx v2) ─────
# The component now uses a MEASURED VERTICAL STACK — no two layers share a y.
# These constants must stay in sync with the component source.
CCA_PAD_X_FRAC  = 0.08    # PAD_X = width * 0.08
CCA_KICKER_FONT = 0.034   # topic/kicker font-size = height * 0.034
CCA_KICKER_TOP  = 0.08    # KICKER_TOP = height * 0.08
CCA_KICKER_GAP  = 0.02    # gap between kicker bottom and segment top = height * 0.02
CCA_SEG_FONT    = 0.038   # segment font-size = height * 0.038
CCA_SEG_GAP     = 0.02    # gap between segment bottom and greeting top = height * 0.02
CCA_SEG_ROW     = 0.06    # segment row height (approx) = height * 0.06
CCA_GREETING_GAP = 0.02   # gap between greeting and card = height * 0.02
CCA_GREETING_ROW = 0.09   # greeting row height (approx) = height * 0.09
CCA_LINE_H      = 1.60    # EB Garamond approximate line-height multiplier
CCA_KICKER_MAX  = 60      # Zod-enforced kicker character limit (1-line guarantee)

# Average char width as fraction of font-size for EB Garamond (narrow-width serif)
# Calibrated empirically for the weight/size used in the eyebrow.
GARAMOND_CW = 0.55

# Rough card + footer height as fraction of canvas height (empirical).
# The composer card, footer strip, running indicator, and output lines together
# occupy approximately 38% of canvas height at typical aspect ratios.
CCA_CARD_H_FRAC = 0.38

# WCAG AA minimums
WCAG_AA_NORMAL = 4.5
WCAG_AA_LARGE  = 3.0       # ≥18pt/24px bold or ≥14pt/18.67px bold


def _lum(c: tuple) -> float:
    def lin(x: float) -> float:
        x /= 255.0
        return x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4
    return 0.2126 * lin(c[0]) + 0.7152 * lin(c[1]) + 0.0722 * lin(c[2])


def contrast(fg: tuple, bg: tuple) -> float:
    l1, l2 = _lum(fg), _lum(bg)
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


# ── Per-component analytical checks ──────────────────────────────────────────

def check_claude_composer_ask(bid: str, props: dict, w: int, h: int) -> list:
    """Analytical layout and contrast checks for ClaudeComposerAsk beats.

    The component uses a MEASURED VERTICAL STACK — kicker/title collision is
    impossible by construction.  What we check instead:

      KICKER-OVERFLOW — topic string longer than Zod max (CCA_KICKER_MAX chars)
      CANVAS-OVERFLOW — measured stack bottom exceeds the canvas
      EDGE-BLEED      — PAD_X < 16 px
      CONTRAST        — WCAG AA for kicker (INK_SOFT on PAGE) and segment (INK on PAGE)
    """
    failures = []
    topic = str(props.get("topic") or "")

    pad_x  = w * CCA_PAD_X_FRAC
    avail_w = w - 2 * pad_x

    # ── Kicker geometry (mirrors ClaudeComposerAsk.tsx measured-stack) ───────
    kicker_font   = h * CCA_KICKER_FONT
    chars_line    = max(1, int(avail_w / (kicker_font * GARAMOND_CW)))
    kicker_lines  = max(1, -(-len(topic) // chars_line))       # ceiling div
    kicker_top    = h * CCA_KICKER_TOP
    kicker_bottom = kicker_top + kicker_lines * kicker_font * CCA_LINE_H

    seg_top      = kicker_bottom + h * CCA_KICKER_GAP
    seg_bottom   = seg_top + h * CCA_SEG_ROW

    greeting_top    = seg_bottom + h * CCA_SEG_GAP
    greeting_bottom = greeting_top + h * CCA_GREETING_ROW

    card_top    = greeting_bottom + h * CCA_GREETING_GAP
    card_bottom = card_top + h * CCA_CARD_H_FRAC

    # ── KICKER-OVERFLOW: topic exceeds 1-line guarantee ──────────────────────
    if len(topic) > CCA_KICKER_MAX:
        failures.append((
            "COLLISION", "kicker-overflow",
            f"topic is {len(topic)} chars — exceeds Zod max {CCA_KICKER_MAX}. "
            f"At {h}p this wraps to ~{kicker_lines} line(s), "
            f"kicker_bottom={kicker_bottom:.0f}px, seg_top={seg_top:.0f}px. "
            f"Shorten topic to ≤{CCA_KICKER_MAX} chars."
        ))

    # ── CANVAS-OVERFLOW: stack taller than canvas ─────────────────────────────
    if card_bottom > h:
        overflow = card_bottom - h
        failures.append((
            "EDGE-BLEED", "canvas-overflow",
            f"measured stack bottom={card_bottom:.0f}px exceeds canvas height {h}px "
            f"by {overflow:.0f}px — reduce kicker length or card content."
        ))

    # ── CONTRAST: kicker eyebrow (INK_SOFT on PAGE) ──────────────────────────
    c_kicker = contrast(CLAUDE_INK_SOFT, CLAUDE_PAGE)
    if c_kicker < WCAG_AA_NORMAL:
        failures.append((
            "CONTRAST", "kicker-wcag-fail",
            f"kicker eyebrow: INK_SOFT on PAGE → {c_kicker:.2f}:1 < WCAG AA {WCAG_AA_NORMAL}:1"
        ))

    # ── CONTRAST: segment title (INK on PAGE) ────────────────────────────────
    c_seg = contrast(CLAUDE_INK, CLAUDE_PAGE)
    if c_seg < WCAG_AA_NORMAL:
        failures.append((
            "CONTRAST", "segment-wcag-fail",
            f"segment title: INK on PAGE → {c_seg:.2f}:1 < WCAG AA {WCAG_AA_NORMAL}:1"
        ))

    # ── EDGE-BLEED: PAD_X too narrow ─────────────────────────────────────────
    if pad_x < 16:
        failures.append((
            "EDGE-BLEED", "topic-left-edge",
            f"PAD_X={pad_x:.0f}px — kicker reaches the canvas left edge"
        ))

    return failures


# Registry: pattern name → check function
_COMPONENT_CHECKS = {
    "ClaudeComposerAsk": check_claude_composer_ask,
    # Add more component checks here as the component set grows.
}


def check_beat(bid: str, pattern: str, props: dict, w: int, h: int) -> list:
    fn = _COMPONENT_CHECKS.get(pattern)
    return fn(bid, props, w, h) if fn else []


def main():
    ap = argparse.ArgumentParser(description="Analytical layout + contrast gate (GATE FRAME)")
    ap.add_argument("reel", type=Path)
    ap.add_argument("--height", type=int, default=DEFAULT_H)
    ap.add_argument("--sheet", default="beat_sheet.json")
    a = ap.parse_args()

    sheet_path = a.reel / a.sheet
    if not sheet_path.exists():
        sys.exit(f"[frame-check] ERROR: no {a.sheet} at {sheet_path}")

    sheet = json.loads(sheet_path.read_text())
    beats = sheet.get("beats") or []
    meta  = sheet.get("metadata") or {}

    # Derive width from aspect ratio
    ar = meta.get("aspect_ratio", "16:9")
    try:
        num, den = (int(x) for x in ar.split(":"))
    except ValueError:
        num, den = 16, 9
    h = a.height
    w = int(round(h * num / den / 2) * 2)

    slug = meta.get("slug", a.reel.name)
    print(f"[frame-check] {slug}  canvas={w}×{h}  beats={len(beats)}")

    all_failures = []
    for b in beats:
        bid  = b.get("beat_id") or b.get("id") or "?"
        shot = b.get("shot") or {}
        rem  = shot.get("remotion") or b.get("remotion") or {}
        pat  = str(rem.get("pattern") or "")
        props = rem.get("props") or {}

        for sev, kind, msg in check_beat(bid, pat, props, w, h):
            all_failures.append((bid, sev, kind, msg))
            print(f"[frame-check] FAIL {bid}: [{sev}] {kind} — {msg}")

    if all_failures:
        print(f"\n[frame-check] FAILED — {len(all_failures)} layout/contrast violation(s). "
              f"Fix props or layout before compiling.")
        sys.exit(2)
    else:
        print(f"[frame-check] PASS — {len(beats)} beats checked, no violations.")
        sys.exit(0)


if __name__ == "__main__":
    main()
