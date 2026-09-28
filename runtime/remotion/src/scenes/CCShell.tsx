import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from 'remotion';
import { z } from 'zod';
import { CC, CC_FONT } from '../tokens/claudecode';
import { AnchorContext, AnchorCtx, AnchorPos } from './CursorLayer';
import { MascotSVG, computeAnimation, ANIMATIONS } from './ClaudeMascotScene';

/**
 * CCShell — terminal window chrome. Title bar with traffic lights, centred
 * session title, body slot for content, footer with verbatim product mode
 * strings. Use as a wrapper in CCSession; register standalone for Studio
 * previews. Optional `mascot` prop plants an animated Clawd in a body corner
 * (PIXEL-ART LAW: translate + axis-aligned scale only — see ClaudeMascotScene).
 */

// ── Layout constants ──────────────────────────────────────────────────────────
// All values are CSS pixels on the 1920×1080 canvas.

export const CC_LAYOUT = {
  WIN_X: 140, WIN_Y: 70, WIN_W: 1640, WIN_H: 940,
  TB_H: 50, FOOT_H: 54,
} as const;

export const CC_BODY = {
  X: 160,  // WIN_X + 20
  Y: 120,  // WIN_Y + TB_H
  W: 1600, // WIN_W - 40
  H: 836,  // WIN_H - TB_H - FOOT_H
} as const;

// ── Footer string helpers ─────────────────────────────────────────────────────

type FooterMode = 'accept-edits' | 'plan' | 'default';

const FOOTER_STRINGS: Record<FooterMode, string> = {
  'accept-edits': 'accept edits on  (shift+tab to cycle) · esc to interrupt',
  'plan':         'plan mode on  (shift+tab to cycle) · esc to interrupt',
  'default':      '◐ medium · /effort',
};

// Fragments that get VIOLET coloring in the footer
const VIOLET_FRAGMENTS = ['shift+tab', 'esc', '/effort', 'ctrl+b', 'ctrl+o'];

/**
 * Split a footer string into spans, coloring keybinding fragments in VIOLET.
 */
function renderFooterSpans(text: string): React.ReactNode[] {
  // Build a regex that matches any of the violet fragments
  const pattern = new RegExp(`(${VIOLET_FRAGMENTS.map(f => f.replace(/[+/]/g, '\\$&')).join('|')})`, 'g');
  const parts = text.split(pattern);
  return parts.map((part, i) => {
    const isViolet = VIOLET_FRAGMENTS.includes(part);
    return (
      <span
        key={i}
        style={{
          color: isViolet ? CC.VIOLET : CC.INK_2,
          fontFamily: CC_FONT.mono,
          fontSize: 44,
          whiteSpace: 'pre',
        }}
      >
        {part}
      </span>
    );
  });
}

// ── Schema ────────────────────────────────────────────────────────────────────

export const ccShellSchema = z.object({
  title:       z.string().default('⚠ SET IN BEAT SHEET'),
  mode:        z.enum(['accept-edits', 'plan', 'default']).default('default'),
  effortLabel: z.string().optional(),
  // Clawd mascot — off unless set. Any of the 18 ClaudeMascotScene animations.
  mascot:       z.enum(ANIMATIONS).optional(),
  mascotCorner: z.enum(['bottom-right', 'bottom-left']).optional(),
});
export type CCShellProps = z.infer<typeof ccShellSchema> & { children?: React.ReactNode };

// ── Component ─────────────────────────────────────────────────────────────────

