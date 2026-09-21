import React from 'react';
import {AbsoluteFill, Img, staticFile, useCurrentFrame, useVideoConfig, spring} from 'remotion';
import {z} from 'zod';
import {NEU, NEU_RED, FONT_NEU} from '../tokens/neu';
import {SPRING_SMOOTH} from '../tokens/vox';
import {useLato} from '../tokens/lato';

/**
 * SeisOutro — BOUT of a SEIS spotlight reel. White card: unit name, school line,
 * one NU Red rule, then the series line and (once confirmed) the channel handle.
 * No logo is drawn until the official lockup is supplied; no mascot, no jingle —
 * this is Northeastern's channel, not @NikBearBrown (OUTRO-LOCK scope).
 */
export const seisOutroSchema = z.object({
  unit: z.string().default('Software Engineering and Information Systems'),
  school: z.string().default('Northeastern University · College of Engineering'),
  series: z.string().default('SEIS student spotlights'),
  handle: z.string().default(''),
  url: z.string().default(''),
  logo: z.string().default(''), // official mark from logos/seis/ via public/seis/ — never re-drawn
});
export type SeisOutroProps = z.infer<typeof seisOutroSchema>;

export const SeisOutro: React.FC<SeisOutroProps> = ({unit, school, series, handle, url, logo}) => {
  useLato();
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const unitIn = spring({frame, fps, config: SPRING_SMOOTH});
  const ruleIn = spring({frame: frame - 8, fps, config: SPRING_SMOOTH});
  const restIn = spring({frame: frame - 16, fps, config: SPRING_SMOOTH});
  const tail = [handle, url.replace(/^https?:\/\//, '')].filter(Boolean).join('  ·  ');

  return (
    <AbsoluteFill style={{
      backgroundColor: NEU.CREAM, display: 'flex', flexDirection: 'column',
      alignItems: 'center', justifyContent: 'center', overflow: 'hidden',
    }}>
      {logo && (
        <Img src={staticFile(logo)} style={{height: height * 0.22, marginBottom: height * 0.05, opacity: unitIn}} />
      )}
      <div style={{
        fontFamily: FONT_NEU.display, fontSize: height * 0.078, fontWeight: 400,
        color: NEU.INK, textAlign: 'center', maxWidth: width * 0.86, lineHeight: 1.15,
        opacity: unitIn, transform: `translateY(${(1 - unitIn) * 18}px)`,
      }}>{unit}</div>
      <div style={{
        fontFamily: FONT_NEU.display, fontSize: height * 0.038, fontWeight: 400,
        color: NEU.SLATE, marginTop: height * 0.02, opacity: unitIn,
      }}>{school}</div>
      <div style={{
        width: width * 0.10 * ruleIn, height: Math.max(4, height * 0.006),
        backgroundColor: NEU_RED, marginTop: height * 0.045, marginBottom: height * 0.045,
      }} />
      <div style={{
        fontFamily: FONT_NEU.display, fontSize: height * 0.042, fontWeight: 400,
        color: NEU.INK, opacity: restIn,
      }}>{series}</div>
      {tail && (
        <div style={{
          fontFamily: FONT_NEU.display, fontSize: height * 0.03, fontWeight: 400,
          color: NEU.SLATE, marginTop: height * 0.02, opacity: restIn,
        }}>{tail}</div>
      )}
    </AbsoluteFill>
  );
};
