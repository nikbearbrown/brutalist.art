import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate, spring, Easing} from 'remotion';
import {z} from 'zod';
import {CLAUDE_FONT} from '../tokens/claude';

/**
 * ShowTellCard — the show-tell CARD family (Bear, 2026-09-27: "keep all typography and
 * colors but add more stop motion cards beyond just the isometric graphics … the skill
 * should never force but more choices can add").
 *
 * Sixteen interface-motion cards, one `kind` each, after a reference sheet of UI motion
 * studies: button→player, search→results, card→workspace, tabs→panels, chart morph,
 * dashboard zoom, spring stack, magnetic dock, masked type, elastic type, text→layout,
 * image reveal, perspective shift, glass focus, flowing paths, particle mark.
 *
 * Show-tell rules hold: ONE card fills the frame per beat; the motion carries the claim;
 * labels are 1–3 words (the data rows are the only multi-word text); the Claude palette
 * never retints (cream stage, warm ink, kraft, ONE terracotta accent — never on text);
 * EB Garamond for words, the UI sans for chrome, mono for numbers.
 *
 * STOP-MOTION: by default the animation is shot "on twos" — every drawing is held for two
 * frames (`onTwos`), like paper cut-outs under a camera. A solid kraft offset under each
 * card (no blur, no gradient) is the cut-out shadow.
 *
 * TIMING: phases are fractions of `durationSeconds` (the beat's measured audio). Each kind
 * finishes its main motion by ~70% and holds, so the voice lands on a finished picture.
 * GATE T samples the midpoint: every kind has its type on screen and SETTLED by 45%.
 */

// ── palette (Claude + show-tell kraft; never retint) ──────────────────────────
const C = {
  STAGE: '#F2F0E9', CARD: '#FAF9F5', INK: '#3D3929', SOFT: '#73705F', GHOST: '#D9D4C7',
  RULE: '#CFC8B8', SPARK: '#D97757', KRAFT: '#DCC9AA', KRAFT2: '#C7AE86', KRAFT_T: '#F3E9D8',
  DARK: '#26221F', DARK2: '#3A3530', BAR1: '#8B8F96', BAR2: '#B4AFA6', ON_DARK: '#F2F0E9',
} as const;
const SERIF = CLAUDE_FONT.serif, SANS = CLAUDE_FONT.ui, MONO = CLAUDE_FONT.mono;

// ── schema ─────────────────────────────────────────────────────────────────────
const row = z.object({label: z.string(), value: z.string().default(''), sub: z.string().default('')});
export const showTellCardSchema = z.object({
  kind: z.enum(['player', 'search', 'workspace', 'tabs', 'chart', 'dashboard', 'stack', 'dock',
    'masked', 'elastic', 'layout', 'reveal', 'perspective', 'focus', 'paths', 'particles']).default('search'),
  /** Main words: player title, search query, workspace/doc/card heading, dashboard metric name… */
  heading: z.string().default(''),
  /** One short secondary line (a kicker, a unit, a caption). */
  sub: z.string().default(''),
  /** The big word for masked / elastic type; the big number for dashboard (e.g. "12,480"). */
  word: z.string().default(''),
  /** Rows: search results, tab panels, table rows, dock labels, path nodes, stack cards. */
  items: z.array(row).default([]),
  /** Second row set (tabs: the panel shown after the switch). */
  items2: z.array(row).default([]),
  /** Tab names (tabs), axis names (chart). */
  labels: z.array(z.string()).default([]),
  /** Numbers: chart values, player [elapsed, total] seconds. */
  values: z.array(z.number()).default([]),
  /** Particles: rows of '#'/'.' drawing the mark the dots assemble into. */
  bitmap: z.array(z.string()).default([]),
  /** Optional move times as fractions of the beat (focus: one per lens move; tabs: [switch]).
   *  Compute them from the narration (phrase index / length) so the card moves on the word. */
  cues: z.array(z.number()).default([]),
  /** Which row/tab/node is the focus (0-based). */
  focus: z.number().int().default(0),
  dark: z.boolean().default(false),
  onTwos: z.boolean().default(true),
  durationSeconds: z.number().min(2).default(8),
});
export type ShowTellCardProps = z.infer<typeof showTellCardSchema>;

// ── helpers ────────────────────────────────────────────────────────────────────
const clamp = (v: number, a = 0, b = 1) => Math.min(b, Math.max(a, v));
const ease = Easing.bezier(0.33, 0, 0.2, 1);
/** 0→1 between two fractions of the beat, eased. */
const seg = (p: number, a: number, b: number) => ease(clamp((p - a) / (b - a)));
const lerp = (a: number, b: number, t: number) => a + (b - a) * t;

const Shadowed: React.FC<{x: number; y: number; w: number; h: number; r?: number; fill?: string;
  border?: string; bw?: number; off?: number; style?: React.CSSProperties; children?: React.ReactNode}> =
  ({x, y, w, h, r = 28, fill = C.CARD, border = C.INK, bw = 3, off = 12, style, children}) => (
  <>
    <div style={{position: 'absolute', left: x + off, top: y + off, width: w, height: h, borderRadius: r, background: C.KRAFT}} />
    <div style={{position: 'absolute', left: x, top: y, width: w, height: h, borderRadius: r, background: fill,
      border: `${bw}px solid ${border}`, overflow: 'hidden', boxSizing: 'border-box', ...style}}>{children}</div>
  </>
);

