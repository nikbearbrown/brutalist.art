import React from 'react';
import {AbsoluteFill, Audio, Img, staticFile, useCurrentFrame, useVideoConfig, interpolate, spring} from 'remotion';
import {z} from 'zod';
import {NEU_RED, FONT_NEU} from '../tokens/neu';
import {SPRING_SMOOTH} from '../tokens/vox';
import {useLato} from '../tokens/lato';
import {SEIS_TRIBUTE} from '../data/seisTribute';

/**
 * SeisTribute — "For the Unconquerable Souls": every SEIS spotlight student's face, one
 * after another, under Bear's adaptation of Invictus, with forced-aligned karaoke lyrics
 * center-bottom and the student's name top-left. Black ground (NU brand allows black),
 * Lato regular, NU red as the one emphasis (the karaoke underline + name rule). No
 * gradients (NEU law) — a flat scrim band sits behind the lyric for legibility.
 * Timeline: title → one face per slot until the final line → the wall of every face
 * under "You are the captain of your soul." → credit.
 */
export const seisTributeSchema = z.object({
  title: z.string().default('For the Unconquerable Souls'),
  dedication: z.string().default('for the international students of SEIS'),
  credit: z.string().default('adapted from Invictus — William Ernest Henley (1875) · music by Nik Bear Brown'),
  unit: z.string().default('Software Engineering and Information Systems · Northeastern University'),
  titleFrames: z.number().default(150),
  wallStart: z.number().default(3335), // frame the last line begins (from lyrics.json)
});
export type SeisTributeProps = z.infer<typeof seisTributeSchema>;

const WHITE = '#FFFFFF';
const DIM = 'rgba(255,255,255,0.45)';

