#!/usr/bin/env python3
"""
lane_check.py — GATE LANE: pipeline-owned and gen-AI/pantry slate detection.

Two failure classes:

  PIPELINE-SLATE-IN-CUT  — a beat whose shot.remotion.pattern or graphic.engine
                           declares a pipeline renderer (remotion or manim) resolves
                           to a SLATE. The pipeline owns this beat; a human cannot
                           supply it. This gate fires regardless of --allow-slates.

  GEN-AI-SLATE-IN-MASTER — a gen-AI/pantry beat (shot.source ∈ {ai, genai, gen},
                           shot.type ∈ {STILL, AI-VIDEO, T2V, I2V, GEN-VIDEO}, or
                           shot.lane == "vox") appears as a SLATE in a MASTER cut.
                           --allow-slates bypasses THE MASTER LAW in compile.py;
                           this gate cannot be bypassed by any flag.

The first class is a complete build error. The second class means a master was
shipped with human-owned gaps that were manually permitted — a deliberate process
failure that this gate closes.

Exit: 2 if any failure, 0 if clean.

Usage:
  python3 lane_check.py <reel_dir>
  python3 lane_check.py <reel_dir> --sheet beat_sheet.json
"""
import argparse, json, sys
from pathlib import Path

# ── Shot sources that indicate gen-AI / pantry content ───────────────────────
GEN_AI_SOURCES = {"ai", "genai", "gen", "t2v", "i2v"}

# ── Shot types that require a human-provided pantry clip ─────────────────────
GEN_AI_TYPES = {"STILL", "AI-VIDEO", "T2V", "I2V", "GEN-VIDEO"}

# ── Lane labels that imply gen-AI / pantry ───────────────────────────────────
GEN_AI_LANES = {"vox", "pantry"}


def is_pipeline_beat(b: dict) -> bool:
    """True if the pipeline (remotion or manim) owns this beat."""
    shot  = b.get("shot") or {}
    rem   = shot.get("remotion") or b.get("remotion") or {}
    if rem.get("pattern"):
        return True
    graphic = b.get("graphic") or {}
    if graphic.get("engine") in ("manim", "remotion"):
        return True
    shot_type = str(shot.get("type") or "").upper()
    if shot_type == "GRAPHIC":
        return True
    if shot_type == "REMOTION":
        return True
    return False


def is_gen_ai_beat(b: dict) -> bool:
    """True if this beat requires a human-supplied gen-AI / pantry clip."""
    shot  = b.get("shot") or {}
    src   = str(shot.get("source") or "").lower()
    stype = str(shot.get("type")   or "").upper()
    lane  = str(shot.get("lane")   or "").lower()
    if src in GEN_AI_SOURCES:
        return True
    if stype in GEN_AI_TYPES:
        return True
    if lane in GEN_AI_LANES:
        return True
    return False


def get_build_slates(sheet: dict) -> set:
    """Return the set of beat IDs marked SLATE in the most recent build stamp."""
    build = (sheet.get("metadata") or {}).get("build") or {}
    return set(build.get("slates") or [])


def get_build_cut(sheet: dict) -> str:
    """Return 'master' | 'review' | 'unknown' from the build stamp."""
    build = (sheet.get("metadata") or {}).get("build") or {}
    return str(build.get("cut") or "unknown").lower()


def main():
    ap = argparse.ArgumentParser(description="Pipeline-owned and gen-AI slate gate")
    ap.add_argument("reel", type=Path)
    ap.add_argument("--sheet", default="beat_sheet.json")
    a = ap.parse_args()

    sheet_path = a.reel / a.sheet
    if not sheet_path.exists():
        sys.exit(f"[lane-check] ERROR: no {a.sheet} at {sheet_path}")

    sheet = json.loads(sheet_path.read_text())
    beats = sheet.get("beats") or []
    slug  = (sheet.get("metadata") or {}).get("slug", a.reel.name)
    cut   = get_build_cut(sheet)
    slates = get_build_slates(sheet)

    # Also check per-beat build status for cases where the stamp is absent
    beat_statuses = {}
    for b in beats:
        bid = b.get("beat_id") or b.get("id") or "?"
        bld = b.get("build") or {}
        beat_statuses[bid] = str(bld.get("status") or "").upper()

    def is_slate(bid: str) -> bool:
        return bid in slates or beat_statuses.get(bid) == "SLATE"

    print(f"[lane-check] {slug}  cut={cut}  known_slates={sorted(slates)}")

    all_failures = []
    for b in beats:
        bid = b.get("beat_id") or b.get("id") or "?"
        if not is_slate(bid):
            continue

        # PIPELINE-SLATE: remotion or manim beat that is still a slate
        if is_pipeline_beat(b):
            all_failures.append((bid, "PIPELINE-SLATE-IN-CUT",
                f"pipeline-owned beat (remotion/manim) is SLATE — "
                f"run remotion_scenes.py or manim to fill it, then recompile"))
            print(f"[lane-check] FAIL {bid}: [PIPELINE-SLATE-IN-CUT] pipeline-owned beat is SLATE")

        # GEN-AI-SLATE-IN-MASTER: gen-AI/pantry slate allowed through by --allow-slates
        elif is_gen_ai_beat(b) and cut == "master":
            shot = b.get("shot") or {}
            src  = shot.get("source", "?")
            lane = shot.get("lane",   "?")
            stype= shot.get("type",   "?")
            all_failures.append((bid, "GEN-AI-SLATE-IN-MASTER",
                f"gen-AI/pantry beat (source={src}, type={stype}, lane={lane}) is SLATE "
                f"in master cut — --allow-slates cannot override this gate; "
                f"provide the clip before mastering"))
            print(f"[lane-check] FAIL {bid}: [GEN-AI-SLATE-IN-MASTER] "
                  f"gen-AI pantry beat (source={src}, lane={lane}) is SLATE in master cut")

    if all_failures:
        n_pipeline = sum(1 for _, k, _ in all_failures if k == "PIPELINE-SLATE-IN-CUT")
        n_gen_ai   = sum(1 for _, k, _ in all_failures if k == "GEN-AI-SLATE-IN-MASTER")
        print(f"\n[lane-check] FAILED — {len(all_failures)} lane violation(s): "
              f"{n_pipeline} pipeline-slate, {n_gen_ai} gen-AI-in-master.")
        sys.exit(2)
    else:
        print(f"[lane-check] PASS — {len(beats)} beats checked, no lane violations.")
        sys.exit(0)


if __name__ == "__main__":
    main()