const Txt: React.FC<{x: number; y: number; size?: number; color?: string; font?: string; weight?: number;
  w?: number; align?: 'left' | 'center' | 'right'; o?: number; children: React.ReactNode}> =
  ({x, y, size = 48, color = C.INK, font = SERIF, weight = 400, w, align = 'left', o = 1, children}) => (
  <div style={{position: 'absolute', left: x, top: y, fontSize: size, color, fontFamily: font, fontWeight: weight,
    width: w, textAlign: align, lineHeight: 1.1, opacity: o, whiteSpace: 'nowrap'}}>{children}</div>
);

const Swatch: React.FC<{x: number; y: number; s?: number; i: number}> = ({x, y, s = 64, i}) => (
  <div style={{position: 'absolute', left: x, top: y, width: s, height: s, borderRadius: 12,
    background: [C.KRAFT2, C.SPARK, C.DARK, C.BAR1][i % 4], border: `3px solid ${C.INK}`, boxSizing: 'border-box'}} />
);

const Cursor: React.FC<{x: number; y: number}> = ({x, y}) => (
  <svg style={{position: 'absolute', left: x, top: y}} width="54" height="66" viewBox="0 0 27 33">
    <path d="M2 2 L2 27 L9 20 L14 31 L18 29 L13 18 L23 18 Z" fill={C.INK} stroke={C.CARD} strokeWidth="2" strokeLinejoin="round" />
  </svg>
);

/** The drawn "ball" object the reference sheet uses as its hero image: kraft floor, terracotta ball. */
const Ball: React.FC<{cx: number; cy: number; r: number}> = ({cx, cy, r}) => (
  <>
    <div style={{position: 'absolute', left: cx - r * 0.9, top: cy + r * 0.8, width: r * 1.8, height: r * 0.34, borderRadius: '50%', background: C.KRAFT2}} />
    <div style={{position: 'absolute', left: cx - r, top: cy - r, width: 2 * r, height: 2 * r, borderRadius: '50%',
      background: C.SPARK, border: `3px solid ${C.INK}`, boxSizing: 'border-box'}} />
    <div style={{position: 'absolute', left: cx - r * 0.55, top: cy - r * 0.62, width: r * 0.5, height: r * 0.34, borderRadius: '50%', background: C.KRAFT_T}} />
  </>
);

const mmss = (s: number) => `${Math.floor(s / 60)}:${String(Math.floor(s % 60)).padStart(2, '0')}`;

// ── the sixteen kinds ─────────────────────────────────────────────────────────
type K = {p: number; f: number; fps: number; P: ShowTellCardProps};

const Player: React.FC<K> = ({p, P}) => {
  const grow = seg(p, 0.16, 0.34);
  const w = lerp(420, 1320, grow), h = lerp(120, 700, grow);
  const x = 960 - w / 2, y = 540 - h / 2 + 30;
  const [el = 22, tot = 42] = P.values;
  const prog = seg(p, 0.38, 0.95);
  const inner = seg(p, 0.3, 0.4);
  return <>
    <Shadowed x={x} y={y} w={w} h={h} r={lerp(60, 36, grow)} fill={C.DARK}>
      <Txt x={48} y={34} size={48} color={C.ON_DARK} font={SANS} weight={600} o={1 - grow}>{'▶  ' + (P.sub || 'Preview')}</Txt>
      <div style={{opacity: inner}}>
        <div style={{position: 'absolute', left: 70, top: 70, width: w - 140, height: h - 300, borderRadius: 22, background: C.KRAFT_T}} />
        <Ball cx={w / 2} cy={70 + (h - 300) / 2 - 10} r={Math.max(10, (h - 300) * 0.3)} />
        <Txt x={70} y={h - 200} size={54} color={C.ON_DARK} weight={600}>{P.heading || 'Spring launch'}</Txt>
        <Txt x={w - 330} y={h - 196} size={44} color={C.ON_DARK} font={MONO} w={260} align="right">{`${mmss(el * prog)} / ${mmss(tot)}`}</Txt>
        <div style={{position: 'absolute', left: 70, top: h - 100, width: w - 140, height: 16, borderRadius: 8, background: C.DARK2}} />
        <div style={{position: 'absolute', left: 70, top: h - 100, width: (w - 140) * (el / tot) * prog, height: 16, borderRadius: 8, background: C.ON_DARK}} />
        <div style={{position: 'absolute', left: 70 + (w - 140) * (el / tot) * prog - 16, top: h - 108, width: 32, height: 32, borderRadius: 16, background: C.SPARK}} />
      </div>
    </Shadowed>
    {grow < 0.05 && <Cursor x={lerp(1500, 1090, seg(p, 0.02, 0.14))} y={lerp(860, 600, seg(p, 0.02, 0.14))} />}
  </>;
};

