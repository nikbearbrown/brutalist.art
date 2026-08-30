import React, {useEffect, useState} from 'react';
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  interpolateColors,
  delayRender,
  continueRender,
  staticFile,
} from 'remotion';
import {z} from 'zod';
import {MEDHAVY_PARTS, MEDHAVY_VIEWBOX, MEDHAVY_TRANSFORM, LogoPart} from '../logos/medhavy';

/**
 * LogoMotion — a parametric logo sting. ONE composition, any mark.
 *
 * Everything a sting varies by is a prop: the logo (a registry key), the
 * wordmark, the tagline, the palette, and the LENGTH. Every ramp is a FRACTION
 * of the total, so a 5s cut and a 9s cut are the same animation at different
 * speeds — no re-timing by hand, no second composition.
 *
 * ── The move this scene exists to perform ────────────────────────────────────
 *
 * The mark does NOT arrive at full strength and then get decorated. It arrives
 * as a near-invisible EMBOSS — pressed into the page, readable only as a shadow
 * and a highlight — and stays that way for roughly the first half. Then it
 * MATERIALISES: one slow, continuous ramp from emboss to full ink.
 *
 * Measured off the reference sting (see reference/TIMING.md), contrast in the
 * mark region as std-dev of luma:
 *
 *     p=0.03..0.16  fragments converge, already ghost-faint   sd  2.9
 *     p=0.16..0.43  settled, still a ghost                    sd  2.6  <- floor
 *     p=0.43..0.48  the first hint                            sd  3.4
 *     p=0.57                                                  sd  9.7
 *     p=0.67                                                  sd 19.8
 *     p=0.80  95% materialised                                sd 28.4
 *     p=0.86  plateau                                         sd 29.5
 *
 * Half the runtime spent nearly invisible is the whole effect. An assembly that
 * lands at full ink and then changes one sub-element's colour is a DIFFERENT,
 * much cheaper animation — that was the first cut of this scene and it was
 * wrong. If you shorten the ghost phase, you lose the sting.
 *
 * ── What happens INSIDE the build ────────────────────────────────────────────
 *
 * The camera pull-back alone is not the build. Frame-by-frame off the reference
 * (0.00–1.33 s of 7.01 s):
 *
 *   frame 1   ONE fragment on the page. Not a whole mark at low opacity — one part.
 *   0.1–0.9s  parts SLIDE in from off-frame on long straight paths, big structural
 *             strokes first, small detail chips last, still arriving at 1.3 s
 *   in flight each part sits HIGH off the page: a long, soft cast shadow trailing
 *             back along its flight path. As it lands the shadow tightens to the
 *             resting emboss depth. That shadow is the only reason a slide is
 *             legible at ±9 LSB of contrast.
 *   light     fixed, upper-left, for every part, in flight and at rest.
 *
 * Before this, every part faded up in place at a shared opacity and the camera
 * did all the work — which is why the client read the open as "it just appears".
 * Parts that do not TRAVEL have not been assembled, and a ghost that does not
 * cast has no height to fall from.
 */

