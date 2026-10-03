---
name: lecture
description: >
  Build a LECTURE: one full-length, act-structured film of a WHOLE chapter or
  document (a full markdown file, a report, a long post). Primarily visual:
  every body beat auditions the entire Brutalist playset (Manim mechanisms and
  math, isometric drawings, ShowTellCard kinds, Remotion patterns, 2-D library
  icons, real code and terminal skins, the real app or website) and takes the
  one visual that teaches that beat best. When a beat is about a tool, an app
  or a website, the film shows that thing itself. Fixed bookends: hesitant
  writer (what the topic is about) → key terms → acts → recap → Your Turn →
  the channel's outro. Default channel @NikBearBrown (claude-liam, Liam in for
  Bear, free Kokoro am_onyx). Use when the user types `lecture`, `lecture
  <chapter | document | path | paste>`, or asks for a full-chapter film, a
  whole-document lecture, or "the whole chapter as one film". Length is an
  output; no cap. Self-contained: assumes the viewer has read none of the
  books and seen none of the other films. Audio-first; free steps run straight
  through with no approval gate (approval only before paid generation).
  Never publishes.
---

# lecture — the whole chapter, shown

Named and set by Bear, 2026-10-02, in his words: *"a skill called lecture that
takes a full chapter or full document … it starts with hesitant writer
explaining what the topic is about then it summarizes the key terms, at the end
it does a recap, a your turn and an outro depending on who is the channel … it
takes the best of all the other skills and mostly show and not tell … whatever
it takes, the best beat of everything that we have … it tries to find the
absolutely best visual beat for the topic being talked about in that beat and
uses that … it takes the entire chapter, works it out on an act structure just
like the deep explainer does, but the key difference is it's primarily visual
… it has the entire brutalist playset."* And, same day: *"when it's using a
website or a tool … it should show that tool. If it needs to make a card for
that tool, fine … it should show the thing that it's representing."*

What that makes this skill, next to its siblings:

| Sibling | Its body | `lecture` differs because |
|---|---|---|
| `deep-explainer` | a multi-act argument, 5–10 min | same act structure, but the WHOLE source is covered, there is no length band, and the lane is chosen per beat from every skill, not from three lanes |
| `tldr` | one learning SECTION per film, pure Manim | one film for the whole chapter; Manim is one lane of many |
| `show-tell` | one isometric drawing per beat | the isometric drawing is one candidate; it wins only where it is the best picture |
| `cc-explainer` | a real terminal session, start to finish | the terminal appears only in the beats that are about the terminal |

This is not the HTML lecture-deck pipeline and not a slide deck. It is a film.

## Lineage — what governs when

This skill EXTENDS `../deep-explainer/`, which extends `../ai-explainer/`, which
extends `../explainer/`. Parent laws all bind unless this file changes them.

- **Act structure, PROOF GATE, GATE L, factcheck sharpening, strip-the-datable,
  GATE T, never publish** → `../deep-explainer/SKILL.md`.
- **Brand, voice, channels table, IN-FOR-BEAR, ASK→RESULT, VISUAL QC,
  FILL-THE-CANVAS, DOODLE-BANNED** → `../ai-explainer/SKILL.md`.
- **SHOW / HOLD / CARD classification and the anti-punt catalog** →
  `../nopunt/SKILL.md`. Read it before routing a single beat.
- **Closing block** → `../your-turn/SKILL.md` (BVDT → BHTF → BOUT).
- **Each lane's own drawing laws and gate traps** → the skill that owns the
  lane (the router table below names it). A lecture borrows a lane WITH its
  laws: an isometric beat obeys show-tell's DRAWING LAWS, a Manim lesson beat
  obeys tldr's Manim laws, a Claude Code beat obeys cc-explainer's session
  fidelity laws.
- **Math** → `docs/MATH-TYPESETTING.md`. **Code and data** →
  `docs/EXECUTABLE-EVIDENCE.md`.
- **This file** governs: whole-source coverage, the opening pair, the
  BEST-BEAT LAW and its router, the SHOW-THE-THING LAW, and the channel outro.

What this file CHANGES from the parents: the composer cold open is dropped (the
film opens on the hesitant writer), and the 5–10 minute band is dropped.

## The spine (fixed)

