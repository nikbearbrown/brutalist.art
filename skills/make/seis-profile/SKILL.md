---
name: seis-profile
description: >
  Crank out ONE spotlight reel per Northeastern COE student spotlight story for
  SEIS (Software Engineering and Information Systems) — every student gets their
  own video, the whole series lands on SEIS's own YouTube. Runs on the NEU skin
  (brands/neu.md + brands/seis.md: white / NU black / NU red as the one accent /
  Lato, regular-weight headings, sentence case) with SEIS bookends
  (SeisSpotlightOpen · SeisCard recap · SeisProfileCredit · SeisOutro) — the
  Claude composer never appears. Inherits the ai-explainer `profile` modifier's
  people-laws (find the ONE idea, name recurs, projects rebuilt as illustrations,
  PERSON CREDIT with verbatim links, honesty sharpened for people) minus the
  Claude greeting and the Liam sign-off. Batch-first: `seis-profile scaffold --all` →
  `seis-profile author <slug>` × N → `seis-profile build <slug>` × N → `seis-profile ledger`. One voice
  for the series: LIAM (Kokoro am_onyx, free), in his own persona, talking
  ABOUT the student in third person — "This is Liam, for SEIS." Two gates replace per-reel GATE P:
  GATE T (template — Bear signs three exemplars before the batch) and GATE F
  per reel (FACTCHECK.md against the article — real names, one source).
  `seis-profile roll` derives the ≤5-min montage for an event from finished profile.json
  records. Sibling: `seis-ai` (the unit's AI explainer — a different flow, same skin).
  Use when the user types `seis profile`, `seis spotlight`, `seis-profile
  scaffold/author/build/ledger/roll`, or points at books/seis. Never publishes.
---

# seis-profile — every student deserves a spotlight

One COE spotlight story in → one ~90–150 s reel out, on Northeastern's brand,
for SEIS's channel. 112 stories → 112 reels → one playlist. The skill exists so
the 112th reel is as careful as the first: the arc, the laws, the gates and the
paperwork are fixed; only the person changes.

## Lineage — what governs when

- **People-laws** → `../ai-explainer/SKILL.md` § *The `profile` modifier*, rules
  2–7 (name recurs · Teardown-warm-on-their-side → here "Spotlight" · find the ONE
  idea · evidence beats are PROJECTS rebuilt, never headshots · PERSON CREDIT card
  · honesty sharpened for people). Rule 1 (the `Profile, [Name]` Claude greeting)
  and the IN-FOR-BEAR sign-off do NOT apply — this is an institutional channel
  with LIAM as narrator: he names himself once in B00 ("This is Liam, for SEIS")
  and signs off in BOUT ("Liam, for SEIS") — the channel-convert org-greeting
  pattern, not "in for Bear" (Bear is not the host here).
- **House laws that still bind** → REBUILD LAW, SHOW-DON'T-TELL, EXECUTIVE-SUMMARY
  LAW (B01 = the BLUF), DOUBLE-CHECK LAW, FILL-THE-CANVAS / TYPESIZE, VISUAL QC LAW,
  DOODLE-BANNED. LOGO LAW is satisfied by the unit name set in type until the
  official lockup exists (see CONFIRMS).
- **Brand** → `brands/neu.md` (laws — if absent in this tree, the NEU laws live in `runtime/remotion/src/tokens/neu.ts` + `docs/`) + `brands/seis.md`
  (deltas). Red is brand, never state. Lato only. White ground only. Every asset
  contains red (each Seis scene carries the one red rule).
- **Pacing** → `../duration-planner/`: duration is an OUTPUT. A thin article makes
  a 70 s reel; a dense one 150 s. Never pad a person's story to a target.
- **Authoring exit** → `../nopunt/SKILL.md`: every beat SHOW / HOLD / CARD, no
  PUNT. CHECKS-REPORT.md before the first compile.
- **Not** `ogilvy`'s "never batch": that rule guards a critique of one person's
  work. A spotlight celebrates; batching is the point.

## Inputs

`books/seis/<slug>/` as the scraper wrote it — `story.md` (frontmatter + body),
`meta.json` (title, date, url, image_details), `story.html`, images. The article
is the ONLY source for facts about the person. Not LinkedIn, not GitHub, not a
web search, not memory. If the article doesn't say it, the reel doesn't say it.

## Verbs

```
seis-profile scaffold <slug> | --all      # deterministic, no LLM, no spend (runtime/scripts/seis_profile.py)
seis-profile author <slug>                # the LLM pass — profile.json → narration → shots → FACTCHECK → CHECKS-REPORT
seis-profile build <slug>                 # kokoro audio → ART_PALETTE=neu render → compile → visual QC (free)
seis-profile ledger                       # books/seis/youtube/REVIEW.md — stage per reel, unconfirmed items
seis-profile roll <event-brief>           # ≤5-min montage from finished profile.json records (see § roll)
```

### `seis-profile scaffold` (done for all 112 on 2026-09-15)
Writes `books/seis/youtube/seis-<slug>/`: `beat_sheet.json` (NEU metadata, the
bookends with real props from meta.json, six body slate beats), `profile.json`
(all-null extraction record), `SOURCES.md`, `RIGHTS.md` (photo row: CONFIRM),
`FACTCHECK.md` (header, unsigned), `SHOTLIST.md`, `PROMPTS.md`, `BUILD-PROMPT.md`;
copies the hero image to `runtime/remotion/public/seis/<slug>.<ext>` so
`SeisSpotlightOpen` can `staticFile()` it. Never overwrites an authored sheet
without `--force`.

### `seis-profile author <slug>` — the pass that makes it a spotlight
Read `story.md` end to end. Then, in this order:

1. **profile.json.** Fill every field by paraphrase from the article; `null`
   when absent; `public_links` VERBATIM (`linkedin.com/in/…`) and only if the
   article prints them; `faculty_named` / `employers_named` exactly as spelled.
   `status` ∈ {student, alum}; `term` as the article states it ("Spring 2027",
   "MS'25"). `theme_tags` from: AI-ML · cybersecurity · networking · systems ·
   data-analytics · software-engineering · product · career-transition · co-op ·
   research · healthcare · sustainability.
2. **The ONE idea.** Every article has a thesis sentence (Donde: "technology is
   most powerful when it is applied with purpose"). Write it as ≤ 12 words in
   sentence case. It is B01, it is BVDT, it is the reel's spine.
3. **Trim the arc.** Six body slates are a maximum. Delete `B06 human` if the
   article gives no personal detail; merge `project-2` into `project-1` if there's
   one project. Keep ids; never renumber.
4. **SHOW first, words second.** For each surviving body beat write `shot` before
   `narration_text`:
   - `before` / `why-seis` / `next` → `SeisCard` (label = the person's name, 2–4
     lines, `emphasis` on at most one line) — CARD is legitimate here.
   - `project-*` → **always a Manim PROCESS** (`shot.type: GRAPHIC`, `source: manim`,
     `lane: manim`, a `show` event list — `source` is what beat_plan keys on) built from the three shapes in `seis_graphics.py`,
     which the scaffold copies into every reel:
       · `FlowStrip` — input → system → output boxes; `run_token()` sends a red
         dot through the path (apps, co-op work, network/telecom paths, "role →
         what they did → outcome")
       · `SchemaCard` + `link()` + `QueryLine` — tables, foreign keys drawing in,
         one query typing and lighting the join (databases, data management,
         any system with entities)
       · `DataPipeline` — messy rows snap into a table, a schematic curve draws,
         named outputs branch off (analytics, ML, forecasting)
     A scene is a `class B0N_Name(Scene)` in the reel's `scenes.py`, timed from
     `beat_dur("B0N")` so it fills the measured narration. Something is always
     MOVING while Liam talks — a beat that would be a still card here is a PUNT.
     Never a screenshot, never a stock "coding" shot. If the article names an
     outcome ("50 enterprise clients") the number lands ON the graphic; if it
     names none, the axes carry no units. A genuinely new shape gets added to
     `runtime/manim/seis_graphics.py` (then it's there for the next reel), not
     hand-rolled in one scene. Pango drops some single spaces on this Mac —
     write a double space at the boundary it eats (`"route  optimization"`).
   - **Second-still rule** (18 of 112 articles print a 2nd image): a second still
     is allowed ONLY if the article printed it AND it depicts the work (a
     screenshot, a demo) — never the person — and it rides alongside the
     rebuild, never instead of it. Courtesy photos of the student are out.
   - `human` → `SeisCard` or a Manim motif that respects the person (a dance
     posture drawn as a line, not a stock photo).
5. **Narration — Spotlight register.** Third person, sentence case, 35–60 words
   per body beat, ~8–12 s each. Warm, specific, honest: say what they built and
   why it mattered in the article's own scope. No superlatives the article didn't
   use; no "incredible", "amazing", "passionate" unless quoted. B00 narration
   opens "This is Liam, for SEIS." then names them and their program in the
   same breath; BVDT restates the ONE idea
   with their name; BHTF reads "Read the full story on the College of Engineering
   site"; BOUT: "SEIS student spotlights. Northeastern University, College of
   Engineering. Liam, for SEIS." Liam never says "we" and never speaks for the unit.
6. **Bookend props.** B00: `name`, `program`, `term`, `eyebrow` ("Student
   spotlight" / "Alumni spotlight"). BHTF: `name`, `role`, `links` (verbatim or
   `[]`), `storyUrl`/`storyDate` already set. BOUT: `handle` stays `""` until
   confirmed (the ledger flags it).
7. **FACTCHECK.md.** One row per claim the viewer hears or reads — names,
   employers, courses, faculty, numbers, dates, degrees — Source = the paragraph
   of `story.md`. Sign it: `Status: **GATE F SIGNED — <date> by Claude Code
   (author pass); Bear countersigns exemplars.**` A claim you cannot trace gets
   cut from the narration, not softened.
8. **SHOTLIST.md + CHECKS-REPORT.md** per nopunt. Remove every `_todo`.

### `seis-profile build <slug>` (free, local)
```
python3 runtime/scripts/generate_audio_kokoro.py <reel>        # bm_fable, one voice for the series
ART_PALETTE=neu bash runtime/scripts/run.sh <reel> --height 1080   # Manim fragments + Remotion scenes + compile, gates on
python3 runtime/qc/type_check.py <reel>                          # Lato / min-size / contrast (NEU brand check rides here)
```
Gate F blocks on an unsigned FACTCHECK — that is the point. `ART_FACTS=0` is for a
previz only and never for a cut that leaves the machine. The master is
`./art final <reel>`. **Never publish** — the batch hands SEIS a folder of
masters plus REVIEW.md; upload is theirs.

### `seis-profile ledger`
`REVIEW.md`: stage per reel (SCAFFOLD → AUTHORED → AUDIO → RENDERED → MASTER),
narration/audio/media counts, Gate F, and the unconfirmed items. Run it after
every batch step; it is the report Bear reads instead of 112 folders.

## What the rest of Brutalist gives this skill (use it, don't rebuild it)

| Tool | Where | What it does for the batch |
|---|---|---|
| `scene_search.py` | `runtime/scripts/` | **Ask before authoring a project beat.** 480+ compositions; a schema / pipeline / data-flow scene may already exist. A miss logs to TEMPLATE-MISSES.md and becomes a SEIS component, then it's in the library for the next 111 |
| `todo.py` | `runtime/scripts/` | Per-reel beat ledger (`todo.json` + `STATUS.md`) — which slots still need filling and by whom. `seis-profile ledger` is the batch view; `todo.py` is the per-reel drill-down |
| `repoloop.py` + `REPOLOOP-PROMPT.md` | root | **The crank.** Resumable, serial, sandboxed film factory: one episode per invocation, never signs, never spends, never publishes. Authoring 112 reels unattended = a repoloop task list of `seis-profile author <slug>` with the exemplar as reference DATA — after GATE T |
| `audit_review_queue.py` → `write_review_queue_report.py` | `runtime/scripts/` | Read-only audit of a finished queue: source routing, master probes, contact sheets of distributed frames per film. This is how Bear reviews 112 masters without watching 4 hours — run it before the hand-off |
| `shorts.py` | `runtime/scripts/` | 9:16 Short from each reel (< 3:00, cuts whole beats, protects hook/hero/outro). SEIS is on Instagram (`@nu_seis`) — every spotlight gets a Short. Needs `*916` variants of the four Seis scenes (21 other 916 scenes exist as the pattern) — **pending** |
| `logo-motion` skill | `skills/make/logo-motion/` | 4–8 s animated sting from a mark (potrace + Remotion, free). Candidate: the official notched-N as the open/close sting once SEIS approves motion on the mark — NU brand law governs; the static mark is the default until then |
| `explainer` VOX grammar | `skills/make/explainer/` | Ken Burns / cutout springs for stills. Applies to B00's hero photo and a qualifying second still (see the second-still rule) (VOX LAW: a still only where it IS the evidence — the person, in a spotlight of the person). No duotone, no cutout — NEU imagery law: the photo stays as published |
| `duration-planner` · `nopunt` · `your-turn` | `skills/make/` | Inherited doctrine (see Lineage) |
| `fellows` / `guests` + `screen-clean` | `skills/make/` | If a student later supplies their own video, the report-plays-as-is grammar wraps it — a `seis-profile` reel becomes the frame |
| `brand_variant.py <reel> seis` | `runtime/scripts/` | Forks any EXISTING reel (e.g. a Bear-channel profile) onto the SEIS skin as `beat_sheet.seis.json` — the base is never touched |

### Hero-photo upscale (Topaz, optional, gated)
**Default: ship the native 600×400.** At 1080p the photo panel is ~576 px wide, so no upscale
is needed; only a 4K master benefits, and one soft photo panel is acceptable.

The CLI (`tpai --cli --upscale --output <dir> <image>`) reaches 2400×1600 in seconds but is
**faces-only**: its switches are `--upscale --noise --sharpen --lighting --color` — there is
no text flag. It inherits the app's Autopilot prefs (`autopilotTextModel`,
`autopilotTextStrength`), but Autopilot never enabled Text Recovery on any probed hero
(checked 2026-09-15, 8 of 112), and the app's Preserve Text is mask-driven (`textMaskBrush`),
which a CLI cannot paint. Result on the Donde hero: clean face, banner text rewritten into
pseudo-letters. The `scale=N` override errors in 4.0.4.

If 4K heroes matter: batch the 112 `image-01.*` through the **Photo AI app** once (Autopilot +
Preserve Text, export to a sibling folder, drop into `public/seis/` by filename) — one human
pass. An upscaled photo is no longer "as published": log it in RIGHTS.md either way.

## Gates — how 112 reels stay honest without 112 sign-offs

- **GATE T (template).** Before any batch authoring, Bear signs THREE exemplars
  that span the story shapes: a current student with projects (Donde), an alum
  with a job (Shete), a career-changer (bridge program). Signing the three signs
  the template: arc, register, card grammar, credit card. Reels 4–112 follow it
  without per-reel GATE P — Kokoro is free, so there is no spend to gate.
- **GATE F (per reel, machine-checked).** `factcheck_check.py` blocks an unsigned
  or half-written table. Real names on a university channel — this gate is
  stricter here, not looser: the Source column names the paragraph.
- **GATE R (rights, batch-level).** `RIGHTS.md` per reel; the ledger's
  `photo_rights` stays unconfirmed until SEIS says the LinkedIn-sourced photos may
  be re-used on video. Until then reels build with the photo (it's the previz)
  but the ledger says CONFIRM in every row.
- **Visual QC** per reel as the family requires (frame-level, Lato, contrast).

## CONFIRMS — asked of SEIS (Erin Macri), tracked in `_confirm`

| Item | Why it's not ours to decide |
|---|---|
| `youtube_handle` | SEIS's channel; the outro and `channel_title` read it. Known socials: `@nu_seis` (LinkedIn, Instagram), `@northeastern.seis` (Facebook) — from the SEIS announcement card |
| `logo_lockup` | NU brand law forbids re-drawing the wordmark — drop the official files in `logos/seis/` (see brands/seis.md § Logo). Until then the unit name is set in Lato as text, not as a mark |
| `photo_rights` | Photos credited "sourced from LinkedIn" are the student's; the article's consent may not cover video |

## `seis-profile roll` — the event montage (secondary)

For a brief like "≤5 min, student stories, event on Sept 29": read every
finished `profile.json`, pick 5–7 full-beat students for THEME DIVERSITY (not
seniority — one AI-ML, one cyber/networking, one career-changer, one co-op, one
research, one human-detail story), lift their B01 + one project beat + BVDT
as-is from the built reels (already rendered, already fact-checked), and add ONE
`SeisCard`-family stat beat — "112 stories · N programs · M employers" computed
from the records, nothing invented — plus a wall of the 112 open cards as a
single beat (the one place scale, not a person, is the evidence). Same
bookends, same voice. Output: `books/seis/youtube/seis-roll-<event>/`. It is an
edit of finished reels, never a re-authoring — which is why the per-reel batch
comes first.

## Hard rules (in addition to the inherited laws)

1. **One source.** The article. Anything else about the person is out.
2. **No Claude UI.** No composer, no spark, no `@NikBearBrown`, no mascot, no
   jingle. Northeastern's channel, Northeastern's outro (OUTRO-LOCK scope).
3. **One voice.** Liam, `am_onyx`, across the series — in persona, third person
   about the student. ElevenLabs only by explicit per-batch request
   (`ELEVENLABS_VOICE_LIAM`).
4. **The photo appears once** (B00, as published, credited). Everything else is
   rebuilt.
5. **Regular-weight headings, sentence case, red as the one accent** — the NEU
   brand check is part of visual QC, not an afterthought.
6. **Never publish.** Not to SEIS's channel, not to Bear's. Masters + REVIEW.md
   are the hand-off.
