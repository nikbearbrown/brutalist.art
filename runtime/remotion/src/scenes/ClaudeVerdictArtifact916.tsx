import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring } from 'remotion';
import { claudeVerdictArtifactSchema } from './ClaudeVerdictArtifact';
import type { ClaudeVerdictArtifactProps } from './ClaudeVerdictArtifact';
import { CLAUDE, CLAUDE_FONT } from '../tokens/claude';

/**
 * ClaudeVerdictArtifact916 — portrait 9:16 (1080×1920) version of ClaudeVerdictArtifact.
 * Same schema. Card fills portrait width (~90% = 972px).
 * Reflow move: R3 (rescale) — card centers in portrait frame, font sizes relative
 * to height so content fills the column without fixed-pixel locks.
 * TEXT LAW: maxWidth on all variable-length text; lineHeight + wordBreak for wrapping.
 * Safe zone: content within SAFE916 (x:54, y:96, r:1026, b:1824).
 */

export const claudeVerdictArtifact916Schema = claudeVerdictArtifactSchema;
export type ClaudeVerdictArtifact916Props = ClaudeVerdictArtifactProps;

const SERIF = CLAUDE_FONT.serif;
const SANS = CLAUDE_FONT.ui;
const clamp = (v: number, a: number, b: number) => Math.min(b, Math.max(a, v));
const stripLeadNum = (s: string) => s.replace(/^\s*\d+\s*[.)\-–—:]\s*/, '');


export const ClaudeVerdictArtifact916: React.FC<ClaudeVerdictArtifact916Props> = ({
  artifactTitle, artifactHeading, artifactLines, fillScale,
}) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  const cardIn = spring({ frame, fps, config: { damping: 28, stiffness: 140, mass: 0.8 } });
  const headIn = spring({ frame: frame - 8, fps, config: { damping: 28, stiffness: 140, mass: 0.8 } });

  const lines = (artifactLines ?? []).map(stripLeadNum);
  const CARD_W = width * 0.90;
  const PAD_H = width * 0.055;
  const PAD_V = height * 0.022;
  const FONT_TITLE = (height * 0.018) * (fillScale ?? 1);
  const FONT_HEADING = (height * 0.024) * (fillScale ?? 1);
  const FONT_LINE = (height * 0.017) * (fillScale ?? 1);
  const TEXT_MAX_W = CARD_W - PAD_H * 2 - 30;

  return (
    <AbsoluteFill style={{ background: '#F2F0E9', alignItems: 'center', justifyContent: 'center' }}>
      <div style={{
        width: CARD_W,
        background: CLAUDE.CARD,
        borderRadius: 20,
        boxShadow: '0 16px 56px rgba(61,57,41,0.16)',
        border: `1px solid ${CLAUDE.BORDER}`,
        overflow: 'hidden',
        transform: `scale(${clamp(cardIn, 0, 1)})`,
        opacity: clamp(cardIn, 0, 1),
      }}>
        {/* Title bar */}
        <div style={{
          background: CLAUDE.PAGE,
          borderBottom: `1px solid ${CLAUDE.BORDER}`,
          padding: `${PAD_V}px ${PAD_H}px`,
          display: 'flex',
          alignItems: 'center',
          gap: 10,
        }}>
          <span style={{
            fontFamily: SERIF,
            fontSize: FONT_TITLE,
            color: CLAUDE.INK,
            fontWeight: 600,
            maxWidth: CARD_W - PAD_H * 2 - FONT_TITLE - 10,
            overflow: 'hidden',
            textOverflow: 'ellipsis',
            whiteSpace: 'nowrap',
          }}>
            {artifactTitle}
          </span>
        </div>

        {/* Body */}
        <div style={{ padding: `${PAD_V * 1.4}px ${PAD_H}px ${PAD_V * 1.8}px` }}>
          {/* Heading */}
          <div style={{
            fontFamily: SERIF,
            fontSize: FONT_HEADING,
            fontWeight: 700,
            color: CLAUDE.INK,
            marginBottom: height * 0.018,
            opacity: clamp(headIn, 0, 1),
            maxWidth: TEXT_MAX_W,
            lineHeight: 1.3,
            wordBreak: 'break-word' as const,
          }}>
            {artifactHeading}
          </div>

          {/* Lines */}
          {lines.map((line, i) => {
            const lineIn = spring({ frame: frame - (i + 2) * 7, fps, config: { damping: 28, stiffness: 140, mass: 0.8 } });
            const op = clamp(lineIn, 0, 1);
            return (
              <div key={i} style={{
                display: 'flex',
                alignItems: 'flex-start',
                gap: 14,
                marginBottom: height * 0.015,
                opacity: op,
                transform: `translateY(${(1 - op) * 12}px)`,
              }}>
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
                <span style={{
                  fontFamily: SANS,
                  fontSize: FONT_LINE,
                  color: CLAUDE.INK,
                  lineHeight: 1.55,
                  maxWidth: TEXT_MAX_W,
                  wordBreak: 'break-word' as const,
                }}>
                  {line}
                </span>
              </div>
            );
          })}
        </div>
      </div>
    </AbsoluteFill>
  );
};
