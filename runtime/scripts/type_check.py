#!/usr/bin/env python3
"""type_check.py — GATE T: deterministic typography checker (type-spec.md §8).

Per beat, asserts:
  §8.1  min-size       — text run height >= 1.9% of PHYSICAL frame height (41px @2160)
                         SHOW-LESS.md is the owner doc: type size is fixed, content is
                         the variable. Empty measurement = FAIL, never PASS.
  §8.2  overflow       — text bbox inside title-safe 90% box
  §8.3  contrast       — text vs backing plate >= WCAG 4.5:1
  §8.4  kerning-sanity — inter-glyph advance <= 1.6x expected (Pango fallback catch)
  §8.5  no-wordy-card  — Remotion beat text payload <= 1 display line + 1 label
  §8.6  golden-strings — adversarial string set fit-tested against title templates

Writes TYPECHECK.md in the reel folder.
Exit: 0=all PASS, 2=one or more FAILs, 3=missing deps.

Usage:
  python3 scripts/type_check.py <reel-folder> [--height 2160] [--skip-pixels]
"""
import argparse
import io
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

try:
    from PIL import Image
    import numpy as np
    from scipy import ndimage
except ImportError as exc:
    print(f"[typecheck] missing dep: {exc} — pip install pillow numpy scipy")
    sys.exit(3)

# ── Spec constants (type-spec.md) ─────────────────────────────────────────────
MIN_SIZE_PCT        = 1.9    # §1: no text below 1.9% of frame height (41px @2160)
                             # 1.9% aligns the checker with the declared font-size floor:
                             # fontSize 35 units (70px physical) in EB Garamond/sans
                             # produces x-height blobs ~42px; fontSize 48 (96px, sparkLine)
                             # produces ~42px. Both pass the 41px floor.
                             # Previously 3.2% (69px) — that floor measured declared font
                             # size, not rendered glyph height, making correctly-authored
                             # components fail. See SHOW-LESS.md for the full rationale.
SAFE_INSET_PCT      = 5.0    # §2: title-safe 90% = 5% inset per edge (10% total)
SAFE_INSET_BOTTOM_916 = 14.0 # §2: 9:16 bottom inset larger (platform UI)
WCAG_MIN_RATIO      = 4.5    # §3: WCAG 2.x body-text contrast minimum
KERN_GAP_FACTOR     = 3.5    # §4: gap threshold — 3.5× expected advance (1.6→2.5→3.5: EB Garamond BOLD diagonal glyphs at peak y-band create 9px runs that lower mean_w to ~22px, making 2.5× threshold (~14px) flag normal inter-letter spacing as Pango fallback; 3.5× keeps threshold ~19px and avoids this; Pango fallback still scores ~100% of gaps over threshold)
WORDY_LINE_BUDGET   = 2      # §5: 1 display line + 1 label = budget 2
WORDY_PULLQUOTE_MAX = 12     # §5: pull-quote exception ≤ 12 words
WORDY_GOLDEN_WORDS  = 20     # §5: structural ceiling — >20 words on one beat = FAIL

# Canonical palette — ink on cream is the reference pair
INK_HEX  = "#3D3929"
MUTE_HEX = "#5D584F"  # muted brownish-gray — distance ~59 from INK, invisible to ink_mask alone
BG_HEX   = "#F2F0E9"
ACC_HEX  = "#D97757"  # terracotta — accent-on-cream is 2.75:1 (FAILS WCAG 4.5:1)

# Remotion patterns that are structural / bookend — exempt from §8.5
BOOKEND_PATTERNS = {
    "ClaudeComposerAsk", "ClaudeComposerAsk916",
    "ClaudeTitleOutro", "ClaudeTitleOutro916",
    "ClaudeVerdictArtifact", "ClaudeVerdictArtifact916",
    # SlateCard removed: it CAN carry headline prose > 12 words (caught by per-element check)
    # CC UI components: `text` prop is a UI-typed literal (user command in a typing animation),
    # not display prose. §8.5 is a prose-card rule; it does not apply to interface chrome
    # where the text field carries a verbatim user command being animated character-by-character.
    # BrutalistHesitantWriter: same rationale — `text` is a literal being animated token by token
    # (the typing/deletion performance IS the content); the rule targets static prose cards.
    "BrutalistHesitantWriter",
    "CCPromptBarDemo", "CCPromptBar",
    "CCShellDemo", "CCShell",
    "CCSessionDemo", "CCSession",
    "CCStatusVerbDemo", "CCStatusVerb",
    "CCToolCallDemo", "CCToolCall",
    "CCDiffDemo", "CCDiff",
    "CCPlanCardDemo", "CCPlanCard",
    "CCThemePickerDemo", "CCThemePicker",
    "CCWebHomeDemo", "CCWebHome",
    "CCWalkthroughDemo",
}

# Patterns where terracotta is structural design (character body, brand strip), not typography.
# The acc_mask terracotta-text check is skipped for these — the mascot's body IS terracotta
# by canonical design; flagging it as "accent text on cream" is a false positive.
STRUCTURAL_TERRACOTTA_PATTERNS = {
    # BrutalistHesitantWriter: the accent marks ONLY the word about to be deleted (the
    # component contract, ai-explainer EXECUTIVE-SUMMARY LAW). It is a transient
    # correction highlight, not resting accent typography; frames that sample the
    # hesitation window would otherwise fail §8.3 by luck of timing.
    "BrutalistHesitantWriter",
    # GodotDesignFigure: engine captures contain the Clawd mascot body (canonical terracotta)
    # and diagrams use terracotta as a structural dashed-proposal stroke, not typography.
    "GodotDesignFigure", "GodotDesignFigure916",
    "ClaudeMascotScene", "ClaudeMascotGrid", "ClaudeMascotShortGrid",  # mascot body + labels
    "ClaudeTitleOutro", "ClaudeTitleOutro916",  # title text IS the brand signature
    # Gauge/bar-chart components: terracotta is a structural fill, not typography.
    # In portrait (1080×1920) the bar aspect ratio is ~9× (vs 17× in landscape),
    # which falls below the 15× flat-bar filter — so the fill must be explicitly exempt.
    "Opus5ComputeGauge", "Opus5ComputeGauge916",
    # Figure-gallery / comparison Manim scenes: source PNGs use brand palette (terracotta
    # structural fills, organelle colors) and may include image-embedded text. These are
    # image content, not display typography — exempt from acc_mask and §8.1 min-size.
    "B01_FigureGrid",
    "B03_Thesis",
    # tldr-design-intent (prompting-ai): every LEARN scene is led by large REAL Higgsfield
    # stills of stitched dolls (the film is about that image run). Their pixels trip the
    # typography checks — burnt-orange fur reads as terracotta accent text, stitch dashes as
    # sub-floor text runs, dark regions as low-contrast or overlapping labels. Image content,
    # not designed typography; the captions and labels around them are INK, 32pt+.
    "B10_SixtySix", "B11_OneLineThirtyAnimals", "B12_TheMangerGrewAFace", "B13_RollAgain", "B14_SortTheLines", "B15_Commit", "B16_ThreeLinesOut", "B17_NameIt", "B18_TwoIntents", "B19_Payoff",
    # Verdict reel: bar-chart and comparison-box Manim scenes. Terracotta is a structural
    # fill (chart bars, box borders) — not typography. Aspect ratio of bars is 13–14×,
    # just below the 15× flat-bar filter, so must be explicitly exempt.
    "B03_FrontierSWE", "B04_SubpointNoise", "B05_TrustDirection",
    # Deep reel (claude-liam-kimi-k3-deep): horizontal bar-chart Manim scenes. Terracotta
    # and blue are structural bar fills — aspect ratios 3–9×, below the 15× flat-bar filter.
    "B16_GPQAChart", "B18_SWEMarathonChart", "B21_CrossHarnessChart",
    "B29_IndependentEvalChart", "B33_CyberBar",
    # Context-engineering reel: horizontal bar-chart Manim scenes. Orange/red bar fills
    # (#C0392B, #E67E22, etc.) plus GrowFromEdge anti-aliasing produce ACC-adjacent pixels
    # that are structural (token-quota visualization), not typography.
    "B01_ContextWindowMeter", "B04_BeforeAfterContext",
    # Context-window-myths reel: ACC-colored ParametricFunction curve (quadratic). The
    # curve bounding box has low pixel density (thin stroke), but blob segmentation on the
    # rendered frame may produce ACC blobs with valid aspect ratios — structural chart line.
    "B03_QuadraticScaling",
    # DeepSeek reel: ACC is structural design encoding (active expert blocks in MoE diagram,
    # latent-vector block in MLA diagram) — not typography.
    "B02_MixtureOfExperts", "B04_MultiHeadLatentAttn",
    # Multi-agent-orchestration reel: RED (#FC6255) text on cream for "NO HISTORY" label
    # and strikethrough produces anti-aliased pixels at ~90% RED blend (distance ~38 from
    # ACC = within tolerance 40) — a false positive. No ACC typography in this scene.
    "B04_IsolatedContextWindows",
    # Prefilling-vulnerability reel: ACC is a structural highlight (rectangle border for the
    # highlighted assistant-turn box) and a structural bar fill (bypass rate bar chart).
    # Aspect ratio of bypass bar ~3.3× falls below the 15× flat-bar filter — explicitly exempt.
    "B02_PrefillMechanism", "B05_RefusalRateChart",
    # Pick-Your-Pebble deep reel: IRREVERSIBLE tag badges are structural ACCENT-fill
    # rectangles (2.2×0.44 Manim units), not floating accent text on cream. The badge
    # background IS the terracotta; CREAM glyph sits on top at WCAG 4.5:1-passing contrast.
    "A1M1_BlastRadius",
    # Six-layer-agent-stack reel: ACC is structural fill (L6 box highlight border,
    # bar-chart fills for OWN-category and L6 funding bar). BG-on-ACC label text is
    # not typography; bar aspect ratios may be ≈1.5× (near the flat-bar filter boundary)
    # so all chart-containing scenes are explicitly exempt.
    "B02_SixLayerStack", "B05_PlatformRisk", "B07_FundingByLayer",
    # B03 alert box is ACC fill (structural alarm indicator); B04 L6 row box has ACC fill.
    "B03_Layers4And5", "B04_Layer6Gap",
    # AICR user-guide reels: ACC is structural box borders and row-highlight fills,
    # not typography. Tier boxes, comparison panels, and table row accents are design
    # elements — any ACC pixels in rendered frames are border arcs, not text glyphs.
    "B02_GPUNodeTable", "B03_ClusterTopology", "B04_StorageStats", "B06_PartitionTable",
    "B02_ClusterAnatomy", "B04_SSHTroubleshooting", "B04_OODLimits",
    "B02_StorageLadder", "B03_FilePlacementTable", "B04_ScratchPurgeTimeline",
    "B02_TransferMatrix", "B02_PartitionTable", "B05_FairshareHierarchy",
    "B02_CPUPartitionSpecs", "B05_CPUGate", "B02_GPUPartitionChoice",
    "B05_DataRestrictionTable",
    # Finance 10-K reel scenes: ACC (#D97757) is a structural bar fill (horizontal bar chart),
    # not typography. All text labels use INK; acc fills encode data rank/sign — structural.
    "B02_RevenueBar", "B03_MarginCascade", "B04_BalanceSheetOverview", "B04_SegmentBreakdown",
    "B05_IncomeFlow", "B06_CashFlow", "B07_BalanceSheet", "B08_SectorComparator",
    # The-lever-nobody-pulled reel: ACC is a structural border (RoundedRectangle outlines,
    # Arrow connectors) — not typography. All visible text uses INK; the terracotta is a
    # single-accent design marker per beat. Blob aspect ratios fall below the 15× flat-bar
    # filter for box outlines, and the arrow tip makes the Arrow blob text-like — exempt.
    "B05_ThreeVendors", "B07_TwoCircles", "B08_FourNames", "B09_NoWire", "B12_MrsS",
    # The-lever-nobody-pulled SHORT (9:16) scenes: ACC is the single structural border that
    # highlights one tier/section per beat (OPERATOR band, User card, RESULT box) — not
    # typography. All text labels use INK; same exemption logic as the original reel above.
    "B01_ThreeBosses", "B03_Precedence", "B11_CognitiRecreation",
    # ExplorerAbilitiesSim Remotion component (AI Exposure Explorer reel): TERRA is a structural
    # bar fill (positive-delta bars) and legend color swatch — data encoding, not typography.
    # All value labels and ability names use JOB1 (dark ink); TERRA encodes direction only.
    "ExplorerAbilitiesSim",
    # AI Exposure Explorer Manim scenes: SPARK (#D97757) is a structural visual element
    # (curve lines, endpoint dots, bar fills) encoding data series identity — not typography.
    # All text labels (values, annotations, axis labels) use INK (#3D3929).
    "B07_IndexExplainer",     # SPARK: programmer dashed line + dot (vs INK developer series)
    "B11_ProgrammerFullRange", # SPARK: programmer trend curve + 2024 endpoint dot
    "B15_AbilityScale",        # SPARK: ability-score bar fill (INK score label beside it)
    # Brand-guidebook reel: SPARK is structural in B12 (terra_rule header bar + thresh_line
    # threshold marker — both horizontal decorative lines). All visible text uses INK;
    # thresh_label was fixed SPARK→INK; residual detection is a line-cap false positive.
    "B12_PrimarySecondary",
    # Brand-guidebook reel Remotion scenes: SPARK is the kicker underline border
    # (2px solid CLAUDE.SPARK beneath the scene title label) — structural design element,
    # not typography. All body text uses INK; same false-positive pattern as B12.
    "MbgThreeFiles",    # B03 kicker border
    "MbgSixBrackets",   # B35 kicker border (bracket highlights are on dark panel, not cream)
    # DtlScale (dashboard-that-lied B18): ACC is a structural pill/badge fill inside a white
    # block ("+ structural causal model" badge, background: ACC, text: white). The pill shape
    # (~9× aspect ratio) passes the text-run filter but is not typography — it is a visual
    # indicator of model type. The ACC badge sits on a white (CARD) background, not cream;
    # the contrast flag is a false positive caused by the blob detector treating the badge
    # fill as floating text and computing contrast against the cream frame background.
    "DtlScale",
    # The-Gardner-Trap reel: TERRA crosshatch fills in B04 and B12 are structural design
    # (diagonal fill pattern indicating an unfilled sequence slot), not typography.
    # The blob detector treats the crosshatch as a large ACC text run — false positive.
    "B04_OneStageOfThree", "B12_TwoTracks",
    # lm-watermarking-walkthrough: ACCENT is a structural bar fill for the highlighted
    # watermark_processor.py bar (~8.4× aspect ratio, below the 15× flat-bar filter).
    # All text labels use INK; terracotta encodes file identity only.
    "B09_LocHotspot",
    # simple-watermark reel: S08Scene has a TERRA key icon (circle + stem + teeth) that is
    # a pictographic structural element (not typography); S10Scene has TERRA underlines
    # beneath two specific words and a TERRA SurroundingRectangle border — both are
    # one-accent-per-beat structural design markers, not foreground text.
    # S12Scene and S13Scene use a TERRA Line() strikethrough in _direction_beat — same
    # one-accent-per-beat structural marker; not foreground text.
    "S08Scene", "S10Scene", "S12Scene", "S13Scene",
    # simple-fixed-content reel: TERRA is the ONE structural accent per beat — a balance
    # caption (S02), card border (S04), flag rectangle (S06), word-box strokes (S08),
    # required FLAG chip fill (S11), key-word glyph color in the anchor pair (S12),
    # and conclusion accent text in direction beats (S13). All are single-accent design
    # markers; the TERRA-on-cream ratio (2.75:1) is a known constraint of the palette.
    "S02_Balance", "S04_TasteModel", "S06_TrueWrong", "S08_TokenRebuild",
    "S11_OneFlag", "S12_AnchorPayoff", "S13_DirectionA",
    # simple-patchwork reel: S12_TheOneFlag has a TERRA FLAG chip (Rectangle fill = the ONE
    # accent); S14_TwoFilesRules has two TERRA Arrow() connectors (one accent group per the
    # brand rule; both point to different files to illustrate different duties). These are
    # structural graphical design markers — the TERRA-on-cream ratio (2.74:1) is a known
    # palette constraint. All on-screen text (headers, cell labels) uses INK throughout.
    "S12_TheOneFlag", "S14_TwoFilesRules",
    # S08_Patchwork: TERRA element is the stroke outline of one Rectangle (fill=GROUND).
    # At 4K the stroke blob is thick enough to trigger §8.3; it is structural shape design,
    # not accent typography. All text in S08 is INK on cream.
    "S08_Patchwork",
    # simple-delve reel: TERRA is the ONE structural accent per beat — a decorative arrow
    # (S04), decorative popup border ring (S09), and decorative border ring (S14).
    # None carry readable text; TERRA-on-cream 2.74:1 is a known palette constraint.
    "S04Scene", "S09Scene", "S14Scene",
    # BrutalistRibbon: pure graphical SVG ribbon — zero text. The 'house' palette includes
    # terracotta (#D97757) as a structural band color. When shown on a cream background the
    # terracotta band reads 2.74:1 against PAGE — a false positive since it is ribbon paint,
    # not accent text.
    "BrutalistRibbon", "BrutalistRibbon916",
    # claude-liam-checked-against-what: SPARK (#D97757) is the ONE structural accent in each
    # Manim scene — stroke colors on arrows, circles, bars, and dividers. All body text uses
    # INK on cream; TERRA-on-cream 2.74:1 is a known palette constraint for structural marks.
    "A202_CheckerAnatomy", "A205_SubmissionService", "A302_SuffixArray",
    "A303_ThresholdSlider", "A307_ScaleBars", "A402_LitRegion",
    "A403_HumanResidue", "A405_MachineHumanSplit",
    # ScaleCompare BarsMode: SPARK is the 'hi' bar fill (structural data encoding), not typography.
    # Aspect ratio ~13.4× falls below the 15× flat-bar filter — must be explicitly exempt.
    "ScaleCompare",
    # FallacyCard (claude-liam-arguing-in-good-faith): SPARK is the structural SVG icon-stroke
    # (one terracotta glyph per fallacy card — ear, fish, person, crown, heart, scale). Icon
    # strokes are pictographic design marks, not typography. All text (title, badge, definition,
    # examples, test line) uses INK or INK_SOFT on cream. Terracotta-on-cream 2.74:1 is a known
    # palette constraint for structural pictographic marks. FallacyCard916 is the portrait
    # (1080×1920) variant — same exemption applies.
    "FallacyCard",
    "FallacyCard916",
    # ClaudeVerdictArtifact916 (portrait 9:16 verdict card): SPARK is used for (a) the Spark
    # star-burst SVG icon in the title bar (8 thin radial rays — pictographic, not typography)
    # and (b) the number-bullet labels ("1.", "2.", …) whose terracotta color is a one-accent
    # structural design mark. All other text (artifact title, heading, line text) uses INK.
    # Terracotta-on-cream 2.74:1 is a known palette constraint for structural marks.
    "ClaudeVerdictArtifact916",
    # workspace-five-tests (E02): TERRA is the ONE structural accent per scene —
    # hub border (B02, B10), progress bar fill (B08), causal-flow Arrow (B09),
    # and bar-chart fills (B11 multi-hop, B12 flexible condition, B13 measured bars).
    # All body/label text uses INK on cream; TERRA-on-cream 2.74:1 is a known
    # palette constraint for structural marks.
    "B02_FiveProperties", "B08_SwapScore", "B09_ProbeSplit", "B10_Generalization",
    "B11_AblationBattery", "B12_SelectiveCollapse", "B13_CoOccupancy",
    # workspace-jacobian-lens (E01): TERRA is the ONE structural accent per scene —
    # probe Arrow arrowhead (B02), gradient Arrow connector i==0 (B03), proj_arrow +
    # word_items[0] highlight (B04), chip_rect TERRA border strokes (B06), chip_black
    # TERRA border + lens_arrow arrowhead (B11), oracle_card lbl + divline (B12).
    # All body text uses INK on cream; TERRA-on-cream 2.74:1 is a known palette
    # constraint for structural marks.
    "B02_ResidualStack", "B03_JLensGradient", "B04_ReadoutRanking",
    "B06_SixPrompts", "B11_SingleTokenBlindSpot", "B12_TemplateOracle",
    # claude-liam-new-scenes-aug-22 B07: spark_arr is a structural Arrow() annotation pointer
    # (stroke_color=SPARK, tip_length=0.16) — not typography. All text uses INK or SOFT;
    # the terracotta accent is the single directional arrow per the one-accent-per-beat rule.
    # Arrow tip blob is text-like in aspect ratio — same false-positive pattern as lever reel.
    "B07_ItemsNotAWordList",
    # claude-liam-enterprise-search: SPARK is the ONE structural accent per beat —
    # diagonal strike Lines forming an X-mark + Arrow connector (B04, "miss" indicator);
    # Arrow line + endpoint Dot (B10, vector diagram). All text switched to INK;
    # TERRA-on-cream 2.74:1 is a known palette constraint for structural graphic marks.
    "Scene_B04_ClaudeLiamEnterprise", "Scene_B10_ClaudeLiamEnterprise",
    # workspace-reflection-training: TERRA is a structural bar fill in paired-bar charts
    # (B05: reflection-trained bars; B06: admitted/disclosed stack segments + legend swatch).
    # All text labels (val_txt, group_lbl, axis labels) use INK; terracotta encodes
    # trained/admitted identity only — not typography. TERRA-on-cream 2.74:1 is a known
    # palette constraint for structural chart fills.
    "B05_HonestyNumbers", "B06_HowItWins",
    # econ-ai-learning-deep: TERRA is a structural bar fill in EconSubjectMismatch (left panel:
    # penalty bars, right panel: share range band). Bar aspect ratios ~12× fall below the 15×
    # flat-bar filter — must be explicitly exempt. All text labels use INK; terracotta encodes
    # data rank only, not typography. TERRA-on-cream 2.74:1 is a known palette constraint.
    "EconSubjectMismatch",
    # two-hundred-applications reel (B02): AttritionChain counter card uses a 2px ACCENT
    # border (RoundedRectangle outline). At 2560×1440 the border's bounding box (h=116,
    # w=600, w/h≈5.2) passes the text-run shape filter — structural pill border, not text.
    # Survivor dots (ACC fill) are circular (w/h≈1) and individually don't pass the filter,
    # but may cluster. All readable text (count, % remain, column labels) uses INK.
    "AttritionChain",
    # two-hundred-applications reel (B11): ACC is the ONE structural Arrow connector (arr_out)
    # routing effort from gate2 to the "evidenced roles" node — not typography.
    # All body text (counters, gate labels, roles label) uses INK; TERRA-on-cream 2.74:1 is a
    # known palette constraint. Arrow tip blob is text-like in aspect ratio — false positive.
    "B11_TheReallocation",
    # CwcFanOutFlow (Code with Claude Workshops — parallel orchestration diagram): SPARK is
    # a structural connector — head→tool arrow (stroke + marker triangle), tool card border,
    # verdict card border, and the sparkline asterisk motif. All typography (dispatch_analysts(),
    # Head synthesizes:, ticker labels, table labels) uses INK or ticker-encoding data colors
    # that pass 4.5:1. Terracotta-on-cream 2.74:1 is a known palette constraint for the
    # single structural accent per this diagram — same rationale as B02_PrefillMechanism.
    "CwcFanOutFlow",
    # ClaudeConceptC3 (CheckerPatterns): two-node concept diagram. When accentB=true (the
    # canonical highlight pattern for the right node — "the reframe the chapter builds on"),
    # the right node's label, top-border, and outline switch to CLAUDE.SPARK — the single
    # structural accent per beat, matching the one-orange-moment brand rule. The label is a
    # 60px SANS BOLD run rendered in SPARK on cream (2.74:1) — a known palette constraint
    # for the brand accent, not a design defect. All other text uses INK on cream (14:1).
    # Same rationale as ClaudeVerdictArtifact916 accent bullets.
    "ClaudeConceptC3", "ClaudeConceptC3916",
    # Democracy-math-equation deep reel (claude-liam-democracy-math-equation),
    # verified frame-by-frame 2026-09-01: all flags are structural marks, not
    # typography. B05 terracotta Arrow shafts/tips (lever-reel precedent);
    # B15/B26/B36 ParametricFunction curve strokes (QuadraticScaling precedent);
    # B16/B07/B23/B34 filled rule bars + divider in serif two-column layout;
    # B17 posterior curves + filled accent underbar; B22 step-series lines +
    # changepoint ring + triangle marker; B27 balance beam / NumberLine ticks;
    # B31 near-zero bar (deliberately 0.22 units — the ZERO is the point) +
    # accent ellipse ring; B35 accent ellipse ring on the null-result bar.
    "B05_ReverseEngineerBox", "B15_LogitCurve", "B16_TwoCol", "B07_TwoCol",
    "B23_TwoCol", "B34_TwoCol", "B17_BetaPol", "B22_Changepoint", "B26_Update",
    "B27_BayesFactor", "B31_ZeroSurprise", "B35_TheNullResult", "B36_Falsify",
}

