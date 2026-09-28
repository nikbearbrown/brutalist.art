# Skill Tiers

## FELLOW TIER — free, safe, hand out
These are the defaults for anyone new to brutalist.art. Deliberately five BUILDERS — the failure
mode for a new person is not missing capability, it is four explainer variants and
no idea which to open. `nopunt` is a reference they consult, not a sixth way to
make a video.

| Skill | Use this when |
|---|---|
| fellows | You have a HAI fellow's video report and want a Claude-bookended reel |
| ai-explainer | You want to explain a concept in the Claude desktop-app visual style |
| hai | You need a Humanitarians AI Plain-register reel |
| your-turn | You want to close a reel with a structured handoff prompt |
| duration-planner | You need to fit content to a target length |
| nopunt | *(reference)* You're unsure how to animate a beat, or a beat is punting |

## ADVANCED — Bear only
| Skill | Notes |
|---|---|
| deep-explainer | Multi-layered concept depth passes |
| cli-explainer | Claude session + live code + output as vox beat |
| tldr | Chapter/report → learning sections → per-section film: TL;DR up front, THE QUESTION, TERMS, then a 3Blue1Brown-template LEARN body in pure Manim; your-turn close; Liam, regular outro |
| godot-waikthrough | Real Godot feature walkthrough with Liam riffs; `walker` adds Claude/GDD bookends; regular outro |
| godot-gamedev | Detailed Godot code/component/art teardown; source-backed editor views and optional `walker` bookends; Liam and regular outro |
| medhavy-walkthrough | Real Medhavy Hub (hub.medhavy.com) browser walkthrough with Liam riffs; `textbook` adds Claude bookends; seeded tenant + human sign-in required; regular outro |
| godot-gdd | GDD design-contract walkthrough using existing game evidence; proposals versus implementation; optional `walker` bookends; Liam and regular outro |
| nbb | NikBearBrown/Teardown register — Kokoro am_onyx voice |
| guests | Board members, advisors, invited speakers. NO feedback beat — staff do not evaluate board members. GATE G. |
| finance | SEC filings → 11 fixed beats, EDGAR XBRL data, two deterministic audits |
| anthropics | The beat: repos, papers, their content, capability claims — read independently |

## UTILITIES — invoked by other skills, rarely run directly
| Skill | Notes |
|---|---|
| screen-clean | Prepares any screen recording (Zoom/Teams/QuickTime) for a reel beat. Called by `fellows` and `guests`. |
| riff | Render/inspect a visual artifact and explain its visible behavior and trade-offs. Called by `godot-waikthrough`; humans judge usefulness. |
| logo-motion | Animates a brand mark into a 4–8s sting for a reel's open/close. Free (potrace + Remotion, no keys). Deliberately NOT a Fellow-tier builder — it makes a *component*, not a video, and the Fellow tier is capped at five builders on purpose. |

## PAID — REQUIRES EXPLICIT SPEND APPROVAL
⚠️ Never present these as default options to a fellow.

| Skill | Cost note |
|---|---|
| explainer | FLUX/nano-banana stills + Higgsfield video. Ask per step, then spend. Kokoro VO is free. |

---

## Modes

**`--silent`** — unattended production. Honoured by every skill above; see
[SILENT-MODE.md](./SILENT-MODE.md). Removes the human from the loop, never the
gates: machine gates still fail the build, third-party gates (GATE N, GATE G)
skip the reel rather than auto-pass.