const Search: React.FC<K> = ({p, P}) => {
  const q = P.heading || 'spring campaign';
  const typed = q.slice(0, Math.round(q.length * seg(p, 0.06, 0.26)));
  const rows = (P.items.length ? P.items : [{label: 'Spring launch email', sub: 'Email · 48% opens', value: ''},
    {label: 'Spring reel cut', sub: 'Reel · 21k views', value: ''}, {label: 'Spring landing page', sub: 'Page · 6.2% signups', value: ''}]).slice(0, 4);
  return <>
    <Shadowed x={300} y={110} w={1320} h={130} r={65}>
      <svg style={{position: 'absolute', left: 44, top: 36}} width="56" height="56" viewBox="0 0 28 28">
        <circle cx="11" cy="11" r="8" fill="none" stroke={C.INK} strokeWidth="3" /><line x1="17" y1="17" x2="25" y2="25" stroke={C.INK} strokeWidth="3" strokeLinecap="round" /></svg>
      <Txt x={130} y={36} size={56} font={SANS}>{typed || <span style={{color: C.SOFT}}>Search</span>}</Txt>
      {p > 0.06 && p < 0.3 && Math.floor(p * 40) % 2 === 0 && <div style={{position: 'absolute', left: 140 + typed.length * 27, top: 38, width: 4, height: 56, background: C.INK}} />}
    </Shadowed>
    {rows.map((r, i) => {
      const a = seg(p, 0.3 + i * 0.07, 0.4 + i * 0.07);
      const y = 300 + i * 175;
      const hot = i === P.focus && p > 0.62;
      return <div key={i} style={{opacity: a, transform: `translateY(${(1 - a) * -40}px)`}}>
        <Shadowed x={300} y={y} w={1320} h={160} r={24} off={hot ? 14 : 8} bw={hot ? 4 : 3}>
          <Swatch x={36} y={40} i={i} s={70} />
          <Txt x={140} y={22} size={52} weight={600}>{r.label}</Txt>
          <Txt x={140} y={80} size={48} color={C.SOFT} font={SANS}>{r.sub}</Txt>
        </Shadowed>
      </div>;
    })}
  </>;
};

const Workspace: React.FC<K> = ({p, P}) => {
  const g = seg(p, 0.14, 0.36);
  const x = lerp(1180, 200, g), y = lerp(680, 110, g), w = lerp(460, 1520, g), h = lerp(200, 860, g);
  const inner = seg(p, 0.34, 0.46);
  const chips = (P.items.length ? P.items : [{label: 'Draft', value: '', sub: ''}, {label: '3 edits', value: '', sub: ''}]).slice(0, 3);
  return <Shadowed x={x} y={y} w={w} h={h} r={30}>
    <Txt x={40} y={34} size={50} weight={600}>{P.heading || 'Q3 brief'}</Txt>
    <div style={{opacity: inner}}>
      <div style={{position: 'absolute', left: 0, top: 120, width: 300, height: h - 120, background: C.STAGE, borderRight: `3px solid ${C.RULE}`}} />
      {[0, 1, 2, 3, 4].map(i => <div key={i} style={{position: 'absolute', left: 40, top: 170 + i * 80, width: 210 - (i % 2) * 50, height: 26, borderRadius: 13,
        background: i === 1 ? C.SPARK : C.GHOST, transform: `scaleX(${seg(p, 0.4 + i * 0.03, 0.5 + i * 0.03)})`, transformOrigin: 'left'}} />)}
      <div style={{position: 'absolute', left: 350, top: 150, width: w - 400, height: h - 330, borderRadius: 22, background: C.KRAFT_T, border: `3px solid ${C.RULE}`}} />
      <Ball cx={350 + (w - 400) * 0.62} cy={150 + (h - 330) * 0.5} r={Math.max(10, (h - 330) * 0.26)} />
      {[0, 1, 2].map(i => <div key={i} style={{position: 'absolute', left: 390, top: 190 + i * 60, width: [420, 340, 260][i], height: 24, borderRadius: 12, background: C.BAR2,
        transform: `scaleX(${seg(p, 0.48 + i * 0.04, 0.58 + i * 0.04)})`, transformOrigin: 'left'}} />)}
      {chips.map((c, i) => <div key={i} style={{position: 'absolute', left: 350 + i * 260, top: h - 150, height: 84, padding: '0 34px', borderRadius: 42,
        border: `3px solid ${C.INK}`, background: i === 0 ? C.DARK : C.CARD, color: i === 0 ? C.ON_DARK : C.INK, fontFamily: SANS, fontSize: 44,
        display: 'flex', alignItems: 'center', opacity: seg(p, 0.5 + i * 0.05, 0.58 + i * 0.05)}}>{c.label}</div>)}
    </div>
  </Shadowed>;
};

const Tabs: React.FC<K> = ({p, P}) => {
  const tabs = P.labels.length ? P.labels.slice(0, 3) : ['Reels', 'Posts', 'Email'];
  const A = P.items.length ? P.items : [{label: 'Launch teaser', value: '21k', sub: ''}, {label: 'Studio tour', value: '14k', sub: ''}, {label: 'Tool tip', value: '9.8k', sub: ''}];
  const B = P.items2.length ? P.items2 : [{label: 'Stack carousel', value: '2.1k', sub: ''}, {label: 'Prompt pack', value: '1.4k', sub: ''}, {label: 'Weekly recap', value: '980', sub: ''}];
  const t0 = P.cues.length ? P.cues[0] : 0.36;
  const sw = seg(p, t0, t0 + 0.14);
  const tw = 360;
  return <Shadowed x={260} y={90} w={1400} h={880} r={34}>
    <div style={{position: 'absolute', left: 60, top: 50, width: tw * tabs.length + 20, height: 110, borderRadius: 55, background: C.STAGE, border: `3px solid ${C.RULE}`}} />
    <div style={{position: 'absolute', left: 70 + lerp(0, tw, sw), top: 60, width: tw, height: 90, borderRadius: 45, background: C.DARK}} />
    {tabs.map((t, i) => <Txt key={i} x={70 + i * tw} y={78} w={tw} align="center" size={48} font={SANS} weight={600}
      color={(i === 0 && sw < 0.5) || (i === 1 && sw >= 0.5) ? C.ON_DARK : C.INK}>{t}</Txt>)}
    {[A, B].map((set, s) => set.slice(0, 3).map((r, i) => {
      const inn = s === 0 ? 1 - seg(p, t0 + i * 0.03, t0 + 0.08 + i * 0.03) : seg(p, t0 + 0.1 + i * 0.04, t0 + 0.2 + i * 0.04);
      const vis = s === 0 ? seg(p, 0.05 + i * 0.05, 0.15 + i * 0.05) * inn : inn;
      return <div key={`${s}-${i}`} style={{position: 'absolute', left: 60, top: 220 + i * 200, width: 1270, height: 170, opacity: vis,
        transform: `translateX(${s === 0 ? -(1 - inn) * 120 : (1 - inn) * 120}px)`}}>
        <Swatch x={10} y={46} i={i + s} s={76} />
        <Txt x={130} y={50} size={56} weight={600}>{r.label}</Txt>
        <Txt x={930} y={54} size={52} font={MONO} w={320} align="right">{r.value}</Txt>
        <div style={{position: 'absolute', left: 0, top: 168, width: 1270, height: 3, background: C.RULE}} />
      </div>;
    }))}
  </Shadowed>;
};