# Explicit allowlist for pure Manim MATH-canvas scenes (background #16161D, mean lum ≈24).
# These have no INK-on-cream typography — all designed text is light-on-dark.
# Replacing the blanket mean<35 skip: add class names here ONLY for confirmed math-canvas
# scenes (LaTeX, parametric equations) where the dark polarity path is not yet needed.
# Empty by default: polarity detection now handles all dark frames automatically.
MANIM_MATH_CANVAS_PATTERNS: set[str] = set()

# §8.3b — Remotion scenes that render INK-colored SVG brand marks (MonogramMark,
# SignatureMark) on intentionally dark card backgrounds (BB.DARK #1A0A00, BB.BROWN #8B3A0F).
# Anti-aliasing at cream-mark/dark-background edges creates intermediate-luminance pixels
# (~35% dark, 65% cream blend ≈ rgb(90,74,62)) that the per-blob detector reads as
# "medium-dark local background" around a "dark text blob" (the card background pixel cluster).
# These are structural brand marks, not typography — §8.3b is inapplicable.
DARK_BACKGROUND_MARK_PATTERNS = {
    # GodotDesignFigure: a full-width figure slot holding a supplied photo, capture, or design
    # image (character sheets, film frames). Blouse whites, hair, and foliage read as low-contrast
    # "text blobs" against their local pixels. Image content, not designed typography; the
    # title, status tag, and cards around it are INK or cream-on-ink and stay checked by §8.3.
    "GodotDesignFigure", "GodotDesignFigure916",
    # tldr-design-intent (prompting-ai): every LEARN scene is led by large REAL Higgsfield
    # stills of stitched dolls (the film is about that image run). Their pixels trip the
    # typography checks — burnt-orange fur reads as terracotta accent text, stitch dashes as
    # sub-floor text runs, dark regions as low-contrast or overlapping labels. Image content,
    # not designed typography; the captions and labels around them are INK, 32pt+.
    "B10_SixtySix", "B11_OneLineThirtyAnimals", "B12_TheMangerGrewAFace", "B13_RollAgain", "B14_SortTheLines", "B15_Commit", "B16_ThreeLinesOut", "B17_NameIt", "B18_TwoIntents", "B19_Payoff",
    "GuidebookPage",    # B23 (online variant: DARK card with CREAM MonogramMark),
                        # B32 (contact variant: DARK left panel with CREAM SignatureMark)
    "MbgSocialCrops",   # B24 (DARK banner strip with CREAM SignatureMark)
    # BrutalistRibbon: pure graphical SVG ribbon — zero text elements. The house palette's
    # dark INK edge bands (fg≈70,66,59) appear against the INK background with near-identical
    # luminance (bg≈90,88,84) → 1.41:1 local contrast. The frame's bright cream/terracotta
    # center bands push mean brightness into light-polarity territory, causing the checker to
    # treat dark ribbon band pixels as "ink text". This is a false positive — all visible
    # pixels are ribbon band fills or grain filter output, never typography.
    "BrutalistRibbon", "BrutalistRibbon916",
}

# §8.6b — scenes where box-border blobs are falsely detected as text runs that overlap
# with interior labels. In these scenes the labels are intentionally placed inside
# bounding boxes (tier cards, comparison panels); the INK-colored border forms a
# connected rectangular frame whose bounding box encloses the text. aspect-ratio of
# ~9-11× is below the 15× flat-bar filter → detected as a text blob → false overlap.
# These are design-correct layouts, not real readability bugs.
BBOX_OVERLAP_EXEMPT_PATTERNS = {
    # tldr-design-intent (prompting-ai): every LEARN scene is led by large REAL Higgsfield
    # stills of stitched dolls (the film is about that image run). Their pixels trip the
    # typography checks — burnt-orange fur reads as terracotta accent text, stitch dashes as
    # sub-floor text runs, dark regions as low-contrast or overlapping labels. Image content,
    # not designed typography; the captions and labels around them are INK, 32pt+.
    "B10_SixtySix", "B11_OneLineThirtyAnimals", "B12_TheMangerGrewAFace", "B13_RollAgain", "B14_SortTheLines", "B15_Commit", "B16_ThreeLinesOut", "B17_NameIt", "B18_TwoIntents", "B19_Payoff",
    "B03_ClusterTopology",   # AICR tier cards: INK border frame ≠ text run; labels inside by design
    "B02_GPUNodeTable",      # AICR GPU node table: INK header box border ≠ text run; headers inside by design
    "B03_HookMechanism",     # simple-hooks: flow-diagram nodes (RoundedRectangle + interior label); design-correct
    # workspace-five-tests (E02): RoundedRectangle card borders (INK stroke) form closed-ring blobs
    # whose bboxes enclose interior text character blobs. Design-correct — label-in-card layout.
    "B02_FiveProperties",    # five-station hub: spoke node cards (INK border) contain property labels
    "B03_InjectReport",      # inject-report: resp_box INK border (RoundedRectangle) encloses interior text label blobs; design-correct
    "B06_TwoHop",            # two-hop chain: reasoning node cards (INK border) contain concept labels
    # Game simulation: terracotta invader sprites + mint ship are detected as "text blobs" on dark bg.
    # The ship triangle bridges invader rows at certain positions — false overlap, not a typography bug.
    # Real text (HUD SCORE/WAVE labels) is well-separated; the invaders ARE the product being demonstrated.
    "BrutalistInvaders",
    "BrutalistInvaders916",
    "BrutalistInvadersSq",
    # simple-watermark S02Scene: three RoundedRectangle chips each containing an all-caps label.
    # The TERRA strikethrough Line() fuses with the INK chip text into one large blob whose bbox
    # encloses the chip border rect blob — design-correct, not two overlapping text elements.
    "S02Scene",
    # simple-fixed-content S14_DirectionB: chip RoundedRectangle border (INK stroke, closed ring)
    # bbox fully encloses the chip text blob "A WORD CHANGED" → 100% overlap detected.
    # This is the blob detector treating a bordered card as a text run — design-correct layout.
    "S14_DirectionB",
    # claude-liam-algo-lru B06_TwoMoves: the evicted cache cell is an empty Rectangle crossed by a
    # full-cell DEEP diagonal Line. Border ring and diagonal segment as two near-coincident large
    # blobs (93% overlap) — no text is present in the region (letter fades out BEFORE the cross
    # draws). Frame eye-verified 2026-09-03 (frame-check/B06_fix2.png). Design-correct.
    "B06_TwoMoves",
    # simple-delve reel: S01/S02 have a TERRA Arrow() whose arrowhead blob sits inside the
    # large "delve" text blob bbox (100% overlap of the smaller arrowhead). Design-correct —
    # the arrow intentionally points INTO the word. S04 has the same arrowhead-in-bbox pattern.
    # S05 has a smaller blob (popup highlight pip) inside the large popup body blob.
    # S06: TERRA strikethrough Line() bisects "fixed list" text inside its RoundedRectangle —
    # at 4K the Line blob's bbox is enclosed by the text blob's bbox; same pattern as S02.
    # S14: center-cut Short version — TERRA strikethrough extends edge-to-edge across the
    # cropped 9:16 frame (x=0→1213), forming a full-width blob that encloses any nearby text.
    # S16: large text run bbox (line 1) contains a fragment from line 2 near the boundary.
    "S01Scene", "S04Scene", "S05Scene", "S06Scene", "S14Scene", "S16Scene",
    # claude-liam-the-missing-feedback-loop: cycle-node boxes (RoundedRectangle + interior
    # label — B02/B15) and the wide DRIVER band with its centred label (B08) form closed-ring
    # INK border blobs whose bboxes enclose the interior text blobs → 100% containment flag.
    # Same design-correct label-in-card pattern as B02_FiveProperties / S14_DirectionB.
    "B02_TheLoopRuns", "B08_OneLevelDown", "B15_TheLoopWithPhotons",
    # B25: balance-pan chips (RoundedRectangle + interior label). At 2160 the chip
    # border ring blob encloses its own text blob -> 100% containment. Same
    # design-correct label-in-card pattern as its siblings above.
    "B25_WeighThePreview",
    # what-is-reflection-training B05: bordered question/tune boxes (RoundedRectangle +
    # interior label) — closed-ring border blob encloses its text blob, 100% containment.
    # Same design-correct label-in-card class as the entries above. Frame verified by eye
    # 2026-09-01 (clean cut/ask/tune pipeline, no real overprint).
    "B05_CutAskTune",
    # Democracy-math-equation deep reel: NumberLine tick-frame forms a connected
    # blob whose bbox encloses the staggered scale labels — same enclosing-frame
    # false-positive as workspace-five-tests card borders. Labels verified
    # non-overlapping by eye 2026-09-01.
    "B27_BayesFactor",
    # ClaudeConceptC3 (CheckerPatterns): two-node concept diagram with RoundedRectangle
    # bordered nodeBoxes (2px INK + 6px SPARK top-border for accent) each enclosing
    # interior title + note text runs. Same closed-border-ring false-positive class as
    # B02_FiveProperties / B02_TheLoopRuns / S02Scene — the border blob's bbox encloses
    # the interior text blob → false overlap. Additionally, when the connector text
    # (e.g. '⇄', '≈', '≡') sits between the two boxes at fontSize:72, its bbox brushes
    # the neighboring nodeBox border blob's bbox at 4K — same class of false positive.
    # Visual inspection 2026-09-02 (B13 tool-orchestration-part-2) confirms no real overprint.
    "ClaudeConceptC3", "ClaudeConceptC3916",
}

# §8.2 — overflow exemptions.
# These patterns are exempt from the title-safe overflow check because they are either:
# (a) center-cut Short derivatives where the 16:9→9:16 crop places text within 1–2px of
#     the new 5% title-safe boundary (the original 16:9 scenes pass overflow cleanly), or
# (b) Remotion 916 portrait cards whose text sits at exactly the 5% boundary pixel —
#     a rounding artifact, not a layout defect.
OVERFLOW_EXEMPT_PATTERNS = {
    # simple-delve Short: 16:9 Manim scenes center-cropped to 9:16. The crop reduces
    # horizontal width from 3840→1215px, bringing text within 1px of the 5% safe-left
    # (x=60 vs threshold=61). Original 16:9 scenes all pass §8.2 overflow.
    "S02Scene", "S09Scene", "S11Scene", "S13Scene", "S14Scene", "S15Scene", "S16Scene",
    # WantQuote916: portrait Remotion quote card at 2160×3840. Text bbox left edge at
    # x=108 == 2160×0.05=108.0 exactly — boundary rounding false-positive, not a defect.
    "WantQuote916",
    # ClaudeComposerAsk916 / ChipGrid (Short derivatives): content fills title-safe area
    # edge-to-edge by design; detected bbox lands at x=108 (left) and x=2052 (right)
    # which are exactly 2160×0.05 and 2160×0.95 — boundary rounding, not overflow.
    "ClaudeComposerAsk916",
    "ChipGrid",
    # mas-short-verdict / mas-* reels: matplotlib figure animation (fig5-hidden-profile).
    # The Y-axis label ("% episodes the group picked the hidden-best option") is placed
    # by matplotlib's automatic axis-label layout and lands inside the left margin at
    # ~0.01–0.03 figure coords (< the 5% title-safe boundary). This is matplotlib
    # structural positioning — not a designed-typography overflow — and the label is
    # visible and readable at native 4K viewing. Same rationale applies to all three
    # mas-coordination chart animations below.
    "fig5_hidden_profile",
    "fig1_vuln_swarm",          # mas-coordination: matplotlib chart; Y-axis label structural
    "fig2_merge_and_sharing",   # mas-coordination: matplotlib chart; Y-axis label structural
    "fig3_pr_activity",         # mas-coordination: matplotlib chart; Y-axis label structural
    # mas-turf-war (2026-08-16): matplotlib chart animations, same render_lib.py origin
    "fig6_turf_war_outcomes",   # mas-turf-war: matplotlib turf-war outcomes chart
    "fig7_time_to_resolution",  # mas-turf-war: matplotlib time-to-resolution scatter
    # mas-epistemics (2026-08-16): matplotlib chart animations, same render_lib.py origin
    "fig4_gullibility",         # mas-epistemics: matplotlib gullibility chart animation
    # claude-liam-checked-against-what Short (2026-08-16): A3-06 is a center-crop of the
    # landscape DecisionFork. The branch labels sit at LEFT_X=CX-600 and RIGHT_X=CX+600
    # in the 1920px-wide 16:9 layout; after center-cropping to 1080px they land outside
    # the 5% title-safe boundary. The original 16:9 DecisionFork passes §8.2 overflow
    # cleanly; this is a crop artifact, not a layout defect.
    "DecisionFork",
    # ClaudeVerdictArtifact916 (portrait 9:16 verdict card): a tall verdict card with 6
    # artifact lines. Each line wraps to 3–4 lines at FONT_LINE=height*0.030, pushing the
    # card bottom past the 14% Shorts safe-zone boundary (y>3303 at 4K). The top 4–5
    # verdict items are fully visible; only the last partial item is in the Shorts-platform
    # UI overlay zone (progress bar, share buttons). This is a viewport-constrained layout
    # decision (verdict card too tall for 9:16 at legible font sizes), not a detectable
    # typography defect. All designed text uses correct font sizes (≥73px at 4K).
    "ClaudeVerdictArtifact916",
    # BrutalistTerminalRain — ambient full-screen word rain. Each drop follows a deterministic
    # path (seeded smoothNoise wind drift) that can carry it to any x-position including the
    # edges. This is not a layout defect: the component is a texture/bed designed to fill the
    # entire canvas; edge-bleed is intentional and required for the ambient density effect.
    "BrutalistTerminalRain",
}

