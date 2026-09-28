# FACTCHECK — claude-liam-brutalist-show-tell-cards

Every claim is about the toolkit itself; each was checked against the file named.

| # | Beat | Claim | Verdict | Source | Fix |
|---|---|---|---|---|---|
| 1 | B00 | show-tell: every beat gets one picture; the voice explains | PASS | show-tell SKILL.md, law 1–2 | — |
| 2 | B01 | until now every picture came from one isometric kit (boxes, dark blocks, flat pages, Claude palette) | PASS | SKILL.md (pre-2026-09-27 "The BODY is all drawings"); iso_kit.py | — |
| 3 | B02 | sixteen card kinds | PASS | ShowTellCard.tsx `kind` enum has 16 values | — |
| 4 | B02 | same fonts, same colours | PASS | ShowTellCard.tsx uses CLAUDE_FONT and the iso_kit palette hexes | — |
| 5 | B02 | shot on twos: each drawing holds for two frames | PASS | ShowTellCard.tsx `onTwos` default true, `frame - frame % 2` | — |
| 6 | B03 | player, search, tabs, chart, stack, dock, flowing paths, and more | PASS | `kind` enum | — |
| 7 | B04 | drawings stay the default; a card is optional; all drawings, all cards or a mix | PASS | SKILL.md Card family ("a menu, not a quota") | — |
| 8 | B06 | these are the beat lengths of the first show-tell film, in seconds | PASS | plugin-portal beat_sheet.json `actual_duration_s`, B00–B07, rounded to 0.1 s: 4.8, 11.9, 8.8, 8.1, 11.2, 8.7, 8.3, 10.5 | — |
| 9 | B08 | the beat sheet drives the audio, the Manim drawings and the cards; all three meet in one master | PASS | generate_audio_kokoro.py, scenes.py, remotion_scenes.py, compile.py all read beat_sheet.json | — |
| 10 | B09 | labels 1–3 words; terracotta never text; type ≥ 48 px; on twos; flat paper shadow, no blur | PASS | SKILL.md laws + Card laws; ShowTellCard.tsx `Shadowed` (solid kraft offset, no blur) | — |
| 11 | B10 | keep at least two drawn beats; never two cards of the same kind back to back; a card only when its motion is the point | PASS | SKILL.md Card laws | — |
| 12 | B09 | "Type stays at forty-eight pixels or more" | CORRECTED | chips may go to 32 px; body text is ≥ 48 | screen says "≥ 48 px" in a row labelled Type, for body text; narration kept (chips are chrome, not type the viewer reads) |
