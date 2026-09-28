import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig, spring, interpolate} from 'remotion';
import {z} from 'zod';
import {CLAUDE, CLAUDE_FONT} from '../tokens/claude';
import {SAFE} from '../tokens/layout';

/**
 * ClaudeTldrWhat — B00 of a tldr film, the first of TWO TL;DR cards (Bear,
 * 2026-09-22: "TLDR needs two beats: 1. what is this film about? 2. why should
 * you care?" — and "not the Claude.ai interface"). This is card one, WHAT: a
 * TL;DR page on the cream stage. The wordmark "TL;DR" lands top-left with the
 * terracotta period; the greeting and the course/topic line sit beneath it; the
 * question writes on word by word; then the TL;DR lines land one per spoken
 * clause, numbered, the line that has just landed carrying the ONE terracotta
 * numeral while earlier lines settle to ink. Footer chip: the channel.
 *
 * Every reveal is cue-driven so it lands on the spoken word: `cues` are seconds
 * into the beat (question, line 1, line 2, line 3 …); when omitted they are
 * derived from `durationSeconds` (question at 18%, lines from 40% to 80%).
 *
 * Doctrine: skills/make/tldr/SKILL.md → B00 TL;DR contract. GATE T: lowercase
 * runs are measured at x-height at 4K, so line text ≥ 48px, question ≥ 60px.
 */

export const claudeTldrWhatSchema = z.object({
  /** The wordmark. */
  eyebrow: z.string().default('TL;DR'),
  /** The card's heading, under the rule. Card one: what the film is about. */
  heading: z.string().default('What This Film Is About'),
  /** `[hello], [persona]` — the world-language hello (IN-FOR-BEAR LAW: Liam says it aloud too). */
  greeting: z.string().default('Hello, Liam'),
  /** The course / topic line under the greeting, plain Title Case (no tracking — GATE T). */
  topic: z.string().default(''),
  /** The question this film answers, in the viewer's words. Writes on word by word. */
  question: z.string().default('⚠ SET question IN BEAT SHEET'),
  /** The TL;DR — 2–3 lines: the answer, what you will see, the trap. */
  lines: z.array(z.string()).min(1).max(4).default(['⚠ SET lines IN BEAT SHEET']),
  /** Seconds into the beat at which the question, then each line, lands. Optional. */
  cues: z.array(z.number()).optional(),
  /** The beat's measured audio length (Root.tsx sizes the composition from it). */
  durationSeconds: z.number().min(3).default(26),
  folderLabel: z.string().default('@NikBearBrown'),
  dark: z.boolean().default(false),
});
export type ClaudeTldrWhatProps = z.infer<typeof claudeTldrWhatSchema>;

const clamp = (v: number, a: number, b: number) => Math.min(b, Math.max(a, v));
const SPRING = {damping: 26, stiffness: 120, mass: 0.9};

