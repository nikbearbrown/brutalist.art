import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring, interpolate } from 'remotion';
import { z } from 'zod';
import { MUSINIQUE, FONT_MUSINIQUE } from '../tokens/musinique';
import { MUSINIQUE_LOGO_2_PATH } from '../musinique-logo-2-path';

/**
 * MusiniqueIntroCard — silent Musinique bookend, front half. The
 * musinique-logo-2 mark springs onto a white stage, then the film's title
 * sets in Inter below it — the ONLY text on screen, per the musinique-bookend
 * skill (skills/make/musinique-bookend/). No <Audio> tag anywhere in this
 * file, ever: the bookend is silent by design, not by omission. Reach for
 * this any time a finished standalone film (a song, a spoken-word recitation)
 * needs a Musinique-branded open. Resolution and fps are props, not
 * constants — musinique_bookend.py ffprobes the source film and passes its
 * exact width/height/fps through, so the render always matches. This is a
 * musinique-native piece: monochrome editorial tokens (`tokens/musinique.ts`)
 * and Inter throughout — never the Claude UI skin.
 */

export const musiniqueIntroCardSchema = z.object({
  title: z.string().default('⚠ SET IN BEAT SHEET'),
  durationS: z.number().min(1.5).max(4).default(2.5),
  width: z.number().int().positive().default(1920),
  height: z.number().int().positive().default(1080),
  fps: z.number().positive().default(30), // not int-constrained — some sources run NTSC-style fractional fps
});
export type MusiniqueIntroCardProps = z.infer<typeof musiniqueIntroCardSchema>;

const clamp = (v: number, a: number, b: number) => Math.min(b, Math.max(a, v));

export const MusiniqueIntroCard: React.FC<MusiniqueIntroCardProps> = ({ title }) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  const isPortrait = height > width;
  const short = Math.min(width, height);

  // Mark: spring-scale entrance from frame 0 (this composition IS the beat
  // window — Sequence-relative timing per REMOTION-STANDARDS §3).
  const markIn = spring({ frame, fps, config: { damping: 16, stiffness: 120, mass: 0.9 } });
  const markScale = clamp(markIn, 0, 1.02);
  const markOpacity = clamp(markIn * 1.4, 0, 1);

  // Title: staggered in half a second (fps-relative, never a bare frame
  // literal, so the beat reads identically at 25fps and 30fps sources).
  const titleDelay = Math.round(fps * 0.5);
  const titleIn = clamp(
    spring({ frame: frame - titleDelay, fps, config: { damping: 20, stiffness: 140, mass: 0.9 } }),
    0,
    1
  );
  const titleY = interpolate(titleIn, [0, 1], [16, 0]);

  const markSize = short * (isPortrait ? 0.3 : 0.24);

  return (
    <AbsoluteFill style={{ background: MUSINIQUE.CREAM, alignItems: 'center', justifyContent: 'center' }}>
      <div style={{
        display: 'flex', flexDirection: 'column', alignItems: 'center',
        gap: isPortrait ? 30 : 38,
      }}>
        <svg
          viewBox="0 0 2048 2048"
          width={markSize}
          height={markSize}
          style={{ display: 'block', transform: `scale(${markScale})`, opacity: markOpacity }}
        >
          <path d={MUSINIQUE_LOGO_2_PATH} fill={MUSINIQUE.INK} />
        </svg>
        <div style={{
          fontFamily: FONT_MUSINIQUE.display,
          fontWeight: 600,
          fontSize: Math.round(short * 0.052),
          color: MUSINIQUE.INK,
          letterSpacing: '-0.01em',
          textAlign: 'center',
          maxWidth: width * 0.78,
          opacity: titleIn,
          transform: `translateY(${titleY}px)`,
        }}>
          {title}
        </div>
        <div style={{
          width: 56, height: 3, background: MUSINIQUE.TEAL, opacity: titleIn, borderRadius: 2,
        }} />
      </div>
    </AbsoluteFill>
  );
};

// ── defaultProps ──────────────────────────────────────────────────────────────

export const musiniqueIntroCardDefaultProps: MusiniqueIntroCardProps = musiniqueIntroCardSchema.parse({});

// ── Demo twin ──────────────────────────────────────────────────────────────────

export const musiniqueIntroCardDemoSchema = musiniqueIntroCardSchema;
export type MusiniqueIntroCardDemoProps = MusiniqueIntroCardProps;

export const MusiniqueIntroCardDemo: React.FC<MusiniqueIntroCardDemoProps> = (props) => (
  <MusiniqueIntroCard {...props} />
);

export const musiniqueIntroCardDemoDefaultProps: MusiniqueIntroCardDemoProps = musiniqueIntroCardDemoSchema.parse({
  title: 'Man Singing to Camera',
  durationS: 2.5,
  width: 1920,
  height: 1080,
  fps: 30,
});
