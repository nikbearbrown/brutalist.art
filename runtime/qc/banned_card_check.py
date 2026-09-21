#!/usr/bin/env python3
"""banned_card_check.py — GATE BANNED-CARD
Detects DESIGN-PRINCIPLES §1 banned card patterns in a reel's beat_sheet.json.

EXIT CODES:
  0 — clean
  1 — advisories only (no blockers)
  2 — one or more blockers

BLOCKERS (BC):
  BC-1: SlateCard pattern — always banned (VOX-token, bold display sans, eyebrow,
        GOLD rule, decorative circle). Replace with FormACard.
  BC-2: ClaudeWindow view='artifact' used for a non-bookend body beat.
        Body card beats MUST use FormACard; ClaudeWindow is for UI-skin beats only
        (ASK→RESULT, verdict panel) and the BVDT bookend.
  BC-3: Banned prop fields — any beat containing props keys 'eyebrow', 'kicker', or
        'headline' (SlateCard-family field names; FormACard/FormBCard have neither).
  BC-4: OutroSeries or OutroCTA in a non-bookend beat — old vox outro patterns;
        must be replaced with the ClaudeTitleOutro + ClaudeComposerAsk bookend pair.

ADVISORIES (BA):
  BA-5: Text truncation — any artifactLines item or lines item ending with '…' or
        a dash+conjunction ('— and', '— but', '— or', '—and'). Never truncate text
        to fit the card; split the beat or tighten the copy instead.
"""

import json, sys
from pathlib import Path

BOOKEND_IDS = frozenset({'B00', 'BVDT', 'BHTF', 'BOUT'})
BANNED_PROP_KEYS = frozenset({'eyebrow', 'kicker', 'headline'})
OLD_OUTRO_PATTERNS = frozenset({'OutroSeries', 'OutroCTA'})
TRUNCATION_SUFFIXES = ('…', '— and', '—and', '— but', '—but', '— or', '—or')

# These patterns legitimately use props named 'eyebrow' or 'headline' for
# non-card purposes (scene captions, scene labels, etc.) — skip BC-3 for them.
BC3_EXEMPT_PATTERNS = frozenset({
    'DoodleScene', 'DoodleChart',            # scene caption
    'ClaudeComposerAsk',                      # legacy unused prop
    'NikBearBrownTerminalAsk', 'MedhavyTerminalAsk',  # terminal prompt labels
    'FluencySegmentCard', 'FluencyDivergence', 'FluencyThreshold',  # custom scene types
    'FluencySourceFlow', 'FluencyScale', 'FluencyChipGrid',
    'FluencyVerdictStamps', 'AttritionChain',
    # GitHub dark skin — headline/kicker are schema fields, not SlateCard-family props
    'GitHubRepoHero', 'GitHubSectionRail', 'GitHubStructureMap',
    'GitHubCallChain', 'GitHubChurn', 'GitHubBucketList',
    'GitHubCodeViewer', 'GitHubCodeDiff', 'GitHubSectionRail',
    # SkillTeardown family — eyebrow is a scene-label/caption field, not a SlateCard prop
    'SkillTeardownAnatomy', 'SkillTeardownPipeline', 'SkillTeardownMechanism',
    'SkillTeardownAnatomy916', 'SkillTeardownPipeline916', 'SkillTeardownMechanism916',
    # CwcConceptCard family — eyebrow is a small SANS letterspaced label above the serif title
    # (design-system convention), not a SlateCard bold-display header
    'CwcModelQuestion', 'CwcParetoExplained', 'CwcSweepAccumulation',
    # madison-brand-guidebook bespoke scenes — kicker is a page-label/caption field
    'GuidebookPage',
    'MbgThreeFiles', 'MbgDeletePages', 'MbgClearSpace', 'MbgDonts',
    'MbgPaletteMorph', 'MbgTypePairing', 'MbgSocialCrops', 'MbgLiveFrames',
    'MbgRulesBend', 'MbgIdmlTree', 'MbgThreeSteps', 'MbgSixBrackets',
    # Diagram/traverse scenes — kicker is a scene-header caption, not a SlateCard field
    'FlowDiagram',
    'AiStackTraverse', 'SecurityBandLift',
    'StepStream',
})


