import React from 'react';
import { AbsoluteFill, Img, staticFile, useCurrentFrame, useVideoConfig, spring } from 'remotion';
import { z } from 'zod';
import { CLAUDE, CLAUDE_FONT } from '../tokens/claude';

/**
 * LibraryIconRow — 2–4 named things, each shown by ONE large 2-D line icon from
 * the canonical icon set (`./art icons`), landing on its spoken cue. The icon is
 * the picture (220 px), the label is one to three words, the sub is optional.
 *
 * Use when a beat names a short set of things that are each recognisable by a
 * mark, and the mark teaches more than a sentence would. FormBCard is the
 * text-first version (44 px icons); this is the picture-first one.
 *
 * icon — a file name (no extension) under runtime/remotion/public/form-b-icons/.
 *        Copy the SVG there from icons/svg/ (found with `./art icons "<need>"`).
 * at   — when the item lands, as a fraction of the beat (0–1). Keep every `at`
 *        out of the 45–55% window (GATE T and Gate V sample the midpoint).
 *
 * Doctrine: skills/make/lecture/SKILL.md → BEST-BEAT LAW router, 2-D icons lane.
 */

export const libraryIconItemSchema = z.object({
  label: z.string(),
  sub:   z.string().default(''),
  icon:  z.string(),
  at:    z.number().min(0).max(1).default(0),
  mono:  z.boolean().default(false),
});

export const libraryIconRowSchema = z.object({
  title: z.string().default(''),
  items: z.array(libraryIconItemSchema).min(2).max(4),
  durationSeconds: z.number().default(8),
  iconPx: z.number().default(220),
});
export type LibraryIconRowProps = z.infer<typeof libraryIconRowSchema>;

const clamp = (v: number, a: number, b: number) => Math.min(b, Math.max(a, v));

export const LibraryIconRow: React.FC<LibraryIconRowProps> = ({ title, items, iconPx = 220 }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const titleIn = clamp(spring({ frame, fps, config: { damping: 26, stiffness: 150, mass: 0.8 } }), 0, 1);
  // The item that landed last carries the one terracotta (its underline); earlier ones settle to ink.
  const landed = items.map((it) => frame >= Math.round(it.at * durationInFrames));
  const current = landed.lastIndexOf(true);

  return (
    <AbsoluteFill style={{ backgroundColor: CLAUDE.PAGE }}>
      {title ? (
        <div style={{ position: 'absolute', left: 0, right: 0, top: 110, textAlign: 'center', fontFamily: CLAUDE_FONT.serif,
                      fontSize: 72, fontWeight: 600, color: CLAUDE.INK, opacity: titleIn }}>
          {title}
        </div>
      ) : null}
      <div style={{ position: 'absolute', left: 120, right: 120, top: 300, bottom: 150, display: 'flex',
                    justifyContent: 'space-evenly', alignItems: 'flex-start' }}>
        {items.map((it, i) => {
          const s = clamp(spring({ frame: frame - Math.round(it.at * durationInFrames), fps,
                                   config: { damping: 18, stiffness: 150, mass: 0.7 } }), 0, 1);
          return (
            <div key={i} style={{ width: 500, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
              {/* The tile is on stage from frame one as an empty slot (so the row is laid out and the
                  frame is never a lone icon); the icon and its words arrive on the spoken cue. */}
              <div style={{ width: iconPx + 80, height: iconPx + 80, borderRadius: 28,
                            background: landed[i] ? CLAUDE.CARD : CLAUDE.PILL,
                            border: `4px solid ${landed[i] ? CLAUDE.INK : CLAUDE.INK_SOFT}`,
                            display: 'flex', alignItems: 'center', justifyContent: 'center',
                            transform: `scale(${landed[i] ? 0.94 + 0.06 * s : 0.94})` }}>
                {landed[i] ? <Img src={staticFile(`form-b-icons/${it.icon}.svg`)}
                                  style={{ width: iconPx, height: iconPx, opacity: s }} /> : null}
              </div>
              <div style={{ marginTop: 34, fontFamily: it.mono ? CLAUDE_FONT.mono : CLAUDE_FONT.serif, fontSize: it.mono ? 60 : 66,
                            fontWeight: 600, color: CLAUDE.INK, opacity: landed[i] ? 1 : 0 }}>
                {it.label}
              </div>
              <div style={{ marginTop: 10, width: 120 * s, height: 8, borderRadius: 4, opacity: landed[i] ? 1 : 0,
                            background: i === current ? CLAUDE.SPARK : CLAUDE.BORDER }} />
              {it.sub ? (
                <div style={{ marginTop: 20, fontFamily: CLAUDE_FONT.serif, fontSize: 44, color: CLAUDE.INK, textAlign: 'center',
                              lineHeight: 1.2, opacity: landed[i] ? 1 : 0 }}>
                  {it.sub}
                </div>
              ) : null}
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

export const libraryIconRowDefaultProps: LibraryIconRowProps = libraryIconRowSchema.parse({
  title: 'Three Ways To Run',
  items: [{ label: 'sbatch', sub: 'runs without you', icon: 'file-code', at: 0.2, mono: true },
          { label: 'srun', sub: 'an interactive shell', icon: 'terminal', at: 0.35, mono: true },
          { label: 'Open OnDemand', sub: 'in the browser', icon: 'browser', at: 0.7 }],
});