const Chart: React.FC<K> = ({p, P}) => {
  const vals = P.values.length ? P.values : [38, 52, 46, 70, 64, 82, 92];
  const labs = P.labels.length ? P.labels : ['M', 'T', 'W', 'T', 'F', 'S', 'S'];
  const max = Math.max(...vals) * 1.12;
  const X0 = 170, W = 1350, Y0 = 820, H = 540, n = vals.length, step = W / (n - 1);
  const grow = seg(p, 0.06, 0.3), morph = seg(p, 0.36, 0.56), line = seg(p, 0.5, 0.66);
  const pts = vals.map((v, i) => [X0 + i * step, Y0 - (v / max) * H * grow] as const);
  const d = pts.map(([x, y], i) => `${i ? 'L' : 'M'}${x},${y}`).join(' ');
  const len = pts.reduce((a, [x, y], i) => i ? a + Math.hypot(x - pts[i - 1][0], y - pts[i - 1][1]) : 0, 0);
  const last = pts[n - 1];
  return <Shadowed x={110} y={90} w={1700} h={900} r={34}>
    <Txt x={60} y={40} size={52} weight={600}>{P.heading || 'Weekly reach'}</Txt>
    {P.sub && <Txt x={1000} y={46} size={48} color={C.SOFT} font={SANS} w={620} align="right">{P.sub}</Txt>}
    <div style={{position: 'absolute', left: X0 - 110, top: Y0 - 90 + 3, width: W + 150, height: 3, background: C.INK}} />
    {pts.map(([x, y], i) => {
      const bw = lerp(110, 0, morph), bh = (Y0 - y);
      return <div key={i}>
        <div style={{position: 'absolute', left: x - 110 - bw / 2, top: y - 90, width: bw, height: bh, background: i === n - 1 ? C.BAR1 : C.BAR2, borderRadius: 10, opacity: 1 - morph * 0.85}} />
        <Txt x={x - 110 - 40} y={Y0 - 60} w={80} align="center" size={42} font={SANS} color={C.SOFT}>{labs[i]}</Txt>
      </div>;
    })}
    <svg style={{position: 'absolute', left: -110, top: -90}} width="1920" height="1080">
      <path d={d} fill="none" stroke={C.INK} strokeWidth={7} strokeLinejoin="round" strokeDasharray={len} strokeDashoffset={len * (1 - line)} />
      {pts.map(([x, y], i) => <circle key={i} cx={x} cy={y} r={14 * morph} fill={i === n - 1 ? C.SPARK : C.CARD} stroke={C.INK} strokeWidth={4} />)}
    </svg>
    <div style={{position: 'absolute', left: last[0] - 110 - 70, top: last[1] - 90 - 120, width: 140, height: 80, borderRadius: 18, background: C.DARK,
      color: C.ON_DARK, fontFamily: MONO, fontSize: 46, display: 'flex', alignItems: 'center', justifyContent: 'center', opacity: seg(p, 0.6, 0.68)}}>{vals[n - 1]}</div>
  </Shadowed>;
};

const Dashboard: React.FC<K> = ({p, P}) => {
  const z = seg(p, 0.12, 0.34);
  const s = lerp(1, 1.35, z), tx = 0, ty = lerp(0, -40, z);
  const big = P.word || '12,480';
  const target = parseFloat(big.replace(/[^0-9.]/g, '')) || 0;
  const count = Math.round(target * seg(p, 0.34, 0.56));
  const shown = big.includes(',') ? count.toLocaleString('en-US') : String(count);
  return <Shadowed x={110} y={90} w={1700} h={900} r={34}>
    <div style={{position: 'absolute', left: 0, top: 0, width: 1700, height: 900, transform: `translate(${tx}px, ${ty}px) scale(${s})`, transformOrigin: '140px 420px'}}>
      {[0, 1, 2].map(i => <div key={i} style={{position: 'absolute', left: 80 + i * 520, top: 70, width: 460, height: 150, borderRadius: 22, background: C.STAGE, border: `3px solid ${C.RULE}`}}>
        <div style={{position: 'absolute', left: 36, top: 44, width: 240, height: 26, borderRadius: 13, background: C.GHOST}} />
        <div style={{position: 'absolute', left: 36, top: 90, width: 160, height: 26, borderRadius: 13, background: C.BAR2}} /></div>)}
      <div style={{position: 'absolute', left: 80, top: 280, width: 1500, height: 540, borderRadius: 26, background: C.CARD, border: `4px solid ${C.INK}`}}>
        <Txt x={60} y={50} size={50} color={C.SOFT} font={SANS}>{P.heading || 'Signups'}</Txt>
        <Txt x={60} y={120} size={150} font={MONO} weight={600}>{shown}</Txt>
        {P.sub && <div style={{position: 'absolute', left: 60, top: 300, height: 80, padding: '0 30px', borderRadius: 40, background: C.DARK, color: C.ON_DARK,
          fontFamily: MONO, fontSize: 48, display: 'flex', alignItems: 'center', opacity: seg(p, 0.5, 0.58)}}>{P.sub}</div>}
        <svg style={{position: 'absolute', left: 60, top: 400}} width="1380" height="120">
          <path d="M0,110 C200,104 260,84 420,88 S700,50 860,62 S1160,16 1380,8" fill="none" stroke={C.INK} strokeWidth="7"
            strokeDasharray="1500" strokeDashoffset={1500 * (1 - seg(p, 0.4, 0.62))} /></svg>
      </div>
    </div>
  </Shadowed>;
};