export const logoMotionSchema = z.object({
  logo: z.enum(['medhavy']).default('medhavy'),
  wordmark: z.string().default('Medhavy'),
  tagline: z.string().default('AI-POWERED INTELLIGENT LEARNING SYSTEMS'),
  durationInSeconds: z.number().default(7),
  page: z.string().default('#F1E9D6'),
  ink: z.string().default('#1E1E1E'),
  /**
   * The MARK's colour, when it is not the type's colour. A brand mark in the
   * brand hue over a near-black wordmark is the standard lockup, and it is one
   * decision, not two: the tagline is small caps and needs every point of
   * contrast it can get, so it must not be dragged along when the mark goes
   * chromatic. Defaults to `ink` — omit it and nothing changes.
   */
  markInk: z.string().optional(),
  accent: z.string().default('#009D70'),
  /** Fractions of the total. Ascending. Measured, not invented — see the header. */
  phases: z
    .object({
      /** camera starts pulling back */
      buildStart: z.number().default(0.03),
      /** camera has settled; the mark is front-on at final scale */
      build: z.number().default(0.157),
      /** the emboss holds, doing nothing, until here */
      ghost: z.number().default(0.44),
      /** full ink reached */
      materialise: z.number().default(0.83),
    })
    .default({buildStart: 0.03, build: 0.157, ghost: 0.44, materialise: 0.83}),
  /**
   * The rule and the tagline. Separate from `phases` because a sting with a
   * voice-over usually wants them AFTER the mark has resolved and the line has
   * started — not folded into the transition.
   */
  textPhases: z
    .object({
      ruleStart: z.number().default(0.44),
      ruleEnd: z.number().default(0.78),
      tagStart: z.number().default(0.50),
      tagEnd: z.number().default(0.87),
    })
    .default({ruleStart: 0.44, ruleEnd: 0.78, tagStart: 0.5, tagEnd: 0.87}),
  /**
   * The camera pull-back. The reference opens on an extreme close-up of the
   * letterform — oversized and tilted — and zooms out to the front-on lockup.
   * That move IS the geometric transition; without it the ghost just fades up.
   */
  camera: z
    .object({
      scale: z.number().default(6.5),
      rotate: z.number().default(-19),
      /** offset at full zoom, as a fraction of the mark's box */
      x: z.number().default(0.16),
      y: z.number().default(0.12),
    })
    .default({scale: 6.5, rotate: -19, x: 0.16, y: 0.12}),
  /**
   * The part assembly that runs UNDER the camera move. Each part travels in from
   * off-frame on its own vector, staggered, casting a long soft shadow while it
   * is still in the air. Without this the build is a fade and the camera is
   * carrying the whole open on its own.
   */
  assembly: z
    .object({
      /** how far out a part starts, as a multiple of the mark's half-diagonal */
      spread: z.number().default(1.35),
      /** how much of the spread is a shared drift rather than each part's own
       *  radial vector. All-radial reads as an explosion played backwards. */
      drift: z.number().default(0.42),
      /** direction the drifting parts come FROM, degrees, screen space (y down) */
      driftAngle: z.number().default(-42),
      /** degrees of tumble a part carries in about its own centroid */
      swirl: z.number().default(13),
      /** fraction of the build window spent staggering starts, 0 = all together */
      stagger: z.number().default(0.66),
      /** cast-shadow offset in flight, as a multiple of the resting emboss depth */
      lift: z.number().default(9),
      /** cast-shadow blur at full lift, in viewBox units */
      blur: z.number().default(16),
      /**
       * Cut the hero part into this many vertical bands and fly each in
       * separately, so the LETTER FORMS instead of arriving finished. 0 = off.
       * On a bold geometric M, 4 bands land on the natural strokes: left stem,
       * left diagonal, right diagonal, right stem — which is exactly the
       * sequence the reference builds in (0.20 s left stem, 0.30 s first
       * diagonal, 0.40 s second, 0.50–0.60 s right stem closes it).
       */
      slices: z.number().default(4),
      /** which role gets sliced — the letterform, normally */
      sliceRole: z.string().default('letter'),
      /** share of the build the slice sequence itself occupies */
      sliceStagger: z.number().default(0.30),
    })
    .default({
      spread: 1.35, drift: 0.42, driftAngle: -42, swirl: 13,
      stagger: 0.66, lift: 9, blur: 16,
      slices: 4, sliceRole: 'letter', sliceStagger: 0.3,
    }),
  /** Depth of the emboss at full ghost, as a fraction of the mark's height. */
  embossDepth: z.number().default(0.006),
  fadeOut: z.boolean().default(true),
});
export type LogoMotionProps = z.infer<typeof logoMotionSchema>;

const LOGOS: Record<string, {parts: LogoPart[]; viewBox: string; transform: string}> = {
  medhavy: {parts: MEDHAVY_PARTS, viewBox: MEDHAVY_VIEWBOX, transform: MEDHAVY_TRANSFORM},
};

const SANS = 'Montserrat, -apple-system, "Segoe UI", "Helvetica Neue", sans-serif';

// Montserrat is bundled in runtime/fonts but nothing in this project ever loaded
// it — tokens/vox.ts says as much ("fall back to system faces until the bundled
// Montserrat ... "), so every scene naming it has silently been rendering in the
// system sans. Loaded here per-component (NOT at module scope): Root.tsx imports
// 600+ compositions, and a module-scope delayRender would block every one of them
// on a font only this scene uses.
const FONT_FILES: [number, string][] = [
  [700, 'fonts/Montserrat-Bold.ttf'],
  [500, 'fonts/Montserrat-Medium.ttf'],
];