```
BIDEA   hesitant writer   BrutalistHesitantWriter   greeting + what this topic is about
BDEFS   key terms         ClaudeDefinitions         the vocabulary the acts will use
  ACT I … ACT N           the body: one best visual per beat (this skill's subject)
BVDT    recap             ClaudeVerdictArtifact     what the chapter established
BHTF    your turn         ClaudeComposerAsk         one prompt, read in full, two checks
BOUT    outro             per channel (table below)
```

- **BIDEA.** Liam's greeting is spoken over it (`Hallo. This is Liam, in for
  Bear. …`), then what the topic is about, in two or three plain sentences. The
  writer types the framing a newcomer arrives with and corrects ONE phrase into
  the chapter's real subject (`triggerWords` → `replacementWords`; the trigger
  must appear verbatim in `text`; neither ends in punctuation, or the
  correction never fires). `lead_silence_s: 0.8`, `seed` = the slug,
  `qc.sparse_by_design` with a reason. Contract: tldr's B02 section.
- **BDEFS.** `ClaudeDefinitions`, title "Terms In This Lecture", 3–6 terms, one
  plain line each, in the order the acts need them. Only prerequisite
  vocabulary: a concept the lecture exists to earn arrives in its act, not
  here. Terms ≤ 17 characters (longer ones truncate and no gate catches it).
  `durationSeconds` = the measured audio. A chapter with more than six
  prerequisite terms defines the rest in the act where each first appears, on
  screen, in the same breath as its first use.
- **Acts.** One act per major movement of the source, in the source's order
  unless a prerequisite forces a swap (log the swap in `ACTS.md`). 4–10 beats
  per act. Each act opens on a short act-title beat (Title Case serif; a
  `FormACard` or the act's first picture carrying the title as its label) so
  the viewer always knows where they are.
- **BVDT.** Handoff line "Let's recap with Claude." after a 0.5 s lead pause,
  then one bare sentence per act, 4 or 6 lines (never 5: the card paginates in
  twos). It recaps; it asserts nothing new.
- **BHTF.** `greeting: "Your turn."`, topic containing "YOUR TURN", a prompt
  the viewer can paste that makes them USE the chapter's main idea, read in
  full (`props.command` == `narration_text`), and two `output` lines that are
  the viewer's own checks on the result.
- **BOUT.** By channel:

| `metadata.channel` | Persona / voice | BOUT |
|---|---|---|
| `claude-liam` **(default)** | Liam, in for Bear · Kokoro `am_onyx` | `ClaudeTitleOutro`, locked by `OUTRO-LOCK.md`: exact title, hardcoded `@NikBearBrown`, slug-seeded mascot, no subline; `kind: "outro_voice"`, narration `"<exact title>. At Nik Bear Brown."`, 1.0 s silent tail. No jingle |
| `claude-hai` | HAI · `am_onyx` · Plain register | the Humanitarians AI outro (`OutroSeries` / `OutroCTA`) per `../hai/SKILL.md`; `metadata.channel_title: "@HumanitariansAI"` |
| `claude-medhavy` | Medhavy · `af_kore` · Wonder | `MedhavyOutro` |
| `claude-musinique` | Musinique · `am_puck` | `MusiniqueOutroCard` |
| SEIS | per `brands/seis.md` | `SeisOutro` |

  The @NikBearBrown card, handle and mascot never appear on another channel,
  and another channel's outro never appears on a claude-liam film. A channel
  not in this table is a question for Bear, not a guess.

`metadata.skill: "lecture"`, `style_preset: "lecture"`, and
`bookend_check.py` accepts the hesitant-writer open for this skill. On the
default channel run it and get a PASS. On any other channel the checker's
outro rule still expects `ClaudeTitleOutro`; record that one expected FAIL in
`BUILD-LOG.md` rather than putting the wrong outro on the film.

## WHOLE-SOURCE LAW — the entire chapter, one film

1. **Read the whole source before planning anything.** Not the first screens,
   not the headings: every section, figure, table, code block and example.
2. **Write `ACTS.md` first.** A coverage map: every section of the source is
   assigned to an act, or listed under `LEFT OUT` with a one-line reason
   (repeats an earlier section; front matter; an aside that teaches nothing on
   its own). Nothing is dropped silently. The act map is a record the human
   can read afterwards, not a thing to wait on.
3. **One film.** A lecture is not cut into per-section films (that is `tldr`).
   If the source is really two unrelated chapters, build the one film anyway
   and say so in `BUILD-LOG.md` and the final report; do not split on your own.
4. **Length is an output.** No cap, no target, no band. Every idea the chapter
   teaches gets its beat; nothing is padded and nothing is repeated to fill.
   A 9-minute chapter and a 30-minute chapter are both correct lectures.
   Log the estimated runtime in `BUILD-LOG.md` as information.
5. **The source's figures, tables, equations and code are the first visuals to
   animate.** A figure in the chapter is rebuilt as a moving beat, never pasted
   as a screenshot. A table becomes a drawn table with the row that matters
   ringed. A code listing is run and shown running.
6. **SELF-CONTAINED LAW** (Bear, 2026-10-02: *"we do not talk about this
   chapter or the book because nobody's read these books … we assume the
   person has not read my other books, has not looked at most of my YouTube
   … it's pretty self-contained"*). Assume the viewer has read none of Bear's
   books and seen none of his other films. So:
   - Narration never says "this chapter", "the book", "as we saw earlier in
     the course", "in the last video", or names a chapter or section number.
   - Anything the source leans on from another chapter, book or film (a term,
     a framework, a running example, a result) is taught here, briefly, at the
     point it is needed, or it goes in BDEFS. A reference the viewer cannot
     follow without outside reading is a defect, the same as a wrong number.
   - Bear's own named frameworks get one plain sentence of what they are the
     first time they are spoken.
   - The one exception is a film made for a particular course: when
     `metadata.course` is set, say the course by name where the credit belongs
     (BIDEA and the outro block). Even then the lesson itself must stand up
     for someone who is not enrolled.
7. **Teardown register.** Every sentence is rewritten for the ear; nothing
   ships in the source's prose. ~7–14 s and ~20–40 words per body beat. A beat
   past ~15 s is usually two ideas: split it.

## BEST-BEAT LAW — audition the whole playset, every beat

The lecture's defining move. For each body beat, ask one question: **what is
the single best thing to LOOK AT while this sentence is spoken?** Then use it,
whichever skill it comes from. No lane is the default. No lane has a quota.

**Per beat, in this order:**

1. **Name what the sentence is about** in a few words: a mechanism, a quantity,
   a physical arrangement, a structure, a piece of code, a tool, a real record.
2. **Ask the library** (GATE L): `./art scenes "<what the beat needs>"` and,
   for marks, `./art icons "<what it needs>"`. A hit is a lead; read its props.
   `./art scenes --check <Name>` before citing any component in the sheet: a
   name that is not renderable is a punt, and several names in older docs are
   not registered.
3. **Audition at least two lanes** from the router below and pick the one
   whose MOTION is the beat's claim (the voice could point at the motion and
   say "that is what I mean").
4. **Write it down.** `SHOTLIST.md` carries one row per body beat:
   `| beat | about | lane picked | runner-up | why this one wins |`. A beat
   with no runner-up was not auditioned.

**The router — what the beat is about → the lane that usually wins:**

| The beat is about… | Lane | Laws live in |
|---|---|---|
| An equation, a derivation, a geometric or physical mechanism, one form becoming another | **Manim lesson** (transform, don't cut) | `../tldr/SKILL.md` Manim laws; `docs/MATH-TYPESETTING.md` |
| A quantity that moves: a trend, a comparison, a distribution, a part of a whole | **Manim chart**, or `ShowTellCard` `chart` / `dashboard` when the numbers are real and the card passes the card test | `../nopunt/SKILL.md` catalog; `../show-tell/SKILL.md` card test |
| A physical arrangement or flow of THINGS: packages, parts, containers, people handing off, a pipeline you could build out of boxes | **Isometric drawing** (`iso_kit.py`, the 25 original props) | `../show-tell/SKILL.md` DRAWING LAWS |
| A structure with a shape: a 2×2, a ladder, a funnel, a stack, a taxonomy, a gate | **Manim diagram**, drawn on the spoken cue | `../nopunt/SKILL.md` catalog |
| A set of 2–4 named things, each recognisable by a mark | **2-D library icons**, large, on `LibraryIconRow` (`./art icons`; copy the SVG into `runtime/remotion/public/form-b-icons/`; specific → general → ask, never invent). `FormBCard` shows the same icons at 44 px and reads as a text card: use it only when the words matter more than the marks | `../nopunt/SKILL.md` FormB rules |
| An interface behaviour: searching, switching, choosing, a document assembling | **`ShowTellCard`** (16 kinds), only when it passes the card test | `../show-tell/SKILL.md` Card family |
| Code: a listing, a diff, a run, an error, an output | **The real code, run**: `ClaudeCodeBeat` for a listing, `CCPlainShell` for a plain terminal, the output captured from an actual run | `docs/EXECUTABLE-EVIDENCE.md`; `../cli-explainer/SKILL.md` |
| Claude Code, Codex, the Claude app, a website, any named tool | **The thing itself** (SHOW-THE-THING LAW, below) | `../cc-explainer/SKILL.md`; `../medhavy-walkthrough/SKILL.md` |
| A real person, place, document or event, where the record IS the evidence | **VOX still** from `pantry/`, machine-animated | `../deep-explainer/SKILL.md` VOX BEATS; VOX LAW |
| An act title, an aphorism, a breath | **Card** (`FormACard`), last resort | `../nopunt/SKILL.md` CARD |

The table says what USUALLY wins. The beat decides. A flow of data through
named services may be better as an isometric conveyor than as a node diagram;
a "structure" may be better shown as the real config file. Pick by which
picture a viewer would understand with the sound off.

**The laws around the pick:**

- **PRIMARILY VISUAL.** The picture carries the idea and the voice explains
  it. On screen: labels of one to three words, a hero number, the real text of
  a real artifact. Never a sentence of narration set as type, never a bullet
  list. Text-only cards are for act titles and at most one breath per act; a
  card whose narration makes a claim or names a visual is a PUNT.
- **MOTION CARRIES THE CLAIM.** The still-frame test: if a beat reads the same
  as a still, it fails. Every spoken point has a motion that lands on its
  word.
- **NEVER FOR VARIETY.** A lane change must be earned by the content. Do not
  switch lanes to break monotony, to show off the playset, or because the
  best lane is harder to build. Equally, do not stay in one lane because it is
  already open: three isometric beats in a row are right only if all three
  ideas are physical arrangements.
- **ONE LOOK.** Lanes change; the film does not. Every lane renders in the
  Claude palette (stage `#F2F0E9`, ink `#3D3929`, terracotta `#D97757` as the
  one accent, EB Garamond) so a cut from a drawing to a chart to a card reads
  as one film. The exception is a real tool's own interface, which keeps its
  real look.
