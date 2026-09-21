import React from 'react';
import {AbsoluteFill, Img, staticFile, useCurrentFrame, useVideoConfig, interpolate, spring, Easing, random} from 'remotion';
import {z} from 'zod';
import {NEU, NEU_RED, FONT_NEU} from '../tokens/neu';
import {useLato} from '../tokens/lato';

/**
 * SeisLogoTechnique — ONE motion technique per beat, applied to a RASTER mark (PNG/JPG), on the
 * NEU page: technique name Title Case in Lato with the one red underline, the mark performing the
 * move. The "Logo, In Motion" showcase grammar (H / Bear Brown / Musinique showcases), made
 * parametric: `technique` + `logo` + `label`. Every beat is motion, never a slide.
 */
export const seisLogoTechniqueSchema = z.object({
  technique: z.enum(['spring-entrance', 'overshoot-spring', 'mask-reveal', 'scale-zoom', 'rotation', 'skew-shear', 'opacity-through-blur', 'color-treatment',
    'kinetic-grid', 'glitch-slices', 'trail-echo', 'noise-wobble', 'elastic-physics', 'card-flip', 'shadow-play', 'tile-assemble', 'exit-family']).default('spring-entrance'),
  logo: z.string().default('seis/seis-logo.png'),
  label: z.string().default('Spring Entrance'),
  index: z.string().default(''),
  markWidth: z.number().default(0.46),   // fraction of frame width
  square: z.boolean().default(false),    // the button is 1:1; the lockup is wide
});
export type SeisLogoTechniqueProps = z.infer<typeof seisLogoTechniqueSchema>;

const Label: React.FC<{label: string; index: string}> = ({label, index}) => {
  const frame = useCurrentFrame(); const {fps, width, height} = useVideoConfig();
  const s = spring({frame, fps, config: {damping: 200}});
  return (<>
    <div style={{position: 'absolute', left: width * 0.07, top: height * 0.07, fontFamily: FONT_NEU.display, fontSize: height * 0.022, letterSpacing: 1.5, textTransform: 'uppercase', color: NEU.SLATE, opacity: s}}>SEIS · Logo, In Motion</div>
    {index && <div style={{position: 'absolute', right: width * 0.07, top: height * 0.07, fontFamily: FONT_NEU.display, fontSize: height * 0.022, color: NEU.SLATE, opacity: s}}>{index}</div>}
    <div style={{position: 'absolute', left: width * 0.07, bottom: height * 0.10, opacity: s}}>
      <div style={{fontFamily: FONT_NEU.display, fontSize: height * 0.056, color: NEU.INK}}>{label}</div>
      <div style={{width: width * 0.10 * s, height: Math.max(4, height * 0.006), backgroundColor: NEU_RED, marginTop: height * 0.012}} />
    </div>
  </>);
};

