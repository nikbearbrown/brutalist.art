import React from 'react';
import {AbsoluteFill, Img, staticFile, useCurrentFrame, useVideoConfig, spring} from 'remotion';
import {z} from 'zod';
import {NEU_RED, FONT_NEU} from '../tokens/neu';
import {SPRING_SMOOTH} from '../tokens/vox';
import {useLato} from '../tokens/lato';
import {SEIS_TRIBUTE} from '../data/seisTribute';

/** SeisWall — the wall of every spotlight face (from the tribute data) assembling behind 1–3 big lines
 *  (the breadth numbers). Black ground; the lines sit on a flat scrim band (no gradients — NEU law). */
export const seisWallSchema = z.object({
  lines: z.array(z.string()).default(['about 250 films', '36 fellows', 'four in five came through SEIS']),
  emphasis: z.number().int().default(2),
  cols: z.number().int().default(14),
});
export type SeisWallProps = z.infer<typeof seisWallSchema>;

export const SeisWall: React.FC<SeisWallProps> = ({lines, emphasis, cols}) => {
  useLato();
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const faces = SEIS_TRIBUTE.faces; const rows = Math.ceil(faces.length / cols);
  // inset inside the 90% title-safe box (VISUAL QC edge-bleed) — the mosaic is not full-bleed
  const X0 = width * 0.07, Y0 = height * 0.07; const tw = (width * 0.86) / cols, th = (height * 0.86) / rows;
  return (
    <AbsoluteFill style={{backgroundColor: '#000', overflow: 'hidden'}}>
      {faces.map((f, i) => {
        const s = spring({frame: frame - (i % cols) * 1.2 - Math.floor(i / cols) * 3, fps, config: SPRING_SMOOTH});
        return <div key={i} style={{position: 'absolute', left: X0 + (i % cols) * tw, top: Y0 + Math.floor(i / cols) * th, width: tw, height: th, overflow: 'hidden', opacity: s * 0.3}}><Img src={staticFile(f.file)} style={{width: '100%', height: '100%', objectFit: 'cover'}} /></div>;
      })}
      <div style={{position: 'absolute', left: 0, right: 0, top: '50%', transform: 'translateY(-50%)', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: height * 0.02}}>
        {lines.map((ln, i) => {
          const s = spring({frame: frame - 40 - i * 14, fps, config: SPRING_SMOOTH});
          return <div key={i} style={{fontFamily: FONT_NEU.display, fontSize: height * (i === emphasis ? 0.10 : 0.07), fontWeight: 400, color: i === emphasis ? NEU_RED : '#fff', backgroundColor: 'rgba(0,0,0,0.85)', padding: `${height * 0.012}px ${width * 0.024}px`, opacity: s, transform: `translateY(${(1 - s) * 14}px)`}}>{ln}</div>;
        })}
      </div>
    </AbsoluteFill>
  );
};
