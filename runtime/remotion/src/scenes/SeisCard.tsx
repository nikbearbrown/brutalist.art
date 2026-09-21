import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig, spring} from 'remotion';
import {z} from 'zod';
import {NEU, NEU_RED, FONT_NEU} from '../tokens/neu';
import {SPRING_SMOOTH} from '../tokens/vox';
import {useLato} from '../tokens/lato';

/**
 * SeisCard — the NEU Form A text card (the ONLY text card on the seis skin).
 * White ground, Lato, regular weight, sentence case, lines reveal staggered,
 * one NU Red rule. `label` is a small eyebrow (the subject's name, per the
 * profile modifier's "name recurs" rule, or an act title). Max 4 lines.
 */
export const seisCardSchema = z.object({
  label: z.string().default(''),
  lines: z.array(z.string()).default(['One idea.', 'Stated plainly.']),
  emphasis: z.number().int().min(-1).default(-1), // index of the ONE line set in red, or -1
});
export type SeisCardProps = z.infer<typeof seisCardSchema>;

export const SeisCard: React.FC<SeisCardProps> = ({label, lines, emphasis}) => {
  useLato();
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const PAD = width * 0.10;
  const n = Math.max(1, lines.length);
  // Estimate wrapped rows (Lato ≈ 0.5em per glyph) so long lines never bleed past the
  // title-safe bottom (VISUAL QC: edge-bleed) while the block still fills the frame
  // (FILL-THE-CANVAS: ≥55% of the safe area). The block is anchored to the safe bottom.
  const usable = width - PAD * 2;
  const rowsAt = (sz: number) => lines.reduce((acc, ln) => acc + Math.max(1, Math.ceil((ln.length * 0.5 * sz) / usable)), 0);
  let size = n <= 2 ? height * 0.105 : n === 3 ? height * 0.097 : height * 0.075;
  let rows = rowsAt(size);
  while (rows > 5 && size > height * 0.05) { size *= 0.92; rows = rowsAt(size); }
  const gap = height * 0.03;
  const blockH = rows * size * 1.18 + (n - 1) * gap;
  const top = Math.max(height * 0.30, height * 0.86 - blockH);
  const ruleIn = spring({frame, fps, config: SPRING_SMOOTH});
  const labelIn = spring({frame: frame - 4, fps, config: SPRING_SMOOTH});

  return (
    <AbsoluteFill style={{backgroundColor: NEU.CREAM, overflow: 'hidden'}}>
      <div style={{
        position: 'absolute', left: PAD, top: height * 0.16,
        width: width * 0.14 * ruleIn, height: Math.max(4, height * 0.007),
        backgroundColor: NEU_RED,
      }} />
      {label && (
        <div style={{
          position: 'absolute', left: PAD, top: height * 0.20,
          fontFamily: FONT_NEU.display, fontSize: height * 0.034, fontWeight: 400,
          color: NEU.SLATE, opacity: labelIn,
        }}>{label}</div>
      )}
      <div style={{
        position: 'absolute', left: PAD, right: PAD, top,
        display: 'flex', flexDirection: 'column', gap: height * 0.03,
      }}>
        {lines.map((ln, i) => {
          const s = spring({frame: frame - 10 - i * 9, fps, config: SPRING_SMOOTH});
          return (
            <div key={i} style={{
              fontFamily: FONT_NEU.display, fontSize: size, fontWeight: 400,
              lineHeight: 1.18, color: i === emphasis ? NEU_RED : NEU.INK,
              opacity: s, transform: `translateY(${(1 - s) * 14}px)`,
            }}>{ln}</div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
