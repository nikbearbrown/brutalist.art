import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from 'remotion';
import { z } from 'zod';
import { CC, CC_FONT } from '../tokens/claudecode';
import { AnchorContext } from './CursorLayer';
import { CCShell, CC_BODY } from './CCShell';
import { MascotSVG, computeAnimation, ANIMATIONS } from './ClaudeMascotScene';

/**
 * CCStatusVerb — animated status line. Pulsing ✳ spark, animated ellipsis,
 * elapsed time and token count. Uses VERBS from claudecode tokens.
 * Optional `mascot` renders an animated Clawd on the right ('think' pairs well).
 */

// ── Schema ────────────────────────────────────────────────────────────────────

export const ccStatusVerbSchema = z.object({
  verb:    z.string().default('⚠ SET IN BEAT SHEET'),
  elapsed: z.string().optional(),
  tokens:  z.string().optional(),
  mascot:  z.enum(ANIMATIONS).optional(),
});
export type CCStatusVerbProps = z.infer<typeof ccStatusVerbSchema>;

const clamp = (v: number, a: number, b: number) => Math.min(b, Math.max(a, v));

// ── Component ─────────────────────────────────────────────────────────────────

export const CCStatusVerb: React.FC<CCStatusVerbProps> = ({ verb, elapsed, tokens, mascot }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const ctx   = React.useContext(AnchorContext);

  // Pulsing spark: scale = 1 + 0.12 * sin(frame * 0.2)
  const sparkScale = 1 + 0.12 * Math.sin(frame * 0.2);

  // Animated ellipsis: 1, 2, or 3 dots, cycling every 10 frames
  const dotCount  = (Math.floor(frame / 10) % 3) + 1;
  const ellipsis  = '.'.repeat(dotCount);

  // Register anchor at center of the verb line (vertically centered in body)
  const verbCX = CC_BODY.X + CC_BODY.W / 2;
  const verbCY = CC_BODY.Y + CC_BODY.H / 2;
  ctx.register('cc.status', verbCX, verbCY);

  // Build metadata string
  const metaParts: string[] = [];
  if (elapsed) metaParts.push(elapsed);
  if (tokens)  metaParts.push(`↓ ${tokens}`);
  const meta = metaParts.join(' · ');

  return (
    <CCShell title="claude-code" mode="default">
      {/* Vertically centered in the body */}
      <div style={{
        position: 'absolute',
        left: 20,
        right: 20,
        top: 0,
        bottom: 0,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'flex-start',
        justifyContent: 'center',
        gap: 16,
      }}>
        {/* Main status row */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: 14,
          fontFamily: CC_FONT.mono,
          fontSize: 58,
          lineHeight: 1,
        }}>
          {/* Pulsing spark ✳ */}
          <span style={{
            color: CC.SPARK,
            fontSize: 58,
            display: 'inline-block',
            transform: `scale(${sparkScale})`,
            transformOrigin: 'center center',
            lineHeight: 1,
          }}>
            ✳
          </span>
          {/* Verb */}
          <span style={{
            color: CC.INK,
            fontWeight: 700,
            fontSize: 58,
          }}>
            {verb}
          </span>
          {/* Animated ellipsis */}
          <span style={{
            color: CC.INK_2,
            fontSize: 58,
            minWidth: 48,
          }}>
            {ellipsis}
          </span>
        </div>

        {/* Elapsed + tokens metadata */}
        {meta.length > 0 && (
          <div style={{
            fontFamily: CC_FONT.mono,
            fontSize: 48,
            color: CC.INK_3,
            paddingLeft: 72, // indent to align with verb text (spark+gap)
          }}>
            {meta}
          </div>
        )}
      </div>

      {/* ── Clawd (prop-gated) — right of the status column ─────────────── */}
      {mascot && (
        <div style={{
          position: 'absolute',
          right: 80,
          top: '50%',
          transform: 'translateY(-50%)',
          width: 380,
          height: 240,
          pointerEvents: 'none',
        }}>
          <MascotSVG s={computeAnimation(mascot, frame, fps)} scale={1} />
        </div>
      )}
    </CCShell>
  );
};

// ── defaultProps ──────────────────────────────────────────────────────────────

export const ccStatusVerbDefaultProps: CCStatusVerbProps = ccStatusVerbSchema.parse({});

// ── Demo ──────────────────────────────────────────────────────────────────────

export const ccStatusVerbDemoSchema = ccStatusVerbSchema;
export type CCStatusVerbDemoProps = CCStatusVerbProps;

export const CCStatusVerbDemo: React.FC<CCStatusVerbDemoProps> = (props) => {
  return <CCStatusVerb {...props} />;
};

export const ccStatusVerbDemoDefaultProps: CCStatusVerbDemoProps = ccStatusVerbDemoSchema.parse({
  verb:    'Pontificating',
  elapsed: '1m 46s',
  tokens:  '5.0k tokens',
  mascot:  'think',
});
