---
name: logo-motion
description: >
  Build a logo sting — the 4–8 second animated brand mark that opens or closes a
  reel. ONE parametric Remotion composition (`LogoMotion`) drives every mark: the
  logo, the wordmark, the tagline, the palette and the LENGTH are all props, so a
  new brand is a traced part-list plus a props block, never a copied scene file.
  Use when the user types `logo motion`, `logo sting`, `logo animation`,
  `animate my logo`, `brand intro`, `intro animation`, `outro sting`, or hands
  over a logo (PNG/SVG) and asks to make it move — and when a reel needs a
  branded open/close. Also the right skill when an existing sting is being FIXED
  ("the transition looks wrong/cheap"): the phase map below is the diagnosis
  tool. Requires a mark that can be traced (dark ink on a light ground). Unlike
  every other skill here, the TRANSITION CURVE sets the timing and narration is
  laid over it — a sting is a fixed-length slot, not an audio-driven beat. The
  build is a camera pull-back AND a staggered part assembly; when an open reads
  as "it just appears", the parts are not travelling.
  Register: Teardown. Never publishes.
---

# logo-motion — one composition, every mark

## The problem this exists to stop

Before this skill, `runtime/remotion/src/` held **eight** logo showcase files —
`BearBrownLogoRemotionShowcase{,16x9}`, `BearBrownInitialsShowcase{,169}`,
`HLogoRemotionShowcase{,169}`, `Musiniqu*` ×3, `HaiWordmarkShowcase{,16x9}` — at
40–75 KB each. Every one is the same architecture copy-pasted: an inlined
`LOGO_PATH` const, a hand-written timing JSON, and a 20-plus-beat catalog of
motion techniques. The vocabulary is genuinely good. It was just never once
written down, and adding a ninth brand meant copying 50 KB.

**A new mark must not add a scene file.** It adds:

1. `runtime/remotion/src/logos/<name>.ts` — generated, never hand-edited
2. one line in the `LOGOS` registry in `scenes/LogoMotion.tsx`
3. a props block in the reel's `beat_sheet.json`

If you find yourself copying `LogoMotion.tsx`, stop — the thing you want is a
prop that does not exist yet. Add the prop.

## Inputs

| Input | Required | Notes |
|---|---|---|
| **logo** | yes | Raster, dark ink on a light ground. Any size — everything downstream is vector. |
| **wordmark** | no | String. Live text, not traced. |
| **tagline** | no | String. |
| **page / ink / accent** | no | Hex. Defaults are Medhavy's. |
| **narration** | no | **A STRING.** Kokoro synthesises it — free, local, no keys. |
| **voice** | no | `am_onyx` (Onyx) or `af_bella` (Bella). Those two, nothing else. |
| **audio file** | no | Only when the client supplies a recording you must keep. |
| **length** | no | An output when narrated: transition + speech + tail. |

**Narration is text by default.** Put the line in the beat's `narration_text`
and run `runtime/scripts/generate_audio_kokoro.py <REEL>` — it writes
`mp3/beat-B00.mp3` and `mp3/timings.json`, and the measured duration is ground
truth for everything downstream. Reach for a supplied mp3 ONLY when the voice
must be a specific human's, or when re-synthesising would change a track the
client has already signed off. Medhavy is the second case and is therefore the
exception, not the pattern.

## Flow

### Step 1 — get the mark as parts

A sting needs the logo **broken into pieces**. One flat path can only fade or
scale. Separate parts converge and stagger — that is the difference between a
logo that appears and a logo that is built.

```bash
python3 skills/make/logo-motion/scripts/trace_logo.py mark.png --name acme \
  --out runtime/remotion/src/logos/acme.ts
```

Input is any raster with dark ink on a light ground — a PNG export, or a frame
lifted out of an existing sting with `ffmpeg`. It need not be large; everything
downstream is vector. The script crops to the ink, upsamples 4×, labels
8-connected components, traces each one separately with `potrace`, and records
for every part its centroid, its angle from centre, and its normalised radius.
Those three numbers are what the scene staggers on.

Then add the key to `LOGOS` in `scenes/LogoMotion.tsx`. That is the whole
integration.

**Check the trace by looking at it.** Render the parts to a flat SVG and open it
before animating anything — a bad threshold silently drops hairlines, and at
ghost opacity you will never catch it in the render.

```bash
python3 skills/make/logo-motion/scripts/parts_to_svg.py \
  runtime/remotion/src/logos/acme.ts -o <reel>/acme.svg --color '#0072B2'
```

