/**
 * ChatReplyMock — three-skin chat interface mock (chatgpt / gemini / claude) for
 * the "Everybody Picked 17" reel. Shows prompt typing → thinking → reply landing
 * → terracotta ring on ringToken. Deterministic: frame-time only, no CSS
 * transitions, no Math.random.
 */
import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate } from 'remotion';
import { z } from 'zod';
import { CLAUDE, CLAUDE_FONT } from '../tokens/claude';

export const chatReplyMockSchema = z.object({
  vendor: z.enum(['chatgpt', 'gemini', 'claude']),
  prompt: z.string().default('⚠ SET IN BEAT SHEET'),
  reply: z.string().default('⚠ SET IN BEAT SHEET'),
  replyEmphasis: z.string().optional(),
  title: z.string().optional(),
  sidebar: z.array(z.string()).optional(),
  promptTypeMs: z.number().default(35),
  replyAt: z.number().default(0.45),
  ringAt: z.number().default(0.75),
  ringToken: z.string().optional(),
  durationSeconds: z.number().default(8),
  cues: z.array(z.object({ at: z.number(), card: z.string() })).optional(),
});
export type ChatReplyMockProps = z.infer<typeof chatReplyMockSchema>;

// ── palette per vendor ────────────────────────────────────────────────────────
const SKIN = {
  chatgpt: {
    page: '#212121', sidebar: '#171717', sidebarW: 200,
    userBg: '#2F2F2F', userText: '#ECECEC',
    replyText: '#ECECEC', replyFont: CLAUDE_FONT.ui,
    thinkDot: '#B4B4B4', iconColor: '#B4B4B4',
    wordmark: 'ChatGPT', wordmarkColor: '#ECECEC',
  },
  gemini: {
    page: '#1B1C1D', sidebar: '#1B1C1D', sidebarW: 56,
    userBg: '#2A2B2D', userText: '#E3E3E3',
    replyText: '#E3E3E3', replyFont: CLAUDE_FONT.ui,
    thinkDot: '#8AB4F8', iconColor: '#C4C7C5',
    wordmark: 'Gemini', wordmarkColor: '#E3E3E3',
  },
  claude: {
    page: CLAUDE.PAGE, sidebar: '#F5F3EE', sidebarW: 270,
    userBg: '#F0EEE8', userText: CLAUDE.INK,
    replyText: CLAUDE.INK, replyFont: CLAUDE_FONT.serif,
    thinkDot: CLAUDE.SPARK, iconColor: CLAUDE.INK_SOFT,
    wordmark: 'Claude', wordmarkColor: CLAUDE.INK,
  },
} as const;

const clamp = (v: number, lo: number, hi: number) => Math.min(hi, Math.max(lo, v));

// Simple SVG outline icons (24×24 viewBox) returned as path strings
const ICON = {
  thumbUp: 'M7 22V11L4 11V22H7ZM7 11C7 11 9.5 10 10 7L11 2L12 2C13 2 14 3 14 4.5V7H19C20.1 7 21 7.9 21 9V10C21 10.6 20.8 11.1 20.4 11.5L18 19C17.6 20.2 16.5 21 15.3 21H10C8.3 21 7 19.7 7 18V11Z',
  thumbDown: 'M17 2V13L20 13V2H17ZM17 13C17 13 14.5 14 14 17L13 22L12 22C11 22 10 21 10 19.5V17H5C3.9 17 3 16.1 3 15V14C3 13.4 3.2 12.9 3.6 12.5L6 5C6.4 3.8 7.5 3 8.7 3H14C15.7 3 17 4.3 17 6V13Z',
  copy: 'M8 16H6C4.9 16 4 15.1 4 14V6C4 4.9 4.9 4 6 4H14C15.1 4 16 4.9 16 6V8M10 20H18C19.1 20 20 19.1 20 18V10C20 8.9 19.1 8 18 8H10C8.9 8 8 8.9 8 10V18C8 19.1 8.9 20 10 20Z',
  refresh: 'M1 4V10H7M23 20V14H17M20.49 9A9 9 0 0 0 5.64 5.64L1 10M23 14L18.36 18.36A9 9 0 0 1 3.51 15',
  more: 'M5 12C5 12.6 4.6 13 4 13C3.4 13 3 12.6 3 12C3 11.4 3.4 11 4 11C4.6 11 5 11.4 5 12ZM13 12C13 12.6 12.6 13 12 13C11.4 13 11 12.6 11 12C11 11.4 11.4 11 12 11C12.6 11 13 11.4 13 12ZM21 12C21 12.6 20.6 13 20 13C19.4 13 19 12.6 19 12C19 11.4 19.4 11 20 11C20.6 11 21 11.4 21 12Z',
  speaker: 'M11 5L6 9H2V15H6L11 19V5ZM19.07 4.93A10 10 0 0 1 19.07 19.07M15.54 8.46A5 5 0 0 1 15.54 15.54',
};