- **ONE CAST PER ACT.** Within an act, the same object is the same picture. If
  act II's request is a kraft box in beat 3, it is that box in beat 7, even
  when beat 5 is a chart. Recurring objects are listed in `ACTS.md` per act.
- **A MISS IS A BUILD, NOT A SLATE.** If the best visual does not exist yet,
  build it (a Manim scene, or a new Remotion component, registered, then
  `./art scene-index`). The library logs the miss to `TEMPLATE-MISSES.md`.
  Settling for the second-best existing component is legal only when the
  SHOTLIST row says why it teaches as well.
- **PROOF GATE.** Every body beat classifies SHOW, justified HOLD, or CARD per
  nopunt, and the whole-sheet teaching-arc checklist passes. Write
  `CHECKS-REPORT.md` before the first compile, with the lane histogram
  included as information, never as a quota.

## SHOW-THE-THING LAW — a tool is shown as itself

When a beat uses or talks about a specific tool, app or website (Claude Code,
Codex, the Claude app, GitHub, Figma, a course site, a dashboard, any named
product), **the screen shows that thing**. Never a generic drawing standing in
for a product's interface: no isometric box labelled "Codex", no abstract
window labelled "the website".

Take the highest rung that is available:

1. **The real thing, captured.** Drive the real site or app and record it, or
   run the real command and capture the session. Browser capture follows
   `../medhavy-walkthrough/` (its scripts and its DPR, popup-tab and sign-in
   gotchas); app capture follows `../godot-waikthrough/`; a human-supplied
   screen recording is prepared by `../screen-clean/`. A sign-in is the
   human's: stop and ask, never enter credentials. A still capture of a public
   page plays on **`BrowserCapture`**: capture at 1600×900 with device scale
   2.4 (a 3840-wide PNG), put it under `runtime/remotion/public/<slug>/`, and
   give the scene the real address, a dated caption, and camera `moves` that
   push in to what the sentence names (one terracotta ring; no move inside the
   45–55% window). Real command-line output plays on `CCPlainShell`, verbatim,
   with `durationSeconds` set so the lines land with the voice; only read-only
   commands are run on a shared system, and a command that was not run is
   shown without output.
