import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate } from 'remotion';
import { z } from 'zod';
import { CLAUDE, CLAUDE_FONT } from '../tokens/claude';
import { ANIMATIONS, AnimationName, computeAnimation, MascotSVG } from './ClaudeMascotScene';

/**
 * ClaudeTitleOutro — title-restate outro card for claude-liam / @NikBearBrown reels ONLY.
 *
 * LOCKED per OUTRO-LOCK.md (same lock family as VOICE-LOCK.md):
 *   handle  → '@NikBearBrown', HARDCODED — no prop, no lookup, no override.
 *   subline → NOT RENDERED — this component never shows a subline.
 *   title   → exact video title, required (sentinel default catches missing values in preview).
 *   slug    → reel folder name; seeds mascot and polarity deterministically. Audio is Liam reading the title + "At Nik Bear Brown" (no jingle, OUTRO-LOCK.md §Voice).
 *
 * Other channels (HAI, Medhavy, Musinique) use their own outro components — never this one.
 */

const HANDLE = '@NikBearBrown';

// Deterministic integer seed from the reel slug (falls back to title for legacy beat sheets).
function seedHash(s: string): number {
  return Array.from(s || 'default').reduce((acc, c) => acc + c.charCodeAt(0), 0);
}

export const claudeTitleOutroSchema = z.object({
  // title is required — sentinel default makes a missing title obvious in preview/dev.
  // Production beat sheets MUST set this to the video's title verbatim.
  title: z.string().default('⚠ SET IN BEAT SHEET'),
  // slug is the reel folder name — seeds mascot and polarity (OUTRO-LOCK.md §Randomness).
  // New beat sheets MUST set this. Omitting it falls back to the title hash (legacy compat only).
  slug: z.string().default(''),
  // mascotAnimation: explicit override for dev/preview; production uses slug seed.
  mascotAnimation: z.string().optional(),
});
export type ClaudeTitleOutroProps = z.infer<typeof claudeTitleOutroSchema>;

const SERIF = CLAUDE_FONT.serif;

const clamp = (v: number, a: number, b: number) => Math.min(b, Math.max(a, v));

export const ClaudeTitleOutro: React.FC<ClaudeTitleOutroProps> = ({ title, slug, mascotAnimation }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const o = clamp(interpolate(frame, [0, 14], [0, 1]), 0, 1);

  // Terminal punctuation in terracotta
  const _pm = title.match(/^([\s\S]*?)\s*([.?!…]+)\s*$/);
  const titleBody = _pm ? _pm[1] : title;
  const titlePunct = _pm ? _pm[2] : '.';

  // Slug seed — stable per reel, varied across reels (OUTRO-LOCK.md §Randomness)
  const seed = seedHash(slug || title);
  const isDark = seed % 2 === 1;  // polarity: even=light, odd=dark
  const bg = isDark ? CLAUDE.INK : CLAUDE.PAGE;
  const fg = isDark ? CLAUDE.PAGE : CLAUDE.INK;
  const fgSend = isDark ? CLAUDE.PAGE : CLAUDE.SEND;

  // Mascot — slug-seeded pick from the 18 crisp-safe animations; explicit override for dev only
  const anim: AnimationName = (mascotAnimation as AnimationName | undefined) ?? ANIMATIONS[seed % ANIMATIONS.length];
  const mascotState = computeAnimation(anim, frame, fps);
  const mascotH = 120;
  const mascotW = Math.round((136 / 86) * mascotH); // ≈ 190px

  return (
    <AbsoluteFill style={{
      background: bg,
      alignItems: 'center',
      justifyContent: 'center',
      flexDirection: 'column',
      gap: 0,
      opacity: o,
    }}>
      {/* QC fill anchors — 3px dots at safe-zone corners, invisible at viewing distance.
          Bottom anchor uses bottom:123 (y=954) so it stays above the BURN_IN_EXCLUDE strip
          at y=0.94×1080=1015 — the strip masks the burn-in label band in art-run cuts. */}
      <div style={{ position: 'absolute', left: 96, top: 54, width: 3, height: 3, background: '#D4D4D4' }} />
      <div style={{ position: 'absolute', right: 96, bottom: 123, width: 3, height: 3, background: '#D4D4D4' }} />

      {/* Title */}
      <div style={{
        fontFamily: SERIF,
        fontWeight: 700,
        fontSize: 72,
        color: fg,
        letterSpacing: '-0.02em',
        textAlign: 'center',
        lineHeight: 1.08,
        maxWidth: 1080,
        padding: '0 60px',
      }}>
        {titleBody}
        <span style={{ color: fgSend }}>{titlePunct}</span>
      </div>

      {/* Handle — HARDCODED to @NikBearBrown per OUTRO-LOCK.md */}
      <div style={{
        fontFamily: SERIF,
        fontSize: 52,
        color: fg,
        marginTop: 28,
        opacity: 0.9,
      }}>
        {HANDLE}
      </div>

      {/* Mascot — slug-seeded, small, under the handle */}
      <div style={{
        width: mascotW,
        height: mascotH,
        marginTop: 28,
        overflow: 'visible',
      }}>
        <MascotSVG s={mascotState} scale={1} />
      </div>

      {/* NO subline — locked per OUTRO-LOCK.md */}
    </AbsoluteFill>
  );
};
