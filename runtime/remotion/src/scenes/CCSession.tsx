import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate, spring } from 'remotion';
import { z } from 'zod';
import { CC, CC_FONT } from '../tokens/claudecode';
import { AnchorContext, AnchorCtx, AnchorPos } from './CursorLayer';
import { CCShell, CC_BODY, CC_LAYOUT } from './CCShell';
import { ANIMATIONS, AnimationName } from './ClaudeMascotScene';
import { diffLineSchema } from './GitHubCodeDiff';
import { planSectionSchema, CCPlanCardContent } from './CCPlanCard';

/**
 * CCSession — full CC terminal session. Stacks prompt/tool/diff/status blocks
 * inside CCShell with staggered live-session reveal. One beat = one block list.
 * Use the VERBS export from claudecode tokens for status beats.
 * `mascot: 'auto'` plants a corner Clawd whose pose follows the latest cued
 * block: prompt→look, status→think, tool/diff→type, plan→nod; 90 frames after
 * the last cue it celebrates. Any explicit animation name pins the pose.
 */

// ── Block schemas (discriminated union) ──────────────────────────────────────

const textBlockSchema = z.object({
  type: z.literal('text'),
  text: z.string(),
});

const promptBlockSchema = z.object({
  type:         z.literal('prompt'),
  text:         z.string(),
  cue:          z.number().int().default(0),
  typeDuration: z.number().int().default(60),
});

const toolChildSchema = z.object({
  name: z.string(),
  arg:  z.string().optional(),
});

const toolBlockSchema = z.object({
  type:           z.literal('tool'),
  name:           z.string(),
  arg:            z.string().optional(),
  state:          z.enum(['running', 'done']).default('running'),
  children:       z.array(toolChildSchema).optional(),
  moreCount:      z.number().int().optional(),
  backgroundHint: z.boolean().default(false),
});

const diffBlockSchema = z.object({
  type:     z.literal('diff'),
  file:     z.string(),
  addCount: z.number().int().default(0),
  delCount: z.number().int().default(0),
  lines:    z.array(diffLineSchema).default([]),
});

const statusBlockSchema = z.object({
  type:    z.literal('status'),
  verb:    z.string(),
  elapsed: z.string().optional(),
  tokens:  z.string().optional(),
});

const planBlockSchema = z.object({
  type:     z.literal('plan'),
  sections: z.array(planSectionSchema).default([]),
});

const blockSchema = z.discriminatedUnion('type', [
  textBlockSchema,
  promptBlockSchema,
  toolBlockSchema,
  diffBlockSchema,
  statusBlockSchema,
  planBlockSchema,
]);

export type CCBlock = z.infer<typeof blockSchema>;

// ── Session schema ────────────────────────────────────────────────────────────

export const ccSessionSchema = z.object({
  title:  z.string().default('⚠ SET IN BEAT SHEET'),
  mode:   z.enum(['accept-edits', 'plan', 'default']).default('default'),
  blocks: z.array(blockSchema).default([]),
  cues:   z.array(z.number().int()).optional(),
  mascot: z.union([z.literal('off'), z.literal('auto'), z.enum(ANIMATIONS)]).default('off'),
});
export type CCSessionProps = z.infer<typeof ccSessionSchema>;

// ── Block height estimation ───────────────────────────────────────────────────

function estimateBlockHeight(block: CCBlock): number {
  switch (block.type) {
    case 'text':    return 68;
    case 'prompt':  return 88;
    case 'tool': {
      const childLines = (block.children?.length ?? 0) * 60;
      const moreLine   = (block.moreCount != null && block.moreCount > 0) ? 56 : 0;
      const bgLine     = block.backgroundHint ? 56 : 0;
      return 68 + childLines + moreLine + bgLine;
    }
    case 'diff':    return 56 + 48 + block.lines.length * 56;
    case 'status':  return 80;
    case 'plan': {
      const titleLines = block.sections.length;
      const itemLines  = block.sections.reduce((sum, s) => sum + s.items.length, 0);
      return titleLines * 78 + itemLines * 62 + 36;
    }
    default:        return 68;
  }
}

const clamp = (v: number, a: number, b: number) => Math.min(b, Math.max(a, v));
const SPRING_CFG = { damping: 26, stiffness: 120, mass: 0.9 };

