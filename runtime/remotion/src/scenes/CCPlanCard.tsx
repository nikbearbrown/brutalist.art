import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring } from 'remotion';
import { z } from 'zod';
import { CC, CC_FONT } from '../tokens/claudecode';
import { AnchorContext } from './CursorLayer';
import { CCShell, CC_BODY } from './CCShell';

/**
 * CCPlanCard — bordered rounded plan box. Sections (e.g. "Files to create",
 * "Verification") with optional numbered steps and inline file-path
 * highlighting. Designed to sit inside CCSession as a 'plan' block type;
 * also registered standalone for Studio previews.
 *
 * Path values are rendered in CC.VIOLET monospace at the end of item text,
 * distinguishing file references from prose descriptions.
 */

// ── Schema ────────────────────────────────────────────────────────────────────

export const planItemSchema = z.object({
  text: z.string(),
  path: z.string().optional(),
});
export type PlanItem = z.infer<typeof planItemSchema>;

export const planSectionSchema = z.object({
  title:    z.string(),
  numbered: z.boolean().default(false),
  items:    z.array(planItemSchema).default([]),
});
export type PlanSection = z.infer<typeof planSectionSchema>;

export const ccPlanCardSchema = z.object({
  sections: z.array(planSectionSchema).default([]),
});
export type CCPlanCardProps = z.infer<typeof ccPlanCardSchema>;

// ── Helpers ───────────────────────────────────────────────────────────────────

const clamp = (v: number, a: number, b: number) => Math.min(b, Math.max(a, v));
const SPRING = { damping: 26, stiffness: 120, mass: 0.9 };

// ── Content renderer (no shell — used by CCSession inline) ────────────────────

export interface CCPlanCardContentProps {
  sections: PlanSection[];
  frame:    number;
  fps:      number;
  /** Absolute top offset within the CCSession body div (default 0). */
  offsetY?: number;
}

export const CCPlanCardContent: React.FC<CCPlanCardContentProps> = ({
  sections, frame, fps, offsetY = 0,
}) => {
  const CARD_BORDER  = `1.5px solid ${CC.BORDER}`;
  const SECT_TITLE_H = 52;  // section heading size — above §8.1 floor
  const ITEM_SIZE    = 52;  // item text size
  const PATH_SIZE    = 48;  // path size

  // Flatten items for stagger index
  const flatItems: { sIdx: number; iIdx: number }[] = [];
  sections.forEach((s, si) =>
    s.items.forEach((_, ii) => flatItems.push({ sIdx: si, iIdx: ii })),
  );

  // The card expands section-by-section with a gentle spring
  const cardIn = spring({ frame, fps, config: SPRING });

  return (
    <div style={{
      background:   CC.PANEL,
      border:       CARD_BORDER,
      borderRadius: 14,
      overflow:     'hidden',
      opacity:      clamp(cardIn, 0, 1),
      transform:    `translateY(${(1 - clamp(cardIn, 0, 1)) * 12}px)`,
    }}>
      {sections.map((section, si) => {
        const prevItemCount = flatItems.filter(fi => fi.sIdx < si).length;

        return (
          <div key={si} style={{
            borderTop: si > 0 ? `1px solid ${CC.BORDER}` : undefined,
            padding: '18px 22px',
          }}>
            {/* Section title */}
            <div style={{
              fontFamily:  CC_FONT.ui,
              fontSize:    SECT_TITLE_H,
              fontWeight:  700,
              color:       CC.INK,
              lineHeight:  1.25,
              marginBottom: 14,
              letterSpacing: '-0.01em',
            }}>
              {section.title}
            </div>

            {/* Items */}
            {section.items.map((item, ii) => {
              const flatIdx    = prevItemCount + ii;
              const itemSpring = spring({
                frame: frame - flatIdx * 6,
                fps,
                config: SPRING,
              });
              const itemOp = clamp(itemSpring, 0, 1);

              return (
                <div
                  key={ii}
                  style={{
                    display:       'flex',
                    alignItems:    'baseline',
                    gap:           12,
                    marginBottom:  10,
                    opacity:       itemOp,
                    transform:     `translateX(${(1 - itemOp) * -8}px)`,
                  }}
                >
                  {/* Number or bullet */}
                  <span style={{
                    fontFamily: CC_FONT.mono,
                    fontSize:   ITEM_SIZE,
                    color:      CC.INK_2,
                    flexShrink: 0,
                    width:      40,
                    textAlign:  'right',
                  }}>
                    {section.numbered ? `${ii + 1}.` : '·'}
                  </span>

                  {/* Item text */}
                  <span style={{
                    fontFamily: CC_FONT.mono,
                    fontSize:   ITEM_SIZE,
                    color:      CC.INK,
                    lineHeight: 1.35,
                    flex:       1,
                  }}>
                    {item.text}
                    {item.path && (
                      <span style={{
                        marginLeft:  10,
                        fontFamily:  CC_FONT.mono,
                        fontSize:    PATH_SIZE,
                        color:       CC.VIOLET,
                        whiteSpace:  'nowrap',
                      }}>
                        {item.path}
                      </span>
                    )}
                  </span>
                </div>
              );
            })}
          </div>
        );
      })}
    </div>
  );
};

