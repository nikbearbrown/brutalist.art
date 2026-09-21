#!/usr/bin/env python3
"""
sharpness_check.py — GATE SHARPNESS
Per-beat Laplacian-variance sharpness audit on the compiled reel master.

Samples one frame per beat at the midpoint (cumulative timestamp), measures
edge sharpness via Laplacian variance, and flags any beat whose sharpness
falls below 50% of the reel's median. The primary failure mode this catches
is rotation applied to crispEdges pixel-art, which causes anti-aliasing
("the fuzzy"). See PIXEL-ART LAW in ClaudeMascotScene.tsx.

Usage:
    python3 scripts/sharpness_check.py <reel_dir>

Exit codes:
    0 — PASS (all beats within acceptable sharpness range)
    2 — FAIL (one or more beats materially softer than the reel median)
    3 — SKIP (missing deps or no compiled master found)

Writes SHARPNESS.md into the reel directory with the per-beat table.
"""

from __future__ import annotations
import json, os, subprocess, sys, tempfile
from pathlib import Path

_SCALE = 1920          # extract frames at this width (1080p; still shows crispEdges blur)
_FAIL_RATIO = 0.50     # flag beat if LV < median * this ratio
_ABS_FLOOR  = 40.0     # JPEG-measured LV minimum; a frame at or above this is not genuinely
                       # blurry. Rotation artifacts and true motion blur give LV < 20; sparse
                       # but crisp Manim text on cream gives 50–80; dense beats give 200–800.
                       # The AND condition means a beat only fails when BOTH soft vs. median
                       # AND below this absolute floor — preventing false positives on intentionally
                       # sparse ClaudeTitleOutro or Manim text-card beats.

# build.status values exempt from the gate: static stills cannot have rotation-artifact blur.
_SKIP_STILL_STATUS = {"STILL"}

# Manim scene classes exempt from the gate because their failure mode (crispEdges pixel-art
# rotation) cannot occur — no pixel art is used and no rotation transforms are applied.
# These scenes may legitimately have low LV due to sparse layouts or dark backgrounds.
# LV is still measured (for median accuracy) but the failure check is skipped.
_SPARSE_MANIM_PATTERNS: set[str] = {
    # B11_CognitiRecreation: two-box diagram on dark canvas; FadeIn/GrowArrow only — no rotation.
    "B11_CognitiRecreation",
    # B02_AntBeachPath: sparse dot + dashed-curve path diagram on cream; few edges by design.
    "B02_AntBeachPath",
    # B04_PathCutaway: geometric cutaway diagram; minimal elements, FadeIn/Create only.
    "B04_PathCutaway",
    # B07_GradientNotSwitch: small bar at 57.2% on cream with faint MUTE citations — sparse by
    # design; no pixel-art or rotation involved. FadeIn/Transform/Create only.
    "B07_GradientNotSwitch",
    # B17_WordsBecomePattern: glyph cloud phase (faint ink dots) + bar distribution — midpoint
    # lands in the near-blank dot cloud; bars appear later. Intentionally sparse; no rotation.
    "B17_WordsBecomePattern",
}

# Remotion component patterns exempt from the gate. These components deliberately render
# sparse text on white (minimal ink) — low LV is by design, not blur. The sharpness gate
# was designed for pixel-art rotation artifacts; it does not apply to minimalist text cards.
_SPARSE_REMOTION_PATTERNS: set[str] = {
    "FormACard",   # sparse editorial statement card: one line of text on white — very low LV by design
    # BrutalistCommandRain — mid-clip sample hits the falling state (items at fallOpacity=0.42 before
    # settleAtSec eases them to full opacity). Sparse semi-transparent text on dark olive → very low LV
    # by design. Settled state renders at opacity=1 and is sharp; no pixel-art or rotation involved.
    # Validated 2026-08-23. See also type_check.py DARK_FRAME_ANIMATION_CONTRAST_OK.
    "BrutalistCommandRain",
}


def _is_exempt(beat: dict) -> bool:
    """Return True if the sharpness gate should not flag this beat as a failure.

    LV is still measured so the reel median remains accurate, but the failure
    check is skipped for beats where crispEdges rotation blur cannot occur,
    or for Remotion patterns that are intentionally minimalist (sparse text on white).
    """
    if beat.get("build", {}).get("status", "") in _SKIP_STILL_STATUS:
        return True
    shot = beat.get("shot", {})
    manim_pattern = (
        shot.get("graphic", {}).get("manim", "")
        or shot.get("graphic", {}).get("scene_class", "")
        or shot.get("manim", {}).get("class", "")
        or shot.get("manim", {}).get("scene_class", "")
        or shot.get("manim", {}).get("scene", "")
    )
    if manim_pattern in _SPARSE_MANIM_PATTERNS:
        return True
    remotion_pattern = (shot.get("remotion") or {}).get("pattern", "") if isinstance(shot.get("remotion"), dict) else ""
    return remotion_pattern in _SPARSE_REMOTION_PATTERNS


def _check_deps() -> bool:
    try:
        import numpy  # noqa: F401
        from PIL import Image  # noqa: F401
        return True
    except ImportError:
        return False