// ── Braille spinner ───────────────────────────────────────────────────────────
const BRAILLE = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'];

const VIOLET_BINDINGS = ['shift+tab', 'esc', '/effort', 'ctrl+b', 'ctrl+o'];

function renderWithBinding(text: string, bindings: string[]): React.ReactNode {
  const pattern = new RegExp(`(${bindings.map(b => b.replace(/[+/]/g, '\\$&')).join('|')})`, 'g');
  const parts = text.split(pattern);
  return parts.map((part, i) => (
    <span key={i} style={{ color: bindings.includes(part) ? CC.VIOLET : 'inherit', whiteSpace: 'pre' }}>
      {part}
    </span>
  ));
}

// ── Block renderers (inline, no circular dep) ─────────────────────────────────

function RenderTextBlock({ block, frame }: { block: z.infer<typeof textBlockSchema>; frame: number }) {
  return (
    <div style={{
      fontFamily: CC_FONT.mono,
      fontSize: 52,
      color: CC.INK,
      lineHeight: 1.3,
      padding: '8px 0',
    }}>
      {block.text}
    </div>
  );
}

function RenderPromptBlock({ block, frame }: { block: z.infer<typeof promptBlockSchema>; frame: number }) {
  const localFrame  = frame - block.cue;
  const charRate    = block.text.length / Math.max(1, block.typeDuration);
  const charsVisible = localFrame < 0 ? 0 : Math.min(block.text.length, Math.floor(localFrame * charRate));
  const isTyping    = charsVisible < block.text.length;
  const visibleText = block.text.slice(0, charsVisible);
  const cursorOn    = isTyping && Math.floor(frame / 8) % 2 === 0;

  return (
    <div style={{
      background: CC.PROMPT_BG,
      borderTop:    `1px solid ${CC.BORDER}`,
      borderBottom: `1px solid ${CC.BORDER}`,
      height: 88,
      display: 'flex',
      alignItems: 'center',
      paddingLeft: 12,
      paddingRight: 12,
    }}>
      <span style={{
        fontFamily: CC_FONT.mono,
        fontSize: 52,
        color: CC.VIOLET,
        marginRight: 10,
        flexShrink: 0,
        lineHeight: 1,
      }}>
        &gt;&nbsp;
      </span>
      <span style={{
        fontFamily: CC_FONT.mono,
        fontSize: 52,
        color: CC.INK,
        lineHeight: 1,
        flex: 1,
        overflow: 'hidden',
        whiteSpace: 'nowrap',
        textOverflow: 'ellipsis',
      }}>
        {visibleText}
        {cursorOn && (
          <span style={{
            display: 'inline-block',
            width: 2,
            height: 36,
            background: CC.VIOLET,
            verticalAlign: 'middle',
            marginLeft: 2,
          }} />
        )}
      </span>
    </div>
  );
}

