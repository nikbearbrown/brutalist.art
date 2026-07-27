#!/usr/bin/env bash
# Render brutalist.art thumbnails to 1280x720 (from a crisp 2x master). No npm/network/keys.
#
# TEMPLATE MODE — make one skill card from the parametric template:
#   ./render.sh claude-skills --cmd /pdf --num 53
#   ./render.sh claude-skills --cmd /commit --num 54 --skin dark
#   ./render.sh claude-skills --cmd /slides --num 55 --title "Claude Skills" --out slides
#     flags: --cmd <slash-command>  --num <n|"" to hide>  --skin light|dark
#            --title <headline>      --out <filename>  (default: derived from --cmd)
#
# GALLERY MODE — render the example HTML in skills/<slug>/ (+ contact & mobile sheets):
#   ./render.sh superpowers          # whole folder + sheets
#   ./render.sh superpowers v05      # a single variation
set -euo pipefail

CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
HERE="$(cd "$(dirname "$0")" && pwd)"

shot(){ # shot <url> <out-png> <w> <h> <bg-aarrggbb>
  "$CHROME" --headless=new --disable-gpu --hide-scrollbars \
    --force-device-scale-factor=2 --window-size="$3,$4" \
    --default-background-color="$5" --virtual-time-budget=2800 \
    --screenshot="$2" "$1" >/dev/null 2>&1; }
enc(){ node -e 'process.stdout.write(encodeURIComponent(process.argv[1]||""))' "$1"; }
spec(){ cp "$1" "$2"; sips -z 720 1280 "$2" >/dev/null 2>&1; }   # 2x master -> 1280x720 spec

SLUG="${1:-superpowers}"; [ $# -gt 0 ] && shift
ONLY=""; TPL=0; NUM=""; CMD="superpowers"; TITLE="Claude Skills"; SKIN="light"; MASCOT="shocked"; OUTNAME=""
while [ $# -gt 0 ]; do case "$1" in
  --num)    NUM="${2:-}";    shift 2; TPL=1;;
  --cmd)    CMD="${2:-}";    shift 2; TPL=1;;
  --title)  TITLE="${2:-}";  shift 2; TPL=1;;
  --skin)   SKIN="${2:-}";   shift 2; TPL=1;;
  --mascot) MASCOT="${2:-}"; shift 2; TPL=1;;
  --out)    OUTNAME="${2:-}"; shift 2;;
  --*)      echo "unknown flag: $1" >&2; shift;;
  *)        ONLY="$1"; shift;;
esac; done

OUT="$HERE/out/$SLUG"; RAW="$OUT/@2x"; SRC="$HERE/skills/$SLUG"; mkdir -p "$OUT" "$RAW"

# ---------- template mode ----------
if [ "$TPL" = 1 ]; then
  name="$OUTNAME"
  [ -z "$name" ] && name="$(printf '%s' "$CMD" | sed 's#^/##; s#[^A-Za-z0-9._-].*##')"
  [ -z "$name" ] && name="card"
  url="file://$HERE/templates/skill-card.html?title=$(enc "$TITLE")&cmd=$(enc "$CMD")&num=$(enc "$NUM")&skin=$(enc "$SKIN")&mascot=$(enc "$MASCOT")"
  shot "$url" "$RAW/$name.png" 1280 720 00000000
  spec "$RAW/$name.png" "$OUT/$name.png"
  printf '  built  /%s  #%-3s  %-5s  %-10s -> out/%s/%s.png\n' "${CMD#/}" "${NUM:-–}" "$SKIN" "${MASCOT:-none}" "$SLUG" "$name"
  echo "done -> $OUT/$name.png"; exit 0
fi

# ---------- gallery mode ----------
label(){ local t
  t=$(tr -d '\r\n' < "$SRC/$1.html" | grep -oE '<title>[^<]*</title>' | sed -E 's:</?title>::g')
  t=${t#v[0-9][0-9] — }
  [ -n "$t" ] && echo "$t" || echo "$1"; }

shopt -s nullglob
NAMES=()
for html in "$SRC"/*.html; do
  n="$(basename "$html" .html)"
  [ -n "$ONLY" ] && [ "$n" != "$ONLY" ] && continue
  NAMES+=("$n")
  shot "file://$html" "$RAW/$n.png" 1280 720 00000000
  spec "$RAW/$n.png" "$OUT/$n.png"
  printf '  rendered %-16s -> out/%s/%s.png\n' "$n" "$SLUG" "$n"
done

[ -n "$ONLY" ] && { echo "done -> $OUT"; exit 0; }

TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
{ printf '<!doctype html><meta charset=utf-8><style>*{margin:0;box-sizing:border-box}body{background:#0c0c0c;font-family:ui-monospace,Menlo,monospace;padding:56px}.g{display:grid;grid-template-columns:1fr 1fr;gap:46px 44px}.cap{color:#8a8a8a;font-size:26px;margin:0 0 14px 4px}.cap b{color:#D97757}img{width:100%%;display:block;border:1px solid #2a2a2a;border-radius:8px}</style><div class=g>'
  for n in "${NAMES[@]}"; do printf '<div><div class=cap><b>%s</b> · %s</div><img src="%s/@2x/%s.png"></div>' "$n" "$(label "$n")" "$OUT" "$n"; done
  printf '</div>'; } > "$TMP/contact.html"
rows=$(( (${#NAMES[@]} + 1) / 2 )); shot "file://$TMP/contact.html" "$OUT/contact.png" 2560 $(( 130 + rows * 760 )) ff0c0c0c
echo "  contact  -> out/$SLUG/contact.png"

{ printf '<!doctype html><meta charset=utf-8><style>*{margin:0;box-sizing:border-box}body{background:#181818;font-family:ui-monospace,Menlo,monospace;padding:40px}.r{display:flex;gap:22px;flex-wrap:wrap}.c{width:246px}.cap{color:#9a9a9a;font-size:15px;margin:0 0 7px 2px}.cap b{color:#D97757}img{width:246px;display:block;border-radius:5px}</style><div class=r>'
  for n in "${NAMES[@]}"; do printf '<div class=c><div class=cap><b>%s</b></div><img src="%s/@2x/%s.png"></div>' "$n" "$OUT" "$n"; done
  printf '</div>'; } > "$TMP/mobile.html"
mrows=$(( (${#NAMES[@]} + 4) / 5 )); shot "file://$TMP/mobile.html" "$OUT/mobile.png" 1420 $(( 80 + mrows * 220 )) ff181818
echo "  mobile   -> out/$SLUG/mobile.png"
echo "done -> $OUT"
