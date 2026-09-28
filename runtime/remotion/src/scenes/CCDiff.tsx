import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate } from 'remotion';
import { z } from 'zod';
import { CC, CC_FONT } from '../tokens/claudecode';
import { AnchorContext } from './CursorLayer';
import { CCShell, CC_BODY } from './CCShell';
import { diffLineSchema } from './GitHubCodeDiff';

/**
 * CCDiff — inline diff view. Imports diffLineSchema from GitHubCodeDiff.
 * Full-width add/del bands with gutter numbers, staggered line reveal.
 */

// ── Schema ────────────────────────────────────────────────────────────────────

export const ccDiffSchema = z.object({
  file:     z.string().default('⚠ SET IN BEAT SHEET'),
  addCount: z.number().int().default(0),
  delCount: z.number().int().default(0),
  lines:    z.array(diffLineSchema).default([]),
});
export type CCDiffProps = z.infer<typeof ccDiffSchema>;

const clamp = (v: number, a: number, b: number) => Math.min(b, Math.max(a, v));

const HEADER_TOP  = 20;   // relative to body
const HEADER_H    = 56;
const SUMMARY_H   = 48;
const GAP         = 16;
const LINE_H      = 52;
const GUTTER_W    = 60;

// ── Component ─────────────────────────────────────────────────────────────────

export const CCDiff: React.FC<CCDiffProps> = ({ file, addCount, delCount, lines }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const ctx = React.useContext(AnchorContext);

  // Register anchor at header center
  const headerCY = CC_BODY.Y + HEADER_TOP + HEADER_H / 2;
  ctx.register('cc.diff.header', CC_BODY.X + CC_BODY.W / 2, headerCY);

  return (
    <CCShell title="claude-code" mode="default">
      {/* ── Header: Update(file) ───────────────────────────────────────── */}
      <div style={{
        position: 'absolute',
        left: 20,
        top: HEADER_TOP,
        right: 20,
        height: HEADER_H,
        display: 'flex',
        alignItems: 'center',
        fontFamily: CC_FONT.mono,
        fontSize: 52,
        color: CC.INK,
      }}>
        <span style={{ fontWeight: 700 }}>Update</span>
        <span>(</span>
        <span style={{ color: CC.VIOLET }}>{file}</span>
        <span>)</span>
      </div>

      {/* ── Summary line ──────────────────────────────────────────────── */}
      <div style={{
        position: 'absolute',
        left: 20,
        top: HEADER_TOP + HEADER_H,
        right: 20,
        height: SUMMARY_H,
        display: 'flex',
        alignItems: 'center',
        fontFamily: CC_FONT.mono,
        fontSize: 44,
        color: CC.INK_2,
      }}>
        <span style={{ color: CC.ADD_FG }}>+{addCount} added</span>
        <span style={{ margin: '0 12px', color: CC.INK_3 }}>·</span>
        <span style={{ color: CC.DEL_FG }}>{delCount} removed</span>
      </div>

      {/* ── Diff lines ────────────────────────────────────────────────── */}
      {lines.map((line, i) => {
        const lineTop = HEADER_TOP + HEADER_H + SUMMARY_H + GAP + i * LINE_H;

        // Stagger reveal
        const revealStart = fps * 0.2 + i * 5;
        const revealEnd   = revealStart + 8;
        const opacity = interpolate(frame, [revealStart, revealEnd], [0, 1], {
          extrapolateLeft:  'clamp',
          extrapolateRight: 'clamp',
        });

        const bg =
          line.kind === 'add' ? CC.ADD_BG :
          line.kind === 'del' ? CC.DEL_BG :
          'transparent';

        const textColor =
          line.kind === 'add' ? CC.ADD_FG :
          line.kind === 'del' ? CC.DEL_FG :
          CC.INK;

        const gutterColor =
          line.kind === 'add' ? CC.ADD_FG :
          line.kind === 'del' ? CC.DEL_FG :
          CC.INK_3;

        return (
          <div key={i} style={{
            position: 'absolute',
            left: 0,
            right: 0,
            top: lineTop,
            height: LINE_H,
            background: bg,
            display: 'flex',
            alignItems: 'center',
            opacity,
          }}>
            {/* Gutter */}
            <div style={{
              width: GUTTER_W,
              flexShrink: 0,
              textAlign: 'center',
              fontFamily: CC_FONT.mono,
              fontSize: 44,
              color: gutterColor,
              userSelect: 'none',
            }}>
              {line.gutter}
            </div>
            {/* Text */}
            <div style={{
              flex: 1,
              fontFamily: CC_FONT.mono,
              fontSize: 48,
              color: textColor,
              whiteSpace: 'pre',
              overflow: 'hidden',
              paddingLeft: 8,
            }}>
              {line.text}
            </div>
          </div>
        );
      })}
    </CCShell>
  );
};

// ── defaultProps ──────────────────────────────────────────────────────────────

export const ccDiffDefaultProps: CCDiffProps = ccDiffSchema.parse({});

// ── Demo ──────────────────────────────────────────────────────────────────────

export const ccDiffDemoSchema = ccDiffSchema;
export type CCDiffDemoProps = CCDiffProps;

export const CCDiffDemo: React.FC<CCDiffDemoProps> = (props) => {
  return <CCDiff {...props} />;
};

export const ccDiffDemoDefaultProps: CCDiffDemoProps = ccDiffDemoSchema.parse({
  file:     'src/scenes/CCShell.tsx',
  addCount: 4,
  delCount: 1,
  lines: [
    { gutter: '1',  text: "import React from 'react';",                       kind: 'context' },
    { gutter: '2',  text: "import { AbsoluteFill } from 'remotion';",         kind: 'context' },
    { gutter: '-',  text: "import { CC } from '../tokens/claude';",           kind: 'del'     },
    { gutter: '+',  text: "import { CC, CC_FONT } from '../tokens/claudecode';", kind: 'add'  },
    { gutter: '+',  text: "import { AnchorContext } from './CursorLayer';",   kind: 'add'     },
    { gutter: '+',  text: "export const CCShell: React.FC<CCShellProps> = (", kind: 'add'     },
    { gutter: '+',  text: "  props) => {",                                     kind: 'add'     },
    { gutter: '8',  text: "  const { title, mode = 'default' } = props;",    kind: 'context' },
  ],
});
