# Claude Code interface templates

Reusable Remotion scenes for videos in which Claude Code — the terminal
session, the theme picker, the web home — is the subject. They parallel the
Cowork walkthrough kit and the Codex interface family: **no screen recording,
no click tracking — just props.** Every pixel is a motion component driven by
a beat sheet.

## Components

All registered in Remotion Studio under the `CC` folder. Each exports a Zod
schema, a props type, and a `*Demo` twin with filled default props. Product
colors, typography, and the VERBS list live in `../tokens/claudecode.ts`.

- `CCShell` — terminal window chrome: traffic lights, centred session title,
  body slot, footer with verbatim product mode strings (`plan mode on`,
  `accept edits on`, `◐ medium · /effort`). Keybinding fragments render VIOLET.
- `CCSession` — full session: stacks prompt / status / tool / diff / plan /
  text blocks with staggered live-session reveal. One beat = one block list.
- `CCPromptBar` — the `>` input band with char-rate typing and block cursor.
- `CCStatusVerb` — pulsing ✳ spark + gerund + animated ellipsis + elapsed /
  token metadata. Verbs come from `VERBS` (Pontificating, Fermenting,
  Symbioting, Spelunking, …) — real product gerunds only.
- `CCToolCall` — nested tool tree (`Explore` └ `Bash` / `Read`), braille
  spinner while live, green ✓ on return, `+N more tool uses (ctrl+o)` and
  `ctrl+b to run in background` hints.
- `CCDiff` — `Update(file)` header, add/remove counts, gutter-numbered diff
  rows on the dark ADD_BG / DEL_BG bands.
- `CCPlanCard` — the bordered plan box: **Files to create**, **Verification**
  numbered steps.
- `CCThemePicker` — onboarding theme list with ✓ / ❯ selection and a live
  diff preview that reskins per theme; Clawd + pixel flowers strip.
- `CCWebHome` — claude.ai/code home: dotted canvas, centred Clawd, repo /
  branch pills, suggestion rows with ghost previews.
- `CCWalkthroughDemo` — 12 s, 4-shot kit tour (WebHome → ThemePicker →
  Session → StatusVerb outro), Clawd threaded through every shot. The CC
  sibling of `CoworkWalkthroughDemo`.

## The Clawd mascot contract

The mascot is ONE component — `ClaudeMascotScene.tsx` exports `MascotSVG`,
`computeAnimation`, and the 18-name `ANIMATIONS` enum (idle, bounce, wave,
look, walk, run, think, type, sleep, error, nod, shake, dance, stretch,
crouch, jump, spin, celebrate). Never redraw the pig; never inline a second
copy.

Where Clawd appears in this family — always prop-gated, always off by default:

- `CCShell.mascot` (+ `mascotCorner`) — small corner Clawd inside the body.
- `CCSession.mascot` — `'off' | 'auto' | <animation>`. `'auto'` follows the
  latest cued block: prompt→look, status→think, tool/diff→type, plan→nod;
  90 frames after the last cue Clawd celebrates.
- `CCStatusVerb.mascot` — large Clawd right of the status column (`think`
  pairs with a running verb, `celebrate` with a finished run).
- `CCThemePicker` / `CCWebHome` — Clawd is part of the scene itself.

**PIXEL-ART LAW (hard — no exceptions).** `shape-rendering: crispEdges` rects
move ONLY by translation and axis-aligned scale. NEVER rotation. spin =
scaleX flip; nod/bounce/stretch/crouch/jump = foot-anchored scaleY; wave =
rightArmTy oscillation. Foot anchor: `ty = 86*(1−sy) − jumpH`. Integer-crisp
scaling, no anti-aliasing, no tilt.

## Editorial law

Use Claude Code chrome only when Claude Code or terminal work is the subject
(the ILLUSTRATE LAW from the ai-explainer family applies). The visual
sequence should reveal the product's actual loop:

```text
PROMPT → THINK → TOOLS → CHANGE → VERIFY → HANDOFF
```

Name the owner of every interface judgment: say "Claude Code's tool tree" or
"Cowork's composer", not "the interface", whenever two products appear in the
same script. Mode strings, keybindings, and verbs are verbatim product
strings — never paraphrase them. Generated charts, diagrams, and simulations
still belong on their own result plane; CC chrome earns the prompt, status,
tool, diff, plan, and theme beats — it is not generic wallpaper.

Clawd is punctuation, not wallpaper: one mascot per shot, posed by what the
session is actually doing. If the pose doesn't answer "what is the session
doing right now?", turn it off.
