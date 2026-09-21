// NEU audience palette — Northeastern brand (brand law: runtime/design/NEU-DESIGN.md).
// Same ROLE KEYS as tokens/vox.ts. RED = brand / emphasis / primary series ONLY,
// NEVER state — so good/bad is carried by KEPT/LOST label + position, no hue coding.
// White ground only. Gold is ceremonial + large-area only. Type is Lato (FONT_NEU).
export const NEU = {
  CREAM: '#FFFFFF',    // ground — white only (brand standard; no cream/off-white)
  INK: '#000000',      // text / marks — NU black
  TEAL: '#000000',     // good / kept — BLACK; the label carries it (red is never state)
  CRIMSON: '#545454',  // bad / lost — GRAY; the label carries it (NEVER red)
  SLATE: '#545454',    // structure — neutral gray
  GOLD: '#A4804A',     // NU gold — highlighter, rare + large-area only (fails AA small)
  HAIRLINE: '#E3E3E3', // gridlines / neutral-1
} as const;

// NU Red — brand / emphasis / primary chart series only. Never a negative value.
export const NEU_RED = '#C8102E';

// NEU data-viz: NU brand FORBIDS the categorical rainbow. Primary series = NU Red,
// the rest = grays; gridline #E3E3E3. (House Okabe-Ito does not apply to NEU.)
export const NEU_SERIES = ['#C8102E', '#000000', '#545454', '#787878', '#C4C4C4'] as const;

// NEU type override — Lato (required by brand), regular-weight headings, sentence case.
// Bundle the Lato TTFs in runtime/fonts/Lato/ so Manim/Pango resolves the family.
export const FONT_NEU = {
  display: 'Lato, "Helvetica Neue", Arial, sans-serif',
  serif: 'Lato, "Helvetica Neue", Arial, sans-serif', // NEU has no editorial serif — Lato throughout
  mono: '"PT Mono", "SF Mono", Menlo, monospace',      // data numbers + math only
} as const;
