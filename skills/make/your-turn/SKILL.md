---
name: your-turn
description: >
  Standardize and upgrade the CLOSING block of a claude-explainer / nbb reel:
  a three-beat, Liam-narrated sign-off — VERDICT recap (ClaudeVerdictArtifact) →
  YOUR TURN prompt the viewer can run (ClaudeComposerAsk) → TITLE re-read
  (ClaudeTitleOutro). Adds the handoff line ("Thanks Bear, let's recap with
  Claude." after a Bear body; "Let's recap with Claude." after a
  Liam body) with a 0.5s lead pause; makes the YOUR TURN prompt RELEVANT to the
  specific video and has Liam read it in full; has Liam re-read the title on the
  outro; enlarges the verdict card and kills double-numbered recap lines. Use
  when the user types `your-turn`, `your turn`, `recap block`, `closing block`,
  `liam outro`, or asks to standardize/fix the ending of the explainers, add a
  "your turn" prompt, or batch-fix the verdict/recap cards. Beat-sheet driven,
  idempotent, phase-gated. Never publishes; re-render + re-upload is a separate
  human-triggered step.
---

# your-turn — the standardized Liam sign-off

Every claude-explainer reel should end the same way: Liam hands off from the
body, recaps on the artifact card, gives the viewer a prompt to run, and re-reads
the title. This skill makes that block uniform across the catalog and fixes the
two defects in the current cards (tiny verdict card, double-numbered lines).

It is a CLOSING-BLOCK skill, not a whole-reel skill — it edits the last three
beats of an existing `beat_sheet.json`. The parent pipeline is `claude-explainer`;
voices, palette, and render all inherit from there.

## The block (in order)

1. **Handoff + VERDICT** — `ClaudeVerdictArtifact`, Liam (`kokoro`/`am_onyx`).
   - 0.5s lead pause (`lead_silence_s: 0.5`), then the handoff line:
     - **prior body beat persona was Bear** → `"Thanks Bear, let's recap with Claude."`
     - **prior body beat was already Liam** → `"Let's recap with Claude."`
   - then the full recap narration over the card.
   - card is enlarged (see Fixes); recap lines are BARE sentences — the card
     numbers them itself.
2. **YOUR TURN** — `ClaudeComposerAsk`, Liam, `greeting: "Your turn."`
   - the composer shows a prompt **relevant to this specific video**, and Liam
     **reads the whole prompt** (`props.command` == `narration_text`).
   - footer `@NikBearBrown`, model chip unchanged (`Fable 5` / `High`).
3. **TITLE re-read** — `ClaudeTitleOutro`, Liam.
   - `narration_text` = `"<exact title>. At Nik Bear Brown."` — Liam re-reads the
     title and speaks the handle as the sign-off. **No jingle, no music** on the
     card (OUTRO-LOCK.md §Voice, 2026-09-18); 1 s silent tail hold after the voice.
   - `props.title` = title; the handle is hardcoded in the component; no subline.

## Voices (inherited)

| Persona | Engine / voice | Role |
|---|---|---|
| **Liam** | `kokoro` / `am_onyx` (free) | the recap voice — owns all three closing beats |
| **Bear** | `kokoro` / `am_onyx` | main body narrator; the handoff thanks him by name |

The handoff wording is decided by the persona of the beat immediately before the
verdict — persona `bear` → "Thanks Bear, let's recap with Claude."; anything else → "Let's recap with Claude."

## Auto-drafting the YOUR TURN prompt

The prompt must be RELEVANT to the video, so it is drafted per reel, never
templated. Draft one prompt per slug from the reel's own material:

- Read `metadata.source` (the source chapter/section) and the body beats'
  `narration_text`. The prompt should let a curious viewer go one step DEEPER
  than the video: a real question a student would paste into Claude after
  watching — grounded in the same mechanism, 3–5 sentences, ending in a concrete
  multi-part ask. First person ("I'm studying…, I understand…, can you walk me
  through (1)… (2)… (3)…").
- Write all drafts to a `drafts.json` map keyed by `metadata.slug`:
  `{"[slug]": {"prompt": "[text]", "recap": {"title": "<=6 words", "lines": [4 bare sentences]} | null}}`.
  `recap` is drafted ONLY for reels that lack a verdict card — the transformer
  uses it to INSERT one before the your-turn beat. This is the one
  non-deterministic step and the one human gate — review `drafts.json` before
  applying.

## Fixes folded in

- **Verdict card too small** — `ClaudeVerdictArtifact.tsx` was hard-pinned to
  860px on a 1920 frame. Now fills ~84% width with legible type. One component
  edit fixes every reel on re-render.
- **Double-numbered recap lines** — ~160 lines across the catalog had authored
  `"1."`/`"2."` colliding with the card's own numbering. The transformer strips
  leading numbers from `artifactLines`, and the component now strips them
  defensively too (`stripLeadNum`), so it can never happen again.

## Commands (run from `books/`)

```bash
SK=brutalist-art/skills/make/your-turn

# 1. DRAFT prompts (+ recaps) for the target reels → drafts.json  (LLM step; human reviews)
#    (draft with this skill's guidance above; one entry per slug)

# 2. DRY RUN a census + planned edits, write nothing:
python3 $SK/scripts/apply_your_turn.py --root . --drafts drafts.json \
    --report your-turn-report.json --dry-run

# 3. APPLY in place (touches sheets with a your-turn OR liam outro; inserts a
#    verdict card where missing, using the drafted recap):
python3 $SK/scripts/apply_your_turn.py --root . --drafts drafts.json \
    --report your-turn-report.json

# 4. RE-RENDER + RE-UPLOAD is separate and human-triggered, per reel:
./brutalist-art/art run   [book]/youtube/[slug]     # review cut
./brutalist-art/art final [book]/youtube/[slug]     # master
# then youtube-publisher (new upload → new URL; delete/unlist the old ID)
```

The transformer is **idempotent** — re-running never stacks handoffs or
re-numbers. Sheets without a verdict card (slate cuts, other families) are
skipped untouched. Reels with no drafted prompt keep their existing YOUR TURN
content and are listed under `needs_prompt` in the report.

## Rules

1. **Audio-first** — the handoff, the read prompt, and the title re-read are new
   Liam lines: regenerate audio, then conform. Never hand-time.
2. **Phase gate** — review `prompts.json` and `your-turn-report.json` BEFORE any
   audio spend or render. The agent drafts prompts; the human signs them off.
3. **Never publishes** — applying the block and re-rendering is safe; going
   public is a manual Studio flip. Re-upload replaces the file via a NEW video
   ID — the old URL/views are lost, so batch deliberately.
4. Only edits the closing three beats. The body is out of scope.
