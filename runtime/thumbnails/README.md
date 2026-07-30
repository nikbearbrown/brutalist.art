# Thumbnails — brutalist.art

How to make **premium, brand-consistent, faceless** YouTube thumbnails for the
Brutalist explainer videos (videos about Claude skills / Claude Code). No human
faces, no shocked expressions — the design carries the click.

This is both a **guide** (the research + rules below) and a **generator** (HTML
templates rendered to 1280×720 PNGs with `render.sh`). It reuses the toolkit's
own design tokens, so thumbnails read as the same brand as the videos.

---

## TL;DR — how to make a set

```bash
cd runtime/thumbnails
./render.sh superpowers          # render every skills/superpowers/*.html
./render.sh superpowers v05      # render just one
```

Output lands in `out/<slug>/vNN.png` (1280×720, YouTube spec) plus a crisp 2×
master in `out/<slug>/@2x/`. To make thumbnails for a **new** skill, copy
`skills/superpowers/` to `skills/<your-skill>/`, edit the copy in the words, and
`./render.sh <your-skill>`. Everything visual comes from `lib/base.css`.

Then eyeball `out/<slug>/contact.png` (all variations) and, critically,
`out/<slug>/mobile.png` (feed size — see the QA rule below).

---

## The locked series template (Claude Skills)

The chosen look for the Claude-skills series is a parametric card
(`templates/skill-card.html`): a centered `✳ Claude Skills` serif lockup, the
`/command` underneath, a `#num` index top-left, and the pixel Claude mascot
bottom-right. Each new video is **one command** — only the number and the
command word change:

```bash
./render.sh claude-skills --cmd /pdf --num 53 --mascot suspicious   # light (default)
./render.sh claude-skills --cmd /commit --num 54 --skin dark --mascot smug
./render.sh claude-skills --cmd /slides --num 55 --mascot laughing --out slides
```

Flags: `--cmd` slash command (drives the filename too) · `--num` skill index
(`--num ""` hides it) · `--skin light|dark` · `--mascot <emotion>` (`--mascot ""`
hides it) · `--title` headline (default "Claude Skills") · `--out` output
filename. Output → `out/claude-skills/<cmd>.png` (+ `@2x/`). Light↔dark
auto-adapts (logo, ink, and dot grid flip; the mascot stays terracotta).
`skills/claude-skills/*.html` holds the earlier exploration (a–e) that led here;
the template is the source of truth going forward.

### Mascots (bottom-right)

The pixel Claude mascot in the bottom-right sets the tone (a proven CTR lever).
**26** live in `assets/mascots/` — pick one per video with `--mascot`
(`--mascot ""` hides it). See `out/claude-skills/mascots-library.png`.

- **Emotions:** shocked · laughing · furious · crying · suspicious · smug
- **Actions:** explaining · question · idea · tip · example · coding ·
  debugging · searching · testing · fixing · success · error · warning ·
  blocked · retry · setup · automate · compare · connect · launch

Tip: match the mascot to the command (`/debug` + debugging, `/ship` + launch).

They're cut from a grid sprite sheet by `tools/extract_mascots.py`, which knocks
out the cream/shadow background to transparent (keeping bodies, eyes, and colour
/ tool accessories) and crops each cell's text label — so they sit cleanly on
both light and dark grounds:

```bash
# args: <sheet.png> <out_dir> <cols> <comma,separated,names,row-major>
python3 tools/extract_mascots.py sheet.png assets/mascots 5 "explaining,question,..."
```

### Batch: one thumbnail per video folder

`tools/thumbnail_youtube.sh` writes a `thumbnail.png` into every
`clauded/youtube/<skill>/` folder — title "Claude Skills", command `/<slug>`,
skin light, and a topic-matched mascot (see the `mascot_for()` map in the
script). The command line auto-shrinks so long slugs never clip. Numbers are
omitted (no canonical episode order in the repo).

```bash
tools/thumbnail_youtube.sh                       # defaults to ../../clauded/youtube
tools/thumbnail_youtube.sh /path/to/youtube      # or point it somewhere
```

Re-run anytime; it overwrites in place. To change a single card, use the
one-off template command with `--dest`:

```bash
./render.sh claude-skills --cmd /code-review --mascot searching \
  --dest /path/to/youtube/code-review/thumbnail.png
```

To retheme for a different series, copy `templates/skill-card.html` and edit it.

---

## Part 1 — The brand (non-negotiable look)

Pulled from `runtime/remotion/src/tokens/` so thumbnails match the videos.

### The two laws
- **Anti-default law:** *No centered layouts. No purple gradients. No Inter
  font.* Everything is left-anchored / asymmetric — which also happens to be
  what "premium" thumbnails do (rule-of-thirds, not dead-center).
- **One-accent law:** exactly **one** terracotta moment per thumbnail. The
  accent is *earned* — a single period, one keyword, one chip, one cursor.
  Body text is never terracotta (it fails contrast). Everything else is
  ink-on-ground.

### Palette (Claude skin)
| | Dark (default) | Cream (primary brand) |
|---|---|---|
| ground | `#1F1E1B` | `#FAF9F5` |
| ink | `#F0EEE6` | `#3D3929` |
| ink-soft | `#B0AC9F` | `#73705F` |
| card | `#2E2C28` | `#FFFFFF` |
| border | `#413F3A` | `#E5E2D9` |
| **accent (spark)** | `#D97757` | `#D97757` |
| accent-deep (send) | `#C6613F` | `#C6613F` |

