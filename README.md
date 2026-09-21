# brutalist

The pared-down Brutalist video toolkit: builders, personas, and shared production
doctrine, with local Kokoro voices (Onyx `am_onyx`, Bella `af_bella`).

**Free by default** — Kokoro, Manim, Remotion, no account required.
**Optional:** a Higgsfield CLI login (`higgsfield auth login`) unlocks AI video
beats. Absent = the free path (Ken Burns stills) runs silently. No ElevenLabs,
ever.

**Read [`HOW-TO.md`](HOW-TO.md)** — what Brutalist is, install, the three
core builders, and the worked examples. `CLAUDE.md` has the session rules for
agents.

```bash
./setup --install     # deps + Remotion node modules + the Kokoro model (~340MB, auto-downloaded)
./art --list          # the skills
./art keys            # check optional Higgsfield login + SI key
```

## Builders

| Skill | What it makes |
|---|---|
| `ai-explainer` | Claude-branded explainer reel — the tight cut |
| `cli-explainer` | Prompt → real code → moving output (the build reel) |
| [`godot-waikthrough`](skills/make/godot-waikthrough/SKILL.md) | Play a Godot game, cover its implemented features with Liam riffs, render in 4K; optional `walker` Claude/GDD bookends |
| [`godot-gamedev`](skills/make/godot-gamedev/SKILL.md) | Detailed game-development film: actual code, scenes, resources, assets and art in source-backed Godot teaching views; optional `walker` bookends |
| [`godot-gdd`](skills/make/godot-gdd/SKILL.md) | Explain a complete GDD using existing game evidence; separate proposals, implementation, tests and human decisions; optional `walker` bookends |
| `deep-explainer` | 5–10 min documentary episode with vox pantry beats |
| `anthropics` | Reads an Anthropic artifact (repo/paper/content) against its own claims; practitioner-report register |
| `fashionista` | AI fashion-call experiment — sports-announcer call with stated confidence + correction ask |
| `fellows` | Wraps a HAI fellow's video report in Claude bookends for @HumanitariansAI |
| `finance` | Templatized SEC EDGAR filings reel — 11 beats, 5 charts, fully deterministic, two audits |
| `guests` | Wraps a board-member or invited-speaker video in Claude bookends for @HumanitariansAI |
| [`seis-profile`](skills/make/seis-profile/SKILL.md) | One spotlight reel per Northeastern COE student story for SEIS — NEU brand, Liam narrates in third person, batch of 112 |
| [`seis-ai`](skills/make/seis-ai/SKILL.md) | The SEIS unit's own AI explainer ("SEIS & the future of AI"), corpus-first, ≤5 min |
| [`seis-extract`](skills/make/seis-extract/SKILL.md) | Alumni interview (Teams/Zoom mp4) → branded Q&A clips: Bella asks on a SEIS page, the alum answers with captions and a lower third |
| [`seis-composite`](skills/make/seis-composite/SKILL.md) | Assemble seis-extract clips into the SEIS alumni impact film from an editing-brief timeline |
| [`medhavy-walkthrough`](skills/make/medhavy-walkthrough/SKILL.md) | Real Medhavy Hub browser capture with Liam riffs; optional textbook bookends |
| [`cc-explainer`](skills/make/cc-explainer/SKILL.md) | Terminal-first Claude Code explainer: cold open → idea → definitions → loop → conduct/human |
| [`musinique-bookend`](skills/make/musinique-bookend/SKILL.md) | Musinique intro/outro cards around a raw music film |
| [`lyric-overlay`](skills/make/lyric-overlay/SKILL.md) | Karaoke-style word timing over a song (real transcription, never guessed lyrics) |
| [`post`](skills/make/post/SKILL.md) | Stage a verified 4K master into the one upload folder (`./art post`) |

## Brands (what a SEIS or Northeastern user needs, all in this repo)

| File | What it holds |
|---|---|
| [`brands/neu.md`](brands/neu.md) | Northeastern palette (NU Red `#C8102E`, black, white, gold), Lato type, logo rules, layout laws |
| [`brands/seis.md`](brands/seis.md) | The SEIS unit variant: unit marks, Spotlight register, Liam/Bella voices, bookends |
| [`runtime/design/NEU-DESIGN.md`](runtime/design/NEU-DESIGN.md) | The full NEU visual constitution (from brand.northeastern.edu) |
| `runtime/remotion/src/tokens/neu.ts`, `tokens/lato.ts` | The values the scenes read; `useLato()` loads the bundled face per scene |
| `runtime/remotion/public/fonts/Lato-*.ttf` | Lato Regular + Bold (SIL OFL, license alongside) |
| [`logos/seis/`](logos/seis/README.md) | Official NU Primary Marks (eps/png/svg) + the two SEIS unit marks in `unit/`; RGB SVGs at `runtime/remotion/public/northeastern/official/` |
| `runtime/remotion/public/seis/` | The two unit marks for `staticFile()`; per-reel photos are NOT shipped (rights) — the scripts copy them in from the story corpus |

Nothing else is needed from any laptop: clone, `./setup --install`, and the SEIS skills run on these files.

## Personas

| Skill | Register | Voice |
|---|---|---|
| `nbb` | Teardown — take it apart, judge the design | Kokoro `am_onyx` |
| `hai` | Plain — simple and direct; method, when to use it, when NOT to | Kokoro `af_bella` |

## Doctrine (not entry points — inherited by builders)

| Skill | What it governs |
|---|---|
| `explainer` | Parent compositing chassis all builders inherit |
| `your-turn` | The closing three-beat standard |
| `duration-planner` | Duration is an output of the content, never a target |
| `nopunt` | Maps every animatable beat-type to the right Brutalist primitive |
| `screen-clean` | Prepares screen recordings (Zoom/Teams/Meet) for use as a reel beat |
| [`riff`](skills/make/riff/SKILL.md) | Inspect/render an artifact; explain the visible event, mechanism, trade-offs, and educational use |

### Game walkthroughs

Ask your agent: `godot-waikthrough walker /path/to/walker-jumpman` (or use the
alias `godot-walkthrough`). Without `walker`, it opens on gameplay; with it, the
Claude prompt asks Walker to convert the game's GDD, and beat two summarizes
what was actually built. Both use real gameplay, Liam's on-screen riffs, and the
regular outro—not a game-themed sound/voice ending. The skill renders locally
for review; it does not publish.

`./art godot-waikthrough --help` and `./art riff --help` show the agent workflows.
`./art godot-waikthrough --check /path/to/reel` runs the read-only coverage gate.
As with the other builders, invoking `./art <skill>` alone shows the skill to
follow; it is not an autonomous film-render command.

Note: the Kokoro voice model is not in this repo (GitHub's 100MB file limit)
— `./setup --install` fetches it once from the kokoro-onnx releases.

### Godot development films

Ask your agent: `godot-gamedev walker /path/to/walker-jumpman`. This is the
component-by-component companion to the gameplay walkthrough: code, saved and
runtime scenes, resources, assets, procedural art, tests, and export status.
The `walker` modifier adds the Claude/GDD opening, built-result summary, verdict,
Your Turn, and regular stock-only outro. Without it, open directly on the game.

`./art godot-gamedev --help` shows the workflow. The read-only source gate is:

```bash
./art godot-gamedev --check /path/to/reel --game /path/to/project-containing-project.godot
```

The reusable `GodotDevWorkbench` scene has code, tree, asset, and trace views,
including native portrait layout. Its editor chrome is explicitly reconstructed;
source excerpts, runtime observations and art previews must come from the actual
game. It does not modify game code, pretend to export a game, or publish a film.
