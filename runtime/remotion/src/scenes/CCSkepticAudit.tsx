import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring, interpolate } from 'remotion';
import { z } from 'zod';
import { CC, CC_FONT } from '../tokens/claudecode';
import { CCShell, CC_BODY } from './CCShell';

/**
 * CCSkepticAudit — the SKEPTIC beat of a cc-explainer. Claude's completion
 * claim is pinned at the top of the terminal; beneath it the skeptic's four
 * moves (Descartes · Hume · Popper · Plato) each show the question she asked
 * aloud and the command she ran, and take a stamp — ✓ pass, ✗ fail, ○ open —
 * on their cue. A verdict line lands last.
 *
 * The stamps are the evidence: every ✓ points at a command that returned.
 * Doctrine: skills/make/cc-explainer/reference/three-beats.md.
 */

// ── Schema ────────────────────────────────────────────────────────────────────

export const skepticMoveSchema = z.object({
  name:     z.enum(['Descartes', 'Hume', 'Popper', 'Plato']),
  question: z.string().default('⚠ SET IN BEAT SHEET'),
  command:  z.string().default('⚠ SET IN BEAT SHEET'),
  result:   z.enum(['pass', 'fail', 'open', 'pending']).default('pending'),
  /** Frame at which the stamp lands. */
  cue:      z.number().int().default(0),
});
export type SkepticMove = z.infer<typeof skepticMoveSchema>;

export const ccSkepticAuditSchema = z.object({
  /** Claude's completion line, verbatim. */
  claim:   z.string().default('⚠ SET IN BEAT SHEET'),
  moves:   z.array(skepticMoveSchema).min(1).max(4).default([]),
  /** Lands after the last stamp. ≤ 12 words. */
  verdict: z.string().optional(),
  /** Frame at which the verdict lands (default: last cue + 30). */
  verdictCue: z.number().int().optional(),
});
export type CCSkepticAuditProps = z.infer<typeof ccSkepticAuditSchema>;

// ── Helpers ───────────────────────────────────────────────────────────────────

const clamp = (v: number, a: number, b: number) => Math.min(b, Math.max(a, v));
const SPRING = { damping: 24, stiffness: 140, mass: 0.9 };
const STAMP  = { damping: 18, stiffness: 220, mass: 0.7 };

const stampGlyph = (r: SkepticMove['result']) =>
  r === 'pass' ? '✓' : r === 'fail' ? '✗' : r === 'open' ? '○' : '·';
const stampColor = (r: SkepticMove['result']) =>
  r === 'pass' ? CC.DONE : r === 'fail' ? CC.DEL_FG : r === 'open' ? CC.INK_2 : CC.INK_3;

// ── Component ─────────────────────────────────────────────────────────────────

