import { random, staticFile } from 'remotion';

/**
 * PROFESSOR BEAR LAW (Bear, 2026-10-07): a person icon, or Professor Bear himself, is never a drawn
 * token or a library icon. It is one of the portraits in brutalist.art/professor-bear/, chosen at random
 * among those of the right aspect ratio. Downscaled copies live in public/professor-bear/ as
 * professor-bear-<ratio>-NN.jpg; the counts below must match that folder (see its manifest.json).
 * Cropping is fine (Bear, 2026-10-07): a circle, a rounded square, a tight head-and-shoulders — whatever the slot needs.
 */
export type BearRatio = '1x1' | '2x3' | '16x9';
export const PROFESSOR_BEAR_COUNTS: Record<BearRatio, number> = { '1x1': 287, '2x3': 46, '16x9': 13 };
export const PROFESSOR_BEAR_ASPECT: Record<BearRatio, number> = { '1x1': 1, '2x3': 2 / 3, '16x9': 16 / 9 };

/** A stable pick: same seed → same portrait on every render. Use the beat id as the seed. */
export function pickProfessorBear(ratio: BearRatio, seed: string): string {
  const n = PROFESSOR_BEAR_COUNTS[ratio];
  const k = 1 + Math.floor(random(`professor-bear:${ratio}:${seed}`) * n);
  return staticFile(`professor-bear/professor-bear-${ratio}-${String(k).padStart(2, '0')}.jpg`);
}
