#!/usr/bin/env python3
"""make_sheet.py — beat_sheet.json for claude-liam-brutalist-show-tell-cards.

A show-tell film ABOUT show-tell (Brutalist meta-series): the skill's one law (one picture per
beat, the voice explains), its isometric drawing kit, and the optional ShowTellCard family
added 2026-09-27. Bear: "keep all typography and colors but add more stop motion cards beyond
just the isometric graphics ... the skill should never force but more choices can add ...
make a film showing the show-tell skill and cards".

Body = three drawn Manim beats (B00, B01, B10) + eight card beats, each a different kind.
Every number on screen is true of the toolkit: 16 kinds; the chart is the measured beat
lengths of the first show-tell film (anthropics/youtube/show-tell-claude-plugin-portal).
"""
import json
from pathlib import Path
HERE = Path(__file__).resolve().parent
SLUG = "claude-liam-brutalist-show-tell-cards"
TITLE = "Show-Tell: Drawings and Cards"

SPARSE_REASON = ("show-tell style (Bear, 2026-09-26): one drawn object or scene on a cream stage per beat, minimal "
                 "labels, the voice carrying the explanation. The negative space is the style, so only underfill and "
                 "clustered are waived; edge-bleed, empty-frame and contrast still apply.")


def beat(bid, narration, cls, image, show, sparse=True):
    b = {"beat_id": bid, "act": "show-tell", "lane": "manim", "proof_gate": "SHOW",
         "narration_text": narration, "estimated_duration_s": round(len(narration.split()) / 2.5, 1),
         "voice": "am_onyx", "engine": "kokoro",
         "shot": {"type": "GRAPHIC", "source": "own", "visual_intent": image, "show": show, "manim": {"class": cls},
                  "motion_claim": image}}
    if sparse:
        b["qc"] = {"sparse_by_design": True, "sparse_reason": SPARSE_REASON}
    return b


def remotion(bid, act, narration, pattern, props, show, gate="SHOW", lane="bookend", **extra):
    b = {"beat_id": bid, "act": act, "lane": lane, "proof_gate": gate,
         "narration_text": narration, "estimated_duration_s": round(len(narration.split()) / 2.5, 1),
         "voice": "am_onyx", "engine": "kokoro",
         "shot": {"type": "REMOTION", "source": "own", "show": show, "remotion": {"pattern": pattern, "props": props}}}
    b.update(extra)
    return b


def card(bid, narration, props, claim):
    return remotion(bid, "show-tell", narration, "ShowTellCard", props,
                    [{"at": 0.0, "event": f"{props['kind']} card, shot on twos"}], lane="card", motion_claim=claim)


# The first show-tell film's body beats, measured (actual_duration_s, rounded to 0.1 s).
FIRST = json.load(open(HERE.parents[3] / "anthropics/youtube/show-tell-claude-plugin-portal/beat_sheet.json"))
FIRST_BODY = [b for b in FIRST["beats"] if b["beat_id"].startswith("B0")]
LENGTHS = [round(float(b["actual_duration_s"]), 1) for b in FIRST_BODY]