function RenderToolBlock({ block, frame, fps }: {
  block: z.infer<typeof toolBlockSchema>;
  frame: number;
  fps: number;
}) {
  const isDone = block.state === 'done';
  const doneSpring = isDone ? spring({ frame, fps, config: SPRING_CFG }) : 0;
  const clamped = clamp(doneSpring, 0, 1);
  const spinnerIdx = Math.floor(frame / 3) % BRAILLE.length;
  const argStr = block.arg ? `(${block.arg})` : '()';

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 0 }}>
      {/* Header */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        gap: 14,
        height: 68,
      }}>
        <span style={{
          fontFamily: CC_FONT.mono,
          fontSize: 52,
          color: isDone ? CC.DONE : CC.SPARK,
          width: 52,
          textAlign: 'center',
          lineHeight: 1,
          transform: isDone ? `scale(${0.6 + 0.4 * clamped})` : 'scale(1)',
          display: 'inline-block',
        }}>
          {isDone ? '✓' : BRAILLE[spinnerIdx]}
        </span>
        <span style={{
          fontFamily: CC_FONT.mono,
          fontSize: 52,
          color: CC.INK,
          fontWeight: 700,
          lineHeight: 1,
        }}>
          {block.name}
        </span>
        <span style={{
          fontFamily: CC_FONT.mono,
          fontSize: 52,
          color: CC.INK_2,
          lineHeight: 1,
        }}>
          {argStr}
        </span>
      </div>
      {/* Children */}
      {(block.children ?? []).map((child, ci) => {
        const childArg = child.arg ? `(${child.arg})` : '()';
        return (
          <div key={ci} style={{
            display: 'flex',
            alignItems: 'center',
            gap: 12,
            height: 60,
            paddingLeft: 40,
            position: 'relative',
          }}>
            <div style={{
              width: 1,
              height: 60,
              background: CC.BORDER,
              position: 'absolute',
              left: 20,
              top: 0,
            }} />
            <span style={{ fontFamily: CC_FONT.mono, fontSize: 44, color: CC.INK_2 }}>
              {child.name}
            </span>
            <span style={{ fontFamily: CC_FONT.mono, fontSize: 44, color: CC.INK_3 }}>
              {childArg}
            </span>
          </div>
        );
      })}
      {/* +N more */}
      {block.moreCount != null && block.moreCount > 0 && (
        <div style={{
          paddingLeft: 40,
          height: 56,
          display: 'flex',
          alignItems: 'center',
          fontFamily: CC_FONT.mono,
          fontSize: 44,
          color: CC.INK_3,
        }}>
          {renderWithBinding(`+${block.moreCount} more tool uses (ctrl+o to expand)`, ['ctrl+o'])}
        </div>
      )}
      {/* ctrl+b hint */}
      {block.backgroundHint && (
        <div style={{
          paddingLeft: 40,
          height: 56,
          display: 'flex',
          alignItems: 'center',
          fontFamily: CC_FONT.mono,
          fontSize: 44,
          color: CC.INK_3,
        }}>
          {renderWithBinding('ctrl+b to run in background', ['ctrl+b'])}
        </div>
      )}
    </div>
  );
}

function RenderDiffBlock({ block, frame, fps }: {
  block: z.infer<typeof diffBlockSchema>;
  frame: number;
  fps: number;
}) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 0 }}>
      {/* Header */}
      <div style={{
        height: 56,
        display: 'flex',
        alignItems: 'center',
        fontFamily: CC_FONT.mono,
        fontSize: 52,
        color: CC.INK,
      }}>
        <span style={{ fontWeight: 700 }}>Update</span>
        <span>(</span>
        <span style={{ color: CC.VIOLET }}>{block.file}</span>
        <span>)</span>
      </div>
      {/* Summary */}
      <div style={{
        height: 48,
        display: 'flex',
        alignItems: 'center',
        fontFamily: CC_FONT.mono,
        fontSize: 44,
        color: CC.INK_2,
        gap: 12,
      }}>
        <span style={{ color: CC.ADD_FG }}>+{block.addCount} added</span>
        <span style={{ color: CC.INK_3 }}>·</span>
        <span style={{ color: CC.DEL_FG }}>{block.delCount} removed</span>
      </div>
      {/* Lines */}
      {block.lines.map((line, li) => {
        const revealStart = fps * 0.2 + li * 5;
        const revealEnd   = revealStart + 8;
        const opacity = interpolate(frame, [revealStart, revealEnd], [0, 1], {
          extrapolateLeft:  'clamp',
          extrapolateRight: 'clamp',
        });
        const bg =
          line.kind === 'add' ? CC.ADD_BG :
          line.kind === 'del' ? CC.DEL_BG :
          'transparent';
        const textColor =
          line.kind === 'add' ? CC.ADD_FG :
          line.kind === 'del' ? CC.DEL_FG :
          CC.INK;
        const gutterColor =
          line.kind === 'add' ? CC.ADD_FG :
          line.kind === 'del' ? CC.DEL_FG :
          CC.INK_3;
        return (
          <div key={li} style={{
            height: 56,
            display: 'flex',
            alignItems: 'center',
            background: bg,
            opacity,
          }}>
            <div style={{
              width: 60,
              flexShrink: 0,
              textAlign: 'center',
              fontFamily: CC_FONT.mono,
              fontSize: 44,
              color: gutterColor,
            }}>
              {line.gutter}
            </div>
            <div style={{
              flex: 1,
              fontFamily: CC_FONT.mono,
              fontSize: 48,
              color: textColor,
              whiteSpace: 'pre',
              overflow: 'hidden',
              paddingLeft: 8,
            }}>
              {line.text}
            </div>
          </div>
        );
      })}
    </div>
  );
}

