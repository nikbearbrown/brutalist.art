// claudecode — Claude Code terminal session palette.
// Dark warm terminal. Terracotta spark for status verb only.
// Violet for keybindings, paths, accept-edits highlight.
// VERBS: real product gerunds for CCStatusVerb beats.

export const CC = {
  PAGE:      '#1F1E1B',   // terminal ground — warm near-black
  PANEL:     '#252422',   // raised block bg (tool calls, prompts)
  BORDER:    '#3A3835',   // hairline separators
  PROMPT_BG: '#2C2B28',   // user prompt band

  INK:       '#F2F0E9',   // primary — warm off-white
  INK_2:     '#A8A398',   // secondary — args, metadata
  INK_3:     '#6B6760',   // ghost — elapsed, token counts

  SPARK:     '#D97757',   // terracotta — status verb spark glyph ✳
  VIOLET:    '#A78BFA',   // keybindings, paths, accept-edits

  ADD_BG:    '#1C3322',   // diff added line bg
  ADD_FG:    '#4ADE80',   // diff added accent
  DEL_BG:    '#3C1C1C',   // diff removed line bg
  DEL_FG:    '#F87171',   // diff removed accent

  DONE:      '#22C55E',   // tool-done bullet

  TL_RED:    '#FF5F57',
  TL_YEL:    '#FEBC2E',
  TL_GRN:    '#28C840',

  RADIUS:    10,
} as const;

export const CC_FONT = {
  ui:   '-apple-system, "SF Pro Text", "Segoe UI", "Helvetica Neue", sans-serif',
  mono: 'ui-monospace, "SF Mono", Menlo, "Cascadia Code", monospace',
} as const;

export const VERBS = [
  'Analyzing', 'Building', 'Checking', 'Compiling', 'Crafting',
  'Debugging', 'Deploying', 'Exploring', 'Fermenting', 'Generating',
  'Indexing', 'Installing', 'Investigating', 'Loading', 'Mapping',
  'Optimizing', 'Planning', 'Pontificating', 'Processing', 'Reading',
  'Reasoning', 'Running', 'Scanning', 'Searching', 'Spelunking',
  'Symbioting', 'Testing', 'Thinking', 'Updating', 'Writing',
] as const;
export type CCVerb = typeof VERBS[number];

export type CcTokens = typeof CC;
