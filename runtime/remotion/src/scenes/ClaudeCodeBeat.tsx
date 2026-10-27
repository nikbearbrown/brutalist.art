import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring, interpolate } from 'remotion';
import { z } from 'zod';
import { CLAUDE, CLAUDE_FONT } from '../tokens/claude';

/**
 * ClaudeCodeBeat — code display beat in the Claude fidelity skin.
 * Cream page (#FAF9F5), white code card, terracotta accent on the
 * active traffic-light dot + spark line at bottom.
 * Per ILLUSTRATE LAW: used for code beats only — never as wallpaper.
 * Duration-agnostic — compile.py conforms to actual audio length.
 */

export const claudeCodeBeatSchema = z.object({
  title:     z.string().default('script.py'),
  code:      z.string().default('# code here'),
  sparkLine: z.string().default('The code speaks.'),
  language: z.string().optional(),
  largeText: z.boolean().optional(),
  brandLabel: z.string().optional(),
  /** Optional (2026-10-11): the frame each line lands (one per line), so lines can arrive on their spoken words. A cue <= 0 = on screen at once. */
  lineCues: z.array(z.number()).optional(),
  /**
   * Optional (2026-10-26): size the type to the content and let the card hug the
   * result, instead of a fixed slab at a fixed font size. Opt-in, because turning
   * it on changes the layout of every code beat that already exists.
   */
  fit: z.boolean().optional(),
});
export type ClaudeCodeBeatProps = z.infer<typeof claudeCodeBeatSchema>;

const SERIF = CLAUDE_FONT.serif;
const SANS  = CLAUDE_FONT.ui;
const MONO  = CLAUDE_FONT.mono;
const COMMENT_CLR = '#8B8878';
const clamp = (v: number, a: number, b: number) => Math.min(b, Math.max(a, v));