Add `class="cream"` on `.frame` to switch skins. Dark reads as the reliable,
high-contrast default; cream is the calmer, more editorial primary brand.

### Type (all bundled in `runtime/fonts/`, loaded offline via `@font-face`)
- **EB Garamond** — editorial serif for hero titles (weights 400/500; no bold,
  so go big instead of heavy). This is the signature premium move.
- **Montserrat** — geometric sans, **Bold 700** for punchy stacked headlines.
- **PT Mono** — labels, terminals, `/commands`, the CLI identity.

### Motifs
`// ` label prefix (mono, uppercase, letterspaced) · `›` list bullets · block
cursor `▌` in accent · radial dotted grid at 5% · 2px hairline rules ·
fidelity "windows" (traffic-light chrome, active dot = spark) for terminal /
file / composer mockups.

---

## Part 2 — Faceless premium principles (the research)

The core insight: **a face conveys emotion; a faceless thumbnail must convey an
*object* or an *event*.** You manufacture, with type and graphics, the instant
"what is this?" that a face gives for free — one unmistakable hook + a few words.

**Premium = restraint.** Cheap is crowded, loud, many colors. Premium is calm,
high-contrast, few elements, deliberate space.

- **≤ 3 elements.** One hero + one line of text + one brand mark. That's it.
- **2–3 colors max** = monochrome ground + one accent doing all the work (the
  Stripe / Linear / Vercel formula; here it's ink + terracotta).
- **30–40% negative space.** Take the spacing that feels like enough, then
  leave it. Crowded reads as cheap and stressful.
- **One dominant hero** at ~40–60% of the frame (a big word, a `/command`, a
  UI window, a file card). One focal point only.
- **Aggressive contrast.** Off-white on warm charcoal; warm near-black on
  cream. Nothing muddy in between.
- **Complement the title, don't repeat it.** Thumbnail words + video title are
  a *pair* delivering two halves of the hook.

### Hard specs (build to these)
| Parameter | Value |
|---|---|
| Canvas | **1280×720**, 16:9 (we master at 2× = 2560×1440) |
| File size | **< 2 MB** (PNG for crisp text — our outputs are ~100 KB) |
| Safe area | keep essentials inside central **1100×620** (90/50px margin) |
| Timestamp dead zone | **bottom-right ~15–20%** is covered by YouTube's
  duration stamp — never put text/logo/hero there (wordmark sits bottom-**left**) |
| Words | **3–5 max; 1–2 ideal.** Fewer is more premium |
| Min text size | hero huge; supporting text **≥ ~26px** in the 1280 file |
| Contrast | 4.5:1 body, 3:1 large/bold (the Claude palette clears this) |

### The one test that matters: **mobile**
70%+ of impressions are on a phone, where the thumbnail shrinks to ~160–250px.
`render.sh` also emits `out/<slug>/mobile.png` at ~246px. **If the hero doesn't
read there, the design fails** — no matter how good it looks full-size. Text-
heavy layouts (pure terminals, small captions) are the usual casualties.

---

## Part 3 — The layout archetypes (= the 10 templates)

Ten reusable, locked layouts for faceless dev/AI content. The example set is the
**superpowers** skill; each maps to a template in `skills/superpowers/`.

| # | Template | Archetype | Notes |
|---|---|---|---|
| v01 | typographic serif hero | Big-word | One huge serif word + accent period. Max restraint. **Feed-proof.** |
| v02 | word left + terminal | Split (word + UI) | The workhorse for "explaining a tool." |
| v03 | terminal-window hero | Product hero | The CLI *is* the subject. Beautiful up close, weak at feed size. |
| v04 | SKILL.md file + word | Product hero | The skill file as hero; serif word anchors it. |
| v05 | cream · restraint | Big-word (cream) | Two-line serif on the primary-brand ground. **Feed-proof.** |
| v06 | before / after | Diptych | Plain Claude vs + skills. Transformation at a glance. |
| v07 | mono `/command` hero | Typographic (mono) | Pure CLI identity: giant `/skill` + cursor. **Feed-proof.** |
| v08 | composer + chip | Diff / highlight | Fidelity composer, skill chip lit in accent. |
| v09 | cream · poster | Editorial poster | Title + rule + subline. The most "publication" look. |
| v10 | anatomy diagram | Explainer / list | Serif title + 3 labelled parts. Good for "how it works." |

**For a series, pick one or two templates and lock them.** Consistency is the
brand: viewers (and the algorithm) learn to recognize the look across 5–10
videos. Color-code by persona if useful — same grid + type + wordmark, swap the
accent (e.g. keep terracotta for one channel, use each persona's accent for
another) so the set reads as one system.

---

## Part 4 — Files

```
runtime/thumbnails/
  README.md            ← this guide
  render.sh            ← HTML → 2× PNG → 1280×720 (Chrome headless, offline)
  lib/base.css         ← tokens, fonts, motif helpers, window/chip components
  skills/<slug>/*.html ← the templates (one per variation)
  out/<slug>/          ← vNN.png (spec) + @2x/ (masters) + contact.png + mobile.png
```

`render.sh` uses the system Google Chrome in headless mode — no npm install, no
network, no keys. Fonts load from `runtime/fonts/` via relative `@font-face`.

### QC checklist before shipping a thumbnail
1. **Look at the frame** (not just the file). `out/<slug>/vNN.png`.
2. **Look at `mobile.png`** — does the hero read at feed size?
3. One accent moment only? Left-anchored (no dead-center)? No Inter, no purple?
4. Nothing critical in the bottom-right timestamp zone?
5. 3–5 words max, complementing (not repeating) the planned title?
