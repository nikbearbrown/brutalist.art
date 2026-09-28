import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring } from 'remotion';
import { z } from 'zod';
import { CC, CC_FONT } from '../tokens/claudecode';
import { AnchorContext } from './CursorLayer';
import { CCShell, CC_BODY } from './CCShell';
import { diffLineSchema } from './GitHubCodeDiff';
import { MascotSVG, computeAnimation } from './ClaudeMascotScene';

/**
 * CCThemePicker — syntax-theme selection overlay. Numbered option list with
 * ✓ on current choice and ❯ on active selection; optional diff preview shows
 * how the chosen theme looks; pixel mascot + inline flowers strip decorates
 * the bottom-right corner.
 *
 * PIXEL-ART LAW: MascotSVG uses translate + axis-aligned scale ONLY.
 * Flowers are inline rects — never CSS rotate or SVG transform="rotate(…)".
 */

// ── Schema ────────────────────────────────────────────────────────────────────

export const themeOptionSchema = z.object({
  label:    z.string(),
  current:  z.boolean().default(false),
  selected: z.boolean().default(false),
});
export type ThemeOption = z.infer<typeof themeOptionSchema>;

export const ccThemePickerSchema = z.object({
  title:   z.string().default('⚠ SET IN BEAT SHEET'),
  hint:    z.string().default(''),
  options: z.array(themeOptionSchema).default([]),
  preview: z.array(diffLineSchema).default([]),
});
export type CCThemePickerProps = z.infer<typeof ccThemePickerSchema>;

// ── Helpers ───────────────────────────────────────────────────────────────────

const clamp = (v: number, a: number, b: number) => Math.min(b, Math.max(a, v));
const SPRING = { damping: 26, stiffness: 120, mass: 0.9 };

// ── Pixel flower (all rects, no rotate) ──────────────────────────────────────

const PixelFlower: React.FC<{ x: number; y: number; color: string }> = ({ x, y, color }) => (
  <g>
    {/* center */}
    <rect x={x + 4} y={y + 4} width={6} height={6} fill={color} />
    {/* top / bottom / left / right petals */}
    <rect x={x + 4} y={y}     width={6} height={4} fill={color} />
    <rect x={x + 4} y={y + 10} width={6} height={4} fill={color} />
    <rect x={x}     y={y + 4} width={4} height={6} fill={color} />
    <rect x={x + 10} y={y + 4} width={4} height={6} fill={color} />
  </g>
);

// ── Diff preview row colors ───────────────────────────────────────────────────

const previewBg = (kind: 'add' | 'del' | 'context'): string =>
  kind === 'add' ? CC.ADD_BG : kind === 'del' ? CC.DEL_BG : 'transparent';

const previewFg = (kind: 'add' | 'del' | 'context'): string =>
  kind === 'add' ? CC.ADD_FG : kind === 'del' ? CC.DEL_FG : CC.INK_2;

const previewPrefix = (kind: 'add' | 'del' | 'context'): string =>
  kind === 'add' ? '+' : kind === 'del' ? '-' : ' ';

// ── Component ─────────────────────────────────────────────────────────────────

