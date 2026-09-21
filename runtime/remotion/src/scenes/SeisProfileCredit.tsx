import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig, spring} from 'remotion';
import {z} from 'zod';
import {NEU, NEU_RED, FONT_NEU} from '../tokens/neu';
import {SPRING_SMOOTH} from '../tokens/vox';
import {useLato} from '../tokens/lato';

/**
 * SeisProfileCredit — the PERSON CREDIT card (BHTF) required by the profile
 * modifier: name, program/role, public links VERBATIM from the article (never
 * invented — empty array when the article gives none), and the article credit
 * (URL · date · author when known). This is the handoff beat on the seis skin:
 * "read the full story" replaces YOUR TURN.
 */
export const seisProfileCreditSchema = z.object({
  name: z.string().default('Student Name'),
  role: z.string().default('MS Information Systems'),
  links: z.array(z.string()).default([]),
  storyUrl: z.string().default(''),
  storyDate: z.string().default(''),
  storyAuthor: z.string().default(''),
});
export type SeisProfileCreditProps = z.infer<typeof seisProfileCreditSchema>;

export const SeisProfileCredit: React.FC<SeisProfileCreditProps> = ({
  name, role, links, storyUrl, storyDate, storyAuthor,
}) => {
  useLato();
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const PAD = width * 0.10;
  const nameIn = spring({frame, fps, config: SPRING_SMOOTH});
  const ruleIn = spring({frame: frame - 6, fps, config: SPRING_SMOOTH});
  const storyIn = spring({frame: frame - 14 - links.length * 8, fps, config: SPRING_SMOOTH});
  const credit = [storyUrl.replace(/^https?:\/\//, ''), storyDate, storyAuthor].filter(Boolean).join(' · ');

  return (
    <AbsoluteFill style={{backgroundColor: NEU.CREAM, overflow: 'hidden'}}>
      <div style={{
        position: 'absolute', left: PAD, top: height * 0.18,
        fontFamily: FONT_NEU.display, fontSize: height * 0.10, fontWeight: 400,
        color: NEU.INK, opacity: nameIn, transform: `translateY(${(1 - nameIn) * 16}px)`,
      }}>{name}</div>
      <div style={{
        position: 'absolute', left: PAD, top: height * 0.31,
        fontFamily: FONT_NEU.display, fontSize: height * 0.042, fontWeight: 400,
        color: NEU.SLATE, opacity: nameIn,
      }}>{role}</div>
      <div style={{
        position: 'absolute', left: PAD, top: height * 0.37,
        width: width * 0.10 * ruleIn, height: Math.max(4, height * 0.006), backgroundColor: NEU_RED,
      }} />
      <div style={{position: 'absolute', left: PAD, top: height * 0.43, display: 'flex', flexDirection: 'column', gap: height * 0.018}}>
        {links.map((l, i) => {
          const s = spring({frame: frame - 12 - i * 8, fps, config: SPRING_SMOOTH});
          return (
            <div key={i} style={{
              fontFamily: FONT_NEU.mono, fontSize: height * 0.036, color: NEU.INK,
              opacity: s, transform: `translateY(${(1 - s) * 10}px)`,
            }}>{l}</div>
          );
        })}
      </div>
      <div style={{
        position: 'absolute', left: PAD, right: PAD, bottom: height * 0.10,
        fontFamily: FONT_NEU.display, fontSize: height * 0.034, fontWeight: 400,
        color: NEU.SLATE, opacity: storyIn,
      }}>
        <div style={{color: NEU.INK, marginBottom: height * 0.008}}>Read the full story</div>
        <div>{credit}</div>
      </div>
    </AbsoluteFill>
  );
};