function RenderStatusBlock({ block, frame }: {
  block: z.infer<typeof statusBlockSchema>;
  frame: number;
}) {
  const sparkScale = 1 + 0.12 * Math.sin(frame * 0.2);
  const dotCount   = (Math.floor(frame / 10) % 3) + 1;
  const ellipsis   = '.'.repeat(dotCount);
  const metaParts: string[] = [];
  if (block.elapsed) metaParts.push(block.elapsed);
  if (block.tokens)  metaParts.push(`↓ ${block.tokens}`);
  const meta = metaParts.join(' · ');

  return (
    <div style={{
      height: 80,
      display: 'flex',
      alignItems: 'center',
      gap: 14,
      fontFamily: CC_FONT.mono,
      fontSize: 58,
    }}>
      <span style={{
        color: CC.SPARK,
        display: 'inline-block',
        transform: `scale(${sparkScale})`,
        transformOrigin: 'center',
        lineHeight: 1,
      }}>✳</span>
      <span style={{ color: CC.INK, fontWeight: 700, lineHeight: 1 }}>{block.verb}</span>
      <span style={{ color: CC.INK_2, minWidth: 48, lineHeight: 1 }}>{ellipsis}</span>
      {meta.length > 0 && (
        <span style={{ color: CC.INK_3, fontSize: 48, lineHeight: 1 }}>({meta})</span>
      )}
    </div>
  );
}

// ── Component ─────────────────────────────────────────────────────────────────

