#!/usr/bin/env python3
"""bookend_check.py — GATE BOOKEND: assert all four structural bookends are present
in the correct order with correct metadata.

Applies to every reel produced by the ai-explainer family. A reel that passes
Gate V and Gate T but fails Gate BOOKEND is structurally incomplete — same as
a reel missing FACTCHECK.md.

SKILL OVERRIDES. Child skills may legally replace a bookend; the gate must know
which, or it fails correct reels. `cc-explainer` (metadata.skill == "cc-explainer")
may open on a CC kit surface (CCSession / CCWebHome / CCShell / CCPromptBar).
`simple` (metadata.skill == "simple") overrides
two of the four by design:
  - COLD OPEN — HOST LAW replaces the composer with a generated puppet host beat
    (AI-VIDEO). The composer still appears at YOUR TURN, which is still checked.
  - RECAP — CARRY-OUT LAW replaces the verdict artifact with BCRY, one sentence
    built to survive being repeated secondhand. It is the skill's defining move.
The OUTRO rules are NOT overridden for any skill.

EXPLICIT EXEMPTIONS. A beat sheet may declare `metadata.bookend_exempt` as a list
of bookend names to skip. Valid values: "cold-open", "bvdt", "bhtf". The OUTRO
check is never exempt. Use this only for intentional short-format or performance-
open reels where the standard bookend would break the design.

  Example:  "bookend_exempt": ["cold-open", "bvdt", "bhtf"]

Required structure (in order):
  1. Cold-open  — ClaudeComposerAsk (B00 or first beat)
  2. Recap      — ClaudeVerdictArtifact (beat_id BVDT)
  3. Your Turn  — ClaudeComposerAsk with topic containing "YOUR TURN" (beat_id BHTF)
  4. Outro      — ClaudeTitleOutro (beat_id BOUT)

Outro assertions:
  - handle == metadata.channel_title (defaults to @NikBearBrown when not set)
  - subline is absent, null, or empty string — never a baked tagline
  - title matches metadata.title (ignoring terminal punctuation)

Usage:
  python3 scripts/bookend_check.py <reel-folder>
Exit: 0=PASS, 2=one or more FAILs.
"""
import json
import sys
from pathlib import Path

COLD_OPEN_PATTERNS = {'ClaudeComposerAsk', 'ClaudeComposerAsk916', 'ClaudeCodeBeat'}
# cc-explainer (metadata.skill == "cc-explainer") opens ON the Claude Code
# interface — TERMINAL-FIRST LAW: the terminal is the body, not a skin. Its
# legal cold opens are the CC kit's session surfaces. Recap / Your Turn / Outro
# rules are unchanged for it, like every other skill.
CC_COLD_OPEN_PATTERNS = {'CCSession', 'CCWebHome', 'CCShell', 'CCPromptBar'}
RECAP_PATTERNS     = {'ClaudeVerdictArtifact', 'ClaudeVerdictArtifact916'}
OUTRO_PATTERNS     = {'ClaudeTitleOutro', 'ClaudeTitleOutro916'}
DEFAULT_HANDLE     = '@NikBearBrown'


def _strip_punct(s: str) -> str:
    return s.rstrip('.?!…').strip()


def _pattern(beat: dict) -> str:
    shot = beat.get('shot') or {}
    remotion = shot.get('remotion') or {} if isinstance(shot, dict) else {}
    return (remotion.get('pattern') or '') if isinstance(remotion, dict) else ''


def _props(beat: dict) -> dict:
    shot = beat.get('shot') or {}
    remotion = shot.get('remotion') or {} if isinstance(shot, dict) else {}
    return (remotion.get('props') or {}) if isinstance(remotion, dict) else {}


