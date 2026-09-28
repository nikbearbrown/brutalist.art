---
name: show-tell
description: >
  Build a SHOW-TELL film: very simple, direct explanations where every beat is
  ONE drawn isometric illustration in the Claude palette (cream stage, warm ink,
  terracotta tape) or, optionally, one stop-motion interface card from the
  ShowTellCard family (16 kinds), with a few words of label at most, and Liam's voiceover
  carrying the explanation. Liam, in for Bear, narrates by default (Kokoro
  `am_onyx`, free). One scene per beat, drawn in Manim from a shared
  isometric kit (boxes, MCP blocks, skill pages, servers, conveyors, dashboards).
  Fixed bookends (Bear, 2026-09-26): BIDEA hesitant writer first (greeting +
  the naive question corrected), BDEFS key terms second (ClaudeDefinitions, as
  in tldr), the drawn body, BHTF Your Turn in the Claude.ai composer
  (ClaudeComposerAsk), and the spoken @NikBearBrown outro. No verdict card.
  Use when the user types `show-tell` or `show tell` (+ a paste, URL or topic),
  asks for an explainer "with an image every beat", "minimal text, the voice
  explains", or for an isometric or illustrated product or announcement
  explainer. No length cap: as long as the idea needs and not a second
  longer, to the point, no filler. Never publishes.
---

# show-tell — the image shows, the voice tells

Style named and set by Bear, 2026-09-26, in his words: *"make an explainer in a
new style that I call show-tell focused on very simple direct explanations and
with images every beat needs an image ... minimal text ... the voice over
explains"*, and *"make show-tell a new skill using drawn isometric illustrations
in the Claude palette default to the Liam voice over"*. His reference was the
launch animation for Claude's plugin portal: cardboard boxes, dark MCP blocks,
a conveyor with gates, a usage dashboard, and a big counter.

First film, and the worked example to copy:
`anthropics/youtube/show-tell-claude-plugin-portal/` (87 s, nine beats plus the outro).

## Lineage

This skill extends `../ai-explainer/`. Its laws hold (IN-FOR-BEAR, FACT-CHECK,
VISUAL QC, GATE T, OUTRO-LOCK, never publish), except where this file drops
them. The bookends are the house ones, set by Bear on 2026-09-26 after the
first cut: *"add hesitant writer as the first beat and key terms like tldr uses
as the second, the 'Your turn' should still mimic the Claude.ai interface like
the all do."*

- **BIDEA**, first beat: `BrutalistHesitantWriter`. Liam's greeting is spoken
  over it (`Hallo. This is Liam, in for Bear. …`). The writer types the naive
  question and corrects one phrase into the real one (`triggerWords` →
  `replacementWords`; the trigger must appear verbatim in `text`). Add
  `lead_silence_s: 0.8` and `qc.sparse_by_design` with a reason.
- **BDEFS**, second beat: `ClaudeDefinitions`, "Terms In This Film", 2–4 terms
  with one line each. Set `durationSeconds` to the measured audio.
- **BHTF**, Your Turn: `ClaudeComposerAsk`, the Claude.ai composer, with
  `greeting: "Your turn."`, a topic containing "YOUR TURN", and the prompt read
  in full. The two `output` lines are the viewer's own checks.
- **BOUT**: `ClaudeTitleOutro`, `kind: "outro_voice"`, a 1.0 s tail. Liam reads
  the title, then "At Nik Bear Brown" (no jingle). Never exempt.
- Dropped: the composer cold open and the verdict card. Declare
  `metadata.bookend_exempt: ["cold-open","bvdt"]` with a
  `bookend_exempt_reason`; `bookend_check.py` passes it.
- The BODY is drawings. Isometric Manim is the default; a beat MAY instead
  use one card from the optional `ShowTellCard` family (see **Card family**).
  No other Remotion text cards between BDEFS and BHTF.

## The laws

1. **ONE IMAGE PER BEAT.** Each beat is one scene, and each scene is one
   drawing that changes as the voice speaks. Never a text slide, a bullet list,
   or a card of words. The picture is an isometric Manim drawing by default.
   A `ShowTellCard` replaces it only when the beat passes the card test (see
   **Card family**), never for variety.