const Stack: React.FC<K> = ({p, f, fps, P}) => {
  const cards = P.items.length ? P.items.slice(0, 3) : [{label: 'Summer kit', value: '£24', sub: ''}, {label: 'Starter pack', value: '£12', sub: ''}, {label: 'Pro bundle', value: '£48', sub: ''}];
  // Front card (i=0) in the centre, the others fan out left and right and settle side by side,
  // so the settled picture fills the frame (Gate V underfill) and no card hides another's words.
  const CW = 520, CH = 720, GAP = 560;
  return <>{cards.map((c, i) => {
    const k = cards.length - 1 - i;           // back to front
    const sp = spring({frame: f - Math.round(fps * (0.1 + k * 0.12) * P.durationSeconds / 8), fps, config: {damping: 11, stiffness: 120, mass: 0.8}});
    const settle = seg(p, 0.3, 0.44);
    const rot = lerp([-3, -14, 14][i], [0, -4, 4][i], settle) * sp;
    const dx = lerp([0, -GAP * 0.55, GAP * 0.55][i], [0, -GAP, GAP][i], settle);
    const lift = i === 0 ? -40 * seg(p, 0.62, 0.72) : 0;
    const x = 960 - CW / 2 + dx, y = 180 + (1 - sp) * 700 + lift;
    return <div key={i} style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080, transform: `rotate(${rot}deg)`, transformOrigin: `${x + CW / 2}px ${y + CH / 2}px`, zIndex: 10 - i}}>
      <Shadowed x={x} y={y} w={CW} h={CH} r={30}>
        <div style={{position: 'absolute', left: 36, top: 36, width: CW - 72, height: 380, borderRadius: 20, background: C.KRAFT_T, border: `3px solid ${C.RULE}`}} />
        <Ball cx={CW / 2} cy={226} r={100} />
        <Txt x={40} y={460} size={56} weight={600}>{c.label}</Txt>
        <Txt x={40} y={540} size={52} font={MONO}>{c.value}</Txt>
        {i === 0 && <div style={{position: 'absolute', left: CW - 150, top: CH - 150, width: 110, height: 110, borderRadius: 55, background: C.DARK, opacity: seg(p, 0.66, 0.72)}}>
          <svg width="110" height="110" viewBox="0 0 110 110"><path d="M32 57 L49 73 L80 40" fill="none" stroke={C.ON_DARK} strokeWidth="10" strokeLinecap="round" strokeLinejoin="round" /></svg></div>}
      </Shadowed>
    </div>;
  })}</>;
};