function SvgIcon({ path, size, color, strokeWidth = 2 }: { path: string; size: number; color: string; strokeWidth?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" style={{ display: 'block', flexShrink: 0 }}>
      <path d={path} stroke={color} strokeWidth={strokeWidth} strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

// Terracotta spark asterisk (8-point), matching ClaudeComposerAsk's brand accent
function SparkAsterisk({ size, opacity }: { size: number; opacity: number }) {
  const R = size / 2;
  const arms = 8;
  const pts: string[] = [];
  for (let i = 0; i < arms; i++) {
    const a = (i / arms) * Math.PI * 2;
    pts.push(`M ${R} ${R} L ${R + Math.cos(a) * R} ${R + Math.sin(a) * R}`);
  }
  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} style={{ opacity }}>
      {pts.map((d, i) => (
        <path key={i} d={d} stroke={CLAUDE.SPARK} strokeWidth={size * 0.08} strokeLinecap="round" />
      ))}
    </svg>
  );
}

export const ChatReplyMock: React.FC<ChatReplyMockProps> = (props) => {
  const {
    vendor, prompt, reply, replyEmphasis, title, sidebar,
    replyAt, ringAt, ringToken, durationSeconds,
  } = props;
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  const sk = SKIN[vendor];
  const totalFrames = durationSeconds * fps;
  const progress = clamp(frame / totalFrames, 0, 1);

  // Typing: 0 → 0.40 of progress
  const TYPING_END = 0.40;
  const typingFrac = clamp(progress / TYPING_END, 0, 1);
  const charsShown = Math.floor(typingFrac * prompt.length);
  const isTyping = charsShown < prompt.length;
  const blinkOn = Math.floor(frame / 11) % 2 === 0;

  // Thinking: 0.40 → replyAt
  const isThinking = progress >= TYPING_END && progress < replyAt;

  // Reply visible
  const replyOpacity = clamp(interpolate(progress, [replyAt, replyAt + 0.08], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }), 0, 1);
  const actionOpacity = clamp(interpolate(progress, [replyAt + 0.12, replyAt + 0.20], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }), 0, 1);

  // Ring draw progress
  const ringProgress = clamp(interpolate(progress, [ringAt, ringAt + 0.20], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }), 0, 1);

  // Layout constants
  const REPLY_SIZE = height * 0.044;   // ≈ 48px at 1080
  const PROMPT_SIZE = height * 0.040;  // ≈ 44px
  const ICON_SIZE = height * 0.020;    // ≈ 22px
  const SAFE_L = 96; const SAFE_R = width - 96;
  const SAFE_T = 54;  const SAFE_B = height - 54;
  const CONTENT_L = sk.sidebarW + 24;
  const CONTENT_W = (SAFE_R - 96) - CONTENT_L;
  const BODY_TOP = SAFE_T + height * 0.10;  // below header

  // Ring geometry — drawn as an SVG ellipse over the ringToken
  const RING_RX = REPLY_SIZE * 1.0;
  const RING_RY = REPLY_SIZE * 0.72;
  const RING_CIRC = Math.PI * (3 * (RING_RX + RING_RY) - Math.sqrt((3 * RING_RX + RING_RY) * (RING_RX + 3 * RING_RY)));
  const ringDashOffset = RING_CIRC * (1 - ringProgress);

  // Split reply into [before, ringToken, after] for ring overlay
  const ringIdx = ringToken ? reply.indexOf(ringToken) : -1;
  const replyBefore = ringIdx >= 0 ? reply.slice(0, ringIdx) : reply;
  const replyMid = ringIdx >= 0 ? ringToken! : '';
  const replyAfter = ringIdx >= 0 ? reply.slice(ringIdx + ringToken!.length) : '';

  // Helper: bold-emphasis in reply (gemini has "Let's go with **17**!")
  function renderReply() {
    if (!replyEmphasis || ringIdx < 0) {
      return (
        <span>
          {replyBefore}
          <span style={{ position: 'relative', display: 'inline-block' }}>
            {replyMid}
            {ringProgress > 0 && (
              <svg
                style={{ position: 'absolute', left: -RING_RX * 0.35, top: '50%', transform: 'translateY(-55%)', overflow: 'visible', pointerEvents: 'none' }}
                width={RING_RX * 2.7} height={RING_RY * 3.2} viewBox={`0 0 ${RING_RX * 2.7} ${RING_RY * 3.2}`}
              >
                <ellipse
                  cx={RING_RX * 1.35} cy={RING_RY * 1.6}
                  rx={RING_RX * 1.1} ry={RING_RY * 1.2}
                  fill="none"
                  stroke={CLAUDE.SPARK}
                  strokeWidth={Math.max(3, REPLY_SIZE * 0.07)}
                  strokeDasharray={RING_CIRC}
                  strokeDashoffset={ringDashOffset}
                  strokeLinecap="round"
                />
              </svg>
            )}
          </span>
          {replyAfter}
        </span>
      );
    }
    // replyEmphasis present: render matching substring as bold
    const emphIdx = reply.indexOf(replyEmphasis);
    if (emphIdx < 0) return <span>{reply}</span>;
    return (
      <span>
        {reply.slice(0, emphIdx)}
        <strong>{reply.slice(emphIdx, emphIdx + replyEmphasis.length)}</strong>
        {reply.slice(emphIdx + replyEmphasis.length)}
      </span>
    );
  }

  return (
    <AbsoluteFill style={{ backgroundColor: sk.page, overflow: 'hidden', fontFamily: CLAUDE_FONT.ui }}>

      {/* ── Sidebar ────────────────────────────────────────────────── */}
      {vendor === 'chatgpt' && (
        <div style={{ position: 'absolute', left: 0, top: 0, bottom: 0, width: sk.sidebarW, backgroundColor: sk.sidebar, display: 'flex', flexDirection: 'column', padding: '16px 12px', gap: 8 }}>
          <div style={{ fontSize: height * 0.016, color: sk.wordmarkColor, fontWeight: 600, marginBottom: 12 }}>{sk.wordmark}</div>
          <div style={{ fontSize: height * 0.014, color: '#6E6E6E', padding: '6px 8px', borderRadius: 6 }}>New chat</div>
          <div style={{ fontSize: height * 0.013, color: '#555', padding: '4px 8px' }}>Yesterday</div>
          <div style={{ fontSize: height * 0.013, color: '#555', padding: '4px 8px' }}>A week ago</div>
        </div>
      )}

      {vendor === 'gemini' && (
        <div style={{ position: 'absolute', left: 0, top: 0, bottom: 0, width: sk.sidebarW, backgroundColor: sk.sidebar, display: 'flex', flexDirection: 'column', alignItems: 'center', paddingTop: 20, gap: 20 }}>
          {/* 5 outline icon circles */}
          {[ICON.copy, ICON.refresh, ICON.thumbUp, ICON.thumbDown, ICON.more].map((p, i) => (
            <div key={i} style={{ opacity: 0.7 }}>
              <SvgIcon path={p} size={22} color={sk.iconColor} />
            </div>
          ))}
        </div>
      )}

      {vendor === 'claude' && (
        <div style={{ position: 'absolute', left: 0, top: 0, bottom: 0, width: sk.sidebarW, backgroundColor: sk.sidebar, display: 'flex', flexDirection: 'column', padding: '14px 16px', gap: 6, overflow: 'hidden' }}>
          {/* Wordmark row */}
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 10 }}>
            <span style={{ fontFamily: CLAUDE_FONT.serif, fontSize: height * 0.022, color: CLAUDE.INK, fontWeight: 600 }}>{sk.wordmark}</span>
            <div style={{ display: 'flex', gap: 10 }}>
              <SvgIcon path="M3 12H21M3 6H21M3 18H21" size={18} color={CLAUDE.INK_SOFT} />
              <SvgIcon path="M21 21L15 15M17 11A6 6 0 1 1 5 11A6 6 0 0 1 17 11Z" size={18} color={CLAUDE.INK_SOFT} />
            </div>
          </div>
          {/* Tabs */}
          <div style={{ display: 'flex', gap: 4, marginBottom: 8 }}>
            {['⌂ Home', '</> Code'].map((tab, i) => (
              <div key={i} style={{ fontSize: height * 0.014, padding: '4px 8px', borderRadius: 6, background: i === 1 ? CLAUDE.PILL : 'transparent', color: i === 1 ? CLAUDE.INK : CLAUDE.INK_SOFT, fontWeight: i === 1 ? 600 : 400 }}>{tab}</div>
            ))}
          </div>
          {/* Nav items */}
          {['New', 'Projects', 'Artifacts', 'Customize'].map(item => (
            <div key={item} style={{ fontSize: height * 0.014, color: CLAUDE.INK_SOFT, padding: '3px 6px' }}>{item}</div>
          ))}
          <div style={{ fontSize: height * 0.012, color: CLAUDE.GHOST, marginTop: 8, marginBottom: 2, textTransform: 'uppercase', letterSpacing: 1 }}>Starred</div>
          {(sidebar ?? ['CAJAL', 'Indiana', 'Promptster', 'Courses', 'Fry', 'CRITIQ', 'Brutalist', 'Ogilvy', 'Gru']).map(name => (
            <div key={name} style={{ fontSize: height * 0.013, color: CLAUDE.INK_SOFT, padding: '2px 6px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{name}</div>
          ))}
        </div>
      )}

      {/* ── Header bar ────────────────────────────────────────────── */}
      <div style={{ position: 'absolute', left: sk.sidebarW, right: 0, top: SAFE_T, height: height * 0.08, display: 'flex', alignItems: 'center', padding: `0 ${SAFE_L - sk.sidebarW > 0 ? 32 : 20}px`, justifyContent: 'space-between' }}>
        {vendor === 'gemini' ? (
          <>
            <span style={{ fontSize: height * 0.022, color: sk.wordmarkColor, fontWeight: 700 }}>{sk.wordmark}</span>
            <SvgIcon path={ICON.more} size={22} color={sk.iconColor} />
          </>
        ) : vendor === 'claude' ? (
          <>
            <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
              <span style={{ fontFamily: CLAUDE_FONT.serif, fontSize: height * 0.020, color: CLAUDE.INK }}>{title ?? 'Conversation'}</span>
              <span style={{ color: CLAUDE.INK_SOFT, fontSize: height * 0.018 }}>⌄</span>
            </div>
            <div style={{ fontSize: height * 0.014, color: CLAUDE.INK, border: `1px solid ${CLAUDE.BORDER}`, borderRadius: 8, padding: '5px 14px' }}>Share</div>
          </>
        ) : null}
      </div>

      {/* ── Chat body ─────────────────────────────────────────────── */}
      <div style={{ position: 'absolute', left: CONTENT_L, width: CONTENT_W, top: BODY_TOP, bottom: SAFE_B * 0.12, overflow: 'hidden', display: 'flex', flexDirection: 'column', gap: height * 0.030, paddingTop: 16 }}>

        {/* User bubble */}
        <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
          <div style={{
            maxWidth: '72%',
            background: sk.userBg,
            borderRadius: vendor === 'claude' ? 18 : 22,
            padding: `${height * 0.012}px ${height * 0.016}px`,
            fontSize: PROMPT_SIZE,
            color: sk.userText,
            whiteSpace: 'pre-wrap',
            wordBreak: 'break-word',
            lineHeight: 1.4,
          }}>
            {prompt.slice(0, charsShown)}
            {isTyping && blinkOn && (
              <span style={{ display: 'inline-block', width: 2, height: PROMPT_SIZE * 0.9, background: sk.userText, verticalAlign: 'text-bottom', marginLeft: 2, borderRadius: 1 }} />
            )}
          </div>
        </div>

        {/* Thinking indicator */}
        {isThinking && (
          <div style={{ display: 'flex', gap: 6, alignItems: 'center', marginLeft: 4 }}>
            {[0, 1, 2].map(i => {
              const pulse = clamp(interpolate((frame + i * 8) % 30, [0, 10, 20, 30], [0.3, 1, 0.3, 0.3], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }), 0, 1);
              return <div key={i} style={{ width: ICON_SIZE * 0.6, height: ICON_SIZE * 0.6, borderRadius: '50%', background: sk.thinkDot, opacity: pulse }} />;
            })}
          </div>
        )}

        {/* Reply */}
        {progress >= replyAt && (
          <div style={{ opacity: replyOpacity }}>
            <div style={{
              fontSize: REPLY_SIZE,
              fontFamily: sk.replyFont,
              color: sk.replyText,
              lineHeight: 1.5,
              marginLeft: 4,
              whiteSpace: 'pre-wrap',
              wordBreak: 'break-word',
              position: 'relative',
            }}>
              {replyEmphasis && ringIdx < 0 ? (
                // No separate ringToken — just render with bold emphasis
                (() => {
                  const ei = reply.indexOf(replyEmphasis);
                  if (ei < 0) return <span>{reply}</span>;
                  return (
                    <span>
                      {reply.slice(0, ei)}
                      <strong>{replyEmphasis}</strong>
                      {reply.slice(ei + replyEmphasis.length)}
                    </span>
                  );
                })()
              ) : renderReply()}
            </div>

            {/* Claude spark asterisk */}
            {vendor === 'claude' && (
              <div style={{ marginLeft: 4, marginTop: height * 0.01, opacity: actionOpacity }}>
                <SparkAsterisk size={height * 0.030} opacity={0.85} />
              </div>
            )}

            {/* Action icon row */}
            <div style={{ display: 'flex', gap: 14, marginTop: height * 0.012, marginLeft: 4, opacity: actionOpacity, alignItems: 'center' }}>
              {vendor === 'claude' && (
                <>
                  <SvgIcon path={ICON.copy} size={ICON_SIZE} color={sk.iconColor} />
                  <SvgIcon path={ICON.speaker} size={ICON_SIZE} color={sk.iconColor} />
                  <SvgIcon path={ICON.thumbUp} size={ICON_SIZE} color={sk.iconColor} />
                  <SvgIcon path={ICON.thumbDown} size={ICON_SIZE} color={sk.iconColor} />
                  <SvgIcon path={ICON.refresh} size={ICON_SIZE} color={sk.iconColor} />
                </>
              )}
              {vendor === 'gemini' && (
                <>
                  <SvgIcon path={ICON.thumbUp} size={ICON_SIZE} color={sk.iconColor} />
                  <SvgIcon path={ICON.thumbDown} size={ICON_SIZE} color={sk.iconColor} />
                  <SvgIcon path={ICON.refresh} size={ICON_SIZE} color={sk.iconColor} />
                  <SvgIcon path={ICON.copy} size={ICON_SIZE} color={sk.iconColor} />
                  <SvgIcon path={ICON.more} size={ICON_SIZE} color={sk.iconColor} />
                </>
              )}
              {vendor === 'chatgpt' && (
                <>
                  <SvgIcon path={ICON.copy} size={ICON_SIZE} color={sk.iconColor} />
                  <SvgIcon path={ICON.thumbUp} size={ICON_SIZE} color={sk.iconColor} />
                  <SvgIcon path={ICON.thumbDown} size={ICON_SIZE} color={sk.iconColor} />
                  <SvgIcon path={ICON.refresh} size={ICON_SIZE} color={sk.iconColor} />
                </>
              )}
            </div>
          </div>
        )}
      </div>

    </AbsoluteFill>
  );
};

// ── Demo twin ─────────────────────────────────────────────────────────────────
export const ChatReplyMockDemo: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const DUR = 10;
  const progress = Math.min(1, frame / (DUR * fps));
  const v = progress < 0.33 ? 'chatgpt' : progress < 0.66 ? 'gemini' : 'claude';
  return (
    <ChatReplyMock
      vendor={v}
      prompt="pick a number between 1 and 30"
      reply={v === 'gemini' ? "Let's go with 17!" : '17'}
      replyEmphasis={v === 'gemini' ? '17' : undefined}
      title={v === 'claude' ? 'Random number selection game' : undefined}
      sidebar={v === 'claude' ? ['CAJAL', 'Indiana', 'Promptster', 'Courses', 'Fry', 'CRITIQ', 'Brutalist', 'Ogilvy', 'Gru'] : undefined}
      replyAt={0.45}
      ringAt={0.72}
      ringToken="17"
      durationSeconds={DUR}
    />
  );
};