2. **THE VOICE EXPLAINS.** Narration carries every idea. On screen, labels only:
   one to three words, at most two or three per beat (`plugin`, `MCP`, `skill`,
   `GitHub repo`, `Submit`). The one exception is a single hero number (`110×`),
   which may be large.
3. **SIMPLE AND DIRECT.** One idea per beat, in plain words. Say what a term is
   in the same breath you first use it ("MCP connectors, which plug Claude into
   outside tools and data"). No jokes, no setup-and-payoff: the Teardown
   register at its plainest.
4. **SAME OBJECTS, WHOLE FILM.** Pick a small cast of objects and keep it: the
   thing (a box), its parts (blocks, pages), where it goes (a window, a
   conveyor), and what comes back (a dashboard). A viewer should recognise
   beat 8's box as beat 0's box.
5. **MOTION CARRIES THE CLAIM.** Each spoken point has a motion: parts drop in,
   a cable draws, a scan line sweeps, a box rides through gates, bars grow, a
   counter climbs. Apply the still-frame test: if a beat reads the same as a
   still, it fails.
6. **LIAM BY DEFAULT.** Kokoro `am_onyx`, channel `claude-liam`, persona
   "Liam (in for Bear)". BIDEA opens with a world-language greeting
   (`Hallo. This is Liam, in for Bear.`). Another voice only if Bear names one.
7. **YOUR TURN IS THE COMPOSER.** BHTF gives one concrete prompt the viewer
   pastes into Claude, read in full, then two checks they run themselves.
8. **ATTRIBUTE THIN NUMBERS.** A figure that exists only in a social post or a
   single source is attributed aloud ("Claude's developer team says") and
   captioned on screen ("per Claude's developer team").
9. **AS LONG AS IT NEEDS, NO LONGER.** There is no length cap and no length
   target (Bear, 2026-09-27: *"it's as long as it should be but it should just
   be to the point no bullshit"*). The content sets the length: one beat per
   step the viewer actually needs, and no more. Cut any beat that repeats,
   pads, recaps what was just shown, or exists to hit a length. Never merge or
   rush two real steps to come in shorter. If a topic needs 25 beats, it gets 25.
   If it needs 5, it gets 5.

## Spine

| beat | job | on screen |
|---|---|---|
| BIDEA | greeting + the naive question corrected | `BrutalistHesitantWriter` |
| BDEFS | the 2–4 terms the film needs | `ClaudeDefinitions` |
| B00 | the hero object | it arrives |
| B01 | what it is | the object opens and shows its parts |
| B02…Bn | how it works, one step per beat | each step is one motion on the same cast |
| Bn+1 | why now (the number, attributed) | a counter plus a curve |
| BHTF | your turn | `ClaudeComposerAsk` (the Claude.ai composer) |
| BOUT | spoken outro | `ClaudeTitleOutro` |

**Length.** Law 9 governs: no cap, no target. Count the steps the viewer needs
and give each one beat. A beat runs as long as its sentence or two takes to
say (usually 5–12 s; a beat that runs past ~15 s is usually two ideas and
should be split). The measured audio sets the film's length. For reference only:
the first films came to 1.5–2.6 min because their topics needed that much, not
because of a limit.

## Drawing kit and laws

Paste `templates/iso_kit.py` into the top of `scenes.py`. **Do not import it:
Gate A copies only `scenes.py`.** It provides:

- `Iso(ox, oy, s)`: the projection. `p(x,y,z)` gives a screen point; `v()` gives a
  vector; plus `quad`, `box`, `open_box` (returns back and front so contents sit
  between), `tape`, `mcp`, `page`, and `server` (returns stack and lights).
- `check`, `cursor`, `pill`, `T` (EB Garamond), `ease_in`.
- Pacing: `until(self, "spoken phrase")` waits for the phrase (by its share of
  the characters in the narration, times the measured audio), and `finish(self)`
  holds to the end. Class names must start with the beat id (`B03_Bundle`).

Palette: stage `#F2F0E9`, ink `#3D3929`, terracotta `#D97757`, dim `#8B8F96`,
ghost `#D9D4C7`, card `#FAF9F5`, and the cardboard, dark and page face tones in
the kit. Never retint.

**DRAWING LAWS.** These are the GATE B, T and V traps, already obeyed by the kit:

- Labels sit **beside** objects, never inside an outline, and never on a
  terracotta fill. Keep a leader line clear of its label, with at least
  0.3 units of gap.
- Terracotta only for: tape, dots, lights, one curve, a check, a scan line.
  Never terracotta text, and never a thin or short-wide terracotta bar.
- Chart blocks use `BAR1/BAR2/BAR3` greys with gaps between segments. Dark ink
  blocks packed together fuse under GATE T.
- Text size is at least 32. Every coordinate, labels included, stays inside
  ±6.2 × ±3.3. The layout audit warns past ±6.3 × ±3.4, measured on text bottoms.
- Every scene must **add** at least one new non-text shape after its first
  frame. Moving only is not enough: Gate A reads "shapes never change" as a
  repeated animation. A landing shadow or a scan line is enough.
- Don't use `rate_functions.ease_in_quad` (Gate A's stub lacks it); use the
  kit's `ease_in`. `ease_out_bounce` is fine.
- Continuity: if a scene adds something, the next scene starts with it on
  stage (e.g. `floor_shadow()` in B00 and B01).
- **Contrast (Gate V).** Gate V averages every non-background pixel, so pale
  cardboard reads as "low contrast" even when every label is dark ink. The kit
  therefore uses **kraft** faces (`#F3E9D8 / #DCC9AA / #C7AE86`) and **4 px ink
  outlines** by default; the first film's pale boxes measured 0.18–0.23 against
  a floor of 0.30. A pale UI panel (a browser window) needs a dark element to
  carry it: B04 uses a `DARK_TOP` title bar.
- **Fill (Gate V).** The canvas-fill law (content bbox ≥ 55% of the safe area)
  fights this style: one hero object on cream measures 19–50%. Show-tell body
  beats declare the gate's per-beat waiver in the sheet:
  `"qc": {"sparse_by_design": true, "sparse_reason": "…show-tell…"}`. It waives
  only underfill and clustered. Edge-bleed, empty-frame and contrast still
  apply. Leave the waiver off any beat that fills on its own, and never use it
  to hide a frame that is actually empty.
- Numerals and step markers ("1", "2") are ink, never terracotta (GATE T).
- **GATE T samples each clip at its MIDPOINT.** Whatever is half-done there
  gets judged as type:
  - a half-faded dark object reads as a faint fused text blob, so slide objects
    in fully opaque, or have them land before the midpoint;
  - a half-drawn terracotta curve reads as accent text, so draw curves in ink
    and keep terracotta for the end dot;
  - labels in `DIM` on a `CARD` panel aren't detected at all ("no text blobs"),
    so use ink.
- Don't use `rate_functions.ease_out_cubic` either (also missing from the stub).
- `mob.animate(path_arc=…)` crashes Gate A (the stub's animate proxy isn't
  callable). Use `MoveAlongPath(obj, ArcBetweenPoints(a, b))`.
- **Hesitant writer:** `triggerWords` and `replacementWords` must NOT end in
  punctuation. The component strips punctuation before matching, so a trigger
  like "the smartest agent?" never fires and the naive question ships
  uncorrected. Leave the "?" out of both.
- **Clip longer than its audio gets centre-cut.** `compile.py` trims a scene
  that runs past its beat's audio from both ends, silently (one log line),
  which drops the opening and the payoff. Keep every scene's run time within
  its `actual_duration_s` (`finish()` does this as long as the `play` calls
  fit), and ffprobe each `manim/<BID>.mp4` against its audio before the final.
- More GATE T midpoint traps: a label still fading in at the midpoint, copies
  of labels in flight, or a terracotta scan line mid-sweep all fail. Have them
  land before the midpoint or start after it. A leader line touching its label
  also fails. A polygon `Transform` (plate to slip) crumples mid-flight; move
  and scale a copy instead.
- `art run` only renders scenes whose `manim/<BID>.mp4` is missing. After
  editing a scene, move its old clip to `_superseded/` and re-run. Frame
  rounding at 4K can push a clip a few hundredths of a second past its audio,
  so leave about 0.05 s of slack.
- The "SKIN LINT: COLD OPEN LAW" line on BIDEA is advisory and expected under
  `bookend_exempt`.
- **Scene classes must be written literally as `class BNN_Name(Scene):`.**
  `run.sh` finds scenes by that exact text. A class that subclasses a helper
  is silently skipped and compiled as a placeholder, and the run still exits 0.
  Attach helpers after the class line instead.
- A stale Manim cache in `<reel>/media/videos` survives between runs and can
  push re-renders 1–4 frames past the audio. Move it to `_superseded/` along
  with the old clips before re-rendering.
- More GATE T traps: an ink-outlined card loose inside an ink-outlined
  container reads as overlapping text (give contents grey outlines); a
  midpoint frame with NO type fails (every drawn beat needs a label up by its
  midpoint); a short leader line reads as sub-floor text; a short terracotta
  tape stripe on a small crate reads as accent text.
- A midpoint guard pattern (see `show-tell-context-is-a-budget/scenes.py`,
  `ST`/`guard`) holds every animation off the clip midpoint, where GATE T and
  Gate V sample. Run the guard before placing anything off-stage. Give it a
  margin of about 0.22 s, because frame rounding beats a 0.06–0.08 s margin.
- Kokoro reads "plugin.json" as "plugin. JSON". Write "plugin dot json" in
  the narration and keep `plugin.json` in on-screen text and prompts.
- Small ink-outlined objects with ticks (dials under about radius 1) fuse
  into one "text" blob that encloses their pointer and fails GATE T §8.6b.
  Outline small objects in dark kraft (`#917A55`), and keep cables and leader
  lines from touching dark blocks, whose faces sit inside GATE T's ink
  tolerance.
- Kokoro misreads version numbers and acronyms. Spell them out in the
  narration ("five point five", "X S S") and check with a whisper transcript.
- **Greetings:** Kokoro voices "Hej" as "hedge" and "passkey" as "pass-ski",
  and `generate_audio_kokoro.py` has no pronunciation override. Pick a
  greeting Kokoro says cleanly, or re-voice it from phonemes (see
  `show-tell-claude-on-your-desk/tts_greeting_fix.py`), and whisper-check the
  first beat every time. "Olá" comes out as "Allah" (re-voiced as oh-LAH in
  `show-tell-one-plugin-per-service/`). Greetings that have come out clean:
  Hallo, Bonjour, Hola, Ciao, Konnichiwa, Namaste, Salaam.
- Parallel `manim` renders that share one media dir collide on the Text
  cache. Give each scratch render its own `--media_dir`.
- The dark-kraft outline (`#917A55`, grey 117) is only for SMALL objects.
  GATE T's light-frame contrast check counts any pixel with grey below 120
  as text, so a large object outlined in it fails. Large objects keep ink
  outlines.
- Kokoro swallows the "A" in a spelled-out "A P I" ("PI key"). Plain "API"
  is voiced correctly, so check each acronym with whisper rather than
  spelling them all out.
- Gate A's stub returns plain lists from `get_center()`. Wrap them in
  `np.array(...)` before subtracting.
- GATE T reads a thin ink outline along a long diagonal edge, or grey dashes
  on a pale belt, as small low-contrast text. Give belt edges dark kraft and
  make the centre dashes pale ghost grey.
- `generate_audio_kokoro.py` re-voices EVERY beat on each run unless you pass
  `--only`, which silently drops BOUT's 1.0 s pad. Use `--only <BID>` for
  re-voices, and re-pad and re-measure BOUT after any full run.
- The kit's `DARK_R` face (30,27,24) sits within GATE T's ink tolerance of
  INK. A dense lattice of dark blocks (a tool wall) breaks into false "text"
  blobs under codec noise. Make large dark walls darker, or space the blocks
  apart.
- A slanted terracotta tape band on a box can fail GATE T contrast as
  accent text. If it does, use a grey strap with one spark-sized terracotta
  seal.
- Pipes or cables edged in ink join the objects they connect into one wide
  "text" blob, and GATE T then fails anything drawn inside it. Edge
  connectors in deep kraft (`#9C8462`).
- Keep references to the objects on screen. `FadeOut` of a NEW copy of a
  label leaves the original on screen; two builders hit this.
- Keep terracotta sparks inside a block's top face. A spark crossing the
  corner outline leaves a small ink fragment under the GATE T size floor.
- Cards fanned along a diagonal have overlapping bounding boxes, which GATE T
  reads as stacked labels. Line them up in a row. Small tabs inside ink cards
  take grey outlines.
- A pale kraft block on its own fails Gate V contrast; set it on a dark
  plinth.
- A dark header band inside an ink-outlined card reads as two overlapping
  labels under GATE T. Make the band grey (`BAR1`).
- Gate V counts any surface more than 28 per channel away from the stage as
  ink. Darkening a pale belt LOWERS the contrast average, so keep belts and
  pads within 28 of the stage, and carry contrast with small dark parts
  (ports, lamps).
- Tiny icons (keys, locks) outlined in dark kraft read as sub-floor text.
  Draw them larger, with ink outlines.
- A beam or highlight that fades out after a guarded move can still be on
  screen at the midpoint. Guard the move AND the fade as one span.
- `MoveAlongPath` and `.animate` on the same object in one `play` silently
  cancels the move. Split them into two plays, or animate a wrapper group.
- **`ClaudeDefinitions` truncates a term longer than about 17 characters**
  with an ellipsis, and no gate catches it. Keep terms short
  ("reference repo", not "reference implementation") and look at the BDEFS
  late frame.
- Gate A's stub measures object centres differently from Manim, and treats a
  group slice as a plain list. Write camera and rig positions as fixed
  numbers, and wrap slices explicitly in `VGroup(*…)`.
- Don't re-run `make_sheet.py` after the final: it wipes the build stamps in
  `beat_sheet.json`, and a plain `art run` restores them as `cut: review`,
  which `art post` refuses ("need master or final"). If it happens, re-run
  `art final` (nothing re-renders; the master comes out byte-identical).
- `factcheck_check.py` is in `runtime/qc/`; `bookend_check.py` is in
  `runtime/scripts/`.
- `bookend_check.py` lives in `runtime/scripts/`, not `runtime/qc/`. Gate F
  runs at `art run`, so write the paperwork before the first run.
- Lines drawn on pages that sit inside an ink-outlined tray cut each page's
  thin outline loose from the tray, and GATE T §8.6b then reads each page as a
  stacked label. Put maps and paths BESIDE the tray, not on its pages
  (`show-tell-what-is-claude-code`, B07 and B09).
- A kraft card with an ink outline parked over a dark terminal fails GATE T's
  per-blob contrast. Keep light cards off dark panels.
- `Indicate` on one part of a group brings that part to the front, where it
  covers the other parts at the same z-index (it hid a page's grey lines).
  Indicate the whole group.
- A beat whose only new shape is created, moved and then removed can still
  fail Gate A with "shapes never change". The stub snapshots only after each
  `play` and ignores moves, and with no beat sheet its first snapshot already
  holds the new shape. Add a membership change after the first play (a ring
  that grows, then fades) (`show-tell-choosing-the-right-claude-model`, B06).
- Kokoro fuses "four Claude models" into "foreclawed". Whisper-check any
  number spoken right before "Claude" and reword if it fuses.

## Card family — optional (Bear, 2026-09-27)

Bear, 2026-09-27: *"keep all typography and colors but add more stop motion
cards beyond just the isometric graphics ... the skill should never force but
more choices can add"*, then: *"the ability to use these new cards only if they
actually make sense no using a card just for using a card"*. So the cards are a
**menu, not a quota**. The drawing is the default for every beat, and a film
with zero cards is a normal, complete show-tell film.

**THE CARD TEST.** A beat gets a card only if all three answers are yes:
1. **Is the idea itself an interface, a set of numbers, or one word?** (A
   search really returning results; a real metric; a real trend; a name.) An
   idea that is a thing, a part or a flow is a drawing.
2. **Is the card's motion the beat's claim?** The voice could point at the
   motion and say "that's what I mean": results arriving IS "you ask, it
   returns"; bars melting into a line IS "same numbers, different shape".
3. **Does it beat a drawing of the film's own cast?** If the box, blocks and
   pages can show it as clearly, draw it.

Any "no" means a drawing. Never use a card for variety, to show off the family,
to fill a beat, or because a drawing is harder to make. Numbers on a card must
be real (fact-checked like any other claim), never placeholder data dressed up
as evidence. Write the reason for each card in SHOTLIST.md (a "why a card"
column), so a reviewer can check it against the test. (The one film that is ABOUT
the cards, `claude-liam-brutalist-show-tell-cards`, uses eight because the cards
are its subject. Don't copy its ratio.)

One Remotion composition, `ShowTellCard`
(`runtime/remotion/src/scenes/ShowTellCard.tsx`), with one `kind` per beat.
Each card fills the frame, uses the same palette and fonts as the drawings
(cream stage, warm ink, kraft, one terracotta accent that is never text; EB
Garamond words, UI-sans chrome, mono numbers), and is shot **on twos**: every
drawing is held for two frames, with a solid kraft offset under each card for
a paper cut-out look. No blur, no gradients.

| kind | the motion | use it when the voice says |
|---|---|---|
| `player` | a pill button grows into a video player; the scrubber runs | "press play", something opens into media |
| `search` | a query types, then results drop in one by one | finding, retrieval, "you ask, it returns" |
| `workspace` | a small card expands into a full workspace | a tool opens up, "this is where you work" |
| `tabs` | the tab pill slides; one panel leaves, the next arrives | switching views, compare A then B |
| `chart` | bars grow, then melt into a line with a value tag | a trend, "the same numbers, a different shape" |
| `dashboard` | the camera zooms onto one metric; the number counts up | the one number that matters (`word`) |
| `stack` | cards spring in from below, fan, settle; the top one is chosen | options, choosing one of several |
| `dock` | a cursor path sweeps a dock; icons swell under it | a toolbox, a set of tools, hovering the one you need |
| `masked` | a big word fills from below inside its own outline | a name, a title, a single key word (`word`) |
| `elastic` | letters stretch on a wave, then settle | flexibility, "it bends to fit" (`word`) |
| `layout` | a loose headline snaps into a laid-out page | raw text becomes a finished page |
| `reveal` | dark shutters open strip by strip onto the picture | a reveal, the hidden thing |
| `perspective` | one page tilts into a 3-D stack of pages | many versions, drafts, layers |
| `focus` | a lens slides down a report row by row | reading a table, finding the one row (`focus`) |
| `paths` | edges draw between nodes, then dots flow along them | a pipeline, a workflow, "this feeds that" |
| `particles` | scattered dots assemble into a mark (`bitmap`) | many parts become one thing |

**Props** (all optional; defaults are a neutral demo): `kind`, `heading`,
`sub`, `word`, `items` / `items2` (`{label, value, sub}` rows), `labels`,
`values`, `bitmap` (rows of `#` and `.`), `focus`, `cues` (optional move times as fractions of the beat, for `focus` and `tabs`: compute them from the narration so the card moves on the spoken word, and keep every move out of the 45–55% window GATE T samples), `onTwos` (default true),
`durationSeconds` (the measured audio; the composition sizes itself from it).
Each kind finishes its motion by about 70% and holds, so the voice lands on a
finished picture. Type is on screen and settled by 45%, the frame GATE T samples.

**Card laws.** The show-tell laws still hold, and the card test comes first.
Labels stay at 1–3 words, and data rows are the only longer text. Cards are the
exception in a body, not the rule: if more than a third of the body beats are
cards, re-check each against the test. Reuse the film's cast: if the film's
object is a box, the `search` results are those boxes. Never put a card
back-to-back with a card of the same kind.

**Beat sheet.** A card beat is `lane: "card"`, `shot.type: "REMOTION"`,
`shot.remotion.pattern: "ShowTellCard"`, `shot.remotion.props: {kind, …,
durationSeconds}`, built with the same `remotion()` helper as BDEFS in
`make_sheet.py`. Write `durationSeconds` from `actual_duration_s` after audio. Render only via
`runtime/scripts/remotion_scenes.py`. Test a kind first with
`npx remotion still src/index.ts ShowTellCard out.png --frame=<n> --props='{"kind":"chart"}'`
at 25%, 50% and 95% of its frames, and look at the stills.

**Card sizes that pass GATE T at 4K:** body text ≥ 48 design px, headings ≥ 50,
chips ≥ 32; headings in ink, never terracotta.

**Gate traps from the first card film (2026-09-27):** (1) a card whose picture is
mid-move at 50% gets flagged; `focus` now snaps row to row and holds, and
`stack` settles by 44%. Keep that rule if you add a kind. (2) A tight stack
underfills in Gate V, so cards fan out side by side. (3) In a DRAWN beat, a large
near-black field (a film strip, a dark panel) reads as one giant ink "text" blob
in GATE T §8.6b, and pale kraft fails Gate V contrast (0.30). Use `DIM` grey for
big backing shapes. (4) `make_sheet.py` must carry `audio_file` forward, as well as
`actual_duration_s`, or `art run` refuses with "missing required audio".

## Workflow (run from `books/`)

1. **Source + facts.** Read the source and save it (or its URL) in
   `SOURCES.md`. List every claim in `FACTCHECK.md`
   (`| # | Beat | Claim | Verdict | Source | Fix |`, verdicts PASS, CORRECTED
   or EXEMPT). Write `SHOTLIST.md`, and a `PROMPTS.md` that says "no generation
   prompts". Gate F refuses to render without all three.
2. **Sheet.** Write `make_sheet.py` (copy `reference/example-make_sheet.py`):
   the three bookends use the `remotion()` helper, and every body beat has
   `lane: "manim"` and `shot.manim.class`; metadata sets
   `skill`/`style_preset: "show-tell"`, `channel: "claude-liam"`,
   `bookend_exempt`, `playlist`, and `tags`. Run it.
3. **Audio.** Run `python3 brutalist.art/runtime/scripts/generate_audio_kokoro.py <reel>`,
   then pad BOUT with a 1.0 s silent tail. Write the ffprobe durations back
   to `actual_duration_s`.
4. **Stills first.** Render each scene's last frame at low resolution
   (`manim -ql -s`) into the scratchpad and look at a contact sheet before any
   4K render.
5. **Pre-audit** Gate A from a scratch folder holding ONLY `scenes.py` (copy nothing else),
   because that is exactly what `art run`'s Gate A sees. With `beat_sheet.json` beside it,
   `until()` pacing runs and a scene can pass locally, then fail inside `art run` with "shapes
   never change" (2026-09-27, two scenes). Run
   `runtime/qc/static_scene_check.py scenes.py --class <C>` there, and
   `runtime/qc/manim_layout_audit.py scenes.py --class <C> --curve-strict` in the reel folder.
   Every scene needs at least one NEW shape (Create/GrowFromCenter/FadeIn of a new object);
   moves, fills and Transform don't count.
6. **Render.** `./brutalist.art/art run <reel> --height 2160` (Gates A, B, V
   and the review cut), then look at frames. Then
   `./brutalist.art/art final <reel> --height 2160 --out <reel>/exports/landscape`
   (GATE T, then the master). Check the master: sha, 3840×2160, silent tail.
7. **STOP.** Send Bear the master. Stage (`art post`) and publish only on his
   word, and only from TOPOST.