export const CCSkepticAudit: React.FC<CCSkepticAuditProps> = ({ claim, moves, verdict, verdictCue }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const claimIn = clamp(spring({ frame, fps, config: SPRING }), 0, 1);
  const lastCue = moves.reduce((m, mv) => Math.max(m, mv.cue), 0);
  const vCue    = verdictCue ?? lastCue + 30;
  const vIn     = clamp(spring({ frame: frame - vCue, fps, config: SPRING }), 0, 1);

  const TOP   = 14;
  const ROW_Y = 128;
  const ROW_H = 150;

  return (
    <AbsoluteFill>
      <CCShell title="claude-code" mode="default">
        <div style={{ position: 'absolute', left: 16, right: 16, top: TOP, bottom: 0 }}>

          {/* The claim, pinned. */}
          <div style={{
            display: 'flex', alignItems: 'center', gap: 18,
            background: CC.PROMPT_BG, border: `1.5px solid ${CC.BORDER}`, borderRadius: 10,
            padding: '14px 22px', opacity: claimIn,
            transform: `translateY(${(1 - claimIn) * 10}px)`,
          }}>
            <span style={{ fontFamily: CC_FONT.mono, fontSize: 30, letterSpacing: '0.16em', color: CC.SPARK }}>CLAIM</span>
            <span style={{ fontFamily: CC_FONT.mono, fontSize: 44, color: CC.INK, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
              {claim}
            </span>
          </div>

          {/* The four moves. */}
          {moves.map((mv, i) => {
            const rowIn  = clamp(spring({ frame: frame - (8 + i * 10), fps, config: SPRING }), 0, 1);
            const stamp  = clamp(spring({ frame: frame - mv.cue, fps, config: STAMP }), 0, 1);
            const landed = frame >= mv.cue;
            return (
              <div key={i} style={{
                position: 'absolute', left: 0, right: 0, top: ROW_Y + i * ROW_H, height: ROW_H - 12,
                display: 'flex', alignItems: 'center', gap: 22,
                borderBottom: `1px solid ${CC.BORDER}`,
                opacity: rowIn, transform: `translateX(${(1 - rowIn) * -12}px)`,
              }}>
                <div style={{ width: 200, fontFamily: CC_FONT.mono, fontSize: 34, letterSpacing: '0.08em', color: CC.VIOLET, flexShrink: 0 }}>
                  {mv.name.toUpperCase()}
                </div>
                <div style={{ flex: 1, minWidth: 0 }}>
                  <div style={{ fontFamily: CC_FONT.ui, fontSize: 44, color: CC.INK, lineHeight: 1.2, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                    {mv.question}
                  </div>
                  <div style={{ fontFamily: CC_FONT.mono, fontSize: 38, color: CC.INK_2, marginTop: 6, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                    <span style={{ color: CC.VIOLET }}>&gt; </span>{mv.command}
                  </div>
                </div>
                <div style={{
                  width: 90, textAlign: 'center', flexShrink: 0,
                  fontFamily: CC_FONT.mono, fontSize: 64, lineHeight: 1,
                  color: landed ? stampColor(mv.result) : CC.INK_3,
                  opacity: landed ? stamp : 0.5,
                  transform: `scale(${landed ? 0.8 + stamp * 0.2 : 1})`,
                }}>
                  {landed ? stampGlyph(mv.result) : '·'}
                </div>
              </div>
            );
          })}

          {/* Verdict line. */}
          {verdict ? (
            <div style={{
              position: 'absolute', left: 0, right: 0, bottom: 18,
              display: 'flex', alignItems: 'baseline', gap: 16,
              opacity: vIn, transform: `translateY(${(1 - vIn) * 8}px)`,
            }}>
              <span style={{ fontFamily: CC_FONT.mono, fontSize: 44, color: CC.SPARK }}>✳</span>
              <span style={{ fontFamily: CC_FONT.ui, fontSize: 46, color: CC.INK, fontWeight: 700 }}>{verdict}</span>
            </div>
          ) : null}
        </div>
      </CCShell>
    </AbsoluteFill>
  );
};

// ── defaultProps ──────────────────────────────────────────────────────────────

export const ccSkepticAuditDefaultProps: CCSkepticAuditProps = ccSkepticAuditSchema.parse({});

// ── Demo twin ─────────────────────────────────────────────────────────────────

export const ccSkepticAuditDemoSchema = ccSkepticAuditSchema;
export type CCSkepticAuditDemoProps   = CCSkepticAuditProps;

export const CCSkepticAuditDemo: React.FC<CCSkepticAuditDemoProps> = (props) => (
  <CCSkepticAudit {...props} />
);

export const ccSkepticAuditDemoDefaultProps: CCSkepticAuditDemoProps = ccSkepticAuditDemoSchema.parse({
  claim: '✓ Created index.html — form, list, localStorage, no dependencies',
  moves: [
    { name: 'Descartes', question: 'What would have to be true for "done" to be wrong?', command: 'grep -c localStorage index.html', result: 'pass', cue: 40 },
    { name: 'Hume',      question: 'It worked for the last ask. That proves nothing about this one.', command: 'wc -l index.html && git status --short', result: 'pass', cue: 80 },
    { name: 'Popper',    question: 'I asked for no external requests. Name the failure, then look.', command: 'grep -nE "https?://|<script src" index.html', result: 'fail', cue: 120 },
    { name: 'Plato',     question: 'The file is the artifact. The page in a browser is the world.', command: 'open index.html', result: 'open', cue: 160 },
  ],
  verdict: 'Three checks pass. One found something. One I cannot run here.',
});
