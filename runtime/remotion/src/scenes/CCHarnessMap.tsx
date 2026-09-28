import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring } from 'remotion';
import { z } from 'zod';
import { CC, CC_FONT } from '../tokens/claudecode';

/**
 * CCHarnessMap — the one diagram a cc-explainer is allowed to leave the
 * terminal for: what sits between the model and the file. Concentric rings on
 * the CC page, landing from the inside out: the MODEL at the core (it can only
 * talk), then each ring the session showed — PROMPT, CONTEXT, HARNESS, YOUR
 * LOOP — with the items that ring carried in that session (real strings from
 * the init event and the shell). Each ring lands on its cue; its items follow;
 * a caption lands last. The motion is the claim: the harness is the rings, and
 * every ring is something you already saw on screen.
 *
 * Doctrine: skills/make/cc-explainer/SKILL.md → TERMINAL-FIRST LAW (a diagram
 * of structure the session only implies).
 */

// ── Schema ────────────────────────────────────────────────────────────────────

export const harnessRingSchema = z.object({
  label:  z.string().default('⚠ SET IN BEAT SHEET'),
  /** ≤ 5 words — what this ring is, in the narration's terms. */
  sub:    z.string().optional(),
  /** ≤ 4 items, mono chips; real strings from the session. */
  items:  z.array(z.string()).max(4).default([]),
  /** Frame the ring lands. Items follow at itemGap. */
  cue:    z.number().int().default(0),
  accent: z.enum(['ink', 'violet', 'spark', 'add']).default('ink'),
});

export const ccHarnessMapSchema = z.object({
  /** The core label — the model. */
  core:       z.string().default('⚠ SET IN BEAT SHEET'),
  coreSub:    z.string().optional(),
  rings:      z.array(harnessRingSchema).min(1).max(4).default([]),
  /** ≤ 14 words, lands last. */
  caption:    z.string().optional(),
  captionCue: z.number().int().optional(),
  itemGap:    z.number().int().default(8),
});
export type CCHarnessMapProps = z.infer<typeof ccHarnessMapSchema>;

// ── Helpers ───────────────────────────────────────────────────────────────────

const clamp = (v: number, a: number, b: number) => Math.min(b, Math.max(a, v));
const SPRING = { damping: 22, stiffness: 130, mass: 0.9 };
const ACCENT: Record<'ink' | 'violet' | 'spark' | 'add', string> = {
  ink: CC.INK_2, violet: CC.VIOLET, spark: CC.SPARK, add: CC.ADD_FG,
};

// ── Component ─────────────────────────────────────────────────────────────────