That writes a clean, role-grouped SVG from the same part list the scene animates
— `<g id="letter">`, `<g id="book">`, `<g id="circuit">`, every path carrying its
`data-rad`/`data-ang`. It is the artefact you look at, the one you hand a
designer, and the one you diff a re-trace against. It is generated, never a
second source of truth: if the SVG looks wrong, the trace is wrong.

Look at it **at thumbnail size too**. A mark that dissolves at 150 px will
dissolve in the ghost phase.

`--color` sets the root `color` attribute, which every path inherits through
`fill="currentColor"`. Recolouring the mark is one attribute in one place — if
you ever find yourself editing 42 `fill=` values, stop, because the SVG you are
editing is generated and your edit will not survive the next re-trace.

### Step 2 — measure the lockup, do not eyeball it

If you are matching an existing sting, take the ink bounding boxes off a settled
frame and put them in the scene as fractions. Measured, the Medhavy rebuild lands
within a pixel on the mark, the rule and the tagline. Eyeballed, the first cut had
the wordmark 24 px low and the tagline 56 px high, and neither was visible at
thumbnail size.

Position type by **cap-top**, not by box top. A CSS box top is not where the
letters start; at `line-height: 1` Montserrat's cap top sits `0.115em` below it.
That constant is in the scene.

### Step 3 — set the phase map, then lay the audio over it

The transition curve is the timing. If the sting is narrated, get word times so
you know what lands where — not to bend the curve to them:

```bash
python3 -c "from faster_whisper import WhisperModel as M; m=M('base.en',device='cpu',compute_type='int8'); s,_=m.transcribe('audio.wav',word_timestamps=True); [print(f'{w.start:5.2f}-{w.end:5.2f} {w.word}') for x in s for w in x.words]"
```

Note the word times — but do **not** re-time the transition to them. See
[reference/TIMING.md](reference/TIMING.md): the materialisation curve is the
thing that makes a sting work, and bending it to land on a word breaks it. Lay
the narration over the sting and let the picture finish after the line, which is
what the reference does.

### Step 3c — colour, and the fact that length is free

**The mark's ink and the type's ink are two decisions, not one.** `ink` drives
the wordmark AND the small-caps tagline; `markInk` (optional, defaults to `ink`)
drives the mark alone. Colour the mark by setting `markInk`. Setting `ink`
instead takes the tagline with it, and a brand hue that clears 3:1 as a large
graphic will be the one unreadable element in the piece at 6 px in caps.

Medhavy in Okabe-Ito blue is the worked example: `markInk #0072B2` on `page
#F0EAD6` is 4.3:1 — fine for the mark, nowhere near enough for type, so `ink`
stays `#000000` and `accent` takes vermillion `#D55E00`. Three colours, one job
each. House palettes live in `runtime/remotion/src/tokens/`; take the values from
there rather than typing a near-miss of the ground colour.

A chromatic mark also *improves* the ghost phase. A black emboss on cream is a
grey smudge; a blue one keeps a faint cool cast and reads as ink pressed into
warm paper.

**Changing the length is changing one number.** Every phase is a fraction of
runtime, so `durationInSeconds` 11.7 → 9.4 needs no re-timing at all — the
fractions stay byte-identical and the whole transition scales. The only other
number that moves is the voice offset, because runtime is an output: transition +
speech + tail.

Prove it rather than trusting it. The Medhavy shorten kept the same fractions and
the materialisation crossings came out 50% p=0.383 / 95% p=0.450 against the long
cut's 0.379 / 0.464 — same curve, shorter clock. If your crossings move, a phase
got typed in seconds somewhere.

### Step 3d — the voice: say the name right, then make it audible

Three things go wrong with a narrated sting's audio, and only one of them is the
performance.

**1. The brand name.** Espeak's G2P reads spelling, so it will mispronounce every
invented name you give it. "Medhavy" came out `mˈɛdhævi` — *med-HAV-ee*, rhyming
with *savvy*, when the name is *meh-DHAA-vee*. A sting that mispronounces the
brand it is announcing has failed at the only job it has. Fix it with a lexicon
in the beat sheet:

```json
"metadata": {"pronounce": {"Medhavy": "mɛdˈhɑːviː"}}
```

Get the starting IPA from `generate_audio_kokoro.py --phonemize "<line>"`, then
edit the one word. The script phonemizes the line, substitutes the listed words,
and synthesizes the whole thing as phonemes.

