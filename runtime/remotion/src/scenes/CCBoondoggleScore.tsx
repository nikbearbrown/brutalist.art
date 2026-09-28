import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring } from 'remotion';
import { z } from 'zod';
import { CC, CC_FONT } from '../tokens/claudecode';
import { CCShell } from './CCShell';

/**
 * CCBoondoggleScore — the CONDUCT beat of a cc-explainer: Gru's Boondoggle
 * Score for the session just shown. Steps land in dependency order; each is
 * CLAUDE (with the prompt that drove it and the handoff condition that had to
 * be true before the next step) or HUMAN (with the supervisory capacity
 * exercised — PA / PF / TO / IJ / EI). One step may be ringed as the
 * dangerous middle. A capacity tally lands last; zero counts are named.
 *
 * Doctrine: skills/make/cc-explainer/reference/three-beats.md (Gru).
 */

// ── Schema ────────────────────────────────────────────────────────────────────

export const CAPACITIES = ['PA', 'PF', 'TO', 'IJ', 'EI'] as const;
export const CAPACITY_NAMES: Record<typeof CAPACITIES[number], string> = {
  PA: 'plausibility auditing', PF: 'problem formulation', TO: 'tool orchestration',
  IJ: 'interpretive judgment', EI: 'executive integration',
};

export const boondoggleStepSchema = z.object({
  n:         z.number().int(),
  phase:     z.enum(['F', 'C', 'I', 'B', 'H', 'R']).default('C'),
  labor:     z.enum(['claude', 'human']),
  /** The prompt (claude) or the action (human). */
  text:      z.string().default('⚠ SET IN BEAT SHEET'),
  /** Human steps only. */
  capacity:  z.enum(CAPACITIES).optional(),
  /** Claude steps only — testable, ≤ 20 words. */
  handoff:   z.string().optional(),
  dependsOn: z.array(z.number().int()).optional(),
});
export type BoondoggleStep = z.infer<typeof boondoggleStepSchema>;

export const ccBoondoggleScoreSchema = z.object({
  system:          z.string().default('⚠ SET IN BEAT SHEET'),
  steps:           z.array(boondoggleStepSchema).min(1).max(7).default([]),
  /** Step number to ring in terracotta as the dangerous middle. */
  dangerousMiddle: z.number().int().optional(),
  /** Show the capacity tally after the last step. */
  distribution:    z.boolean().default(true),
  /** Frames between step landings. */
  stepGap:         z.number().int().default(18),
});
export type CCBoondoggleScoreProps = z.infer<typeof ccBoondoggleScoreSchema>;

// ── Helpers ───────────────────────────────────────────────────────────────────

const clamp = (v: number, a: number, b: number) => Math.min(b, Math.max(a, v));
const SPRING = { damping: 24, stiffness: 140, mass: 0.9 };

// ── Component ─────────────────────────────────────────────────────────────────