export const CCThemePicker: React.FC<CCThemePickerProps> = ({
  title, hint, options, preview,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const { register } = React.useContext(AnchorContext);

  register('cc.theme.header', CC_BODY.X + CC_BODY.W / 2, CC_BODY.Y + 40);

  const OPTION_H   = 68;
  const ITEM_SIZE  = 52;
  const HINT_SIZE  = 44;
  const FOOTER_SIZE = 44;
  const PREV_LINE_H = 52;
  const PADDING    = 24;

  const selectedOption = options.find(o => o.selected) ?? options.find(o => o.current);
  const selectedLabel  = selectedOption?.label ?? title;

  // card-in spring
  const cardIn = spring({ frame, fps, config: SPRING });
  const cardOp = clamp(cardIn, 0, 1);

  // mascot idle animation
  const animState = computeAnimation('idle', frame, fps);

  return (
    <AbsoluteFill>
      <CCShell title={title} mode="default">
        <div style={{
          position: 'absolute',
          left:    16,
          right:   16,
          top:     12,
          bottom:  0,
          opacity: cardOp,
          transform: `translateY(${(1 - cardOp) * 12}px)`,
        }}>

          {/* ── Option list ──────────────────────────────────────────────── */}
          <div style={{
            background:   CC.PANEL,
            border:       `1.5px solid ${CC.BORDER}`,
            borderRadius: 14,
            overflow:     'hidden',
          }}>
            {options.map((opt, i) => {
              const rowSpring = spring({ frame: frame - i * 4, fps, config: SPRING });
              const rowOp = clamp(rowSpring, 0, 1);

              const isSelected = opt.selected;
              const isCurrent  = opt.current;

              return (
                <div
                  key={i}
                  style={{
                    display:         'flex',
                    alignItems:      'center',
                    gap:             16,
                    padding:         `10px ${PADDING}px`,
                    borderBottom:    i < options.length - 1 ? `1px solid ${CC.BORDER}` : undefined,
                    background:      isSelected ? `${CC.VIOLET}18` : 'transparent',
                    opacity:         rowOp,
                    transform:       `translateX(${(1 - rowOp) * -10}px)`,
                  }}
                >
                  {/* row glyph: ❯ selected, ✓ current, number otherwise */}
                  <span style={{
                    fontFamily:  CC_FONT.mono,
                    fontSize:    ITEM_SIZE,
                    color:       isSelected ? CC.VIOLET : isCurrent ? CC.DONE : CC.INK_3,
                    width:       52,
                    textAlign:   'right',
                    flexShrink:  0,
                  }}>
                    {isSelected ? '❯' : isCurrent ? '✓' : `${i + 1}.`}
                  </span>

                  {/* label */}
                  <span style={{
                    fontFamily: CC_FONT.mono,
                    fontSize:   ITEM_SIZE,
                    color:      isSelected ? CC.INK : isCurrent ? CC.INK : CC.INK_2,
                    fontWeight: isSelected || isCurrent ? 600 : 400,
                    flex:       1,
                  }}>
                    {opt.label}
                  </span>

                  {/* current badge */}
                  {isCurrent && !isSelected && (
                    <span style={{
                      fontFamily:  CC_FONT.mono,
                      fontSize:    40,
                      color:       CC.DONE,
                      flexShrink:  0,
                    }}>
                      current
                    </span>
                  )}
                </div>
              );
            })}
          </div>

          {/* ── Hint line ────────────────────────────────────────────────── */}
          {hint.length > 0 && (
            <div style={{
              fontFamily:  CC_FONT.ui,
              fontSize:    HINT_SIZE,
              color:       CC.INK_3,
              marginTop:   16,
              paddingLeft: 4,
              lineHeight:  1.4,
              opacity:     clamp(spring({ frame: frame - options.length * 4, fps, config: SPRING }), 0, 1),
            }}>
              {hint}
            </div>
          )}

          {/* ── Diff preview ─────────────────────────────────────────────── */}
          {preview.length > 0 && (
            <div style={{
              marginTop:    20,
              background:   CC.PANEL,
              border:       `1.5px solid ${CC.BORDER}`,
              borderRadius: 10,
              overflow:     'hidden',
            }}>
              {preview.map((line, li) => {
                const lineSpring = spring({
                  frame: frame - (options.length * 4 + 8 + li * 3),
                  fps, config: SPRING,
                });
                const lineOp = clamp(lineSpring, 0, 1);
                return (
                  <div
                    key={li}
                    style={{
                      display:    'flex',
                      alignItems: 'center',
                      background: previewBg(line.kind),
                      opacity:    lineOp,
                      height:     PREV_LINE_H,
                      paddingLeft: 20,
                      gap:        12,
                    }}
                  >
                    <span style={{
                      fontFamily: CC_FONT.mono,
                      fontSize:   40,
                      color:      previewFg(line.kind),
                      flexShrink: 0,
                      width:      22,
                    }}>
                      {previewPrefix(line.kind)}
                    </span>
                    <span style={{
                      fontFamily: CC_FONT.mono,
                      fontSize:   40,
                      color:      previewFg(line.kind),
                      opacity:    line.kind === 'context' ? 0.65 : 1,
                    }}>
                      {line.text}
                    </span>
                  </div>
                );
              })}
            </div>
          )}

          {/* ── Footer ───────────────────────────────────────────────────── */}
          <div style={{
            fontFamily: CC_FONT.mono,
            fontSize:   FOOTER_SIZE,
            color:      CC.INK_3,
            marginTop:  18,
            paddingLeft: 4,
            opacity:    clamp(spring({ frame: frame - 20, fps, config: SPRING }), 0, 1),
          }}>
            {'Syntax theme: '}
            <span style={{ color: CC.INK }}>{selectedLabel}</span>
            {' ('}
            <span style={{ color: CC.VIOLET }}>ctrl+t</span>
            {' to disable)'}
          </div>

          {/* ── Mascot + flowers strip (bottom-right) ────────────────────── */}
          <div style={{
            position:  'absolute',
            right:     8,
            bottom:    8,
            width:     180,
            height:    100,
            opacity:   clamp(spring({ frame: frame - 10, fps, config: SPRING }), 0, 1),
          }}>
            {/* Pixel flowers — rects only, no rotate (PIXEL-ART LAW) */}
            <svg
              viewBox="0 0 180 100"
              style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%' }}
              shapeRendering="crispEdges"
            >
              <PixelFlower x={6}  y={60} color={CC.SPARK}  />
              <PixelFlower x={28} y={68} color={CC.VIOLET} />
              <PixelFlower x={50} y={62} color={CC.SPARK}  />
              <PixelFlower x={72} y={70} color={CC.VIOLET} />
            </svg>
            {/* Mascot */}
            <div style={{
              position: 'absolute',
              right:    0,
              bottom:   0,
              width:    96,
              height:   86,
            }}>
              <MascotSVG s={animState} scale={1} />
            </div>
          </div>

        </div>
      </CCShell>
    </AbsoluteFill>
  );
};

// ── defaultProps ──────────────────────────────────────────────────────────────

export const ccThemePickerDefaultProps: CCThemePickerProps = ccThemePickerSchema.parse({
  title:   '⚠ SET IN BEAT SHEET',
  hint:    '',
  options: [{ label: '⚠ SET IN BEAT SHEET' }],
  preview: [],
});

// ── Demo twin ─────────────────────────────────────────────────────────────────

export const ccThemePickerDemoSchema = ccThemePickerSchema;
export type CCThemePickerDemoProps   = CCThemePickerProps;

export const CCThemePickerDemo: React.FC<CCThemePickerDemoProps> = (props) => (
  <CCThemePicker {...props} />
);

export const ccThemePickerDemoDefaultProps: CCThemePickerDemoProps = ccThemePickerDemoSchema.parse({
  title: 'claude-code',
  hint:  'Select a syntax theme. Changes apply to all future sessions.',
  options: [
    { label: 'Dark (default)', current: true,  selected: false },
    { label: 'Light',          current: false, selected: false },
    { label: 'Solarized Dark', current: false, selected: true  },
    { label: 'Monokai',        current: false, selected: false },
    { label: 'Dracula',        current: false, selected: false },
  ],
  preview: [
    { kind: 'context', text: 'export function greet(name: string) {' },
    { kind: 'del',     text: '  return `Hello, ${name}!`;'           },
    { kind: 'add',     text: '  return `Hey there, ${name} 👋`;'     },
    { kind: 'context', text: '}'                                      },
  ],
});
