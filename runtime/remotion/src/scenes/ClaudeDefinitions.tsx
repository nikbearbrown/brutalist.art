import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig, spring, interpolate} from 'remotion';
import {z} from 'zod';
import {CLAUDE, CLAUDE_FONT} from '../tokens/claude';
import {SAFE} from '../tokens/layout';

/**
 * ClaudeDefinitions — the TERMS beat of a Claude-skinned explainer: the two-
 * to-five pieces of jargon this film cannot avoid, each defined in one plain
 * line for a smart viewer who may not know the technical words. Rows land one
 * at a time — the term first, then its meaning slides in beside it — so the
 * viewer reads each before the next arrives. The row that has just landed
 * carries the ONE terracotta moment; earlier rows settle to ink.
 *
 * Cream stage (CLAUDE.PAGE), EB Garamond throughout, no chrome — this is the
 * Claude-register port of the CC kit's CCDefinitions (dark terminal shell),
 * for skills whose body is NOT the terminal (tldr, ai-explainer family).
 *
 * Doctrine: skills/make/tldr/SKILL.md → TERMS beat (only when there is
 * critical jargon; high level; never a lecture). Title Case title per brand law.
 */

// ── Schema ────────────────────────────────────────────────────────────────────

export const claudeDefinitionSchema = z.object({
  /** The word as it appears on screen in this film. ≤ 22 chars. */
  term: z.string().default('⚠ SET IN BEAT SHEET'),
  /** One plain line, ≤ ~80 chars; wraps to two lines at most. */
  meaning: z.string().default('⚠ SET IN BEAT SHEET'),
});

export const claudeDefinitionsSchema = z.object({
  title: z.string().default('Terms In This Film'),
  terms: z.array(claudeDefinitionSchema).min(1).max(5).default([]),
  /**
   * The beat's measured audio length. Root.tsx sizes the composition from it
   * (calculateMetadata); rows are distributed across 12%–70% of it unless
   * startCue/rowGap are given explicitly.
   */
  durationSeconds: z.number().min(2).default(14),
  /** Frame the first row lands (overrides the duration-derived spacing). */
  startCue: z.number().int().optional(),
  /** Frames between rows (overrides the duration-derived spacing). */
  rowGap: z.number().int().optional(),
  /** Dark-canvas polarity (charcoal ground, cream ink) — off by default. */
  dark: z.boolean().default(false),
  /** Footer chip; hardcoded default is the one channel. */
  folderLabel: z.string().default('@NikBearBrown'),
});
export type ClaudeDefinitionsProps = z.infer<typeof claudeDefinitionsSchema>;

// ── Helpers ───────────────────────────────────────────────────────────────────

const clamp = (v: number, a: number, b: number) => Math.min(b, Math.max(a, v));
const SPRING = {damping: 26, stiffness: 130, mass: 0.9};

// ── Component ─────────────────────────────────────────────────────────────────