def check_reel(reel_dir: Path):
    bs_path = reel_dir / 'beat_sheet.json'
    if not bs_path.exists():
        return 0, 0, []

    data = json.loads(bs_path.read_text())
    blockers, advisories = 0, 0
    messages = []

    for b in data.get('beats', []):
        bid = b.get('beat_id', '')
        is_bookend = bid in BOOKEND_IDS
        rem = b.get('shot', {}).get('remotion') or {}
        pattern = rem.get('pattern', '')
        props = rem.get('props', {})

        # BC-1: SlateCard (always banned regardless of beat position)
        if pattern == 'SlateCard':
            messages.append(
                f'  ✗ BC-1 BLOCKER — {bid}: SlateCard is banned '
                f'(bold display sans, eyebrow, GOLD rule, decorative circle); '
                f'replace with FormACard (lines=["{props.get("headline", "")[:40]}…"])'
            )
            blockers += 1
            continue  # don't also fire BC-3 for the eyebrow prop in SlateCard

        # BC-2: ClaudeWindow view='artifact' in body beats
        if pattern == 'ClaudeWindow' and props.get('view') == 'artifact' and not is_bookend:
            messages.append(
                f'  ✗ BC-2 BLOCKER — {bid}: ClaudeWindow view=artifact is a banned '
                f'card pattern for body beats; replace with FormACard'
            )
            blockers += 1

        # BC-3: Banned prop key names in card-type beats (eyebrow/kicker/headline).
        # Exempt patterns that legitimately use these names for non-card purposes
        # (scene captions, legacy unused props, custom exhibit labels).
        if pattern not in BC3_EXEMPT_PATTERNS:
            for key in BANNED_PROP_KEYS:
                if key in props and props[key]:
                    messages.append(
                        f'  ✗ BC-3 BLOCKER — {bid}: banned prop key "{key}" '
                        f'(eyebrow/kicker/headline are banned card-pattern field names; '
                        f'pattern={pattern!r})'
                    )
                    blockers += 1
                    break

        # BC-4: Old vox outro patterns in non-bookend positions
        if pattern in OLD_OUTRO_PATTERNS and not is_bookend:
            messages.append(
                f'  ✗ BC-4 BLOCKER — {bid}: {pattern} is an old vox outro pattern; '
                f'replace with ClaudeTitleOutro (BOUT) + ClaudeComposerAsk (BHTF) bookends'
            )
            blockers += 1

        # BA-5: Text truncation
        raw_fields = (
            list(props.get('artifactLines', []))
            + list(props.get('lines', []))
            + ([props['artifactHeading']] if props.get('artifactHeading') else [])
        )
        # CodeDiff lines are dicts {gutter, text, kind} — extract the text field
        all_text_fields = [
            item['text'] if isinstance(item, dict) else item
            for item in raw_fields
            if isinstance(item, (str, dict))
        ]
        for text in all_text_fields:
            stripped = text.rstrip()
            if any(stripped.endswith(s) for s in TRUNCATION_SUFFIXES):
                messages.append(
                    f'  ⚠ BA-5 advisory — {bid}: text ends with truncation marker: '
                    f'"{stripped[-50:]}"'
                )
                advisories += 1
                break

    return blockers, advisories, messages


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: banned_card_check.py <reel_dir>', file=sys.stderr)
        sys.exit(1)

    reel_dir = Path(sys.argv[1])
    slug = reel_dir.name
    blockers, advisories, messages = check_reel(reel_dir)

    for msg in messages:
        print(msg)

    if blockers:
        print(f'[banned-card] BLOCKED — {blockers} blocker(s) in {slug}')
        sys.exit(2)
    elif advisories:
        print(f'[banned-card] ADVISORY — {advisories} advisory(s) in {slug}')
        sys.exit(1)
    else:
        print(f'[banned-card] PASS — {slug}')
        sys.exit(0)