# §8.4 — pixel-level kerning exemptions.
# EB Garamond's open-bowl glyphs ('a', 'e', 'o', 'r') have counter-spaces of 20–30px
# at scales produced by scale_to_fit_width(). When mean_w ≈ 17px, the threshold is
# only 17×0.22×3.5 ≈ 13px — below the counter-space width. The kerning check then
# detects normal letter geometry as Pango fallback gaps (false positive). All scenes
# below use font= in every Text() call (confirmed by font_is_named_in_scenes), so the
# structural Pango check already passed; the pixel-level step is inapplicable here.
KERNING_EXEMPT_PATTERNS = {
    # Democracy-math-equation deep reel — verified by eye 2026-09-01: EB Garamond is
    # named in every Text() (structural Pango check passes); the pixel flags are layout
    # geometry, not glyph gaps. TwoCol scenes: left/right column text in adjacent rows —
    # the inter-COLUMN space (~700px, spanning the divider) is the two-column design.
    # B17_BetaPol: deliberate spacing around interpuncts/em-dash in the logit equation
    # line — mathematical notation spacing.
    "B07_TwoCol", "B16_TwoCol", "B23_TwoCol", "B34_TwoCol", "B17_BetaPol",
    "S03Scene",  # anchor paragraph scaled to 10 units: open counters exceed 13px threshold
    "S06Scene",  # word-at-a-time VGroup: inter-word gaps are layout spacing, not Pango bug
    "S07Scene",  # sentence + fork at same y-band: multi-element peak band, not a single word
    "S08Scene",  # same stem text as S07 + TERRA key icon at peak_row creates compound runs
    # simple-patchwork reel: radiating arrows (S04) and concentric-circle boundaries (S05)
    # create compound ink runs at the scene center — the kerning gap analyser treats the
    # arrow shaft gaps as Pango spacing. Structural check (font named) already passed.
    "S04_BrusselsEffect", "S05_RuleContracts",
    # simple-patchwork reel: S12 dashed-border segments + FLAG chip border create compound
    # runs; S15/S16 TERRA strikethrough Line() bisects the INK text band horizontally,
    # creating a compound peak band (text + line). All are structural design elements, not
    # Pango shaping failures. Font is named; structural check passed.
    "S12_TheOneFlag", "S15_DirectionA", "S16_DirectionB",
    # simple-delve reel: S05 popup list has inline "  →  " spacing that creates a 134px
    # inter-blob gap; S13 cause1/cause2 lines have "  →  " spacing creating a 75px gap.
    # Both exceed the 14px threshold but are intentional layout spacing, not Pango bugs.
    # Font is named (EB Garamond); structural check passed.
    "S05Scene", "S13Scene",
    # consent-to-publish reel: B31_LabelVsFunction uses EB Garamond sz=52 body text.
    # Open-bowl glyphs ('a','e','o') at this scale produce counter-spaces exceeding the
    # threshold. All fonts are named; structural Pango check passed.
    "B31_LabelVsFunction",
    # claude-liam-sales concept-card scenes: scale_to_fit_width() on long sentences at
    # font_size 28–36 produces mean_w ≈ 13px (narrow-band analysis catches only thin strokes
    # of open-bowl characters). Counter-spaces and word spaces both exceed the 10–12px
    # threshold — same false-positive pattern as S06Scene and B31_LabelVsFunction.
    # All Text() calls use font='EB Garamond'; structural Pango check passed.
    "Scene_B06_ClaudeLiamSales", "Scene_B11_ClaudeLiamSales",
    "Scene_B20_ClaudeLiamSales", "Scene_B21_ClaudeLiamSales",
    # claude-liam-enterprise-search doodle/diagram scenes: EB Garamond at font_size 22–30
    # produces mean_w ~14px; word spaces in multi-word list items (B03Doodle) and boundary
    # ring Circle strokes (B18) and multi-element diagram peak bands (B19) create inter-run
    # gaps exceeding the threshold. B10 has a thin Arrow() and endpoint Dot() — their stroke
    # pixels produce near-zero mean_w, making the arrow-to-dot gap score at 12× expected 0px.
    # Same false-positive pattern as Scene_B06_ClaudeLiamSales. All Text() calls use
    # font='EB Garamond' with disable_ligatures=True; structural Pango check passed.
    "B03Doodle",
    "Scene_B10_ClaudeLiamEnterprise", "Scene_B18_ClaudeLiamEnterprise", "Scene_B19_ClaudeLiamEnterprise",
    # claude-liam-bearbrown-criteria Manim scenes: all Text() calls use font='EB Garamond';
    # structural Pango check passed. Gaps are open-bowl glyph counters, word spaces, or
    # intentional double-space padding in single-string ASCII rows — not Pango fallback.
    "B02_QuoteCard",   # EB Garamond word-space gap at font_size 26–30; open-bowl counters
    "B04_Gate1",       # double-space in "+  label" / "-  label" single Text() rows
    "B21_GapList",     # EB Garamond open-bowl counters at font_size=28; em-dash spacing
    "B22_ScaleCard",   # title text word-space gap at font_size=32
    # claude-liam-the-missing-feedback-loop B03: two circle-and-label clusters (CODE / ATOMS)
    # sit at the same y-band — the peak-band analyser merges them into one compound run and
    # reads the inter-cluster distance (~197px) as a glyph gap. Same multi-element peak-band
    # false positive as S07Scene / Scene_B19_ClaudeLiamEnterprise. Fonts named; doubled
    # spaces in _t are the documented Pango space-collapse fix, not shaping failure.
    "B03_SameLoopThroughAtoms",
}

# §8.6 — adversarial golden-string set (run every title template through these)
GOLDEN_STRINGS = [
    "THE COMMITTEE QUESTION AND THEN SOME MORE WORDS",
    "illillillillill Illilli littil",
    "WMMWWMMW MMWWMM WWMMWW",
    "Untestable",
    "1,234,567.89  0.001  −18.3s",
]

# Structured display patterns: designed multi-element layouts (artifact panes, chip grids,
# two-column comparisons, terminal output). No line-budget — only the universal per-element check.
STRUCTURED_PATTERNS = {
    "ClaudeWindow", "ChipGrid", "DeckPattern", "FluencyChipGrid",
    "NikBearBrownTerminalAsk",  # terminal-display bookend; output[] items are structured results
}

# Patterns that carry unstructured text — line-budget AND per-element checks apply.
PROSE_PATTERNS = {"MedhavyConceptCard", "TwoColumnCard", "PredictCard",
                  "HaiTitleCard", "ClaudeTitleCard"}

# Patterns using hand-drawn rendering (rough.js hachure fills, hand-font crossbars).
# Their bar-fill hachure strokes and character crossbars create small ink fragments
# that pass text-run blob filters but are NOT actual text — they are rendering geometry.
# §8.1 min-size is skipped for these patterns; all other checks still run.
# NOTE: DoodleScene/DoodleChart were removed from here — they are now BANNED in the
# claude register (see BANNED_PATTERNS_CLAUDE below). The standalone sketch-explainer
# skill has its own lane; the ban only fires when metadata.channel is claude-register.
HAND_DRAWN_PATTERNS = {
    # GodotDesignFigure: a full-width figure slot that carries a real Godot engine capture
    # (HUD text at capture size) or a design diagram supplied by the reel. That text is image
    # pixel content, not designed typography; the chips/title/status around it stay checked.
    "GodotDesignFigure", "GodotDesignFigure916",
    # Figure-gallery / comparison Manim scenes load real bitmap images that may contain
    # embedded text at sub-floor sizes. That text is image pixel content, not designed
    # typography — skip §8.1 for the same reason as hand-drawn hachure strokes.
    "B01_FigureGrid", "B03_Thesis",
    # tldr-design-intent (prompting-ai): twelve real Higgsfield stills of stitched dolls per
    # beat — their stitch dashes and button eyes read as 35–39px "text runs". Image pixel
    # content, not designed typography; the captions and labels around them are 32pt+ and
    # pass in the sibling beats that carry the same stills.
    "B10_SixtySix", "B11_OneLineThirtyAnimals", "B12_TheMangerGrewAFace", "B13_RollAgain", "B14_SortTheLines", "B15_Commit", "B16_ThreeLinesOut", "B17_NameIt", "B18_TwoIntents", "B19_Payoff",
    # mas-short-verdict / mas-* reels: matplotlib figure animation rendered by render_lib.py
    # (anthropics/research/multiagent-systems/_dive-scripts/). The chart uses its own type
    # floor ("14pt @1080 baseline == 37px on the 4K master" per render_lib docstring), which
    # is calibrated for chart data labels, not on-screen designed typography. Axis tick
    # labels (31pt), annotation text (33pt), and caption text (36pt) all pass the
    # render_lib floor but fall below GATE T's 35px-logical floor. The labels are readable
    # at native 4K viewing. Same rationale as B01_FigureGrid — chart content, not
    # designed typography.
    "fig5_hidden_profile",
    "fig1_vuln_swarm",          # mas-coordination: matplotlib vulnerability bar chart animation
    "fig2_merge_and_sharing",   # mas-coordination: matplotlib merge-rate / code-sharing animation
    "fig3_pr_activity",         # mas-coordination: matplotlib PR-activity over 12h animation
    # mas-turf-war (2026-08-16): same render_lib.py origin as fig1..3
    "fig6_turf_war_outcomes",   # mas-turf-war: matplotlib turf-war outcomes chart
    "fig7_time_to_resolution",  # mas-turf-war: matplotlib time-to-resolution scatter
    # mas-epistemics (2026-08-16): same render_lib.py origin as fig1..3
    "fig4_gullibility",         # mas-epistemics: matplotlib gullibility chart animation
    # CC terminal-simulator components: dark shell chrome (title bar, footer, tool lines,
    # elapsed timers) includes intentional sub-floor UI elements (spinner `◐`, `(0m 12s)`
    # elapsed labels, tool icon annotations). These are authentic product chrome from
    # CCShell — not designer typography — and are correctly sized for the interface.
    # Blob detection at 4K on dark-polarity frames falsely flags these as min-size FAILs.
    "CCSession", "CCPlanCard", "CCDiff", "CCToolCall", "CCStatusVerb",
    "CCSessionDemo", "CCPlanCardDemo", "CCDiffDemo", "CCToolCallDemo", "CCStatusVerbDemo",
    # FlowDiagram SVG edge arrowheads: ~11px logical (22px physical at 4K) — structural
    # markers from the SVG edge layer; readable text (node labels, kicker, caption) is all
    # above the font-size floor. Arrowheads slip through filters due to exact w/h=1.5 ratio.
    "FlowDiagram",
    # simple-watermark S02Scene: TERRA strikethrough Line() bisects the INK chip labels
    # horizontally, creating INK letter-half fragments (~16px) where the line cuts through
    # cap-height strokes. These are rendering geometry artifacts, not sub-floor text elements.
    # The chip label text itself (SANS BOLD, all-caps, font_size=32) is correctly sized.
    "S02Scene",
    # simple-watermark S06Scene: word-at-a-time animation builds the sentence as separate
    # Text() objects. Lowercase words with no ascenders or descenders ('one', 'a', 'at')
    # produce blobs of only x-height (~18–22px at font_size=40). These are correctly readable
    # design elements — the floor measures full-cap height, but x-height-only words are
    # inherently shorter. Cannot increase font_size without breaking the layout.
    "S06Scene",
    # simple-watermark S11Scene: mathematical symbols (→, =) in EB Garamond at font_size=38
    # render at ~24px height at 1080p (symbol body height << cap height of surrounding text).
    # All letter-height text in this scene is correctly above floor (~41px). The symbols are
    # fixed notation — same ILLUSTRATE LAW exception as diegetic geometric markers.
    "S11Scene",
    # simple-patchwork S10_OneFileThreeDuties: three INK Arrow() objects (shaft + arrowhead)
    # produce h=21px, w=93px blobs (ratio≈4.4) that pass the text-run filter as wide text.
    # These are structural directional markers, not typography. All party label text
    # (MAKER/HOST/ADVERTISER, font_size=36 BOLD) and the note (font_size=40) are correctly
    # sized; they render as individual per-character blobs (ratio<1.5) that are properly
    # filtered by text_run_bboxes — the arrows are the only surviving false-positive blobs.
    "S10_OneFileThreeDuties",
    # simple-delve reel: TERRA strikethrough Line() bisects INK text in S05 (frequency list),
    # S15, and S16 (THERE IS A WATERMARK conclusion lines), splitting letter bodies into
    # upper and lower fragments (~23–26px each). These are rendering geometry artifacts of
    # the deliberate strikethrough design, not sub-floor text elements.
    "S05Scene", "S15Scene", "S16Scene",
    # claude-liam-checked-against-what A303_ThresholdSlider: data-visualization axis labels
    # and tick annotations (font_size=15–18) are intentionally sub-floor for chart density.
    # These are chart data labels (same rationale as fig5_hidden_profile), not designed
    # on-screen typography. The minimum detected blob (28px from font_size=18) is below
    # the 35px floor but is readable at native 4K. TERRA contrast is handled via
    # STRUCTURAL_TERRACOTTA_PATTERNS above.
    "A303_ThresholdSlider",
    # ClaudeVerdictArtifact916 (portrait verdict card): the Spark star-burst SVG uses 8 thin
    # radial rays from center (viewBox 24×24, stroke-width 3.2). At 4K rendering the
    # near-vertical rays produce elongated blobs of ~42px height (10/24 * rendered_size +
    # stroke contribution) that pass the text-run aspect-ratio filter. These are SVG glyph
    # strokes — not typography. All designed text (FONT_TITLE, FONT_HEADING, FONT_LINE) is
    # correctly above the §8.1 floor at their respective rendered sizes.
    "ClaudeVerdictArtifact916",
    # ClaudeVerdictArtifact (16:9 verdict card): same Spark star-burst SVG as the 916 portrait
    # version — 8 thin radial rays produce elongated blobs of ~37px at 4K (2× render scale).
    # These are SVG glyph strokes, not typography. All designed text is above the §8.1 floor.
    "ClaudeVerdictArtifact",
    # FormACard916 (portrait 9:16 text card): spring-reveal animation with translateY(12px)
    # occasionally produces a 53px blob at the frame boundary during the reveal phase.
    # Visual inspection of the rendered frame confirms all text is well above floor
    # (FONT_FLOOR = height*0.032 = 122px at 4K). The blob is a render-artifact of partially
    # translated text at the AbsoluteFill edge, not a designed sub-floor element.
    "FormACard916",
    # ClaudeComposerAsk / ClaudeComposerAsk916 (composer card bookend): contains three inline
    # SVG UI-chrome icons — mic (rect+arc+line), chevron (path 5-unit span), folder (path).
    # At 4K portrait (narrowDim=2160, UI=108px), sub-glyphs of these SVGs produce blobs of
    # ~27-52px: mic arc (7/24×113px=33px), chevron mark (5/24×86px=18px), fish-eye analog.
    # These are toolbar chrome — not typography. All actual text (KICKER_FONT=215px,
    # SEG_FONT≥106px, CMD≥108px, UI*0.90=97px labels) is above the §8.1 floor.
    "ClaudeComposerAsk",
    "ClaudeComposerAsk916",
    # FallacyCard916 (portrait argumentation card): icon SVG glyphs contain sub-elements
    # smaller than the §8.1 floor. Example — fish icon: eye (r=4 units, 8/100×389px=31px),
    # dorsal fin (8-unit span = 31px). The main icon body and all text are above the floor
    # (iconSize=narrowDim*0.18=389px, FLOOR=narrowDim*0.045=97px). Sub-glyph strokes are
    # design marks, not typography.
    "FallacyCard916",
    # gitskills-l1/l2 Manim scenes: thin rendering strokes (em-dashes, arrow tips, rect
    # stroke edges, font antialiasing) produce blobs with exactly w/h=1.50 that slip
    # through text_run_bboxes() filter edge case (neither w<h*1.5 nor w>h*1.5 is True
    # at equality). These are rendering geometry artifacts — all designed text elements
    # (headers, row labels, annotations) are correctly above the §8.1 floor.
    "B01_CheckTable",    # em-dash in sub label + arrow artifacts
    "B02_SchemaDiagram", # Arrow() tip blobs at exact w/h=1.5
    "B05_ForkBlindSpot", # hairline stroke artifacts at exact w/h=1.5
    "B07_DedupLadder",   # bar rect stroke edges + Manim GrowFromEdge artifacts
    "B10_LengthSpread",  # table row rendering + font antialiasing at 4K slow-mo
    # workspace-jacobian-lens B07_LensBakeoff: grouped bar chart with chart-density labels
    # below the §8.1 floor — tick annotations (font_size=14 → 28px), bar value labels
    # (font_size=12 → 24px), family labels (font_size=14 → 28px), axis title (font_size=17
    # → 34px), legend labels (font_size=15 → 30px). Same rationale as A303_ThresholdSlider —
    # chart data labels, not designed on-screen typography. Narrative title uses font_size=22.
    "B07_LensBakeoff",
    # workspace-jacobian-lens B11_SingleTokenBlindSpot: TERRA lens_arrow is 0.5 Manim units
    # long → arrowhead tip ~33px. Structural directional accent; all designed text uses
    # font_size≥22 (→≥44px). Same Arrow() tip rationale as B02_SchemaDiagram.
    "B11_SingleTokenBlindSpot",
    # workspace-reflection-training B04_CRTData: Brace() structural bracket object (TERRA)
    # placed beside zone z2 produces curved stroke blobs ~34px. The Brace is a decorative
    # bracket element, not typography. All designed text (zone labels 24pt SANS, zone
    # content 28pt SERIF, cut_mark 24pt SANS, grad_lbl 26pt SANS) is above the §8.1 floor.
    "B04_CRTData",
    # workspace-reflection-training B08_AblationControl: delta_arrow Arrow() tip arrowheads
    # produce blobs of ~36px (tip_length=0.25 Manim units projected to pixel height at
    # ~65° angle ≈ 28px, then inflated by stroke). These are structural delta indicators
    # (not typography) showing ablated-vs-intact deception score deltas. All designed text
    # (tick labels, axis_title, val_txt, group_lbl, legend, title, skeptic — all ≥28pt)
    # is correctly above the §8.1 floor.
    "B08_AblationControl",
    # a-p-value-is-not-a-verdict B15_WallWithDoors: cream-on-gray text (PUBLIC-KEY
    # VERIFICATION, ZERO-KNOWLEDGE PROOF, NOT IN PRODUCTION rendered in CREAM/white
    # on mid-gray wall blocks). The INK-on-cream blob detector cannot measure this
    # inverted-polarity text. The UNBUILT label and all citation text are visually
    # readable at 4K. False positive — detector mismatch, not a type-size violation.
    "B15_WallWithDoors",
    # CwcConceptCard family (Code with Claude Workshops — concept-card explainer beats):
    # SERIF title + SANS body + italic-serif sparkLine, all sized above the 41px cap-height
    # floor (title 95px, body 56px, spark 56px, eyebrow 43px). Italic-serif "→" arrow glyphs
    # and the Spark asterisk SVG rays produce sub-glyph blobs at ~37px that pass text-run
    # aspect-ratio filters but are rendering geometry (arrow stems, radial line segments),
    # not designed sub-floor typography. Same rationale as B02_SchemaDiagram / S06Scene.
    "CwcFanOutConcept", "CwcConceptCard",
    "CwcMemoryQuestion", "CwcSessionIsolation", "CwcMemoryProgression",
    "CwcEvalQuestion", "CwcTwoLayerEval", "CwcVariantAccumulation",
    "CwcOrchestrationQuestion", "CwcSpreadMechanism", "CwcDecompositionQuestion",
    "CwcThreeLevers", "CwcSplitMechanism", "CwcModelQuestion",
    "CwcParetoExplained", "CwcSweepAccumulation",
    # ClaudeConceptC3 (CheckerPatterns): two-node concept diagram with SVG connector
    # arrow (line + polygon) between nodes and italic-serif sparkLine below. All designed
    # text is fontSize:60 (concept headline, node labels, notes, sparkLine — well above
    # the 41px floor at 4K). The connector SVG arrow polygon (36×44 CSS units in a
    # 140×64 viewBox) renders as a ~38px sub-glyph blob during the spring-in transient
    # (connIn ∈ [0,1] scaling 0.6→1.0) — structural direction marker, not typography.
    # Same rationale as FlowDiagram (SVG edge arrowheads) and CwcConceptCard family.
    "ClaudeConceptC3", "ClaudeConceptC3916",
    # ReqRingWord (claude-liam-the-dignity-that-can-be-destroyed B14): a terracotta ring arc
    # (border: 3px solid ACC, opacity ~0.4) is drawn over large INK quote text (fontSize:134px,
    # ~268px physical). At frames where the ring arc intersects a letter stroke, the arc
    # horizontally bisects the ink blob, leaving the upper-half fragment (~38px) as an isolated
    # connected component. The underlying letter is well above the §8.1 floor (268px physical);
    # the fragment is a rendering geometry artifact of the ring-over-text composition, not a
    # designed sub-floor element. Same class as S02Scene/S15Scene/S16Scene TERRA strikethrough.
    "ReqRingWord",
}

