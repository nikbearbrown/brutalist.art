/**
 * illustrations/structural.tsx — the STRUCTURAL illustration family.
 *
 * WHAT THIS FAMILY IS (and what it is NOT)
 * ----------------------------------------
 * Structural illustrations diagram the PARTS OF A SYSTEM: layers of a stack, a
 * source feeding a destination, a set of peer tools. The beat *enumerates* —
 * it does not make an argument that moves. That is the dividing line:
 *
 *   STRUCTURAL (here)          the beat names the parts of a thing
 *   RHETORICAL (deckPatterns)  the beat asserts something that changes over time
 *                              (AttritionChain / DivergentFates / ScaleComparison
 *                               / BinaryBranch / Threshold — a different file)
 *
 * Do NOT merge these two families into one "pattern" enum. They live on
 * orthogonal axes; a beat picks a FAMILY first, then a component within it.
 * (See ILLUSTRATIONS.md for the decision tree.)
 *
 * PROVENANCE
 * ----------
 * Extracted and parameterized from the "Claude, For Teachers" reel
 * (youtube/claude-for-teachers/remotion-src/TeachersIllu.tsx) and the medhavy
 * MCP reel (youtube/mcp/remotion-src/Illustrations.tsx). The two flow scenes
 * from those reels (StandardsToCowork + ServerToCowork) were the SAME component
 * with different labels — they are merged here into one <SourceFlow>.
 *
 * LAWS EVERY COMPONENT HERE KEEPS
 * -------------------------------
 *  • ONE terracotta accent (CLAUDE.SPARK) per beat — if two things are orange,
 *    neither is the point. The accent marks the focal item / the "landed" state.
 *  • Pure function of useP() — no CSS transitions, no timers, no random().
 *  • Wrap in <IlluStage spark="…"> so the spark-line law is satisfied.
 *  • 1280×720 stage assumed (the reel canvas). Geometry is in those units.
 *
 * HOW TO ADAPT (starter-template contract)
 * ----------------------------------------
 * Change the PROPS, never the motion math. Each component's props are the only
 * things a new reel should touch. Worked examples are in the header of each.
 */
import React from 'react';
import { CLAUDE } from '../tokens/claude';
import { SERIF, SANS, MONO, clamp, remap, ease, useP } from './kit';

/* ==================================================================== *
 * LayerStack — staggered cards that stack up.                          *
 * -------------------------------------------------------------------- *
 * WHEN: the beat says "X is made of N layers / tiers / parts."         *
 * TEACHERS USE: "Three layers, not an app" (free tier / skills /       *
 *   connectors). The connectors card was the accent (spark left rail). *
 * PROPS:                                                               *
 *   layers   [{title, sub, accent?}]  — accent:true → terracotta rail  *
 *   caption? one-line clarifier pinned near the bottom                 *
 *   top?     first card's y (default 150)                              *
 * ADAPT: swap the layer list. Mark the ONE card that matters accent.   *
 * ==================================================================== */
export type Layer = { title: string; sub: string; accent?: boolean };
/**
 * `fillScale` (optional, 2026-10-26): widen the cards and grow their type. The
 * stack is 640 of 1280 wide but already spans ~66% of the stage height, so a
 * uniform transform overflows vertically and clips a card. Widening is the axis
 * that has room. Omitted or 1, geometry is unchanged.
 */
