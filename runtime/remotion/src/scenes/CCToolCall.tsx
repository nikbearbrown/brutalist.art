import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring } from 'remotion';
import { z } from 'zod';
import { CC, CC_FONT } from '../tokens/claudecode';
import { AnchorContext } from './CursorLayer';
import { CCShell, CC_BODY } from './CCShell';

/**
 * CCToolCall — tool call block. Braille spinner → green ✓ on done. Bold
 * name(arg), nested children, '+N more' and 'ctrl+b' hints with violet
 * keybinding styling.
 */

// ── Braille spinner frames ────────────────────────────────────────────────────

const BRAILLE = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'];

// ── Schema ────────────────────────────────────────────────────────────────────

const childSchema = z.object({
  name: z.string(),
  arg:  z.string().optional(),
});

export const ccToolCallSchema = z.object({
  name:           z.string().default('⚠ SET IN BEAT SHEET'),
  arg:            z.string().optional(),
  state:          z.enum(['running', 'done']).default('running'),
  children:       z.array(childSchema).optional(),
  moreCount:      z.number().int().optional(),
  backgroundHint: z.boolean().default(false),
});
export type CCToolCallProps = z.infer<typeof ccToolCallSchema>;

const clamp = (v: number, a: number, b: number) => Math.min(b, Math.max(a, v));
const SPRING_CFG = { damping: 26, stiffness: 120, mass: 0.9 };

const BLOCK_TOP = CC_BODY.Y + 40;
const INDENT_PX = 40;
const ROW_H = 60;

// ── Inline keybinding renderer ────────────────────────────────────────────────

function renderWithBinding(text: string, bindings: string[]): React.ReactNode {
  const pattern = new RegExp(`(${bindings.map(b => b.replace(/[+/]/g, '\\$&')).join('|')})`, 'g');
  const parts = text.split(pattern);
  return parts.map((part, i) => (
    <span key={i} style={{ color: bindings.includes(part) ? CC.VIOLET : 'inherit', whiteSpace: 'pre' }}>
      {part}
    </span>
  ));
}

// ── Component ─────────────────────────────────────────────────────────────────

export const CCToolCall: React.FC<CCToolCallProps> = ({
  name, arg, state, children, moreCount, backgroundHint,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const ctx = React.useContext(AnchorContext);

  const isDone = state === 'done';

  // Spring from 0→1 when done, stays 0 when running
  const doneSpring = isDone
    ? spring({ frame, fps, config: SPRING_CFG })
    : 0;
  const clamped = clamp(doneSpring, 0, 1);

  // Braille spinner index
  const spinnerIdx = Math.floor(frame / 3) % BRAILLE.length;
  const spinnerGlyph = BRAILLE[spinnerIdx];

  // Register anchor at header row
  const headerCY = BLOCK_TOP + 34;
  ctx.register('cc.tool.header', CC_BODY.X + CC_BODY.W / 2, headerCY);

  const argStr = arg ? `(${arg})` : '()';

  return (
    <CCShell title="claude-code" mode="default">
      {/* ── Header row ───────────────────────────────────────────────────── */}
      <div style={{
        position: 'absolute',
        left: CC_BODY.X - 140,  // offset relative to body inside window
        top: BLOCK_TOP - 120,   // offset inside body (body starts at TB_H=50)
        display: 'flex',
        alignItems: 'center',
        gap: 16,
        height: 68,
      }}>
        {/* Spinner / checkmark */}
        <span style={{
          fontFamily: CC_FONT.mono,
          fontSize: 52,
          color: isDone ? CC.DONE : CC.SPARK,
          opacity: isDone ? clamped : 1,
          transform: isDone ? `scale(${0.6 + 0.4 * clamped})` : 'scale(1)',
          display: 'inline-block',
          width: 52,
          textAlign: 'center',
          lineHeight: 1,
        }}>
          {isDone ? '✓' : spinnerGlyph}
        </span>
        {/* name(arg) */}
        <span style={{
          fontFamily: CC_FONT.mono,
          fontSize: 52,
          color: CC.INK,
          fontWeight: 700,
          lineHeight: 1,
        }}>
          {name}
        </span>
        <span style={{
          fontFamily: CC_FONT.mono,
          fontSize: 52,
          color: CC.INK_2,
          lineHeight: 1,
        }}>
          {argStr}
        </span>
      </div>

      {/* ── Children ─────────────────────────────────────────────────────── */}
      {(children ?? []).map((child, i) => {
        const childArg = child.arg ? `(${child.arg})` : '()';
        return (
          <div key={i} style={{
            position: 'absolute',
            left: CC_BODY.X - 140 + INDENT_PX,
            top: BLOCK_TOP - 120 + 68 + i * ROW_H,
            display: 'flex',
            alignItems: 'center',
            gap: 12,
            height: ROW_H,
          }}>
            {/* tree connector */}
            <div style={{
              width: 1,
              height: ROW_H,
              background: CC.BORDER,
              position: 'absolute',
              left: -20,
              top: 0,
            }} />
            <span style={{
              fontFamily: CC_FONT.mono,
              fontSize: 44,
              color: CC.INK_2,
              lineHeight: 1,
            }}>
              {child.name}
            </span>
            <span style={{
              fontFamily: CC_FONT.mono,
              fontSize: 44,
              color: CC.INK_3,
              lineHeight: 1,
            }}>
              {childArg}
            </span>
          </div>
        );
      })}

      {/* ── +N more line ─────────────────────────────────────────────────── */}
      {moreCount != null && moreCount > 0 && (
        <div style={{
          position: 'absolute',
          left: CC_BODY.X - 140 + INDENT_PX,
          top: BLOCK_TOP - 120 + 68 + (children?.length ?? 0) * ROW_H,
          height: 56,
          display: 'flex',
          alignItems: 'center',
          fontFamily: CC_FONT.mono,
          fontSize: 44,
          color: CC.INK_3,
        }}>
          {renderWithBinding(
            `+${moreCount} more tool uses (ctrl+o to expand)`,
            ['ctrl+o'],
          )}
        </div>
      )}

      {/* ── ctrl+b background hint ───────────────────────────────────────── */}
      {backgroundHint && (
        <div style={{
          position: 'absolute',
          left: CC_BODY.X - 140 + INDENT_PX,
          top: BLOCK_TOP - 120 + 68
            + (children?.length ?? 0) * ROW_H
            + (moreCount != null && moreCount > 0 ? 56 : 0),
          height: 56,
          display: 'flex',
          alignItems: 'center',
          fontFamily: CC_FONT.mono,
          fontSize: 44,
          color: CC.INK_3,
        }}>
          {renderWithBinding('ctrl+b to run in background', ['ctrl+b'])}
        </div>
      )}
    </CCShell>
  );
};

// ── defaultProps ──────────────────────────────────────────────────────────────

export const ccToolCallDefaultProps: CCToolCallProps = ccToolCallSchema.parse({});

// ── Demo ──────────────────────────────────────────────────────────────────────

export const ccToolCallDemoSchema = ccToolCallSchema;
export type CCToolCallDemoProps = CCToolCallProps;

export const CCToolCallDemo: React.FC<CCToolCallDemoProps> = (props) => {
  return <CCToolCall {...props} />;
};

export const ccToolCallDemoDefaultProps: CCToolCallDemoProps = ccToolCallDemoSchema.parse({
  name:           'Explore',
  arg:            'src/scenes/',
  state:          'done',
  children:       [
    { name: 'Read', arg: 'CCShell.tsx'   },
    { name: 'Read', arg: 'CCSession.tsx' },
  ],
  moreCount:      3,
  backgroundHint: true,
});
