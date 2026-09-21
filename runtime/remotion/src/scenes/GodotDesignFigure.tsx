import React from 'react';
import {AbsoluteFill, Img, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {z} from 'zod';
import {CLAUDE as C, CLAUDE_FONT as F} from '../tokens/claude';

/** GDD figure view: one full-width design diagram or real engine capture with a
 * status banner and up to four cue-lit cards (short: they never wrap or truncate). Use when the figure IS the beat and
 * the GodotDesignBoard's excerpt column would shrink it below legibility. The
 * image is supplied by the reel (data URI or staticFile); dashed elements in a
 * diagram are proposals, solid ones are observed — the banner says which. */
export const godotDesignFigureSchema=z.object({
 title:z.string(),status:z.string(),image:z.string(),imageLabel:z.string().default(''),
 excerpt:z.string().default(''),source:z.string(),
 cards:z.array(z.object({label:z.string(),text:z.string()})).min(1).max(4),
 cues:z.array(z.object({at:z.number().nonnegative(),card:z.number().int().nonnegative()})).default([]),
 durationSeconds:z.number().positive().default(20),
});
export const GodotDesignFigure:React.FC<z.infer<typeof godotDesignFigureSchema>>=(p)=>{
 const {width,height,fps}=useVideoConfig(),frame=useCurrentFrame(),portrait=height>width;
 const current=[...p.cues].reverse().find(c=>frame/fps>=c.at)?.card ?? -1;
 const pad=width*.055;
 return <AbsoluteFill style={{background:C.PAGE,color:C.INK,fontFamily:F.ui}}>
  <div style={{position:'absolute',top:height*.045,left:pad,right:pad,fontFamily:F.serif,fontSize:portrait?58:56,lineHeight:1.1}}>{p.title}</div>
  <div style={{position:'absolute',left:pad,right:pad,top:height*.135,bottom:height*.115,display:'flex',flexDirection:'column',gap:14,minHeight:0}}>
   <div style={{display:'flex',gap:16,alignItems:'stretch'}}>
    <div style={{background:'#303d34',color:'#fffdf8',padding:'12px 22px',borderRadius:10,fontSize:25,lineHeight:1.25,fontWeight:700,flex:'0 0 auto',maxWidth:'62%'}}>{p.status}</div>
    {p.excerpt?<div style={{flex:1,minWidth:0,borderLeft:'5px solid #985039',paddingLeft:18,fontFamily:F.serif,fontSize:27,lineHeight:1.25,overflow:'hidden',display:'-webkit-box',WebkitLineClamp:2,WebkitBoxOrient:'vertical' as const}}>{p.excerpt}</div>
     :<div style={{flex:1,minWidth:0,fontSize:24,color:'#564739',alignSelf:'center'}}>{p.imageLabel}</div>}
   </div>
   <div style={{flex:1,minHeight:0,position:'relative',background:'#fffdf8',border:'2px solid #cfc6b5',borderRadius:14}}>
    <Img src={p.image.startsWith('data:')?p.image:staticFile(p.image)} style={{position:'absolute',inset:10,width:'calc(100% - 20px)',height:'calc(100% - 20px)',objectFit:'contain'}}/>
   </div>
   <div style={{display:'grid',gridTemplateColumns:`repeat(${p.cards.length},1fr)`,gap:12,flex:'0 0 auto'}}>
    {p.cards.map((v,i)=><div key={i} style={{padding:'12px 18px',border:`2px solid ${i===current?'#985039':'#ccc6ba'}`,borderLeft:`7px solid ${i===current?'#985039':'#ccc6ba'}`,background:i===current?'#f2e5d8':'#fffdf8',borderRadius:10,minWidth:0}}>
     <div style={{fontSize:26,fontWeight:700,color:'#663725',lineHeight:1.2,whiteSpace:'nowrap',overflow:'hidden',textOverflow:'ellipsis'}}>{v.label}</div>
     <div style={{fontSize:24,lineHeight:1.25,marginTop:6,whiteSpace:'nowrap',overflow:'hidden',textOverflow:'ellipsis'}}>{v.text}</div>
    </div>)}
   </div>
  </div>
  <div style={{position:'absolute',left:pad,bottom:height*.045,maxWidth:width*.72,fontSize:22,color:'#564739',lineHeight:1.2}}>{p.source}</div>
  <div style={{position:'absolute',right:pad,bottom:height*.04,fontSize:28,fontFamily:F.serif}}>@NikBearBrown</div>
 </AbsoluteFill>;
};