def run(reel_dir: str) -> int:
    reel = Path(reel_dir).resolve()
    bs_path = reel / 'beat_sheet.json'
    if not bs_path.exists():
        print(f'[bookend] no beat_sheet.json at {reel}')
        return 2

    bs     = json.loads(bs_path.read_text())
    meta   = bs.get('metadata') or {}
    beats  = bs.get('beats') or []
    slug   = meta.get('slug', reel.name)

    expected_handle = (meta.get('channel_title') or DEFAULT_HANDLE).strip() or DEFAULT_HANDLE
    expected_title  = (meta.get('title') or '').strip()

    failures = []

    if not beats:
        failures.append('beat_sheet.json has no beats')
        _report(slug, failures)
        return 2

    skill  = (meta.get('skill') or '').strip().lower()
    exempt = set(meta.get('bookend_exempt') or [])

    # ── 1. Cold-open: first beat must be ClaudeComposerAsk
    #      EXCEPT `simple` and `critiq`, whose HOST LAW opens on a generated host beat.
    #      EXCEPT reels with "cold-open" in metadata.bookend_exempt.
    first_pat = _pattern(beats[0])
    if 'cold-open' in exempt:
        pass  # explicitly exempted — any B00 pattern is accepted
    elif skill in ('simple', 'critiq'):
        _shot = beats[0].get('shot') or {}
        _type = (_shot.get('type') or '').upper() if isinstance(_shot, dict) else ''
        if _type not in ('AI-VIDEO', 'T2V', 'I2V', 'GEN-VIDEO') and first_pat not in COLD_OPEN_PATTERNS:
            failures.append(
                f'COLD-OPEN ({skill}): first beat shot.type={_type!r} — HOST LAW expects a '
                f'generated host beat (AI-VIDEO) or ClaudeComposerAsk'
            )
    elif skill == 'cc-explainer':
        if first_pat not in COLD_OPEN_PATTERNS | CC_COLD_OPEN_PATTERNS:
            failures.append(
                f'COLD-OPEN (cc-explainer): first beat pattern={first_pat!r} — expected one of '
                f'{sorted(COLD_OPEN_PATTERNS | CC_COLD_OPEN_PATTERNS)}')
    elif first_pat not in COLD_OPEN_PATTERNS:
        failures.append(
            f'COLD-OPEN: first beat pattern={first_pat!r} — expected one of {sorted(COLD_OPEN_PATTERNS)}'
        )

    # ── 2. Recap (BVDT): ClaudeVerdictArtifact present
    bvdt_idx = next(
        (i for i, b in enumerate(beats)
         if b.get('beat_id') == 'BVDT' or _pattern(b) in RECAP_PATTERNS),
        -1,
    )
    if bvdt_idx < 0 and 'bvdt' in exempt:
        bvdt_idx = 0  # satisfied by exemption — skip the check
    elif bvdt_idx < 0 and skill == 'simple':
        # CARRY-OUT LAW: `simple` lands one compressible sentence (BCRY) instead
        # of a verdict recap. Accept it, and require it — a `simple` reel with
        # neither is genuinely incomplete.
        bvdt_idx = next((i for i, b in enumerate(beats)
                         if b.get('beat_id') == 'BCRY'), -1)
        if bvdt_idx < 0:
            failures.append('CARRY-OUT (BCRY): no carry-out beat found — `simple` reels '
                            'land BCRY where other skills put BVDT')
    elif bvdt_idx < 0:
        failures.append('RECAP (BVDT): no ClaudeVerdictArtifact beat found — add beat_id=BVDT')

    # ── 3. Your Turn (BHTF): ClaudeComposerAsk with YOUR TURN signal
    # Accept beat_id=BHTF OR any ClaudeComposerAsk whose props.topic OR
    # props.segment contains "YOUR TURN" (case-insensitive).
    def _is_your_turn(b: dict) -> bool:
        if b.get('beat_id') == 'BHTF':
            return True
        if _pattern(b) not in COLD_OPEN_PATTERNS:
            return False
        p = _props(b)
        combined = ((p.get('topic') or '') + ' ' + (p.get('segment') or '')).upper()
        return 'YOUR TURN' in combined

    bhtf_idx = next((i for i, b in enumerate(beats) if _is_your_turn(b)), -1)
    if bhtf_idx < 0 and 'bhtf' in exempt:
        bhtf_idx = 0  # satisfied by exemption — skip the check
    elif bhtf_idx < 0:
        failures.append('YOUR TURN (BHTF): no beat with beat_id=BHTF — add the Your Turn beat')
    else:
        yt_pat   = _pattern(beats[bhtf_idx])
        yt_props = _props(beats[bhtf_idx])
        if yt_pat not in COLD_OPEN_PATTERNS:
            failures.append(f'YOUR TURN (BHTF): pattern={yt_pat!r} — expected ClaudeComposerAsk')

    # ── 4. Outro (BOUT): ClaudeTitleOutro present
    bout_idx = next(
        (i for i, b in enumerate(beats)
         if b.get('beat_id') == 'BOUT' or _pattern(b) in OUTRO_PATTERNS),
        -1,
    )
    if bout_idx < 0:
        failures.append('OUTRO (BOUT): no ClaudeTitleOutro beat — add beat_id=BOUT')
    else:
        outro = beats[bout_idx]
        props = _props(outro)

        # handle
        actual_handle = (props.get('handle') or '').strip()
        if not actual_handle:
            failures.append(f'OUTRO handle is empty — must be {expected_handle!r}')
        elif actual_handle != expected_handle:
            failures.append(
                f'OUTRO handle {actual_handle!r} != expected {expected_handle!r} '
                f'(set metadata.channel_title or pass handle explicitly)'
            )

        # subline — must be absent or empty
        actual_subline = (props.get('subline') or '').strip()
        if actual_subline:
            failures.append(
                f'OUTRO subline {actual_subline!r} is not empty — '
                f'subline is opt-in per video; remove it or set to ""'
            )

        # title — must match metadata.title (ignoring terminal punctuation)
        actual_title = (props.get('title') or '').strip()
        if not actual_title or actual_title.startswith('⚠'):
            failures.append(
                f'OUTRO title is missing or is the sentinel placeholder — '
                f'set title={expected_title!r} in the outro beat props'
            )
        elif _strip_punct(actual_title) != _strip_punct(expected_title):
            failures.append(
                f'OUTRO title {actual_title!r} does not match metadata.title {expected_title!r} '
                f'(stripped: {_strip_punct(actual_title)!r} vs {_strip_punct(expected_title)!r})'
            )

    # ── Order check
    if bvdt_idx > -1 and bhtf_idx > -1 and bvdt_idx > bhtf_idx:
        _rn = 'CARRY-OUT (BCRY)' if skill == 'simple' else 'RECAP (BVDT)'
        failures.append(f'ORDER: {_rn} appears after YOUR TURN (BHTF) — order must be RECAP → YOUR TURN → OUTRO')
    if bhtf_idx > -1 and bout_idx > -1 and bhtf_idx > bout_idx:
        failures.append('ORDER: YOUR TURN (BHTF) appears after OUTRO (BOUT) — order must be YOUR TURN → OUTRO last')

    _report(slug, failures)
    return 2 if failures else 0


def _report(slug: str, failures: list) -> None:
    if failures:
        print(f'[bookend] BLOCKED — {len(failures)} failure(s) in {slug}:')
        for f in failures:
            print(f'  ✗ {f}')
    else:
        print(f'[bookend] PASS — four bookends correct for {slug}')


def main() -> None:
    if len(sys.argv) < 2:
        print('usage: bookend_check.py <reel-folder>')
        sys.exit(1)
    sys.exit(run(sys.argv[1]))


if __name__ == '__main__':
    main()