const useMontserrat = () => {
  const [handle] = useState(() => delayRender('LogoMotion: Montserrat'));
  useEffect(() => {
    let live = true;
    Promise.all(
      FONT_FILES.map(([weight, file]) =>
        new FontFace('Montserrat', `url(${staticFile(file)}) format('truetype')`, {
          weight: String(weight),
        })
          .load()
          .then((f) => {
            // This project's TS lib predates FontFaceSet.add in lib.dom; the API
            // is present in every browser Remotion renders in.
            (document.fonts as unknown as {add: (f: FontFace) => void}).add(f);
          }),
      ),
    )
      // Continue on failure too: a missing font should degrade to the system sans,
      // never hang the render at 100% forever.
      .catch(() => undefined)
      .then(() => {
        if (live) continueRender(handle);
      });
    return () => {
      live = false;
    };
  }, [handle]);
};

const clamp = (v: number, a: number, b: number) => Math.min(b, Math.max(a, v));
const ramp = (p: number, a: number, b: number) => clamp((p - a) / (b - a), 0, 1);
const easeOut = (t: number) => 1 - Math.pow(1 - t, 3);
// The materialisation is slow at both ends — it creeps out of the ghost floor and
// eases into the plateau. Smoothstep matches the measured curve to within a few
// percent across the whole window.
const smooth = (t: number) => t * t * (3 - 2 * t);

/** Mix a colour toward the page — how a ghost is made. */
const toward = (c: string, page: string, amount: number) =>
  interpolateColors(amount, [0, 1], [c, page]);

const RAD = Math.PI / 180;

/**
 * Bounding box of a potrace path, in PATH space. potrace emits exactly four
 * commands — M (absolute), c and l (both relative), z — so this walks those and
 * nothing else. Control points are included, which makes the box a hair generous;
 * it is used to place slice cuts, where a hair generous is free.
 */
const pathBox = (d: string) => {
  const tok = d.match(/[MmCcLlZz]|-?\d*\.?\d+/g);
  if (!tok) return null;
  let x = 0, y = 0, cmd = 'M';
  let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
  const see = (px: number, py: number) => {
    x0 = Math.min(x0, px); y0 = Math.min(y0, py);
    x1 = Math.max(x1, px); y1 = Math.max(y1, py);
  };
  for (let i = 0; i < tok.length; ) {
    const t = tok[i];
    if (/[A-Za-z]/.test(t)) {cmd = t; i++; continue;}
    const num = () => Number(tok[i++]);
    if (cmd === 'M' || cmd === 'L') {x = num(); y = num(); see(x, y);}
    else if (cmd === 'm' || cmd === 'l') {x += num(); y += num(); see(x, y);}
    else if (cmd === 'C') {
      for (let k = 0; k < 2; k++) see(num(), num());
      x = num(); y = num(); see(x, y);
    } else if (cmd === 'c') {
      for (let k = 0; k < 2; k++) see(x + num(), y + num());
      x += num(); y += num(); see(x, y);
    } else i++; // z, or anything unexpected: skip a token rather than spin
  }
  return x1 > x0 ? {x0, y0, x1, y1} : null;
};

