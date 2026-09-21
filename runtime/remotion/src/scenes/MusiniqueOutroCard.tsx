import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring, interpolate } from 'remotion';
import { z } from 'zod';
import { MUSINIQUE, FONT_MUSINIQUE } from '../tokens/musinique';
import { MUSINIQUE_LOGO_2_PATH } from '../musinique-logo-2-path';

/**
 * MusiniqueOutroCard — silent Musinique bookend, back half. The
 * musinique-logo-2 mark, the @Musinique handle, and the performing artist's
 * name + link list (Spotify / Apple Music / musinique.com — whichever the
 * registry actually has) stagger in, in Inter. No <Audio> tag anywhere in
 * this file, ever — the bookend is silent by design. Use this any time a
 * finished standalone film needs a Musinique-branded close with artist
 * attribution: `artistName` and `links` are always read from
 * skills/make/musinique-bookend/artists.json by the skill's script, never
 * invented here or by the caller. Resolution and fps are props so the
 * render always matches the source film exactly. musinique-native tokens
 * only (monochrome, Inter, no serif) — never the Claude UI skin.
 */

export const musiniqueOutroLinkSchema = z.object({
  label: z.string(),
  url: z.string(),
});
export type MusiniqueOutroLink = z.infer<typeof musiniqueOutroLinkSchema>;

export const musiniqueOutroCardSchema = z.object({
  artistName: z.string().default('⚠ SET IN BEAT SHEET'),
  links: z.array(musiniqueOutroLinkSchema).default([]),
  durationS: z.number().min(1.5).max(4).default(2.5),
  width: z.number().int().positive().default(1920),
  height: z.number().int().positive().default(1080),
  fps: z.number().positive().default(30), // not int-constrained — some sources run NTSC-style fractional fps
});
export type MusiniqueOutroCardProps = z.infer<typeof musiniqueOutroCardSchema>;

const clamp = (v: number, a: number, b: number) => Math.min(b, Math.max(a, v));

export const MusiniqueOutroCard: React.FC<MusiniqueOutroCardProps> = ({ artistName, links }) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  const isPortrait = height > width;
  const short = Math.min(width, height);

  const markIn = clamp(
    spring({ frame, fps, config: { damping: 18, stiffness: 130, mass: 0.9 } }),
    0,
    1
  );

  const handleDelay = Math.round(fps * 0.35);
  const handleIn = clamp(
    spring({ frame: frame - handleDelay, fps, config: { damping: 22, stiffness: 140, mass: 0.9 } }),
    0,
    1
  );

  const nameDelay = Math.round(fps * 0.6);
  const nameIn = clamp(
    spring({ frame: frame - nameDelay, fps, config: { damping: 22, stiffness: 140, mass: 0.9 } }),
    0,
    1
  );
  const nameY = interpolate(nameIn, [0, 1], [14, 0]);

  const markSize = short * (isPortrait ? 0.17 : 0.14);

  return (
    <AbsoluteFill style={{ background: MUSINIQUE.CREAM, alignItems: 'center', justifyContent: 'center' }}>
      <div style={{
        display: 'flex', flexDirection: 'column', alignItems: 'center',
        gap: isPortrait ? 18 : 22,
      }}>
        <svg
          viewBox="0 0 2048 2048"
          width={markSize}
          height={markSize}
          style={{ display: 'block', transform: `scale(${markIn})`, opacity: markIn }}
        >
          <path d={MUSINIQUE_LOGO_2_PATH} fill={MUSINIQUE.INK} />
        </svg>
        <div style={{
          fontFamily: FONT_MUSINIQUE.display,
          fontWeight: 600,
          fontSize: Math.round(short * 0.032),
          color: MUSINIQUE.TEAL,
          letterSpacing: '0.01em',
          opacity: handleIn,
        }}>
          @Musinique
        </div>
        <div style={{
          fontFamily: FONT_MUSINIQUE.display,
          fontWeight: 600,
          fontSize: Math.round(short * 0.046),
          color: MUSINIQUE.INK,
          textAlign: 'center',
          maxWidth: width * 0.8,
          opacity: nameIn,
          transform: `translateY(${nameY}px)`,
        }}>
          {artistName}
        </div>
        <div style={{
          display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 8, marginTop: 4,
        }}>
          {links.map((link, i) => {
            const rowDelay = Math.round(fps * (0.85 + i * 0.18));
            const rowIn = clamp(
              spring({ frame: frame - rowDelay, fps, config: { damping: 24, stiffness: 150, mass: 0.85 } }),
              0,
              1
            );
            return (
              <div key={`${link.label}-${i}`} style={{
                display: 'flex', flexDirection: 'column', alignItems: 'center',
                opacity: rowIn, transform: `translateY(${(1 - rowIn) * 8}px)`,
                maxWidth: width * 0.7,
              }}>
                <div style={{
                  fontFamily: FONT_MUSINIQUE.display,
                  fontWeight: 600,
                  fontSize: Math.round(short * 0.021),
                  color: MUSINIQUE.SLATE,
                  letterSpacing: '0.08em',
                  textTransform: 'uppercase' as const,
                }}>
                  {link.label}
                </div>
                <div style={{
                  fontFamily: FONT_MUSINIQUE.display,
                  fontWeight: 400,
                  fontSize: Math.round(short * 0.019),
                  color: MUSINIQUE.INK,
                  textAlign: 'center',
                  wordBreak: 'break-word' as const,
                }}>
                  {link.url}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </AbsoluteFill>
  );
};

// ── defaultProps ──────────────────────────────────────────────────────────────

export const musiniqueOutroCardDefaultProps: MusiniqueOutroCardProps = musiniqueOutroCardSchema.parse({});

// ── Demo twin ──────────────────────────────────────────────────────────────────

export const musiniqueOutroCardDemoSchema = musiniqueOutroCardSchema;
export type MusiniqueOutroCardDemoProps = MusiniqueOutroCardProps;

export const MusiniqueOutroCardDemo: React.FC<MusiniqueOutroCardDemoProps> = (props) => (
  <MusiniqueOutroCard {...props} />
);

export const musiniqueOutroCardDemoDefaultProps: MusiniqueOutroCardDemoProps = musiniqueOutroCardDemoSchema.parse({
  artistName: 'Nik Bear Brown',
  links: [
    { label: 'Spotify', url: 'open.spotify.com/artist/0hSpFCJodAYMP2cWK72zI6' },
    { label: 'Apple Music', url: 'music.apple.com/us/artist/nik-bear-brown/1779725275' },
    { label: 'Musinique', url: 'nikbear.musinique.com' },
  ],
  durationS: 3,
  width: 1920,
  height: 1080,
  fps: 30,
});
