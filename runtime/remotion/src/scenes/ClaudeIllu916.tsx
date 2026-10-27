/**
 * ClaudeIllu916.tsx — portrait 9:16 (1080×1920) versions of the five illustration
 * patterns the fellows' weekly reels use.
 *
 * These are NOT scaled-down landscape renders. Per the REFLOW rule they are native
 * portrait layouts: fill the width, distribute content down the height.
 *
 * Geometry follows the house convention set by ClaudeWindow916:
 *   canvas 1080×1920 · top safe 230px · bottom safe from 1440px
 *   active band 230–1440 (1210px) · content width 950px, centred
 * Top and bottom reserves exist because the Shorts player overlays UI there.
 *
 * Schemas are re-exported unchanged from the landscape components, so a beat sheet
 * needs no prop edits to render portrait.
 *
 * Compositions: ClaudeScienceLayerStack916 | ClaudeScienceSourceFlow916 |
 *               ClaudeScienceChipGrid916 | CwcConceptCard916 | ClaudeCodeBeat916
 */
import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring } from 'remotion';
import { CLAUDE, CLAUDE_FONT } from '../tokens/claude';
import {
  claudeScienceLayerStackSchema, claudeScienceSourceFlowSchema, claudeScienceChipGridSchema,
} from '../ClaudeScienceIllu';
import type {
  ClaudeScienceLayerStackProps, ClaudeScienceSourceFlowProps, ClaudeScienceChipGridProps,
} from '../ClaudeScienceIllu';
import { cwcConceptCardSchema } from './CwcShared';
import type { CwcConceptCardProps } from './CwcShared';
import { claudeCodeBeatSchema } from './ClaudeCodeBeat';
import type { ClaudeCodeBeatProps } from './ClaudeCodeBeat';

const SERIF = CLAUDE_FONT.serif;
const SANS  = CLAUDE_FONT.ui;
const MONO  = CLAUDE_FONT.mono;
const STAGE = '#F2F0E9';

const TOP_SAFE = 230;
const BOT_SAFE = 1440;
const BAND_H   = BOT_SAFE - TOP_SAFE;
const WIDTH    = 950;
const LEFT     = (1080 - WIDTH) / 2;

const clamp = (v: number, a: number, b: number) => Math.min(b, Math.max(a, v));

/**
 * Stagger progress for element `i` (7 frames apart, matching landscape timing).
 *
 * PURE on purpose: it takes frame/fps rather than calling Remotion hooks, because
 * these layouts call it inside .map() and a hook there breaks the Rules of Hooks.
 * Each component reads the clock ONCE at its top and threads it through.
 */
const inAt = (frame: number, fps: number, i: number) =>
  clamp(spring({ frame: frame - i * 7, fps, config: { damping: 28, stiffness: 140, mass: 0.8 } }), 0, 1);

/** Reads the clock once; returns the stagger function bound to it. */
const useStagger = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (i: number) => inAt(frame, fps, i);
};