2. **The library's faithful skin of that tool.** The CC kit for Claude Code
   (`CCSession`, `CCShell`, `CCPromptBar`, `CCToolCall`, `CCPlainShell`), the
   Codex templates (`CodexWindow`, `CodexComposerAsk`, `CodexCodeBeat`), the
   Claude app (`ClaudeComposerAsk`, `ClaudeWindow`, `ClaudeVerdictArtifact`),
   `ClaudeCodeBeat` for code. Search first: `./art scenes "<tool name>"`.
3. **A card built for that tool.** No capture possible and no skin in the
   library: build a Remotion card that reproduces the tool's real layout and
   real labels closely enough that a user of the tool recognises it at once.
   Register it, run `./art scene-index`, and note it in `BUILD-LOG.md`. That
   card is now in the library for the next film.

Rules on every rung:

- **What the screen says is real.** A prompt shown as typed is one that was
  typed; output shown is output that came back. A skin or a built card may
  only display content taken from a real run, the tool's own documentation, or
  the source chapter, and `FACTCHECK.md` lists where each came from. Invented
  interface output is a fabricated record and fails Gate F.
- **Claude Code and Codex session beats trace to a real session** (`SESSION.md`
  in the reel folder), per cc-explainer's REAL-SESSION and TYPES-NOT-NARRATES
  laws. Talking ABOUT the tool without a session (what it is, where it sits)
  still shows the tool's real surface, with nothing typed into it that was
  not really typed.