const Dock: React.FC<K> = ({p, P}) => {
  const labels = P.items.length ? P.items.map(i => i.label) : ['Home', 'Search', 'Player', 'Assets', 'Notes', 'Focus', 'Share'];
  const n = labels.length, gap = 170, x0 = 960 - ((n - 1) * gap) / 2, y = 700;
  const cx = interpolate(p, [0.1, 0.4, 0.62, 0.8], [x0 - 60, x0 + gap * 2, x0 + gap * 4, x0 + gap * P.focus], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: ease});
  const hovered = Math.round((cx - x0) / gap);
  return <Shadowed x={160} y={160} w={1600} h={760} r={40} fill={C.DARK}>
    <svg style={{position: 'absolute', left: -160, top: -160}} width="1920" height="1080">
      <path d={`M220,560 C520,${420 - 80 * seg(p, 0.2, 0.5)} 760,300 ${cx},260 S1400,420 1700,520`} fill="none" stroke={C.DARK2} strokeWidth="5" /></svg>
    <div style={{position: 'absolute', left: x0 - 160 - 110, top: y - 160 - 20, width: (n - 1) * gap + 220, height: 180, borderRadius: 60, background: C.DARK2}} />
    {labels.map((l, i) => {
      const x = x0 + i * gap;
      const d = Math.abs(cx - x);
      const sc = 1 + 0.7 * Math.max(0, 1 - d / 260);
      return <div key={i} style={{position: 'absolute', left: x - 160 - 50, top: y - 160 + 10 - (sc - 1) * 60, width: 100, height: 100, borderRadius: 24,
        background: i % 3 === 0 ? C.SPARK : i % 3 === 1 ? C.ON_DARK : C.KRAFT, transform: `scale(${sc})`, transformOrigin: 'bottom center'}}>
        <div style={{position: 'absolute', left: 30, top: 30, width: 40, height: 40, borderRadius: i % 2 ? 20 : 8, background: i % 3 === 1 ? C.DARK : C.CARD}} /></div>;
    })}
    {p > 0.12 && <div style={{position: 'absolute', left: x0 + hovered * gap - 160 - 120, top: y - 160 - 230, width: 240, height: 86, borderRadius: 43, background: C.CARD,
      color: C.INK, fontFamily: SANS, fontSize: 48, fontWeight: 600, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>{labels[Math.max(0, Math.min(n - 1, hovered))]}</div>}
  </Shadowed>;
};

const Masked: React.FC<K> = ({p, P}) => {
  const word = P.word || 'OPUS';
  const rise = seg(p, 0.1, 0.42);
  return <Shadowed x={160} y={110} w={1600} h={860} r={34}>
    {P.heading && <Txt x={70} y={50} size={48} font={MONO} color={C.SOFT}>{P.heading}</Txt>}
    <div style={{position: 'absolute', left: 0, top: 150, width: 1600, textAlign: 'center', fontFamily: SERIF, fontSize: 340, fontWeight: 700, lineHeight: 1,
      color: 'transparent', WebkitTextStroke: `5px ${C.INK}`}}>{word}</div>
    <div style={{position: 'absolute', left: 0, top: 150, width: 1600, textAlign: 'center', fontFamily: SERIF, fontSize: 340, fontWeight: 700, lineHeight: 1,
      color: C.INK, clipPath: `inset(${(1 - rise) * 100}% 0 0 0)`}}>{word}</div>
    <div style={{position: 'absolute', left: 170, top: 520 - rise * 360, width: 1260, height: 6, background: C.RULE}} />
    <div style={{position: 'absolute', left: 1440, top: 500 - rise * 360, width: 44, height: 44, borderRadius: 22, background: C.SPARK}} />
    <div style={{position: 'absolute', left: 0, top: 600, width: 1600, textAlign: 'center', fontFamily: SERIF, fontSize: 96, color: C.INK,
      clipPath: `inset(0 0 ${(1 - seg(p, 0.3, 0.44)) * 100}% 0)`, transform: `translateY(${(1 - seg(p, 0.3, 0.44)) * 40}px)`}}>{P.sub || 'in motion'}</div>
  </Shadowed>;
};

const Elastic: React.FC<K> = ({p, f, P}) => {
  const word = (P.word || 'STRETCH').split('');
  const on = seg(p, 0.04, 0.14);
  return <Shadowed x={160} y={110} w={1600} h={860} r={34} fill={C.DARK}>
    <div style={{position: 'absolute', left: 0, top: 250, width: 1600, display: 'flex', justifyContent: 'center', alignItems: 'flex-end', height: 300}}>
      {word.map((ch, i) => {
        const wave = Math.sin((f / 7) - i * 0.8) * seg(p, 0.12, 0.3) * (1 - seg(p, 0.7, 0.85));
        return <div key={i} style={{fontFamily: SERIF, fontSize: 230, fontWeight: 700, lineHeight: 1, color: C.ON_DARK, opacity: on,
          transform: `scaleY(${1 + 0.35 * wave}) scaleX(${1 - 0.18 * wave})`, transformOrigin: 'bottom center', margin: '0 4px'}}>{ch}</div>;
      })}
    </div>
    <div style={{position: 'absolute', left: 170, top: 560, width: 1260, height: 5, background: C.DARK2}} />
    <div style={{position: 'absolute', left: 170 + 1260 * ((Math.sin(f / 9) + 1) / 2), top: 541, width: 42, height: 42, borderRadius: 21, background: C.SPARK}} />
    <Txt x={0} y={620} w={1600} align="center" size={60} color={C.ON_DARK} o={seg(p, 0.2, 0.3)}>{P.sub || 'at rest, then stretched'}</Txt>
  </Shadowed>;
};

const Layout: React.FC<K> = ({p, P}) => {
  const head = P.heading || 'Design that moves people';
  const split = seg(p, 0.14, 0.34);
  return <Shadowed x={160} y={100} w={1600} h={880} r={34}>
    <div style={{position: 'absolute', left: lerp(420, 70, split), top: lerp(380, 60, split), fontFamily: SERIF, fontSize: lerp(60, 50, split), color: C.SOFT,
      padding: '10px 26px', border: `3px solid ${C.INK}`, borderRadius: 16, opacity: 1 - seg(p, 0.28, 0.36)}}>{head}</div>
    <div style={{opacity: seg(p, 0.3, 0.42)}}>
      <Txt x={70} y={170} size={48} font={SANS} weight={700}>{P.sub || 'FIELD NOTES'}</Txt>
      <div style={{position: 'absolute', left: 70, top: 250, width: 820, fontFamily: SERIF, fontSize: 104, fontWeight: 600, lineHeight: 1.05, color: C.INK}}>{head}</div>
      <div style={{position: 'absolute', left: 980, top: 170, width: 540, height: 600, borderRadius: 24, background: C.KRAFT_T, border: `3px solid ${C.RULE}`,
        clipPath: `inset(0 0 ${(1 - seg(p, 0.36, 0.5)) * 100}% 0)`}} />
      <Ball cx={1250} cy={450} r={120} />
      {(P.items.length ? P.items : [{label: '“Motion explains the change.”', value: '', sub: ''}]).slice(0, 1).map((q, i) =>
        <div key={i} style={{position: 'absolute', left: 70, top: 680, fontFamily: SERIF, fontSize: 54, color: C.INK, opacity: seg(p, 0.46, 0.56)}}>{q.label}</div>)}
    </div>
  </Shadowed>;
};

const Reveal: React.FC<K> = ({p, P}) => {
  const n = 8, sw = 1600 / n;
  return <Shadowed x={160} y={100} w={1600} h={880} r={34}>
    <div style={{position: 'absolute', left: 0, top: 0, width: 1600, height: 880, background: C.KRAFT_T}} />
    <div style={{position: 'absolute', left: 120, top: 120, width: 520, height: 420, borderRadius: 40, background: C.KRAFT, transform: 'rotate(-8deg)'}} />
    <Ball cx={880} cy={430} r={250} />
    <div style={{position: 'absolute', left: 60, top: 60, height: 84, padding: '0 34px', borderRadius: 42, background: C.CARD, border: `3px solid ${C.INK}`,
      fontFamily: SANS, fontSize: 46, fontWeight: 600, color: C.INK, display: 'flex', alignItems: 'center', opacity: seg(p, 0.4, 0.46)}}>{P.heading || 'New drop'}</div>
    {Array.from({length: n}).map((_, i) => {
      const o = seg(p, 0.08 + i * 0.03, 0.26 + i * 0.03);
      return <div key={i} style={{position: 'absolute', left: i * sw, top: 0, width: o >= 1 ? 0 : sw * (1 - o) + 1, height: 880, background: i % 2 ? C.DARK : C.DARK2}} />;
    })}
  </Shadowed>;
};

const Perspective: React.FC<K> = ({p, P}) => {
  const t = seg(p, 0.1, 0.4);
  return <div style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080, perspective: 2200}}>
    {[2, 1, 0].map(i => {
      const ry = lerp(0, -32, t) + i * lerp(0, 8, t), tx = lerp(0, -260, t) + i * lerp(0, 330, t), tz = -i * lerp(0, 160, t);
      return <div key={i} style={{position: 'absolute', left: 560, top: 150, width: 800, height: 780, transform: `translateX(${tx}px) translateZ(${tz}px) rotateY(${ry}deg)`,
        transformStyle: 'preserve-3d', opacity: i === 0 ? 1 : seg(p, 0.12 + i * 0.05, 0.3 + i * 0.05)}}>
        <Shadowed x={0} y={0} w={800} h={780} r={26}>
          {i === 0 && <Txt x={50} y={44} size={52} weight={600}>{P.heading || 'Launch plan'}</Txt>}
          {[0, 1, 2, 3, 4].map(k => <div key={k} style={{position: 'absolute', left: 50, top: 150 + k * 80, width: [620, 540, 600, 420, 500][k], height: 28, borderRadius: 14, background: k === 0 ? C.BAR1 : C.GHOST}} />)}
          <div style={{position: 'absolute', left: 50, top: 600, width: 260, height: 100, borderRadius: 18, background: i === 0 ? C.SPARK : C.KRAFT}} />
        </Shadowed>
      </div>;
    })}
  </div>;
};