**Check it with the ASR, because you cannot hear it.** Transcribe each candidate:
the recognizer's spelling is a readout of what the audio actually sounds like.
`mɛdˈɑːviː` transcribed as *Medavi* (aspiration gone); `mˈeɪdhɑːviː` as
*Made-Havi* (the hyphen is the ASR reporting an audible break); `mɛdˈhɑːviː` as
*Medhavi*. Those are the two failure modes — under-aspirate and it loses a
consonant, over-separate and it becomes two words.

**2. The level and the bitrate.** Kokoro's raw output is around −27 LUFS with a
16 dB crest factor, and it is easy to then bury it in a low-bitrate mux. The
Medhavy master shipped one cut at **12.9 kbps AAC / 24 kHz**, which is most of
why the voice sounded thin — no amount of re-generating would have fixed it.
Shape, normalise, and mux properly (full chain in that reel's `NARRATION.md`):

```
highpass 70 · +1.5 dB @ 180 Hz · +2.2 dB @ 2.9 kHz · 3:1 comp from -24 dB
two-pass loudnorm, linear=true, I=-16 TP=-1.5      # linear: a 4s clip is too
                                                   # short for dynamic mode
mux: -c:a aac -b:a 160k -ar 48000 -ac 1
```

**3. Punctuation is direction.** "Medhavy AI**,** an…" left a 0.38 s hole that
reads as the synthesizer losing its place. "Medhavy AI**.** An…" makes the same
silence a 0.16 s beat. Set `speed` per beat too — 1.0 reads brisk, ~0.94 suits a
brand line, and past ~0.85 Kokoro smears the vowels. Try the other house voice
and measure: `af_bella` put a pause *inside* "Medhavy AI", so Onyx stayed.

### Step 4 — render, then LOOK

```bash
python3 runtime/scripts/remotion_scenes.py <REEL> --only B00 --force
```

Never trust the probe. Pull a contact sheet and read it. The defects that matter
in a sting — a ghost phase that is too short, a mark that arrives at full
strength, a part that never converges, type 4 px off its baseline — are all
invisible to `ffprobe` and obvious in a frame grid. Contrast-stretch the ghost
frames or you will be reviewing a blank page.

### Step 3b — check the build, not just the phase map

The phase map can be perfect and the open still read as *"it just appears"*. The
phases say *when* the mark is a ghost; they say nothing about what happens
**inside** the build, and that is where two Medhavy cuts went wrong.

Put the first ~45 frames in a grid, contrast-stretched, and follow **one part**
across them. It must **travel**. A camera pull-back over a rigid lockup is a
flypast, not an assembly. What the reference does, measured frame by frame:

| | |
|---|---|
| frame 1 | ONE fragment, already mid-slide — not a whole mark at low opacity |
| 0.1–1.3 s | parts slide in from off-frame, **mass first, detail last**, still arriving as the camera settles |
| in flight | each part sits high off the page: a long soft cast shadow trailing back along its path, tightening as it lands |
| the letter | **forms stroke by stroke** — left stem 0.20 s, first diagonal 0.30 s, second 0.40 s, right stem closes it 0.50–0.60 s |

That last row is its own failure mode and the one that survives longest. A trace
gives you a bold letterform as ONE connected component, so it can only slide in
finished — every other part can be moving correctly and the mark still reads as
delivered rather than built, because the mark *is* the letter. Do not fix it in
the trace; set `assembly.slices` and the scene cuts the hero part into N vertical
bands that fly in separately and reassemble seamlessly. On a geometric M, 4 bands
land on the real strokes.

`assembly` is the prop group that does this (`spread`, `drift`, `driftAngle`,
`swirl`, `stagger`, `lift`, `blur`, `slices`, `sliceRole`, `sliceStagger`).
Defaults are in
[reference/TIMING.md](reference/TIMING.md), along with why travel distance is
divided by the camera scale and why the landing order is mass-first.

The cast shadow is not decoration. At ±9 LSB the part itself is invisible; the
shadow it throws while airborne is the only thing the eye can track.

## Hard rules

- **The build is a camera move AND a part assembly.** Both, or neither works. The
  camera opens on an extreme close-up and pulls back; underneath it, parts travel
  in from off-frame on their own vectors, each casting a long soft shadow while
  it is still in the air. Parts that only fade up in place have not been
  assembled — that is a flypast over a finished logo, and it is the single defect
  that survives every other check on this list.
- **Runtime is transition + voice, in that order** — an output, not a round
  number picked up front. Trim leading silence off the supplied track before
  offsetting it, or the voice starts late by exactly that much.
- **Length is a prop, not a re-time.** `calculateMetadata` turns
  `durationInSeconds` into `durationInFrames`, and every ramp in the scene is a
  fraction of the total. A 4-second cut and a 9-second cut are the same animation
  at different speeds. Never fork the scene to change length.
- **Duration is an INPUT here — the one place in this toolkit where it is.**
  Everywhere else duration falls out of measured narration
  (see `skills/make/duration-planner/`). A sting is a fixed-length slot: a
  pre-roll is 5 seconds because the channel says 5 seconds. And when a sting *is*
  narrated the words still do not move the phases — the materialisation curve
  does. This is a deliberate exception to the audio-first law, not an oversight;
  see reference/TIMING.md.
- **The mark enters as a ghost.** Nearly invisible for the first ~44% of the
  runtime, then one slow materialisation. A mark that arrives at full strength
  has nothing to arrive *from*, and no amount of later colour work rescues it.
  This is the single easiest thing to get wrong from a contact sheet.
- **Colour the mark with `markInk`, never with `ink`.** `ink` also sets the
  small-caps tagline. A brand hue that clears 3:1 as a large graphic is not
  readable as 6 px type, so the two must move independently — and if the answer
  is "the tagline looks fine to me", you are looking at it at 4K, not at the size
  anyone will see it.
- **Say the name right.** The G2P reads spelling and will mispronounce every
  invented brand name. Force it with `metadata.pronounce`, and verify with the
  ASR rather than assuming — a sting that mispronounces the brand it announces
  has failed at its only job. Check the level and the mux bitrate in the same
  pass; a −27 LUFS bed at 12.9 kbps is not a performance problem and cannot be
  re-generated away.
- **The accent is earned.** One accent colour, arriving once, after a full stop.
  If the accent is present from frame one it is decoration and it is not doing
  any work.
- **Parts, not a picture.** If a mark is traced as a single component the
  assembly phase has nothing to stagger and the sting collapses into a fade. Fix
  the trace, not the animation.
- **No chrome, no gloss, no bevel.** A metallic sweep across a flat mark is the
  single most common way a sting reads as a stock template. It also destroys the
  logo's own colour while it passes. The replacement is the ghost→materialise
  ramp, which gets you the same "something is happening to the surface" read
  without ever showing the brand in the wrong colour.
- **Never publish.** Same as every skill here: the master stays in the reel folder.

## Where a sting lives

Same law as every reel — it travels with its book, at
`<book>/youtube/<slug>/`, never inside the toolkit. A one-beat reel folder is the
right shape: `beat_sheet.json` with a single `B00`, `mp3/B00.mp3`, a comment-only
`scenes.py`, and the master beside them.

## Reference

- [reference/TIMING.md](reference/TIMING.md) — the phase map AND the build
  anatomy, measured off two real stings, with the failure mode each prevents
- `scripts/trace_logo.py` — raster → animatable part list
- `scripts/parts_to_svg.py` — part list → clean role-grouped SVG to look at
- `scripts/measure_sting.py` — per-frame ink geometry and emboss amplitude off a
  rendered sting. High-passes each frame first: a reference plate's own grain or
  vignette will otherwise swamp a ±9 LSB mark and every number will be noise.
- `runtime/remotion/src/scenes/LogoMotion.tsx` — the composition
- Worked examples:
  - `youtube/medhavy-logo-sting-okabe/` (Medhavy AI, 9.400 s) — **the pattern**.
    The v2 build, recoloured to Okabe-Ito (`markInk` blue over black type),
    shortened by changing one number, and with the name's pronunciation forced
    and the bed mastered. `BUILD-LOG.md` has the ASR pronunciation table and the
    proof that shortening did not move the materialisation curve.
  - `youtube/medhavy-logo-sting-onyx-v2/` (11.700 s) — where the part assembly
    and the letterform slicing were worked out, plus `_qc/teardown.png`, the
    sheet that diagnoses a build
  - `youtube/medhavy-logo-sting-onyx/` (11.700 s) — same audio and text timing,
    build carried by the camera alone. Kept as the before-picture.
  - `youtube/medhavy-logo-sting/` (11.500 s) — the client's own recording reused
    verbatim; the supplied-mp3 exception

## Keep in sync

`nopunt`'s catalog has no row for a brand mark. When this skill changes, add or
update the row there — a beat that says "the logo animates in" is otherwise an
unfilled slate with no named tool.
