import React from 'react';
import {AbsoluteFill, Audio, Img, OffthreadVideo, Sequence, staticFile, useCurrentFrame, useVideoConfig, interpolate, spring} from 'remotion';
import {z} from 'zod';
import {NEU, NEU_RED, FONT_NEU} from '../tokens/neu';
import {SPRING_SMOOTH} from '../tokens/vox';
import {useLato} from '../tokens/lato';

/**
 * SeisQA — one extracted Q&A clip (seis-extract): PART A the question, typed onto a SEIS page while
 * Bella (Kokoro af_bella, the interviewer's voice) asks it; PART B the alum's answer — the interview
 * segment full-frame with a slow reframe, a lower third naming the PROGRAM explicitly (name · program ·
 * grad year · title · company), and burned captions from the transcript's word timings.
 * NEU brand throughout; everything timed from the audio.
 */
export const seisQASchema = z.object({
  question: z.string().default('What did the program change for you?'),
  questionAudio: z.string().default(''),   // public/ path to Bella's mp3
  questionFrames: z.number().default(90),
  clip: z.string().default(''),            // public/ path to the pre-cut answer mp4
  clipFrames: z.number().default(300),
  name: z.string().default('Alum Name'),
  program: z.string().default('MS Information Systems · SEIS'),
  gradYear: z.string().default(''),
  title: z.string().default(''),
  company: z.string().default(''),
  captions: z.array(z.object({t: z.string(), s: z.number(), e: z.number()})).default([]), // clip-local frames
  logo: z.string().default('seis/seis-button-logo.jpg'),        // the SEIS tile 'button' — top-right on every frame
  lockup: z.string().default('seis/seis-logo.png'),             // the SEIS lockup — under the name in the lower third
});
export type SeisQAProps = z.infer<typeof seisQASchema>;

const Question: React.FC<SeisQAProps> = ({question, questionAudio, questionFrames, logo}) => {
  const frame = useCurrentFrame(); const {fps, width, height} = useVideoConfig();
  const chars = Math.floor(interpolate(frame, [8, Math.max(20, questionFrames - 18)], [0, question.length], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}));
  const ruleIn = spring({frame, fps, config: SPRING_SMOOTH});
  const out = interpolate(frame, [questionFrames - 8, questionFrames], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{backgroundColor: NEU.CREAM, opacity: out}}>
      {questionAudio && <Audio src={staticFile(questionAudio)} />}
      <div style={{position: 'absolute', left: width * 0.07, top: height * 0.07, fontFamily: FONT_NEU.display, fontSize: height * 0.024, letterSpacing: 1.5, textTransform: 'uppercase', color: NEU.SLATE}}>SEIS · Alumni · Software Engineering and Information Systems</div>
      <Img src={staticFile(logo)} style={{position: 'absolute', right: width * 0.06, top: height * 0.05, height: height * 0.11}} />
      <div style={{position: 'absolute', left: width * 0.07, top: height * 0.30, width: width * 0.12 * ruleIn, height: Math.max(4, height * 0.007), backgroundColor: NEU_RED}} />
      <div style={{position: 'absolute', left: width * 0.07, top: height * 0.36, width: width * 0.86, fontFamily: FONT_NEU.display, fontSize: height * 0.085, fontWeight: 400, lineHeight: 1.15, color: NEU.INK}}>
        {question.slice(0, chars)}<span style={{color: NEU_RED, opacity: frame % 20 < 10 ? 1 : 0}}>|</span>
      </div>
    </AbsoluteFill>
  );
};

const Answer: React.FC<SeisQAProps> = ({clip, clipFrames, name, program, gradYear, title, company, captions, logo, lockup}) => {
  const frame = useCurrentFrame(); const {fps, width, height} = useVideoConfig();
  const zoom = interpolate(frame, [0, clipFrames], [1.0, 1.06], {extrapolateRight: 'clamp'});
  const lt = spring({frame: frame - 10, fps, config: SPRING_SMOOTH});
  const ltOut = interpolate(frame, [fps * 5.5, fps * 6.5], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const cap = captions.find((c) => frame >= c.s && frame < c.e);
  const fadeIn = interpolate(frame, [0, 8], [0, 1], {extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{backgroundColor: '#000', opacity: fadeIn}}>
      {clip && <OffthreadVideo src={staticFile(clip)} style={{width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${zoom})`}} />}
      {/* lower third — the PROGRAM is named, not just the university */}
      <div style={{position: 'absolute', left: width * 0.05, bottom: height * 0.20, opacity: lt * ltOut, transform: `translateX(${(1 - lt) * -30}px)`}}>
        <div style={{display: 'inline-block', backgroundColor: 'rgba(255,255,255,0.96)', borderLeft: `${Math.max(6, width * 0.005)}px solid ${NEU_RED}`, padding: `${height * 0.012}px ${width * 0.018}px`}}>
          <div style={{fontFamily: FONT_NEU.display, fontSize: height * 0.046, color: NEU.INK, lineHeight: 1.1}}>{name}</div>
          <div style={{fontFamily: FONT_NEU.display, fontSize: height * 0.026, color: NEU_RED, marginTop: height * 0.006}}>{program}{gradYear ? ` · ${gradYear}` : ''}</div>
          {(title || company) && <div style={{fontFamily: FONT_NEU.display, fontSize: height * 0.026, color: NEU.SLATE, marginTop: height * 0.004}}>{[title, company].filter(Boolean).join(' · ')}</div>}
          <Img src={staticFile(lockup)} style={{display: 'block', height: height * 0.055, marginTop: height * 0.012}} />
        </div>
      </div>
      {/* captions, burned */}
      {cap && <div style={{position: 'absolute', left: 0, right: 0, bottom: height * 0.06, textAlign: 'center'}}>
        <span style={{fontFamily: FONT_NEU.display, fontSize: height * 0.044, color: '#fff', backgroundColor: 'rgba(0,0,0,0.62)', padding: `${height * 0.008}px ${width * 0.014}px`, lineHeight: 1.35}}>{cap.t}</span>
      </div>}
      <Img src={staticFile(logo)} style={{position: 'absolute', right: width * 0.05, top: height * 0.05, height: height * 0.11}} />
    </AbsoluteFill>
  );
};

export const SeisQA: React.FC<SeisQAProps> = (props) => {
  useLato();
  return (
    <AbsoluteFill style={{backgroundColor: '#000'}}>
      <Sequence from={0} durationInFrames={props.questionFrames}><Question {...props} /></Sequence>
      <Sequence from={props.questionFrames} durationInFrames={props.clipFrames}><Answer {...props} /></Sequence>
    </AbsoluteFill>
  );
};