export const SeisTribute: React.FC<SeisTributeProps> = ({title, dedication, credit, unit, titleFrames, wallStart}) => {
  useLato();
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const faces = SEIS_TRIBUTE.faces;
  const lines = SEIS_TRIBUTE.lines;
  const PAD = width * 0.05;

  // ── faces: evenly across [titleFrames, wallStart)
  const span = wallStart - titleFrames;
  const per = span / faces.length;
  const XF = 6; // crossfade frames
  const faceAt = (f: number) => Math.min(faces.length - 1, Math.max(0, Math.floor((f - titleFrames) / per)));
  const idx = faceAt(frame);
  const slotStart = titleFrames + idx * per;
  const local = frame - slotStart;

  // ── karaoke: current line + word progress
  const line = lines.find((l) => frame >= l.start - 8 && frame <= l.end + 12);

  const inTitle = frame < titleFrames;
  const inWall = frame >= wallStart;
  const titleOut = interpolate(frame, [titleFrames - 12, titleFrames], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const cols = 14, rows = Math.ceil(faces.length / cols);
  const tileW = width / cols, tileH = height / rows;

  return (
    <AbsoluteFill style={{backgroundColor: '#000000', overflow: 'hidden'}}>
      <Audio src={staticFile('seis-tribute/audio.wav')} />

      {/* ── one face per slot, cover + slow zoom, 6-frame crossfade */}
      {!inTitle && !inWall && [idx - 1, idx].map((i) => {
        if (i < 0 || i >= faces.length) return null;
        const s0 = titleFrames + i * per;
        const l = frame - s0;
        const zoom = interpolate(l, [0, per], [1.0, 1.07], {extrapolateRight: 'clamp'});
        const a = i === idx ? interpolate(l, [0, XF], [0, 1], {extrapolateRight: 'clamp'}) : interpolate(l, [per, per + XF], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
        return (
          <AbsoluteFill key={i} style={{opacity: a}}>
            <Img src={staticFile(faces[i].file)} style={{width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${zoom})`}} />
          </AbsoluteFill>
        );
      })}

      {/* ── name, top-left, with the red rule */}
      {!inTitle && !inWall && (
        <div style={{position: 'absolute', left: PAD, top: height * 0.06, opacity: interpolate(local, [2, 8], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})}}>
          <div style={{width: width * 0.04, height: Math.max(3, height * 0.005), backgroundColor: NEU_RED, marginBottom: height * 0.012}} />
          <div style={{fontFamily: FONT_NEU.display, fontSize: height * 0.040, fontWeight: 400, color: WHITE, backgroundColor: 'rgba(0,0,0,0.45)', padding: `${height * 0.006}px ${width * 0.008}px`, display: 'inline-block'}}>
            {faces[idx].name}
          </div>
        </div>
      )}

      {/* ── the wall: every face, staggered pop-in under the last line */}
      {inWall && faces.map((fc, i) => {
        const s = spring({frame: frame - wallStart - (i % cols) * 1.2 - Math.floor(i / cols) * 4, fps, config: SPRING_SMOOTH});
        return (
          <div key={i} style={{position: 'absolute', left: (i % cols) * tileW, top: Math.floor(i / cols) * tileH, width: tileW, height: tileH, overflow: 'hidden', opacity: s, transform: `scale(${0.85 + 0.15 * s})`}}>
            <Img src={staticFile(fc.file)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
          </div>
        );
      })}

      {/* ── title card */}
      {inTitle && (
        <AbsoluteFill style={{opacity: titleOut, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center'}}>
          <div style={{width: width * 0.06, height: Math.max(4, height * 0.006), backgroundColor: NEU_RED, marginBottom: height * 0.04, opacity: spring({frame, fps, config: SPRING_SMOOTH})}} />
          <div style={{fontFamily: FONT_NEU.display, fontSize: height * 0.10, fontWeight: 400, color: WHITE, textAlign: 'center', maxWidth: width * 0.86, opacity: spring({frame: frame - 6, fps, config: SPRING_SMOOTH})}}>{title}</div>
          <div style={{fontFamily: FONT_NEU.display, fontSize: height * 0.04, fontWeight: 400, color: DIM, marginTop: height * 0.03, opacity: spring({frame: frame - 18, fps, config: SPRING_SMOOTH})}}>{dedication}</div>
          <div style={{fontFamily: FONT_NEU.display, fontSize: height * 0.026, fontWeight: 400, color: DIM, marginTop: height * 0.06, opacity: spring({frame: frame - 30, fps, config: SPRING_SMOOTH})}}>{credit}</div>
        </AbsoluteFill>
      )}

      {/* ── karaoke, center-bottom: sung words white, coming words dim, the current word underlined red */}
      {line && (
        <div style={{position: 'absolute', left: 0, right: 0, bottom: height * 0.09, display: 'flex', justifyContent: 'center'}}>
          <div style={{backgroundColor: 'rgba(0,0,0,0.55)', padding: `${height * 0.014}px ${width * 0.022}px`, display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: `0 ${width * 0.011}px`, maxWidth: width * 0.9}}>
            {line.words.map((w, i) => {
              const sung = frame >= w.s; const current = frame >= w.s && frame < w.e;
              const prog = current ? interpolate(frame, [w.s, w.e], [0, 1], {extrapolateRight: 'clamp'}) : sung ? 1 : 0;
              return (
                <span key={i} style={{position: 'relative', fontFamily: FONT_NEU.display, fontSize: height * 0.052, fontWeight: 400, color: sung ? WHITE : DIM, lineHeight: 1.25}}>
                  {w.t}
                  <span style={{position: 'absolute', left: 0, bottom: 0, height: Math.max(3, height * 0.005), width: `${prog * 100}%`, backgroundColor: NEU_RED}} />
                </span>
              );
            })}
          </div>
        </div>
      )}

      {/* ── credit + unit after the last line */}
      {inWall && (
        <>
          <div style={{position: 'absolute', left: PAD, top: height * 0.06, fontFamily: FONT_NEU.display, fontSize: height * 0.03, color: WHITE, backgroundColor: 'rgba(0,0,0,0.5)', padding: `${height * 0.006}px ${width * 0.008}px`, opacity: interpolate(frame, [wallStart + 60, wallStart + 90], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})}}>{unit}</div>
          <div style={{position: 'absolute', left: 0, right: 0, bottom: height * 0.025, textAlign: 'center', fontFamily: FONT_NEU.display, fontSize: height * 0.024, color: WHITE, opacity: interpolate(frame, [durationInFrames - 240, durationInFrames - 200], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})}}>
            <span style={{backgroundColor: 'rgba(0,0,0,0.55)', padding: `${height * 0.006}px ${width * 0.012}px`}}>{credit}</span>
          </div>
        </>
      )}
    </AbsoluteFill>
  );
};
