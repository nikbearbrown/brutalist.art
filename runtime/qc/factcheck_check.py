#!/usr/bin/env python3
"""
factcheck_check.py — GATE F, the content half.

Gate F in run.sh tests that FACTCHECK.md, SHOTLIST.md and PROMPTS.md EXIST. It
never opens them. A file containing one character passes; so does a file whose
every verdict reads UNVERIFIED. This module reads the one that carries claims
and checks that it holds up, against the format the reels already use:

    | # | Beat | Claim (as spoken / shown) | Verdict | Source / derivation | Fix |

See FACTCHECK-SPEC.md at the repo root for the authoring protocol. This script
enforces only what a machine can establish; the verification itself is human
(or agent) work and always was.

RULES
  FC-1  BLOCKER   A claims table exists, with a Beat column, a Verdict column,
                  and at least one row.
  FC-2  BLOCKER   No row has an empty Verdict or an empty Source cell. A blank
                  verdict is an unfinished check wearing a finished coat.
  FC-3  BLOCKER   No verdict is unresolved or failing (UNVERIFIED, FAIL, TODO,
                  TBD, PENDING, ?, x). Resolve it or reword the narration.
  FC-4  ADVISORY  Every beat whose narration carries a checkable claim — a
                  figure, a date, a quantity — is named in at least one row.
                  Advisory by default because claim detection is a heuristic
                  and a gate that cries wolf gets switched off. Promote it with
                  --strict-coverage once a channel's sheets are clean.
  FC-5  ADVISORY  A Status line exists, so the sign-off has a date and a name.
  FC-6  ADVISORY  Every verdict is one of PASS / CORRECTED / EXEMPT. A freeform
                  verdict the gate cannot classify is one a reader six months
                  from now cannot classify either — but blocking on it would
                  invite routing around the gate, so it is advisory.

Exit 2 on any BLOCKER, 1 on advisories only, 0 clean.
Usage: factcheck_check.py <reel_dir> [--quiet] [--strict-coverage]
"""
import json, os, re, sys, argparse

# Word-boundary matching, not substring. "EXEMPT" contains "x"; "corrected"
# contains "correct" — a substring test on short tokens fails a passing row and a
# gate that fails passing rows gets switched off within the week.
FAIL_RE = re.compile(r"\b(unverified|unverifiable|fail|failed|failing|todo|tbd|"
                     r"pending|unknown|unresolved|open|no)\b", re.I)
FAIL_EXACT = {"?", "x", "-", "—", "–", "n/a", "na", ""}
OK_RE = re.compile(r"\b(pass|passed|confirmed|corrected|verified|exempt|ok)\b|[✓✅]", re.I)

# A beat carries a checkable claim if its narration contains a digit, or a
# number word followed closely by a magnitude/unit word. Deliberately narrow:
# "one engineering insight" must NOT trip this, or the gate flags everything
# and gets ignored. Both lists are editable — that is the intended tuning knob.
NUM_WORDS = ("one two three four five six seven eight nine ten eleven twelve "
             "thirteen fourteen fifteen sixteen seventeen eighteen nineteen "
             "twenty thirty forty fifty sixty seventy eighty ninety").split()
MAGNITUDES = ("hundred thousand million billion trillion percent times fold "
              "century centuries decade decades year years month months day days "
              "hour hours minute minutes second seconds "
              "bytes kilobytes megabytes gigabytes terabytes petabytes "
              "dollars cents pounds euros").split()

_NUM = r"(?:%s)" % "|".join(NUM_WORDS)
_MAG = r"(?:%s)" % "|".join(MAGNITUDES)
CLAIM_RE = re.compile(
    r"\d"                                  # any digit at all
    r"|\b%s[-\s]+(?:\w+[-\s]+){0,1}%s\b" % (_NUM, _MAG),   # "sixty-four million"
    re.I)

# Match any beat ID the schema allows: B followed by digits/uppercase letters.
# B\d{1,3} missed named beats like BHTF, BVDT, BOUT, B02B.
BEAT_RE = re.compile(r"B[0-9A-Z]+")
RANGE_RE = re.compile(r"B(\d{1,3})\s*[–—-]\s*B?(\d{1,3})")

# A cell may contain an escaped pipe — `P(Y\|X)` is legal markdown and appears in
# real claims tables. Splitting on every `|` shreds that row and reports a verdict
# of "X) = conditional/observational". Split on unescaped pipes only.
CELL_SPLIT = re.compile(r"(?<!\\)\|")


def split_row(line):
    parts = CELL_SPLIT.split(line.strip().strip("|"))
    return [p.replace("\\|", "|").strip() for p in parts]


def read_rows(md):
    """Pull the first markdown table that has both a Beat and a Verdict column.
    Returns (header, rows) with rows as lists of stripped cells."""
    lines = md.splitlines()
    for i, ln in enumerate(lines):
        if ln.count("|") < 3:
            continue
        cells = [c.lower() for c in split_row(ln)]
        if not any(c.startswith("beat") for c in cells):
            continue
        if not any(c.startswith("verdict") for c in cells):
            continue
        # next line must be the separator
        if i + 1 >= len(lines) or not re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1]):
            continue
        header = split_row(ln)
        rows = []
        for ln2 in lines[i + 2:]:
            if ln2.count("|") < 3:
                break
            rows.append(split_row(ln2))
        return header, rows
    return None, []


