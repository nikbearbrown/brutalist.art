---
name: seis-ai
description: >
  Build the SEIS (Software Engineering and Information Systems, Northeastern
  COE) unit explainer on AI — "SEIS & the future of AI": the unit's AI
  offerings, initiatives and student work, forward-looking but evidenced, ≤5 min
  for an event or the channel. NOT a profile and NOT a batch — one reel, built
  from a CORPUS the skill assembles first (SEIS program/course pages, the
  unit's brief, and the AI-tagged records the seis-profile batch produced), on
  the NEU skin (brands/seis.md) with the SEIS bookends, no Claude UI. Register:
  Spotlight-institutional (sentence case, no hype, every forward-looking line
  ATTRIBUTED to SEIS, never asserted by the narrator). Gates: GATE C (corpus
  signed — nothing about the unit is said that a listed source doesn't say),
  GATE P (Bear signs narration on an animated slate; Erin countersigns the
  facts), GATE F, NEU brand check. Sibling of seis-profile — different flow,
  one skin, one voice (Liam, Kokoro am_onyx, in persona). Use when the user types `seis ai`,
  `seis-ai`, `SEIS and AI`, `SEIS future of AI`, or hands over an event brief
  about the unit's AI work. Never publishes.
---

# seis-ai — the unit's own AI story, evidenced

`seis-profile` is 112 reels about people. `seis-ai` is ONE reel about the unit —
what SEIS teaches, builds and plans in AI — and the difference in flow is the
difference between a story you are handed and a story you have to assemble. A
profile has one source. This reel has a corpus, and the corpus is the first
gate, because the fastest way to embarrass a unit on its own channel is a
forward-looking claim nobody in the unit actually made.

## Lineage

- **Skin, voice, bookends, laws** → `brands/seis.md` (NEU palette + laws, Lato,
  red as brand only), `../seis-profile/SKILL.md` § Hard rules 2–6 apply verbatim
  (no Claude UI, one voice, never publish, NEU brand check in visual QC).
- **Authoring doctrine** → `../explainer/` doctrine (SHOW first; MOTION.md, the slot contract) with register overridden to Spotlight-institutional;
  `../nopunt/` exit conditions; `../duration-planner/` — here the brief's cap
  (≤5:00) is a hard CONSTRAINT, still not a target: a 3:40 reel that says only
  true things beats a 4:58 reel that pads.
- **Not** `seis-profile`'s people-laws (no ONE-idea-per-person, no PERSON CREDIT)
  and **not** `ai-explainer`'s ASK→RESULT (the Claude UI is not the subject —
  ILLUSTRATE LAW).

## Flow

### Step 0 — The brief
Write `BRIEF.md` in `books/seis/youtube/seis-ai-<slug>/`: who asked, the event
or channel slot, the hard cap, the audience (the Sept 29 "Evolution of SEIS"
room: faculty, leadership, students, hybrid), and the requested ANGLE in the
requester's own words (Erin: "how SEIS is positioning itself as a leader in AI
education and innovation, while looking ahead"). The angle is a request, not a
fact — the reel earns it or narrows it.

### Step 1 — CORPUS.md (GATE C)
Assemble every source the reel may draw on, one row each: URL / file, what it
establishes, date, who wrote it. Three tiers:

| Tier | Source | What it may support |
|---|---|---|
| A — the unit speaks | SEIS/COE program + course pages (`coe.northeastern.edu/…/seis/`), the MGEN→SEIS announcement, materials Erin supplies (offerings list, initiatives, faculty AI work), leadership quotes she signs | Offerings, initiatives, plans, "positioning" — the ONLY tier that may carry a forward-looking line, and only as ATTRIBUTED speech ("SEIS says / plans / is building") |
| B — the students' record | (1) `books/seis/youtube/*/profile.json` with `theme_tags` ∋ AI-ML (built by `seis-profile author`), each fact-checked against its article; (2) **`books/seis/HAI-FELLOWS.md`** — the Humanitarians AI fellows corpus (`books/humanitarians-youtube/fellows/`, 264 built films on @humanitariansai), usable two ways: the AGGREGATE line ("about 80% of Humanitarians AI fellows came through SEIS, formerly MGEN" — Bear's 2026-09-15 attestation, attributed) is allowed now; naming an INDIVIDUAL fellow as SEIS needs per-person confirmation (roster program column / ISE profile / COE spotlight) — otherwise they're shown as a Humanitarians AI fellow. The fellows tree itself never names a program | Evidence of AI work happening: named projects, co-ops, tools — lifted as already-rendered beats where possible. A fellow without program evidence is a *Humanitarians AI fellow*, not SEIS |
| C — context | Public numbers about the AI job market or the field, primary-sourced | ONE beat at most, and only if the brief asks for it |