const Focus: React.FC<K> = ({p, P}) => {
  const rows = P.items.length ? P.items.slice(0, 5) : [{label: 'Open rate', value: '48%', sub: ''}, {label: 'Click rate', value: '6.2%', sub: ''},
    {label: 'Replies', value: '31', sub: ''}, {label: 'Unsubscribes', value: '0.3%', sub: ''}, {label: 'Revenue', value: '£4.2k', sub: ''}];
  const n = rows.length, rh = 132, y0 = 230;
  // The lens SNAPS row to row (0.05 of the beat per move) and holds between moves, so the
  // GATE T midpoint (50%) always lands on a hold, never on a border crossing a label.
  const target = Math.min(n - 1, P.focus || 4);
  const stops = (P.cues.length ? P.cues : [0.22, 0.36, 0.56, 0.72]).slice(0, target);
  const pos = stops.reduce((a, t) => a + seg(p, t, t + 0.05), 0);
  return <Shadowed x={260} y={80} w={1400} h={900} r={34}>
    <Txt x={70} y={60} size={56} weight={600}>{P.heading || 'Campaign report'}</Txt>
    <div style={{position: 'absolute', left: 1250, top: 80, width: 40, height: 40, borderRadius: 20, background: C.SPARK}} />
    {rows.map((r, i) => {
      const near = Math.max(0, 1 - Math.abs(pos - i));
      return <div key={i} style={{opacity: seg(p, 0.02 + i * 0.03, 0.1 + i * 0.03)}}>
        <Txt x={120} y={y0 + i * rh + 34} size={52} color={near > 0.5 ? C.INK : C.SOFT} font={SANS} weight={near > 0.5 ? 600 : 400}>{r.label}</Txt>
        <Txt x={760} y={y0 + i * rh + 34} w={520} align="right" size={52} font={MONO} color={near > 0.5 ? C.INK : C.SOFT}>{r.value}</Txt>
        <div style={{position: 'absolute', left: 90, top: y0 + i * rh + rh - 4, width: 1220, height: 3, background: C.RULE}} />
      </div>;
    })}
    <div style={{position: 'absolute', left: 70, top: y0 + pos * rh + 8, width: 1260, height: rh - 16, borderRadius: 24, border: `4px solid ${C.INK}`,
      background: 'rgba(250,249,245,0.0)', transform: `scale(${1 + 0.02 * Math.sin(p * 30)})`}} />
  </Shadowed>;
};

