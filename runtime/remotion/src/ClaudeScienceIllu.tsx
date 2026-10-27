/**
 * ClaudeScienceIllu.tsx — parameterized wrappers for the structural illustration
 * family, registered as Remotion Compositions for the claude-liam-claude-science reel.
 *
 * Each wrapper accepts a `sparkLine` prop (the IlluStage header text) plus the
 * props of the underlying structural component. The stage is 1280×720 to match
 * the pixel geometry baked into the structural components.
 *
 * Composition IDs: ClaudeScienceLayerStack | ClaudeScienceSourceFlow | ClaudeScienceChipGrid
 */
import React from 'react';
import { z } from 'zod';
import { IlluStage } from './illustrations/kit';
import { LayerStack, SourceFlow, ChipGrid } from './illustrations/structural';

// ── ClaudeScienceLayerStack ────────────────────────────────────────────────
export const claudeScienceLayerStackSchema = z.object({
  sparkLine: z.string().default('Layers.'),
  layers: z.array(z.object({
    title: z.string(),
    sub: z.string(),
    accent: z.boolean().optional(),
  })).default([]),
  caption: z.string().optional(),
  top: z.number().optional(),
  /** Optional: scale the content box to satisfy the canvas-fill law. 1 = unchanged. */
  fillScale: z.number().optional(),
});
export type ClaudeScienceLayerStackProps = z.infer<typeof claudeScienceLayerStackSchema>;

export const ClaudeScienceLayerStack: React.FC<ClaudeScienceLayerStackProps> = (props) => (
  <IlluStage spark={props.sparkLine}>
    <LayerStack layers={props.layers} caption={props.caption} top={props.top} fillScale={props.fillScale} />
  </IlluStage>
);

// ── ClaudeScienceSourceFlow ────────────────────────────────────────────────
export const claudeScienceSourceFlowSchema = z.object({
  sparkLine: z.string().default('Data flows.'),
  sourceLabel: z.string().default('Source'),
  feeds: z.array(z.object({
    label: z.string(),
    tint: z.string().optional(),
  })).default([]),
  destApp: z.string().default('Destination'),
  destTitle: z.string().default(''),
  arcCaption: z.string().optional(),
  settleLine: z.string().optional(),
  rackRows: z.number().optional(),
  /** Optional: scale the content box to satisfy the canvas-fill law. 1 = unchanged. */
  fillScale: z.number().optional(),
});
export type ClaudeScienceSourceFlowProps = z.infer<typeof claudeScienceSourceFlowSchema>;

export const ClaudeScienceSourceFlow: React.FC<ClaudeScienceSourceFlowProps> = (props) => (
  <IlluStage spark={props.sparkLine}>
    <SourceFlow
      sourceLabel={props.sourceLabel}
      feeds={props.feeds}
      destApp={props.destApp}
      destTitle={props.destTitle}
      arcCaption={props.arcCaption}
      settleLine={props.settleLine}
      rackRows={props.rackRows}
    />
  </IlluStage>
);

// ── ClaudeScienceChipGrid ──────────────────────────────────────────────────
export const claudeScienceChipGridSchema = z.object({
  sparkLine: z.string().default('Options.'),
  items: z.array(z.string()).default([]),
  cols: z.number().optional(),
  caption: z.string().optional(),
  /** Optional: scale the content box to satisfy the canvas-fill law. 1 = unchanged. */
  fillScale: z.number().optional(),
});
export type ClaudeScienceChipGridProps = z.infer<typeof claudeScienceChipGridSchema>;

export const ClaudeScienceChipGrid: React.FC<ClaudeScienceChipGridProps> = (props) => (
  <IlluStage spark={props.sparkLine}>
    <ChipGrid items={props.items} cols={props.cols} caption={props.caption} fillScale={props.fillScale} />
  </IlluStage>
);
