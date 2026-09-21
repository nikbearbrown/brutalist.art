import React from 'react';
import {AbsoluteFill, Audio, Img, staticFile, useCurrentFrame, useVideoConfig, interpolate, spring} from 'remotion';
import {z} from 'zod';
import {NEU, NEU_RED, FONT_NEU} from '../tokens/neu';
import {SPRING_SMOOTH} from '../tokens/vox';
import {useLato} from '../tokens/lato';
import {SEIS_READ} from '../data/seisReadAlong';
import {SEIS_TRIBUTE} from '../data/seisTribute';

/**
 * SeisReadAlong — "SEIS, Oh the Things That We Do" as a Seuss-style read-along: the poem's
 * lines on the page, each word lit NU red the moment Bear speaks it (forced alignment of the
 * VO), and the thing being named shown beside the words — a showcase card, Ashlesha's photo,
 * the wall of faces, the mark. White page, Lato regular, red as the one accent. Page turns
 * follow pages.json; every timing comes from lyrics.json, never by hand.
 */
export const seisReadAlongSchema = z.object({});

const Words: React.FC<{page: (typeof SEIS_READ.pages)[number]; frame: number; width: number; height: number; wide: boolean}> = ({page, frame, width, height, wide}) => {
  const size = height * (page.lines.length > 6 ? 0.042 : page.lines.length > 4 ? 0.05 : 0.06);
  return (
    <div style={{position: 'absolute', left: width * 0.07, top: height * 0.16, width: wide ? width * 0.86 : width * 0.50, display: 'flex', flexDirection: 'column', gap: size * 0.45}}>
      {page.lines.map((ln, i) => (
        <div key={i} style={{fontFamily: FONT_NEU.display, fontSize: size, lineHeight: 1.2, color: NEU.INK, display: 'flex', flexWrap: 'wrap', gap: `0 ${size * 0.28}px`}}>
          {ln.words.map((w, j) => {
            const sung = frame >= w.s; const cur = frame >= w.s && frame < w.e;
            return <span key={j} style={{position: 'relative', color: sung ? NEU.INK : '#8a8a8a', transition: 'none'}}>{w.t}
              <span style={{position: 'absolute', left: 0, bottom: -size * 0.06, height: Math.max(3, size * 0.07), width: cur ? `${interpolate(frame, [w.s, w.e], [0, 100], {extrapolateRight: 'clamp'})}%` : sung ? '100%' : '0%', backgroundColor: NEU_RED, opacity: sung ? 1 : 0}} />
            </span>;
          })}
        </div>
      ))}
    </div>
  );
};

const Side: React.FC<{page: (typeof SEIS_READ.pages)[number]; local: number; fps: number; width: number; height: number}> = ({page, local, fps, width, height}) => {
  const p = page.props; const inn = spring({frame: local - 4, fps, config: SPRING_SMOOTH});
  const X = width * 0.60, W = width * 0.33;
  if (page.kind === 'showcase' || page.kind === 'photo') {
    return (
      <div style={{position: 'absolute', left: X, top: height * 0.16, width: W, opacity: inn, transform: `translateY(${(1 - inn) * 14}px)`}}>
        {page.kind === 'photo' && p.photo && <div style={{width: W, height: W * 9 / 16, overflow: 'hidden', border: `1px solid ${NEU.HAIRLINE}`, marginBottom: height * 0.03}}><Img src={staticFile(p.photo)} style={{width: '100%', height: '100%', objectFit: 'cover'}} /></div>}
        <div style={{width: width * 0.06, height: Math.max(4, height * 0.006), backgroundColor: NEU_RED, marginBottom: height * 0.02}} />
        <div style={{fontFamily: FONT_NEU.display, fontSize: height * 0.05, color: NEU.INK, lineHeight: 1.1}}>{p.name}</div>
        <div style={{fontFamily: FONT_NEU.display, fontSize: height * 0.044, color: NEU_RED, marginTop: height * 0.02, lineHeight: 1.1}}>{p.project}</div>
        <div style={{fontFamily: FONT_NEU.display, fontSize: height * 0.028, color: NEU.SLATE, marginTop: height * 0.02, lineHeight: 1.3}}>{p.line}</div>
      </div>
    );
  }
  if (page.kind === 'mark') {
    return (
      <div style={{position: 'absolute', left: X, top: height * 0.22, width: W, display: 'flex', flexDirection: 'column', alignItems: 'center', opacity: inn}}>
        {p.logo && <Img src={staticFile(p.logo)} style={{width: W * 0.8}} />}
        {p.caption && <div style={{fontFamily: FONT_NEU.display, fontSize: height * 0.034, color: NEU.SLATE, marginTop: height * 0.04, textAlign: 'center'}}>{p.caption}</div>}
      </div>
    );
  }
  return null;
};

export const SeisReadAlong: React.FC = () => {
  useLato();
  const frame = useCurrentFrame(); const {fps, width, height} = useVideoConfig();
  const d = SEIS_READ;
  const page = d.pages.find((p) => frame >= p.start && frame < p.end) || d.pages[d.pages.length - 1];
  const local = frame - page.start;
  const wall = page.kind === 'wall';
  const cols = 14, faces = SEIS_TRIBUTE.faces, rows = Math.ceil(faces.length / cols);
  const tw = (width * 0.86) / cols, th = (height * 0.86) / rows;
  return (
    <AbsoluteFill style={{backgroundColor: wall ? '#000' : NEU.CREAM, overflow: 'hidden'}}>
      {d.audio && <Audio src={staticFile(d.audio)} />}
      {wall && faces.map((f, i) => { const s = spring({frame: local - (i % cols) * 1.2 - Math.floor(i / cols) * 3, fps, config: SPRING_SMOOTH});
        return <div key={i} style={{position: 'absolute', left: width * 0.07 + (i % cols) * tw, top: height * 0.07 + Math.floor(i / cols) * th, width: tw, height: th, overflow: 'hidden', opacity: s * 0.35}}><Img src={staticFile(f.file)} style={{width: '100%', height: '100%', objectFit: 'cover'}} /></div>; })}
      {!wall && <div style={{position: 'absolute', left: width * 0.07, top: height * 0.09, width: width * 0.06, height: Math.max(4, height * 0.006), backgroundColor: NEU_RED}} />}
      {page.props.caption && !wall && page.kind === 'text' && <div style={{position: 'absolute', right: width * 0.07, top: height * 0.085, fontFamily: FONT_NEU.display, fontSize: height * 0.024, letterSpacing: 1.5, textTransform: 'uppercase', color: NEU.SLATE}}>{page.props.caption}</div>}
      <div style={wall ? {position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center'} : {}}>
        {wall ? (
          <div style={{backgroundColor: 'rgba(0,0,0,0.8)', padding: `${height * 0.03}px ${width * 0.04}px`, maxWidth: width * 0.8}}>
            {page.lines.map((ln, i) => <div key={i} style={{fontFamily: FONT_NEU.display, fontSize: height * 0.06, color: '#fff', lineHeight: 1.25, display: 'flex', flexWrap: 'wrap', gap: `0 ${height * 0.017}px`}}>
              {ln.words.map((w, j) => <span key={j} style={{color: frame >= w.s ? '#fff' : 'rgba(255,255,255,0.45)', borderBottom: frame >= w.s ? `4px solid ${NEU_RED}` : '4px solid transparent'}}>{w.t}</span>)}
            </div>)}
          </div>
        ) : <Words page={page} frame={frame} width={width} height={height} wide={page.kind === 'text'} />}
      </div>
      {!wall && <Side page={page} local={local} fps={fps} width={width} height={height} />}
    </AbsoluteFill>
  );
};
