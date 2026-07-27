#!/usr/bin/env bash
# Render brutalist.art thumbnails: HTML -> crisp 2x PNG -> 1280x720 spec PNG.
# A full run also writes contact.png (all variations) and mobile.png (feed-size QA).
#
# Usage: ./render.sh <skill-slug>        (default: superpowers) -> full set + sheets
#        ./render.sh <skill-slug> v03    (single variation, no sheets)
set -euo pipefail

CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
HERE="$(cd "$(dirname "$0")" && pwd)"
SLUG="${1:-superpowers}"
ONLY="${2:-}"
SRC="$HERE/skills/$SLUG"
OUT="$HERE/out/$SLUG"
RAW="$OUT/@2x"
mkdir -p "$OUT" "$RAW"

# label for a variation file (edit to taste; used only in contact.png)
label(){ case "$1" in
  v01) echo "typographic serif hero";; v02) echo "word left + terminal";;
  v03) echo "terminal-window hero";;   v04) echo "SKILL.md file + word";;
  v05) echo "cream · restraint";;       v06) echo "before / after";;
  v07) echo "mono /command hero";;      v08) echo "composer + chip";;
  v09) echo "cream · poster";;          v10) echo "anatomy diagram";;
  *) echo "$1";; esac; }

shot(){ # shot <src-html> <out-png> <w> <h> <bg-aarrggbb>
  "$CHROME" --headless=new --disable-gpu --hide-scrollbars \
    --force-device-scale-factor=2 --window-size="$3,$4" \
    --default-background-color="$5" --virtual-time-budget=2800 \
    --screenshot="$2" "file://$1" >/dev/null 2>&1; }

shopt -s nullglob
NAMES=()
for html in "$SRC"/*.html; do
  name="$(basename "$html" .html)"
  [ -n "$ONLY" ] && [ "$name" != "$ONLY" ] && continue
  NAMES+=("$name")
  raw="$RAW/$name.png"; final="$OUT/$name.png"
  shot "$html" "$raw" 1280 720 00000000
  cp "$raw" "$final"; sips -z 720 1280 "$final" >/dev/null 2>&1   # downsample to spec
  printf '  rendered %-6s -> %s\n' "$name" "out/$SLUG/$name.png"
done

# sheets only on a full run
[ -n "$ONLY" ] && { echo "done -> $OUT"; exit 0; }

TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
# contact sheet: 2 columns, captioned
{ printf '<!doctype html><meta charset=utf-8><style>*{margin:0;box-sizing:border-box}body{background:#0c0c0c;font-family:ui-monospace,Menlo,monospace;padding:56px}.g{display:grid;grid-template-columns:1fr 1fr;gap:46px 44px}.cap{color:#8a8a8a;font-size:26px;margin:0 0 14px 4px}.cap b{color:#D97757}img{width:100%%;display:block;border:1px solid #2a2a2a;border-radius:8px}</style><div class=g>'
  for n in "${NAMES[@]}"; do printf '<div><div class=cap><b>%s</b> · %s</div><img src="%s/@2x/%s.png"></div>' "$n" "$(label "$n")" "$OUT" "$n"; done
  printf '</div>'; } > "$TMP/contact.html"
rows=$(( (${#NAMES[@]} + 1) / 2 )); ch=$(( 130 + rows * 760 ))
shot "$TMP/contact.html" "$OUT/contact.png" 2560 "$ch" ff0c0c0c
echo "  contact  -> out/$SLUG/contact.png"

# mobile QA: feed-size row(s) at ~246px
{ printf '<!doctype html><meta charset=utf-8><style>*{margin:0;box-sizing:border-box}body{background:#181818;font-family:ui-monospace,Menlo,monospace;padding:40px}.r{display:flex;gap:22px;flex-wrap:wrap}.c{width:246px}.cap{color:#9a9a9a;font-size:15px;margin:0 0 7px 2px}.cap b{color:#D97757}img{width:246px;display:block;border-radius:5px}</style><div class=r>'
  for n in "${NAMES[@]}"; do printf '<div class=c><div class=cap><b>%s</b></div><img src="%s/@2x/%s.png"></div>' "$n" "$OUT" "$n"; done
  printf '</div>'; } > "$TMP/mobile.html"
mrows=$(( (${#NAMES[@]} + 4) / 5 )); mh=$(( 80 + mrows * 220 ))
shot "$TMP/mobile.html" "$OUT/mobile.png" 1420 "$mh" ff181818
echo "  mobile   -> out/$SLUG/mobile.png"
echo "done -> $OUT"
