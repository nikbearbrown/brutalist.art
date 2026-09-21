import React from 'react';
import {AbsoluteFill, Audio, Img, Sequence, staticFile, useCurrentFrame, useVideoConfig, interpolate, spring} from 'remotion';
import {z} from 'zod';
import {NEU_RED, FONT_NEU} from '../tokens/neu';
import {SPRING_SMOOTH} from '../tokens/vox';
import {useLato} from '../tokens/lato';
import {SEIS_ROLL} from '../data/seisStoriesRoll';

/**
 * SeisStoriesRoll — every SEIS spotlight student in the MGEN-Awards grammar: face full-frame (slow zoom),
 * NAME + PROGRAM top-left, the story's title as the one line bottom, Liam speaking the name and program
 * per beat (Kokoro mp3 per person; durations from mp3/timings.json are the clock). Open + wall + outro
 * bookends carry their own narration. Black ground, Lato, NU red as the one accent, flat scrims.
 */
export const seisStoriesRollSchema = z.object({
  title: z.string().default('Student Spotlights'),
  subtitle: z.string().default('112 stories · Software Engineering and Information Systems'),
});
export type SeisStoriesRollProps = z.infer<typeof seisStoriesRollSchema>;

const Beat: React.FC<{name: string; program: string; line: string; photo: string; dur: number}> = ({name, program, line, photo, dur}) => {
  const frame = useCurrentFrame(); const {width, height} = useVideoConfig();
  const zoom = interpolate(frame, [0, dur], [1.0, 1.06], {extrapolateRight: 'clamp'});
  const a = interpolate(frame, [0, 5, dur - 5, dur], [0, 1, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const inn = interpolate(frame, [3, 10], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{opacity: a}}>
      <Img src={staticFile(photo)} style={{width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${zoom})`}} />
      <div style={{position: 'absolute', left: width * 0.05, top: height * 0.06, opacity: inn}}>
        <div style={{width: width * 0.04, height: Math.max(3, height * 0.005), backgroundColor: NEU_RED, marginBottom: height * 0.012}} />
        <div style={{fontFamily: FONT_NEU.display, fontSize: height * 0.052, color: '#fff', backgroundColor: 'rgba(0,0,0,0.5)', padding: `${height * 0.006}px ${width * 0.01}px`, display: 'inline-block'}}>{name}</div>
        <div style={{marginTop: height * 0.008}}><span style={{fontFamily: FONT_NEU.display, fontSize: height * 0.03, color: '#fff', backgroundColor: 'rgba(0,0,0,0.5)', padding: `${height * 0.004}px ${width * 0.01}px`}}>{program}</span></div>
      </div>
      <div style={{position: 'absolute', left: 0, right: 0, bottom: height * 0.08, textAlign: 'center', opacity: inn}}>
        <span style={{fontFamily: FONT_NEU.display, fontSize: height * 0.044, color: '#fff', backgroundColor: 'rgba(0,0,0,0.55)', padding: `${height * 0.01}px ${width * 0.02}px`}}>{line}</span>
      </div>
    </AbsoluteFill>
  );
};

export const SeisStoriesRoll: React.FC<SeisStoriesRollProps> = ({title, subtitle}) => {
  useLato();
  const frame = useCurrentFrame(); const {fps, width, height} = useVideoConfig();
  const d = SEIS_ROLL; let t = 0;
  const openDur = d.open.frames, outDur = d.outro.frames;
  const seqs: React.ReactNode[] = [];
  seqs.push(<Sequence key="open" from={0} durationInFrames={openDur}><Audio src={staticFile(d.open.mp3)} />
    <AbsoluteFill style={{backgroundColor: '#000', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center'}}>
      <div style={{width: width * 0.06, height: Math.max(4, height * 0.006), backgroundColor: NEU_RED, marginBottom: height * 0.04, opacity: spring({frame, fps, config: SPRING_SMOOTH})}} />
      <div style={{fontFamily: FONT_NEU.display, fontSize: height * 0.11, color: '#fff', opacity: spring({frame: frame - 6, fps, config: SPRING_SMOOTH})}}>{title}</div>
      <div style={{fontFamily: FONT_NEU.display, fontSize: height * 0.036, color: 'rgba(255,255,255,0.6)', marginTop: height * 0.03, opacity: spring({frame: frame - 18, fps, config: SPRING_SMOOTH})}}>{subtitle}</div>
    </AbsoluteFill></Sequence>);
  t = openDur;
  d.people.forEach((p, i) => {
    seqs.push(<Sequence key={i} from={t} durationInFrames={p.frames}><Audio src={staticFile(p.mp3)} /><Beat name={p.name} program={p.program} line={p.line} photo={p.photo} dur={p.frames} /></Sequence>);
    t += p.frames;
  });
  const cols = 14, rows = Math.ceil(d.people.length / cols); const tw = width / cols, th = height / rows;
  seqs.push(<Sequence key="outro" from={t} durationInFrames={outDur}><Audio src={staticFile(d.outro.mp3)} />
    <AbsoluteFill style={{backgroundColor: '#000'}}>
      {d.people.map((p, i) => { const s = spring({frame: frame - t - (i % cols) * 1.1 - Math.floor(i / cols) * 3, fps, config: SPRING_SMOOTH});
        return <div key={i} style={{position: 'absolute', left: (i % cols) * tw, top: Math.floor(i / cols) * th, width: tw, height: th, overflow: 'hidden', opacity: s}}><Img src={staticFile(p.photo)} style={{width: '100%', height: '100%', objectFit: 'cover'}} /></div>; })}
      <div style={{position: 'absolute', left: 0, right: 0, bottom: height * 0.06, textAlign: 'center'}}><span style={{fontFamily: FONT_NEU.display, fontSize: height * 0.04, color: '#fff', backgroundColor: 'rgba(0,0,0,0.6)', padding: `${height * 0.01}px ${width * 0.02}px`}}>{d.outro.line}</span></div>
    </AbsoluteFill></Sequence>);
  return <AbsoluteFill style={{backgroundColor: '#000'}}>{seqs}</AbsoluteFill>;
};
