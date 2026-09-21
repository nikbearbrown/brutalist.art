---
name: medhavy-walkthrough
description: Walk ONE Medhavy textbook the way a student meets it — sign in at hub.medhavy.com, open the book, then the book's own features (chapter sidebar, search, the "Ask this textbook" AI tutor with its sources and memory, night mode) — captured from a real browser at native 4K, riffed by Liam, rendered with the regular outro. One reel per book. The `admin` modifier films the hub's admin panel instead. Also accepts medhavi-walkthrough. Never types credentials, never shows real student data, never publishes.
---

# medhavy-walkthrough — a textbook that answers back, one book at a time

The web sibling of [godot-waikthrough](../godot-waikthrough/SKILL.md). The
**subject is the textbook**, not the hub: the hub is the front door (sign in,
dashboard, Open Textbook), and everything after that door is the book's own
UI. Inventory what is built, drive it through real clicks, capture the real
screen, hand the captures to [riff](../riff/SKILL.md), assemble on the
ai-explainer chassis, close with the regular outro.

```text
medhavy-walkthrough "Cancer textbook" /path/to/medhavi-hub
medhavy-walkthrough admin /path/to/medhavi-hub          # the hub's admin panel instead
```

`medhavi-walkthrough` (old spelling) is an alias. The book name is the title
as the hub's registry shows it. Output belongs in
`medhavi-hub/youtube/claude-liam-medhavy-<book-slug>-walkthrough/`.

Read first: the hub repo's `README.md`, `DEVELOPER.md` §4 (tokens), §9;
`docs/creating-a-new-textbook.md`; the book's own doc set under
`medhavy_documentation/<book>/` (ARCHITECTURE, API, USER_GUIDE) — that is the
feature list; then [feature-inventory.md](references/feature-inventory.md),
[capture-and-coverage.md](references/capture-and-coverage.md),
[RENDER-TARGETS.md](../../../RENDER-TARGETS.md), and
[PIPELINE-SAFETY.md](../../../docs/PIPELINE-SAFETY.md).

## 0. Hard walls

- **Credentials.** Clerk sign-in is the human's. The agent never types a
  password, code, or key and never creates an account. The human signs in
  once via `scripts/save_session.py`; the driver reuses that session. The
  sign-in and sign-up pages are shown **signed out and untouched**
  (`--no-session`), then the film cuts to the signed-in state and says so.
- **Real people.** Production holds real students. Every email, person name
  and `CLS-` invite code is masked in the DOM before a frame is recorded;
  the driver aborts if a raw one is visible at any step. A leaked capture is
  deleted, never blurred later.
- **Accounts.** One dedicated account is enough. An admin account sees every
  book but its `/dashboard` redirects to `/admin`, so the *student* dashboard
  (pending / approved / request counts) cannot be filmed from it; show the
  admin's shelf and say so in narration and Verdict, or film with a student
  account. Never Bear's personal login if another exists.

## 1. Inventory the book

Confirm on the live site what the docs promise. For a Fumadocs textbook that
is typically: chapter/section sidebar; the chapter page (headings, figures,
KaTeX, Mermaid, "On this page"); hybrid search (⌘K); the **AI tutor panel**
("Ask this textbook": suggested prompts, streamed answer, *Top sources used*,
"Dive deeper into all sources", follow-ups that keep context via the hub's
memory API); theme toggle; feedback. Distinguish built / not shown / api-only
(memory, articles, verify). Record the hub commit, the book URL, the tenant,
and the capture method. Do not fix the book to make a demo succeed.

## 2. Drive and capture, then riff

Two runs. **Run A, signed out:** landing, `/sign-in`, `/sign-up`; nothing
typed. **Run B, signed in:** dashboard or shelf → `Open Textbook` (a new
tab; the driver follows it and records it as a second page) → book home →
sidebar → a chapter → search → the AI panel: type a real question on
screen, let the answer stream, show its sources; a follow-up that depends on
the first answer (memory); a simpler-terms / analogy ask; a summary ask →
night mode. Capture at `--css-size 1600x900 --dpr 2.4` (native 3840×2160,
legible). Real clicks only; no API calls, no cookie edits.

Invoke **riff** on the captures. Narrate what happened on screen, the
mechanism (retrieval over the chapter, not training; per-book 24h token;
short-term memory keyed by session), and a useful trade-off. Liam in for Bear,
Kokoro `am_onyx`. If the tutor's *top sources* include off-topic sections,
say so: that is the honest riff, not a defect to hide. The site's own "AI can
make mistakes" line stays on screen.

## 3. Assemble

Read [ai-explainer](../ai-explainer/SKILL.md) for the chassis. **Real screen
capture** overrides its REBUILD LAW; the UI is the subject. Footage beats are
`shot.type: SCREEN` (the type gate treats browser UI as captured, not designed).

Bookends, in order: **B00 ClaudeComposerAsk** — the student's ask ("What if my
textbook could answer my questions and show its work? …"), labelled a
reconstruction; **B01 BrutalistHesitantWriter** — the misconception corrected.
Bear's framing rule (2026-09-18): never leave the viewer with "a PDF with a
chatbot". The card must land on what Medhavy *knows*: this book and chapter,
you (memory), and the course that gave you the book, with answers grounded in
that and citing the pages used. The writer replaces WHOLE WORDS from
comma-separated lists, positionally (`triggerWords: "chatbot, PDF"` →
`replacementWords: "tutor, book and knows you and your course"`); a phrase
that crosses a line break never matches and the correction silently never
renders, so check the last frame of the beat. **Body** as above; **Verdict**
(observed / not shown / open / human); **Your Turn** (a concrete ask for the
student to type into their own book, plus "check the sources it lists");
**regular outro** per [OUTRO-LOCK.md](../../../OUTRO-LOCK.md): Liam re-reads the title, then "At Nik Bear Brown"; no jingle.

## 4. Render, gate, stage

```bash
# From brutalist.art; REEL = the resolved reel path.
python3 skills/make/medhavy-walkthrough/scripts/save_session.py            # human signs in once
python3 skills/make/medhavy-walkthrough/scripts/capture_admin.py REEL --run run-signin --plan REEL/capture/plan-signin.json --css-size 1600x900 --dpr 2.4 --no-session
python3 skills/make/medhavy-walkthrough/scripts/capture_admin.py REEL --run run-book   --plan REEL/capture/plan-book.json   --css-size 1600x900 --dpr 2.4
python3 runtime/scripts/generate_audio_kokoro.py REEL
python3 skills/make/medhavy-walkthrough/scripts/prepare_media.py REEL       # frame-exact cuts, narration padded, spoken outro + tail
python3 runtime/scripts/remotion_scenes.py REEL
./art medhavy-walkthrough --check REEL
python3 runtime/scripts/compile.py REEL --review --fps 30 --height 2160     # NOT `art run` (24 fps grid)
python3 runtime/qc/final_frame_check.py REEL --mp4 REEL/<slug>-slate.mp4
./art final REEL --height 2160 --fps 30 --out REEL/exports/landscape
```

Rules that cost rebuilds: end every footage window at the last screenshot,
before the next `goto` (white load frame); narration must fit the window,
padded not stretched (`prepare_media.py` refuses otherwise); per-beat tracks
limited to −1 dBTP before staging; captions via
`scripts/build_srt_and_description.py REEL --to TOPOST` (the generic emitter
truncates). Then `runtime/scripts/post.py REEL --no-topaz`. No upload.

Deliver the MP4's absolute path, a quoted `open` command, feature coverage,
tenant and redaction status, limitations, QC results.