export const LayerStack: React.FC<{ layers: Layer[]; caption?: string; top?: number; fillScale?: number }> = ({ layers, caption, top = 150, fillScale }) => {
  const _k = fillScale ?? 1;
  const _w = Math.round(640 * _k);
  const _left = Math.round((1280 - _w) / 2);
  const p = useP();
  return (
    <>
      {layers.map((l, i) => {
        const t0 = 0.08 + i * (0.5 / Math.max(1, layers.length)); // spread appearance across the first half
        const lp = ease(remap(p, t0, t0 + 0.12, 0, 1));
        if (lp <= 0) return null;
        return (
          <div key={i} style={{
            position: 'absolute', left: _left, width: _w, top: top + i * 130 + (1 - lp) * 40,
            opacity: lp, background: '#FFFFFF', border: `1px solid ${CLAUDE.BORDER}`,
            borderLeft: `10px solid ${l.accent ? CLAUDE.SPARK : CLAUDE.INK}`,
            borderRadius: 14, padding: '20px 28px', boxShadow: '0 8px 24px rgba(61,57,41,0.10)',
          }}>
            <div style={{ fontFamily: SERIF, fontSize: 34 * _k, color: CLAUDE.INK }}>{l.title}</div>
            <div style={{ fontFamily: SANS, fontSize: 19 * _k, color: CLAUDE.INK_SOFT, marginTop: 4 }}>{l.sub}</div>
          </div>
        );
      })}
      {caption && (
        <div style={{ position: 'absolute', bottom: 96, left: 0, right: 0, textAlign: 'center', fontFamily: SANS, fontSize: 24, color: CLAUDE.INK_SOFT, opacity: remap(p, 0.72, 0.82, 0, 1) }}>
          {caption}
        </div>
      )}
    </>
  );
};

/* ==================================================================== *
 * SourceFlow — items fly from a source rack, along a drawn connector    *
 *   arc, into a receiving app window where they check off as they land. *
 * -------------------------------------------------------------------- *
 * WHEN: the beat says "data/content served FROM a source INTO a tool."  *
 * MERGES: TeachersIllu.StandardsToCowork ("Standards served as data")   *
 *   and Illustrations.ServerToCowork ("vetted books → Cowork"). Same    *
 *   component; only labels + tints differed.                            *
 * PROPS:                                                                 *
 *   sourceLabel   caption under the dark rack ("Learning Commons")      *
 *   feeds  [{label, tint?}] — the flying chips; first one defaults to   *
 *          the accent. Also listed in the window, checking off on land. *
 *   destApp       window chrome label ("Cowork")                        *
 *   destTitle     the window's serif task line ("plan Monday's lesson") *
 *   arcCaption?   mono note above the arc ("served as data, not prose") *
 *   settleLine?   final spark line inside the window ("scaffolded to…")  *
 * ADAPT: change the feed list + the four labels. Geometry is fixed.     *
 * ==================================================================== */