B = [
 beat("B00", "Show-tell has one rule. Every beat gets one picture, and the voice does the explaining. The picture shows. The voice tells.",
      "B00_ShowTell", "A sealed kraft box drops onto the stage; beside it a row of voice bars grows and pulses; 'show' under the box, 'tell' under the bars.",
      [{"at": 0.1, "event": "box drops"}, {"at": 0.4, "event": "voice bars grow"}, {"at": 0.75, "event": "labels"}]),
 beat("B01", "Until now, every picture came from one kit of isometric drawings. Cardboard boxes, dark blocks, flat pages, all in Claude's colours.",
      "B01_Kit", "The box opens; two dark blocks rise out to the left and two flat pages to the right, each group labelled once.",
      [{"at": 0.1, "event": "lid lifts"}, {"at": 0.4, "event": "blocks rise"}, {"at": 0.65, "event": "pages rise"}]),
 card("B02", "Now there's a second choice: sixteen stop-motion cards. Same fonts, same colours, and every card is shot on twos, so each drawing holds for two frames, like paper under a camera.",
      {"kind": "dashboard", "heading": "Card kinds", "word": "16", "sub": "opt-in"},
      "The camera zooms onto one metric and it counts up from 0 to 16."),
 card("B03", "Each card is an interface you already know, moving the way it moves on screen. A player. Search. Tabs. A chart. A stack. A dock. Flowing paths. And more.",
      {"kind": "dock", "items": [{"label": l} for l in ["Player", "Search", "Tabs", "Chart", "Stack", "Dock", "Paths"]], "focus": 6},
      "A cursor sweeps a dock of seven card kinds; each icon swells and names itself as it passes."),
 card("B04", "The drawings stay the default. A card is optional. You choose, beat by beat, and a film can be all drawings, all cards, or a mix.",
      {"kind": "stack", "items": [{"label": "Per beat", "value": "you pick"}, {"label": "Card", "value": "optional"},
                                  {"label": "Drawing", "value": "default"}]},
      "Three choice cards spring in, fan out, settle, and the top one, 'Per beat', is ticked."),
 card("B05", "Pick a card when the idea is an interface. A search card types the query, then drops the results in one at a time, so the voice can say 'you ask, it returns' while it happens.",
      {"kind": "search", "heading": "show-tell cards",
       "items": [{"label": "Search card", "sub": "a query, then results"}, {"label": "Chart card", "sub": "bars become a line"},
                 {"label": "Dock card", "sub": "tools swell on hover"}]},
      "The query types letter by letter; three results drop in one at a time; the first is picked."),
 card("B06", "Pick one when the idea is a set of numbers. These are the beat lengths of the first show-tell film, in seconds. The bars grow, then melt into a line: the same numbers, a different shape.",
      {"kind": "chart", "heading": "Beat lengths, first film", "sub": "seconds", "values": LENGTHS,
       "labels": [b["beat_id"] for b in FIRST_BODY]},
      "Eight bars grow to the measured beat lengths, then melt into a line whose last point is tagged."),
 card("B07", "Or when the idea is a single word. The word fills from below, inside its own outline, while the voice says what it means.",
      {"kind": "masked", "word": "SHOW", "sub": "the voice tells"},
      "An outlined word fills with ink from the bottom up; a line under it rises with the fill."),
 card("B08", "Under the hood, nothing new. The beat sheet drives the audio, the Manim drawings and the cards, and all three meet in one master.",
      {"kind": "paths", "items": [{"label": l} for l in ["Sheet", "Audio", "Master", "Manim", "Cards"]], "focus": 2},
      "Edges draw from the sheet through audio, Manim and cards into the master; dots flow along them."),
 card("B09", "And the laws still hold. Labels stay at one to three words. Terracotta is an accent, never text. Type stays at forty-eight pixels or more. Every card moves on twos, with a flat paper shadow and no blur.",
      {"kind": "focus", "heading": "Card laws", "focus": 3,
       "items": [{"label": "Labels", "value": "1–3 words"}, {"label": "Accent", "value": "never text"},
                 {"label": "Type", "value": "≥ 48 px"}, {"label": "Frames", "value": "on twos"},
                 {"label": "Shadows", "value": "no blur"}]},
      "A lens slides down the table row by row as each law is spoken, stopping on 'Frames'."),
 beat("B10", "So mix them. Keep at least two drawn beats. Never put two cards of the same kind back to back. And choose a card only when its motion is the point.",
      "B10_Mix", "A film strip draws across the stage; a kraft box drops into one frame and a flat card drops into the next; a check appears.",
      [{"at": 0.15, "event": "strip draws"}, {"at": 0.4, "event": "box drops in"}, {"at": 0.6, "event": "card drops in"}, {"at": 0.85, "event": "check"}]),
]

OPEN = [
 remotion("BIDEA", "the question",
    "Kia ora. This is Liam, in for Bear. Show-tell used to draw every picture. So the question isn't whether every picture has to be a drawing. It's whether each picture earns its motion.",
    "BrutalistHesitantWriter",
    {"text": "Does every picture\nhave to be a drawing?", "triggerWords": "have to be a drawing", "replacementWords": "earn its motion",
     "fontSize": 70, "charMs": 22, "hesitateBetween": 6, "hesitateWithin": 1, "mistakeRate": 2, "jitter": 20,
     "seed": SLUG, "banner": ""},
    [{"at": 0.0, "event": "types 'Does every picture'"}, {"at": 0.55, "event": "'have to be a drawing' → 'earn its motion'"}],
    lead_silence_s=0.8, motion_claim="The writer types the naive question and corrects it to the real one: does the picture earn its motion.",
    qc={"sparse_by_design": True, "sparse_reason": "Hesitant-writer bookend: the correction is the motion."}),
 remotion("BDEFS", "terms",
    "Four terms. Show-tell: one picture per beat, and the voice explains. A beat: a sentence or two of narration, and the picture under it. A card: an interface picture, like a player, a chart or a search. And on twos: each drawing held for two frames, the way stop motion is shot.",
    "ClaudeDefinitions",
    {"title": "Terms In This Film",
     "terms": [{"term": "show-tell", "meaning": "one picture per beat; the voice explains"},
               {"term": "beat", "meaning": "a sentence or two of narration, and the picture under it"},
               {"term": "card", "meaning": "an interface picture: a player, a chart, a search"},
               {"term": "on twos", "meaning": "each drawing held for two frames, as stop motion is shot"}],
     "folderLabel": "@NikBearBrown"},
    [{"at": 0.12, "event": "'show-tell'"}, {"at": 0.35, "event": "'beat'"}, {"at": 0.55, "event": "'card'"}, {"at": 0.75, "event": "'on twos'"}], gate="CARD",
    qc={"sparse_by_design": True, "sparse_reason": "TERMS card: four prerequisites, one line each."}),
]
YT_PROMPT = ("I'm making a 90-second explainer about [your topic]. Plan it as a show-tell film: one picture per beat, "
             "six to ten beats. For each beat, write the one or two sentences the voice says, then choose the picture: "
             "an isometric drawing, or one card, but only if the idea is an interface, a set of numbers, or a single word. "
             "Say in one line how the picture's motion carries that beat's claim.")
