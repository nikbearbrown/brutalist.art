import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring } from 'remotion';
import { z } from 'zod';
import { CLAUDE, CLAUDE_FONT } from '../tokens/claude';

/**
 * ClaudeVerdictArtifact — reusable verdict/artifact page in the Claude fidelity skin.
 * Renders an artifact window card (cream stage, white card, staggered lines).
 * Per ILLUSTRATE LAW this is a UI beat (verdict) — the Claude UI is the subject here.
 *
 * 2026-07 (your-turn skill): card enlarged from 860px to fill the frame at
 * legible size (was a ~45%-width UI mock marooned in dead space). Line numbers
 * are drawn by the component from list position; a defensive sanitizer strips
 * any leading "N." / "N)" an author typed into a line so the number never
 * renders twice. Feed artifactLines as BARE sentences.
 */

export const claudeVerdictArtifactSchema = z.object({
  artifactTitle: z.string().default('Verdict'),
  artifactHeading: z.string().default('The split'),
  brandLabel: z.string().optional(),
  lectureLayout: z.boolean().optional(),
  durationSeconds: z.number().optional(),
  lecturePageFrames: z.array(z.number()).optional(),
  /**
   * Optional (2026-10-26): scale the card and its type together. The card is
   * capped at 1560px, which puts a 16:9 master just under the canvas-fill law.
   * Omitted or 1, nothing changes.
   */
  fillScale: z.number().optional(),
  artifactLines: z.array(z.string()).default([
    'Chat: synchronous judgment — you, in the loop.',
    'Cowork: asynchronous recipes — runs while you rehearse.',
    'Code: the pipeline room — systems you own.',
  ]),
});
export type ClaudeVerdictArtifactProps = z.infer<typeof claudeVerdictArtifactSchema>;

const SERIF = CLAUDE_FONT.serif;
const SANS = CLAUDE_FONT.ui;

const clamp = (v: number, a: number, b: number) => Math.min(b, Math.max(a, v));

// Strip a leading "1." / "2)" / "3 -" an author may have typed into the line —
// the component owns the numbering, so authored digits would double-render.
const stripLeadNum = (s: string) => s.replace(/^\s*\d+\s*[.)\-–—:]\s*/, '');


export const ClaudeVerdictArtifact: React.FC<ClaudeVerdictArtifactProps> = ({
  artifactTitle, artifactHeading, artifactLines, brandLabel, lectureLayout, lecturePageFrames, fillScale}) => {
  const frame = useCurrentFrame();
  const { fps, width, durationInFrames } = useVideoConfig();

  const cardIn = spring({ frame, fps, config: { damping: 28, stiffness: 140, mass: 0.8 } });
  const headIn = spring({ frame: frame - 8, fps, config: { damping: 28, stiffness: 140, mass: 0.8 } });

  // Fill the frame: ~84% of width, capped so ultrawide stays readable.
  const fs = fillScale ?? 1;
  const cardW = Math.min(width * 0.84 * fs, 1560 * fs);
  const lines = (artifactLines ?? []).map(stripLeadNum);

  if (lectureLayout) {
    const pageCount=Math.ceil(lines.length/2);
    const start=Math.round(1.8*fps);
    const page=lecturePageFrames?.length
      ? Math.min(pageCount-1,lecturePageFrames.reduce((last,cue,i)=>frame>=cue?i:last,0))
      : Math.min(pageCount-1,Math.floor(Math.max(0,frame-start)/Math.max(1,(durationInFrames-start)/pageCount)));
    return <AbsoluteFill style={{background:'#F2F0E9',color:CLAUDE.INK,fontFamily:SERIF,padding:'90px 140px'}}>
      <div style={{border:'3px solid #3D3929',borderRadius:24,background:'#fffefb',height:780,padding:'45px 60px',boxSizing:'border-box'}}>
        <div style={{fontSize:44,borderBottom:'2px solid #3D3929',paddingBottom:25}}>{artifactTitle}</div>
        <div style={{fontSize:64,margin:'34px 0 55px'}}>{artifactHeading}</div>
        {lines.slice(page*2,page*2+2).map((line,j)=><div key={page*2+j} style={{display:'flex',gap:30,marginBottom:55,fontSize:58,lineHeight:1.25}}>
          <span style={{color:'#A64A24',minWidth:60}}>{page*2+j+1}.</span><span>{line}</span>
        </div>)}
      </div>
      {brandLabel?<div style={{position:'absolute',bottom:65,right:140,fontSize:40}}>{brandLabel}</div>:null}
    </AbsoluteFill>;
  }

  return (
    <AbsoluteFill style={{ background: '#F2F0E9', alignItems: 'center', justifyContent: 'center' }}>
      {brandLabel && <div style={{position:'absolute',right:width*.07,bottom:'6.5%',fontFamily:SERIF,fontSize:28,color:CLAUDE.INK}}>{brandLabel}</div>}
      {/* Artifact card */}
      <div style={{
        width: cardW,
        background: CLAUDE.CARD,
        borderRadius: 24,
        boxShadow: '0 20px 72px rgba(61,57,41,0.16)',
        border: `1px solid ${CLAUDE.BORDER}`,
        overflow: 'hidden',
        transform: `scale(${clamp(cardIn, 0, 1)})`,
        opacity: clamp(cardIn, 0, 1),
      }}>
        {/* Title bar */}
        <div style={{
          background: CLAUDE.PAGE, borderBottom: `1px solid ${CLAUDE.BORDER}`,
          padding: '22px 40px', display: 'flex', alignItems: 'center', gap: 16,
        }}>
          <span style={{ fontFamily: SERIF, fontSize: 30 * fs, color: CLAUDE.INK, fontWeight: 600 }}>
            {artifactTitle}
          </span>
        </div>

        {/* Artifact body */}
        <div style={{ padding: '48px 60px 54px' }}>
          {/* Heading */}
          <div style={{
            fontFamily: SERIF, fontSize: 46 * fs, fontWeight: 700, color: CLAUDE.INK,
            marginBottom: 36,
            opacity: clamp(headIn, 0, 1),
          }}>
            {artifactHeading}
          </div>

          {/* Lines */}
          {lines.map((line, i) => {
            const lineIn = spring({ frame: frame - (i + 2) * 7, fps, config: { damping: 28, stiffness: 140, mass: 0.8 } });
            const op = clamp(lineIn, 0, 1);
            const ty = (1 - op) * 12;
            return (
              <div key={i} style={{
                display: 'flex', alignItems: 'flex-start', gap: 22,
                marginBottom: 26, opacity: op, transform: `translateY(${ty}px)`,
              }}>
                <span style={{ fontFamily: SANS, fontSize: 28 * fs, color: CLAUDE.SPARK, flexShrink: 0, marginTop: 3, fontWeight: 700 }}>
                  {i + 1}.
                </span>
                <span style={{ fontFamily: SANS, fontSize: 28 * fs, color: CLAUDE.INK, lineHeight: 1.55 }}>
                  {line}
                </span>
              </div>
            );
          })}
        </div>
      </div>
    </AbsoluteFill>
  );
};
