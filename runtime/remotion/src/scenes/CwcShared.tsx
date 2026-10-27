import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring } from 'remotion';
import { z } from 'zod';
import { CLAUDE, CLAUDE_FONT } from '../tokens/claude';

/**
 * Shared utility scenes for CWC (Code with Claude) workshop videos.
 * Used for question framing, concept explanation, and exclusion beats.
 */

const SERIF = CLAUDE_FONT.serif;
const SANS = CLAUDE_FONT.ui;
const clamp = (v: number, a: number, b: number) => Math.min(b, Math.max(a, v));


// ─── CwcExclusions ─────────────────────────────────────────────────────────
// Honesty beat: "What this video is not covering"

export const cwcExclusionsSchema = z.object({
  title: z.string().default('What this doesn\'t cover'),
  items: z.array(z.string()).min(1).max(6),
  sparkLine: z.string().default('Scope is honest.'),
});
export type CwcExclusionsProps = z.infer<typeof cwcExclusionsSchema>;

export const CwcExclusions: React.FC<CwcExclusionsProps> = ({ title, items, sparkLine }) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  const PAD_X = width * 0.10;
  const PAD_Y = height * 0.10;

  const titleIn = spring({ frame, fps, config: { damping: 30, stiffness: 120, mass: 0.8 } });
  const sparkIn = spring({ frame: frame - items.length * 18 - 20, fps, config: { damping: 28, stiffness: 100, mass: 0.8 } });

  return (
    <AbsoluteFill style={{ background: CLAUDE.PAGE, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
      <div style={{
        width: width * 0.72, maxWidth: 900,
        background: CLAUDE.CARD,
        border: `1.5px solid ${CLAUDE.BORDER}`,
        borderRadius: 18,
        overflow: 'hidden',
        boxShadow: '0 16px 48px rgba(61,57,41,0.10)',
        opacity: clamp(titleIn, 0, 1),
        transform: `scale(${0.9 + 0.1 * clamp(titleIn, 0, 1)})`,
      }}>
        {/* Header */}
        <div style={{
          background: CLAUDE.PAGE,
          borderBottom: `1px solid ${CLAUDE.BORDER}`,
          padding: '24px 36px',
          display: 'flex', alignItems: 'center', gap: 14,
        }}>
          <span style={{ fontFamily: SERIF, fontSize: height * 0.028, fontWeight: 700, color: CLAUDE.INK }}>
            {title}
          </span>
        </div>
        {/* Items */}
        <div style={{ padding: '28px 36px 32px' }}>
          {items.map((item, i) => {
            const itemIn = spring({ frame: frame - 10 - i * 18, fps, config: { damping: 26, stiffness: 100, mass: 0.9 } });
            return (
              <div key={i} style={{
                display: 'flex', alignItems: 'flex-start', gap: 18,
                marginBottom: i < items.length - 1 ? 20 : 0,
                opacity: clamp(itemIn, 0, 1),
                transform: `translateY(${(1 - clamp(itemIn, 0, 1)) * 10}px)`,
              }}>
                <span style={{ fontFamily: SANS, fontSize: height * 0.018, color: CLAUDE.GHOST, flexShrink: 0, marginTop: 2 }}>
                  ✕
                </span>
                <span style={{ fontFamily: SANS, fontSize: height * 0.018, color: CLAUDE.INK_SOFT, lineHeight: 1.5 }}>
                  {item}
                </span>
              </div>
            );
          })}
        </div>
      </div>

      {/* Spark line */}
      <div style={{
        position: 'absolute', left: 0, right: 0, bottom: height * 0.06,
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        gap: 10, opacity: clamp(sparkIn, 0, 1),
      }}>
        <span style={{ fontFamily: SERIF, fontSize: height * 0.022, fontStyle: 'italic', color: CLAUDE.INK }}>
          {sparkLine}
        </span>
      </div>
    </AbsoluteFill>
  );
};

// ─── CwcConceptCard ─────────────────────────────────────────────────────────
// Generic concept explanation beat — title + body + spark line

export const cwcConceptCardSchema = z.object({
  eyebrow: z.string().default(''),
  title: z.string().default('Concept'),
  body: z.string().default(''),
  sparkLine: z.string().default(''),
  /**
   * Optional (2026-10-26): scale the content box to satisfy the canvas-fill
   * law. The landscape card widens from its 0.76-of-frame default and its type
   * grows with it; the 9:16 variant, whose width is already at the safe edge,
   * scales type only. Omitted or 1, nothing changes.
   */
  fillScale: z.number().optional(),
});
export type CwcConceptCardProps = z.infer<typeof cwcConceptCardSchema>;

export const CwcConceptCard: React.FC<CwcConceptCardProps> = ({ eyebrow, title, body, sparkLine, fillScale }) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  const PAD_X = width * 0.10;
  // Type scales with the card so a wider card is not just more whitespace.
  const tScale   = fillScale ?? 1;
  const cardFrac = 0.76 * tScale;
  const cardIn = spring({ frame, fps, config: { damping: 28, stiffness: 110, mass: 0.9 } });
  const bodyIn = spring({ frame: frame - 20, fps, config: { damping: 26, stiffness: 100, mass: 0.9 } });
  const sparkIn = spring({ frame: frame - 50, fps, config: { damping: 28, stiffness: 100, mass: 0.8 } });

  return (
    <AbsoluteFill style={{ background: CLAUDE.PAGE, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: 0 }}>
      <div style={{
        width: width * cardFrac,
        opacity: clamp(cardIn, 0, 1),
        transform: `translateY(${(1 - clamp(cardIn, 0, 1)) * 12}px)`,
      }}>
        {eyebrow && (
          <div style={{
            fontFamily: SANS, fontSize: height * 0.013 * tScale, fontWeight: 700,
            letterSpacing: 3, textTransform: 'uppercase' as const,
            color: CLAUDE.INK_SOFT, marginBottom: 16,
          }}>
            {eyebrow}
          </div>
        )}
        <div style={{
          fontFamily: SERIF, fontSize: height * 0.044 * tScale, fontWeight: 700,
          color: CLAUDE.INK, letterSpacing: '-0.02em', lineHeight: 1.15,
          marginBottom: 28,
        }}>
          {title}
        </div>
        <div style={{
          fontFamily: SANS, fontSize: height * 0.022 * tScale,
          color: CLAUDE.INK_SOFT, lineHeight: 1.65,
          opacity: clamp(bodyIn, 0, 1),
          transform: `translateY(${(1 - clamp(bodyIn, 0, 1)) * 8}px)`,
        }}>
          {body}
        </div>
      </div>

      {sparkLine && (
        <div style={{
          position: 'absolute', left: 0, right: 0, bottom: height * 0.06,
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          gap: 10, opacity: clamp(sparkIn, 0, 1),
        }}>
          <span style={{ fontFamily: SERIF, fontSize: height * 0.022, fontStyle: 'italic', color: CLAUDE.INK }}>
            {sparkLine}
          </span>
        </div>
      )}
    </AbsoluteFill>
  );
};

