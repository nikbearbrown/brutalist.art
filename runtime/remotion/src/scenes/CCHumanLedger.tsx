import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring } from 'remotion';
import { z } from 'zod';
import { CC, CC_FONT } from '../tokens/claudecode';
import { CCShell } from './CCShell';

/**
 * CCHumanLedger — the HUMAN beat of a cc-explainer: two columns filled from
 * the session just shown. THE AI: what it CAN / SHOULD do. THE HUMAN: what she
 * MUST / SHOULD do. The AI column lands first and the human column second and
 * holds — the order is the argument (Tier 4: the machine cannot report its own
 * uncertainty, so the metacognitive burden is hers). MUST rows carry the
 * terracotta rule. A closing line — what she would not delegate next time.
 *
 * Doctrine: skills/make/cc-explainer/reference/three-beats.md (Tier 4).
 */

// ── Schema ────────────────────────────────────────────────────────────────────

export const humanRowSchema = z.object({
  tier: z.enum(['MUST', 'SHOULD']),
  text: z.string().default('⚠ SET IN BEAT SHEET'),
});
export const aiRowSchema = z.object({
  tier: z.enum(['CAN', 'SHOULD']),
  text: z.string().default('⚠ SET IN BEAT SHEET'),
});

export const ccHumanLedgerSchema = z.object({
  human:   z.array(humanRowSchema).min(1).max(6).default([]),
  ai:      z.array(aiRowSchema).min(1).max(6).default([]),
  /** ≤ 14 words — what she would not delegate next time. */
  closing: z.string().optional(),
  /** Frame at which the human column starts landing (AI column starts at 0). */
  humanCue: z.number().int().default(60),
  /** Frames between rows within a column. */
  rowGap:   z.number().int().default(10),
});
export type CCHumanLedgerProps = z.infer<typeof ccHumanLedgerSchema>;

// ── Helpers ───────────────────────────────────────────────────────────────────

const clamp = (v: number, a: number, b: number) => Math.min(b, Math.max(a, v));
const SPRING = { damping: 24, stiffness: 140, mass: 0.9 };

// ── Component ─────────────────────────────────────────────────────────────────

export const CCHumanLedger: React.FC<CCHumanLedgerProps> = ({ human, ai, closing, humanCue, rowGap }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const headIn  = clamp(spring({ frame, fps, config: SPRING }), 0, 1);
  const closeCue = humanCue + human.length * rowGap + 30;
  const closeIn  = clamp(spring({ frame: frame - closeCue, fps, config: SPRING }), 0, 1);

  const COL_TOP = 80;
  const ROW_H   = 100;
  const GUTTER  = 40;

  const column = (
    side: 'ai' | 'human',
    header: string,
    headerColor: string,
    rows: { tier: string; text: string }[],
    startCue: number,
  ) => (
    <div style={{ flex: 1, minWidth: 0, position: 'relative' }}>
      <div style={{
        fontFamily: CC_FONT.mono, fontSize: 30, letterSpacing: '0.18em', color: headerColor,
        borderBottom: `1.5px solid ${CC.BORDER}`, paddingBottom: 12, opacity: headIn,
      }}>{header}</div>
      {rows.map((r, i) => {
        const rowIn = clamp(spring({ frame: frame - (startCue + i * rowGap), fps, config: SPRING }), 0, 1);
        const must = r.tier === 'MUST';
        return (
          <div key={i} style={{
            position: 'absolute', left: 0, right: 0, top: COL_TOP + i * ROW_H, height: ROW_H - 10,
            display: 'flex', alignItems: 'center', gap: 16,
            paddingLeft: 14,
            borderLeft: `5px solid ${must ? CC.SPARK : 'transparent'}`,
            borderBottom: `1px solid ${CC.BORDER}`,
            opacity: rowIn, transform: `translateY(${(1 - rowIn) * 8}px)`,
          }}>
            <span style={{
              width: 118, flexShrink: 0, fontFamily: CC_FONT.mono, fontSize: 30, letterSpacing: '0.1em', fontWeight: 700,
              color: must ? CC.SPARK : side === 'human' ? CC.VIOLET : CC.INK_2,
            }}>{r.tier}</span>
            <span style={{
              fontFamily: CC_FONT.ui, fontSize: 40, color: CC.INK, lineHeight: 1.18,
              whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis',
            }}>{r.text}</span>
          </div>
        );
      })}
    </div>
  );

  return (
    <AbsoluteFill>
      <CCShell title="claude-code" mode="default">
        <div style={{ position: 'absolute', left: 16, right: 16, top: 12, bottom: 0, display: 'flex', gap: GUTTER }}>
          {column('ai', 'THE AI', CC.INK_2, ai, 8)}
          {column('human', 'THE HUMAN', CC.SPARK, human, humanCue)}
        </div>
        {closing ? (
          <div style={{
            position: 'absolute', left: 16, right: 16, bottom: 18,
            display: 'flex', alignItems: 'baseline', gap: 16,
            opacity: closeIn, transform: `translateY(${(1 - closeIn) * 8}px)`,
          }}>
            <span style={{ fontFamily: CC_FONT.mono, fontSize: 44, color: CC.SPARK }}>✳</span>
            <span style={{ fontFamily: CC_FONT.ui, fontSize: 44, color: CC.INK, fontWeight: 700, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{closing}</span>
          </div>
        ) : null}
      </CCShell>
    </AbsoluteFill>
  );
};

// ── defaultProps ──────────────────────────────────────────────────────────────

export const ccHumanLedgerDefaultProps: CCHumanLedgerProps = ccHumanLedgerSchema.parse({});

// ── Demo twin ─────────────────────────────────────────────────────────────────

export const ccHumanLedgerDemoSchema = ccHumanLedgerSchema;
export type CCHumanLedgerDemoProps   = CCHumanLedgerProps;

export const CCHumanLedgerDemo: React.FC<CCHumanLedgerDemoProps> = (props) => (
  <CCHumanLedger {...props} />
);

export const ccHumanLedgerDemoDefaultProps: CCHumanLedgerDemoProps = ccHumanLedgerDemoSchema.parse({
  ai: [
    { tier: 'CAN',    text: 'write the whole file in one pass' },
    { tier: 'CAN',    text: 'wire the form, the list, the storage' },
    { tier: 'SHOULD', text: 'say what it added that I did not ask for' },
  ],
  human: [
    { tier: 'MUST',   text: 'decide what done means — one file, no requests out' },
    { tier: 'MUST',   text: 'read it before I run it' },
    { tier: 'MUST',   text: 'catch the confident extra — it sounded as sure about that as the rest' },
    { tier: 'SHOULD', text: 'name the failure before I look for it' },
  ],
  closing: 'Next time I keep the constraints list. Five lines. Mine.',
});
