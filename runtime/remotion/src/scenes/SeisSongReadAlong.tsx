import React from 'react';
import {AbsoluteFill, Audio, Img, staticFile, useCurrentFrame, useVideoConfig, interpolate, spring} from 'remotion';
import {z} from 'zod';
import {NEU, NEU_RED, FONT_NEU} from '../tokens/neu';
import {SPRING_SMOOTH} from '../tokens/vox';
import {useLato} from '../tokens/lato';
import {SEIS_READ} from '../data/seisReadAlong';

/**
 * SeisSongReadAlong — "SEIS, Oh the Things That We Do!" on Bear's track.
 * NEU brand: white page, Lato regular, NU red as the one accent, the official mark on every page.
 * LEFT: a fixed 1:1 light-grey slot Bear overlays with Seuss-style art (a faint art brief sits in it).
 * RIGHT: the shout-out (builder · project · line) or a theme panel (headline + lines + a drawn diagram
 * from Conducting AI / Irreducibly Human / Computational Skepticism).
 * BOTTOM: karaoke of the current line — real words only — lit as sung. All timing from lyrics.json.
 */
export const seisSongReadAlongSchema = z.object({});
type Page = (typeof SEIS_READ.pages)[number];
const GREY = '#EBEBEB';

// ── drawn diagrams (pure SVG, NEU palette) ────────────────────────────────────
const Loop: React.FC<{w: number; t: number}> = ({w, t}) => {  // prompt → build → check → judge → again
  const r = w * 0.30, cx = w / 2, cy = w * 0.40; const steps = ['prompt', 'build', 'check', 'judge'];
  return <svg width={w} height={w * 0.92} viewBox={`0 0 ${w} ${w * 0.92}`}>
    <circle cx={cx} cy={cy} r={r} fill="none" stroke={NEU.SLATE} strokeWidth={2} strokeDasharray={`${2 * Math.PI * r}`} strokeDashoffset={2 * Math.PI * r * (1 - Math.min(1, t))} />
    {steps.map((s, i) => { const a = -Math.PI / 2 + (i / 4) * 2 * Math.PI; const x = cx + r * Math.cos(a), y = cy + r * Math.sin(a); const on = t > (i + 0.5) / 4;
      return <g key={s}><circle cx={x} cy={y} r={w * 0.095} fill={on ? (s === 'judge' ? NEU_RED : NEU.INK) : '#fff'} stroke={NEU.INK} strokeWidth={2} />
        <text x={x} y={y + w * 0.018} textAnchor="middle" fontFamily="Lato" fontSize={w * 0.042} fill={on ? '#fff' : NEU.INK}>{s}</text></g>; })}
    <text x={cx} y={cy + w * 0.015} textAnchor="middle" fontFamily="Lato" fontSize={w * 0.05} fill={NEU.SLATE}>again</text>
    <text x={cx} y={w * 0.90} textAnchor="middle" fontFamily="Lato" fontSize={w * 0.045} fill={NEU.INK}>not a prompt and done — a loop</text>
  </svg>;
};
const Gate: React.FC<{w: number; t: number}> = ({w, t}) => {  // phase gate: AI scaffolds | gate | human thinks
  const h = w * 0.5; const gx = w * 0.5;
  return <svg width={w} height={h} viewBox={`0 0 ${w} ${h}`}>
    <rect x={0} y={h * 0.25} width={gx * Math.min(1, t * 2)} height={h * 0.4} fill="#F3F3F3" stroke={NEU.SLATE} strokeWidth={2} />
    <text x={gx * 0.5} y={h * 0.49} textAnchor="middle" fontFamily="Lato" fontSize={w * 0.04} fill={NEU.INK}>AI does AI things</text>
    <line x1={gx} y1={h * 0.1} x2={gx} y2={h * 0.8} stroke={NEU_RED} strokeWidth={6} opacity={t > 0.5 ? 1 : 0} />
    <text x={gx} y={h * 0.95} textAnchor="middle" fontFamily="Lato" fontSize={w * 0.04} fill={NEU_RED} opacity={t > 0.5 ? 1 : 0}>the phase gate</text>
    <rect x={gx} y={h * 0.25} width={(w - gx) * Math.max(0, Math.min(1, t * 2 - 1))} height={h * 0.4} fill="#fff" stroke={NEU.INK} strokeWidth={2} />
    <text x={gx + (w - gx) * 0.5} y={h * 0.49} textAnchor="middle" fontFamily="Lato" fontSize={w * 0.036} fill={NEU.INK} opacity={t > 0.75 ? 1 : 0}>humans do the human things</text>
  </svg>;
};
const Tiers: React.FC<{w: number; t: number}> = ({w, t}) => {  // Irreducibly Human taxonomy, bottom-up
  const rows = [['pattern & association', 'machines win'], ['embodied', 'physics'], ['social & personal', 'human'], ['metacognitive · supervisory', 'human'], ['causal & counterfactual', 'human'], ['collective', 'human'], ['wisdom', 'human']];
  const rh = w * 0.056; const h = rh * rows.length + w * 0.06;
  return <svg width={w} height={h} viewBox={`0 0 ${w} ${h}`}>
    {rows.map(([a, b], i) => { const y = h - w * 0.06 - (i + 1) * rh; const on = t > (i + 1) / rows.length; const human = b === 'human';
      return <g key={a} opacity={on ? 1 : 0.15}><rect x={0} y={y} width={w} height={rh - 4} fill={human ? '#fff' : '#F3F3F3'} stroke={human ? NEU_RED : NEU.SLATE} strokeWidth={human ? 2.5 : 1.5} />
        <text x={w * 0.03} y={y + rh * 0.62} fontFamily="Lato" fontSize={w * 0.033} fill={NEU.INK}>{`tier ${i + 1} · ${a}`}</text>
        <text x={w * 0.97} y={y + rh * 0.62} textAnchor="end" fontFamily="Lato" fontSize={w * 0.03} fill={human ? NEU_RED : NEU.SLATE}>{b}</text></g>; })}
    <text x={w / 2} y={h - w * 0.015} textAnchor="middle" fontFamily="Lato" fontSize={w * 0.04} fill={NEU.SLATE}>the irreducibly human tiers</text>
  </svg>;
};
const Effort: React.FC<{w: number; t: number}> = ({w, t}) => {  // cognitive load → learning, with a mentor
  const h = w * 0.5; const pts: [number, number][] = []; const n = 40;
  for (let i = 0; i <= n * Math.min(1, t); i++) { const x = i / n; const y = 1 - (1 / (1 + Math.exp(-(x - 0.55) * 9))); pts.push([w * 0.08 + x * w * 0.84, h * 0.12 + y * h * 0.6]); }
  return <svg width={w} height={h} viewBox={`0 0 ${w} ${h}`}>
    <line x1={w * 0.08} y1={h * 0.74} x2={w * 0.92} y2={h * 0.74} stroke={NEU.SLATE} strokeWidth={2} /><line x1={w * 0.08} y1={h * 0.1} x2={w * 0.08} y2={h * 0.74} stroke={NEU.SLATE} strokeWidth={2} />
    {pts.length > 1 && <polyline points={pts.map((p) => p.join(',')).join(' ')} fill="none" stroke={NEU_RED} strokeWidth={4} />}
    <text x={w * 0.5} y={h * 0.86} textAnchor="middle" fontFamily="Lato" fontSize={w * 0.045} fill={NEU.INK}>struggle (cognitive load) →</text>
    <text x={w * 0.05} y={h * 0.08} fontFamily="Lato" fontSize={w * 0.045} fill={NEU.INK}>learning</text>
    <text x={w * 0.9} y={h * 0.3} textAnchor="end" fontFamily="Lato" fontSize={w * 0.038} fill={NEU.SLATE} opacity={t > 0.7 ? 1 : 0}>a mentor pushes you here ↗</text>
    <text x={w * 0.5} y={h * 0.97} textAnchor="middle" fontFamily="Lato" fontSize={w * 0.04} fill={NEU.SLATE}>no load, no learning</text>
  </svg>;
};
const Verify: React.FC<{w: number; t: number}> = ({w, t}) => {  // solve / verify asymmetry
  const h = w * 0.5;
  return <svg width={w} height={h} viewBox={`0 0 ${w} ${h}`}>
    <rect x={w * 0.05} y={h * 0.2} width={w * 0.4 * Math.min(1, t * 1.5)} height={h * 0.3} fill="#F3F3F3" stroke={NEU.SLATE} strokeWidth={2} />
    <text x={w * 0.25} y={h * 0.39} textAnchor="middle" fontFamily="Lato" fontSize={w * 0.05} fill={NEU.INK}>AI solves</text>
    <text x={w * 0.25} y={h * 0.62} textAnchor="middle" fontFamily="Lato" fontSize={w * 0.031} fill={NEU.SLATE}>fast · plausible · sometimes wrong</text>
    <rect x={w * 0.55} y={h * 0.2} width={w * 0.4 * Math.max(0, Math.min(1, t * 1.5 - 0.5))} height={h * 0.3} fill="#fff" stroke={NEU_RED} strokeWidth={3} />
    <text x={w * 0.75} y={h * 0.39} textAnchor="middle" fontFamily="Lato" fontSize={w * 0.05} fill={NEU_RED} opacity={t > 0.4 ? 1 : 0}>humans verify</text>
    <text x={w * 0.75} y={h * 0.62} textAnchor="middle" fontFamily="Lato" fontSize={w * 0.036} fill={NEU.SLATE} opacity={t > 0.4 ? 1 : 0}>the plausibility audit</text>
    <text x={w * 0.5} y={h * 0.9} textAnchor="middle" fontFamily="Lato" fontSize={w * 0.04} fill={NEU.INK}>faster solving → more to verify</text>
  </svg>;
};
const Chips: React.FC<{w: number; t: number}> = ({w, t}) => {  // what the machine does well — chips popping in
  const items = ['draft', 'sort', 'guess', 'hum', 'pattern', 'retrieve']; const cw = w / 3 - w * 0.02, ch = w * 0.14;
  return <svg width={w} height={ch * 2 + w * 0.1} viewBox={`0 0 ${w} ${ch * 2 + w * 0.1}`}>
    {items.map((it, i) => { const on = t > (i + 1) / items.length; const x = (i % 3) * (cw + w * 0.03), y = Math.floor(i / 3) * (ch + w * 0.03);
      return <g key={it} opacity={on ? 1 : 0.15}><rect x={x} y={y} width={cw} height={ch} rx={ch * 0.2} fill="#F3F3F3" stroke={NEU.SLATE} strokeWidth={2} />
        <text x={x + cw / 2} y={y + ch * 0.62} textAnchor="middle" fontFamily="Lato" fontSize={w * 0.05} fill={NEU.INK}>{it}</text></g>; })}
    <text x={w / 2} y={ch * 2 + w * 0.085} textAnchor="middle" fontFamily="Lato" fontSize={w * 0.04} fill={NEU.SLATE}>tier 1 — machines win here; let them</text>
  </svg>;
};
const DIAGRAMS: Record<string, React.FC<{w: number; t: number}>> = {loop: Loop, gate: Gate, tiers: Tiers, effort: Effort, verify: Verify, chips: Chips};