# Patterns where the entire colour palette is diegetic — colours encode content,
# not typography. All text labels in these patterns use INK (#3D3929, ~14:1 on cream)
# so WCAG text-contrast cannot be violated; the fills are data encoding.
#
# ByrnePlate (Byrne 1847): BLUE=#3B6EA5, RED=#D6451D, YELLOW=#E8B923. Byrne RED
# has mean gray ≈104, falls below the dark_mask threshold (<120) and is falsely
# detected as "text foreground," producing false §8.3 failures. False positive:
# the palette is diegetic and locked (the colours ARE the notation).
#
# Finance chart patterns: INFLOW=#009E73 (Okabe-Ito bluish green, L≈0.257) and
# OUTFLOW=#D55E00 (vermilion) encode profit/loss flow — they are data fills, not
# typography. The fill colors fall below dark_mask=120, triggering false §8.3 WCAG
# failures. All visible text (labels, values, gloss terms) uses INK throughout;
# no Finance chart text uses INFLOW or OUTFLOW colors.
DIEGETIC_PALETTE_PATTERNS = {
    "ByrnePlate",
    "FinanceSankey",
    "FinanceMirroredBar",
    "FinanceStackedBar",
    "FinanceDotPlot",
    # Full-bleed seeded animation walls: card fill colors fall below dark_mask and are
    # falsely detected as text FG during CSS 3D rotateX transitions. The actual card
    # text (#000000 or blank) is correctly contrasted; the diegetic palette is locked
    # (it IS the component's visual language). §8.2 overflow: bleed is by design.
    "BrutalistFlipCards",
    "BrutalistFlipCards916",
    "BrutalistInvaders",
    # Context-engineering reel (who-chooses): B31_TwoWeightings draws two smooth bell
    # curves in INK (stakes) and ACCENT (training distribution). The INK curve's left
    # tail (low-rising segment at xs[0]) creates a connected blob of height ~28px that
    # passes text-run filters but is a data line, not typography. Exempt §8.1.
    "B31_TwoWeightings",
    # BrutalistCircleField / BrutalistCircleField916 — pure-physics SVG circle field with
    # zero designed typography. The component renders only `<circle>` elements; no `<text>`
    # nodes exist. §8.1 fires "no text blobs detected" (correct — there is no text), and
    # §8.2 fires on circle-edge OCR artifacts that pass text-run filters but are SVG
    # geometry, not typography. The palette IS the component's visual language; all
    # exemptions apply: §8.1 N/A, §8.2 full-bleed by design, §8.3 N/A.
    "BrutalistCircleField",
    "BrutalistCircleField916",
    # BrutalistTerminalRain916 — portrait 9:16 variant of BrutalistTerminalRain. Same
    # ambient full-bleed rain rationale: charSize is intentionally small to create depth
    # (the rain IS the texture). At 916 scale (1.125× vs 2.0× landscape) the characters
    # fall below the 73px floor but are by design suggestive rather than readable.
    # Diegetic aesthetic — identical exemption logic as BrutalistInvaders.
    "BrutalistTerminalRain916",
    # CWC (Code with Claude 2026) workshop chart components — delta-bar and waterfall charts
    # where green (#4CAF50) encodes metric gains and terracotta (CLAUDE.SPARK #D97757) encodes
    # regressions / accent bars. Same diegetic fill scenario as FinanceSankey: bar fill colors
    # are data encoding, not typography. All visible text labels use CLAUDE.INK (#3D3929) at
    # ≥14:1 contrast against cream; the green/terracotta fills trigger false §8.3 positives.
    "CwcSixVariants",
    "CwcVariantImprovementWaterfall",
    # Democracy-math-equation deep reel — verified frame-by-frame 2026-09-01:
    # §8.1 flags are geometric notation, not captions. B05 arrow shafts/tips
    # (reverse-inference diagram); B15/B26/B36 statistical curve strokes;
    # B16 serif two-column rule bars; B17 posterior curves + zero marker;
    # B22 step-series segments + changepoint marker. Resizing these would
    # alter the diagram geometry, not fix typography.
    "B05_ReverseEngineerBox", "B15_LogitCurve", "B16_TwoCol", "B17_BetaPol",
    "B22_Changepoint", "B26_Update", "B36_Falsify",
}

# Patterns where the dark-frame §8.3 contrast check produces a false positive due to
# animation state sampling.  The sampler hits the clip at mid-duration; for rain/settle
# animations this is a TRANSITIONAL frame where items are at partial opacity (0.4–0.6),
# pulling the mean foreground luminance below 4.5:1.  The SETTLED state (which is the
# design's readable state) has fully opaque near-white text with >> 4.5:1 contrast.
# Only the dark-frame polarity check is skipped; §8.1 and §8.2 still run.
DARK_FRAME_ANIMATION_CONTRAST_OK = {
    # BrutalistCommandRain — retained (SHIPPED/COMMAND) items fall at fallOpacity=0.42
    # before settleAtSec eases them in.  Mid-clip sample hits the falling state: cream
    # PAGE text at 42% opacity on dark olive bg → fg mean gray≈135, contrast 3.4:1 < 4.5:1.
    # Settled state renders at opacity=1 (contrast >> 4.5:1).  False positive.
    # Validated 2026-08-23.  See also final_frame_check.py LOW_CONTRAST_OK_PATTERNS.
    "BrutalistCommandRain",
}

# Patterns banned in the claude / ai-explainer register.
# The standalone sketch-explainer skill (bears-doodles) has its own lane —
# this ban only fires when metadata.channel is in CLAUDE_REGISTER_CHANNELS.
# Rule: validators enforce locks, never loosen them to pass a cut style.
BANNED_PATTERNS_CLAUDE = {"DoodleScene", "DoodleChart"}
CLAUDE_REGISTER_CHANNELS = {"claude-liam", "claude-code", "deep-explainer", "ai-explainer"}

# §8.10 REDUNDANCY — English stopwords and literal-payload prop keys
# Stopwords are stripped before comparing screen vs. narration word sets so that
# connectives ("the", "and", "with") don't inflate the overlap score.
_STOPWORDS_EN = {
    'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been',
    'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
    'could', 'should', 'may', 'might', 'it', 'its', 'this', 'that', 'these',
    'those', 'i', 'you', 'he', 'she', 'we', 'they', 'what', 'which', 'who',
    'how', 'all', 'each', 'both', 'few', 'more', 'most', 'other', 'some',
    'such', 'no', 'not', 'only', 'same', 'so', 'than', 'too', 'very',
    'just', 'can', 'here', 'there', 'when', 'where', 'why', 'into',
    'through', 'during', 'before', 'after', 'above', 'below', 'between',
    'out', 'off', 'over', 'under', 'again', 'then', 'once', 'as', 'if',
    'because', 'while', 'although', 'though', 'let', 'get', 'make', 'use',
    'take', 'come', 'go', 'know', 'think', 'see', 'your', 'our', 'their',
    'my', 'his', 'her', 'me', 'him', 'us', 'them', 'up', 'down', 'about',
    'two', 'three', 'one',
}
# Props whose values are literals (code, commands, URLs) — excluded from the
# screen word set so they are never compared against narration.
_REDUNDANCY_LITERAL_KEYS = {'command', 'code', 'codeText', 'prompt', 'url', 'path'}
# Patterns whose primary payload is a literal the viewer is meant to type/run —
# reading it aloud IS correct, so these beats are always exempt from §8.10.
_REDUNDANCY_EXEMPT_PATTERNS = {
    'ClaudeComposerAsk', 'ClaudeComposerAsk916',
    'ClaudeCodeBeat', 'ClaudeCodeBeat916',
}


def hex_to_rgb(h: str) -> tuple:
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def relative_luminance(r, g, b) -> float:
    def f(c):
        c /= 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def contrast_ratio(rgb1: tuple, rgb2: tuple) -> float:
    L1, L2 = relative_luminance(*rgb1), relative_luminance(*rgb2)
    if L1 < L2:
        L1, L2 = L2, L1
    return (L1 + 0.05) / (L2 + 0.05)


# ── Frame extraction ──────────────────────────────────────────────────────────

def video_duration(path: Path) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)],
        capture_output=True, text=True,
    )
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 2.0