YOURTURN = remotion("BHTF", "your turn",
    "Your turn. Paste this into Claude: " + YT_PROMPT + " Then check two things yourself. Does each picture move with the "
    "sentence it sits under? And is any beat just a slide of words? If it is, draw it again.",
    "ClaudeComposerAsk",
    {"greeting": "Your turn.", "topic": "CLAUDE · YOUR TURN", "segment": "Plan A Show-Tell Film", "command": YT_PROMPT,
     "runningText": "paste this into Claude…",
     "output": ["Check: each picture moves with its sentence.", "Check: no beat is a slide of words."],
     "folderLabel": "@NikBearBrown", "modelLabel": "Opus 5.5", "effortLabel": "High"},
    [{"at": 0.0, "event": "Composer opens — 'Your turn.'"}, {"at": 0.1, "event": "the prompt types in full"}, {"at": 0.8, "event": "two check lines land"}])

B = OPEN + B + [YOURTURN]
B.append({"beat_id": "BOUT", "act": "outro", "lane": "bookend", "proof_gate": "SHOW",
          "narration_text": f"{TITLE}. At Nik Bear Brown.", "estimated_duration_s": 4.0, "voice": "am_onyx", "engine": "kokoro",
          "shot": {"type": "REMOTION", "source": "own", "show": [{"at": 0.0, "event": "title restates; handle; mascot"}],
                   "remotion": {"pattern": "ClaudeTitleOutro", "props": {"title": TITLE, "slug": SLUG, "handle": "@NikBearBrown", "subline": ""}}},
          "kind": "outro_voice", "tail_silence_s": 1.0})

sheet = {"metadata": {
    "slug": SLUG, "title": TITLE, "topic": "BRUTALIST · SHOW-TELL", "skill": "show-tell", "style_preset": "show-tell",
    "channel": "claude-liam", "persona": "Liam (in for Bear)", "voice": "am_onyx", "voice_kokoro": "am_onyx", "engine": "kokoro",
    "clock": "narration", "palette": "claude", "register": "Teardown", "fps": 24, "aspect_ratio": "16:9", "width": 3840, "height": 2160,
    "caption_policy": "none", "greeting_language": "Māori (Kia ora)",
    "bookend_exempt": ["cold-open", "bvdt"],
    "bookend_exempt_reason": "show-tell style (Bear, 2026-09-26): opens on the hesitant writer + terms card, no verdict card; Your Turn is the Claude.ai composer; spoken outro stays.",
    "audience": "fellows and collaborators making explainer films with the brutalist.art toolkit",
    "source_doc": "brutalist.art/skills/make/show-tell/SKILL.md (Card family, 2026-09-27); runtime/remotion/src/scenes/ShowTellCard.tsx; Bear's reference sheet of 16 interface motion studies (2026-09-27)",
    "playlist": "Claude & Agentic AI", "chapter_number": 0,
    "tags": ["show-tell", "motion graphics", "stop motion", "Remotion", "Manim", "explainer video", "Claude", "brutalist.art", "Nik Bear Brown"]},
    "beats": B}

# Keep measured durations (and card durationSeconds) across re-runs of this script.
old = HERE / "beat_sheet.json"
if old.exists():
    prev = {b["beat_id"]: b for b in json.load(open(old))["beats"]}
    for b in B:
        p = prev.get(b["beat_id"])
        if p and p.get("narration_text") == b["narration_text"]:
            for k in ("actual_duration_s", "audio_file"):
                if p.get(k):
                    b[k] = p[k]
        if not b.get("audio_file") and (HERE / f"mp3/beat-{b['beat_id']}.mp3").exists():
            b["audio_file"] = f"mp3/beat-{b['beat_id']}.mp3"
for b in B:
    rem = b["shot"].get("remotion")
    if rem and b.get("actual_duration_s") and rem["pattern"] in ("ShowTellCard", "ClaudeDefinitions", "BrutalistHesitantWriter"):
        rem["props"]["durationSeconds"] = round(float(b["actual_duration_s"]), 3)
old.write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + "\n")
print(len(B), "beats; est", round(sum(b["estimated_duration_s"] for b in B)), "s; first-film lengths", LENGTHS)
