#!/usr/bin/env bash
# Write a brutalist "Claude Skills" thumbnail.png into each clauded/youtube/<skill>/ folder.
# Title = "Claude Skills"; command = /<folder-slug>; mascot chosen per topic; skin light.
# Usage: tools/thumbnail_youtube.sh [youtube_dir]
set -euo pipefail
HERE="$(cd "$(dirname "$0")/.." && pwd)"      # runtime/thumbnails
YT="${1:-$HERE/../../clauded/youtube}"
[ -d "$YT" ] || { echo "no such dir: $YT" >&2; exit 1; }

# topic -> mascot (from the 26-mascot library). Fallback: idea.
mascot_for(){ case "$1" in
  academic-paper|project-artifact|receipts|session-report|academic-paper-reviewer) echo example;;
  academic-pipeline|hookify|commit-commands)   echo automate;;
  agent-sdk-dev|feature-dev|plugin-dev|mcp-server-dev) echo coding;;
  claude-code-setup)          echo setup;;
  claude-md-management)       echo example;;
  code-modernization)         echo fixing;;
  code-review|pr-review-toolkit|deep-research)  echo searching;;
  code-simplifier)            echo idea;;
  cwc-makers|superml)         echo launch;;
  explanatory-output-style)   echo explaining;;
  frontend-design|ui-ux-pro-max|frontend-slides|math-olympiad|learning-output-style|skill-creator) echo idea;;
  impeccable)                 echo success;;
  mcp-tunnels)                echo connect;;
  playground)                 echo laughing;;
  pyright-lsp)                echo debugging;;
  ralph-loop-keep-building)   echo retry;;
  security-guidance)          echo warning;;
  *)                          echo idea;;
esac; }

n=0
for d in "$YT"/*/; do
  slug="$(basename "$d")"
  # a video folder is one that carries the build metadata
  [ -f "$d/beat_sheet.json" ] || [ -d "$d/mp4" ] || continue
  m="$(mascot_for "$slug")"
  "$HERE/render.sh" claude-skills --cmd "/$slug" --skin light --mascot "$m" \
    --out "yt-$slug" --dest "$d/thumbnail.png" | sed 's/^/  /'
  n=$((n+1))
done
echo "== wrote $n thumbnails =="