const Spark: React.FC<{ size?: number }> = ({ size = 30 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" style={{ flexShrink: 0 }}>
    {Array.from({ length: 8 }, (_, i) => (
      <line key={i} x1={12} y1={12}
        x2={12 + 10 * Math.cos((i * Math.PI) / 4 + 0.2)}
        y2={12 + 10 * Math.sin((i * Math.PI) / 4 + 0.2)}
        stroke={CLAUDE.SPARK} strokeWidth={3.2} strokeLinecap="round" />
    ))}
  </svg>
);

/** Cream stage + the spark headline pinned at the top of the active band. */
const Stage916: React.FC<{ spark: string; children: React.ReactNode }> = ({ spark, children }) => {
  const op = useStagger()(0);
  return (
    <AbsoluteFill style={{ background: STAGE }}>
      <div style={{
        position: 'absolute', top: TOP_SAFE - 130, left: LEFT, width: WIDTH,
        display: 'flex', alignItems: 'flex-start', gap: 14, opacity: op,
      }}>
        <div style={{ marginTop: 10 }}><Spark size={34} /></div>
        <span style={{ fontFamily: SERIF, fontSize: 52, lineHeight: 1.15, color: CLAUDE.INK }}>
          {spark}
        </span>
      </div>
      {children}
    </AbsoluteFill>
  );
};

const Caption: React.FC<{ text?: string; i: number }> = ({ text, i }) => {
  const op = useStagger()(i);
  if (!text) return null;
  return (
    <div style={{
      position: 'absolute', top: BOT_SAFE + 24, left: LEFT, width: WIDTH,
      fontFamily: SANS, fontSize: 30, lineHeight: 1.45, color: '#6b6555',
      textAlign: 'center', opacity: op,
    }}>{text}</div>
  );
};

// ── ClaudeScienceLayerStack916 ─────────────────────────────────────────────
export const claudeScienceLayerStack916Schema = claudeScienceLayerStackSchema;
export const ClaudeScienceLayerStack916: React.FC<ClaudeScienceLayerStackProps> = ({ layers, caption, sparkLine }) => {
  const at = useStagger();
  const n = Math.max(layers.length, 1);
  const gap = 34;
  const h = Math.min(230, (BAND_H - gap * (n - 1)) / n);
  const total = h * n + gap * (n - 1);
  const top0 = TOP_SAFE + (BAND_H - total) / 2;
  return (
    <Stage916 spark={sparkLine}>
      {layers.map((l, i) => {
        const op = at(i + 1);
        return (
          <div key={i} style={{
            position: 'absolute', top: top0 + i * (h + gap), left: LEFT, width: WIDTH, height: h,
            background: CLAUDE.CARD, borderRadius: 20,
            borderLeft: `14px solid ${l.accent ? CLAUDE.SPARK : '#3D3929'}`,
            boxShadow: '0 12px 40px rgba(61,57,41,0.13)',
            padding: '26px 34px', boxSizing: 'border-box',
            display: 'flex', flexDirection: 'column', justifyContent: 'center',
            opacity: op, transform: `translateY(${(1 - op) * 16}px)`,
          }}>
            <div style={{ fontFamily: SERIF, fontSize: 46, color: CLAUDE.INK, marginBottom: 10 }}>{l.title}</div>
            <div style={{ fontFamily: SANS, fontSize: 28, lineHeight: 1.4, color: '#6b6555' }}>{l.sub}</div>
          </div>
        );
      })}
      <Caption text={caption} i={n + 1} />
    </Stage916>
  );
};

// ── ClaudeScienceChipGrid916 ───────────────────────────────────────────────
export const claudeScienceChipGrid916Schema = claudeScienceChipGridSchema;
export const ClaudeScienceChipGrid916: React.FC<ClaudeScienceChipGridProps> = ({ items, caption, sparkLine }) => {
  const at = useStagger();
  // Portrait always stacks one per row — two columns at this width would force
  // 2-3 line wraps and shrink the type below the mobile legibility floor.
  const n = Math.max(items.length, 1);
  const gap = 26;
  const h = Math.min(170, (BAND_H - gap * (n - 1)) / n);
  const total = h * n + gap * (n - 1);
  const top0 = TOP_SAFE + (BAND_H - total) / 2;
  return (
    <Stage916 spark={sparkLine}>
      {items.map((t, i) => {
        const op = at(i + 1);
        return (
          <div key={i} style={{
            position: 'absolute', top: top0 + i * (h + gap), left: LEFT, width: WIDTH, height: h,
            background: CLAUDE.CARD, borderRadius: 18,
            boxShadow: '0 10px 34px rgba(61,57,41,0.12)',
            padding: '0 34px', boxSizing: 'border-box',
            display: 'flex', alignItems: 'center', gap: 20,
            opacity: op, transform: `translateY(${(1 - op) * 14}px)`,
          }}>
            <div style={{ width: 14, height: 14, borderRadius: 7, background: CLAUDE.SPARK, flexShrink: 0 }} />
            <span style={{ fontFamily: SANS, fontWeight: 700, fontSize: 34, lineHeight: 1.3, color: CLAUDE.INK }}>{t}</span>
          </div>
        );
      })}
      <Caption text={caption} i={n + 1} />
    </Stage916>
  );
};

// ── ClaudeScienceSourceFlow916 ─────────────────────────────────────────────
// Landscape runs source → arc → destination left-to-right. Portrait runs it
// top-to-bottom, which is the natural reading order on a phone.
export const claudeScienceSourceFlow916Schema = claudeScienceSourceFlowSchema;
export const ClaudeScienceSourceFlow916: React.FC<ClaudeScienceSourceFlowProps> = ({
  sourceLabel, feeds, destApp, destTitle, arcCaption, settleLine, sparkLine,
}) => {
  const at = useStagger();
  const srcOp = at(1);
  const arcOp = at(2);
  const dstOp = at(3);
  const setOp = at(feeds.length + 4);

  // Centre the whole group in the active band rather than pinning it to the top —
  // otherwise the composition hugs the header and leaves the lower half empty.
  const SRC_H = 220;
  const GAP   = 118;                       // connector + its caption
  const cardH = 250 + feeds.length * 56 + (settleLine ? 56 : 0);
  const top0  = TOP_SAFE + Math.max(0, (BAND_H - (SRC_H + GAP + cardH)) / 2);
  const capY  = top0 + SRC_H + 40;

  return (
    <Stage916 spark={sparkLine}>
      {/* source block */}
      <div style={{
        position: 'absolute', top: top0, left: LEFT, width: WIDTH, height: SRC_H,
        background: '#3A3627', borderRadius: 22, opacity: srcOp,
        transform: `translateY(${(1 - srcOp) * 16}px)`,
        display: 'flex', alignItems: 'center', justifyContent: 'center',
      }}>
        <span style={{ fontFamily: MONO, fontSize: 38, color: '#CFC9B6' }}>{sourceLabel}</span>
      </div>

      {/* Connector drawn as two segments so the caption sits BETWEEN them —
          a single line would strike straight through the text. */}
      <div style={{ position: 'absolute', top: top0 + SRC_H, left: 1080 / 2 - 2, width: 4, height: 36,
        background: CLAUDE.SPARK, opacity: arcOp }} />
      {arcCaption ? (
        <div style={{
          position: 'absolute', top: capY, left: LEFT, width: WIDTH,
          fontFamily: MONO, fontSize: 26, lineHeight: 1.3, color: CLAUDE.SPARK,
          textAlign: 'center', opacity: arcOp,
        }}>{arcCaption}</div>
      ) : null}
      <div style={{ position: 'absolute', top: capY + 44, left: 1080 / 2 - 2, width: 4, height: 34,
        background: CLAUDE.SPARK, opacity: arcOp }} />

      {/* destination card */}
      <div style={{
        position: 'absolute', top: top0 + SRC_H + GAP, left: LEFT, width: WIDTH,
        background: CLAUDE.CARD, borderRadius: 22, border: `1px solid ${CLAUDE.BORDER}`,
        boxShadow: '0 12px 44px rgba(61,57,41,0.14)', padding: '30px 36px 36px',
        boxSizing: 'border-box', opacity: dstOp, transform: `translateY(${(1 - dstOp) * 16}px)`,
      }}>
        <div style={{ fontFamily: SANS, fontSize: 28, color: '#6b6555', marginBottom: 16 }}>{destApp}</div>
        <div style={{ display: 'flex', alignItems: 'flex-start', gap: 12, marginBottom: 24 }}>
          <div style={{ marginTop: 8 }}><Spark size={30} /></div>
          <span style={{ fontFamily: SERIF, fontSize: 44, lineHeight: 1.2, color: CLAUDE.INK }}>{destTitle}</span>
        </div>
        {feeds.map((f, i) => (
          <div key={i} style={{
            fontFamily: MONO, fontSize: 30, lineHeight: 1.85, color: '#4a4535', opacity: at(i + 4),
          }}>✓ {f.label}</div>
        ))}
        {settleLine ? (
          <div style={{
            fontFamily: MONO, fontSize: 30, lineHeight: 1.85, color: CLAUDE.SPARK, opacity: setOp, marginTop: 8,
          }}>✳ {settleLine}</div>
        ) : null}
      </div>
    </Stage916>
  );
};

// ── CwcConceptCard916 ──────────────────────────────────────────────────────
export const cwcConceptCard916Schema = cwcConceptCardSchema;
export const CwcConceptCard916: React.FC<CwcConceptCardProps> = ({ eyebrow, title, body, sparkLine, fillScale }) => {
  // Portrait width is already at the safe edge, so only the type scales.
  const _fs = fillScale ?? 1;
  const at = useStagger();
  const eOp = at(0);
  const tOp = at(1);
  const bOp = at(3);
  const sOp = at(5);
  return (
    <AbsoluteFill style={{ background: STAGE }}>
      <div style={{ position: 'absolute', top: TOP_SAFE + 170, left: LEFT, width: WIDTH }}>
        <div style={{
          fontFamily: SANS, fontSize: 26 * _fs, letterSpacing: 5, color: '#8a8474',
          textTransform: 'uppercase', opacity: eOp, marginBottom: 26,
        }}>{eyebrow}</div>
        <div style={{
          fontFamily: SERIF, fontSize: 78 * _fs, lineHeight: 1.12, fontWeight: 700, color: CLAUDE.INK,
          opacity: tOp, transform: `translateY(${(1 - tOp) * 14}px)`, marginBottom: 34,
        }}>{title}</div>
        <div style={{
          fontFamily: SANS, fontSize: 34 * _fs, lineHeight: 1.5, color: '#6b6555', opacity: bOp,
        }}>{body}</div>
      </div>
      {sparkLine ? (
        <div style={{
          position: 'absolute', top: BOT_SAFE - 60, left: LEFT, width: WIDTH,
          display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 14, opacity: sOp,
        }}>
          <Spark size={30} />
          <span style={{ fontFamily: SERIF, fontSize: 40, fontStyle: 'italic', color: CLAUDE.INK }}>{sparkLine}</span>
        </div>
      ) : null}
    </AbsoluteFill>
  );
};

// ── ClaudeCodeBeat916 ──────────────────────────────────────────────────────
// Code cannot reflow, so portrait sizes the mono type to the LONGEST line and
// lets the panel take the height it needs. A wrapped code line is unreadable.
export const claudeCodeBeat916Schema = claudeCodeBeatSchema;
export const ClaudeCodeBeat916: React.FC<ClaudeCodeBeatProps> = ({ title, code, sparkLine }) => {
  const at = useStagger();
  const pOp = at(0);
  const sOp = at(2);
  const lines = code.split('\n');
  const longest = lines.reduce((m, l) => Math.max(m, l.length), 1);
  const inner = WIDTH - 56;                       // panel padding
  const fs = clamp(inner / (longest * 0.6), 13, 27);
  return (
    <AbsoluteFill style={{ background: '#FAF9F5' }}>
      <div style={{
        position: 'absolute', top: TOP_SAFE + 40, left: LEFT, width: WIDTH,
        background: CLAUDE.CARD, borderRadius: 20, border: `1px solid ${CLAUDE.BORDER}`,
        boxShadow: '0 12px 44px rgba(61,57,41,0.13)', overflow: 'hidden',
        opacity: pOp, transform: `scale(${0.97 + 0.03 * pOp})`,
      }}>
        <div style={{
          background: STAGE, borderBottom: `1px solid ${CLAUDE.BORDER}`,
          padding: '16px 24px', display: 'flex', alignItems: 'center', gap: 12,
        }}>
          <div style={{ display: 'flex', gap: 8 }}>
            {['#E06C5A', '#E0B44A', '#7FB069'].map((c) => (
              <div key={c} style={{ width: 14, height: 14, borderRadius: 7, background: c }} />
            ))}
          </div>
          <span style={{ fontFamily: MONO, fontSize: 24, color: '#6b6555' }}>{title}</span>
        </div>
        <div style={{ padding: '24px 28px 30px' }}>
          {lines.map((l, i) => {
            const op = at(i * 0.35 + 1);
            return (
              <div key={i} style={{
                fontFamily: MONO, fontSize: fs, lineHeight: 1.75, color: CLAUDE.INK,
                whiteSpace: 'pre', opacity: op,
              }}>{l || ' '}</div>
            );
          })}
        </div>
      </div>
      {sparkLine ? (
        <div style={{
          position: 'absolute', top: BOT_SAFE - 40, left: LEFT, width: WIDTH,
          display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 14, opacity: sOp,
        }}>
          <Spark size={28} />
          <span style={{ fontFamily: SERIF, fontSize: 38, fontStyle: 'italic', color: CLAUDE.INK }}>{sparkLine}</span>
        </div>
      ) : null}
    </AbsoluteFill>
  );
};
