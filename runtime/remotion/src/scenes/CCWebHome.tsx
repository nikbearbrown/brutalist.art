import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring } from 'remotion';
import { z } from 'zod';
import { CC, CC_FONT } from '../tokens/claudecode';
import { AnchorContext } from './CursorLayer';
import { MascotSVG, computeAnimation } from './ClaudeMascotScene';

/**
 * CCWebHome — full-screen dark canvas for the Claude web UI home state.
 * Dotted-grid background via CSS radial-gradient; centred MascotSVG (idle);
 * two dropdown pills (repo/branch); suggestion rows with ghost right-column
 * previews. NOT wrapped in CCShell — its own dark surface, no chrome.
 *
 * PIXEL-ART LAW: MascotSVG uses translate + axis-aligned scale ONLY.
 */

// ── Schema ────────────────────────────────────────────────────────────────────

export const suggestionRowSchema = z.object({
  icon:    z.string().default('◆'),
  label:   z.string(),
  preview: z.string().default(''),
});
export type SuggestionRow = z.infer<typeof suggestionRowSchema>;

export const ccWebHomeSchema = z.object({
  repoLabel:   z.string().default('⚠ SET IN BEAT SHEET'),
  branchLabel: z.string().default('main'),
  suggestions: z.array(suggestionRowSchema).default([]),
});
export type CCWebHomeProps = z.infer<typeof ccWebHomeSchema>;

// ── Helpers ───────────────────────────────────────────────────────────────────

const clamp = (v: number, a: number, b: number) => Math.min(b, Math.max(a, v));
const SPRING      = { damping: 26, stiffness: 120, mass: 0.9 };
const SPRING_SLOW = { damping: 30, stiffness:  80, mass: 1.2 };

// Canvas dimensions (1920×1080)
const W = 1920;
const H = 1080;

// Dotted grid: 32px cell, 2px dot
const DOTS_CSS = `radial-gradient(circle, ${CC.BORDER} 2px, transparent 2px)`;

// ── Pill (repo / branch) ──────────────────────────────────────────────────────

const Pill: React.FC<{ label: string; icon?: string }> = ({ label, icon = '⬡' }) => (
  <div style={{
    display:         'flex',
    alignItems:      'center',
    gap:             10,
    padding:         '10px 24px',
    background:      CC.PANEL,
    border:          `1.5px solid ${CC.BORDER}`,
    borderRadius:    9999,
    fontFamily:      CC_FONT.mono,
    fontSize:        44,
    color:           CC.INK_2,
    whiteSpace:      'nowrap',
  }}>
    <span style={{ color: CC.VIOLET }}>{icon}</span>
    {label}
    <span style={{ color: CC.INK_3, marginLeft: 4 }}>▾</span>
  </div>
);

// ── Component ─────────────────────────────────────────────────────────────────