/** Pull translate()/scale() out of the generator's transform string. */
const parseXform = (t: string) => {
  const tr = /translate\(\s*(-?[\d.]+)\s*[, ]\s*(-?[\d.]+)/.exec(t);
  const sc = /scale\(\s*(-?[\d.]+)\s*[, ]\s*(-?[\d.]+)/.exec(t);
  return {
    tx: tr ? Number(tr[1]) : 0, ty: tr ? Number(tr[2]) : 0,
    sx: sc ? Number(sc[1]) : 1, sy: sc ? Number(sc[2]) : 1,
  };
};

/**
 * Landing order. The reference lands MASS first and DETAIL last — the letterform
 * is standing before the small chips arrive, so the mark is legible early and
 * keeps accruing. Sorting by radius alone gets this backwards half the time,
 * because a big stroke can sit far out; sorting by area alone scatters the read.
 *
 * Returns each part's key in [0,1]: 0 lands first.
 */
const landingOrder = (parts: LogoPart[]): number[] => {
  const ROLE: Record<string, number> = {letter: 0, book: 0.18, circuit: 0.42};
  const areas = parts.map((q) => Math.log(Math.max(q.area, 1)));
  const aMin = Math.min(...areas);
  const aMax = Math.max(...areas);
  const raw = parts.map((q, i) => {
    // small parts late; log because a trace's areas span three decades
    const small = aMax > aMin ? 1 - (areas[i] - aMin) / (aMax - aMin) : 0;
    return (ROLE[q.role] ?? 0.42) + q.rad * 0.34 + small * 0.24;
  });
  const lo = Math.min(...raw);
  const hi = Math.max(...raw);
  return raw.map((v) => (hi > lo ? (v - lo) / (hi - lo) : 0));
};

export const LogoMotion: React.FC<LogoMotionProps> = ({
  logo,
  wordmark,
  tagline,
  page,
  ink,
  markInk,
  accent,
  phases,
  textPhases,
  camera,
  assembly,
  embossDepth,
  fadeOut,
}) => {
  useMontserrat();
  const frame = useCurrentFrame();
  const {durationInFrames, width, height} = useVideoConfig();
  const p = frame / durationInFrames;

  const {parts, viewBox, transform} = LOGOS[logo] ?? LOGOS.medhavy;
  const [, , vbW, vbH] = viewBox.split(' ').map(Number);
  const order = React.useMemo(() => landingOrder(parts), [parts]);

  // ── the three things that actually happen ──────────────────────────────────
  const pAssemble = ramp(p, phases.buildStart, phases.build);
  const mat = smooth(ramp(p, phases.ghost, phases.materialise));
  const pOut = fadeOut ? ramp(p, 0.975, 0.999) : 0;

  // The camera. easeOut — the big move is over early and the tail of the
  // pull-back is a crawl, which is what makes it land rather than stop. Exponent
  // 4 put it 82% home by a third of the window, so the back half of the build was
  // a static frame with chips appearing on it; 2.4 keeps it drifting to the end,
  // which is what the reference does.
  const cam = 1 - Math.pow(1 - pAssemble, 2.4);
  const camScale = interpolate(cam, [0, 1], [camera.scale, 1]);
  const camRot = interpolate(cam, [0, 1], [camera.rotate, 0]);
  const camDX = interpolate(cam, [0, 1], [camera.x * 100, 0]);
  const camDY = interpolate(cam, [0, 1], [camera.y * 100, 0]);

  // ── layout ─────────────────────────────────────────────────────────────────
  // MEASURED off the Medhavy lockup, not eyeballed. Ink bounding boxes at
  // 1920x1080, from a settled frame:
  //   mark      y 216-621 (h 406)   x 714-1204 (w 491)
  //   wordmark  y 669-755 (h  87)   x 764-1161 (w 398)   cap-top at y=669
  //   rule      y 794-797 (h   4)   x 672-1247 (w 576)
  //   tagline   y 845-865 (h  21)   x 507-1407 (w 901)   cap-top at y=845
  // The traced viewBox carries ~6px of padding per side, so markH is the INK
  // height grossed up by 418/406 and markY pulled up to match.
  const markH = height * 0.38704;
  const markW = markH * (vbW / vbH);
  const markX = (width - markW) / 2;
  const markY = height * 0.19444;

  // Type is positioned by CAP-TOP. A CSS box top is not where the letters start;
  // 0.115em below it is, for Montserrat at line-height 1. Measured, because the
  // nominal metrics predict 0.1585 and that put both cap tops 4px high.
  const CAP_INSET = 0.115;
  const wordSize = height * 0.08519;
  const wordY = height * 0.61944 - wordSize * CAP_INSET;
  const ruleY = height * 0.73519;
  const ruleH = Math.max(2, height * 0.0037);
  const ruleW = width * 0.3;
  const tagSize = height * 0.02778;
  const tagY = height * 0.78241 - tagSize * CAP_INSET;

  // ── the emboss ─────────────────────────────────────────────────────────────
  // A debossed mark is three copies: a dark edge pushed down-right, a light edge
  // pushed up-left, and a face barely off the page. As `mat` rises the offsets
  // collapse to zero and the face takes the real colour, so the emboss does not
  // "cross-fade out" — it resolves INTO the solid mark.
  const depth = vbH * embossDepth * (1 - mat);
  // The mark's ink and the type's ink are separate decisions; see `markInk`.
  const solid = markInk ?? ink;
  const ghostFace = toward(solid, page, 0.955);
  const ghostShadow = toward(solid, page, 0.80);
  const ghostHigh = '#FFFFFF';
  const edgeOpacity = (1 - mat) * 0.9;

  // The wordmark rides the mark's materialisation. The rule and the tagline do
  // NOT — they get their own late window, so a narrated sting can resolve the
  // logo first and bring the supporting type in under the voice.
  const matWord = smooth(ramp(p, phases.ghost + 0.04, phases.materialise + 0.02));
  const matRule = smooth(ramp(p, textPhases.ruleStart, textPhases.ruleEnd));
  const matTag = smooth(ramp(p, textPhases.tagStart, textPhases.tagEnd));

  // ── the flight ─────────────────────────────────────────────────────────────
  // Each part gets its own start offset, its own window inside the build, and a
  // cast shadow whose offset and softness track how far it still has to travel.
  const half = Math.hypot(vbW, vbH) / 2;
  const base = Math.max(1 - assembly.stagger, 0.12); // the LAST part's window
  const driftX = Math.cos(assembly.driftAngle * RAD);
  const driftY = Math.sin(assembly.driftAngle * RAD);
  const castColour = toward(solid, page, 0.86);
  // The first part is already moving at frame 0 — the reference has one fragment
  // on the page from the first frame, and an empty opening frame is a dead beat
  // in a 5-frame window nobody gets back.
  const PREROLL = 0.07;

  // Where the hero part sits in viewBox space, so its slice cuts can be placed.
  // The part list carries a centroid but not a box, and a centroid cannot tell
  // you where a stem ends.
  const heroBox = React.useMemo(() => {
    const hero = parts.find((q) => q.role === assembly.sliceRole);
    if (!hero || assembly.slices < 2) return null;
    const b = pathBox(hero.d);
    if (!b) return null;
    const {tx, ty, sx, sy} = parseXform(transform);
    const xs = [b.x0 * sx + tx, b.x1 * sx + tx];
    const ys = [b.y0 * sy + ty, b.y1 * sy + ty];
    return {
      id: hero.id,
      x0: Math.min(...xs), x1: Math.max(...xs),
      y0: Math.min(...ys), y1: Math.max(...ys),
    };
  }, [parts, transform, assembly.sliceRole, assembly.slices]);

  const flight = parts.flatMap((part, i) => {
    const sliced = heroBox !== null && heroBox.id === part.id;
    const n = sliced ? Math.round(assembly.slices) : 1;

    return Array.from({length: n}, (_, k) => {
      // ── the slice, if this is the hero part ────────────────────────────────
      // Bands are cut in viewBox space and each flies separately, so the LETTER
      // ASSEMBLES rather than arriving whole. Because adjacent bands share an
      // edge exactly, they are seamless the instant they are all home.
      let clip: {x: number; w: number; y: number; h: number} | null = null;
      let sub = 0; // 0..1 across the slice sequence, left to right
      if (sliced && heroBox) {
        const bw = (heroBox.x1 - heroBox.x0) / n;
        // The two OUTER bands run to infinity outward, so the emboss and cast
        // copies — which are offset a few units past the ink — are not shaved off
        // at the letter's left and right edges. Interior cuts stay exact, which
        // is what makes the reassembled letter seamless.
        const l = k === 0 ? heroBox.x0 - vbW : heroBox.x0 + k * bw;
        const r = k === n - 1 ? heroBox.x1 + vbW : heroBox.x0 + (k + 1) * bw;
        clip = {
          x: l, w: r - l,
          // generous vertically: the cut is horizontal only
          y: heroBox.y0 - vbH, h: (heroBox.y1 - heroBox.y0) + 2 * vbH,
        };
        sub = n > 1 ? k / (n - 1) : 0;
      }

      // A sliced part's bands run in sequence inside the part's own lane; an
      // unsliced part is one band with sub = 0 and nothing changes for it.
      const lane = order[i] * assembly.stagger - PREROLL + sub * assembly.sliceStagger;
      // Early parts get a LONGER slide than late ones — they have the room, and the
      // hero part's travel is the only one the eye actually tracks. A uniform window
      // put the mark in place inside 8 frames and left the camera to carry the rest.
      const span = base + (1 - order[i]) * assembly.stagger * 0.55;
      // easeOut so a part decelerates into its slot rather than stopping dead
      const t = easeOut(ramp(pAssemble, lane, lane + span));
      const away = 1 - t; // 1 = still out there, 0 = landed
      const rx = Math.cos(part.ang * RAD);
      const ry = Math.sin(part.ang * RAD);
      // mostly its own radial vector, partly a shared drift — pure radial reads as
      // an explosion in reverse, pure drift reads as one sheet sliding
      let ux = rx * (1 - assembly.drift) + driftX * assembly.drift;
      let uy = ry * (1 - assembly.drift) + driftY * assembly.drift;
      // Strokes come in SIDEWAYS, from the side of the letter they belong to, so
      // the letter closes up horizontally. A radial vector off the letterform's
      // centroid would send every band in the same direction — they would arrive
      // in convoy and the letter would never look like it was being built.
      if (sliced) {
        const sx = (sub - 0.5) * 2; // -1 leftmost band, +1 rightmost
        ux = sx * 0.94 + driftX * 0.2;
        uy = -0.3 + driftY * 0.2;
      }
      // Divided by the camera scale, so a part travels a constant fraction of the
      // SCREEN rather than of the mark. At 6.5x an un-divided offset would park
      // every part several frame-widths away and they would all pop in at the end
      // of their travel, bunched — which is a fade with extra steps.
      // The 0.7 floor matters: keying reach off radius alone gives the centre part
      // — which on most marks is the letterform, i.e. the hero — almost no travel.
      const reach =
        (half * assembly.spread * (sliced ? 0.62 : 0.7 + part.rad * 0.9)) / camScale;
      return {
      part,
      key: `${part.id}-${k}`,
      clip,
      // a part fades up over the first third of its OWN travel, not the build's,
      // so the frame is never empty and never gets a batch of parts at once
      opacity: clamp(t / 0.3, 0, 1),
      dx: ux * reach * away,
      dy: uy * reach * away,
      // A slice must not rotate: two bands at different angles do not meet along
      // their shared edge, and the seam shows for the whole flight.
      rot: sliced ? 0 : assembly.swirl * away * (part.cx < vbW / 2 ? -1 : 1),
      away,
      // trail: the shadow lags BACK along the flight path, and the light stays
      // upper-left, so a travelling part gets a long shadow and a landed one a
      // tight offset. Same light, different height.
      castX: depth * (1 + away * assembly.lift) + (ux * half * 0.09 * away) / camScale,
      castY: depth * (1 + away * assembly.lift) + (uy * half * 0.09 * away) / camScale,
      };
    });
  });
  const castBlur = assembly.blur * (0.35 + 0.65 * clamp(1 - pAssemble, 0, 1));
  const castOpacity = (1 - mat) * 0.55;

  return (
    <AbsoluteFill style={{background: page, overflow: 'hidden'}}>
      {/* The camera. Oversized and tilted at the open, pulling back to front-on.
          AbsoluteFill clips it, so the first frames are an extreme close-up of
          whatever part of the mark happens to be under the lens. */}
      <div
        style={{
          position: 'absolute',
          inset: 0,
          transform: `translate(${camDX}%, ${camDY}%) scale(${camScale}) rotate(${camRot}deg)`,
          transformOrigin: '50% 46%',
        }}
      >
      <svg
        width={markW}
        height={markH}
        viewBox={viewBox}
        style={{position: 'absolute', left: markX, top: markY}}
      >
        <defs>
          {/* One filter, applied ONCE to the whole shadow group. Per-path filters
              would be 42 separate raster passes a frame at 4K. */}
          <filter id="lm-cast" x="-70%" y="-70%" width="240%" height="240%"
            filterUnits="objectBoundingBox">
            <feGaussianBlur stdDeviation={castBlur} />
          </filter>
          {/* One rect per stroke band of the hero part. Adjacent bands share an
              edge exactly, so the letter is seamless once they are all home. */}
          {flight.map((f) =>
            f.clip ? (
              <clipPath key={f.key} id={`lm-clip-${f.key}`} clipPathUnits="userSpaceOnUse">
                <rect x={f.clip.x} y={f.clip.y} width={f.clip.w} height={f.clip.h} />
              </clipPath>
            ) : null,
          )}
        </defs>

        {/* The cast shadows. This layer is what makes a slide visible at ghost
            contrast: the part itself barely differs from the page, but the shadow
            it throws while it is still in the air does. */}
        {castOpacity > 0.005 && (
          <g filter="url(#lm-cast)" opacity={castOpacity}>
            {flight.map((f) => (
              <g key={f.key}
                transform={`translate(${f.dx + f.castX} ${f.dy + f.castY}) rotate(${f.rot} ${f.part.cx} ${f.part.cy})`}
                opacity={f.opacity}>
                <g clipPath={f.clip ? `url(#lm-clip-${f.key})` : undefined}>
                  <g transform={transform} stroke="none">
                    <path d={f.part.d} fill={castColour} />
                  </g>
                </g>
              </g>
            ))}
          </g>
        )}

        {/* The mark. Every part carries its own translate/rotate, so the assembly
            is a set of independent arrivals under one camera move. */}
        {flight.map((f) => {
          const face = interpolateColors(mat, [0, 1], [ghostFace, solid]);
          return (
            <g key={f.key} opacity={f.opacity}
              transform={`translate(${f.dx} ${f.dy}) rotate(${f.rot} ${f.part.cx} ${f.part.cy})`}>
              <g clipPath={f.clip ? `url(#lm-clip-${f.key})` : undefined}>
                <g transform={transform} stroke="none">
                  {depth > 0.01 && (
                    <>
                      <path d={f.part.d} fill={ghostHigh} opacity={edgeOpacity}
                        transform={`translate(${-depth * 10} ${depth * 10})`} />
                      <path d={f.part.d} fill={ghostShadow} opacity={edgeOpacity}
                        transform={`translate(${depth * 10} ${-depth * 10})`} />
                    </>
                  )}
                  <path d={f.part.d} fill={face} />
                </g>
              </g>
            </g>
          );
        })}
      </svg>

      {/* wordmark — embossed with the mark, resolves with it */}
      <div
        style={{
          position: 'absolute',
          top: wordY,
          left: 0,
          width,
          textAlign: 'center',
          lineHeight: 1,
          fontFamily: SANS,
          fontWeight: 700,
          fontSize: wordSize,
          // Montserrat sets ~9% wider than the reference face at matched cap
          // height; a touch of negative tracking closes it without cramping.
          letterSpacing: '-0.048em',
          textIndent: '0.048em', // cancel the trailing letter-space so it stays centred
          color: interpolateColors(matWord, [0, 1], [toward(ink, page, 0.955), ink]),
          textShadow:
            matWord < 1
              ? `${-depth * 0.06}px ${depth * 0.06}px 0 rgba(255,255,255,${edgeOpacity}), ` +
                `${depth * 0.06}px ${-depth * 0.06}px 0 ${toward(ink, page, 0.8)}`
              : 'none',
          opacity: easeOut(ramp(pAssemble, 0.45, 1)),
        }}
      >
        {wordmark}
      </div>

      {/* accent rule — the one place colour, not just contrast, arrives */}
      <div
        style={{
          position: 'absolute',
          top: ruleY,
          left: width / 2,
          width: interpolate(matRule, [0, 1], [0, ruleW]),
          height: ruleH,
          marginLeft: interpolate(matRule, [0, 1], [0, -ruleW / 2]),
          background: interpolateColors(matRule, [0, 1], [toward(accent, page, 0.9), accent]),
        }}
      />

      {/* tagline — last to resolve */}
      <div
        style={{
          position: 'absolute',
          top: tagY,
          left: 0,
          width,
          textAlign: 'center',
          lineHeight: 1,
          fontFamily: SANS,
          fontWeight: 500,
          fontSize: tagSize,
          letterSpacing: '0.143em',
          textIndent: '0.143em',
          color: interpolateColors(matTag, [0, 1], [toward(ink, page, 0.94), ink]),
          opacity: 0.82 * matTag,
        }}
      >
        {tagline}
      </div>
      </div>

      {pOut > 0 && <AbsoluteFill style={{background: '#000000', opacity: smooth(pOut)}} />}
    </AbsoluteFill>
  );
};