export const ClaudeDefinitions: React.FC<ClaudeDefinitionsProps> = ({
  title, terms, durationSeconds, startCue, rowGap, dark, folderLabel,
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const n = Math.max(1, terms.length);

  const total = Math.max(2, durationSeconds) * fps;
  const first = startCue ?? Math.round(total * 0.12);
  const gap = rowGap ?? Math.max(fps * 0.9, Math.round((total * 0.58) / n));

  const page = dark ? '#1F1E1B' : CLAUDE.PAGE;
  const ink = dark ? '#F2F0E9' : CLAUDE.INK;
  const soft = dark ? '#A9A491' : CLAUDE.INK_SOFT;
  const rule = dark ? '#3A382F' : CLAUDE.BORDER;

  const headIn = clamp(spring({frame, fps, config: SPRING}), 0, 1);

  // Layout: rows fill the safe area below the title (FILL-THE-CANVAS).
  const top = SAFE.y + 150;
  const bottom = SAFE.y + SAFE.h - 70;
  const rowH = Math.floor((bottom - top) / n);
  const termSize = n <= 3 ? 54 : 50;
  const meanSize = 48;   // ≥ 48: a lowercase run's x-height must clear GATE T's 41px floor at 4K

  // Which row landed most recently → carries the terracotta.
  let active = -1;
  terms.forEach((_, i) => { if (frame >= first + i * gap) active = i; });

  return (
    <AbsoluteFill style={{backgroundColor: page, fontFamily: CLAUDE_FONT.serif}}>
      {/* Title — Title Case serif, letterspaced small caps feel, hairline under */}
      <div style={{
        position: 'absolute', left: SAFE.x, right: SAFE.x, top: SAFE.y + 24,
        fontSize: 54, letterSpacing: '0.06em', color: soft,   // ≥ 54: tracked letters are single blobs; their x-height must clear GATE T's 41px floor at 4K
        borderBottom: `1.5px solid ${rule}`, paddingBottom: 18,
        opacity: headIn, transform: `translateY(${(1 - headIn) * 10}px)`,
      }}>
        {title}
      </div>

      {terms.map((t, i) => {
        const cue = first + i * gap;
        const termIn = clamp(spring({frame: frame - cue, fps, config: SPRING}), 0, 1);
        const meanIn = clamp(spring({frame: frame - cue - Math.round(fps * 0.25), fps, config: SPRING}), 0, 1);
        const isActive = i === active;
        // Settle: terracotta while active, then a soft fade to ink over ~0.6 s.
        const sinceNext = active > i ? frame - (first + (i + 1) * gap) : 0;
        const settle = active > i ? clamp(interpolate(sinceNext, [0, fps * 0.6], [0, 1]), 0, 1) : 0;
        const termOpacity = isActive ? termIn : termIn * (1 - settle) + settle;
        return (
          <div key={i} style={{
            position: 'absolute', left: SAFE.x, right: SAFE.x,
            top: top + i * rowH, height: rowH - 12,
            display: 'flex', alignItems: 'center', gap: 40,
          }}>
            <div style={{position: 'absolute', left: 0, right: 0, bottom: 0, height: 1, backgroundColor: rule, opacity: termIn}} />
            {/* GATE T (2026-09-22): the landed row's terracotta is a DOT beside the term,
                never the term's glyphs — terracotta text on cream is 2.74:1 and fails §8.3
                whenever the mid-beat sample lands on a long active term. */}
            <div style={{
              position: 'absolute', left: 0, top: '50%', width: 18, height: 18, marginTop: -9,   // inside title-safe (Gate V edge-bleed at left:-34)
              borderRadius: 9, backgroundColor: CLAUDE.SPARK,
              opacity: isActive ? termIn : (1 - settle) * termIn,
            }} />
            <span style={{
              width: 520, flexShrink: 0, marginLeft: 34, fontSize: termSize, fontWeight: 600,
              color: ink,
              whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis',
              opacity: termOpacity, transform: `translateY(${(1 - termIn) * 10}px)`,
            }}>{t.term}</span>
            <span style={{
              flex: 1, fontSize: meanSize, color: ink, lineHeight: 1.25,
              overflow: 'hidden', display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical' as const,
              opacity: meanIn, transform: `translateX(${(1 - meanIn) * 16}px)`,
            }}>{t.meaning}</span>
          </div>
        );
      })}

      {/* Footer chip — the channel, small, inside the safe inset */}
      <div style={{
        position: 'absolute', right: SAFE.x, bottom: SAFE.y,
        fontFamily: CLAUDE_FONT.ui, fontSize: 32, color: soft, opacity: 0.9,
      }}>{folderLabel}</div>
    </AbsoluteFill>
  );
};

// ── defaultProps ──────────────────────────────────────────────────────────────

export const claudeDefinitionsDefaultProps: ClaudeDefinitionsProps = claudeDefinitionsSchema.parse({
  terms: [
    {term: 'basis vector', meaning: 'the two arrows every other arrow in the plane is built from'},
    {term: 'linear', meaning: 'grid lines stay parallel and evenly spaced; the origin stays put'},
    {term: 'matrix', meaning: 'a 2×2 box of numbers that records where the basis vectors landed'},
    {term: 'determinant', meaning: 'how much one unit of area is stretched, and whether it flips'},
  ],
});