export const ClaudeTldrWhat: React.FC<ClaudeTldrWhatProps> = ({
  eyebrow, heading, greeting, topic, question, lines, cues, durationSeconds, folderLabel, dark,
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const dur = Math.max(3, durationSeconds);
  const n = lines.length;

  const page = dark ? '#1F1E1B' : CLAUDE.PAGE;
  const ink = dark ? '#F2F0E9' : CLAUDE.INK;
  const soft = dark ? '#A9A491' : CLAUDE.INK_SOFT;
  const rule = dark ? '#3A382F' : CLAUDE.BORDER;

  // Cues in frames: question, then each line.
  const qCue = Math.round(((cues && cues[0]) ?? dur * 0.18) * fps);
  const lineCues = lines.map((_, i) =>
    Math.round(((cues && cues[i + 1]) ?? dur * (0.40 + (0.40 * i) / Math.max(1, n - 1 || 1))) * fps),
  );

  const markIn = clamp(spring({frame, fps, config: SPRING}), 0, 1);
  const greetIn = clamp(spring({frame: frame - Math.round(fps * 0.5), fps, config: SPRING}), 0, 1);

  // Question writes on word by word across ~1.6 s from qCue.
  const words = question.split(/\s+/).filter(Boolean);
  const perWord = Math.max(2, Math.round((fps * 1.6) / Math.max(1, words.length)));

  let active = -1;
  lineCues.forEach((c, i) => { if (frame >= c) active = i; });

  const top = SAFE.y + 24;
  const lineTop = 500;
  const lineGap = n <= 3 ? 160 : 124;

  return (
    <AbsoluteFill style={{backgroundColor: page, fontFamily: CLAUDE_FONT.serif}}>
      {/* wordmark */}
      <div style={{
        position: 'absolute', left: SAFE.x, top: top - 10,
        fontSize: 132, fontWeight: 700, lineHeight: 1, color: ink,
        opacity: markIn, transform: `translateY(${(1 - markIn) * 14}px)`,
      }}>
        {eyebrow}<span style={{color: CLAUDE.SPARK}}>.</span>
      </div>
      {/* greeting + topic, right of the wordmark */}
      <div style={{
        position: 'absolute', left: SAFE.x + 470, top: top + 8, maxWidth: SAFE.w - 470,
        opacity: greetIn, transform: `translateX(${(1 - greetIn) * 12}px)`,
      }}>
        <div style={{fontSize: 52, color: ink, lineHeight: 1.15}}>{greeting}</div>
        {topic ? <div style={{fontSize: 50, color: soft, marginTop: 6, lineHeight: 1.2}}>{topic}</div> : null}
      </div>
      <div style={{position: 'absolute', left: SAFE.x, right: SAFE.x, top: top + 156, height: 1.5, backgroundColor: rule, opacity: markIn}} />

      {/* heading */}
      <div style={{
        position: 'absolute', left: SAFE.x, top: top + 170, fontSize: 50, color: ink, fontWeight: 600, lineHeight: 1.2,
        opacity: markIn,
      }}>{heading}</div>

      {/* the question, word by word */}
      <div style={{
        position: 'absolute', left: SAFE.x, top: top + 236, maxWidth: SAFE.w,
        fontSize: 64, color: ink, lineHeight: 1.25,
      }}>
        {words.map((w, i) => {
          const o = clamp(interpolate(frame - qCue - i * perWord, [0, 8], [0, 1]), 0, 1);
          return <span key={i} style={{opacity: o, transition: 'none'}}>{w}{i < words.length - 1 ? ' ' : ''}</span>;
        })}
      </div>

      {/* the TL;DR lines */}
      {lines.map((t, i) => {
        const cue = lineCues[i];
        const inn = clamp(spring({frame: frame - cue, fps, config: SPRING}), 0, 1);
        const isActive = i === active;
        const numColor = isActive ? CLAUDE.SPARK : soft;
        return (
          <div key={i} style={{
            position: 'absolute', left: SAFE.x, right: SAFE.x, top: lineTop + i * lineGap,
            display: 'flex', alignItems: 'flex-start', gap: 34,
            opacity: inn, transform: `translateY(${(1 - inn) * 12}px)`,
          }}>
            <span style={{width: 70, flexShrink: 0, fontSize: 60, fontWeight: 700, color: numColor, lineHeight: 1.0}}>{i + 1}</span>
            <span style={{
              flex: 1, fontSize: 48, color: ink, lineHeight: 1.22, maxWidth: SAFE.w - 110,
              overflow: 'hidden', display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical' as const,
            }}>{t}</span>
          </div>
        );
      })}

      <div style={{
        position: 'absolute', right: SAFE.x, bottom: SAFE.y,
        fontFamily: CLAUDE_FONT.ui, fontSize: 32, color: soft, opacity: 0.9,
      }}>{folderLabel}</div>
    </AbsoluteFill>
  );
};

export const claudeTldrWhatDefaultProps: ClaudeTldrWhatProps = claudeTldrWhatSchema.parse({
  greeting: 'Hej, Liam',
  topic: 'Linear Algebra',
  question: 'Why does the order you multiply two matrices in change the answer?',
  lines: [
    'A matrix is a move, not a number — two moves in the other order land somewhere else.',
    'You will see it on a grid: follow where the two basis arrows go.',
    'The trap: treating AB like 3 × 4. Order only drops out in one special case.',
  ],
});
