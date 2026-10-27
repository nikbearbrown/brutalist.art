import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring } from 'remotion';
import { claudeWindowSchema } from './ClaudeWindow';
import type { ClaudeWindowProps } from './ClaudeWindow';
import { CLAUDE, CLAUDE_FONT } from '../tokens/claude';

/**
 * ClaudeWindow916 — portrait 9:16 (1080×1920) version of ClaudeWindow.
 * Same schema. Card fills portrait width (~88% = ~950px).
 * Safe zone: top 12% (~230px) and bottom 25% (~480px) reserved for platform UI.
 * Card is centered in the active band (230–1440px), max ~900px tall.
 * Per REFLOW rule: fill the width, distribute content down the height.
 */

export const claudeWindow916Schema = claudeWindowSchema;
export type ClaudeWindow916Props = ClaudeWindowProps;

const SERIF = CLAUDE_FONT.serif;
const SANS = CLAUDE_FONT.ui;
const MONO = CLAUDE_FONT.mono;
const clamp = (v: number, a: number, b: number) => Math.min(b, Math.max(a, v));


export const ClaudeWindow916: React.FC<ClaudeWindow916Props> = ({
  view, artifactTitle, artifactHeading, artifactLines, sparkLine, numbered = true, fillScale,
}) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  const cardIn = spring({ frame,        fps, config: { damping: 28, stiffness: 140, mass: 0.8 } });
  const headIn = spring({ frame: frame - 8, fps, config: { damping: 28, stiffness: 140, mass: 0.8 } });
  const sparkIn = spring({ frame: frame - ((artifactLines?.length ?? 0) + 3) * 7, fps, config: { damping: 28, stiffness: 140, mass: 0.8 } });

  const lines = artifactLines ?? [];

  // Portrait layout — card fills ~90% of width
  const CARD_W = width * 0.90;
  const PAD_X = (width - CARD_W) / 2;
  const FONT_HEADING = height * 0.024;  // ~46px at 1920
  const _fs = fillScale ?? 1;
  const FONT_LINE = height * 0.017 * _fs;     // ~33px at 1920
  // Pre-formatted content (numbered:false) cannot wrap without destroying its
  // column alignment, so size the mono type to the LONGEST line instead.
  const longest = (artifactLines ?? []).reduce((m, l) => Math.max(m, l.length), 1);
  const FONT_PRE = Math.min(FONT_LINE, (CARD_W - 130) / (longest * 0.6));
  const FONT_TITLE_BAR = height * 0.018 * _fs;

  if (view === 'blank') {
    return <AbsoluteFill style={{ background: CLAUDE.PAGE }} />;
  }

  return (
    <AbsoluteFill style={{ background: '#F2F0E9', alignItems: 'center', justifyContent: 'center', flexDirection: 'column', gap: 0 }}>
      {/* Artifact card */}
      <div style={{
        width: CARD_W,
        background: CLAUDE.CARD,
        borderRadius: 18,
        boxShadow: '0 12px 48px rgba(61,57,41,0.14)',
        border: `1px solid ${CLAUDE.BORDER}`,
        overflow: 'hidden',
        transform: `scale(${clamp(cardIn, 0, 1)})`,
        opacity: clamp(cardIn, 0, 1),
        maxHeight: height * 0.65,
      }}>
        {/* Title bar */}
        <div style={{
          background: CLAUDE.PAGE,
          borderBottom: `1px solid ${CLAUDE.BORDER}`,
          padding: `${height * 0.012}px ${width * 0.05}px`,
          display: 'flex',
          alignItems: 'center',
          gap: 10,
        }}>
          <span style={{ fontFamily: SERIF, fontSize: FONT_TITLE_BAR, color: CLAUDE.INK, fontWeight: 600 }}>
            {artifactTitle}
          </span>
        </div>

        {/* Body */}
        <div style={{ padding: `${height * 0.025}px ${width * 0.06}px ${height * 0.028}px` }}>
          {/* Heading */}
          <div style={{
            fontFamily: SERIF,
            fontSize: FONT_HEADING,
            fontWeight: 700,
            color: CLAUDE.INK,
            marginBottom: height * 0.018,
            opacity: clamp(headIn, 0, 1),
          }}>
            {artifactHeading}
          </div>

          {/* Lines */}
          {lines.map((line, i) => {
            const lineIn = spring({ frame: frame - (i + 2) * 7, fps, config: { damping: 28, stiffness: 140, mass: 0.8 } });
            const op = clamp(lineIn, 0, 1);
            const ty = (1 - op) * 12;
            return (
              <div key={i} style={{
                display: 'flex',
                alignItems: 'flex-start',
                gap: 14,
                marginBottom: height * 0.014,
                opacity: op,
                transform: `translateY(${ty}px)`,
              }}>
                {numbered ? (
                  <span style={{
                    fontFamily: SANS,
                    fontSize: FONT_LINE,
                    color: CLAUDE.SPARK,
                    flexShrink: 0,
                    marginTop: 2,
                    fontWeight: 700,
                  }}>
                    {i + 1}.
                  </span>
                ) : null}
                <span style={{
                  fontFamily: numbered ? SANS : MONO,
                  whiteSpace: numbered ? 'normal' : 'pre',
                  fontSize: numbered ? FONT_LINE : FONT_PRE,
                  color: CLAUDE.INK,
                  lineHeight: 1.55,
                }}>
                  {line}
                </span>
              </div>
            );
          })}
        </div>
      </div>

      {/* Spark line below card */}
      {sparkLine ? (
        <div style={{
          marginTop: height * 0.020,
          display: 'flex',
          alignItems: 'center',
          gap: 10,
          opacity: clamp(sparkIn, 0, 1),
          transform: `translateY(${(1 - clamp(sparkIn, 0, 1)) * 8}px)`,
          paddingLeft: PAD_X,
          paddingRight: PAD_X,
        }}>
          <span style={{
            fontFamily: SERIF,
            fontSize: height * 0.020,
            fontStyle: 'italic',
            color: CLAUDE.INK,
            textAlign: 'center',
          }}>
            {sparkLine}
          </span>
        </div>
      ) : null}
    </AbsoluteFill>
  );
};
