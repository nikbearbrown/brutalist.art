import React from 'react';
import {AbsoluteFill, Img, staticFile, useCurrentFrame, useVideoConfig, spring, interpolate} from 'remotion';
import {z} from 'zod';
import {NEU, NEU_RED, FONT_NEU} from '../tokens/neu';
import {SPRING_SMOOTH} from '../tokens/vox';
import {useLato} from '../tokens/lato';

/**
 * SeisSpotlightOpen — B00 of a SEIS spotlight reel (brands/seis.md).
 * NEU brand law: white ground, Lato regular-weight headings, sentence case,
 * NU Red as the ONE brand accent (the rule that draws in). No logo is drawn —
 * the unit name is set as type until the official lockup is supplied.
 * `photo` is the article's hero image as COE published it (public/seis/<slug>.*),
 * optional — the card composes without it.
 */
export const seisSpotlightOpenSchema = z.object({
  eyebrow: z.string().default('Student spotlight'),
  name: z.string().default('Student Name'),
  program: z.string().default('MS Information Systems'),
  term: z.string().default(''),
  unit: z.string().default('Software Engineering and Information Systems'),
  school: z.string().default('Northeastern University · College of Engineering'),
  photo: z.string().default(''),
  photoCredit: z.string().default(''),
  logo: z.string().default(''), // official mark (logos/seis → public/seis); text fallback when empty
});
export type SeisSpotlightOpenProps = z.infer<typeof seisSpotlightOpenSchema>;

export const SeisSpotlightOpen: React.FC<SeisSpotlightOpenProps> = ({
  eyebrow, name, program, term, unit, school, photo, photoCredit, logo,
}) => {
  useLato();
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const PAD = width * 0.08;
  const hasPhoto = photo.length > 0;
  const textW = hasPhoto ? width * 0.50 : width * 0.84;

  const schoolIn = spring({frame, fps, config: SPRING_SMOOTH});
  const ruleIn = spring({frame: frame - 6, fps, config: SPRING_SMOOTH});
  const eyebrowIn = spring({frame: frame - 12, fps, config: SPRING_SMOOTH});
  const nameIn = spring({frame: frame - 18, fps, config: SPRING_SMOOTH});
  const progIn = spring({frame: frame - 26, fps, config: SPRING_SMOOTH});
  const photoIn = spring({frame: frame - 10, fps, config: SPRING_SMOOTH});
  const photoScale = interpolate(frame, [0, 300], [1.0, 1.04], {extrapolateRight: 'clamp'});

  return (
    <AbsoluteFill style={{backgroundColor: NEU.CREAM, overflow: 'hidden'}}>
      {/* school line */}
      <div style={{
        position: 'absolute', left: PAD, top: height * 0.09,
        fontFamily: FONT_NEU.display, fontSize: height * 0.022, fontWeight: 400,
        letterSpacing: 1.5, textTransform: 'uppercase', color: NEU.INK,
        opacity: schoolIn,
      }}>{school}</div>

      {/* the ONE red — a rule that draws in */}
      <div style={{
        position: 'absolute', left: PAD, top: height * 0.145,
        width: width * 0.12 * ruleIn, height: Math.max(4, height * 0.006),
        backgroundColor: NEU_RED,
      }} />

      {/* eyebrow */}
      <div style={{
        position: 'absolute', left: PAD, top: height * 0.30, width: textW,
        fontFamily: FONT_NEU.display, fontSize: height * 0.030, fontWeight: 400,
        color: NEU.SLATE, opacity: eyebrowIn,
        transform: `translateY(${(1 - eyebrowIn) * 10}px)`,
      }}>{eyebrow}</div>

      {/* name — regular weight per brand law */}
      <div style={{
        position: 'absolute', left: PAD, top: height * 0.35, width: textW,
        fontFamily: FONT_NEU.display, fontSize: height * 0.12, fontWeight: 400,
        lineHeight: 1.05, color: NEU.INK, opacity: nameIn,
        transform: `translateY(${(1 - nameIn) * 18}px)`,
      }}>{name}</div>

      {/* program · term */}
      <div style={{
        position: 'absolute', left: PAD, top: height * 0.64, width: textW,
        fontFamily: FONT_NEU.display, fontSize: height * 0.044, fontWeight: 400,
        color: NEU.INK, opacity: progIn,
        transform: `translateY(${(1 - progIn) * 10}px)`,
      }}>{program}{term ? ` · ${term}` : ''}</div>

      {logo && (
        <Img src={staticFile(logo)} style={{position: 'absolute', right: PAD, top: height * 0.07, height: height * 0.09, opacity: schoolIn}} />
      )}
      {/* unit line, bottom-left */}
      <div style={{
        position: 'absolute', left: PAD, bottom: height * 0.09, width: textW,
        fontFamily: FONT_NEU.display, fontSize: height * 0.024, fontWeight: 400,
        color: NEU.SLATE, opacity: progIn,
      }}>{unit}</div>

      {/* photo, as published, right column */}
      {hasPhoto && (
        <div style={{
          position: 'absolute', right: PAD, top: height * 0.22,
          width: width * 0.34, height: height * 0.66, overflow: 'hidden',
          border: `1px solid ${NEU.HAIRLINE}`, opacity: photoIn,
        }}>
          <Img src={staticFile(photo)} style={{
            width: '100%', height: '100%', objectFit: 'cover',
            transform: `scale(${photoScale})`,
          }} />
        </div>
      )}
      {hasPhoto && photoCredit && (
        <div style={{
          position: 'absolute', right: PAD, top: height * 0.895, width: width * 0.34,
          fontFamily: FONT_NEU.display, fontSize: height * 0.017, color: NEU.SLATE,
          textAlign: 'right', opacity: photoIn,
        }}>{photoCredit}</div>
      )}
    </AbsoluteFill>
  );
};
