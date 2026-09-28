import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring } from 'remotion';
import { z } from 'zod';
import { CC, CC_FONT } from '../tokens/claudecode';
import { CCShell } from './CCShell';

/**
 * CCDefinitions — the definitions card of a cc-explainer: the two-to-five
 * pieces of jargon this film cannot avoid, each defined in one plain line for
 * a smart viewer who uses the chat window but may not know the technical
 * words. Rows land one at a time — term first (mono, violet), then its meaning
 * slides in beside it — so the viewer reads each before the next arrives.
 * Sits in the CCShell chrome so the cut from the session is quiet.
 *
 * Doctrine: skills/make/cc-explainer/SKILL.md → DEFINITIONS LAW (only when
 * there is critical jargon; high level; never a lecture).
 */

// ── Schema ────────────────────────────────────────────────────────────────────

export const definitionSchema = z.object({
  /** The word as it appears on screen in this film. ≤ 18 chars. */
  term:    z.string().default('⚠ SET IN BEAT SHEET'),
  /** One plain line, ≤ ~70 chars; wraps to two lines at most. */
  meaning: z.string().default('⚠ SET IN BEAT SHEET'),
});

export const ccDefinitionsSchema = z.object({
  title:   z.string().default('TERMS IN THIS FILM'),
  terms:   z.array(definitionSchema).min(1).max(5).default([]),
  /** Frame the first row lands. */
  startCue: z.number().int().default(12),
  /** Frames between rows. */
  rowGap:   z.number().int().default(48),
});
export type CCDefinitionsProps = z.infer<typeof ccDefinitionsSchema>;

// ── Helpers ───────────────────────────────────────────────────────────────────

const clamp = (v: number, a: number, b: number) => Math.min(b, Math.max(a, v));
const SPRING = { damping: 24, stiffness: 140, mass: 0.9 };

// ── Component ─────────────────────────────────────────────────────────────────

export const CCDefinitions: React.FC<CCDefinitionsProps> = ({ title, terms, startCue, rowGap }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const headIn = clamp(spring({ frame, fps, config: SPRING }), 0, 1);
  const n = terms.length;
  const ROW_H = n <= 3 ? 190 : n === 4 ? 160 : 136;
  const TOP = 92;

  return (
    <AbsoluteFill>
      <CCShell title="definitions" mode="default">
        <div style={{
          position: 'absolute', left: 16, right: 16, top: 12,
          fontFamily: CC_FONT.mono, fontSize: 30, letterSpacing: '0.18em', color: CC.SPARK,
          borderBottom: `1.5px solid ${CC.BORDER}`, paddingBottom: 12, opacity: headIn,
        }}>{title}</div>
        {terms.map((t, i) => {
          const cue = startCue + i * rowGap;
          const termIn = clamp(spring({ frame: frame - cue, fps, config: SPRING }), 0, 1);
          const defIn  = clamp(spring({ frame: frame - cue - 10, fps, config: SPRING }), 0, 1);
          return (
            <div key={i} style={{
              position: 'absolute', left: 16, right: 16, top: TOP + i * ROW_H, height: ROW_H - 14,
              display: 'flex', alignItems: 'center', gap: 28,
              borderBottom: `1px solid ${CC.BORDER}`,
            }}>
              <span style={{
                width: 400, flexShrink: 0, fontFamily: CC_FONT.mono, fontSize: 36, fontWeight: 700, color: CC.VIOLET,
                whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis',
                opacity: termIn, transform: `translateY(${(1 - termIn) * 8}px)`,
              }}>{t.term}</span>
              <span style={{
                flex: 1, fontFamily: CC_FONT.ui, fontSize: 38, color: CC.INK, lineHeight: 1.22,
                overflow: 'hidden', display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical' as const,
                opacity: defIn, transform: `translateX(${(1 - defIn) * 14}px)`,
              }}>{t.meaning}</span>
            </div>
          );
        })}
      </CCShell>
    </AbsoluteFill>
  );
};

// ── defaultProps ──────────────────────────────────────────────────────────────

export const ccDefinitionsDefaultProps: CCDefinitionsProps = ccDefinitionsSchema.parse({});

// ── Demo twin ─────────────────────────────────────────────────────────────────

export const ccDefinitionsDemoSchema = ccDefinitionsSchema;
export type CCDefinitionsDemoProps   = CCDefinitionsProps;

export const CCDefinitionsDemo: React.FC<CCDefinitionsDemoProps> = (props) => (
  <CCDefinitions {...props} />
);

export const ccDefinitionsDemoDefaultProps: CCDefinitionsDemoProps = ccDefinitionsDemoSchema.parse({
  terms: [
    { term: 'headless',        meaning: 'Claude Code run from the shell with one prompt — no chat window, it answers and exits' },
    { term: 'tools list',      meaning: 'what the model is allowed to call: read a file, write one, run a command, use a connector' },
    { term: 'connector (MCP)', meaning: 'an outside service plugged in as tools — Google Drive, Vercel, your calendar' },
    { term: 'permission mode', meaning: 'the rule for which tool calls need your yes before they run' },
    { term: 'stream-json',     meaning: 'the whole session as a log, one event per line — the receipt' },
  ],
});