- **The tool keeps its own look** inside its window. The stage around it stays
  cream.
- **Capture is evidence, not wallpaper.** Crop and zoom to the part the
  sentence is about; highlight with the one terracotta ring. A full-screen
  capture held while the voice talks about one button fails the still-frame
  test.
- Type inside a capture must clear the GATE T floor at 4K. If the real
  interface is too small to read, zoom the capture; do not shrink the law.

## Workflow — straight through; approval only before paid steps

**NO-GATE-ON-FREE LAW** (Bear, 2026-10-02: *"because it's free, we don't have
any approval gates ever in front of free things. Approval gates are only for
paid things."*). The default build is entirely free (Kokoro `am_onyx`, Liam
persona, Manim, Remotion, real captures), so it runs from source to master
without stopping for approval: no plan gate, no audio gate, no "watch the
previz first". The plan documents are still written, as records. The MACHINE
gates still fail the build (Gate F, A, B, V, T, bookend, PROOF GATE); passing
them is the work, not a request for sign-off. The only stops are:

- a **paid** step (any Higgsfield or other paid generation): ask for that
  beat, before spending, every time;
- a **sign-in or credential** on a site being captured: the human does it;
- **publishing**: never without the human's word.

Run from `books/`. The reel builds into the OWNING BOOK:
`<book>/youtube/<channel>-lecture-<concept>/` (default
`claude-liam-lecture-…`); a document with no book builds beside the document
in `youtube/`. Never into the toolkit.

1. **Read + `ACTS.md`.** The whole source; the coverage map; the cast per act;
   the BIDEA correction and the BDEFS terms. Save the source or its path in
   `SOURCES.md`.
2. **Route + `SHOTLIST.md`.** BEST-BEAT LAW per beat: library asked, two lanes
   auditioned, the pick and the runner-up written down. List every tool beat
   and its SHOW-THE-THING rung. List what must be captured, run, or built.
   Log the lane histogram and estimated runtime in `BUILD-LOG.md` and keep
   going; nothing here waits for approval.