export const CCWebHome: React.FC<CCWebHomeProps> = ({
  repoLabel, branchLabel, suggestions,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const { register } = React.useContext(AnchorContext);

  register('cc.webhome.mascot', W / 2, H / 2 - 80);
  register('cc.webhome.pills',  W / 2, H / 2 + 60);

  // mascot idle
  const animState = computeAnimation('idle', frame, fps);

  // entrance springs
  const mascotIn = spring({ frame,            fps, config: SPRING_SLOW });
  const pillsIn  = spring({ frame: frame - 8,  fps, config: SPRING });
  const rowBase  = 20;

  const MASCOT_SIZE  = 160;
  const ROW_H        = 80;
  const ROW_FONT     = 48;
  const PREVIEW_FONT = 40;

  return (
    <AbsoluteFill style={{
      background:          CC.PAGE,
      backgroundImage:     DOTS_CSS,
      backgroundSize:      '32px 32px',
      backgroundPosition:  '0 0',
    }}>
      {/* ── Centred mascot ─────────────────────────────────────────────── */}
      <div style={{
        position:  'absolute',
        left:      W / 2 - MASCOT_SIZE / 2,
        top:       H / 2 - MASCOT_SIZE - 60,
        width:     MASCOT_SIZE,
        height:    MASCOT_SIZE,
        opacity:   clamp(mascotIn, 0, 1),
        transform: `scale(${0.6 + clamp(mascotIn, 0, 1) * 0.4})`,
      }}>
        <MascotSVG s={animState} scale={1} />
      </div>

      {/* ── Dropdown pills ─────────────────────────────────────────────── */}
      <div style={{
        position:       'absolute',
        left:           0,
        right:          0,
        top:            H / 2 - 24,
        display:        'flex',
        justifyContent: 'center',
        gap:            20,
        opacity:        clamp(pillsIn, 0, 1),
        transform:      `translateY(${(1 - clamp(pillsIn, 0, 1)) * 16}px)`,
      }}>
        <Pill label={repoLabel} icon="⬡" />
        <Pill label={branchLabel} icon="⑂" />
      </div>

      {/* ── Suggestion rows ─────────────────────────────────────────────── */}
      <div style={{
        position: 'absolute',
        left:     W / 2 - 600,
        right:    W / 2 - 600,
        width:    1200,
        top:      H / 2 + 60,
      }}>
        {suggestions.map((row, i) => {
          const rowSpring = spring({ frame: frame - rowBase - i * 5, fps, config: SPRING });
          const rowOp     = clamp(rowSpring, 0, 1);

          return (
            <div
              key={i}
              style={{
                display:        'flex',
                alignItems:     'center',
                height:         ROW_H,
                borderBottom:   `1px solid ${CC.BORDER}`,
                opacity:        rowOp,
                transform:      `translateX(${(1 - rowOp) * -12}px)`,
                gap:            18,
                paddingLeft:    4,
              }}
            >
              {/* icon */}
              <span style={{
                fontFamily: CC_FONT.mono,
                fontSize:   ROW_FONT,
                color:      CC.VIOLET,
                flexShrink: 0,
                width:      52,
                textAlign:  'center',
              }}>
                {row.icon}
              </span>

              {/* label */}
              <span style={{
                fontFamily: CC_FONT.ui,
                fontSize:   ROW_FONT,
                color:      CC.INK,
                flex:       1,
                overflow:   'hidden',
                textOverflow: 'ellipsis',
                whiteSpace: 'nowrap',
              }}>
                {row.label}
              </span>

              {/* ghost preview */}
              {row.preview.length > 0 && (
                <span style={{
                  fontFamily:   CC_FONT.mono,
                  fontSize:     PREVIEW_FONT,
                  color:        CC.INK_3,
                  opacity:      0.55,
                  whiteSpace:   'nowrap',
                  maxWidth:     380,
                  overflow:     'hidden',
                  textOverflow: 'ellipsis',
                }}>
                  {row.preview}
                </span>
              )}
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

// ── defaultProps ──────────────────────────────────────────────────────────────

export const ccWebHomeDefaultProps: CCWebHomeProps = ccWebHomeSchema.parse({
  repoLabel:   '⚠ SET IN BEAT SHEET',
  branchLabel: 'main',
  suggestions: [{ label: '⚠ SET IN BEAT SHEET' }],
});

// ── Demo twin ─────────────────────────────────────────────────────────────────

export const ccWebHomeDemoSchema = ccWebHomeSchema;
export type CCWebHomeDemoProps   = CCWebHomeProps;

export const CCWebHomeDemo: React.FC<CCWebHomeDemoProps> = (props) => (
  <CCWebHome {...props} />
);

export const ccWebHomeDemoDefaultProps: CCWebHomeDemoProps = ccWebHomeDemoSchema.parse({
  repoLabel:   'anthropics/claude-code',
  branchLabel: 'main',
  suggestions: [
    { icon: '◆', label: 'Fix the flaky integration test',        preview: 'tests/integration/auth.test.ts' },
    { icon: '◆', label: 'Add dark-mode support to the sidebar',  preview: 'src/components/Sidebar.tsx'     },
    { icon: '◆', label: 'Write a migration for the users table',  preview: 'db/migrations/'                },
    { icon: '◆', label: 'Explain the caching strategy',          preview: 'docs/caching.md'                },
  ],
});