export const CCBoondoggleScore: React.FC<CCBoondoggleScoreProps> = ({
  system, steps, dangerousMiddle, distribution, stepGap,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const headIn = clamp(spring({ frame, fps, config: SPRING }), 0, 1);
  const nClaude = steps.filter((s) => s.labor === 'claude').length;
  const nHuman  = steps.length - nClaude;
  const tally: Record<string, number> = { PA: 0, PF: 0, TO: 0, IJ: 0, EI: 0 };
  steps.forEach((s) => { if (s.capacity) tally[s.capacity] += 1; });

  const HEAD_H = 88;
  const rowsTop = HEAD_H + 6;
  const rowsBottom = distribution ? 836 - 90 : 836 - 12;
  const rowH = Math.min(112, Math.floor((rowsBottom - rowsTop) / Math.max(1, steps.length)));
  const tallyCue = 12 + steps.length * stepGap + 10;
  const tallyIn  = clamp(spring({ frame: frame - tallyCue, fps, config: SPRING }), 0, 1);

  return (
    <AbsoluteFill>
      <CCShell title="claude-code" mode="default">
        <div style={{ position: 'absolute', left: 16, right: 16, top: 12, bottom: 0 }}>

          {/* Header */}
          <div style={{
            display: 'flex', alignItems: 'baseline', justifyContent: 'space-between',
            borderBottom: `1.5px solid ${CC.BORDER}`, paddingBottom: 12, opacity: headIn,
          }}>
            <div style={{ display: 'flex', alignItems: 'baseline', gap: 18 }}>
              <span style={{ fontFamily: CC_FONT.mono, fontSize: 30, letterSpacing: '0.16em', color: CC.SPARK }}>BOONDOGGLE SCORE</span>
              <span style={{ fontFamily: CC_FONT.ui, fontSize: 42, color: CC.INK, fontWeight: 700 }}>{system}</span>
            </div>
            <span style={{ fontFamily: CC_FONT.mono, fontSize: 32, color: CC.INK_2 }}>
              {steps.length} steps · {nClaude} claude · {nHuman} human
            </span>
          </div>

          {/* Steps */}
          {steps.map((s, i) => {
            const rowIn = clamp(spring({ frame: frame - (12 + i * stepGap), fps, config: SPRING }), 0, 1);
            const isDM  = dangerousMiddle === s.n;
            const isHuman = s.labor === 'human';
            const pillBg = isHuman ? CC.VIOLET : CC.PANEL;
            const pillFg = isHuman ? CC.PAGE : CC.INK_2;
            return (
              <div key={i} style={{
                position: 'absolute', left: 0, right: 0, top: rowsTop + i * rowH, height: rowH - 8,
                display: 'flex', alignItems: 'center', gap: 18,
                paddingLeft: isDM ? 14 : 0,
                borderLeft: isDM ? `5px solid ${CC.SPARK}` : '5px solid transparent',
                borderBottom: `1px solid ${CC.BORDER}`,
                opacity: rowIn, transform: `translateX(${(1 - rowIn) * -12}px)`,
              }}>
                <span style={{ width: 54, fontFamily: CC_FONT.mono, fontSize: 36, color: CC.INK_3, flexShrink: 0 }}>{s.n}</span>
                <span style={{ width: 44, fontFamily: CC_FONT.mono, fontSize: 30, color: CC.INK_3, flexShrink: 0 }}>{s.phase}</span>
                <span style={{
                  flexShrink: 0, fontFamily: CC_FONT.mono, fontSize: 30, letterSpacing: '0.1em', fontWeight: 700,
                  color: pillFg, background: pillBg, border: `1.5px solid ${isHuman ? CC.VIOLET : CC.BORDER}`,
                  borderRadius: 8, padding: '6px 14px', minWidth: 186, textAlign: 'center',
                }}>
                  {isHuman ? `HUMAN ${s.capacity ? `[${s.capacity}]` : ''}` : 'CLAUDE'}
                </span>
                <div style={{ flex: 1, minWidth: 0 }}>
                  <div style={{ fontFamily: CC_FONT.ui, fontSize: 40, color: CC.INK, lineHeight: 1.18, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                    {s.text}
                  </div>
                  {s.handoff ? (
                    <div style={{ fontFamily: CC_FONT.mono, fontSize: 32, color: CC.ADD_FG, marginTop: 4, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                      ↳ handoff: {s.handoff}
                    </div>
                  ) : null}
                </div>
                {isDM ? (
                  <span style={{ flexShrink: 0, fontFamily: CC_FONT.mono, fontSize: 28, letterSpacing: '0.12em', color: CC.SPARK }}>
                    DANGEROUS MIDDLE
                  </span>
                ) : null}
              </div>
            );
          })}

          {/* Capacity tally */}
          {distribution ? (
            <div style={{
              position: 'absolute', left: 0, right: 0, bottom: 14,
              display: 'flex', alignItems: 'baseline', gap: 30,
              opacity: tallyIn, transform: `translateY(${(1 - tallyIn) * 8}px)`,
            }}>
              <span style={{ fontFamily: CC_FONT.mono, fontSize: 30, letterSpacing: '0.16em', color: CC.INK_2 }}>CAPACITIES</span>
              {CAPACITIES.map((c) => (
                <span key={c} style={{ fontFamily: CC_FONT.mono, fontSize: 38, color: tally[c] === 0 ? CC.DEL_FG : CC.INK }}>
                  {c} <span style={{ color: tally[c] === 0 ? CC.DEL_FG : CC.VIOLET }}>{tally[c]}</span>
                </span>
              ))}
            </div>
          ) : null}
        </div>
      </CCShell>
    </AbsoluteFill>
  );
};

// ── defaultProps ──────────────────────────────────────────────────────────────

export const ccBoondoggleScoreDefaultProps: CCBoondoggleScoreProps = ccBoondoggleScoreSchema.parse({});

// ── Demo twin ─────────────────────────────────────────────────────────────────

export const ccBoondoggleScoreDemoSchema = ccBoondoggleScoreSchema;
export type CCBoondoggleScoreDemoProps   = CCBoondoggleScoreProps;

export const CCBoondoggleScoreDemo: React.FC<CCBoondoggleScoreDemoProps> = (props) => (
  <CCBoondoggleScore {...props} />
);

export const ccBoondoggleScoreDemoDefaultProps: CCBoondoggleScoreDemoProps = ccBoondoggleScoreDemoSchema.parse({
  system: 'reading log — one file',
  steps: [
    { n: 1, phase: 'F', labor: 'human',  capacity: 'PF', text: 'One sentence: a self-contained index.html, no frameworks, no external requests' },
    { n: 2, phase: 'C', labor: 'claude', text: 'Build the form, the list, localStorage persistence', handoff: 'every listed constraint holds under grep' , dependsOn: [1] },
    { n: 3, phase: 'C', labor: 'human',  capacity: 'PA', text: 'Read the file before running it — the delete button was never asked for', dependsOn: [2] },
    { n: 4, phase: 'C', labor: 'claude', text: 'Remove what was not asked for; change nothing else', handoff: 'git diff --stat shows one file, deletions only', dependsOn: [3] },
    { n: 5, phase: 'H', labor: 'human',  capacity: 'IJ', text: 'A tool nobody else sees: rough edges are fine, silent scope is not', dependsOn: [4] },
  ],
  dangerousMiddle: 3,
  distribution: true,
});