const Paths: React.FC<K> = ({p, P}) => {
  const nodes = P.items.length >= 5 ? P.items.slice(0, 5).map(i => i.label) : ['Brief', 'Reel', 'Report', 'Email', 'Post'];
  const pos: [number, number][] = [[330, 540], [960, 540], [1590, 540], [960, 250], [960, 830]];
  const edges: [number, number][] = [[0, 1], [1, 2], [0, 3], [3, 2], [0, 4], [4, 2]];
  const curve = ([a, b]: [number, number]) => {
    const [x1, y1] = pos[a], [x2, y2] = pos[b];
    const mx = (x1 + x2) / 2;
    return `M${x1},${y1} C${mx},${y1} ${mx},${y2} ${x2},${y2}`;
  };
  const draw = seg(p, 0.08, 0.34);
  return <Shadowed x={110} y={90} w={1700} h={900} r={34} fill={C.DARK}>
    <svg style={{position: 'absolute', left: -110, top: -90}} width="1920" height="1080">
      {edges.map((e, i) => <path key={i} id={`e${i}`} d={curve(e)} fill="none" stroke={C.BAR1} strokeWidth="5" pathLength={1}
        strokeDasharray="1" strokeDashoffset={1 - draw} />)}
      {p > 0.34 && edges.map((e, i) => {
        const t = ((p - 0.34) * 2.4 + i * 0.17) % 1;
        const [x1, y1] = pos[e[0]], [x2, y2] = pos[e[1]];
        const mx = (x1 + x2) / 2;
        const u = 1 - t;
        const x = u * u * u * x1 + 3 * u * u * t * mx + 3 * u * t * t * mx + t * t * t * x2;
        const y = u * u * u * y1 + 3 * u * u * t * y1 + 3 * u * t * t * y2 + t * t * t * y2;
        return <circle key={i} cx={x} cy={y} r={13} fill={i % 2 ? C.ON_DARK : C.SPARK} />;
      })}
    </svg>
    {nodes.map((l, i) => {
      const [x, y] = pos[i];
      const hot = i === P.focus;
      return <div key={i} style={{position: 'absolute', left: x - 110 - 130, top: y - 90 - 48, width: 260, height: 96, borderRadius: 48,
        background: hot ? C.CARD : C.DARK2, color: hot ? C.INK : C.ON_DARK, fontFamily: SANS, fontSize: 48, fontWeight: 600,
        display: 'flex', alignItems: 'center', justifyContent: 'center', opacity: seg(p, 0.02 + i * 0.03, 0.1 + i * 0.03)}}>{l}</div>;
    })}
  </Shadowed>;
};

const DEFAULT_MARK = ['..#####..', '.#.....#.', '#..#.#..#', '#.......#', '#.#...#.#', '#..###..#', '.#.....#.', '..#####..'];
const Particles: React.FC<K> = ({p, P}) => {
  const bm = P.bitmap.length ? P.bitmap : DEFAULT_MARK;
  const cells: [number, number][] = [];
  bm.forEach((r, y) => r.split('').forEach((c, x) => { if (c === '#') cells.push([x, y]); }));
  const cols = Math.max(...bm.map(r => r.length)), rws = bm.length;
  const cs = Math.min(560 / rws, 900 / cols);
  const gx = 960 - (cols * cs) / 2, gy = 540 - (rws * cs) / 2 + 20;
  const a = seg(p, 0.1, 0.42);
  const rnd = (i: number, k: number) => { const s = Math.sin(i * 12.9898 + k * 78.233) * 43758.5453; return s - Math.floor(s); };
  return <Shadowed x={160} y={100} w={1600} h={880} r={34}>
    {P.heading && <Txt x={70} y={50} size={48} font={MONO} color={C.SOFT}>{P.heading}</Txt>}
    {cells.map(([cx, cy], i) => {
      const x0 = 200 + rnd(i, 1) * 1400, y0 = 180 + rnd(i, 2) * 740;
      const t = clamp((a - rnd(i, 3) * 0.3) / 0.7);
      const e = ease(t);
      const x = lerp(x0, gx + cx * cs + cs / 2, e) - 160, y = lerp(y0, gy + cy * cs + cs / 2, e) - 100;
      const r = cs * 0.36;
      return <div key={i} style={{position: 'absolute', left: x - r, top: y - r, width: 2 * r, height: 2 * r, borderRadius: r * 0.3,
        background: i % 7 === 3 ? C.SPARK : C.INK}} />;
    })}
    <Txt x={0} y={770} w={1600} align="center" size={56} o={seg(p, 0.42, 0.5)}>{P.sub || 'assembled'}</Txt>
  </Shadowed>;
};

const KINDS: Record<ShowTellCardProps['kind'], React.FC<K>> = {
  player: Player, search: Search, workspace: Workspace, tabs: Tabs, chart: Chart, dashboard: Dashboard, stack: Stack, dock: Dock,
  masked: Masked, elastic: Elastic, layout: Layout, reveal: Reveal, perspective: Perspective, focus: Focus, paths: Paths, particles: Particles,
};

export const ShowTellCard: React.FC<ShowTellCardProps> = (P) => {
  const frame = useCurrentFrame();
  const {fps, durationInFrames} = useVideoConfig();
  const f = P.onTwos ? frame - (frame % 2) : frame;           // stop-motion: hold every drawing two frames
  const p = clamp(f / Math.max(1, durationInFrames - 1));
  const Kind = KINDS[P.kind];
  return <AbsoluteFill style={{backgroundColor: C.STAGE, overflow: 'hidden'}}>
    <Kind p={p} f={f} fps={fps} P={P} />
  </AbsoluteFill>;
};

export const showTellCardDefaultProps: ShowTellCardProps = showTellCardSchema.parse({kind: 'search'});
