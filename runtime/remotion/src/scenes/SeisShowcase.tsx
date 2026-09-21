import React from 'react';
import {AbsoluteFill, Img, staticFile, useCurrentFrame, useVideoConfig, spring, interpolate} from 'remotion';
import {z} from 'zod';
import {NEU, NEU_RED, FONT_NEU} from '../tokens/neu';
import {SPRING_SMOOTH} from '../tokens/vox';
import {useLato} from '../tokens/lato';

/**
 * SeisShowcase — the MGEN-Awards grammar on the SEIS skin: NAME (spoken every time) · PROJECT ·
 * ONE LINE, hard-cut, big type, one NU-red rule. `photo` (optional, public/ path) fills the right
 * third as published. `index` ("3 / 9") is the small counter that gives the sequence momentum.
 */
export const seisShowcaseSchema = z.object({
  eyebrow: z.string().default('SEIS · student work'),
  name: z.string().default('Student Name'),
  project: z.string().default('Project'),
  line: z.string().default('One line about the work.'),
  index: z.string().default(''),
  photo: z.string().default(''),
});
export type SeisShowcaseProps = z.infer<typeof seisShowcaseSchema>;

export const SeisShowcase: React.FC<SeisShowcaseProps> = ({eyebrow, name, project, line, index, photo}) => {
  useLato();
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const PAD = width * 0.07;
  const hasPhoto = photo.length > 0;
  const textW = hasPhoto ? width * 0.55 : width * 0.86;
  const ruleIn = spring({frame, fps, config: SPRING_SMOOTH});
  const nameIn = spring({frame: frame - 4, fps, config: SPRING_SMOOTH});
  const projIn = spring({frame: frame - 10, fps, config: SPRING_SMOOTH});
  const lineIn = spring({frame: frame - 16, fps, config: SPRING_SMOOTH});
  const zoom = interpolate(frame, [0, 300], [1.0, 1.05], {extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{backgroundColor: NEU.CREAM, overflow: 'hidden'}}>
      <div style={{position: 'absolute', left: PAD, top: height * 0.10, fontFamily: FONT_NEU.display, fontSize: height * 0.026, letterSpacing: 1.5, textTransform: 'uppercase', color: NEU.SLATE, opacity: ruleIn}}>{eyebrow}</div>
      {index && <div style={{position: 'absolute', right: PAD, top: height * 0.10, fontFamily: FONT_NEU.display, fontSize: height * 0.026, color: NEU.SLATE, opacity: ruleIn}}>{index}</div>}
      <div style={{position: 'absolute', left: PAD, top: height * 0.155, width: width * 0.14 * ruleIn, height: Math.max(4, height * 0.007), backgroundColor: NEU_RED}} />
      {/* name · project · line flow in a column so long titles never collide */}
      <div style={{position: 'absolute', left: PAD, top: height * 0.21, width: textW, height: height * 0.68, display: 'flex', flexDirection: 'column', justifyContent: 'space-between'}}>
        <div style={{fontFamily: FONT_NEU.display, fontSize: height * (name.length > 28 ? 0.08 : 0.11), fontWeight: 400, lineHeight: 1.05, color: NEU.INK, opacity: nameIn, transform: `translateY(${(1 - nameIn) * 16}px)`}}>{name}</div>
        <div style={{fontFamily: FONT_NEU.display, fontSize: height * (project.length > 36 ? 0.055 : 0.075), fontWeight: 400, lineHeight: 1.1, color: NEU_RED, opacity: projIn, transform: `translateY(${(1 - projIn) * 12}px)`}}>{project}</div>
        <div style={{fontFamily: FONT_NEU.display, fontSize: height * 0.05, fontWeight: 400, lineHeight: 1.25, color: NEU.INK, opacity: lineIn, transform: `translateY(${(1 - lineIn) * 10}px)`}}>{line}</div>
      </div>
      {hasPhoto && (
        <div style={{position: 'absolute', right: PAD, top: height * 0.22, width: width * 0.28, height: height * 0.64, overflow: 'hidden', border: `1px solid ${NEU.HAIRLINE}`, opacity: nameIn}}>
          <Img src={staticFile(photo)} style={{width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${zoom})`}} />
        </div>
      )}
    </AbsoluteFill>
  );
};