3. **`FACTCHECK.md` (Gate F).** Every number and named claim checked against
   the source and, where the source cites one, the primary. Strip what will
   date the film. Attribute thin numbers aloud and on screen. Rows:
   `| # | Beat | Claim | Verdict | Source | Fix |`. Write `PROMPTS.md` (or "no
   generation prompts"). The run refuses without the paperwork.
4. **Evidence first.** Run the code, capture the sessions and the sites, fetch
   any genuinely necessary still (free sources first, deep-explainer tiers).
   A beat whose evidence cannot be produced is re-routed now, not slated later.
5. **Sheet.** `make_sheet.py` (start from
   `../show-tell/reference/example-make_sheet.py`): bookends via the
   `remotion()` helper; each body beat carries `act`, `lane`, `proof_gate`,
   `shot.visual_intent`, `shot.show`, `shot.motion_claim`, and its lane's
   block (`shot.manim.class` or `shot.remotion.pattern` + `props`). Metadata:
   `skill` / `style_preset: "lecture"`, `channel`, `title`, `playlist`,
   `tags`, and `course` when there is a course credit. Carry `audio_file` and
   `actual_duration_s` forward on re-runs.
6. **Audio.** `generate_audio_kokoro.py <reel>` (free). Pad BOUT with its 1.0 s
   tail. Write measured durations back; they are the clock. Whisper-check the
   greeting, numbers and acronyms. Re-voice single beats with `--only <BID>`.
7. **Stills first.** Low-resolution last frames of every Manim scene and
   25/50/95% stills of every Remotion beat, on a contact sheet, LOOKED at,
   before any 4K render. Write `CHECKS-REPORT.md`.
8. **Review cut.** `./brutalist.art/art run <reel> --height 2160`. Manim and
   Remotion beats render for real; only a justified HOLD may slate. Look at
   frames and the qc-sheet. Fix, re-run. A long lecture renders act by act:
   keep the Manim scenes for each act in the one `scenes.py` (Gate A copies
   only that file) and move superseded clips to `_superseded/` before
   re-rendering.
9. **Final.** `./brutalist.art/art final <reel> --height 2160 --out
   <reel>/exports/landscape` (GATE T, then the master). Check the master:
   3840×2160, runtime equals the sum of the audio, silent tail present.
   `python3 brutalist.art/runtime/scripts/bookend_check.py <reel>`.
10. **STOP.** Hand over the master, the runtime, the lane histogram and any
    open HOLD. Stage (`art post`) and publish only on the human's word, and
    only from TOPOST.

## Output contract

```
<book>/youtube/<channel>-lecture-<concept>/
  beat_sheet.json     the heart
  make_sheet.py       the sheet builder
  ACTS.md             coverage map: source section → act, LEFT OUT with reasons, cast per act
  SHOTLIST.md         per beat: about | lane | runner-up | why; tool beats with their rung
  FACTCHECK.md        claim | verdict | source | fix
  CHECKS-REPORT.md    SHOW/HOLD/PUNT counts, teaching arc, lane histogram
  SOURCES.md          the source, primaries, captures, credits
  SESSION.md          only when a Claude Code / Codex session is shown
  PROMPTS.md  BUILD-PROMPT.md  BUILD-LOG.md
  scenes.py  manim/  media/  mp3/  pantry/  captures/  exports/
```

## Hard rules (this genre's own — parents' rules all still bind)

1. **The whole source or a written reason.** Every section is in an act or in
   `LEFT OUT`. A lecture that quietly covers the first half is a defect.
2. **Best beat, not nearest beat.** Every body beat has a SHOTLIST row with a
   runner-up. No lane is default; no lane has a quota; no lane is banned.
3. **A tool is shown as itself.** Captured, skinned, or carded, in that order.
   Nothing on a tool's screen is invented.
4. **Primarily visual.** Text-only beats are act titles and the rare breath.
   Narration is never set as type.
5. **One film, no cap.** Never split, never padded, never trimmed to a length.
6. **The opening pair and the closing three are fixed.** Hesitant writer, key
   terms; recap, Your Turn, the channel's outro. No composer cold open, no
   TL;DR page.
7. **The outro belongs to the channel.** Default @NikBearBrown, locked by
   `OUTRO-LOCK.md`. Never one channel's card on another channel's film.
8. **Borrowed lane, borrowed laws.** A beat built in another skill's lane
   passes that skill's laws and traps, read from that skill's file.
9. **Free by default, and free means no approval gate.** Kokoro, Manim,
   Remotion, real captures run straight through. Any paid generation is asked
   per beat, in advance; that is the only approval gate before the master.
10. **Self-contained.** The viewer has read none of the books and seen none of
    the other films. No "this chapter", no "the book"; a course is named only
    when the film is for that course.
11. **Never publish.** The master stays in the reel folder until the human
    says otherwise.
