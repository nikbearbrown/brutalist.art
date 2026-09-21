import React from 'react';
import {AbsoluteFill, Audio, Img, OffthreadVideo, Sequence, staticFile, useCurrentFrame, useVideoConfig, interpolate, spring} from 'remotion';
import {z} from 'zod';
import {NEU, NEU_RED, FONT_NEU} from '../tokens/neu';
import {SPRING_SMOOTH} from '../tokens/vox';
import {useLato} from '../tokens/lato';

/**
 * SeisFilm — seis-composite: the alumni impact film. A timeline of items rendered back to back:
 *   card   — kinetic text on the SEIS page (section titles, the stat card, the bridge)
 *   clip   — a rendered SeisQA mp4 (or any mp4) played as is
 *   end    — the static SEIS end slide (primary logo, ~10 s)
 * Optional music bed, ducked under speech. NEU brand throughout.
 */
const item = z.object({kind: z.enum(['card', 'clip', 'end']), frames: z.number(), src: z.string().default(''),
  eyebrow: z.string().default(''), lines: z.array(z.string()).default([]), emphasis: z.number().default(-1), dark: z.boolean().default(false)});
export const seisFilmSchema = z.object({items: z.array(item).default([]), music: z.string().default(''), musicGain: z.number().default(0.12)});
export type SeisFilmProps = z.infer<typeof seisFilmSchema>;

const Card: React.FC<{it: z.infer<typeof item>}> = ({it}) => {
  const frame = useCurrentFrame(); const {fps, width, height} = useVideoConfig();
  const bg = it.dark ? '#000' : NEU.CREAM; const ink = it.dark ? '#fff' : NEU.INK;
  const out = interpolate(frame, [it.frames - 8, it.frames], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const n = Math.max(1, it.lines.length); const size = height * (n <= 2 ? 0.10 : n === 3 ? 0.08 : 0.064);
  return (
    <AbsoluteFill style={{backgroundColor: bg, opacity: out}}>
      {it.eyebrow && <div style={{position: 'absolute', left: width * 0.07, top: height * 0.08, fontFamily: FONT_NEU.display, fontSize: height * 0.024, letterSpacing: 1.5, textTransform: 'uppercase', color: NEU.SLATE, opacity: spring({frame, fps, config: SPRING_SMOOTH})}}>{it.eyebrow}</div>}
      <div style={{position: 'absolute', left: width * 0.07, top: height * 0.13, width: width * 0.12 * spring({frame, fps, config: SPRING_SMOOTH}), height: Math.max(4, height * 0.007), backgroundColor: NEU_RED}} />
      <div style={{position: 'absolute', left: width * 0.07, right: width * 0.07, top: height * 0.30, display: 'flex', flexDirection: 'column', gap: height * 0.03}}>
        {it.lines.map((ln, i) => { const s = spring({frame: frame - 6 - i * 9, fps, config: SPRING_SMOOTH});
          return <div key={i} style={{fontFamily: FONT_NEU.display, fontSize: size, lineHeight: 1.12, color: i === it.emphasis ? NEU_RED : ink, opacity: s, transform: `translateY(${(1 - s) * 18}px)`}}>{ln}</div>; })}
      </div>
      <Img src={staticFile('seis/seis-button-logo.jpg')} style={{position: 'absolute', right: width * 0.06, top: height * 0.05, height: height * 0.11}} />
    </AbsoluteFill>
  );
};
const End: React.FC = () => {
  const frame = useCurrentFrame(); const {fps, width, height} = useVideoConfig(); const s = spring({frame, fps, config: SPRING_SMOOTH});
  return (
    <AbsoluteFill style={{backgroundColor: NEU.CREAM, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center'}}>
      <Img src={staticFile('seis/seis-logo.png')} style={{height: height * 0.20, opacity: s}} />
      <Img src={staticFile('seis/seis-button-logo.jpg')} style={{height: height * 0.16, marginTop: height * 0.05, opacity: s}} />
      <div style={{fontFamily: FONT_NEU.display, fontSize: height * 0.036, color: NEU.SLATE, marginTop: height * 0.02, opacity: s}}>Northeastern University · College of Engineering</div>
      <div style={{width: width * 0.08, height: Math.max(4, height * 0.006), backgroundColor: NEU_RED, marginTop: height * 0.05, opacity: s}} />
      <div style={{fontFamily: FONT_NEU.display, fontSize: height * 0.05, color: NEU.INK, marginTop: height * 0.04, opacity: s}}>This is SEIS.</div>
    </AbsoluteFill>
  );
};
export const SeisFilm: React.FC<SeisFilmProps> = ({items, music, musicGain}) => {
  useLato(); let t = 0;
  return (
    <AbsoluteFill style={{backgroundColor: '#000'}}>
      {music && <Audio src={staticFile(music)} volume={musicGain} />}
      {items.map((it, i) => { const from = t; t += it.frames;
        return <Sequence key={i} from={from} durationInFrames={it.frames}>
          {it.kind === 'card' ? <Card it={it} /> : it.kind === 'end' ? <End /> : <OffthreadVideo src={staticFile(it.src)} style={{width: '100%', height: '100%'}} />}
        </Sequence>; })}
    </AbsoluteFill>
  );
};