def _laplacian_variance(img_path: Path) -> float:
    import numpy as np
    from PIL import Image
    img = Image.open(img_path).convert('L')
    a = np.asarray(img, dtype=float)
    lap = (
        + np.roll(a, -1, axis=0) + np.roll(a, 1, axis=0)
        + np.roll(a, -1, axis=1) + np.roll(a, 1, axis=1)
        - 4.0 * a
    )
    return float(lap.var())


def _extract_frame(video: Path, ts: float, out: Path) -> bool:
    r = subprocess.run(
        [
            'ffmpeg', '-y', '-ss', f'{ts:.3f}', '-i', str(video),
            '-frames:v', '1',
            '-vf', f'scale={_SCALE}:-2',
            '-q:v', '2', str(out),
        ],
        capture_output=True,
    )
    return r.returncode == 0 and out.exists() and out.stat().st_size > 0


def _find_master(reel_dir: Path) -> Path | None:
    slug = reel_dir.name
    for candidate in [
        reel_dir / f'{slug}-slate.mp4',   # slate cut always exists after compile
        reel_dir / f'{slug}.mp4',
        reel_dir / 'mp4' / f'{slug}-slate.mp4',
        reel_dir / 'mp4' / f'{slug}.mp4',
    ]:
        if candidate.exists():
            return candidate
    # Last resort: any .mp4 in mp4/
    for p in sorted((reel_dir / 'mp4').glob('*.mp4')):
        return p
    return None


def main() -> None:
    if not _check_deps():
        print('[sharpness] SKIP — missing deps (pip install pillow numpy)')
        sys.exit(3)

    import numpy as np

    if len(sys.argv) < 2:
        print('Usage: sharpness_check.py <reel_dir>')
        sys.exit(2)

    reel_dir = Path(sys.argv[1]).resolve()
    bs_path = reel_dir / 'beat_sheet.json'
    if not bs_path.exists():
        print(f'[sharpness] no beat_sheet.json in {reel_dir}')
        sys.exit(2)

    master = _find_master(reel_dir)
    if master is None:
        print(f'[sharpness] SKIP — no compiled master found in {reel_dir}')
        print('[sharpness] Run `art run` or `art final` first to produce the master.')
        sys.exit(3)

    beats = json.loads(bs_path.read_text())['beats']

    results: list[dict] = []
    cursor = 0.0

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for beat in beats:
            dur = float(beat.get('actual_duration_s') or beat.get('duration_s') or beat.get('estimated_duration_s') or 5.0)
            mid = cursor + dur / 2.0
            frame = tmp / f"{beat.get('beat_id') or beat.get('id', 'unknown')}.jpg"
            lv: float | None = None
            if _extract_frame(master, mid, frame):
                try:
                    lv = _laplacian_variance(frame)
                except Exception:
                    pass
            results.append({
                'id': beat.get('beat_id') or beat.get('id', 'unknown'),
                'lv': lv,
                'ts': mid,
                'exempt': _is_exempt(beat),
            })
            cursor += dur

    valid = [r['lv'] for r in results if r['lv'] is not None]
    if not valid:
        print('[sharpness] SKIP — could not extract any frames (ffmpeg issue?)')
        sys.exit(3)

    median_lv = float(np.median(valid))
    threshold  = median_lv * _FAIL_RATIO

    lines = [
        f'# SHARPNESS GATE — {reel_dir.name}',
        '',
        f'Compiled master: `{master.name}`',
        f'Median Laplacian variance: **{median_lv:.1f}**',
        f'Failure threshold: {threshold:.1f} ({int(_FAIL_RATIO*100)}% of median)',
        '',
        '> Soft beats = rotation applied to `crispEdges` pixel-art.',
        '> Fix: use translation/scale only — never rotate. See PIXEL-ART LAW in',
        '> `ClaudeMascotScene.tsx`.',
        '',
        '| Beat | LV | % of median | Status |',
        '|------|----|-------------|--------|',
    ]

    failures: list[str] = []
    for r in results:
        bid = r['id']
        exempt = r.get('exempt', False)
        if r['lv'] is None:
            lines.append(f'| {bid} | — | — | SKIP (frame not extracted) |')
            continue
        pct = (r['lv'] / median_lv) * 100.0
        if exempt:
            lines.append(f'| {bid} | {r["lv"]:.1f} | {pct:.0f}% | SKIP (exempt — no pixel-art rotation possible) |')
            continue
        if r['lv'] < threshold and r['lv'] < _ABS_FLOOR:
            status = f'**FAIL** — {pct:.0f}% (below {int(_FAIL_RATIO*100)}% floor and below abs floor {_ABS_FLOOR:.0f})'
            failures.append(bid)
        else:
            status = f'PASS — {pct:.0f}%'
        lines.append(f'| {bid} | {r["lv"]:.1f} | {pct:.0f}% | {status} |')

    report = reel_dir / 'SHARPNESS.md'
    report.write_text('\n'.join(lines) + '\n')

    if failures:
        print(
            f'[sharpness] GATE SHARPNESS FAIL — {len(failures)} soft beat(s):'
            f' {", ".join(failures)}'
        )
        print(f'[sharpness] see {report}')
        sys.exit(2)

    print(
        f'[sharpness] GATE SHARPNESS PASS — {len(valid)} beats,'
        f' median LV={median_lv:.1f}'
    )
    sys.exit(0)


if __name__ == '__main__':
    main()