def col(header, prefix):
    for idx, h in enumerate(header):
        if h.strip().lower().startswith(prefix):
            return idx
    return None


def beats_in(cell):
    out = set()
    for m in RANGE_RE.finditer(cell):
        lo, hi = int(m.group(1)), int(m.group(2))
        if hi >= lo and hi - lo < 100:
            width = max(len(m.group(1)), len(m.group(2)))
            out.update("B" + str(n).zfill(width) for n in range(lo, hi + 1))
    out.update(BEAT_RE.findall(cell))
    return out


def has_claim(text):
    return bool(CLAIM_RE.search(text or ""))


def check(reel_dir, strict_coverage=False):
    blockers, advisories = [], []
    fc_path = os.path.join(reel_dir, "FACTCHECK.md")
    if not os.path.exists(fc_path):
        return [("FC-1", "FACTCHECK.md is missing — Gate F's -f test should have "
                         "caught this first.")], [], {}

    md = open(fc_path, encoding="utf-8", errors="replace").read()
    header, rows = read_rows(md)
    if not header or not rows:
        blockers.append(("FC-1",
                         "no claims table found. FACTCHECK.md needs a markdown table "
                         "with a Beat column and a Verdict column — see FACTCHECK-SPEC.md."))
        return blockers, advisories, {}

    i_beat = col(header, "beat")
    i_verd = col(header, "verdict")
    i_src = col(header, "source")

    covered, bad = set(), 0
    for n, r in enumerate(rows, 1):
        if i_beat is not None and i_beat < len(r):
            covered |= beats_in(r[i_beat])
        v = r[i_verd].strip() if i_verd is not None and i_verd < len(r) else ""
        s = r[i_src].strip() if i_src is not None and i_src < len(r) else ""
        vl = v.lower().strip("*_` ")
        if vl in FAIL_EXACT:
            blockers.append(("FC-2", f"row {n}: empty or placeholder Verdict ({v!r}). "
                                     f"An unfilled row is not a check."))
            bad += 1
            continue
        if i_src is not None and s.lower().strip("*_` ") in FAIL_EXACT:
            blockers.append(("FC-2", f"row {n} ({v}): empty or placeholder Source ({s!r}). "
                                     f"A verdict with no derivation cannot be re-checked "
                                     f"by anyone."))
            bad += 1
        ok = bool(OK_RE.search(vl))
        if FAIL_RE.search(vl) and not ok:
            blockers.append(("FC-3", f"row {n}: verdict {v!r} is unresolved or failing. "
                                     f"Resolve it, or reword the narration so the claim "
                                     f"is not made."))
            bad += 1
        elif not ok:
            advisories.append(("FC-6", f"row {n}: verdict {v!r} is not one of PASS / "
                                       f"CORRECTED / EXEMPT. The gate cannot tell whether "
                                       f"that is a pass — see FACTCHECK-SPEC.md."))

    if not re.search(r"^\s*status\s*:", md, re.I | re.M):
        advisories.append(("FC-5", "no `Status:` line — add one naming who signed off "
                                   "and when, so the file is auditable."))

    # ---- FC-4 coverage
    stats = {"rows": len(rows), "covered": len(covered), "claim_beats": 0, "uncovered": []}
    bs_path = os.path.join(reel_dir, "beat_sheet.json")
    if os.path.exists(bs_path):
        try:
            bs = json.load(open(bs_path))
        except Exception as e:
            advisories.append(("FC-4", f"beat_sheet.json unreadable ({e}) — coverage not checked."))
            bs = None
        if bs:
            missing = []
            for b in bs.get("beats", []):
                bid = b.get("beat_id", "")
                if not bid or not has_claim(b.get("narration_text", "")):
                    continue
                stats["claim_beats"] += 1
                if bid not in covered:
                    missing.append(bid)
            stats["uncovered"] = missing
            if missing:
                msg = (f"{len(missing)} beat(s) speak a figure, date or quantity and appear "
                       f"in no FACTCHECK row: {', '.join(missing)}. Either add a row or "
                       f"confirm the number is not a claim.")
                (blockers if strict_coverage else advisories).append(("FC-4", msg))
    return blockers, advisories, stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("reel_dir")
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--strict-coverage", action="store_true",
                    help="promote the FC-4 coverage advisory to a blocking defect")
    a = ap.parse_args()
    blockers, advisories, st = check(a.reel_dir, strict_coverage=a.strict_coverage)
    if not a.quiet:
        if blockers:
            print(f"[factcheck] {len(blockers)} blocker(s):")
            for rule, msg in blockers:
                print(f"  [{rule}] {msg}")
        if advisories:
            print(f"[factcheck] {len(advisories)} advisory(ies) — not blocking:")
            for rule, msg in advisories:
                print(f"  ({rule}) {msg}")
        if not blockers and not advisories:
            print("[factcheck] clean — every row resolved, every claim-bearing beat covered")
        if st:
            print(f"[factcheck] rows={st.get('rows',0)} beats_covered={st.get('covered',0)} "
                  f"claim_bearing_beats={st.get('claim_beats',0)} "
                  f"uncovered={len(st.get('uncovered',[]))}")
    if blockers:
        return 2
    return 1 if advisories else 0


if __name__ == "__main__":
    sys.exit(main())
