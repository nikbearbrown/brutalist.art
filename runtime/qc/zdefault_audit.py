#!/usr/bin/env python3
"""
zdefault_audit.py — find Zod .default() fields that are read UNGUARDED at render.

The defect class this exists for (FormBCard.tsx, fixed 2026-08-08):

    // schema
    cueFrame: z.number().int().default(0),
    // body
    const cue = item.cueFrame;          // <-- undefined at render

Zod `.default()` does NOT apply when Remotion renders. `Root.tsx`'s
`schema.parse({})` only feeds Remotion Studio; the render path passes beat-sheet
props straight through. So any field the sheet omits arrives as `undefined`, and
the declared default never runs. In FormBCard that made `frame >= undefined`
false forever and every item panel rendered at opacity 0 — the "near-empty frame"
defect class that GATE V keeps catching downstream.

A read is SAFE when the undefined case is handled at the read site:
    item.cueFrame ?? 0                  -- nullish coalescing
    ({ cueFrame = 0 }) => ...           -- destructuring default

Two severities, because they are genuinely different:

  NESTED  — the field lives inside z.array(z.object({...})). A destructuring
            default on the component's props cannot reach it, so the ONLY fix is
            a guard at the read site. These are the dangerous ones.

  TOP     — a top-level prop. Often harmless (an omitted boolean whose default is
            `false` behaves identically to `undefined`), so these need triage by
            falsy-equivalence rather than blanket patching.

Usage:
    python3 zdefault_audit.py --root runtime/remotion/src/scenes
    python3 zdefault_audit.py --root runtime/remotion/src/scenes --json zdefault-audit.json

Report only. This script never edits a scene file.
"""

import argparse
import glob
import json
import os
import re
import sys
from collections import Counter

FIELD = re.compile(
    r'(?m)^\s*([A-Za-z_$][\w$]*)\s*:\s*(z\.[^\n]*?\.default\(([^\n]*?)\)[^\n]*)$'
)

# Defaults that are falsy — for these, `undefined` and the default behave the
# same in a boolean test, so an unguarded read is usually benign. Reported, but
# ranked below the rest.
FALSY_DEFAULTS = {'false', '0', "''", '""', 'null', '[]'}


def zobject_spans(src):
    """Return (call_start, brace_open, brace_close) for every z.object({...})."""
    spans = []
    for m in re.finditer(r'z\.object\(\s*\{', src):
        i = src.index('{', m.start())
        depth = 0
        for j in range(i, len(src)):
            if src[j] == '{':
                depth += 1
            elif src[j] == '}':
                depth -= 1
                if depth == 0:
                    spans.append((m.start(), i, j))
                    break
    return spans


def audit_file(path):
    src = open(path, encoding='utf-8', errors='replace').read()
    spans = zobject_spans(src)
    if not spans:
        return []

    # Blank out schema regions so "is it read?" only looks at the component body.
    body = src
    for _s, a, b in spans:
        body = body[:a] + (' ' * (b - a)) + body[b:]

    out = []
    for s, a, b in spans:
        head = src[max(0, s - 30):s]
        nested = bool(re.search(r'z\.array\(\s*$', head))
        for m in FIELD.finditer(src[a:b]):
            name, default = m.group(1), m.group(3).strip()
            if not re.search(r'\b' + re.escape(name) + r'\b', body):
                continue  # declared but never read — not a render defect
            # A read is guarded if EVERY line that references the field also
            # carries a `??`. This catches both `x.field ?? d` and the indexed
            # form `MAP[x.field] ?? d`, where the `??` does not sit directly
            # against the identifier.
            ref_lines = [ln for ln in body.split('\n')
                         if re.search(r'\b' + re.escape(name) + r'\b', ln)]
            guarded = bool(ref_lines) and all('??' in ln for ln in ref_lines)
            destructured = bool(re.search(r'[{,]\s*' + re.escape(name) + r'\s*=', body))
            if guarded or destructured:
                continue
            out.append({
                'file': os.path.basename(path),
                'path': path,
                'field': name,
                'default': default,
                'nested': nested,
                'falsy_default': default in FALSY_DEFAULTS,
            })
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default='runtime/remotion/src/scenes',
                    help='directory of .tsx scene files')
    ap.add_argument('--json', default='', help='write full findings here')
    ap.add_argument('--strict', action='store_true',
                    help='exit 2 if any NESTED non-falsy finding survives')
    a = ap.parse_args()

    files = sorted(glob.glob(os.path.join(a.root, '*.tsx')))
    if not files:
        print(f'no .tsx files under {a.root}', file=sys.stderr)
        return 1

    rows = []
    for f in files:
        rows.extend(audit_file(f))

    nested = [r for r in rows if r['nested']]
    top = [r for r in rows if not r['nested']]
    nested_real = [r for r in nested if not r['falsy_default']]

    print(f'scene files scanned         : {len(files)}')
    print(f'unguarded .default() reads   : {len(rows)} across '
          f'{len({r["file"] for r in rows})} files')
    print(f'  NESTED (array item)        : {len(nested)}  '
          f'-- of these {len(nested_real)} have a NON-falsy default')
    print(f'  top-level                  : {len(top)}')

    if nested_real:
        print('\n=== NESTED, non-falsy default — renders WRONG when the sheet omits the field ===')
        for r in nested_real:
            print(f'  {r["file"]:34s} {r["field"]:18s} default={r["default"]}')

    benign = [r for r in nested if r['falsy_default']]
    if benign:
        print('\n=== NESTED, falsy default — undefined behaves like the default; low priority ===')
        for r in benign:
            print(f'  {r["file"]:34s} {r["field"]:18s} default={r["default"]}')

    if top:
        print('\n=== top-level, by file (triage by falsy-equivalence) ===')
        for f, n in Counter(r['file'] for r in top).most_common(15):
            print(f'  {f:40s} {n}')

    if a.json:
        json.dump(rows, open(a.json, 'w'), indent=1)
        print(f'\nwrote {a.json}')

    if a.strict and nested_real:
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
