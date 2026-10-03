import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring } from 'remotion';
import { z } from 'zod';
import { CC, CC_FONT } from '../tokens/claudecode';

/**
 * CCPlainShell — a plain terminal, not Claude Code. The window a cc-explainer
 * cuts to when the operator runs something OUTSIDE the session (a command the
 * session's fence blocked; a shell loop that wraps several sessions). Same
 * window shape and type size as CCShell so the cut is quiet, but no mode
 * footer, no Clawd, no product strings — nothing that would claim this is a
 * Claude Code session. Lines land one at a time; `$ ` lines are commands
 * (violet prompt), `# ` lines are comments (ghost ink), the rest is output.
 *
 * Doctrine: skills/make/cc-explainer/SKILL.md → REAL-SESSION LAW (rendering a
 * shell command inside the Claude Code chrome would show a session that never
 * happened).
 */

// ── Schema ────────────────────────────────────────────────────────────────────

export const ccPlainShellSchema = z.object({
  /** Window title, e.g. `zsh — ~/scratch`. */
  title:    z.string().default('⚠ SET IN BEAT SHEET'),
  /** Lines in order. `$ ` prefix = a command; `# ` prefix = a comment; else output. */
  lines:    z.array(z.string()).min(1).max(14).default(['$ ⚠ SET IN BEAT SHEET']),
  /** Frame the first line lands. */
  startCue: z.number().int().default(10),
  /** Frames between lines. Commands get an extra beat before their output. */
  lineGap:  z.number().int().default(14),
  /** Optional: the beat's measured audio. Sizes the composition so cues can run past 10 s. */
  durationSeconds: z.number().optional(),
});
export type CCPlainShellProps = z.infer<typeof ccPlainShellSchema>;

// ── Helpers ───────────────────────────────────────────────────────────────────

const clamp = (v: number, a: number, b: number) => Math.min(b, Math.max(a, v));
const SPRING = { damping: 26, stiffness: 160, mass: 0.8 };

// ── Component ─────────────────────────────────────────────────────────────────

export const CCPlainShell: React.FC<CCPlainShellProps> = ({ title, lines, startCue, lineGap }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const winIn = clamp(spring({ frame, fps, config: SPRING }), 0, 1);

  // Each command line waits an extra half-gap so the output reads as a reply.
  let t = startCue;
  const cues = lines.map((l) => {
    if (l.startsWith('$ ')) t += Math.round(lineGap / 2);
    const c = t; t += lineGap; return c;
  });

  return (
    <AbsoluteFill style={{ backgroundColor: CC.PAGE }}>
      <div style={{
        position: 'absolute', left: 140, right: 140, top: 68, bottom: 68,
        background: CC.PANEL, border: `1px solid ${CC.BORDER}`, borderRadius: CC.RADIUS + 4,
        boxShadow: '0 20px 60px rgba(0,0,0,0.45)', overflow: 'hidden',
        opacity: winIn, transform: `translateY(${(1 - winIn) * 10}px)`,
      }}>
        {/* title bar */}
        <div style={{ position: 'absolute', left: 0, right: 0, top: 0, height: 56, background: CC.PROMPT_BG, borderBottom: `1px solid ${CC.BORDER}`, display: 'flex', alignItems: 'center' }}>
          <div style={{ display: 'flex', gap: 10, marginLeft: 20 }}>
            {[CC.TL_RED, CC.TL_YEL, CC.TL_GRN].map((c, i) => <span key={i} style={{ width: 14, height: 14, borderRadius: 7, background: c, display: 'inline-block' }} />)}
          </div>
          <span style={{ position: 'absolute', left: 0, right: 0, textAlign: 'center', fontFamily: CC_FONT.ui, fontSize: 26, fontWeight: 600, color: CC.INK_2 }}>{title}</span>
        </div>
        {/* lines */}
        <div style={{ position: 'absolute', left: 28, right: 28, top: 84, bottom: 24, fontFamily: CC_FONT.mono, fontSize: 40, lineHeight: 1.55, color: CC.INK }}>
          {lines.map((l, i) => {
            const lineIn = clamp(spring({ frame: frame - cues[i], fps, config: SPRING }), 0, 1);
            const isCmd = l.startsWith('$ '); const isComment = l.startsWith('# ');
            return (
              <div key={i} style={{ whiteSpace: 'pre', overflow: 'hidden', textOverflow: 'ellipsis', opacity: lineIn, transform: `translateY(${(1 - lineIn) * 6}px)`,
                                    color: isComment ? CC.INK_3 : CC.INK }}>
                {isCmd ? <><span style={{ color: CC.VIOLET, fontWeight: 700 }}>$ </span>{l.slice(2)}</> : l}
              </div>
            );
          })}
        </div>
      </div>
    </AbsoluteFill>
  );
};

// ── defaultProps ──────────────────────────────────────────────────────────────

export const ccPlainShellDefaultProps: CCPlainShellProps = ccPlainShellSchema.parse({});

// ── Demo twin ─────────────────────────────────────────────────────────────────

export const ccPlainShellDemoSchema = ccPlainShellSchema;
export type CCPlainShellDemoProps   = CCPlainShellProps;

export const CCPlainShellDemo: React.FC<CCPlainShellDemoProps> = (props) => (
  <CCPlainShell {...props} />
);

export const ccPlainShellDemoDefaultProps: CCPlainShellDemoProps = ccPlainShellDemoSchema.parse({
  title: 'zsh — ~/scratch',
  lines: [
    '# the two commands the session could not run',
    '$ ls -d /Applications/Claude.app',
    '/Applications/Claude.app',
    '$ ls ~/.claude/skills',
    'claude-refactor',
    'is-done',
    '$ which claude && claude --version',
    '/opt/homebrew/bin/claude',
    '2.1.150 (Claude Code)',
  ],
});
