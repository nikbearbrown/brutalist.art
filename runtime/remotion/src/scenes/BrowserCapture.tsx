import React from 'react';
import { AbsoluteFill, Img, staticFile, useCurrentFrame, useVideoConfig, spring, interpolate, Easing } from 'remotion';
import { z } from 'zod';
import { CLAUDE, CLAUDE_FONT } from '../tokens/claude';

/**
 * BrowserCapture — a REAL web page, shown as itself. A browser window on the
 * cream Claude stage holds a captured screenshot of the live page; the camera
 * pushes in to the part the narration is talking about and one terracotta ring
 * draws round it. The page keeps its own look inside the window.
 *
 * Use for the lecture skill's SHOW-THE-THING LAW, rung 1: a site, a docs page,
 * a sign-in page, a dashboard. The image is a capture the reel made (Playwright
 * or a human screenshot), never a mock-up: nothing in the window is invented.
 *
 * image  — a data: URI, or a path under runtime/remotion/public/ (staticFile).
 * moves  — camera keyframes. `at` is a fraction of the beat (0–1); x, y are the
 *          focus point as fractions of the IMAGE; scale 1 = the image fits the
 *          window's width. Optional ring = [x, y, w, h] as fractions of the image.
 *          Each move takes `moveSeconds` and then HOLDS. Keep every move out of
 *          the 45–55% window (GATE T and Gate V sample the midpoint).
 *
 * Doctrine: skills/make/lecture/SKILL.md → SHOW-THE-THING LAW.
 */

export const browserCaptureMoveSchema = z.object({
  at:    z.number().min(0).max(1),
  x:     z.number().min(0).max(1).default(0.5),
  y:     z.number().min(0).max(1).default(0.5),
  scale: z.number().min(1).max(4).default(1),
  ring:  z.array(z.number()).length(4).optional(),
});

export const browserCaptureSchema = z.object({
  /** The real address, as shown in the address bar. */
  url:     z.string().default('⚠ SET IN BEAT SHEET'),
  image:   z.string().default(''),
  /** One short line under the window: where and when the capture was made. */
  caption: z.string().default(''),
  moves:   z.array(browserCaptureMoveSchema).min(1).max(6).default([{ at: 0, x: 0.5, y: 0.5, scale: 1 }]),
  moveSeconds:     z.number().default(1.2),
  /** Width / height of the capture (default 16:9). */
  imageAspect:     z.number().default(16 / 9),
  durationSeconds: z.number().default(10),
});
export type BrowserCaptureProps = z.infer<typeof browserCaptureSchema>;

const clamp = (v: number, a: number, b: number) => Math.min(b, Math.max(a, v));

// Window geometry at the 1920×1080 design size.
const WIN = { left: 120, top: 48, width: 1680, height: 900 };
const BAR = 64;
const VIEW = { width: WIN.width, height: WIN.height - BAR };