export const ClaudeCodeBeat: React.FC<ClaudeCodeBeatProps> = ({ title, code, sparkLine, language = 'python', largeText = false, brandLabel, lineCues, fit = false }) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  const cardIn  = spring({ frame,           fps, config: { damping: 28, stiffness: 140, mass: 0.8 } });
  const sparkIn = spring({ frame: frame - 8, fps, config: { damping: 28, stiffness: 140, mass: 0.8 } });

  const lines = code.split('\n');
  const REVEAL_START = 12;
  const LINE_STRIDE  = 3;

  // Extract the filename from the title (everything before " — " or the whole title)
  const filename = title.includes(' — ') ? title.split(' — ')[0].trim() : title;

  // --- fit the code to the card (consulted only when `fit` is set) ---------
  // The card used to be a fixed slab from 8% to 82% of the frame at a fixed
  // font size, so a three-line beat rendered as a mostly empty rectangle and a
  // long line could run past the right edge. Size the type to whichever of the
  // two axes binds first, then let the card hug the result.
  const CARD_W    = width * 0.86;            // left/right insets are 7% each
  const BAND_TOP  = height * 0.08;
  const BAND_H    = height * 0.74;           // the space the card may occupy
  const CHROME_H  = 45;                      // title bar
  const PAD_V     = 40;                      // <pre> padding, top + bottom
  const PAD_H     = 56;                      // <pre> padding, left + right
  const LINE_H    = 1.72;
  const longest   = lines.reduce((m, l) => Math.max(m, l.length), 1);
  const byWidth   = (CARD_W - PAD_H) / (longest * 0.602);   // mono advance ratio
  const byHeight  = (BAND_H - CHROME_H - PAD_V) / (lines.length * LINE_H);
  const FS_MAX      = largeText ? height * 0.032 : height * 0.030;
  const fitFontSize = clamp(Math.min(byWidth, byHeight), height * 0.013, FS_MAX);
  const contentH    = CHROME_H + PAD_V + lines.length * LINE_H * fitFontSize;
  const fitCardH    = clamp(contentH, height * 0.22, BAND_H);
  // With `fit` off the card keeps its original fixed slab, 8% to 82% of frame.
  const cardTop     = fit ? BAND_TOP + (BAND_H - fitCardH) / 2 : BAND_TOP;
  const cardH       = fit ? fitCardH : BAND_H;

  return (
    <AbsoluteFill style={{ background: CLAUDE.PAGE }}>

      {/* Code card */}
      <div style={{
        position: 'absolute',
        left: width * 0.07,
        right: width * 0.07,
        top: cardTop,
        height: cardH,
        background: CLAUDE.CARD,
        border: `1px solid ${CLAUDE.BORDER}`,
        borderRadius: 14,
        boxShadow: '0 8px 32px rgba(61,57,41,0.10)',
        overflow: 'hidden',
        transform: `translateY(${(1 - clamp(cardIn, 0, 1)) * 18}px)`,
        opacity: clamp(cardIn, 0, 1),
      }}>

        {/* Title bar */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: 8,
          padding: '12px 20px',
          background: CLAUDE.PAGE,
          borderBottom: `1px solid ${CLAUDE.BORDER}`,
        }}>
          {/* traffic-light dots — terracotta for the active one */}
          {[CLAUDE.SPARK, CLAUDE.BORDER, CLAUDE.BORDER].map((c, i) => (
            <div key={i} style={{
              width: 11, height: 11, borderRadius: '50%', background: c,
            }} />
          ))}
          <span style={{
            marginLeft: 10,
            fontFamily: MONO,
            fontSize: largeText ? 28 : 13,
            color: CLAUDE.INK_SOFT,
            letterSpacing: '0.02em',
          }}>
            {filename}
          </span>
          <span style={{
            marginLeft: 'auto',
            fontFamily: SANS,
            fontSize: largeText ? 26 : 11,
            fontWeight: 600,
            color: CLAUDE.SPARK,
            letterSpacing: 2,
            textTransform: 'uppercase' as const,
          }}>
            {language}
          </span>
        </div>

        {/* Code lines */}
        <pre style={{
          margin: 0,
          padding: '20px 26px',
          fontFamily: MONO,
          fontSize: fit ? fitFontSize : (largeText ? height * 0.032 : height * 0.022),
          lineHeight: LINE_H,
          textAlign: 'left',
          overflow: 'hidden',
        }}>
          {lines.map((line, i) => {
            const start = lineCues && lineCues[i] !== undefined ? lineCues[i] : REVEAL_START + i * LINE_STRIDE;
            const op = start <= 0 ? 1 : clamp(interpolate(frame, [start, start + 5], [0, 1]), 0, 1);
            const ty = start <= 0 ? 0 : interpolate(frame, [start, start + 7], [6, 0], {
              extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
            });
            const t = line.trimStart();
            const isComment = t.startsWith('#') || t.startsWith('//');
            const color = isComment ? COMMENT_CLR : CLAUDE.INK;
            return (
              <div key={i} style={{
                opacity: op,
                transform: `translateY(${ty}px)`,
                whiteSpace: 'pre' as const,
                color,
              }}>
                {line || '​'}
              </div>
            );
          })}
        </pre>
      </div>

      {/* Spark line at bottom — inset 12px from the card's left AND right edges so no
          glyph (including brandLabel) sits on the card boundary (GATE T §8.13 tol 4px). */}
      <div style={{
        position: 'absolute',
        left: width * 0.07 + 12,
        right: width * 0.07 + 12,
        bottom: height * 0.06,
        display: 'flex',
        alignItems: 'center',
        gap: 10,
        opacity: clamp(sparkIn, 0, 1),
        transform: `translateY(${(1 - clamp(sparkIn, 0, 1)) * 8}px)`,
      }}>
        <span style={{
          flex: 1,
          fontFamily: SERIF,
          fontSize: largeText ? 28 : 22,
          fontStyle: 'italic',
          color: CLAUDE.INK,
        }}>
          {sparkLine}
        </span>
        {brandLabel && <span style={{fontFamily:SERIF,fontSize:28,color:CLAUDE.INK}}>{brandLabel}</span>}
      </div>

    </AbsoluteFill>
  );
};