export const CCSession: React.FC<CCSessionProps> = ({ title, mode, blocks, cues, mascot = 'off' }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Anchor context
  const anchorMapRef = React.useRef<Map<string, AnchorPos>>(new Map());
  const ctx = React.useMemo<AnchorCtx>(() => {
    anchorMapRef.current = new Map();
    return {
      register: (id, x, y) => anchorMapRef.current.set(id, { x, y }),
      resolve:  (id)       => anchorMapRef.current.get(id),
    };
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [frame]);

  // Build vertical layout — cumulative top offsets
  const blockTops: number[] = [];
  let cursor = 0;
  for (const b of blocks) {
    blockTops.push(cursor);
    cursor += estimateBlockHeight(b);
  }

  // Register session-level anchors
  let lastPromptIdx = -1;
  let statusIdx     = -1;
  blocks.forEach((b, i) => {
    if (b.type === 'prompt')  lastPromptIdx = i;
    if (b.type === 'status')  statusIdx     = i;
  });

  const { WIN_X, WIN_Y, TB_H } = CC_LAYOUT;
  const BODY_ORIGIN_Y = WIN_Y + TB_H;

  if (lastPromptIdx >= 0) {
    const h = estimateBlockHeight(blocks[lastPromptIdx]);
    ctx.register(
      'cc.session.prompt',
      WIN_X + CC_LAYOUT.WIN_W / 2,
      BODY_ORIGIN_Y + blockTops[lastPromptIdx] + h / 2,
    );
  }

  blocks.forEach((b, i) => {
    if (b.type === 'tool') {
      const h = estimateBlockHeight(b);
      ctx.register(
        `cc.session.tool.${i}`,
        WIN_X + CC_LAYOUT.WIN_W / 2,
        BODY_ORIGIN_Y + blockTops[i] + h / 2,
      );
    }
  });

  if (statusIdx >= 0) {
    const h = estimateBlockHeight(blocks[statusIdx]);
    ctx.register(
      'cc.session.status',
      WIN_X + CC_LAYOUT.WIN_W / 2,
      BODY_ORIGIN_Y + blockTops[statusIdx] + h / 2,
    );
  }

  // ── Clawd pose (prop-gated; 'auto' derives from the latest cued block) ──
  let mascotAnim: AnimationName | undefined;
  if (mascot !== 'off') {
    if (mascot !== 'auto') {
      mascotAnim = mascot;
    } else if (blocks.length > 0) {
      let latest = -1;
      blocks.forEach((b, i) => {
        const c = cues?.[i] ?? i * 20;
        if (frame >= c) latest = i;
      });
      const lastCue = cues?.[blocks.length - 1] ?? (blocks.length - 1) * 20;
      if (latest < 0) {
        mascotAnim = 'idle';
      } else if (frame > lastCue + 90) {
        mascotAnim = 'celebrate';
      } else {
        const b = blocks[latest];
        mascotAnim =
          b.type === 'prompt' ? 'look'  :
          b.type === 'status' ? 'think' :
          b.type === 'tool'   ? 'type'  :
          b.type === 'diff'   ? 'type'  :
          b.type === 'plan'   ? 'nod'   : 'idle';
      }
    }
  }

  return (
    <AbsoluteFill style={{ background: CC.PAGE }}>
      <AnchorContext.Provider value={ctx}>
        <CCShell title={title} mode={mode} mascot={mascotAnim}>
          <div style={{
            position: 'absolute',
            left: 16,
            right: 16,
            top: 12,
            bottom: 0,
            overflowY: 'hidden',
          }}>
            {blocks.map((block, i) => {
              const blockCue = cues?.[i] ?? (i * 20);
              const blockFrame = frame - blockCue;

              // Spring opacity+translateY for each block
              const entrySpring = spring({
                frame: blockFrame,
                fps,
                config: SPRING_CFG,
              });
              const opacity    = clamp(entrySpring, 0, 1);
              const translateY = (1 - opacity) * 16;

              return (
                <div
                  key={i}
                  style={{
                    position: 'absolute',
                    left: 0,
                    right: 0,
                    top: blockTops[i],
                    opacity,
                    transform: `translateY(${translateY}px)`,
                  }}
                >
                  {block.type === 'text'   && <RenderTextBlock   block={block} frame={frame} />}
                  {block.type === 'prompt' && <RenderPromptBlock block={block} frame={frame} />}
                  {block.type === 'tool'   && <RenderToolBlock   block={block} frame={frame} fps={fps} />}
                  {block.type === 'diff'   && <RenderDiffBlock   block={block} frame={frame} fps={fps} />}
                  {block.type === 'status' && <RenderStatusBlock block={block} frame={frame} />}
                  {block.type === 'plan'   && (
                    <CCPlanCardContent
                      sections={block.sections}
                      frame={blockFrame}
                      fps={fps}
                      offsetY={blockTops[i]}
                    />
                  )}
                </div>
              );
            })}
          </div>
        </CCShell>
      </AnchorContext.Provider>
    </AbsoluteFill>
  );
};

// ── defaultProps ──────────────────────────────────────────────────────────────

export const ccSessionDefaultProps: CCSessionProps = ccSessionSchema.parse({});

// ── Demo ──────────────────────────────────────────────────────────────────────

export const ccSessionDemoSchema = ccSessionSchema;
export type CCSessionDemoProps = CCSessionProps;

export const CCSessionDemo: React.FC<CCSessionDemoProps> = (props) => {
  return <CCSession {...props} />;
};

export const ccSessionDemoDefaultProps: CCSessionDemoProps = ccSessionDemoSchema.parse({
  title: 'brutalist-art · src/scenes',
  mode:  'accept-edits',
  blocks: [
    {
      type: 'prompt',
      text: 'add a CCDiff component to the CC kit — dark diff bands, gutter numbers',
      cue:  0,
      typeDuration: 70,
    },
    {
      type:    'status',
      verb:    'Spelunking',
      elapsed: '0m 12s',
      tokens:  '1.2k tokens',
    },
    {
      type:     'tool',
      name:     'Explore',
      arg:      'src/scenes/',
      state:    'done',
      children: [
        { name: 'Read', arg: 'GitHubCodeDiff.tsx'  },
        { name: 'Read', arg: 'CCSession.tsx'       },
      ],
      moreCount: 2,
    },
    {
      type:  'tool',
      name:  'Write',
      arg:   'src/scenes/CCDiff.tsx',
      state: 'running',
    },
    {
      type:     'diff',
      file:     'src/scenes/CCDiff.tsx',
      addCount: 52,
      delCount: 0,
      lines: [
        { gutter: '1', text: "import React from 'react';",                         kind: 'context' },
        { gutter: '+', text: "import { diffLineSchema } from './GitHubCodeDiff';", kind: 'add'     },
        { gutter: '+', text: "export const CCDiff: React.FC<CCDiffProps> = ({",   kind: 'add'     },
        { gutter: '+', text: "  file, addCount, delCount, lines,",                kind: 'add'     },
      ],
    },
    {
      type:    'status',
      verb:    'Pontificating',
      elapsed: '1m 46s',
      tokens:  '5.0k tokens',
    },
  ],
  cues: [0, 40, 80, 130, 160, 240],
  mascot: 'auto',
});