// ─── Schema re-exports for Root.tsx registration ────────────────────────────
// Additional CWC schemas for scenes that are just a CwcConceptCard variant
export const cwcMemoryQuestionSchema = cwcConceptCardSchema;
export const CwcMemoryQuestion = CwcConceptCard;

export const cwcSessionIsolationSchema = cwcConceptCardSchema;
export const CwcSessionIsolation = CwcConceptCard;

export const cwcMemoryProgressionSchema = cwcConceptCardSchema;
export const CwcMemoryProgression = CwcConceptCard;

export const cwcEvalQuestionSchema = cwcConceptCardSchema;
export const CwcEvalQuestion = CwcConceptCard;

export const cwcTwoLayerEvalSchema = cwcConceptCardSchema;
export const CwcTwoLayerEval = CwcConceptCard;

export const cwcVariantAccumulationSchema = cwcConceptCardSchema;
export const CwcVariantAccumulation = CwcConceptCard;

export const cwcOrchestrationQuestionSchema = cwcConceptCardSchema;
export const CwcOrchestrationQuestion = CwcConceptCard;

export const cwcFanOutConceptSchema = cwcConceptCardSchema;
export const CwcFanOutConcept = CwcConceptCard;

export const cwcSpreadMechanismSchema = cwcConceptCardSchema;
export const CwcSpreadMechanism = CwcConceptCard;

export const cwcDecompositionQuestionSchema = cwcConceptCardSchema;
export const CwcDecompositionQuestion = CwcConceptCard;

export const cwcThreeLeversSchema = cwcConceptCardSchema;
export const CwcThreeLevers = CwcConceptCard;

export const cwcSplitMechanismSchema = cwcConceptCardSchema;
export const CwcSplitMechanism = CwcConceptCard;

export const cwcModelQuestionSchema = cwcConceptCardSchema;
export const CwcModelQuestion = CwcConceptCard;

export const cwcParetoExplainedSchema = cwcConceptCardSchema;
export const CwcParetoExplained = CwcConceptCard;

export const cwcSweepAccumulationSchema = cwcConceptCardSchema;
export const CwcSweepAccumulation = CwcConceptCard;
