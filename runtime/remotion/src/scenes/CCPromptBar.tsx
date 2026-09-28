import React from 'react';
import { AbsoluteFill, useCurrentFrame } from 'remotion';
import { z } from 'zod';
import { CC, CC_FONT } from '../tokens/claudecode';
import { AnchorContext } from './CursorLayer';
import { CCShell, CC_BODY } from './CCShell';

/**
 * CCPromptBar — user prompt band. Reverse-video (CC.PROMPT_BG) with '> '
 * prefix in violet. Karaoke type-on derived from
 * charRate = text.length / typeDuration.
 */

// ── Schema ────────────────────────────────────────────────────────────────────

export const ccPromptBarSchema = z.object({
  text:         z.string().default('⚠ SET IN BEAT SHEET'),
  cue:          z.number().int().default(0),
  typeDuration: z.number().int().default(60),
});
export type CCPromptBarProps = z.infer<typeof ccPromptBarSchema>;

const clamp = (v: number, a: number, b: number) => Math.min(b, Math.max(a, v));

const BAND_H = 72;
const BAND_TOP = CC_BODY.Y + 40; // relative to the AbsoluteFill canvas

// ── Component ─────────────────────────────────────────────────────────────────

export const CCPromptBar: React.FC<CCPromptBarProps> = ({ text, cue, typeDuration }) => {
  const frame = useCurrentFrame();
  const ctx   = React.useContext(AnchorContext);

  const localFrame = frame - cue;
  const charRate = text.length / Math.max(1, typeDuration);
  const charsVisible = localFrame < 0 ? 0 : Math.min(text.length, Math.floor(localFrame * charRate));
  const isTyping = charsVisible < text.length;
  const visibleText = text.slice(0, charsVisible);

  // Blinking cursor — 2px wide × 38px tall, toggles every 8 frames
  const cursorVisible = isTyping && Math.floor(frame / 8) % 2 === 0;

  // Register anchor at center of the band
  const bandCenterX = CC_BODY.X + CC_BODY.W / 2;
  const bandCenterY = BAND_TOP + BAND_H / 2;
  ctx.register('cc.prompt', bandCenterX, bandCenterY);

  return (
    <CCShell title="claude-code" mode="default">
      {/* Prompt band — full body width */}
      <div style={{
        position: 'absolute',
        left: 0,
        top: BAND_TOP - (72 + 70),  // offset inside body (body starts at TB_H=50, BAND_TOP is canvas-relative)
        right: 0,
        height: BAND_H,
        background: CC.PROMPT_BG,
        display: 'flex',
        alignItems: 'center',
        paddingLeft: 20,
        paddingRight: 20,
        boxSizing: 'border-box',
        borderTop:    `1px solid ${CC.BORDER}`,
        borderBottom: `1px solid ${CC.BORDER}`,
      }}>
        {/* "> " prefix */}
        <span style={{
          fontFamily: CC_FONT.mono,
          fontSize: 52,
          color: CC.VIOLET,
          marginRight: 12,
          flexShrink: 0,
          lineHeight: 1,
        }}>
          &gt;&nbsp;
        </span>
        {/* Typed text */}
        <span style={{
          fontFamily: CC_FONT.mono,
          fontSize: 52,
          color: CC.INK,
          lineHeight: 1,
          flex: 1,
        }}>
          {visibleText}
          {/* Blinking cursor */}
          {cursorVisible && (
            <span style={{
              display: 'inline-block',
              width: 2,
              height: 38,
              background: CC.VIOLET,
              verticalAlign: 'middle',
              marginLeft: 2,
            }} />
          )}
        </span>
      </div>
    </CCShell>
  );
};

// ── defaultProps ──────────────────────────────────────────────────────────────

export const ccPromptBarDefaultProps: CCPromptBarProps = ccPromptBarSchema.parse({});

// ── Demo ──────────────────────────────────────────────────────────────────────

export const ccPromptBarDemoSchema = ccPromptBarSchema;
export type CCPromptBarDemoProps = CCPromptBarProps;

export const CCPromptBarDemo: React.FC<CCPromptBarDemoProps> = (props) => {
  return <CCPromptBar {...props} />;
};

export const ccPromptBarDemoDefaultProps: CCPromptBarDemoProps = ccPromptBarDemoSchema.parse({
  text: 'Pull the Q3 budget reports from Drive and flag anything over 80% of limit',
  cue: 20,
  typeDuration: 80,
});