export type Feed = { label: string; tint?: string };
export const SourceFlow: React.FC<{
  sourceLabel: string; feeds: Feed[]; destApp: string; destTitle: string;
  arcCaption?: string; settleLine?: string; rackRows?: number;
}> = ({ sourceLabel, feeds, destApp, destTitle, arcCaption, settleLine, rackRows = 5 }) => {
  const p = useP();
  const W = 1280, H = 720;
  const srvX = 140, srvY = 250, srvW = 220, srvH = 290;
  const winX = 790, winY = 235, winW = 360, winH = 330;
  const plugP = remap(p, 0.05, 0.16, 0, 1);
  const startX = srvX + srvW, endX = winX;
  const tint = (i: number) => feeds[i].tint ?? (i === 0 ? CLAUDE.SPARK : CLAUDE.INK_SOFT);
  return (
    <>
      {/* source rack */}
      <div style={{ position: 'absolute', left: srvX, top: srvY, width: srvW, height: srvH, background: CLAUDE.INK, borderRadius: 14, padding: 16, boxShadow: '0 10px 30px rgba(61,57,41,0.25)' }}>
        {Array.from({ length: rackRows }, (_, i) => (
          <div key={i} style={{ height: 40, borderRadius: 8, background: '#4A4535', marginBottom: 9, display: 'flex', alignItems: 'center', padding: '0 12px', gap: 8 }}>
            <div style={{ width: 9, height: 9, borderRadius: 5, background: (p * 6 + i) % 1.4 < 0.7 ? CLAUDE.SPARK : '#6B6350' }} />
            <div style={{ flex: 1, height: 5, borderRadius: 3, background: '#5C5545' }} />
          </div>
        ))}
        <div style={{ position: 'absolute', bottom: -40, left: 0, right: 0, textAlign: 'center', fontFamily: MONO, fontSize: 16, color: CLAUDE.INK_SOFT }}>
          {sourceLabel}
        </div>
      </div>
      {/* connector arc (draws on via strokeDashoffset — deterministic) */}
      <svg width={W} height={H} style={{ position: 'absolute', inset: 0 }}>
        <path
          d={`M ${startX + 10} ${srvY + srvH / 2} C ${startX + 180} ${srvY + srvH / 2 - 60}, ${endX - 180} ${winY + winH / 2 - 60}, ${endX - 8} ${winY + winH / 2}`}
          stroke={CLAUDE.SPARK} strokeWidth={4} fill="none" strokeLinecap="round"
          strokeDasharray={600} strokeDashoffset={600 * (1 - ease(plugP))}
        />
      </svg>
      {arcCaption && (
        <div style={{ position: 'absolute', left: (startX + endX) / 2 - 90, top: srvY - 46, fontFamily: MONO, fontSize: 17, color: CLAUDE.SPARK, opacity: remap(p, 0.12, 0.18, 0, 1) }}>
          {arcCaption}
        </div>
      )}
      {/* flying feeds — closed-form position from p (no accumulated state) */}
      {feeds.map((b, i) => {
        const t0 = 0.18 + i * (0.6 / Math.max(1, feeds.length));
        const bp = ease(remap(p, t0, t0 + 0.17, 0, 1));
        if (bp <= 0 || bp >= 1) return null;
        const bx = remap(bp, 0, 1, startX - 30, endX + 20);
        const by = srvY + 40 + i * 52 + Math.sin(bp * Math.PI) * -70 + bp * (winY + 70 + i * 40 - (srvY + 40 + i * 52));
        return (
          <div key={i} style={{
            position: 'absolute', left: bx, top: by, padding: '7px 12px',
            background: CLAUDE.PAGE, border: `2px solid ${tint(i)}`, borderLeftWidth: 8,
            borderRadius: 6, fontFamily: SANS, fontSize: 15, color: CLAUDE.INK,
            boxShadow: '0 4px 12px rgba(61,57,41,0.15)',
            transform: `rotate(${Math.sin(bp * 7 + i) * 6}deg)`,
          }}>
            {b.label}
          </div>
        );
      })}
      {/* receiving window */}
      <div style={{ position: 'absolute', left: winX, top: winY, width: winW, height: winH, background: '#FAF9F5', borderRadius: 14, border: `1px solid ${CLAUDE.BORDER}`, boxShadow: '0 10px 30px rgba(61,57,41,0.12)', padding: 16 }}>
        <div style={{ display: 'flex', gap: 6, marginBottom: 12 }}>
          {['#EC6A5E', '#F4BF4F', '#61C554'].map((c) => (
            <div key={c} style={{ width: 10, height: 10, borderRadius: 5, background: c }} />
          ))}
          <div style={{ marginLeft: 12, fontFamily: SANS, fontSize: 14, color: CLAUDE.INK_SOFT }}>{destApp}</div>
        </div>
        <div style={{ fontFamily: SERIF, fontSize: 20, color: CLAUDE.INK, marginBottom: 10 }}>
          <span style={{ color: CLAUDE.SPARK }}>✳</span> {destTitle}
        </div>
        <div style={{ fontFamily: MONO, fontSize: 14, color: CLAUDE.INK_SOFT, lineHeight: 1.95 }}>
          {feeds.map((b, i) => {
            const landed = p > 0.18 + i * (0.6 / Math.max(1, feeds.length)) + 0.17;
            return <div key={i} style={{ opacity: landed ? 1 : 0.18 }}>{landed ? '✓' : '·'} {b.label}</div>;
          })}
          {settleLine && (
            <div style={{ color: CLAUDE.SPARK, opacity: remap(p, 0.88, 0.95, 0, 1) }}>✳ {settleLine}</div>
          )}
        </div>
      </div>
    </>
  );
};

/* ==================================================================== *
 * ChipGrid — peer items snap into a grid, dot turns terracotta on land. *
 * -------------------------------------------------------------------- *
 * WHEN: the beat says "here is a SET of N peer things" (tools, sources, *
 *   options) with no internal ordering or flow.                        *
 * TEACHERS USE: "Nine tools, day one" (Canva/MagicSchool/Diffit/…).     *
 * PROPS:                                                                *
 *   items    string[]  — chip labels                                   *
 *   cols?    columns (default 3)                                       *
 *   caption? one-line clarifier near the bottom                        *
 * ADAPT: swap the item list; grid re-flows. Each dot lights spark when *
 *   its chip has fully settled — the "landed" accent.                  *
 * ==================================================================== */
