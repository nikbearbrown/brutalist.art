#!/usr/bin/env python3
"""make_sheet.py — beat_sheet.json for show-tell-claude-plugin-portal.

SHOW-TELL (new style, Bear 2026-09-26): "very simple direct explanations … every beat
needs an image … minimal text … the voice over explains." Every body beat is ONE drawn
illustration (Manim, Claude palette, isometric objects) with at most a few words of
label; Liam's narration carries the explanation. No composer cold open, no verdict or
your-turn cards (bookend_exempt); the spoken @NikBearBrown outro stays (never exempt).

Source: Anthropic's post "Build plugins for Claude with the directory submission portal"
(claude.com/blog/build-plugins-for-claude) + the ClaudeDevs post on X (the 110x figure).
"""
import json
from pathlib import Path
HERE = Path(__file__).resolve().parent
SLUG = "show-tell-claude-plugin-portal"
TITLE = "Claude Plugins: Package, Submit, Go Live"

def beat(bid, narration, cls, image, show):
    return {"beat_id": bid, "act": "show-tell", "lane": "manim", "proof_gate": "SHOW",
            "narration_text": narration, "estimated_duration_s": round(len(narration.split()) / 2.5, 1),
            "voice": "am_onyx", "engine": "kokoro",
            "shot": {"type": "GRAPHIC", "source": "own", "visual_intent": image, "show": show, "manim": {"class": cls},
                     "motion_claim": image}}

B = [
 beat("B00", "Start with the plugin itself. Picture it as a sealed box. What goes inside?",
      "B00_SealedBox", "A sealed cardboard box with terracotta tape drops onto the stage and settles; the word 'plugin' under it.",
      [{"at": 0.1, "event": "box drops in"}, {"at": 0.7, "event": "label"}]),
 beat("B01", "A plugin is a package. Inside go MCP connectors, which plug Claude into outside tools and data, and skills, which are written instructions Claude can follow. A plugin can carry either one, or both.",
      "B01_Unpack", "The lid lifts off; two dark MCP blocks rise out to the left and two skill pages to the right, each labelled once.",
      [{"at": 0.1, "event": "lid lifts"}, {"at": 0.3, "event": "MCP blocks rise"}, {"at": 0.6, "event": "skill pages rise"}]),
 beat("B02", "There are two ways to submit one. Way one is a single MCP connector. You point it at your own remote MCP server, and that's the submission.",
      "B02_Connector", "One MCP block on the left; a cable draws from its port to a server stack on the right, whose lights come on.",
      [{"at": 0.2, "event": "block"}, {"at": 0.5, "event": "cable draws to the server"}, {"at": 0.8, "event": "server lights"}]),
 beat("B03", "Way two is a plugin bundle. You put your MCP servers and your skills together in a GitHub repository, and you submit the repo.",
      "B03_Bundle", "An open box; an MCP block and two skill pages drop into it; a folder tag 'GitHub repo' clips onto the box.",
      [{"at": 0.2, "event": "open box"}, {"at": 0.45, "event": "parts drop in"}, {"at": 0.75, "event": "repo tag"}]),
 beat("B04", "You submit right inside Claude, from the directory's manage page, if you're a developer on a paid plan. The moment you hit submit, the plugin is checked and safety-scanned, so problems show up early.",
      "B04_Submit", "A Claude window with a Submit button; a cursor clicks it; a scan beam sweeps the plugin box and a shield with a check appears.",
      [{"at": 0.2, "event": "window + button"}, {"at": 0.45, "event": "click"}, {"at": 0.7, "event": "scan sweep, shield"}]),
 beat("B05", "Then you can track it. The portal shows where your plugin is in review, what the safety scan found, and any changes it recommends. Submitted. In review. Live.",
      "B05_Conveyor", "An isometric conveyor with three gates labelled Submit, In review, Live; the box rides through each gate and each turns terracotta with a check.",
      [{"at": 0.2, "event": "conveyor and gates"}, {"at": 0.65, "event": "Submit"}, {"at": 0.78, "event": "In review"}, {"at": 0.9, "event": "Live"}]),
 beat("B06", "Once it's live, you can see it being used: installs by product and version, how often your listing gets viewed, and which searches lead people to it.",
      "B06_Analytics", "A dashboard card: stacked bars grow (installs), a line climbs (views), three search pills point to the box (searches).",
      [{"at": 0.25, "event": "bars grow"}, {"at": 0.55, "event": "line climbs"}, {"at": 0.8, "event": "searches lead to the box"}]),
 beat("B07", "Why does this matter now? Claude's developer team says MCP usage across Claude products is up a hundred and ten times this year, and that plugins are becoming the way to build for Claude.",
      "B07_Growth", "A counter climbs from 1× to 110× while a growth curve sweeps up beside it.",
      [{"at": 0.3, "event": "counter climbs"}, {"at": 0.6, "event": "110×"}]),
]
def remotion(bid, act, narration, pattern, props, show, gate="SHOW", **extra):
    b = {"beat_id": bid, "act": act, "lane": "bookend", "proof_gate": gate,
         "narration_text": narration, "estimated_duration_s": round(len(narration.split()) / 2.5, 1),
         "voice": "am_onyx", "engine": "kokoro",
         "shot": {"type": "REMOTION", "source": "own", "show": show, "remotion": {"pattern": pattern, "props": props}}}
    b.update(extra)
    return b

