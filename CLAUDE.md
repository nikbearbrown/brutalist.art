> **You are in `brutalist.art` (DOT) — the PUBLIC, shippable toolkit.**
> Siblings: `brutalist-art/` (Bear's sandbox) · `brutalist_art/` (website + YouTube).
> Changes here reach outside users. Different trees — never treat a separator as a typo.

# CLAUDE.md — brutalist.art

brutalist.art is a free-by-default video explainer toolkit — 15 skills. Kokoro, Manim, and Remotion run with no account. Optional: Higgsfield CLI login unlocks AI video beats; absent = free path runs silently.

---

## When the user types `help` or "what do you do?"

Respond with exactly this structure — do NOT flatten all skills to an equal list. The tiering is the point.

---

### What this is

brutalist.art is a Brutalist video toolkit for Humanitarians AI fellows and collaborators. You get 15 skills, Kokoro TTS (local, free), Manim + Remotion rendering, and a phase-gated pipeline. Everything runs for free by default. Optional: a Higgsfield CLI login unlocks AI video beats — absent = free path silently.

---

### FELLOW TIER — free, safe, start here

| Skill | Use this when | Example |
|---|---|---|
| `fellows` | You have a HAI fellow's video report (.mp4/.mov) and want a Claude-bookended reel | `./art fellows path/to/reel/` |
| `ai-explainer` | You want to explain a concept in the Claude desktop-app visual style (cream, warm ink, terracotta) | `./art ai-explainer "What is gradient descent?"` |
| `hai` | You need a Humanitarians AI Plain-register reel from any text or beat sheet | `./art hai path/to/reel/` |
| `your-turn` | You want to close an existing reel with a structured handoff prompt for viewers | `./art your-turn path/to/reel/` |
| `duration-planner` | You need to size your content to a target length — or check if a beat is too long | `./art duration-planner path/to/reel/` |

---

### ADVANCED — Bear only

| Skill | Notes |
|---|---|
| `deep-explainer` | Multi-layered concept depth passes on the ai-explainer chassis (5–10 min, act-structured; vox stills only where the still IS the evidence) |
| `cli-explainer` | Claude session + live code + output as a moving vox beat |
| `show-tell` | Very simple, direct explainers: every beat is ONE drawn isometric illustration in the Claude palette (shared `templates/iso_kit.py`), a few words of label at most, and Liam (Kokoro `am_onyx`) explains in the voiceover. Opens hesitant writer → key terms, drawn Manim body, Your Turn in the Claude.ai composer, spoken @NikBearBrown outro; no verdict card |
| `nbb` | NikBearBrown/Teardown register — Kokoro am_onyx voice (free, local) |

---

### OPTIONAL UPGRADE — Higgsfield AI video beats

No key is required. If the `higgsfield` CLI is installed and logged in, AI video
beats are offered on a per-beat basis (you approve each one). Absent = free path
(Ken Burns stills) runs silently — never an error.

Three-way contract for any beat that could use Higgsfield:
1. CLI present + user approves → clip generated
2. CLI present + user declines → free path for that beat
3. CLI absent → free path silently; `./art todo <reel>` logs the beat as
   "free fallback (Higgsfield would upgrade this)"

| Context | Note |
|---|---|
| `explainer` | Parent chassis. Stills from Smithsonian CC0 (`smithsonian_fetch.py`) or pantry/. AI video via three-way contract above. |

---

### Not set up yet?

Run `./setup` first (add `--install` to install deps + fetch the Kokoro model). It verifies every dependency live — imports each Python module, runs `ffmpeg`/`ffprobe`, and synthesizes + decodes a real Kokoro test phrase — and tells you which features are READY.

---

## Rules

**Math in every film:** follow [MATH-TYPESETTING.md](docs/MATH-TYPESETTING.md).
Structured equations, verified algebra and actual rendered-frame review are
required. Ordinary text cards are not a fallback for a missing math renderer.
**Executable evidence:** follow [EXECUTABLE-EVIDENCE.md](docs/EXECUTABLE-EVIDENCE.md).
Run local code/data instead of requesting photographs or generated screenshots
of its output. Pantry remains for genuinely necessary source artifacts.

1. **Read the whole SKILL.md before building.** Every skill under `skills/make/` has a `SKILL.md` — it is doctrine, not a README. Read it completely.
2. **Audio-first.** Narration MP3s are generated and measured first (`runtime/scripts/generate_audio_kokoro.py`); their durations are the master clock. Never fix timing by hand — regenerate audio, recompile.
3. **Videos travel with their book.** Build into `<book>/youtube/<slug>/`, never into this toolkit folder. `examples/` holds study copies only.
4. **Verify renders by LOOKING at frames** (`_qc/` + qc-sheet), never by the mp4 probe alone. Render Remotion only via `runtime/scripts/remotion_scenes.py` (foreground) — never hand-roll `npx remotion render`.
5. **Never publish — render instead.** There is no publishing machinery here: no staging folder, no credentials, no upload. The job is *beat sheet → 4K master*, written to a folder you choose — `--out DIR`, else `$ART_OUT`, else `<toolkit>/renders/`. Any destination works, including a mounted drive. What happens to the file afterwards is yours. Rule-owner: **`RENDER-TARGETS.md`**.
   **9:16 is a different beat sheet, never a crop** — `shorts.py` writes its own sheet into `short/` and rewires each beat to a `<Pattern>916` composition where one is registered; a beat with no portrait variant is flagged, not silently center-cut. Same file, §3.
6. **Free by default (Fellow Tier).** The Fellow Tier runs entirely for free — Kokoro, Manim, Remotion. If any Fellow Tier step appears to require a key, stop: that is a bug, not a missing credential. Higgsfield is opt-in and only offered to ADVANCED users on a per-beat, explicit-approval basis. Never prompt a fellow to spend money.
7. **Tier discipline.** ADVANCED skills require Bear's sign-off. PAID skills require explicit spend approval before every paid API call. Never escalate a fellow into the PAID tier by default.

8. **Library-first — ask before you author.** Before a beat is authored, routed to Manim, slated, or written up as a request card, ask what already exists: `./art scenes "<what the beat needs>"`. `./art scenes --check <Name>` answers "is that composition renderable?" — the check that stops a slate. A hit is a LEAD (read the props); a candidate flagged `[derived text — open the file]` has no header of its own. A genuine miss is a PUNT — a design card, never a licence to slate — and is logged to `TEMPLATE-MISSES.md` automatically. After adding a component run `./art scene-index`: the index (`runtime/remotion/src/scenes.json`, generated from Root.tsx `<Composition>` ids) is the only way anyone finds it, and `SCENE-DOC-TODO.md` lists the scenes still running on derived search text.

## Skill reference

Full tier breakdown: `skills/TIERS.md`
All 15 skills on disk: `skills/make/` — `find skills/make -name SKILL.md | sort`

## Entry point

```bash
./art --list          # every skill
./art keys            # validate keys (FELLOW TIER: all free, no keys needed)
./art todo  <reel>    # per-video beat ledger
./art run   <reel>    # compile a review cut
./art final <reel>    # clean master (no beat markers)
```