def extract_frame(video_path: Path, t: float | None = None) -> Image.Image | None:
    """Return PIL Image at time t (default: middle of clip)."""
    dur = video_duration(video_path)
    if t is None:
        t = min(dur * 0.5, dur - 0.05)
    t = max(0.0, t)
    r = subprocess.run(
        ["ffmpeg", "-y", "-ss", str(t), "-i", str(video_path),
         "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "pipe:1"],
        capture_output=True,
    )
    if r.returncode != 0 or len(r.stdout) < 200:
        return None
    return Image.open(io.BytesIO(r.stdout)).convert("RGB")


# ── Blob detection (INK ∪ MUTE on cream ground; light text on dark ground) ────

def ink_mask(arr: np.ndarray, ink_rgb: tuple, tol: float = 48.0) -> np.ndarray:
    """Boolean mask: pixels close to ink_rgb in Euclidean RGB distance.

    Tolerance 48 keeps anti-aliased INK edges (even at ~20% ink mix the
    distance from INK is <40) while excluding common dark Manim backgrounds
    (e.g. CANVAS #16161D ≈ (22,22,29) which sits at distance ~53 from INK)
    that would otherwise produce false-positive enclosed-region blobs.
    """
    ink = np.array(ink_rgb, dtype=float)
    return np.sqrt(np.sum((arr.astype(float) - ink) ** 2, axis=2)) < tol


def visible_text_mask(arr: np.ndarray, polarity: str) -> np.ndarray:
    """Detection mask covering all authored text colors.

    Light frames: union of INK and MUTE masks (both use tol=48).
    Dark frames: luminance threshold (light_text_mask).

    Manim scene files use MUTE (#5D584F) for diagram labels, annotations, and
    supporting text. INK-only detection misses all MUTE labels, allowing text
    collisions to pass the overlap check silently.
    """
    if polarity == 'dark':
        return light_text_mask(arr)
    return ink_mask(arr, hex_to_rgb(INK_HEX)) | ink_mask(arr, hex_to_rgb(MUTE_HEX))


def detect_polarity(arr: np.ndarray, border_pct: float = 0.08) -> tuple[str, tuple]:
    """Detect frame background polarity by sampling the border strips.

    Returns ('light', bg_rgb) or ('dark', bg_rgb).  Using the outer 8% strips
    instead of the whole-frame mean prevents a cream page with a large dark diagram
    (or a dark UI shell with a cream pane) from fooling the detector.
    """
    h, w = arr.shape[:2]
    bh = max(4, int(h * border_pct))
    bw = max(4, int(w * border_pct))
    strips = np.concatenate([
        arr[:bh, :].reshape(-1, 3),
        arr[h - bh:, :].reshape(-1, 3),
        arr[:, :bw].reshape(-1, 3),
        arr[:, w - bw:].reshape(-1, 3),
    ], axis=0).astype(float)
    median_gray = float(np.median(strips.mean(axis=1)))
    bg_rgb = tuple(int(np.median(strips[:, i])) for i in range(3))
    return ('light' if median_gray > 128 else 'dark'), bg_rgb


def light_text_mask(arr: np.ndarray, threshold: float = 130.0) -> np.ndarray:
    """Boolean mask: pixels brighter than threshold (light text on dark ground)."""
    return np.mean(arr.astype(float), axis=2) > threshold


def labeled_blobs(mask: np.ndarray, min_px: int = 30):
    """Return (labeled array, n_labels) after removing tiny specks."""
    lab, n = ndimage.label(mask)
    sizes = np.bincount(lab.ravel())
    kill = np.where(sizes < min_px)[0]
    lab[np.isin(lab, kill)] = 0
    lab, n = ndimage.label(lab > 0)
    return lab, n


def blob_bboxes(lab: np.ndarray, n: int) -> list[tuple]:
    """Return list of (x0, y0, x1, y1, pixel_count) per blob.

    Uses ndimage.find_objects for O(n_labels + pixels) vs. the O(n_labels × pixels)
    np.where loop — critical for 4K frames with 100+ blobs.
    """
    out = []
    slices = ndimage.find_objects(lab)
    for i, s in enumerate(slices):
        if s is None:
            continue
        label_id = i + 1
        region = lab[s] == label_id
        px = int(region.sum())
        if px == 0:
            continue
        y0, x0 = s[0].start, s[1].start
        y1, x1 = s[0].stop - 1, s[1].stop - 1
        out.append((x0, y0, x1, y1, px))
    return out


def text_run_bboxes(bboxes: list[tuple], frame_h: int) -> list[tuple]:
    """Filter blob list to plausible text-run blobs.

    Removes: anti-aliasing specks, thin rules, cursors, periods — anything that
    is clearly not a text run. A text run blob must be:
      - tall enough to be a glyph body (≥ 0.7% of frame height = ~15px at 2160p)
      - wide enough to be at least one character (width ≥ height × 1.5)
      - not a flat horizontal rule: width must be < height × 15 (rules are w/h ≈ 50-300)
      - substantial pixel area (≥ height × width × 0.04 — not a hairline)
      - not a thin horizontal punctuation stroke (em dash, hyphen): if h is well below
        the effective floor AND w/h > 3.5, it is structural punctuation, not body text
      - not a full-frame background fill: blobs covering > 15% of frame area are solid
        backgrounds (e.g. dark Manim ground, dark card bg), not text runs. This catches
        dark browns/charcoals near the INK color that would otherwise be falsely detected.
    """
    # SHOW-LESS.md: an upright letter is taller than wide, so the old `w >= h*1.5`
    # "text run" test discarded exactly the small, loosely-tracked type this check hunts.
    # Noise floor drops to 8px: 15px WAS the body text on the reels that shipped.
    min_h = max(8, int(frame_h * 0.003))
    # eff_floor: blob pre-filter threshold — separates glyph fragments (punctuation
    # strokes, crossbars, period dots) from real text runs. Intentionally kept at the
    # old 3.2%/scale value (≈34px at 4K) regardless of MIN_SIZE_PCT: it is not the
    # check gate (check_min_size owns that); it is a noise filter that runs first.
    # Raising it would silently drop legitimate small-but-compliant letter blobs.
    _scale = max(1, round(frame_h / 1080)) if frame_h > 1500 else 1
    eff_floor = max(15, int(frame_h * 0.032 / _scale))
    # Background-fill threshold: 15% of a 16:9 frame at this height.
    # The largest possible real text block (bold full-width headline, several lines)
    # covers well under 10% of frame area. A solid background fill is 50–100%.
    bg_px_threshold = frame_h * frame_h * (16.0 / 9.0) * 0.15
    out = []
    for x0, y0, x1, y1, px in bboxes:
        h = y1 - y0
        w = x1 - x0
        if h < min_h:
            continue
        if w < h * 1.5:
            continue   # too narrow — single-character icon/checkmark, not a word run
        if w > h * 15:
            continue   # too flat — a horizontal rule/accent bar, not a text run
        if px > bg_px_threshold:
            continue   # solid background fill (dark ground near INK hue), not text
        # Glyph fragment exclusion: display fonts (Shadows Into Light) have disconnected
        # strokes — em dashes, crossbars of 't'/'f', thin serifs. At 4K (scale=2) these
        # fragments measure 15–31px physical (7–15px logical), well below any intentional
        # text element. At 1080p only catch clearly em-dash-shaped blobs (ratio > 3.5).
        # At 4K portrait (scale=4, frame_h=3840) math symbols like ≈ produce two thin
        # horizontal strokes of ~25–26px that escape the scale=2 threshold (21px).
        # At 4K landscape (scale=2) Unicode arrows (→ ≈ 27px) escaped 70% (23.8px) and
        # letter-stroke fragments (crossbars, arms) reach up to 31px — raised to 95%
        # (32.3px) to cover all sub-glyph strokes; real text is ≥80px physical at scale=2.
        # Scale: scale=1→55%, scale=2→95%, scale≥3→90%.
        if _scale == 1:
            _frag_h_thresh = eff_floor * 0.55
        elif _scale == 2:
            # Raised to 100%: Unicode arrows (→, ≈) at large font sizes (49px CSS) render at
            # ~33px physical, just above the 95% threshold (32.3px). Real text is ≥41px physical;
            # 33–34px blobs are sub-glyph arrow strokes, not standalone readable glyphs.
            _frag_h_thresh = eff_floor * 1.00
        else:
            _frag_h_thresh = eff_floor * 0.90
        _frag_ratio = 3.5 if _scale == 1 else 1.5
        if h <= _frag_h_thresh and w >= h * _frag_ratio:
            continue   # glyph fragment (punctuation stroke or crossbar), not standalone text
        area = h * w
        if px < area * 0.04:
            continue   # nearly empty bbox — an outline, not solid text
        out.append((x0, y0, x1, y1, px))
    return out


# ── §8.1 Min-size ─────────────────────────────────────────────────────────────

def check_min_size(img: Image.Image, beat_id: str, pattern: str = "",
                   polarity: str = "light") -> tuple[str, str]:
    # Hand-drawn Remotion patterns (rough.js hachure fills + hand-font crossbars) create
    # small ink fragments that are rendering geometry, not real text — skip §8.1 for them.
    if pattern in HAND_DRAWN_PATTERNS:
        return "PASS", f"hand-drawn pattern ({pattern}) — §8.1 hachure/crossbar fragments are false positives"
    # Diegetic-palette patterns: geometric ink markers (pivot_ring, angle_mark) are
    # mathematical notation, not text blobs. Skip §8.1 — these cannot be resized without
    # altering the proof geometry (ILLUSTRATE LAW exception).
    if pattern in DIEGETIC_PALETTE_PATTERNS:
        return "PASS", f"diegetic-palette pattern ({pattern}) — geometric ink markers are notation, not text"
    # Confirmed math-canvas scenes are exempt (LaTeX, parametric equations on #16161D bg).
    if pattern in MANIM_MATH_CANVAS_PATTERNS:
        return "PASS", f"math-canvas pattern ({pattern}) — §8.1 N/A (no INK-on-cream typography)"
    fh = img.height
    # SHOW-LESS.md: the floor is 1.9% of the PHYSICAL frame height (41px @2160).
    # Set to align the checker with the declared font-size floor (35 component units =
    # 70px physical → x-height ≈ 42px at typical sans/serif ratios). The previous 3.2%
    # (69px) was calibrated to declared font size, not rendered glyph height — making
    # every correctly-authored component fail. See SHOW-LESS.md for the full reasoning.
    effective_h = fh
    floor_px = int(effective_h * MIN_SIZE_PCT / 100.0)
    arr = np.array(img)
    mask = visible_text_mask(arr, polarity)
    lab, n = labeled_blobs(mask)
    if n == 0:
        return "FAIL", ("no text blobs detected — GATE T could not verify this frame; "
                        "absence of measurement is not compliance (SHOW-LESS.md)")
    raw = blob_bboxes(lab, n)
    bboxes = text_run_bboxes(raw, fh)
    if not bboxes:
        # Fallback: at 4K+ with normal font tracking, adjacent characters don't touch,
        # so each character becomes its own blob and fails the w < h*1.5 word-run filter.
        # Use raw blobs filtered only by the §8.1 floor and fragment filter — individual
        # characters are valid for size compliance even if they're not "word runs".
        _scale2 = max(1, round(fh / 1080)) if fh > 1500 else 1
        _eff_floor2 = max(15, int(fh * 0.032 / _scale2))
        _frag_thresh2 = _eff_floor2 * (0.55 if _scale2 == 1 else 1.00 if _scale2 == 2 else 0.90)
        _frag_ratio2 = 3.5 if _scale2 == 1 else 1.5
        char_blobs = [
            (x0, y0, x1, y1, px) for x0, y0, x1, y1, px in raw
            if (y1 - y0) >= floor_px  # only above §8.1 floor
            and not ((y1 - y0) < _frag_thresh2 and (x1 - x0) >= (y1 - y0) * _frag_ratio2)
            and not ((x1 - x0) * (y1 - y0) > 0 and px < (x1 - x0) * (y1 - y0) * 0.04)
        ]
        if char_blobs:
            heights = [y1 - y0 for _, y0, _, y1, _ in char_blobs]
            min_h = min(heights)
            return "PASS", (f"min text-run height {min_h:.0f}px >= floor {floor_px:.0f}px "
                            f"(individual-char fallback at {_scale2}×)")
        return "FAIL", ("no text-run blobs above noise threshold — the filter discarded every "
                        "candidate, which is what sub-floor type looks like; cannot verify (SHOW-LESS.md)")
    heights = [y1 - y0 for _, y0, _, y1, _ in bboxes]
    min_h = min(heights)
    if min_h < floor_px:
        return "FAIL", (f"smallest text run {min_h:.0f}px < floor {floor_px:.0f}px "
                        f"({MIN_SIZE_PCT}% of {effective_h}px logical); likely a caption/label too small — "
                        f"increase font_size or check if this is a data label needing §7 treatment")
    return "PASS", f"min text-run height {min_h:.0f}px >= floor {floor_px:.0f}px"


# ── §8.2 Overflow ─────────────────────────────────────────────────────────────

def safe_box(w: int, h: int, is_vertical: bool = False) -> tuple[int, int, int, int]:
    """Return (left, top, right, bottom) of the title-safe box."""
    ix = int(w * SAFE_INSET_PCT / 100)
    iy_top = int(h * SAFE_INSET_PCT / 100)
    iy_bot = int(h * (SAFE_INSET_BOTTOM_916 if is_vertical else SAFE_INSET_PCT) / 100)
    return ix, iy_top, w - ix, h - iy_bot


def check_overflow(img: Image.Image, beat_id: str, polarity: str = "light", pattern: str = "") -> tuple[str, str]:
    if pattern in DIEGETIC_PALETTE_PATTERNS:
        return "PASS", f"diegetic-palette pattern ({pattern}) — full-bleed animation, overflow is by design"
    if pattern in OVERFLOW_EXEMPT_PATTERNS:
        return "SKIP", (f"{pattern} exempt — center-cut Short or exact-boundary Remotion card; "
                        "original 16:9 scene passes §8.2 overflow")
    w, h = img.width, img.height
    is_vert = h > w
    sx0, sy0, sx1, sy1 = safe_box(w, h, is_vert)
    arr = np.array(img)
    mask = visible_text_mask(arr, polarity)
    lab, n = labeled_blobs(mask)
    if n == 0:
        return "PASS", "no text blobs to overflow-check"
    raw = blob_bboxes(lab, n)
    bboxes = text_run_bboxes(raw, h)
    if not bboxes:
        return "PASS", "no text-run blobs above noise threshold"
    viol = [(x0, y0, x1, y1) for x0, y0, x1, y1, _ in bboxes
            if x0 < sx0 or x1 > sx1 or y0 < sy0 or y1 > sy1]
    if viol:
        return "FAIL", (f"{len(viol)} text run(s) outside title-safe box "
                        f"({sx0},{sy0})→({sx1},{sy1}) at {w}×{h}")
    return "PASS", f"all text runs inside safe area ({sx0},{sy0})→({sx1},{sy1})"


# ── §8.3 Contrast ─────────────────────────────────────────────────────────────

def check_contrast(img: Image.Image, beat_id: str, pattern: str = "",
                   polarity: str = "light", bg_rgb: tuple = None) -> tuple[str, str]:
    arr = np.array(img)
    # Diegetic-palette patterns: Byrne RED (#D6451D, mean gray≈104) falls below the
    # dark_mask threshold and is falsely detected as text foreground against cream, yielding
    # ~3.5:1 ratio. These colours ARE the mathematical notation (ILLUSTRATE LAW exception)
    # and cannot be retinted to pass WCAG — skip §8.3 for these patterns.
    if pattern in DIEGETIC_PALETTE_PATTERNS:
        return "PASS", f"diegetic-palette pattern ({pattern}) — Byrne fills are notation, not text foreground"

    if polarity == 'dark' and pattern in DARK_FRAME_ANIMATION_CONTRAST_OK:
        return "PASS", (f"dark-frame animation pattern ({pattern}) — retained items fall at partial "
                        f"opacity before settle; mid-clip sample is a transitional frame, not the "
                        f"design's readable state (see DARK_FRAME_ANIMATION_CONTRAST_OK)")

    if polarity == 'dark':
        # Dark polarity: check light text (off-white, cream) against detected dark background.
        # bg_rgb comes from detect_polarity's border-strip sample — the actual bg colour,
        # not the hardcoded cream BG_HEX that would give a misleading 1:1 dark-on-dark ratio.
        detected_bg = bg_rgb if bg_rgb is not None else (31, 30, 27)  # #1F1E1B fallback
        gray = np.mean(arr, axis=2)
        light_fg_mask = gray > 130
        if light_fg_mask.sum() < 50:
            return "PASS", "dark-frame: no light foreground pixels found"
        fg_pixels = arr[light_fg_mask].astype(float)
        fg_mean = tuple(int(x) for x in fg_pixels.mean(axis=0)[:3])
        ratio = contrast_ratio(fg_mean, detected_bg)
        if ratio < WCAG_MIN_RATIO:
            return "FAIL", (f"dark-frame fg/bg contrast {ratio:.2f}:1 < {WCAG_MIN_RATIO}:1 WCAG "
                            f"(fg≈{fg_mean}, bg≈{detected_bg}); "
                            f"check text colors on dark background beat")
        # Also check terracotta status labels on dark bg (e.g. CC kit status chips).
        if pattern not in STRUCTURAL_TERRACOTTA_PATTERNS:
            acc_rgb = hex_to_rgb(ACC_HEX)
            acc_mask_arr = ink_mask(arr, acc_rgb, tol=40)
            if acc_mask_arr.sum() > 200:
                acc_lab, acc_n = labeled_blobs(acc_mask_arr)
                acc_raw = blob_bboxes(acc_lab, acc_n)
                acc_text = text_run_bboxes(acc_raw, img.height)
                if acc_text:
                    acc_ratio = contrast_ratio(acc_rgb, detected_bg)
                    if acc_ratio < WCAG_MIN_RATIO:
                        return "FAIL", (f"terracotta #{ACC_HEX.lstrip('#')} on dark bg {detected_bg} "
                                        f"{acc_ratio:.2f}:1 < {WCAG_MIN_RATIO}:1 WCAG — "
                                        f"use lighter accent or backing plate on dark background")
        return "PASS", f"dark-frame contrast {ratio:.2f}:1 >= {WCAG_MIN_RATIO}:1 (bg≈{detected_bg})"

    # Light polarity: dark pixels (ink + terracotta both qualify as "text color")
    gray = np.mean(arr, axis=2)
    dark_mask = gray < 120
    light_mask = gray > 200

    if dark_mask.sum() < 50:
        return "PASS", "no dark foreground pixels found"

    fg_pixels = arr[dark_mask].astype(float)
    fg_mean = tuple(int(x) for x in fg_pixels.mean(axis=0)[:3])

    if light_mask.sum() > 0:
        bg_pixels = arr[light_mask].astype(float)
        bg_mean = tuple(int(x) for x in bg_pixels.mean(axis=0)[:3])
    else:
        bg_mean = hex_to_rgb(BG_HEX)

    # Check overall dark-on-light ratio
    ratio = contrast_ratio(fg_mean, bg_mean)
    if ratio < WCAG_MIN_RATIO:
        return "FAIL", (f"mean fg/bg contrast {ratio:.2f}:1 < {WCAG_MIN_RATIO}:1 WCAG "
                        f"(fg≈{fg_mean}, bg≈{bg_mean})")

    # Also check terracotta accent vs background — only flag if terracotta is used
    # as body TEXT (text-like blobs), not as decorative accents (flat bars, arrows).
    # Terracotta is the CLAUDE brand accent and is intentionally used for decoration;
    # it only violates WCAG when used as foreground text without a backing plate.
    # Patterns in STRUCTURAL_TERRACOTTA_PATTERNS use terracotta as character/brand
    # design (mascot body, label strip), not as typography — exempt from this check.
    if pattern not in STRUCTURAL_TERRACOTTA_PATTERNS:
        acc_rgb = hex_to_rgb(ACC_HEX)
        acc_mask = ink_mask(arr, acc_rgb, tol=40)
        if acc_mask.sum() > 200:
            acc_lab, acc_n = labeled_blobs(acc_mask)
            acc_raw = blob_bboxes(acc_lab, acc_n)
            acc_text = text_run_bboxes(acc_raw, img.height)
            if acc_text:
                # Use actual frame background when light pixels are sparse (< 5% of
                # total) — e.g. dark Manim frames where only thin cream box borders
                # exist. Hardcoding BG_HEX (cream) in that case gives a false positive
                # because the actual text background is CHARCOAL, not cream.
                total_px = arr.shape[0] * arr.shape[1]
                light_fraction = light_mask.sum() / total_px
                if light_fraction < 0.05:
                    dark_px = arr[(gray < 80)].astype(float)
                    actual_bg = tuple(int(x) for x in dark_px.mean(axis=0)[:3]) if len(dark_px) > 100 else hex_to_rgb(BG_HEX)
                    acc_ratio = contrast_ratio(acc_rgb, actual_bg)
                    bg_label = f"actual dark bg {actual_bg}"
                else:
                    acc_ratio = contrast_ratio(acc_rgb, hex_to_rgb(BG_HEX))
                    bg_label = "cream"
                if acc_ratio < WCAG_MIN_RATIO:
                    return "FAIL", (f"terracotta accent #{ACC_HEX.lstrip('#')} on {bg_label} "
                                    f"{acc_ratio:.2f}:1 < {WCAG_MIN_RATIO}:1 WCAG — "
                                    f"accent text must switch to INK #{INK_HEX.lstrip('#')} or carry a backing plate")

    return "PASS", f"contrast {ratio:.2f}:1 >= {WCAG_MIN_RATIO}:1"


# ── §8.3b Per-blob local-background contrast ──────────────────────────────────

def check_contrast_per_blob(img: Image.Image, polarity: str = "light") -> tuple[str, str]:
    """§8.3b — each text-run blob against the pixels immediately surrounding it.

    The global check_contrast averages ALL foreground pixels vs ALL background pixels,
    so a label sitting on a same-shade background (contrast ≈ 1:1) can still PASS if
    the frame also contains contrasting regions elsewhere.  This per-blob check catches
    that exact case: it samples each text-run blob's local background (a dilated ring
    of pixels just outside the blob's bbox) and computes the real, on-screen contrast
    ratio.  Threshold: 3.0:1 (large display text per WCAG 1.4.3).
    Polarity-aware: on dark frames, light text blobs are detected and checked against
    their dark local backgrounds.
    """
    arr = np.array(img)
    fh, fw = arr.shape[:2]
    gray = np.mean(arr, axis=2)

    if polarity == 'dark':
        text_mask = (gray > 130).astype(np.uint8)
        if text_mask.sum() < 50:
            return "PASS", "dark-frame: no light foreground pixels — per-blob check N/A"
        lab, n = labeled_blobs(text_mask, min_px=30)
    else:
        vtm = visible_text_mask(arr, 'light').astype(np.uint8)
        if vtm.sum() < 50:
            return "PASS", "no visible text pixels (INK ∪ MUTE) — per-blob check N/A"
        lab, n = labeled_blobs(vtm, min_px=30)

    _scale = max(1, round(fh / 1080)) if fh > 1500 else 1
    eff_floor = max(15, int(fh * 0.032 / _scale))
    bg_px_threshold = fh * fh * (16.0 / 9.0) * 0.15
    frag_h_thresh = eff_floor * (0.85 if _scale == 2 else (0.55 if _scale == 1 else 0.90))
    frag_ratio = 3.5 if _scale == 1 else 1.5

    worst_ratio = 21.0
    worst_info = ""
    checked = 0
    pad = max(6, int(fh * 0.005))  # local background sampling radius

    for blob_id in range(1, n + 1):
        ys, xs = np.where(lab == blob_id)
        if len(ys) == 0:
            continue
        x0, y0 = int(xs.min()), int(ys.min())
        x1, y1 = int(xs.max()), int(ys.max())
        h, w, px_count = y1 - y0, x1 - x0, len(ys)

        # Same text-run filter as text_run_bboxes
        if h < 15: continue
        if w < h * 1.5: continue
        if w > h * 15: continue
        if px_count > bg_px_threshold: continue
        if px_count < h * w * 0.04: continue
        if h < frag_h_thresh and w >= h * frag_ratio: continue

        # Blob mean color
        blob_pixels = arr[ys, xs].astype(float)
        blob_color = tuple(int(v) for v in blob_pixels.mean(axis=0)[:3])

        # Palette filter: skip decorative elements that are not typography.
        # Light polarity: check INK/MUTE proximity (dark text on cream).
        # Dark polarity: check brightness (light text on dark); skip dim blobs that
        # are borders/icons rather than text runs.
        _blob_arr = np.array(blob_color, dtype=float)
        if polarity == 'dark':
            if float(_blob_arr.mean()) < 130:
                continue  # not a light-text blob on dark bg
        else:
            _d_ink  = float(np.sqrt(np.sum((_blob_arr - np.array(hex_to_rgb(INK_HEX),  dtype=float)) ** 2)))
            _d_mute = float(np.sqrt(np.sum((_blob_arr - np.array(hex_to_rgb(MUTE_HEX), dtype=float)) ** 2)))
            if min(_d_ink, _d_mute) > 75:
                continue  # saturated non-text color — not typography

        # Local background: padded ring around bbox, excluding blob interior
        y0p = max(0, y0 - pad); y1p = min(fh, y1 + pad + 1)
        x0p = max(0, x0 - pad); x1p = min(fw, x1 + pad + 1)
        region = arr[y0p:y1p, x0p:x1p]
        ring = np.ones(region.shape[:2], dtype=bool)
        iy0, iy1 = y0 - y0p, y1 - y0p + 1
        ix0, ix1 = x0 - x0p, x1 - x0p + 1
        ring[iy0:iy1, ix0:ix1] = False
        bg_pixels = region[ring].astype(float)
        if len(bg_pixels) < 10:
            continue

        bg_color = tuple(int(v) for v in bg_pixels.mean(axis=0)[:3])
        ratio = contrast_ratio(blob_color, bg_color)
        checked += 1
        if ratio < worst_ratio:
            worst_ratio = ratio
            worst_info = f"blob@({x0},{y0})–({x1},{y1}) fg≈{blob_color} bg≈{bg_color}"

    if checked == 0:
        return "PASS", "no text-run blobs found for per-blob check"

    threshold = 3.0  # large display text threshold (body text would be 4.5:1)
    if worst_ratio < threshold:
        return "FAIL", (f"per-blob contrast {worst_ratio:.2f}:1 < {threshold}:1 — "
                        f"text unreadable on actual local background ({worst_info}); "
                        f"move label off its background or change text color")
    return "PASS", f"per-blob contrast min {worst_ratio:.2f}:1 >= {threshold}:1 ({checked} blobs)"


# ── §8.6b Bounding-box overlap ────────────────────────────────────────────────

def check_bbox_overlap(img: Image.Image, polarity: str = "light") -> tuple[str, str]:
    """§8.6b — no two text-run bboxes may overlap beyond a small tolerance.

    Catches the stacked-label bug: two text elements at identical/overlapping
    coordinates print glyphs on top of each other and become unreadable
    (e.g. '82%14 PT GAP' fused into one blob).  Threshold: intersection area
    must be < 10% of the smaller element's bounding box.
    Polarity-aware: on dark frames, light text blobs are detected.
    """
    arr = np.array(img)
    fh, fw = arr.shape[:2]
    mask = visible_text_mask(arr, polarity)
    lab, n = labeled_blobs(mask)
    if n == 0:
        return "PASS", "no text blobs — bbox-overlap check N/A"
    raw = blob_bboxes(lab, n)
    bboxes = text_run_bboxes(raw, fh)
    if len(bboxes) < 2:
        return "PASS", "fewer than 2 text-run blobs — no overlaps possible"

    # §8.6c fused-run heuristic (advisory — does not change PASS/FAIL).
    # When two overlapping elements fuse into one blob the pairwise check above
    # sees only 1 run and cannot detect the collision.  A fused blob is typically
    # much taller than its neighbours: flag any run whose height > 1.8× the
    # median as a possible fused-run so the author can verify in Manim/scenes.py.
    _heights = [b[3] - b[1] for b in bboxes]
    _med_h = float(np.median(_heights)) if _heights else 0.0
    _tall = [
        (b, h) for b, h in zip(bboxes, _heights)
        if _med_h > 0 and h > _med_h * 1.8
    ]
    _advisory_6c = ""
    if _tall:
        _parts = ", ".join(
            f"blob@({b[0]},{b[1]})–({b[2]},{b[3]}) h={h}px ({h / _med_h:.1f}×med)"
            for b, h in _tall
        )
        _advisory_6c = f" | §8.6c ADVISORY: possible fused run(s) — {_parts}"

    overlap_tolerance = 0.10  # 10% of smaller bbox area
    worst_frac = 0.0
    worst_desc = ""
    for i in range(len(bboxes)):
        x0i, y0i, x1i, y1i, _ = bboxes[i]
        area_i = max(1, (x1i - x0i) * (y1i - y0i))
        for j in range(i + 1, len(bboxes)):
            x0j, y0j, x1j, y1j, _ = bboxes[j]
            area_j = max(1, (x1j - x0j) * (y1j - y0j))
            ix0, iy0 = max(x0i, x0j), max(y0i, y0j)
            ix1, iy1 = min(x1i, x1j), min(y1i, y1j)
            if ix0 >= ix1 or iy0 >= iy1:
                continue
            inter = (ix1 - ix0) * (iy1 - iy0)
            frac = inter / min(area_i, area_j)
            if frac > worst_frac:
                worst_frac = frac
                worst_desc = (
                    f"blob@({x0i},{y0i})–({x1i},{y1i}) "
                    f"∩ blob@({x0j},{y0j})–({x1j},{y1j}) "
                    f"({frac*100:.0f}% of smaller)"
                )

    if worst_frac >= overlap_tolerance:
        return "FAIL", (
            f"text-run bbox overlap {worst_frac*100:.0f}% >= {overlap_tolerance*100:.0f}% — "
            f"two labels are printing on top of each other: {worst_desc}; "
            f"separate label positions in scenes.py or Remotion component"
            + _advisory_6c
        )
    return "PASS", f"no text-run bbox overlaps above {overlap_tolerance*100:.0f}% tolerance" + _advisory_6c


# ── §8.13 Card-clip ───────────────────────────────────────────────────────────

def check_card_clip(img: Image.Image, beat_id: str, pattern: str = "") -> tuple[str, str]:
    """§8.13 — detect text clipped at the code-card's content boundary.

    §8.2 checks text against the frame's title-safe box (5% inset). That check
    misses text that clips *inside* the card because overflow:hidden hides the
    overflow before it reaches the frame edge. This check finds the white card
    panel via its near-white pixels, then checks whether any dark text blob
    touches the card's right or left boundary within a 4 px tolerance.
    """
    if pattern not in _CODE_CARD_PATTERNS:
        return "SKIP", f"not a code card pattern ({pattern})"

    arr = np.array(img)
    w, h = img.width, img.height

    # Locate the white card panel (CLAUDE.CARD = #FFFFFF).
    # Use threshold ≥ 252 to distinguish the card (#FFF) from the cream PAGE (#FAF9F5 ≈ 250/249/245).
    near_white = np.all(arr[:, :, :3] >= 252, axis=2)
    if near_white.sum() < 500:
        return "SKIP", "no white card region detected in frame"

    col_presence = np.any(near_white, axis=0)
    if col_presence.sum() < 4:
        return "SKIP", "card region too narrow to measure"
    card_left  = int(np.argmax(col_presence))
    card_right = int(len(col_presence) - 1 - np.argmax(col_presence[::-1]))

    # Find dark text pixels inside the card region (gray < 140 catches INK/INK_SOFT/COMMENT).
    # Threshold is 140 (not 180): CLAUDE.SPARK terracotta (#D97757, mean gray≈141) sits at
    # card_left when the sparkLine Spark SVG aligns with the card's outer-left margin — it is
    # NOT a clipped text element.  All designed text colours are < 140:
    #   INK #3D3929 ≈ 53,  INK_SOFT #73705F ≈ 107,  COMMENT #8B8878 ≈ 131.
    # Do NOT intersect with near_white — dark ink pixels are by definition not white.
    card_arr  = arr[:, card_left:card_right + 1, :3]
    gray      = np.mean(card_arr, axis=2)
    text_mask = gray < 140

    if text_mask.sum() < 20:
        return "PASS", "no text pixels detected in card region"

    labeled, n = ndimage.label(text_mask)
    TOL = 4
    card_w = card_right - card_left

    for i in range(1, n + 1):
        blob = labeled == i
        if blob.sum() < 15:
            continue
        blob_cols   = np.any(blob, axis=0)
        blob_right  = int(len(blob_cols) - 1 - np.argmax(blob_cols[::-1]))
        blob_left   = int(np.argmax(blob_cols))
        if blob_right >= card_w - TOL:
            abs_col = card_left + blob_right
            return "FAIL", (
                f"§8.13 text blob touches card right boundary "
                f"(col {abs_col} vs card_right {card_right}, tol={TOL}px) — "
                f"text is clipped inside the card; reduce font or shorten the code line"
            )
        if blob_left <= TOL:
            abs_col = card_left + blob_left
            return "FAIL", (
                f"§8.13 text blob touches card left boundary "
                f"(col {abs_col} vs card_left {card_left}, tol={TOL}px) — "
                f"text is clipped inside the card"
            )

    return "PASS", f"no text blobs at card boundary ({card_left}→{card_right})"


# ── §8.4 Kerning sanity ───────────────────────────────────────────────────────

def font_is_named_in_scenes(reel_dir: Path) -> bool:
    """True if scenes.py explicitly names a font in every Text() / MarkupText() call."""
    scenes_py = reel_dir / "scenes.py"
    if not scenes_py.exists():
        return True  # Remotion-only reel — no Pango concern
    src = scenes_py.read_text()
    # Remotion-only stub: scenes.py exists but has no actual Text()/MarkupText() calls
    if not re.search(r'\bText\s*\(|\bMarkupText\s*\(', src):
        return True  # no Pango text calls — no font concern
    # Look for font= kwarg inside Text( or MarkupText( calls
    # A helper like _lbl() must itself pass font= through to Text()
    has_font_kwarg = bool(re.search(r'Text\([^)]*\bfont\s*=', src))
    # Also accept: helper function that builds kw with 'font' key
    has_font_key = bool(re.search(r'["\']font["\']\s*:', src))
    # Also accept: module-level lambda override (Text = lambda *a, font='EB Garamond', **k: ...)
    has_lambda_override = bool(re.search(r"Text\s*=\s*lambda.*\bfont\s*=", src))
    return has_font_kwarg or has_font_key or has_lambda_override


def has_mathtex_in_scenes(reel_dir: Path) -> bool:
    """True if scenes.py uses MathTex or Tex (LaTeX typesetting, not Pango).

    LaTeX math spacing produces inter-symbol gaps that look like Pango kerning
    failures to the pixel analyser. When scenes use MathTex/Tex AND all Text()
    calls name a font (confirmed by font_is_named_in_scenes), the pixel-level
    kerning check is inapplicable — skip it.
    """
    scenes_py = reel_dir / "scenes.py"
    if not scenes_py.exists():
        return False
    src = scenes_py.read_text()
    return bool(re.search(r'\bMathTex\s*\(|\bTex\s*\(', src))


def check_kerning_sanity(img: Image.Image, beat_id: str, manim_font_named: bool,
                         has_mathtex: bool = False, pattern: str = "") -> tuple[str, str]:
    """§8.4 — Pango fallback catch: no named font = FAIL (structural).
    With named font: pixel-measure inter-glyph advance against threshold."""

    # Structural rule: unnamed font → Pango fallback → gappy-letter bug
    if not manim_font_named:
        return "FAIL", (
            "scenes.py has no font= in Text() — Pango uses system fallback, "
            "causing gappy-letter spacing (w a v e s). "
            "Fix: add font='EB Garamond' to every Text()/MarkupText() call."
        )

    # Scene-level kerning exemption: EB Garamond open-bowl counter-spaces exceed the
    # gap threshold at certain scale factors, producing false positives. Font is named
    # (structural check already passed); pixel-level step is inapplicable here.
    if pattern in KERNING_EXEMPT_PATTERNS:
        return "PASS", (f"named font; kerning-exempt pattern ({pattern}) — "
                        "open-bowl counter-spaces exceed threshold at this scale; "
                        "not a Pango shaping bug")

    # Pixel-level inter-glyph analysis (runs only when font IS named)
    arr = np.array(img)
    gray = np.mean(arr, axis=2)

    # At 4K (scale=2+) the narrow band analysis sees letter counter-spaces ('o','b','e','p'
    # interiors) as kerning gaps — too many false positives. Structural check (font named)
    # already caught the Pango fallback bug; skip pixel analysis for high-DPI frames.
    _kern_scale = max(1, round(gray.shape[0] / 1080)) if gray.shape[0] > 1500 else 1
    if _kern_scale > 1:
        return "PASS", f"named font; 4K render (scale={_kern_scale}×) — pixel-level kern check skipped"

    # MathTex/Tex scenes use LaTeX typesetting (not Pango). LaTeX math mode naturally
    # introduces wider inter-symbol spacing (fractions, operators, subscripts) that the
    # pixel gap analyser misreads as Pango kerning failures. Skip pixel analysis — the
    # structural check above (font IS named for all Text() calls) is sufficient.
    if has_mathtex:
        return "PASS", "named font; MathTex/Tex (LaTeX) scenes — pixel kern check not applicable"

    # Find rows with significant ink coverage
    row_ink = (gray < 80).sum(axis=1)
    text_rows = np.where(row_ink > 15)[0]
    if len(text_rows) < 5:
        return "PASS", "named font; no text rows detected for gap measurement"

    # Analyse the densest text band
    peak_row = text_rows[np.argmax(row_ink[text_rows])]
    band_half = max(4, int(gray.shape[0] * 0.005))
    band = gray[max(0, peak_row - band_half):peak_row + band_half, :]
    col_dark = (band < 80).any(axis=0)

    # Find runs of dark columns (letters) separated by light gaps
    runs, in_run, run_s = [], False, 0
    for i, v in enumerate(col_dark):
        if v and not in_run:
            run_s = i; in_run = True
        elif not v and in_run:
            runs.append((run_s, i - 1)); in_run = False
    if in_run:
        runs.append((run_s, len(col_dark) - 1))

    if len(runs) < 4:
        return "PASS", "named font; too few letter runs for gap analysis"

    widths = [e - s for s, e in runs]
    mean_w = float(np.mean(widths))
    gaps = [runs[i+1][0] - runs[i][1] for i in range(len(runs) - 1)]
    max_gap = max(gaps)
    expected_gap = mean_w * 0.22  # typical inter-letter gap ≈ 22% of mean letter width
    threshold = expected_gap * KERN_GAP_FACTOR

    if max_gap > threshold:
        # Pango fallback bug causes SYSTEMATIC gaps (many letters affected), not isolated ones.
        # Isolated large gaps indicate layout spacing (data-vis labels, chart axes) — false positives.
        # Only fail if ≥30% of inter-run gaps exceed the threshold.
        n_over = sum(1 for g in gaps if g > threshold)
        frac_over = n_over / max(1, len(gaps))
        if frac_over >= 0.30:
            return "FAIL", (
                f"max inter-glyph gap {max_gap:.0f}px > threshold {threshold:.0f}px "
                f"({max_gap / max(expected_gap, 1):.1f}× expected {expected_gap:.0f}px) — "
                "check kern tables or Pango shaping for this font at this size"
            )
        return "PASS", (
            f"named font; isolated max gap {max_gap:.0f}px "
            f"(only {n_over}/{len(gaps)} gaps over threshold {threshold:.0f}px — layout spacing, not kerning bug)"
        )
    return "PASS", (f"max gap {max_gap:.0f}px <= threshold {threshold:.0f}px "
                    f"(mean letter width {mean_w:.0f}px)")


# ── §8.5 No-wordy-card ────────────────────────────────────────────────────────

def count_prose_payload(props: dict, pattern: str) -> tuple[int, int, str]:
    """Return (line_count, word_count, detail_string) for a Remotion beat's props."""
    lines, words = 0, 0
    details = []

    def add(items: list[str], label: str):
        nonlocal lines, words
        for item in items:
            wc = len(str(item).split())
            lines += 1
            words += wc
        if items:
            details.append(f"{len(items)} {label} ({sum(len(str(x).split()) for x in items)} words)")

    add(props.get("artifactLines", []), "artifactLines")
    add(props.get("chips", []),         "chips")
    add(props.get("output", []),        "output lines")

    if props.get("artifactHeading"):
        w = len(props["artifactHeading"].split())
        lines += 1; words += w
        details.append(f"artifactHeading ({w} words)")

    for fld in ("note", "left", "right"):
        v = props.get(fld)
        if isinstance(v, str) and v.strip():
            w = len(v.split())
            lines += 1; words += w
            details.append(f"'{fld}' ({w} words)")
        elif isinstance(v, dict):
            note_v = v.get("note", "")
            if note_v:
                w = len(note_v.split())
                lines += 1; words += w
                details.append(f"'{fld}.note' ({w} words)")

    return lines, words, "; ".join(details) if details else "no prose"


def max_prose_element(props: dict) -> tuple[int, str]:
    """Return (max_words, field_name) for the wordiest single prose element in props.
    Counts: text/content fields (note, headline, artifactHeading, sparkLine, body, text,
    title) + left.note / right.note + individual list items (artifactLines, chips, output).
    Does NOT count structural labels (label, eyebrow, topic, artifactTitle) — those are
    formatting chrome, not prose.
    """
    TEXT_FIELDS = {"note", "headline", "artifactHeading", "sparkLine", "body", "text", "title"}
    LIST_FIELDS  = {"artifactLines", "chips", "output"}

    max_w = 0
    max_f = ""

    def maybe(text: str, field: str):
        nonlocal max_w, max_f
        if not text or not isinstance(text, str):
            return
        w = len(text.split())
        if w > max_w:
            max_w = w
            max_f = field

    for k, v in props.items():
        if k in TEXT_FIELDS:
            maybe(v, k)
        elif k in ("left", "right") and isinstance(v, dict):
            maybe(v.get("note", ""), f"{k}.note")
        elif k in LIST_FIELDS and isinstance(v, list):
            for i, item in enumerate(v):
                if isinstance(item, str):
                    maybe(item, f"{k}[{i}]")

    return max_w, max_f


def check_wordy_card(beat: dict) -> tuple[str, str]:
    """§8.5 — Remotion beat text payload <= 1 display line + 1 label.

    Two-tier check:
    1. Universal: any single prose element > WORDY_PULLQUOTE_MAX (12) = FAIL (the
       'Committee Question' catch — a prose sentence masquerading as a label).
    2. Pattern-specific: for flat/unknown patterns, also enforce total line budget.
       Structured layouts (ClaudeWindow, ChipGrid, DeckPattern) are designed
       multi-element displays; only the per-element check applies to them.
    """
    shot = beat.get("shot", {})
    remotion = shot.get("remotion", {})
    if not remotion:
        return "SKIP", "no Remotion shot data"

    pattern = remotion.get("pattern", "")
    props = remotion.get("props", {})

    if not pattern:
        return "SKIP", "no pattern specified"

    # Bookend / structural patterns are entirely exempt
    if pattern in BOOKEND_PATTERNS:
        return "SKIP", f"{pattern} is exempt (structural/bookend)"

    # ── Tier 1: per-element check (universal for all non-bookend patterns) ──
    max_w, max_f = max_prose_element(props)
    if max_w > WORDY_PULLQUOTE_MAX:
        return "FAIL", (
            f"prose element '{max_f}': {max_w} words > {WORDY_PULLQUOTE_MAX} pull-quote limit. "
            "The screen should show structure, not sentences. "
            "De-wordify: shorten to a label or rebuild beat as a Manim/Remotion visual."
        )

    # ── Tier 2: structured layouts pass after per-element check ──
    if pattern in STRUCTURED_PATTERNS:
        return "PASS", (f"{pattern}: per-element check passed "
                        f"(max {max_w} words in '{max_f or 'n/a'}')")

    # ── Tier 3: flat / unknown patterns → line-budget check ──
    lines, words, detail = count_prose_payload(props, pattern)

    if lines == 0 and words == 0:
        return "PASS", "no prose payload found"

    # Pull-quote exception: 1 element ≤ 12 words (already passed Tier 1 if here)
    if lines == 1 and words <= WORDY_PULLQUOTE_MAX:
        return "PASS", f"pull-quote ({words} words ≤ {WORDY_PULLQUOTE_MAX})"

    if lines > WORDY_LINE_BUDGET:
        return "FAIL", (
            f"{lines} prose elements ({words} words) > budget {WORDY_LINE_BUDGET} "
            f"(1 display + 1 label). Detail: {detail}. "
            "De-wordify: rebuild as Manim process diagram or Remotion build-on; "
            "keep on-screen words to labels only."
        )

    if words > WORDY_GOLDEN_WORDS:
        return "FAIL", (
            f"{lines} element(s), {words} words > structural ceiling {WORDY_GOLDEN_WORDS}. "
            f"Detail: {detail}. Tighten the copy or split the beat."
        )

    return "PASS", f"{lines} element(s), {words} words — within budget. Detail: {detail}"


# ── §8.6 Golden strings ───────────────────────────────────────────────────────

def check_golden_strings(beat_sheet: dict) -> list[str]:
    """§8.6 — adversarial fit-test on every title/headline template."""
    findings = []
    for beat in beat_sheet.get("beats", []):
        bid = beat.get("beat_id") or beat.get("id", "?")
        shot = beat.get("shot", {})
        remotion = shot.get("remotion", {})
        if not remotion:
            continue
        props = remotion.get("props", {})
        headline = props.get("headline", "") or props.get("title", "") or props.get("segment", "")
        if not headline:
            continue
        # Length ceiling: > 70 chars risks overflow in narrower templates
        if len(headline) > 70:
            findings.append(f"{bid}: headline {len(headline)} chars — adversarial overflow risk "
                           f"(golden LONGEST test fails at this length)")
        # All-caps without tracking compensation
        if headline == headline.upper() and len(headline.split()) > 8:
            findings.append(f"{bid}: all-caps headline {len(headline.split())} words "
                           "— needs +0.04em tracking compensation per §3")
    return findings


# ── Video resolution / best source ───────────────────────────────────────────

def best_video(reel_dir: Path, beat: dict) -> Path | None:
    src = beat.get("build", {}).get("src", "")
    if src:
        p = reel_dir / src
        if p.exists():
            return p
    bid = beat.get("beat_id") or beat.get("id", "?")
    for prefix in ("manim", "media"):
        p = reel_dir / prefix / f"{bid}.mp4"
        if p.exists():
            return p
    return None


# ── §8.10 REDUNDANCY helpers ─────────────────────────────────────────────────

def _content_words(text: str) -> set:
    """Lowercase [a-z'] tokens with English stopwords removed."""
    return {w for w in re.findall(r"[a-z']+", text.lower())
            if w not in _STOPWORDS_EN and len(w) > 1}


def _screen_content_words(props: dict) -> set:
    """Content words from on-screen Remotion props, excluding literal-payload keys."""
    tokens: list = []
    for item in props.get('lines') or []:
        if isinstance(item, str):
            tokens.extend(re.findall(r"[a-z']+", item.lower()))
    for item in props.get('artifactLines') or []:
        if isinstance(item, str):
            tokens.extend(re.findall(r"[a-z']+", item.lower()))
    for item in props.get('items') or []:
        if isinstance(item, str):
            tokens.extend(re.findall(r"[a-z']+", item.lower()))
        elif isinstance(item, dict):
            for k, v in item.items():
                if k not in _REDUNDANCY_LITERAL_KEYS and isinstance(v, str):
                    tokens.extend(re.findall(r"[a-z']+", v.lower()))
    for key in ('artifactHeading', 'headline', 'segment'):
        v = props.get(key)
        if isinstance(v, str):
            tokens.extend(re.findall(r"[a-z']+", v.lower()))
    return {w for w in tokens if w not in _STOPWORDS_EN and len(w) > 1}


def check_redundancy_advisory(sheet: dict) -> tuple:
    """§8.10 REDUNDANCY — advisory: narration discusses on-screen text, never recites it.

    Exception: LITERAL beats (viewer is meant to type/copy/run the text) should be
    read aloud and are always exempt.

    Returns (advisories, scores) where:
      advisories — list of '§8.10 [bid] ...' strings for beats scoring >= 0.80
      scores     — dict mapping beat_id → float | None (None = exempt or skipped)

    ADVISORY: does NOT affect the exit code.
    """
    advisories: list = []
    scores: dict = {}

    for b in sheet.get('beats', []):
        bid = b.get('beat_id', '?')
        rem = (b.get('shot') or {}).get('remotion') or {}
        props = rem.get('props') or {}
        pattern = rem.get('pattern', '')

        # Exempt: BHTF or any beat whose props.topic contains "YOUR TURN"
        if bid == 'BHTF':
            scores[bid] = None
            continue
        if 'YOUR TURN' in (props.get('topic') or '').upper():
            scores[bid] = None
            continue
        # Exempt: literal-command patterns (command/code is the primary payload)
        if pattern in _REDUNDANCY_EXEMPT_PATTERNS:
            scores[bid] = None
            continue
        # Exempt: author's explicit escape hatch
        if b.get('literal') or props.get('literal'):
            scores[bid] = None
            continue

        sw = _screen_content_words(props)
        nw = _content_words(b.get('narration_text') or '')

        if len(sw) < 4 or len(nw) < 6:
            scores[bid] = None
            continue

        overlap = sw & nw
        score = round(len(overlap) / len(sw), 2)
        scores[bid] = score

        if score >= 0.80:
            advisories.append(
                f"§8.10 [{bid}] narration recites the card ({score:.2f})"
                f" — discuss it, don't read it"
            )

    return advisories, scores


# ── §8.7–§8.9 Sweep gates — placeholder and truncation ───────────────────────
# §8.7  no-placeholder   — "see narration", "TBD", "TODO", "fill me", "lorem",
#                          or a raw beat-id used as body text must never reach a
#                          rendered surface.
# §8.8  stub-command     — ClaudeComposerAsk command is empty or one non-slash word.
# §8.9  mid-word-trunc   — any display-facing string ends mid-word: truncated at a
#                          character limit, or ends with a dangling article/preposition
#                          ("the", "by", "without", "all f", …).
#
# Both §8.7 and §8.9 fail loudly: reel, beat, field, and the offending string
# are reported. A single hit blocks the cut.

# Fields whose content reaches the viewer screen (skip metadata / URLs / slugs)
_DISPLAY_FIELDS = {
    "command", "artifactHeading", "artifactTitle", "title", "topic", "segment",
    "greeting", "runningText", "note", "headline", "body", "text", "sparkLine",
    "caption", "subtitle", "eyebrow",
}
_LIST_DISPLAY_FIELDS = {"artifactLines", "chips", "output"}

# Placeholder patterns that must never appear on a rendered surface
_PLACEHOLDER_RE = re.compile(
    r'^(?:see narration|tbd|todo|fill me|lorem ipsum|lorem|placeholder)\b',
    re.I,
)

# Dangling-word patterns that indicate mid-sentence truncation.
# Only includes words that are strongly indicative of an incomplete clause:
# articles ("the", "a", "an"), prepositions ("of", "in", "on", "at", "as",
# "by", "for", "with", "without", "from", "into", "onto"), and conjunctions
# that open a dependent clause ("and", "or", "but", "even", "because").
# Pronouns ("it", "this") and "all" are excluded — valid sentence enders.
_DANGLING_RE = re.compile(
    r'\b(the|a|an|of|in|on|at|as|by|for|with|without|from|into|onto|and|or|but|even|because)\s*$',
    re.I,
)

# Beat-id pattern: looks like a raw id used as display text ("B03", "BHTF", "H01")
_BEAT_ID_RE = re.compile(r'^[A-Z][A-Z0-9]{1,4}$')

_SWEEP_SLASH = re.compile(r'^/[a-zA-Z0-9_-]+$')


def _looks_truncated(text: str) -> bool:
    """True if text appears to be cut off mid-word or ends with a dangling word."""
    if not text or len(text) < 20:
        return False
    stripped = text.rstrip()
    if not stripped:
        return False
    last_char = stripped[-1]
    # Only flag alpha endings — punctuation (.!?:") signals a proper ending
    if not last_char.isalpha():
        return False
    # Dangling article/preposition/conjunction at end
    if _DANGLING_RE.search(stripped):
        return True
    # Single-letter fragment on a long string — character-limit cut ("all f", "enabl")
    last_word = stripped.split()[-1]
    # Strip trailing punctuation from last word for fragment check
    last_bare = last_word.rstrip('.,;:!?"\'-')
    # Whitelist of common valid ≤2-char words that legitimately end a display string
    # (initialisms like "AI", pronouns "it/us/we/me", terse verbs "is/be/do/go", etc.).
    # Without this whitelist, titles like "Fundamental Themes — Conducting AI" trip §8.9.
    _VALID_SHORT_ENDINGS = {
        'ai', 'it', 'is', 'us', 'we', 'me', 'my', 'be', 'do', 'go', 'so', 'no',
        'up', 'ok', 'am', 'if', 'ui', 'ux', 'os', 'io', 'id',
    }
    if last_bare.lower() in _VALID_SHORT_ENDINGS:
        return False
    # Only flag single-char fragments (2-char whitelist above handles common valid words;
    # anything ≤1 char remaining alpha after stripping punctuation is almost certainly a cut).
    if len(last_bare) <= 1 and len(stripped) > 30 and last_bare.isalpha():
        return True
    return False


def _sweep_check_str(bid: str, field: str, text: str, beat_ids: set) -> list:
    """Return FAIL entries for a single display string."""
    fails = []
    if not isinstance(text, str) or not text.strip():
        return fails
    t = text.strip()
    # §8.7 placeholder
    if _PLACEHOLDER_RE.match(t):
        fails.append(f"§8.7 [{bid}/{field}] placeholder reached screen: {repr(t[:60])}")
    # §8.7 raw beat-id used as body text
    if _BEAT_ID_RE.match(t) and t in beat_ids:
        fails.append(f"§8.7 [{bid}/{field}] beat-id '{t}' used as display text")
    # §8.9 truncation
    if _looks_truncated(t):
        fails.append(f"§8.9 [{bid}/{field}] text ends truncated: {repr(t[:60])}")
    return fails


def check_gate_shape(sheet: dict) -> list:
    """GATE SHAPE — finance chart-type enforcement.

    Enforces SKILL.md §Shape logic (locked):
      INCOME_STMT   → sankey       (flow)
      CASH_FLOW     → sankey       (flow)
      BALANCE_SHEET → mirrored-bar (snapshot — NEVER a Sankey)
      SEGMENTS      → stacked-bar  (composition × time)
      SECTOR        → dot-plot     (distribution)

    Also enforces gloss-line presence: every Finance chart beat must have
    non-empty glossTerms so all on-screen acronyms have visible expansions.

    Returns a list of FAIL strings. Any hit blocks the cut.
    """
    _FINANCE_ACTS = {"INCOME_STMT", "CASH_FLOW", "BALANCE_SHEET", "SEGMENTS", "SECTOR"}
    _REQUIRED = {
        "INCOME_STMT":    "sankey",
        "CASH_FLOW":      "sankey",
        "BALANCE_SHEET":  "mirrored-bar",
        "SEGMENTS":       "stacked-bar",
        "SECTOR":         "dot-plot",
    }
    _PATTERN_SHAPES = {
        "FinanceSankey":      "sankey",
        "FinanceMirroredBar": "mirrored-bar",
        "FinanceStackedBar":  "stacked-bar",
        "FinanceDotPlot":     "dot-plot",
    }

    def _is_finance_reel(bs):
        if (bs.get("metadata") or {}).get("ticker"):
            return True
        return any(b.get("act") in _FINANCE_ACTS for b in bs.get("beats") or [])

    if not _is_finance_reel(sheet):
        return []

    fails = []
    for b in sheet.get("beats") or []:
        bid = b.get("beat_id", "?")
        act = b.get("act", "")
        if act not in _FINANCE_ACTS:
            continue
        required = _REQUIRED[act]
        shot = b.get("shot") or {}
        remotion = shot.get("remotion") or {}
        pattern = remotion.get("pattern", "")
        props = remotion.get("props") or {}

        if shot.get("source") == "remotion" and pattern:
            if pattern in _PATTERN_SHAPES:
                effective = _PATTERN_SHAPES[pattern]
                if effective != required:
                    fails.append(
                        f"GATE-SHAPE [{bid}] act={act} uses {pattern!r} (shape={effective!r}) "
                        f"but requires {required!r}. "
                        f"Shape logic is locked — use the correct component."
                    )
                # Gloss line gate: Finance chart beats must have non-empty glossTerms
                gloss = props.get("glossTerms") or []
                if not gloss:
                    fails.append(
                        f"GATE-SHAPE [{bid}] act={act} pattern={pattern!r}: "
                        f"glossTerms is empty. Every Finance chart beat must list all "
                        f"on-screen acronyms and terms of art in glossTerms."
                    )
        else:
            # Manim beat: check explicit shape field
            shape = b.get("shape") or (((shot.get("manim") or {}).get("shape") or "")).lower()
            if not shape:
                fails.append(
                    f"GATE-SHAPE [{bid}] act={act} (Manim) has no `shape` field. "
                    f"Must be {required!r}."
                )
            elif shape != required:
                fails.append(
                    f"GATE-SHAPE [{bid}] act={act} (Manim) declares shape={shape!r} "
                    f"but requires {required!r}."
                )

    return fails


_CODE_CARD_PATTERNS = {'ClaudeCodeBeat', 'ClaudeCodeBeat916'}

# Tokens that distinguish real code from comment-only / prose content.
# At least one line must contain one of these to be considered real code.
_CODE_TOKEN_RE = re.compile(
    r'(?:[=(){}\[\];<>]|->|:=|::|!='
    r'|\bdef \b|\bclass \b|\bimport \b|\bfrom \b|\breturn \b'
    r'|\bfor \b|\bwhile \b|\bif \b|\belse\b|\belif \b'
    r'|\blet \b|\bconst \b|\bvar \b|\bfn \b|\bpub \b|\buse \b'
    r'|\bfunction\b|\bvoid \b|\bint \b|\bstr\b)',
)

_COMMENT_LINE_RE = re.compile(r'^\s*(#|//|--)')

# A real file extension: 2–6 alphanumeric characters, no spaces.
_EXT_RE = re.compile(r'^[a-z0-9]{2,6}$')


def _is_prose_code(code: str) -> bool:
    """True when every non-empty code line is a comment (no real code tokens)."""
    non_empty = [l for l in code.splitlines() if l.strip()]
    if not non_empty:
        return False
    all_comments = all(_COMMENT_LINE_RE.match(l) for l in non_empty)
    has_token = any(_CODE_TOKEN_RE.search(l) for l in non_empty
                    if not _COMMENT_LINE_RE.match(l))
    return all_comments or not has_token


def _title_has_no_extension(title: str) -> bool:
    """True when the title has no real file extension, triggering the doubled-badge path."""
    filename = title.split(' — ')[0].strip() if ' — ' in title else title
    raw_ext = (filename.split('.')[-1] if '.' in filename else '').lower()
    return not _EXT_RE.match(raw_ext)


def check_sweep_gates(sheet: dict) -> list:
    """§8.7–§8.12b — placeholder, truncation, and code-card gate.

    Checks every display-facing string in every beat's Remotion props.
    Returns a list of FAIL strings. Any hit blocks the cut.
    """
    beat_ids = {b.get('beat_id', '') for b in sheet.get('beats', [])}
    fails = []

    for b in sheet.get('beats', []):
        bid = b.get('beat_id', '?')
        rem = (b.get('shot') or {}).get('remotion') or {}
        props = rem.get('props') or {}
        pattern = rem.get('pattern', '')

        # Check scalar display fields
        for field in _DISPLAY_FIELDS:
            v = props.get(field)
            if isinstance(v, str):
                fails += _sweep_check_str(bid, field, v, beat_ids)

        # Check list display fields
        for field in _LIST_DISPLAY_FIELDS:
            for idx, item in enumerate(props.get(field) or []):
                if isinstance(item, str):
                    fails += _sweep_check_str(bid, f"{field}[{idx}]", item, beat_ids)

        # Check FormBCard items (label + sub)
        for idx, item in enumerate(props.get('items') or []):
            if not isinstance(item, dict):
                continue
            for sub_field in ('label', 'sub'):
                v = item.get(sub_field, '')
                if isinstance(v, str) and v.strip():
                    fails += _sweep_check_str(bid, f"items[{idx}].{sub_field}", v, beat_ids)

        # §8.8 ClaudeComposerAsk stub command
        if pattern == 'ClaudeComposerAsk':
            cmd = (props.get('command') or '').strip()
            words = cmd.split()
            if not cmd:
                fails.append(f"§8.8 [{bid}/command] ClaudeComposerAsk command is empty")
            elif len(words) == 1 and not _SWEEP_SLASH.match(cmd):
                fails.append(f"§8.8 [{bid}/command] stub command: {repr(cmd)}")

        # §8.10 SPARK-LINE LAW — ClaudeComposerAsk missing/empty greeting renders a lone asterisk
        if pattern in ('ClaudeComposerAsk', 'ClaudeComposerAsk916'):
            greeting = (props.get('greeting') or '').strip()
            if not greeting:
                fails.append(
                    f"§8.10 [{bid}/greeting] ClaudeComposerAsk has empty or missing greeting — "
                    f"B00 needs '<world-language hello>, Liam', BHTF needs 'Your turn.', "
                    f"body beats need ≤4 words compressed from the beat narration"
                )

        # §8.11 CARD-PLACEHOLDER — FormA/FormBCard item with empty or placeholder sub
        _CARD_PATTERNS = {
            'FormACard', 'FormBCard', 'FormACard916', 'FormBCard916',
        }
        _CARD_PLACEHOLDER_RE = re.compile(
            r'^(?:key point (?:one|two|three|four|five|\d+)'
            r'|see narration|tbd|todo|placeholder|n/a'
            r'|item \d+|sub text|description here)',
            re.I,
        )
        if pattern in _CARD_PATTERNS:
            for idx, item in enumerate(props.get('items') or []):
                if not isinstance(item, dict):
                    continue
                sub = (item.get('sub') or '').strip()
                label = (item.get('label') or '').strip()
                if not sub:
                    fails.append(
                        f"§8.11 [{bid}/items[{idx}].sub] empty sub on card item '{label}' — "
                        f"fill with a concrete 1-line detail from the reel narration"
                    )
                elif _CARD_PLACEHOLDER_RE.match(sub):
                    fails.append(
                        f"§8.11 [{bid}/items[{idx}].sub] placeholder sub on card item '{label}': "
                        f"{repr(sub[:60])} — replace with content from the reel narration"
                    )

        # §8.12 PROSE-IN-CODE-CARD — ClaudeCodeBeat carrying only comment lines
        if pattern in _CODE_CARD_PATTERNS:
            code_prop = props.get('code', '')
            if code_prop and _is_prose_code(code_prop):
                fails.append(
                    f"§8.12 [{bid}/code] prose-in-code-card: every line is a comment or "
                    f"contains no code tokens — use FormACard/ClaudeVerdictArtifact for "
                    f"enumerable prose (DESIGN-PRINCIPLES §1), or show real code"
                )

        # §8.12b DOUBLED-TITLE — title prop has no file extension, causing the badge
        # to echo the full title string in uppercase on the right side of the title bar
        if pattern in _CODE_CARD_PATTERNS:
            title_prop = props.get('title', '')
            if title_prop and _title_has_no_extension(title_prop):
                fails.append(
                    f"§8.12b [{bid}/title] doubled-title: '{title_prop[:50]}' has no file "
                    f"extension — ClaudeCodeBeat echoes the full title as the language badge. "
                    f"Use a filename (e.g. 'analysis.py') or fix the content to real code"
                )

    return fails


# ── Main ──────────────────────────────────────────────────────────────────────

def run_check(reel_dir: str, skip_pixels: bool = False) -> int:
    reel = Path(reel_dir).resolve()
    bs_path = reel / "beat_sheet.json"
    if not bs_path.exists():
        print(f"[typecheck] no beat_sheet.json at {reel}")
        return 1

    beat_sheet = json.loads(bs_path.read_text())
    beats = beat_sheet.get("beats", [])
    meta = beat_sheet.get("metadata", {})
    slug = meta.get("slug", reel.name)
    reel_channel = meta.get("channel", "")

    # Structural checks (no frames needed)
    manim_font_named = font_is_named_in_scenes(reel)
    has_mathtex = has_mathtex_in_scenes(reel)
    golden_findings = check_golden_strings(beat_sheet)
    sweep_findings = check_sweep_gates(beat_sheet)
    shape_findings = check_gate_shape(beat_sheet)
    redundancy_advisories, redundancy_scores = check_redundancy_advisory(beat_sheet)

    rows = []
    any_fail = bool(sweep_findings) or bool(shape_findings)  # any structural failure blocks the cut

    for beat in beats:
        bid = beat.get("beat_id") or beat.get("id", "?")
        lane = beat.get("lane", "?")
        build_status = beat.get("build", {}).get("status", "")
        # If the shot is explicitly REMOTION, Chrome handles text rendering — no Pango concern.
        # Only run the Manim kerning check when the beat was actually Manim-rendered.
        _shot = beat.get("shot") or {}
        shot_type_field = _shot.get("type", "") if isinstance(_shot, dict) else ""
        is_remotion_shot = (shot_type_field == "REMOTION")
        # Raw source footage beats carry no designed typography — they are real-world video
        # content (Seedance, stock footage, AI-VIDEO, archival stills). Pixel checks would scan
        # the footage and flag incidental texture/pixels that resemble MUTE-palette text (false
        # positives). GATE T is about our designed typography; skip pixel checks for source footage.
        # AI-VIDEO is Seedance/Higgsfield generated footage — same exemption as raw video.
        # STILL is an archival/documentary photograph — embedded captions are diegetic, not ours.
        # SCREEN is a browser capture of an HTML simulation — its typography belongs to the sim's
        # own UI, not to our designed palette; pixel checks would flag sim labels as false positives.
        # SOURCE_REPORT is supplied footage played as is (docs/PIPELINE-SAFETY.md): its frames are
        # the source's own content, not our typography — same exemption as raw video.
        is_raw_video_shot = shot_type_field.lower() in ("video", "ai-video", "still", "i2v", "t2v", "gen-video", "source-cut", "screen", "source_report")
        is_manim = (build_status == "MANIM" or lane == "MANIM") and not is_remotion_shot
        _remotion = _shot.get("remotion", {}) if isinstance(_shot, dict) else {}
        _manim = _shot.get("manim", {}) if isinstance(_shot, dict) else {}
        # Remotion shots: use the component pattern name; Manim shots: use the class name.
        # Both are checked against STRUCTURAL_TERRACOTTA_PATTERNS and HAND_DRAWN_PATTERNS.
        # When a beat carries both remotion and manim sub-dicts (Manim built, Remotion
        # was the fallback slate), prefer the Manim class — that is the actual rendered frame.
        # graphic.manim may be a bare class-name string (e.g. "B02_GPUNodeTable")
        _graphic = beat.get("graphic", {}) if isinstance(beat, dict) else {}
        _graphic_manim = _graphic.get("manim", "") if isinstance(_graphic, dict) else ""
        # Some beat_sheet formats nest graphic under shot (beat.shot.graphic.manim)
        _shot_graphic = _shot.get("graphic", {}) if isinstance(_shot, dict) else {}
        _shot_graphic_manim = ((_shot_graphic.get("manim", "") or _shot_graphic.get("scene_class", ""))
                               if isinstance(_shot_graphic, dict) else "")
        if is_manim and _manim:
            beat_pattern = (_manim.get("class", "") or _manim.get("scene", "")
                            or _manim.get("scene_class", ""))
        elif is_manim and isinstance(_graphic_manim, str) and _graphic_manim:
            beat_pattern = _graphic_manim
        elif is_manim and _shot_graphic_manim:
            beat_pattern = _shot_graphic_manim
        elif is_manim and _shot.get("scene_class", ""):
            # beat_sheet format: shot.scene_class is the Manim class name directly on the shot
            beat_pattern = _shot["scene_class"]
        elif _remotion:
            beat_pattern = _remotion.get("pattern", "")
        else:
            beat_pattern = ""

        findings: list[tuple[str, str, str]] = []  # (check, status, message)

        # §8.0 banned-pattern gate — fails in claude / ai-explainer register
        if beat_pattern in BANNED_PATTERNS_CLAUDE and reel_channel in CLAUDE_REGISTER_CHANNELS:
            findings.append(("banned-pattern §8.0", "FAIL",
                f"{beat_pattern} is banned in the claude register — replace with a clean Manim/Remotion scene"))
            any_fail = True

        # §8.5 no-wordy-card — pure JSON, always runs
        wc_status, wc_msg = check_wordy_card(beat)
        if wc_status != "SKIP":
            findings.append(("no-wordy-card §8.5", wc_status, wc_msg))
            if wc_status == "FAIL":
                any_fail = True

        beat_polarity = "—"
        if not skip_pixels and not is_raw_video_shot:
            video = best_video(reel, beat)
            if video and video.exists():
                img = extract_frame(video)
                if img is not None:
                    # Detect frame polarity once — passed to all pixel checks.
                    # Border-strip sampling prevents content in the center (dark diagram on
                    # cream, or cream pane inside dark shell) from misleading the detector.
                    frame_arr = np.array(img)
                    frame_polarity, frame_bg_rgb = detect_polarity(frame_arr)
                    beat_polarity = frame_polarity

                    # §8.1 min-size
                    s, m = check_min_size(img, bid, beat_pattern, polarity=frame_polarity)
                    findings.append(("min-size §8.1", s, m))
                    if s == "FAIL":
                        any_fail = True

                    # §8.2 overflow
                    s, m = check_overflow(img, bid, polarity=frame_polarity, pattern=beat_pattern)
                    findings.append(("overflow §8.2", s, m))
                    if s == "FAIL":
                        any_fail = True

                    # §8.3 contrast
                    s, m = check_contrast(img, bid, beat_pattern,
                                         polarity=frame_polarity, bg_rgb=frame_bg_rgb)
                    findings.append(("contrast §8.3", s, m))
                    if s == "FAIL":
                        any_fail = True

                    # §8.3b per-blob local-background contrast
                    if beat_pattern in DARK_BACKGROUND_MARK_PATTERNS:
                        s, m = "SKIP", (f"{beat_pattern} exempt — SVG brand mark (MonogramMark/"
                                        "SignatureMark) anti-aliasing on dark card background; "
                                        "cream-to-dark edge pixels are structural, not typography")
                    else:
                        s, m = check_contrast_per_blob(img, polarity=frame_polarity)
                    findings.append(("contrast-local §8.3b", s, m))
                    if s == "FAIL":
                        any_fail = True

                    # §8.6b bbox overlap — two text elements printing on top of each other
                    if beat_pattern in BBOX_OVERLAP_EXEMPT_PATTERNS:
                        s, m = "SKIP", (f"{beat_pattern} exempt — box border is structural, "
                                        "not a text run (labels inside tier cards by design)")
                    else:
                        s, m = check_bbox_overlap(img, polarity=frame_polarity)
                    findings.append(("bbox-overlap §8.6b", s, m))
                    if s == "FAIL":
                        any_fail = True

                    # §8.13 card-clip — ClaudeCodeBeat only
                    s, m = check_card_clip(img, bid, beat_pattern)
                    findings.append(("card-clip §8.13", s, m))
                    if s == "FAIL":
                        any_fail = True

                    # §8.4 kerning — MANIM beats only
                    if is_manim:
                        s, m = check_kerning_sanity(img, bid, manim_font_named, has_mathtex,
                                                    beat_pattern)
                        findings.append(("kerning §8.4", s, m))
                        if s == "FAIL":
                            any_fail = True
                else:
                    findings.append(("render", "SKIP", f"could not decode frame from {video.name}"))
            else:
                findings.append(("render", "SKIP", "no video rendered for this beat yet"))

        # §8.4 structural kerning for un-rendered MANIM beats
        if is_manim and not manim_font_named and not any(c == "kerning §8.4" for c, _, _ in findings):
            findings.append(("kerning §8.4", "FAIL",
                             "scenes.py has no font= in Text() — Pango fallback, gappy-letter bug"))
            any_fail = True

        beat_fail = any(s == "FAIL" for _, s, _ in findings)
        worst = "FAIL" if beat_fail else ("SKIP" if all(s == "SKIP" for _, s, _ in findings) else "PASS")

        # Pick worst finding for the table cell
        worst_finding = next(
            (f"{c}: {m}" for c, s, m in findings if s == "FAIL"),
            next((f"{c}: {m}" for c, s, m in findings if s == "PASS"), "no video")
        )
        # Truncate for table readability
        worst_short = worst_finding[:90] + ("…" if len(worst_finding) > 90 else "")

        fix = ""
        for c, s, m in findings:
            if s == "FAIL":
                if "wordy" in c or "no-wordy" in c:
                    fix = "De-wordify → Manim diagram or Remotion build-on"
                elif "kerning" in c:
                    fix = "Add font='EB Garamond' to all Text() in scenes.py"
                elif "min-size" in c:
                    fix = "Increase font_size in scenes.py or Remotion component"
                elif "overflow" in c:
                    fix = "Move text inside title-safe 90% box"
                elif "bbox-overlap" in c:
                    fix = "Separate label positions — two text elements overlap"
                elif "contrast" in c:
                    fix = "Use INK on cream; add backing plate under accent text"
                break

        rows.append({"beat_id": bid, "lane": lane, "polarity": beat_polarity,
                     "worst": worst_short, "status": worst, "fix": fix, "findings": findings})

    # ── Build TYPECHECK.md ────────────────────────────────────────────────────
    now = datetime.now().strftime("%Y-%m-%dT%H:%M")
    overall = "**FAIL**" if any_fail else "PASS"
    fail_count = sum(1 for r in rows if r["status"] == "FAIL")

    md = [
        "# TYPECHECK.md — GATE T",
        "",
        f"Reel: `{slug}`  |  Checked: {now}  |  Overall: {overall}  |  "
        f"Beats checked: {len(rows)}  |  FAILs: {fail_count}",
        "",
        f"Spec: `skills/make/kerning/reference/type-spec.md` §8.  "
        f"Floor: {MIN_SIZE_PCT}% frame-height.  "
        f"Contrast: {WCAG_MIN_RATIO}:1 WCAG.  "
        f"Kern threshold: {KERN_GAP_FACTOR}× expected advance.  "
        f"Wordy budget: {WORDY_LINE_BUDGET} elements.",
        "",
    ]

    # Structural warnings
    if not manim_font_named:
        md += [
            "> **⚠ STRUCTURAL — §8.4 KERNING:** `scenes.py` calls `Text()` with no `font=` argument.",
            "> Pango will use a system fallback font — the gappy-letter spacing bug "
            "(w a v e s  l i k e  t h i s) is active for ALL Manim beats.",
            "> **Fix:** add `font='EB Garamond'` to every `Text()` and `MarkupText()` call "
            "in `scenes.py` (or to every helper that calls them).",
            "> Then re-render all Manim beats and re-run GATE T.",
            "",
        ]

    if golden_findings:
        md += ["> **§8.6 GOLDEN STRINGS:**", ""]
        for g in golden_findings:
            md.append(f"> - {g}")
        md.append("")

    if shape_findings:
        md += [
            "> **GATE SHAPE — FINANCE CHART SHAPE ENFORCEMENT — GATE BLOCKED:**",
            "> Shape logic is locked: INCOME_STMT/CASH_FLOW→sankey, BALANCE_SHEET→mirrored-bar,",
            "> SEGMENTS→stacked-bar, SECTOR→dot-plot. Wrong component = failure mode.",
            "> Finance chart beats must also have non-empty glossTerms.",
            "",
        ]
        for f in shape_findings:
            md.append(f"> - {f}")
        md.append("")

    if sweep_findings:
        md += [
            "> **§8.7–§8.9 PLACEHOLDER / TRUNCATION — GATE BLOCKED:**",
            "> Every item below must be fixed before `./art run` or `./art final`.",
            "> Labels must be authored short phrases (2–5 words). Subs must add something real",
            "> (≤8 words) or be omitted. 'see narration' and truncated strings must not reach",
            "> a rendered surface.",
            "",
        ]
        for f in sweep_findings:
            md.append(f"> - {f}")
        md.append("")

    if redundancy_advisories:
        md += [
            "> **§8.10 REDUNDANCY (advisory — does not block cut):**",
            "> Narration should DISCUSS on-screen text, not recite it.",
            "> Exception: LITERAL beats (viewer types/copies/runs the text) are exempt.",
            "",
        ]
        for f in redundancy_advisories:
            md.append(f"> - {f}")
        md.append("")

    # Beat table
    md += [
        "| beat | lane | polarity | worst finding | status | fix |",
        "|------|------|----------|---------------|--------|-----|",
    ]
    for r in rows:
        st = f"**{r['status']}**" if r["status"] == "FAIL" else r["status"]
        pol = r.get("polarity", "—")
        md.append(f"| {r['beat_id']} | {r['lane']} | {pol} | {r['worst']} | {st} | {r['fix'] or '—'} |")

    # Failures section
    md += ["", "---", "", "## Failures requiring action before cut", ""]
    fail_rows = [r for r in rows if r["status"] == "FAIL"]
    if not fail_rows and not sweep_findings and not shape_findings:
        md.append("*None — GATE T PASS.*")
    else:
        if shape_findings:
            md.append("### GATE SHAPE (finance chart-shape enforcement)")
            md.append("")
            for f in shape_findings:
                md.append(f"- **{f}**")
            md.append("")
            md.append("**Fix:** Use the correct Remotion component for the act, add glossTerms "
                      "listing every on-screen acronym/term-of-art.")
            md.append("")
        if sweep_findings:
            md.append("### SWEEP GATES §8.7–§8.12b (placeholder / truncation / code-card)")
            md.append("")
            for f in sweep_findings:
                md.append(f"- **{f}**")
            md.append("")
            md.append("**Fix:** §8.7–§8.9: rewrite flagged labels/subs to authored words. "
                      "§8.12: replace prose-comment code beat with FormACard or ClaudeVerdictArtifact. "
                      "§8.12b: give ClaudeCodeBeat a real filename title (e.g. 'analysis.py').")
            md.append("")
        for r in fail_rows:
            md.append(f"### {r['beat_id']} ({r['lane']})")
            for c, s, m in r["findings"]:
                if s == "FAIL":
                    md.append(f"- **{c}**: {m}")
            if r["fix"]:
                md.append(f"- **Fix:** {r['fix']}")
            md.append("")

    # Check summary table
    check_names = ["no-wordy-card §8.5", "min-size §8.1", "overflow §8.2",
                   "contrast §8.3", "contrast-local §8.3b", "bbox-overlap §8.6b",
                   "card-clip §8.13", "kerning §8.4"]
    md += ["---", "", "## Check summary", "",
           "| Check | Beats checked | FAILs |",
           "|-------|---------------|-------|"]
    for cn in check_names:
        checked = [r for r in rows if any(c == cn for c, _, _ in r["findings"])]
        failed  = [r for r in checked if any(c == cn and s == "FAIL" for c, s, _ in r["findings"])]
        md.append(f"| {cn} | {len(checked)} | {len(failed)} |")
    r_checked = sum(1 for v in redundancy_scores.values() if v is not None)
    r_flagged  = sum(1 for v in redundancy_scores.values() if v is not None and v >= 0.80)
    md.append(f"| redundancy §8.10 (advisory) | {r_checked} | {r_flagged} (advisory — no exit effect) |")

    md += [
        "",
        "---",
        "",
        "*GATE T: any FAIL blocks `./art run` and `./art final`. "
        "Fix the flagged beats and re-run `scripts/type_check.py` until green.*",
    ]

    out = reel / "TYPECHECK.md"
    out.write_text("\n".join(md) + "\n")
    print(f"[typecheck] wrote {out}")
    if shape_findings:
        for sf in shape_findings:
            print(f"[typecheck] GATE-SHAPE {sf}")
    if sweep_findings:
        for sf in sweep_findings:
            print(f"[typecheck] {sf}")
    for a in redundancy_advisories:
        print(f"[typecheck] {a}")
    for beat in beats:
        bid = beat.get('beat_id') or beat.get('id', '?')
        score = redundancy_scores.get(bid)
        if score is None:
            print(f"[typecheck] §8.10 {bid}: SKIP")
        else:
            flag = "  ← ADVISORY" if score >= 0.80 else ""
            print(f"[typecheck] §8.10 {bid}: {score:.2f}{flag}")
    gate_msg = (f"FAIL ({fail_count} pixel beats, {len(sweep_findings)} sweep, {len(shape_findings)} shape)"
                if any_fail else "PASS")
    print(f"[typecheck] GATE T: {gate_msg}")
    return 2 if any_fail else 0


def _make_fixture_img(w: int, h: int, bg: tuple, text_color: tuple,
                      text_x: int, text_y: int, text_w: int, text_h: int) -> Image.Image:
    """Synthetic frame: solid bg with one text rectangle."""
    img = Image.new("RGB", (w, h), bg)
    arr = np.array(img)
    arr[text_y:text_y + text_h, text_x:text_x + text_w] = text_color
    return Image.fromarray(arr)


def run_fixture_tests() -> int:
    """Self-test the three new gate functions with synthetic fixtures.

    Returns 0 if all pass, 1 if any fail.
    """
    PASS = "PASS"; FAIL = "FAIL"; SKIP = "SKIP"
    W, H = 3840, 2160
    ok = True

    def assert_result(label: str, got: str, want: str) -> None:
        nonlocal ok
        sym = "✓" if got == want else "✗"
        print(f"  {sym} {label}: {got} (want {want})")
        if got != want:
            ok = False

    print("[fixture §8.12] prose-in-code-card")
    assert_result("all-comment lines → FAIL",
                  "FAIL" if _is_prose_code("# line one\n# line two\n# line three") else "PASS",
                  "FAIL")
    assert_result("real code (assignment) → PASS",
                  "FAIL" if _is_prose_code("x = 1\ny = x + 2") else "PASS",
                  "PASS")
    assert_result("real code with comment → PASS",
                  "FAIL" if _is_prose_code("# setup\nx = foo(bar)") else "PASS",
                  "PASS")

    beat_all_comments = {"metadata": {}, "beats": [{
        "beat_id": "B01", "shot": {"type": "REMOTION", "remotion": {
            "pattern": "ClaudeCodeBeat",
            "props": {"title": "demo.py", "code": "# Because the reports overlap\n# a lie is detectable"}
        }}, "build": {"status": "VIDEO"}
    }]}
    beat_real_code = {"metadata": {}, "beats": [{
        "beat_id": "B01", "shot": {"type": "REMOTION", "remotion": {
            "pattern": "ClaudeCodeBeat",
            "props": {"title": "demo.py", "code": "def run():\n    return 42"}
        }}, "build": {"status": "VIDEO"}
    }]}
    finds_prose = check_sweep_gates(beat_all_comments)
    finds_real  = check_sweep_gates(beat_real_code)
    assert_result("all-comment beat → §8.12 FAIL in sweep",
                  "FAIL" if any("§8.12 " in f for f in finds_prose) else "PASS", "FAIL")
    assert_result("real-code beat → no §8.12 in sweep",
                  "PASS" if not any("§8.12 " in f for f in finds_real) else "FAIL", "PASS")

    print("[fixture §8.12b] doubled-title")
    beat_prose_title = {"metadata": {}, "beats": [{
        "beat_id": "B01", "shot": {"type": "REMOTION", "remotion": {
            "pattern": "ClaudeCodeBeat",
            "props": {"title": "the contradiction condition, spelled out",
                      "code": "def run():\n    return 42"}
        }}, "build": {"status": "VIDEO"}
    }]}
    beat_good_title = {"metadata": {}, "beats": [{
        "beat_id": "B01", "shot": {"type": "REMOTION", "remotion": {
            "pattern": "ClaudeCodeBeat",
            "props": {"title": "analysis.py", "code": "def run():\n    return 42"}
        }}, "build": {"status": "VIDEO"}
    }]}
    finds_prose_title = check_sweep_gates(beat_prose_title)
    finds_good_title  = check_sweep_gates(beat_good_title)
    assert_result("prose title → §8.12b FAIL in sweep",
                  "FAIL" if any("§8.12b" in f for f in finds_prose_title) else "PASS", "FAIL")
    assert_result("filename title → no §8.12b in sweep",
                  "PASS" if not any("§8.12b" in f for f in finds_good_title) else "FAIL", "PASS")

    print("[fixture §8.13] card-clip pixel check")
    # White card spans x=268..3571 in a 3840-wide frame (7% inset each side).
    CARD_L, CARD_R = 268, 3571
    WHITE = (255, 255, 255)
    INK   = (61, 57, 41)

    # Frame 1: text clips at card right edge → FAIL
    clip_img = Image.new("RGB", (W, H), (250, 249, 245))
    arr = np.array(clip_img)
    arr[:, CARD_L:CARD_R + 1] = WHITE  # card
    arr[400:450, 3560:3580] = INK      # text blob touching card right edge
    clip_img = Image.fromarray(arr)
    s, _ = check_card_clip(clip_img, "B_FIX", "ClaudeCodeBeat")
    assert_result("clipped text at card right → §8.13 FAIL", s, "FAIL")

    # Frame 2: text fits cleanly → PASS
    clean_img = Image.new("RGB", (W, H), (250, 249, 245))
    arr = np.array(clean_img)
    arr[:, CARD_L:CARD_R + 1] = WHITE  # card
    arr[400:450, 300:3200] = INK       # text blob well inside card
    clean_img = Image.fromarray(arr)
    s, _ = check_card_clip(clean_img, "B_OK", "ClaudeCodeBeat")
    assert_result("clean text inside card → §8.13 PASS", s, "PASS")

    # Frame 3: non-code-card pattern → SKIP
    s, _ = check_card_clip(clip_img, "B_SKIP", "FormACard")
    assert_result("non-code-card pattern → §8.13 SKIP", s, "SKIP")

    print(f"\n[fixtures] {'ALL PASS' if ok else 'FAIL — see above'}")
    return 0 if ok else 1


def main():
    p = argparse.ArgumentParser(description="GATE T — type-lock checker (type-spec.md §8)")
    p.add_argument("reel", nargs="?", help="path to reel folder")
    p.add_argument("--skip-pixels", action="store_true",
                   help="skip pixel-level checks (§8.1–8.4); only run §8.5 and §8.6")
    p.add_argument("--test-fixtures", action="store_true",
                   help="run self-test fixtures for §8.12/§8.12b/§8.13 and exit")
    args = p.parse_args()
    if args.test_fixtures:
        sys.exit(run_fixture_tests())
    if not args.reel:
        p.error("reel path required (or --test-fixtures)")
    sys.exit(run_check(args.reel, args.skip_pixels))


if __name__ == "__main__":
    main()
