import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig, spring, interpolate} from 'remotion';
import {z} from 'zod';
import {CLAUDE, CLAUDE_FONT} from '../tokens/claude';
import {SAFE} from '../tokens/layout';

/**
 * ClaudeTldrWhy — B01 of a tldr film, the second of TWO TL;DR cards (Bear,
 * 2026-09-22: "1. what is this film about? 2. why should you care? What is the
 * relevance"). Same TL;DR page header as ClaudeTldrWhat so the cut reads as a
 * page turn; the body is the RELEVANCE: one lead sentence — the stake — writes
 * on, then 2–3 consequence lines land on their spoken clauses, each marked by a
 * terracotta dash that settles to ink as the next lands. No numerals here (card
 * one owns numerals); dashes are card two's mark.
 *
 * Cues are seconds into the beat (lead, then each line); derived from
 * durationSeconds when omitted. GATE T: line text ≥ 48px, lead ≥ 60px.
 */

export const claudeTldrWhySchema = z.object({
  eyebrow: z.string().default('TL;DR'),
  heading: z.string().default('Why You Should Care'),
  /** Optional small line under the eyebrow (the course / topic). Usually the same as card one. */
  topic: z.string().default(''),
  /** The stake in one sentence. Writes on word by word. */
  lead: z.string().default('⚠ SET lead IN BEAT SHEET'),
  /** 2–3 consequences: what changes for the viewer once they have this. */
  lines: z.array(z.string()).min(1).max(4).default(['⚠ SET lines IN BEAT SHEET']),
  cues: z.array(z.number()).optional(),
  durationSeconds: z.number().min(3).default(20),
  folderLabel: z.string().default('@NikBearBrown'),
  dark: z.boolean().default(false),
});
export type ClaudeTldrWhyProps = z.infer<typeof claudeTldrWhySchema>;

const clamp = (v: number, a: number, b: number) => Math.min(b, Math.max(a, v));
const SPRING = {damping: 26, stiffness: 120, mass: 0.9};

export const ClaudeTldrWhy: React.FC<ClaudeTldrWhyProps> = ({
  eyebrow, heading, topic, lead, lines, cues, durationSeconds, folderLabel, dark,
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const dur = Math.max(3, durationSeconds);
  const n = lines.length;

  const page = dark ? '#1F1E1B' : CLAUDE.PAGE;
  const ink = dark ? '#F2F0E9' : CLAUDE.INK;
  const soft = dark ? '#A9A491' : CLAUDE.INK_SOFT;
  const rule = dark ? '#3A382F' : CLAUDE.BORDER;

  const leadCue = Math.round(((cues && cues[0]) ?? dur * 0.10) * fps);
  const lineCues = lines.map((_, i) =>
    Math.round(((cues && cues[i + 1]) ?? dur * (0.38 + (0.42 * i) / Math.max(1, n - 1 || 1))) * fps),
  );

  // The header is already on screen from card one: no entrance, a held page.
  const headIn = 1;
  const words = lead.split(/\s+/).filter(Boolean);
  const perWord = Math.max(2, Math.round((fps * 1.8) / Math.max(1, words.length)));

  let active = -1;
  lineCues.forEach((c, i) => { if (frame >= c) active = i; });

  const top = SAFE.y + 24;
  const lineTop = 560;
  const lineGap = n <= 3 ? 150 : 118;

  return (
    <AbsoluteFill style={{backgroundColor: page, fontFamily: CLAUDE_FONT.serif}}>
      <div style={{position: 'absolute', left: SAFE.x, top: top - 10, fontSize: 132, fontWeight: 700, lineHeight: 1, color: ink, opacity: headIn}}>
        {eyebrow}<span style={{color: CLAUDE.SPARK}}>.</span>
      </div>
      {topic ? (
        <div style={{position: 'absolute', left: SAFE.x + 470, top: top + 52, maxWidth: SAFE.w - 470, fontSize: 50, color: soft, lineHeight: 1.2}}>{topic}</div>
      ) : null}
      <div style={{position: 'absolute', left: SAFE.x, right: SAFE.x, top: top + 156, height: 1.5, backgroundColor: rule}} />

      <div style={{position: 'absolute', left: SAFE.x, top: top + 170, fontSize: 50, color: ink, fontWeight: 600, lineHeight: 1.2}}>{heading}</div>

      {/* the stake, word by word */}
      <div style={{position: 'absolute', left: SAFE.x, top: top + 244, maxWidth: SAFE.w, fontSize: 64, color: ink, lineHeight: 1.25}}>
        {words.map((w, i) => {
          const o = clamp(interpolate(frame - leadCue - i * perWord, [0, 8], [0, 1]), 0, 1);
          return <span key={i} style={{opacity: o}}>{w}{i < words.length - 1 ? ' ' : ''}</span>;
        })}
      </div>

      {lines.map((t, i) => {
        const inn = clamp(spring({frame: frame - lineCues[i], fps, config: SPRING}), 0, 1);
        const isActive = i === active;
        return (
          <div key={i} style={{
            position: 'absolute', left: SAFE.x, right: SAFE.x, top: lineTop + i * lineGap,
            display: 'flex', alignItems: 'flex-start', gap: 34,
            opacity: inn, transform: `translateY(${(1 - inn) * 12}px)`,
          }}>
            <span style={{width: 70, flexShrink: 0, height: 8, marginTop: 28, backgroundColor: isActive ? CLAUDE.SPARK : soft, borderRadius: 4}} />
            <span style={{
              flex: 1, fontSize: 48, color: ink, lineHeight: 1.22, maxWidth: SAFE.w - 110,
              overflow: 'hidden', display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical' as const,
            }}>{t}</span>
          </div>
        );
      })}

      <div style={{position: 'absolute', right: SAFE.x, bottom: SAFE.y, fontFamily: CLAUDE_FONT.ui, fontSize: 32, color: soft, opacity: 0.9}}>{folderLabel}</div>
    </AbsoluteFill>
  );
};

export const claudeTldrWhyDefaultProps: ClaudeTldrWhyProps = claudeTldrWhySchema.parse({
  topic: 'Linear Algebra',
  lead: 'Every rotation, every neural-network layer, every camera move is matrices applied in order.',
  lines: [
    'Get the order wrong and the picture is wrong, silently — no error, just a different answer.',
    'Once you see a matrix as a move, the rule for composing them stops being a formula to memorize.',
  ],
});