// ── Standalone composition wrapper ────────────────────────────────────────────

export const CCPlanCard: React.FC<CCPlanCardProps> = ({ sections }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const { register } = React.useContext(AnchorContext);

  // Anchor: centre of the plan card header
  register('cc.plan.header', CC_BODY.X + CC_BODY.W / 2, CC_BODY.Y + 40);

  return (
    <AbsoluteFill>
      <CCShell title="claude-code" mode="plan">
        <div style={{
          position: 'absolute',
          left:   16,
          right:  16,
          top:    12,
          bottom: 0,
        }}>
          <CCPlanCardContent
            sections={sections}
            frame={frame}
            fps={fps}
          />
        </div>
      </CCShell>
    </AbsoluteFill>
  );
};

// ── defaultProps ──────────────────────────────────────────────────────────────

export const ccPlanCardDefaultProps: CCPlanCardProps = ccPlanCardSchema.parse({
  sections: [
    {
      title:    '⚠ SET IN BEAT SHEET',
      numbered: false,
      items:    [{ text: '⚠ SET IN BEAT SHEET' }],
    },
  ],
});

// ── Demo twin ─────────────────────────────────────────────────────────────────

export const ccPlanCardDemoSchema = ccPlanCardSchema;
export type CCPlanCardDemoProps   = CCPlanCardProps;

export const CCPlanCardDemo: React.FC<CCPlanCardDemoProps> = (props) => (
  <CCPlanCard {...props} />
);

export const ccPlanCardDemoDefaultProps: CCPlanCardDemoProps = ccPlanCardDemoSchema.parse({
  sections: [
    {
      title:    'Files to create',
      numbered: true,
      items: [
        { text: 'Token palette',          path: 'src/tokens/claudecode.ts'         },
        { text: 'Terminal window chrome', path: 'src/scenes/CCShell.tsx'           },
        { text: 'Prompt bar',             path: 'src/scenes/CCPromptBar.tsx'       },
        { text: 'Tool call block',        path: 'src/scenes/CCToolCall.tsx'        },
        { text: 'Inline diff view',       path: 'src/scenes/CCDiff.tsx'            },
        { text: 'Status verb line',       path: 'src/scenes/CCStatusVerb.tsx'      },
        { text: 'Session compositor',     path: 'src/scenes/CCSession.tsx'         },
      ],
    },
    {
      title:    'Verification',
      numbered: true,
      items: [
        { text: 'npx tsc --noEmit passes with 0 new errors' },
        { text: 'All compositions visible in Remotion Studio' },
        { text: 'GATE T dark-polarity column confirmed in TYPECHECK.md' },
      ],
    },
  ],
});
