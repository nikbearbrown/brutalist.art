#!/usr/bin/env python3
"""
content_default_check.py — GATE TIER-0

Rule: every content-prop in a Remotion scene schema must default to the sentinel
'⚠ SET IN BEAT SHEET'. A plausible default is a silent bug waiting to ship.

Ref: REMOTION-STANDARDS §6

Usage:
  python3 content_default_check.py <file.tsx> [file.tsx ...]   # check specific files
  python3 content_default_check.py --all                        # check all scenes/

Exit 0: clean. Exit 2: violation found.
"""
import re, sys
from pathlib import Path

SENTINEL = '⚠ SET IN BEAT SHEET'

CONTENT_PROPS = frozenset({
    'sparkLine', 'title', 'subtitle', 'segment', 'kicker', 'heading',
    'question', 'call', 'body', 'caption', 'label', 'narration', 'verdict',
    'prompt', 'command', 'greeting', 'output', 'runningText',
    'artifactTitle', 'artifactHeading', 'artifactLines',
})

# Matches: propName: z.anything()...default('value') or .default(['value'])
_PROP_PAT = '|'.join(re.escape(p) for p in sorted(CONTENT_PROPS))
SCHEMA_DEFAULT_RE = re.compile(
    r'\b(' + _PROP_PAT + r')\s*:[^\n;{]*?\.default\(\s*'
    r'([\'"][^\'"]*[\'"]|\[[^\]]*\])',
)

def _is_sentinel(raw: str) -> bool:
    v = raw.strip().strip("'\"")
    return SENTINEL in raw or v == SENTINEL

def _is_demo_twin(path: Path) -> bool:
    return path.stem.endswith('Demo') or 'Demo' in path.stem

def check_file(path: Path) -> list[tuple[str, str]]:
    """Return (prop, default_snippet) pairs that violate the sentinel rule."""
    if _is_demo_twin(path):
        return []
    text = path.read_text()
    failures = []
    for m in SCHEMA_DEFAULT_RE.finditer(text):
        prop = m.group(1)
        raw  = m.group(2)
        stripped = raw.strip().strip("'\"").strip()
        if stripped and not _is_sentinel(raw):
            failures.append((prop, raw.strip()[:100]))
    return failures

def main() -> None:
    args = sys.argv[1:]
    if not args:
        sys.exit(f'usage: {sys.argv[0]} <file.tsx> [...] | --all')

    if '--all' in args:
        here = Path(__file__).parent
        scenes_dir = here.parent / 'remotion' / 'src' / 'scenes'
        paths = sorted(scenes_dir.glob('*.tsx'))
    else:
        paths = [Path(a) for a in args if a.endswith('.tsx')]

    violations: list[tuple[str, str, str]] = []
    for path in paths:
        if not path.exists():
            print(f'[content-default] SKIP: {path.name} not found', file=sys.stderr)
            continue
        for prop, raw in check_file(path):
            violations.append((path.name, prop, raw))

    for fname, prop, raw in violations:
        print(
            f'[content-default] FAIL {fname}: '
            f'prop={prop!r} default={raw!r} — '
            f"must be sentinel '⚠ SET IN BEAT SHEET'",
            file=sys.stderr,
        )

    if violations:
        sys.exit(2)
    print(f'[content-default] PASS — {len(paths)} file(s) clean', file=sys.stderr)
    sys.exit(0)

if __name__ == '__main__':
    main()