export const CCShell: React.FC<CCShellProps> = (props) => {
  const { title, mode = 'default', mascot, mascotCorner = 'bottom-right', children } = props;
  const frame   = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Anchor context — fresh map each render so children can register positions
  const anchorMapRef = React.useRef<Map<string, AnchorPos>>(new Map());
  const ctx = React.useMemo<AnchorCtx>(() => {
    anchorMapRef.current = new Map();
    return {
      register: (id, x, y) => anchorMapRef.current.set(id, { x, y }),
      resolve:  (id)       => anchorMapRef.current.get(id),
    };
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const { WIN_X, WIN_Y, WIN_W, WIN_H, TB_H, FOOT_H } = CC_LAYOUT;
  const footerText = FOOTER_STRINGS[mode];

  return (
    <AbsoluteFill style={{ background: CC.PAGE }}>
      <AnchorContext.Provider value={ctx}>
        {/* Terminal window */}
        <div style={{
          position: 'absolute',
          left: WIN_X, top: WIN_Y,
          width: WIN_W, height: WIN_H,
          background: CC.PAGE,
          border: `1px solid ${CC.BORDER}`,
          borderRadius: CC.RADIUS,
          boxShadow: '0 24px 80px rgba(0,0,0,.6)',
          overflow: 'hidden',
          display: 'flex',
          flexDirection: 'column',
        }}>

          {/* ── Title bar ──────────────────────────────────────────────────── */}
          <div style={{
            flexShrink: 0,
            height: TB_H,
            background: CC.PANEL,
            borderBottom: `1px solid ${CC.BORDER}`,
            display: 'flex',
            alignItems: 'center',
            position: 'relative',
          }}>
            {/* Traffic lights */}
            {[CC.TL_RED, CC.TL_YEL, CC.TL_GRN].map((col, i) => (
              <div key={i} style={{
                marginLeft: i === 0 ? 16 : 8,
                width: 14, height: 14,
                borderRadius: '50%',
                background: col,
                flexShrink: 0,
              }} />
            ))}
            {/* Session title — centred */}
            <div style={{
              position: 'absolute',
              left: '50%',
              transform: 'translateX(-50%)',
              display: 'flex',
              alignItems: 'center',
              gap: 8,
              whiteSpace: 'nowrap',
            }}>
              <span style={{
                fontFamily: CC_FONT.ui,
                fontSize: 36,
                color: CC.INK_2,
              }}>⬡</span>
              <span style={{
                fontFamily: CC_FONT.ui,
                fontSize: 36,
                fontWeight: 500,
                color: CC.INK,
              }}>{title}</span>
            </div>
          </div>

          {/* ── Body — flex-1 slot for children ────────────────────────────── */}
          <div style={{
            flex: 1,
            position: 'relative',
            overflow: 'hidden',
            minHeight: 0,
          }}>
            {children}

            {/* ── Clawd corner mascot (prop-gated) ───────────────────────── */}
            {mascot && (
              <div style={{
                position: 'absolute',
                bottom: 8,
                width: 190,
                height: 120,
                pointerEvents: 'none',
                ...(mascotCorner === 'bottom-left' ? { left: 28 } : { right: 28 }),
              }}>
                <MascotSVG s={computeAnimation(mascot, frame, fps)} scale={1} />
              </div>
            )}
          </div>

          {/* ── Footer ─────────────────────────────────────────────────────── */}
          <div style={{
            flexShrink: 0,
            height: FOOT_H,
            background: CC.PANEL,
            borderTop: `1px solid ${CC.BORDER}`,
            display: 'flex',
            alignItems: 'center',
            paddingLeft: 20,
            paddingRight: 20,
          }}>
            {renderFooterSpans(footerText)}
          </div>

        </div>
      </AnchorContext.Provider>
    </AbsoluteFill>
  );
};

// ── defaultProps ──────────────────────────────────────────────────────────────

export const ccShellDefaultProps: CCShellProps = ccShellSchema.parse({});

// ── Demo ──────────────────────────────────────────────────────────────────────

export const ccShellDemoSchema = ccShellSchema;
export type CCShellDemoProps = CCShellProps;

export const CCShellDemo: React.FC<CCShellDemoProps> = (props) => {
  return (
    <CCShell {...props}>
      <div style={{
        position: 'absolute',
        top: 40,
        left: 20,
        right: 20,
        color: CC.INK_3,
        fontFamily: CC_FONT.mono,
        fontSize: 52,
      }}>
        {/* placeholder body content for studio preview */}
        $ _
      </div>
    </CCShell>
  );
};

export const ccShellDemoDefaultProps: CCShellDemoProps = ccShellDemoSchema.parse({
  title: 'brutalist-art · src/scenes',
  mode: 'accept-edits',
});