export const SeisSongReadAlong: React.FC = () => {
  useLato();
  const frame = useCurrentFrame(); const {fps, width, height} = useVideoConfig();
  const d = SEIS_READ;
  const page: Page = d.pages.find((p) => frame >= p.start && frame < p.end) || d.pages[d.pages.length - 1];
  const local = frame - page.start; const p = page.props;
  const inn = spring({frame: local - 3, fps, config: SPRING_SMOOTH});
  const S = height * 0.62;                      // the 1:1 art slot
  const SX = width * 0.06, SY = height * 0.15;
  const RX = SX + S + width * 0.05, RW = width - RX - width * 0.06;
  const line = page.lines.find((l) => l.words.length && frame >= l.words[0].s - 6 && frame <= l.words[l.words.length - 1].e + 14);
  const Diagram = p.diagram ? DIAGRAMS[p.diagram] : null;
  const diagT = interpolate(local, [6, 6 + fps * 2.2], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{backgroundColor: NEU.CREAM, overflow: 'hidden'}}>
      {d.audio && <Audio src={staticFile(d.audio)} />}
      {/* brand: eyebrow + rule top-left, the mark top-right */}
      <div style={{position: 'absolute', left: SX, top: height * 0.055, fontFamily: FONT_NEU.display, fontSize: height * 0.022, letterSpacing: 1.5, textTransform: 'uppercase', color: NEU.SLATE}}>SEIS · Software Engineering and Information Systems · learning by building</div>
      <div style={{position: 'absolute', left: SX, top: height * 0.095, width: width * 0.05, height: Math.max(4, height * 0.006), backgroundColor: NEU_RED}} />
      <Img src={staticFile('northeastern/official/notched-n-wordmark-red-black.svg')} style={{position: 'absolute', right: width * 0.06, top: height * 0.04, height: height * 0.075}} />
      {/* the 1:1 slot for Bear's art */}
      <div style={{position: 'absolute', left: SX, top: SY, width: S, height: S, backgroundColor: GREY, display: 'flex', alignItems: 'center', justifyContent: 'center', overflow: 'hidden'}}>
        {p.artImage
          ? <Img src={staticFile(p.artImage)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
          : <div style={{fontFamily: FONT_NEU.display, fontSize: height * 0.022, color: '#A9A9A9', textAlign: 'center', padding: S * 0.08, lineHeight: 1.4}}>{p.art || ''}</div>}
      </div>
      {/* right column */}
      <div style={{position: 'absolute', left: RX, top: SY, width: RW, height: S, opacity: inn, transform: `translateY(${(1 - inn) * 12}px)`}}>
        {(page.kind === 'showcase' || page.kind === 'photo') && (<>
          <div style={{fontFamily: FONT_NEU.display, fontSize: height * 0.026, letterSpacing: 1.2, textTransform: 'uppercase', color: NEU.SLATE}}>{p.eyebrow || 'shout-out · built at SEIS'}</div>
          <div style={{fontFamily: FONT_NEU.display, fontSize: height * ((p.name || '').length > 26 ? 0.06 : 0.082), color: NEU.INK, lineHeight: 1.05, marginTop: height * 0.02}}>{p.name}</div>
          <div style={{fontFamily: FONT_NEU.display, fontSize: height * 0.052, color: NEU_RED, marginTop: height * 0.025, lineHeight: 1.1}}>{p.project}</div>
          <div style={{fontFamily: FONT_NEU.display, fontSize: height * 0.032, color: NEU.INK, marginTop: height * 0.025, lineHeight: 1.3}}>{p.line}</div>
          {p.photo && <div style={{marginTop: height * 0.03, width: RW * 0.5, height: RW * 0.5 * 9 / 16, overflow: 'hidden', border: `1px solid ${NEU.HAIRLINE}`}}><Img src={staticFile(p.photo)} style={{width: '100%', height: '100%', objectFit: 'cover'}} /></div>}
        </>)}
        {page.kind === 'theme' && (<>
          <div style={{fontFamily: FONT_NEU.display, fontSize: height * 0.026, letterSpacing: 1.2, textTransform: 'uppercase', color: NEU.SLATE}}>{p.eyebrow || ''}</div>
          <div style={{fontFamily: FONT_NEU.display, fontSize: height * 0.064, color: NEU.INK, lineHeight: 1.08, marginTop: height * 0.015}}>{p.headline}</div>
          {(p.lines || '').split('|').filter(Boolean).map((l, i) => <div key={i} style={{fontFamily: FONT_NEU.display, fontSize: height * 0.03, color: NEU.INK, marginTop: height * 0.012, lineHeight: 1.3}}>{l.trim()}</div>)}
          {Diagram && <div style={{marginTop: height * 0.025}}><Diagram w={RW * (p.diagram === 'loop' ? 0.6 : 0.88)} t={diagT} /></div>}
        </>)}
        {page.kind === 'mark' && (<div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: S}}>
          {p.logo && <Img src={staticFile(p.logo)} style={{width: RW * 0.55}} />}
          {p.caption && <div style={{fontFamily: FONT_NEU.display, fontSize: height * 0.04, color: NEU.INK, marginTop: height * 0.05, textAlign: 'center', lineHeight: 1.2}}>{p.caption}</div>}
        </div>)}
      </div>
      {/* karaoke band — real words only, current line */}
      <div style={{position: 'absolute', left: 0, right: 0, bottom: height * 0.045, display: 'flex', justifyContent: 'center'}}>
        {line && <div style={{display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: `0 ${width * 0.012}px`, maxWidth: width * 0.9, borderTop: `1px solid ${NEU.HAIRLINE}`, paddingTop: height * 0.014}}>
          {line.words.map((w, j) => { const sung = frame >= w.s; const cur = sung && frame < w.e;
            return <span key={j} style={{position: 'relative', fontFamily: FONT_NEU.display, fontSize: height * 0.052, lineHeight: 1.25, color: sung ? NEU.INK : '#9A9A9A'}}>{w.t}
              <span style={{position: 'absolute', left: 0, bottom: 0, height: Math.max(3, height * 0.006), width: cur ? `${interpolate(frame, [w.s, w.e], [0, 100], {extrapolateRight: 'clamp'})}%` : sung ? '100%' : '0%', backgroundColor: NEU_RED}} /></span>; })}
        </div>}
      </div>
    </AbsoluteFill>
  );
};
