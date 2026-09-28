import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion';
import { z } from 'zod';
import { CCWebHome } from './CCWebHome';
import { CCThemePicker } from './CCThemePicker';
import { CCSession } from './CCSession';
import { CCStatusVerb } from './CCStatusVerb';

/**
 * CCWalkthroughDemo — 4-shot walkthrough of the Claude Code kit, with Clawd
 * threaded through every shot. Sibling of CoworkWalkthroughDemo.
 *
 * Shots (30 fps):
 *   S1   0–69   CCWebHome — dotted canvas, idle Clawd, repo pills, suggestions
 *   S2  70–139  CCThemePicker — theme list + diff preview, Clawd + flowers strip
 *   S3 140–299  CCSession — prompt types, status verb, tool tree, live diff;
 *               mascot 'auto': Clawd looks → thinks → types in the corner
 *   S4 300–359  CCStatusVerb — Pontificating outro, Clawd celebrates
 *
 * Total: 360 frames (12 s at 30 fps). Every shot is props-driven — no pixel is
 * hand-rendered, no frame is a screen recording (the kit's whole argument).
 */

export const ccWalkthroughDemoSchema = z.object({});
export type CCWalkthroughDemoProps = z.infer<typeof ccWalkthroughDemoSchema>;

// Frame boundaries for each shot
const S = { S1: 0, S2: 70, S3: 140, S4: 300, END: 360 };

function shotAlpha(frame: number, start: number, end: number, fadeLen = 8): number {
  const inAlpha  = Math.min(1, Math.max(0, interpolate(frame, [start, start + fadeLen], [0, 1], { extrapolateRight: 'clamp' })));
  const outAlpha = end ? Math.min(1, Math.max(0, interpolate(frame, [end - fadeLen, end], [1, 0], { extrapolateRight: 'clamp' }))) : 1;
  return Math.min(inAlpha, outAlpha);
}

export const CCWalkthroughDemo: React.FC<CCWalkthroughDemoProps> = () => {
  const frame = useCurrentFrame();

  const showS1 = frame < S.S2 + 8;
  const showS2 = frame >= S.S2 - 4 && frame < S.S3 + 8;
  const showS3 = frame >= S.S3 - 4 && frame < S.S4 + 8;
  const showS4 = frame >= S.S4 - 4;

  return (
    <AbsoluteFill>

      {/* ── S1: Web home — idle Clawd on the dotted canvas ─────────────── */}
      {showS1 ? (
        <AbsoluteFill style={{ opacity: shotAlpha(frame, S.S1, S.S2) }}>
          <CCWebHome
            repoLabel="anthropics/claude-code"
            branchLabel="main"
            suggestions={[
              { icon: '◆', label: 'Write a CLAUDE.md',       preview: 'Create or update my CLAUDE.md file' },
              { icon: '◆', label: 'Explain this codebase',   preview: 'src/ · index.ts · utils/'           },
              { icon: '◆', label: 'Review recent changes',   preview: 'git log · 3 commits'                },
            ]}
          />
        </AbsoluteFill>
      ) : null}

      {/* ── S2: Theme picker — Clawd + pixel flowers, live diff preview ── */}
      {showS2 ? (
        <AbsoluteFill style={{ opacity: shotAlpha(frame, S.S2, S.S3) }}>
          <CCThemePicker
            title="claude-code"
            hint="Choose the text style that looks best with your terminal"
            options={[
              { label: 'Dark mode',                      current: true,  selected: false },
              { label: 'Light mode',                     current: false, selected: true  },
              { label: 'Dark mode (colorblind-friendly)', current: false, selected: false },
              { label: 'Light mode (colorblind-friendly)', current: false, selected: false },
              { label: 'Dark mode (ANSI colors only)',    current: false, selected: false },
            ]}
            preview={[
              { gutter: '1', text: 'function greet() {',                kind: 'context' },
              { gutter: '-', text: '  console.log("Hello, World!");',  kind: 'del'     },
              { gutter: '+', text: '  console.log("Hello, Claude!");', kind: 'add'     },
              { gutter: '3', text: '}',                                kind: 'context' },
            ]}
          />
        </AbsoluteFill>
      ) : null}

      {/* ── S3: Live session — mascot 'auto' tracks the block stream ───── */}
      {showS3 ? (
        <AbsoluteFill style={{ opacity: shotAlpha(frame, S.S3, S.S4) }}>
          <CCSession
            title="webp-avatar-conversion"
            mode="accept-edits"
            mascot="auto"
            blocks={[
              {
                type: 'prompt',
                text: 'add webp conversion to our image upload pipeline',
                cue:  S.S3,
                typeDuration: 40,
              },
              {
                type:    'status',
                verb:    'Spelunking',
                elapsed: '0m 12s',
                tokens:  '1.2k tokens',
              },
              {
                type:     'tool',
                name:     'Explore',
                arg:      'image upload pipeline',
                state:    'done',
                children: [
                  { name: 'Bash', arg: 'ls -la src/middleware/'  },
                  { name: 'Read', arg: 'errorHandler.ts'         },
                ],
                moreCount: 13,
                backgroundHint: true,
              },
              {
                type:     'diff',
                file:     'tsconfig.json',
                addCount: 2,
                delCount: 1,
                lines: [
                  { gutter: '10', text: '  "types": ["node"]',    kind: 'context' },
                  { gutter: '-',  text: '}',                      kind: 'del'     },
                  { gutter: '+',  text: '},',                     kind: 'add'     },
                  { gutter: '+',  text: '"exclude": ["web"]',     kind: 'add'     },
                ],
              },
            ]}
            cues={[S.S3, S.S3 + 45, S.S3 + 70, S.S3 + 110]}
          />
        </AbsoluteFill>
      ) : null}

      {/* ── S4: Status outro — Clawd celebrates the run ────────────────── */}
      {showS4 ? (
        <AbsoluteFill style={{ opacity: shotAlpha(frame, S.S4, S.END) }}>
          <CCStatusVerb
            verb="Pontificating"
            elapsed="1m 46s"
            tokens="5.0k tokens"
            mascot="celebrate"
          />
        </AbsoluteFill>
      ) : null}

    </AbsoluteFill>
  );
};