export const BrowserCapture: React.FC<BrowserCaptureProps> = ({ url, image, caption, moves, moveSeconds, imageAspect }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const winIn = clamp(spring({ frame, fps, config: { damping: 26, stiffness: 150, mass: 0.8 } }), 0, 1);

  const total = useVideoConfig().durationInFrames;
  const mv = [...moves].sort((a, b) => a.at - b.at);
  const mf = Math.max(1, Math.round(moveSeconds * fps));

  // Camera: hold each keyframe; ease to the next one starting at its `at`.
  let cam = { x: mv[0].x, y: mv[0].y, scale: mv[0].scale };
  let active = 0;
  for (let i = 1; i < mv.length; i++) {
    const start = Math.round(mv[i].at * total);
    if (frame < start) break;
    const t = interpolate(frame, [start, start + mf], [0, 1], {
      extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.inOut(Easing.cubic),
    });
    const from = mv[i - 1];
    cam = { x: from.x + (mv[i].x - from.x) * t, y: from.y + (mv[i].y - from.y) * t, scale: from.scale + (mv[i].scale - from.scale) * t };
    active = i;
  }

  // The image fits the viewport's width at scale 1.
  const imgW = VIEW.width * cam.scale;
  const imgH = imgW / imageAspect;
  // Keep the focus point centred, but never show past the image's edges.
  const tx = clamp(VIEW.width / 2 - cam.x * imgW, VIEW.width - imgW, 0);
  const ty = clamp(VIEW.height / 2 - cam.y * imgH, Math.min(0, VIEW.height - imgH), 0);

  // The ring of the active keyframe draws after its move lands.
  const ring = mv[active].ring;
  const ringStart = Math.round(mv[active].at * total) + (active === 0 ? 12 : mf);
  const ringIn = clamp(spring({ frame: frame - ringStart, fps, config: { damping: 22, stiffness: 120, mass: 0.7 } }), 0, 1);

  const src = image.startsWith('data:') ? image : image ? staticFile(image) : '';

  return (
    <AbsoluteFill style={{ backgroundColor: CLAUDE.PAGE }}>
      <div style={{
        position: 'absolute', left: WIN.left, top: WIN.top, width: WIN.width, height: WIN.height,
        background: CLAUDE.CARD, border: `2px solid ${CLAUDE.INK}`, borderRadius: 16, overflow: 'hidden',
        boxShadow: '0 14px 44px rgba(61,57,41,0.16)',
        opacity: winIn, transform: `translateY(${(1 - winIn) * 14}px)`,
      }}>
        {/* address bar */}
        <div style={{ position: 'absolute', left: 0, right: 0, top: 0, height: BAR, background: CLAUDE.FOOTER,
                      borderBottom: `2px solid ${CLAUDE.INK}`, display: 'flex', alignItems: 'center' }}>
          <div style={{ display: 'flex', gap: 10, marginLeft: 22 }}>
            {[0, 1, 2].map((i) => <span key={i} style={{ width: 15, height: 15, borderRadius: 8, background: CLAUDE.GHOST, display: 'inline-block' }} />)}
          </div>
          <div style={{ marginLeft: 26, marginRight: 26, flex: 1, height: 42, borderRadius: 21, background: CLAUDE.CARD,
                        border: `1px solid ${CLAUDE.BORDER}`, display: 'flex', alignItems: 'center', paddingLeft: 22,
                        fontFamily: CLAUDE_FONT.mono, fontSize: 28, color: CLAUDE.INK, whiteSpace: 'nowrap', overflow: 'hidden' }}>
            {url}
          </div>
        </div>
        {/* the captured page */}
        <div style={{ position: 'absolute', left: 0, top: BAR, width: VIEW.width, height: VIEW.height, overflow: 'hidden', background: '#FFFFFF' }}>
          <div style={{ position: 'absolute', left: tx, top: ty, width: imgW, height: imgH }}>
            {src ? <Img src={src} style={{ width: '100%', height: '100%', display: 'block' }} /> : null}
            {ring ? (
              <div style={{
                position: 'absolute', left: `${ring[0] * 100}%`, top: `${ring[1] * 100}%`,
                width: `${ring[2] * 100}%`, height: `${ring[3] * 100}%`,
                border: `7px solid ${CLAUDE.SPARK}`, borderRadius: 18, boxSizing: 'border-box',
                opacity: ringIn, transform: `scale(${1.06 - 0.06 * ringIn})`,
              }} />
            ) : null}
          </div>
        </div>
      </div>
      {caption ? (
        <div style={{ position: 'absolute', left: 0, right: 0, top: WIN.top + WIN.height + 26, textAlign: 'center',
                      fontFamily: CLAUDE_FONT.serif, fontSize: 36, color: CLAUDE.INK, opacity: winIn }}>
          {caption}
        </div>
      ) : null}
    </AbsoluteFill>
  );
};

export const browserCaptureDefaultProps: BrowserCaptureProps = browserCaptureSchema.parse({});