OPEN = [
 remotion("BIDEA", "the question",
    "Hallo. This is Liam, in for Bear. Claude just opened a portal for plugins. So the question isn't only how you build one. It's how you get one live.",
    "BrutalistHesitantWriter",
    {"text": "What is a Claude plugin,\nand how do I build one?", "triggerWords": "build one", "replacementWords": "get one live",
     "fontSize": 70, "charMs": 22, "hesitateBetween": 6, "hesitateWithin": 1, "mistakeRate": 2, "jitter": 20,
     "seed": SLUG, "banner": ""},
    [{"at": 0.0, "event": "types 'What is a Claude plugin,'"}, {"at": 0.6, "event": "backspaces 'build one' → 'get one live' on the spoken correction"}],
    lead_silence_s=0.8, motion_claim="The writer types the naive build question and corrects it to the real one: getting a plugin live.",
    qc={"sparse_by_design": True, "sparse_reason": "Hesitant-writer bookend: the correction is the motion."}),
 remotion("BDEFS", "terms",
    "Three terms. MCP, the Model Context Protocol: an open standard that plugs Claude into outside tools and data. A skill: written instructions Claude loads to do one kind of task well. And a plugin: a package that carries MCP connectors, skills, or both.",
    "ClaudeDefinitions",
    {"title": "Terms In This Film",
     "terms": [{"term": "MCP", "meaning": "Model Context Protocol — an open standard that plugs Claude into outside tools and data"},
               {"term": "skill", "meaning": "written instructions Claude loads to do one kind of task well"},
               {"term": "plugin", "meaning": "a package that carries MCP connectors, skills, or both"}],
     "folderLabel": "@NikBearBrown"},
    [{"at": 0.12, "event": "'MCP' lands"}, {"at": 0.5, "event": "'skill' lands"}, {"at": 0.78, "event": "'plugin' lands"}], gate="CARD",
    qc={"sparse_by_design": True, "sparse_reason": "TERMS card: three prerequisites, one line each."}),
]
YT_PROMPT = ("I use [name a tool] every week. Help me plan a Claude plugin for it: one MCP connector that exposes only "
             "the two or three actions I actually need, and one skill that says when and how to use them well. "
             "List what the connector needs access to, and flag anything it should not expose. Don't write code yet.")
YOURTURN = remotion("BHTF", "your turn",
    "Your turn. Paste this into Claude: " + YT_PROMPT + " Then check two things yourself. Does every action trace to something "
    "you actually do with that tool? And does the connector reach anything the job doesn't need? If it does, cut it before you submit.",
    "ClaudeComposerAsk",
    {"greeting": "Your turn.", "topic": "CLAUDE · YOUR TURN", "segment": "Plan Your First Plugin", "command": YT_PROMPT,
     "runningText": "paste this into Claude…",
     "output": ["Check: every action traces to something you actually do.", "Check: nothing exposed that the job doesn't need."],
     "folderLabel": "@NikBearBrown", "modelLabel": "Opus 5.5", "effortLabel": "High"},
    [{"at": 0.0, "event": "Composer opens — 'Your turn.'"}, {"at": 0.1, "event": "the prompt types in full"}, {"at": 0.8, "event": "two check lines land"}])

SPARSE_REASON = ("show-tell style (Bear, 2026-09-26): one drawn object or scene on a cream stage per beat, minimal labels, with the voice carrying the explanation. The negative space is the style, so only underfill and clustered are waived; edge-bleed, empty-frame and contrast still apply.")
for b in B:
    if b["lane"] == "manim" and b["beat_id"] != "B02":   # B02 fills the frame on its own
        b["qc"] = {"sparse_by_design": True, "sparse_reason": SPARSE_REASON}
B = OPEN + B + [YOURTURN]
B.append({"beat_id": "BOUT", "act": "outro", "lane": "bookend", "proof_gate": "SHOW",
          "narration_text": f"{TITLE}. At Nik Bear Brown.", "estimated_duration_s": 4.0, "voice": "am_onyx", "engine": "kokoro",
          "shot": {"type": "REMOTION", "source": "own", "show": [{"at": 0.0, "event": "title restates; handle; mascot"}],
                   "remotion": {"pattern": "ClaudeTitleOutro", "props": {"title": TITLE, "slug": SLUG, "handle": "@NikBearBrown", "subline": ""}}},
          "kind": "outro_voice", "tail_silence_s": 1.0})

sheet = {"metadata": {
    "slug": SLUG, "title": TITLE, "topic": "CLAUDE · PLUGINS", "skill": "show-tell", "style_preset": "show-tell",
    "channel": "claude-liam", "persona": "Liam (in for Bear)", "voice": "am_onyx", "voice_kokoro": "am_onyx", "engine": "kokoro",
    "clock": "narration", "palette": "claude", "register": "Teardown", "fps": 24, "aspect_ratio": "16:9", "width": 3840, "height": 2160,
    "caption_policy": "none", "greeting_language": "German/Dutch (Hallo)",
    "bookend_exempt": ["cold-open", "bvdt"],
    "bookend_exempt_reason": "show-tell style (Bear, 2026-09-26): opens on the hesitant writer + terms card (Bear, 2026-09-26: 'add hesitant writer as the first beat and key terms like tldr uses as the second'), no verdict card; Your Turn is the Claude.ai composer; spoken outro stays.",
    "audience": "developers and builders who want to put their tools inside Claude",
    "source_doc": "claude.com/blog/build-plugins-for-claude (read 2026-09-26); ClaudeDevs post on X (110x); Bear's reference frames from the launch animation",
    "playlist": "Claude & Agentic AI", "chapter_number": 0,
    "tags": ["Claude plugins", "MCP", "Model Context Protocol", "Agent Skills", "Claude directory", "Claude", "Nik Bear Brown"]},
    "beats": B}
(HERE / "beat_sheet.json").write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + "\n")
print(len(B), "beats; est", round(sum(b["estimated_duration_s"] for b in B)), "s")