export const CCHarnessMap: React.FC<CCHarnessMapProps> = ({ core, coreSub, rings, caption, captionCue, itemGap }) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  // Geometry: rings are nested rounded rects; each ring's band (top edge)
  // carries its label on the left and its items on the right.
  const BAND    = 104;                 // band height per ring
  // Title-safe: keep everything ≥ 5% from every edge (Gate V edge-bleed).
  const M = 100;
  const OUTER_W = width  - 2 * M;
  const OUTER_H = height - (caption ? 210 : 2 * M);
  const n = rings.length;
  const coreIn = clamp(spring({ frame, fps, config: SPRING }), 0, 1);
  const capCue = captionCue ?? ((rings[n - 1]?.cue ?? 0) + 60);
  const capIn  = clamp(spring({ frame: frame - capCue, fps, config: SPRING }), 0, 1);

  // Ring i (0 = outermost) is inset by a full band at the top (that is where
  // its label and items live) but only a little at the sides and bottom, so
  // every band keeps nearly the full width; the core sits inside the innermost.
  const SIDE = 44, BOTTOM = 34;
  const ringRect = (i: number) => ({
    left: M + i * SIDE, top: M + i * BAND,
    width: OUTER_W - 2 * i * SIDE, height: OUTER_H - i * BAND - i * BOTTOM,
  });
  const coreRect = (() => {
    const r = ringRect(n);
    return { left: r.left + 40, top: r.top + 24, width: r.width - 80, height: r.height - 24 - 40 };
  })();

  // rings[] is authored inside-out (index 0 = closest to the model); draw order outermost first.
  const ordered = rings.map((r, idx) => ({ r, depth: n - 1 - idx }));

  return (
    <AbsoluteFill style={{ backgroundColor: CC.PAGE }}>
      {ordered.map(({ r, depth }) => {
        const rc = ringRect(depth);
        const ringIn = clamp(spring({ frame: frame - r.cue, fps, config: SPRING }), 0, 1);
        const col = ACCENT[r.accent];
        return (
          <div key={depth} style={{
            position: 'absolute', ...rc,
            border: `2px solid ${CC.BORDER}`, borderRadius: CC.RADIUS + 6,
            background: 'transparent',
            opacity: ringIn, transform: `scale(${0.96 + 0.04 * ringIn})`, transformOrigin: 'center',
          }}>
            {/* band: label left, items right */}
            <div style={{ position: 'absolute', left: 0, right: 0, top: 0, height: BAND, display: 'flex', alignItems: 'center', padding: '0 30px', gap: 24 }}>
              <span style={{ fontFamily: CC_FONT.mono, fontSize: 30, letterSpacing: '0.18em', fontWeight: 700, color: col, whiteSpace: 'nowrap' }}>{r.label}</span>
              {r.sub ? <span style={{ fontFamily: CC_FONT.ui, fontSize: 30, color: CC.INK_2, whiteSpace: 'nowrap', flexShrink: 0 }}>{r.sub}</span> : null}
              <span style={{ flex: 1 }} />
              {r.items.map((it, j) => {
                const itIn = clamp(spring({ frame: frame - (r.cue + 12 + j * itemGap), fps, config: SPRING }), 0, 1);
                return (
                  <span key={j} style={{
                    fontFamily: CC_FONT.mono, fontSize: 25, color: CC.INK,
                    background: CC.PANEL, border: `1px solid ${CC.BORDER}`, borderRadius: 8, padding: '8px 14px',
                    whiteSpace: 'nowrap', maxWidth: 560, overflow: 'hidden', textOverflow: 'ellipsis',
                    opacity: itIn, transform: `translateY(${(1 - itIn) * 6}px)`,
                  }}>{it}</span>
                );
              })}
            </div>
            <div style={{ position: 'absolute', left: 0, right: 0, top: BAND - 1, height: 1, background: CC.BORDER, opacity: 0.6 }} />
          </div>
        );
      })}

      {/* the core — the model */}
      <div style={{
        position: 'absolute', ...coreRect,
        display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: 10,
        background: CC.PROMPT_BG, border: `2px solid ${CC.SPARK}`, borderRadius: CC.RADIUS + 6,
        opacity: coreIn, transform: `scale(${0.9 + 0.1 * coreIn})`,
      }}>
        <span style={{ fontFamily: CC_FONT.mono, fontSize: 44, letterSpacing: '0.2em', fontWeight: 700, color: CC.SPARK }}>{core}</span>
        {coreSub ? <span style={{ fontFamily: CC_FONT.ui, fontSize: 34, color: CC.INK_2, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis', maxWidth: '92%' }}>{coreSub}</span> : null}
      </div>

      {caption ? (
        <div style={{
          position: 'absolute', left: M, right: M, bottom: 64,
          display: 'flex', alignItems: 'baseline', gap: 16,
          opacity: capIn, transform: `translateY(${(1 - capIn) * 8}px)`,
        }}>
          <span style={{ fontFamily: CC_FONT.mono, fontSize: 44, color: CC.SPARK }}>✳</span>
          <span style={{ fontFamily: CC_FONT.ui, fontSize: 44, color: CC.INK, fontWeight: 700, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{caption}</span>
        </div>
      ) : null}
    </AbsoluteFill>
  );
};

// ── defaultProps ──────────────────────────────────────────────────────────────

export const ccHarnessMapDefaultProps: CCHarnessMapProps = ccHarnessMapSchema.parse({});

// ── Demo twin ─────────────────────────────────────────────────────────────────

export const ccHarnessMapDemoSchema = ccHarnessMapSchema;
export type CCHarnessMapDemoProps   = CCHarnessMapProps;

export const CCHarnessMapDemo: React.FC<CCHarnessMapDemoProps> = (props) => (
  <CCHarnessMap {...props} />
);

export const ccHarnessMapDemoDefaultProps: CCHarnessMapDemoProps = ccHarnessMapDemoSchema.parse({
  core: 'THE MODEL', coreSub: 'text in, text out — it can only talk',
  rings: [
    { label: 'PROMPT',    sub: 'prompt engineering',  items: ['system prompt', 'CLAUDE.md'], cue: 30, accent: 'ink' },
    { label: 'CONTEXT',   sub: 'context engineering', items: ['"tools": [30 built-in]', '"mcp_servers": 5', '"skills": 40'], cue: 70, accent: 'violet' },
    { label: 'HARNESS',   sub: 'the loop · the rules', items: ['assistant → tool → result', '"permissionMode"', 'the cwd fence', '--max-turns'], cue: 110, accent: 'spark' },
    { label: 'YOUR LOOP', sub: 'harness engineering', items: ['for i in 1 2 3', 'tasks.md', 'fresh session per pass'], cue: 150, accent: 'add' },
  ],
  caption: 'A harness is what the model may touch, the rules, and the loop.',
  captionCue: 220,
});
