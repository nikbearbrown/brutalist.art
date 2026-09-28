import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate, spring, Easing } from 'remotion';
import { z } from 'zod';

// ── Anchor registry ──────────────────────────────────────────────────────────

/** Canvas-coordinate centre of a registered interactive element. */
export type AnchorPos = { x: number; y: number };

/**
 * Context provided by CoworkShell.
 * Components call `register` in their render body to publish their centre
 * coordinates. CursorLayer calls `resolve` to look them up.
 */
export interface AnchorCtx {
  register: (id: string, x: number, y: number) => void;
  resolve:  (id: string) => AnchorPos | undefined;
}

export const AnchorContext = React.createContext<AnchorCtx>({
  register: () => {},
  resolve:  () => undefined,
});

// ── Verify ────────────────────────────────────────────────────────────────────

/**
 * verifyPath — dev guard; call at the start of CursorLayer's render.
 * THROWS if any waypoint has an authored `x` or `y` field (positions must come
 * from anchor IDs, never from pixel coordinates written by hand).
 * THROWS with the anchor ID if a waypoint names an anchor no element registered.
 */
export function verifyPath(
  path: ReadonlyArray<{ anchor: string; atCue: number; click?: boolean }>,
  ctx: AnchorCtx,
): void {
  for (const wp of path) {
    if ((wp as Record<string, unknown>).x !== undefined ||
        (wp as Record<string, unknown>).y !== undefined) {
      throw new Error(
        `CursorLayer: authored x/y in cursor path for anchor "${wp.anchor}". ` +
        `Use anchorId strings only — coordinates are resolved at render time.`,
      );
    }
    if (!ctx.resolve(wp.anchor)) {
      throw new Error(
        `CursorLayer: cursor path references unregistered anchor "${wp.anchor}". ` +
        `Ensure the element that owns this anchor renders before CursorLayer.`,
      );
    }
  }
}

// ── Schema ────────────────────────────────────────────────────────────────────

const waypointSchema = z.object({
  /** Registered anchor ID to navigate to. No x/y fields allowed. */
  anchor: z.string(),
  /** Frame number at which the cursor arrives at this anchor. */
  atCue:  z.number().int().min(0),
  /** If true: show a scale-dip + ripple click animation on arrival. */
  click:  z.boolean().optional(),
});

export const cursorLayerSchema = z.object({
  path:  z.array(waypointSchema).default([]),
  /** Overall cursor scale multiplier (1.0 = 32 px arrow). */
  scale: z.number().default(1.0),
});
export type CursorLayerProps = z.infer<typeof cursorLayerSchema>;

// ── Arrow SVG ─────────────────────────────────────────────────────────────────

/** macOS default arrow pointer. White fill, black outline, drop shadow. */
const Arrow: React.FC<{ px: number }> = ({ px }) => (
  <svg
    width={px} height={px}
    viewBox="0 0 32 38"
    style={{ display: 'block', filter: 'drop-shadow(1px 2px 3px rgba(0,0,0,0.4))' }}
  >
    {/* Outer black stroke */}
    <polygon
      points="4,2 4,28 10,22 15,32 20,30 15,20 23,20"
      fill="black"
      strokeLinejoin="round"
    />
    {/* Inner white fill, slightly inset */}
    <polygon
      points="6,5 6,24 11,19 16,29 18,28 13,18 21,18"
      fill="white"
      strokeLinejoin="round"
    />
  </svg>
);

// ── Component ─────────────────────────────────────────────────────────────────

/**
 * CursorLayer — animated macOS pointer that walks a path of registered anchors.
 * Renders as an AbsoluteFill overlay and must be the LAST child of CoworkShell
 * so all sibling components have registered their anchors before this renders.
 *
 * Declare a `path` of {anchor, atCue, click?} waypoints; the cursor eases
 * between them with cubic in-out. Click waypoints show a scale-dip + ripple.
 * verifyPath() enforces: (1) no authored x/y in path waypoints, and (2) every
 * anchor ID names a registered element — missing anchors throw with the ID.
 */
export const CursorLayer: React.FC<CursorLayerProps> = (raw) => {
  const path  = raw.path  ?? [];
  const scale = raw.scale ?? 1.0;

  const ctx   = React.useContext(AnchorContext);
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Dev guard: verify the full path each frame.
  if (path.length > 1) verifyPath(path, ctx);

  if (path.length === 0) return <AbsoluteFill style={{ pointerEvents: 'none' }} />;

  // ── resolve all anchor positions ──────────────────────────────────────────
  const pos = path.map(wp => ctx.resolve(wp.anchor) ?? { x: 960, y: 540 });

  // ── compute current cursor position by finding the active segment ─────────
  let cx = pos[0].x;
  let cy = pos[0].y;

  if (frame < path[0].atCue) {
    cx = pos[0].x;
    cy = pos[0].y;
  } else {
    for (let i = 0; i < path.length - 1; i++) {
      const t0 = path[i].atCue;
      const t1 = path[i + 1].atCue;
      if (frame >= t0 && frame <= t1) {
        cx = interpolate(frame, [t0, t1], [pos[i].x, pos[i + 1].x], {
          extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
          easing: Easing.inOut(Easing.cubic),
        });
        cy = interpolate(frame, [t0, t1], [pos[i].y, pos[i + 1].y], {
          extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
          easing: Easing.inOut(Easing.cubic),
        });
        break;
      }
      if (frame > t1) {
        cx = pos[i + 1].x;
        cy = pos[i + 1].y;
      }
    }
    if (frame >= path[path.length - 1].atCue) {
      cx = pos[path.length - 1].x;
      cy = pos[path.length - 1].y;
    }
  }

  // ── click animation: scale-dip + expanding ripple ─────────────────────────
  let cursorScale = scale;
  let rippleOpacity = 0;
  let rippleRadius = 0;

  for (const wp of path) {
    if (!wp.click) continue;
    const f = frame - wp.atCue;
    if (f >= 0 && f < 22) {
      // Scale-dip: spring from 1→0.6→1
      const dip = spring({ frame: f, fps, config: { damping: 12, stiffness: 500, mass: 0.4 } });
      cursorScale = scale * (0.6 + 0.4 * dip);
      // Ripple: expand and fade
      rippleRadius  = interpolate(f, [0, 20], [0, 44], { extrapolateRight: 'clamp' });
      rippleOpacity = interpolate(f, [0, 20], [0.5, 0], { extrapolateRight: 'clamp' });
    }
  }

  const ARROW_PX = Math.round(32 * cursorScale);

  return (
    <AbsoluteFill style={{ pointerEvents: 'none' }}>
      {/* click ripple circle */}
      {rippleOpacity > 0 && (
        <div style={{
          position: 'absolute',
          left: cx - rippleRadius,
          top:  cy - rippleRadius,
          width:  rippleRadius * 2,
          height: rippleRadius * 2,
          borderRadius: '50%',
          background: 'rgba(255,255,255,0.6)',
          opacity: rippleOpacity,
          pointerEvents: 'none',
        }} />
      )}
      {/* cursor arrow — hotspot at top-left corner (0, 0) of the SVG */}
      <div style={{
        position: 'absolute',
        left: cx,
        top:  cy,
        pointerEvents: 'none',
      }}>
        <Arrow px={ARROW_PX} />
      </div>
    </AbsoluteFill>
  );
};