export const SeisLogoTechnique: React.FC<SeisLogoTechniqueProps> = ({technique, logo, label, index, markWidth, square}) => {
  useLato();
  const frame = useCurrentFrame(); const {fps, width, height, durationInFrames} = useVideoConfig();
  const W = width * markWidth; const H = square ? W : W * 149 / 463; const cx = width / 2 - W / 2, cy = height * 0.44 - H / 2;
  const base: React.CSSProperties = {position: 'absolute', left: cx, top: cy, width: W, height: H, objectFit: 'contain'};
  const img = (style: React.CSSProperties = {}, key?: React.Key) => <Img key={key} src={staticFile(logo)} style={{...base, ...style}} />;
  const t = frame / fps; const clamp = (v: number, a = 0, b = 1) => Math.min(b, Math.max(a, v));
  let mark: React.ReactNode = null;
  switch (technique) {
    case 'spring-entrance': { const s = spring({frame: frame - 6, fps, config: {damping: 14, stiffness: 120}}); mark = img({transform: `scale(${s})`, opacity: clamp(s * 1.5)}); break; }
    case 'overshoot-spring': { const s = spring({frame: frame - 6, fps, config: {damping: 6, stiffness: 160, mass: 0.8}}); const sq = 1 + (1 - clamp(s)) * 0.25;
      mark = img({transform: `scale(${s * sq}, ${s / sq})`, transformOrigin: '50% 100%', opacity: clamp(s * 2)}); break; }
    case 'mask-reveal': { const wipe = interpolate(frame, [4, fps * 1.4], [0, 100], {extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic)});
      const iris = interpolate(frame, [fps * 2.6, fps * 4], [0, 75], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
      mark = frame < fps * 2.4 ? img({clipPath: `inset(0 ${100 - wipe}% 0 0)`}) : img({clipPath: `circle(${iris}% at 50% 50%)`}); break; }
    case 'scale-zoom': { const lin = interpolate(frame, [0, fps * 2], [8, 1], {extrapolateRight: 'clamp'}); const bez = interpolate(frame, [fps * 2.6, fps * 4.6], [8, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.exp)});
      const s = frame < fps * 2.4 ? lin : bez; mark = <>{img({transform: `scale(${s})`, opacity: frame < fps * 2.4 || frame > fps * 2.6 ? 1 : 0})}
      <div style={{position: 'absolute', right: width * 0.07, bottom: height * 0.10, fontFamily: FONT_NEU.display, fontSize: height * 0.028, color: NEU.SLATE}}>{frame < fps * 2.4 ? 'linear' : 'bezier out'}</div></>; break; }
    case 'rotation': { const s = spring({frame: frame - 4, fps, config: {damping: 12}}); const rot = interpolate(s, [0, 1], [-540, 0]) + (frame > fps * 2.5 ? Math.sin((frame - fps * 2.5) / 18) * 6 : 0);  // settle, then a ±6° sway — a wide mark can't turn continuously inside title-safe
      mark = img({transform: `rotate(${rot}deg) scale(${clamp(s)})`}); break; }
    case 'skew-shear': { const lean = interpolate(frame, [0, fps * 0.8, fps * 1.6, fps * 2.6], [-28, 14, -6, 0], {extrapolateRight: 'clamp', easing: Easing.inOut(Easing.cubic)});
      const x = interpolate(frame, [0, fps * 0.8], [-width * 0.4, 0], {extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic)}); mark = img({transform: `translateX(${x}px) skewX(${lean}deg)`}); break; }
    case 'opacity-through-blur': { const p = interpolate(frame, [0, fps * 1.8], [0, 1], {extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic)}); mark = img({opacity: p, filter: `blur(${(1 - p) * 40}px)`, transform: `scale(${0.9 + p * 0.1})`}); break; }
    case 'color-treatment': { const p = interpolate(frame, [fps * 0.5, fps * 2, fps * 3.5], [0, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
      mark = <>{img({})}<div style={{...base, backgroundColor: NEU_RED, opacity: p * 0.85, mixBlendMode: 'screen', WebkitMaskImage: `url(${staticFile(logo)})`, maskImage: `url(${staticFile(logo)})`, WebkitMaskSize: 'contain', maskSize: 'contain', WebkitMaskRepeat: 'no-repeat', maskRepeat: 'no-repeat', WebkitMaskPosition: 'center', maskPosition: 'center'}} />
      <div style={{position: 'absolute', right: width * 0.07, bottom: height * 0.10, fontFamily: FONT_NEU.display, fontSize: height * 0.028, color: NEU.SLATE}}>a treatment, not brand law</div></>; break; }
    case 'kinetic-grid': { const cols = square ? 6 : 3, rows = square ? 3 : 5; const X0 = width * 0.06, Y0 = height * 0.06; const tw = (width * 0.88) / cols, th = (height * 0.70) / rows; const items = [];  // inset inside title-safe, above the label band
      for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) { const i = r * cols + c; const s = spring({frame: frame - i * 3, fps, config: {damping: 10}}); const rip = Math.sin(frame / 9 - (r + c) * 0.7) * 0.05;
        items.push(<Img key={i} src={staticFile(logo)} style={{position: 'absolute', left: X0 + c * tw + tw * 0.08, top: Y0 + r * th + th * 0.12, width: tw * 0.84, height: th * 0.76, objectFit: 'contain', transform: `scale(${clamp(s) * (1 + rip)})`, opacity: clamp(s) * 0.9}} />); }
      mark = <>{items}</>; break; }
    case 'glitch-slices': { const on = frame > fps * 1.2 && frame < fps * 1.2 + 10 || frame > fps * 2.8 && frame < fps * 2.8 + 8; const n = 8; const slices = [];
      for (let i = 0; i < n; i++) { const off = on ? (random(`g${i}${Math.floor(frame / 2)}`) - 0.5) * W * 0.18 : 0;
        slices.push(<Img key={i} src={staticFile(logo)} style={{...base, clipPath: `inset(${(i / n) * 100}% 0 ${100 - ((i + 1) / n) * 100}% 0)`, transform: `translateX(${off}px)`}} />); }
      mark = <>{slices}{on && <Img src={staticFile(logo)} style={{...base, opacity: 0.35, transform: 'translateX(6px)', filter: 'hue-rotate(180deg)'}} />}</>; break; }
    case 'trail-echo': { const x = interpolate(frame, [0, fps * 1.2], [-width * 0.6, 0], {extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic)}); const echoes = [];
      for (let i = 1; i <= 6; i++) { const xi = interpolate(frame - i * 3, [0, fps * 1.2], [-width * 0.6, 0], {extrapolateRight: 'clamp', extrapolateLeft: 'clamp', easing: Easing.out(Easing.cubic)}); echoes.push(img({transform: `translateX(${xi}px)`, opacity: 0.22 - i * 0.03}, i)); }
      mark = <>{echoes}{img({transform: `translateX(${x}px)`})}</>; break; }
    case 'noise-wobble': { const amp = interpolate(frame, [0, fps * 3], [1, 0], {extrapolateRight: 'clamp'}); const jx = (random(`x${frame}`) - 0.5) * 18 * amp, jy = (random(`y${frame}`) - 0.5) * 18 * amp, jr = (random(`r${frame}`) - 0.5) * 3 * amp;
      mark = img({transform: `translate(${jx}px, ${jy}px) rotate(${jr}deg)`}); break; }
    case 'elastic-physics': { const drop = interpolate(frame, [0, fps * 0.55], [-height * 0.6, 0], {extrapolateRight: 'clamp', easing: Easing.in(Easing.quad)}); const s = spring({frame: frame - fps * 0.55, fps, config: {damping: 7, stiffness: 200}});
      const sy = frame < fps * 0.55 ? 1 : 1 - (1 - clamp(s)) * 0.35, sx = frame < fps * 0.55 ? 1 : 1 + (1 - clamp(s)) * 0.25; mark = img({transform: `translateY(${drop}px) scale(${sx}, ${sy})`, transformOrigin: '50% 100%'}); break; }
    case 'card-flip': { const rot = interpolate(frame, [0, fps * 2.2], [180, 0], {extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic)}) + Math.max(0, frame - fps * 3) * 0.4;
      mark = <div style={{position: 'absolute', inset: 0, perspective: 1600}}>{img({transform: `rotateY(${rot}deg)`, backfaceVisibility: 'visible'})}</div>; break; }
    case 'shadow-play': { const dx = interpolate(frame, [0, fps * 1.5, fps * 3], [width * 0.18, -width * 0.12, 0], {extrapolateRight: 'clamp', easing: Easing.inOut(Easing.cubic)}); const dy = interpolate(frame, [0, fps * 1.5, fps * 3], [height * 0.08, height * 0.14, height * 0.02], {extrapolateRight: 'clamp'});
      mark = <>{img({transform: `translate(${dx}px, ${dy}px)`, filter: 'brightness(0) blur(6px)', opacity: 0.25})}{img({})}</>; break; }
    case 'tile-assemble': { const cols = 8, rows = 4; const tiles = []; for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) { const i = r * cols + c; const s = spring({frame: frame - (random(`t${i}`) * 30), fps, config: {damping: 12}});
        const ox = (random(`ox${i}`) - 0.5) * width * 0.9 * (1 - clamp(s)), oy = (random(`oy${i}`) - 0.5) * height * 0.9 * (1 - clamp(s));
        tiles.push(<div key={i} style={{position: 'absolute', left: cx + (c / cols) * W, top: cy + (r / rows) * H, width: W / cols + 0.5, height: H / rows + 0.5, backgroundImage: `url(${staticFile(logo)})`, backgroundSize: `${W}px ${H}px`, backgroundPosition: `${-(c / cols) * W}px ${-(r / rows) * H}px`, transform: `translate(${ox}px, ${oy}px) rotate(${(1 - clamp(s)) * 90}deg)`, opacity: clamp(s * 1.5)}} />); }
      mark = <>{tiles}</>; break; }
    case 'exit-family': { const seg = Math.floor(frame / (fps * 1.6)) % 3; const l = (frame % (fps * 1.6)) / (fps * 1.6); const p = interpolate(l, [0.45, 1], [0, 1], {extrapolateLeft: 'clamp', easing: Easing.in(Easing.cubic)});
      const style: React.CSSProperties = seg === 0 ? {transform: `scale(${1 - p}) rotate(${p * 360}deg)`} : seg === 1 ? {opacity: 1 - p, filter: `blur(${p * 30}px)`} : {clipPath: `inset(0 ${p * 50}% 0 ${p * 50}%)`};
      mark = <>{img(style)}<div style={{position: 'absolute', right: width * 0.07, bottom: height * 0.10, fontFamily: FONT_NEU.display, fontSize: height * 0.028, color: NEU.SLATE}}>{['shrink-spin', 'blur-out', 'mask-close'][seg]}</div></>; break; }
  }
  return <AbsoluteFill style={{backgroundColor: NEU.CREAM, overflow: 'hidden'}}>{mark}<Label label={label} index={index} /></AbsoluteFill>;
};