/**
 * `fillScale` (optional, 2026-10-26): grow the chips. A 2-column grid is 646 of
 * 1280 wide and ~32% of the stage height, which is the worst underfill in the
 * family, so both axes have room here. Omitted or 1, geometry is unchanged.
 */
export const ChipGrid: React.FC<{ items: string[]; cols?: number; caption?: string; fillScale?: number }> = ({ items, cols = 3, caption, fillScale }) => {
  const p = useP();
  const _k = fillScale ?? 1;
  const cw = Math.round(300 * _k), ch = Math.round(96 * (1 + (_k - 1) * 0.7));
  const gapX = 46, gapY = Math.round(42 * _k);
  const gridW = cols * cw + (cols - 1) * gapX;
  const x0 = (1280 - gridW) / 2, y0 = 168;
  const step = 0.7 / Math.max(1, items.length); // spread over first 70%
  return (
    <>
      {items.map((t, i) => {
        const t0 = 0.07 + i * step;
        const tp = ease(remap(p, t0, t0 + 0.09, 0, 1));
        if (tp <= 0) return null;
        const cx = x0 + (i % cols) * (cw + gapX);
        const cy = y0 + Math.floor(i / cols) * (ch + gapY);
        return (
          <div key={t} style={{
            position: 'absolute', left: cx, top: cy + (1 - tp) * 26, width: cw, height: ch,
            opacity: tp, background: '#FFFFFF', border: `1px solid ${CLAUDE.BORDER}`,
            borderRadius: 14, boxShadow: '0 8px 22px rgba(61,57,41,0.09)',
            display: 'flex', alignItems: 'center', gap: 14, padding: '0 20px',
          }}>
            <div style={{ width: 12, height: 12, borderRadius: 7, background: tp >= 1 ? CLAUDE.SPARK : CLAUDE.BORDER }} />
            <div style={{ fontFamily: SANS, fontSize: 22 * _k, fontWeight: 600, color: CLAUDE.INK }}>{t}</div>
          </div>
        );
      })}
      {caption && (
        <div style={{ position: 'absolute', bottom: 92, left: 0, right: 0, textAlign: 'center', fontFamily: SANS, fontSize: 24, color: CLAUDE.INK_SOFT, opacity: remap(p, 0.78, 0.88, 0, 1) }}>
          {caption}
        </div>
      )}
    </>
  );
};

/* ==================================================================== *
 * PredictCard — commit-before-reveal. A question, a drawn underline,    *
 *   then a "commit to an answer" nudge. No UI, no system diagram.       *
 * -------------------------------------------------------------------- *
 * WHEN: a pedagogy beat that asks the viewer to predict before the      *
 *   answer lands (retrieval-practice move). Shared across brands.       *
 * PROPS: question, commit                                               *
 * NOTE: kept here because it is a pure illustration, but it is a        *
 *   PEDAGOGY device, not a structural diagram — the odd one out.        *
 * ==================================================================== */
export const PredictCard: React.FC<{ question: string; commit: string }> = ({ question, commit }) => {
  const p = useP();
  const qo = remap(p, 0.05, 0.15, 0, 1);
  const lo = ease(remap(p, 0.3, 0.5, 0, 1));
  const co = remap(p, 0.55, 0.65, 0, 1);
  return (
    <>
      <div style={{ position: 'absolute', top: 250, left: 0, right: 0, textAlign: 'center', fontFamily: SERIF, fontSize: 62, color: CLAUDE.INK, opacity: qo, padding: '0 140px', lineHeight: 1.2 }}>
        {question}
      </div>
      <svg width={1280} height={720} style={{ position: 'absolute', inset: 0 }}>
        <line x1={440} y1={450} x2={440 + 400 * lo} y2={450} stroke={CLAUDE.SPARK} strokeWidth={5} strokeLinecap="round" />
      </svg>
      <div style={{ position: 'absolute', top: 480, left: 0, right: 0, textAlign: 'center', fontFamily: SANS, fontSize: 26, color: CLAUDE.INK_SOFT, opacity: co }}>
        {commit}
      </div>
    </>
  );
};