Rules: a claim with no row is not made. Tier C never supports a claim about
SEIS. Bear's own courses (e.g. INFO 7375) enter only via Tier A — listed as
SEIS offerings, not as the narrator's résumé. **GATE C: Bear signs CORPUS.md
before authoring; Erin confirms the Tier A rows are current.** Missing
offerings → ask Erin, don't infer from a course catalog search.

### Step 2 — Extract the spine
From Tier A alone, write three lines in `SPINE.md`: what SEIS offers in AI
today (nouns, countable), what it is building (attributed), what it says it is
aiming at (attributed, dated). If Tier A cannot fill a line, the reel doesn't
have that act — say so in BUILD-LOG.md, don't paper over it.

### Step 3 — The arc (≤5:00 hard cap; typical landing 3:30–4:30)
| Beat | Scene | Content |
|---|---|---|
| B00 open | `SeisSpotlightOpen` (eyebrow "SEIS & the future of AI", name = the title, program = "Software Engineering and Information Systems", logo `northeastern/nu-wordmark-rh.svg`) | The unit and the question in one breath |
| B01 BLUF | `SeisCard` | The claim the reel can actually stand behind, in Tier-A words — e.g. "SEIS teaches AI across its programs and its students are shipping it on co-op" — NOT "SEIS is a leader in AI" unless a Tier A source says it, attributed |
| B02–B04 offerings | Manim under `ART_PALETTE=neu`: a MAP of programs → AI courses/concentrations, drawn as it's named; a second graphic for initiatives/labs | Countable nouns from Tier A; every program name spelled as the page spells it |
| B05–B07 student evidence | Three lifted beats from AI-tagged `seis-profile` reels (their `project` beat + the name card) — already rendered, already Gate-F'd — OR a `SeisCard` wall of N AI-tagged names computed from profile.json | The proof that the offering produces work; names on screen (people-law "name recurs" honoured even here) |
| B08 looking ahead | `SeisCard` + a Manim timeline ONLY if Tier A dates it | Attributed: "SEIS says…", "the unit plans…". The narrator never predicts |
| B09 (optional) context | one Tier C beat | Only if the brief asks |
| BVDT recap | `SeisCard` | The BLUF restated |
| BHTF handoff | `SeisProfileCredit` re-purposed (`name` = "Explore SEIS", `role` = program URL, `links` = `@nu_seis`, `@northeastern.seis`) | Where to go next — real URLs from Tier A |
| BOUT | `SeisOutro` (logo, handle `@nu_seis`) | Unit, school, series line |

### Step 4 — Narration (Spotlight-institutional)
Third person, sentence case, no superlatives without a Tier A quote, 40–70
words per body beat. **Attribution law:** every sentence about the future
carries its speaker ("the unit says", "Dean/Director X, in the announcement,
says"). Present-tense facts carry their Tier A page in FACTCHECK. The narrator
never says "we" — Liam reports what the unit says, he does not speak for it.

### Step 5 — Gates, then build
- **GATE P** on an animated slate (`ART_FACTS=0` previz allowed for this pass
  only): Bear signs the narration; Erin countersigns Tier A facts and every
  attributed line. Write the sign-off into `FACTCHECK.md`'s Status line.
- **GATE F** `factcheck_check.py` — one row per claim, Source = the CORPUS row.
- **Build** exactly as `seis-profile build`: `generate_audio_kokoro.py` (am_onyx — Liam)
  → `ART_PALETTE=neu bash runtime/scripts/run.sh <reel>` → `type_check.py` → visual
  QC → `./art final`. Cap check: the master must be ≤ 5:00 or the brief's cap.
- **Hand-off**: master + FACTCHECK.md + CORPUS.md to SEIS. Never publish.

**MGEN → SEIS rename law.** SEIS is the new name of MGEN (Multidisciplinary Graduate Engineering). Pre-rename sources say MGEN; narration says "SEIS, formerly MGEN" on first citation of such a source, then "SEIS". Quoted text is never rewritten.

## What this skill refuses
- A "leader in AI" line with no Tier A sentence behind it.
- Any student named who has no built, Gate-F'd profile reel or a Tier A mention.
- Generated B-roll of "AI" (circuits, robots, neon) — NEU imagery law + the
  toolkit's no-AI-cliché law.
- The Claude composer as a visual, even though the subject is AI.
- Padding toward the cap.
