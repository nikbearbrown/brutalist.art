# TIMING.md — the phase map

## The move

**The mark arrives nearly invisible and stays that way for half the runtime.**

Not: parts fly in at full strength and then something gets decorated. That is a
different, much cheaper animation, and it is the first thing you will build if
you only skim a contact sheet. The logo enters as an **emboss** — pressed into
the page, readable only as a shadow edge and a highlight edge — holds there, and
then **materialises** over one slow continuous ramp.

| # | phase | p | what is happening |
|---|---|---|---|
| 1 | BUILD | 0.03–0.16 | **camera pull-back** — opens on an extreme close-up of the letterform, oversized and tilted ~19°, zooming out and unrotating to front-on. Parts stagger in underneath, but the camera is the visible move |
| 2 | GHOST HOLD | 0.16–0.44 | settled. Nearly invisible. Nothing changes. |
| 3 | MATERIALISE | 0.44–0.83 | one slow ramp, emboss → full ink |
| 4 | LOCK | 0.83–1.00 | static |

## Measured, not invented

Contrast in the mark region (std-dev of luma) across the reference sting
(`logo animation.mov`, 7.01 s):

```
p 0.03-0.16   sd  2.9      fragments converge
p 0.16-0.43   sd  2.6      <- the ghost FLOOR. half a second either side of it, nothing.
p 0.43        sd  3.4      first hint
p 0.53        sd  5.2
p 0.57        sd  9.7
p 0.62        sd 15.2
p 0.67        sd 19.8
p 0.74        sd 24.5
p 0.80        sd 28.4      95% materialised
p 0.86        sd 29.5      plateau
```

Crossings: **5% at p=0.36, 50% at p=0.64, 95% at p=0.80.**

The ramp is slow at both ends — it creeps out of the floor and eases into the
plateau. `smoothstep` over `[ghost, materialise]` tracks it to a mean absolute
error of **0.040** across the whole window, verified against a rebuild.

## Why the ghost hold is the whole effect

Forty-four percent of the runtime spent nearly invisible is not dead air being
tolerated — it is the mechanism. The materialisation only reads as an arrival
because there was nothing to arrive from. Shorten the ghost and you do not get a
snappier sting, you get a fade-in.

The same logic as a hold before an accent, one level up: the pause is not the gap
between the events, it is what makes the event an event.

## The build is a CAMERA move AND a part assembly. Both.

The reference opens on an **extreme close-up**: the mark at ~6.5x scale, rotated
about -19 degrees, offset, filling and overflowing the frame, then pulls back to
the settled lockup. Clipped by the frame, the first few hundred milliseconds read
as an abstract geometric plate sliding through — which is the whole appeal.

Ease it (`1-(1-t)^2.4`): the big move is over early and the tail is a crawl, so
it lands rather than stops. Exponent 4 — the first value here — put the camera
82% home by a third of the window, and the back half of the build became a static
frame with details appearing on it. Keep it drifting to the end.

**But the camera is not the whole build, and this is the thing this skill got
wrong for two cuts.** Read the reference frame by frame, 0.00–1.33 s of 7.01 s:

```
frame 1     ONE fragment on the page, already mid-slide.
            Not a whole mark at low opacity — one part.
0.1-0.9 s   parts SLIDE IN from off-frame along long straight paths.
            Mass first: the letterform is standing before the small
            detail parts arrive.
1.3 s       parts are STILL arriving as the camera finishes.
in flight   each part sits HIGH off the page — a long, soft cast shadow
            trailing back along its flight path. On landing the shadow
            tightens to the resting emboss depth.
```

The first version of this scene faded every part up in place at a shared opacity
and let the camera do all the work. The client's words were *"it's just
appearing."* They were right, and "stagger the opacity a bit" is not the fix —
**a part that does not travel has not been assembled**, and a ghost that does not
cast has no height to fall from.

Two numbers make the flight legible at ±9 LSB of contrast:

1. **The cast shadow.** The part itself barely differs from the page. Its shadow,
   thrown far and soft while it is in the air, is the only thing the eye can
   actually track. One light, upper-left, fixed; what changes is height.
2. **Travel distance scaled by the inverse of the camera scale.** At 6.5x, an
   offset measured in mark-widths parks every part several frame-widths away and
   they all pop in at the end of their travel, bunched — a fade with extra steps.
   Divide by `camScale` and a part crosses a constant fraction of the SCREEN.

### The LETTER must form, not arrive

Watch the reference's letterform alone, cropped and stretched:

```
0.20 s   the LEFT STEM only — a bar with a hook. No other part of the M exists.
0.30 s   left stem + FIRST DIAGONAL: a partial, unreadable letter
0.40 s   second diagonal arrives, the V closes
0.50-0.60 s   the RIGHT STEM lands and the M becomes an M
```

The letter is built **stroke by stroke**, and until 0.5 s it is not yet a letter.
A letterform that slides in already finished is the same defect as a lockup that
slides in already finished, one level down — and it is the one you will still see
after fixing everything else, because the mark *is* the letter.

Most traces give you the letterform as ONE connected component, so it cannot be
staggered: `trace_logo.py` separates parts by connectivity and a bold M is one
blob. **Do not fix this in the trace.** Splitting a glyph into strokes with a
threshold is fragile and produces different fragments on every re-trace.

Cut it at render time instead: `assembly.slices` clips the hero part into N
vertical bands and flies each one in separately. On a bold geometric M, 4 bands
land almost exactly on the real strokes — left stem, left diagonal, right
diagonal, right stem — because that is how such an M is drawn. The bands run
left-to-right over `sliceStagger` (0.30 of the build ≈ 0.15 s apart at 1.5 s),
which reproduces the reference sequence above.

Two rules for slices, both learned the hard way:

- **A slice must not rotate.** Two bands at different angles do not meet along
  their shared edge and the seam shows for the whole flight.
- **Slices come in SIDEWAYS**, each from the side of the letter it belongs to, so
  the letter closes horizontally. Give them the part's radial vector instead and
  all four travel the same direction — they arrive in convoy and the letter is
  never seen being built.

Adjacent bands share an edge exactly, so the reassembled letter is seamless the
instant they are all home; the two outer bands run to infinity outward so the
emboss and cast copies are not shaved off at the letter's edges.

### Landing order: mass first, detail last

Sort by role, then radius, then log-area — big structural parts land early, small
ones trickle in. The mark is legible early and keeps accruing. Radius alone gets
it backwards whenever a big stroke sits far out; area alone scatters the read.

Give early parts a **longer** slide than late ones (`span = base + (1-key)·stagger·0.55`).
The hero part's travel is the only one the eye tracks; a uniform window put the
Medhavy M in place inside 8 frames and left the camera carrying the rest.

## Length is a prop — verified, not asserted

Every number in this file is a fraction of total runtime, which means shortening
a cut is editing `durationInSeconds` and nothing else. Medhavy went 11.700 s ->
9.400 s with the phase block untouched:

```
buildStart 0.0   build 0.128205   ghost 0.263248   materialise 0.496581
```

and the materialisation crossings came out **50% p=0.383, 95% p=0.450** against
the long cut's 0.379 / 0.464. Same curve, shorter clock.

Measure it after you shorten. If the crossings move, some phase got typed in
seconds instead of fractions, and the whole point of the parametric map is gone.

The one number that does move is the voice offset, because runtime is an output:
transition + speech + tail. Shortening the transition moves the line earlier by
the same amount; it does not shorten the line.

What does NOT scale gracefully is going very short. Below ~8 s the pieces start
to fight: the ghost hold has to hold long enough to be a hold (~1.2 s is about
the floor before it reads as a hesitation rather than a phase), the materialise
ramp is the effect and wants ~2 s, and the copy takes as long as it takes.
9.4 s = 1.2 build + 1.3 hold + 2.2 ramp + 0.5 resolved + 3.6 speech + 0.6 tail
is close to the floor for a narrated one-liner.

## Colour: the mark's ink is not the type's ink

`markInk` colours the mark; `ink` colours the wordmark and the tagline. Two
props because they are two decisions, and conflating them breaks the tagline:

```
markInk #0072B2 on page #F0EAD6   4.3:1   large graphic, fine
ink     #000000 on page #F0EAD6  18.6:1   6px small caps, necessary
accent  #D55E00                           the rule — Okabe-Ito's blue complement
```

3:1 is the bar for a large graphic and 4.5:1 for text, so a brand hue that is
comfortable on the mark is usually disqualifying on the tagline. There is no
version of this where the small caps get to be chromatic.

A chromatic mark makes the **ghost phase better**, which is not obvious. Black
ink at 95.5% page is a neutral grey smudge; blue ink at 95.5% page keeps a faint
cool cast, so the emboss reads as ink pressed into warm paper rather than as a
dirty mark. The measured amplitude barely moves (+24/-26 LSB in blue against
+22/-32 in black) — the *quality* of the read changes, not the contrast.

## Defaults

```
buildStart 0.00   build 0.157   ghost 0.44   materialise 0.83
colour     page #F0EAD6   markInk = the brand hue   ink #000000   accent = one
camera     scale 6.5   rotate -19   x 0.16   y 0.12
assembly   spread 1.35   drift 0.42   driftAngle -42   swirl 13
           stagger 0.66   lift 9   blur 16
           slices 4   sliceRole letter   sliceStagger 0.30
```

Fractions of total runtime, so they hold at any length.

`buildStart` is **0**, not 0.03. The reference has ink on the page at frame 1;
holding a flat page first spends the frames where the sting is most exposed.
Widen `build` when the mark has many parts — 42 arrivals want ~1.5 s.

`drift` mixes each part's own radial vector with one shared direction. All-radial
reads as an explosion played backwards; all-drift reads as one sheet sliding.

## Text after the voice, not with the mark

`textPhases` is separate from `phases` on purpose. For a narrated sting the
useful order is: **logo resolves -> voice starts -> supporting type arrives under
the line.** The rule and the tagline are not part of the transition, and folding
them into it wastes the one moment the mark has the frame to itself.

## When there is narration

**The transition wins, and the voice waits for it.** This is the one place in the
toolkit where audio does not set the shape. A sting reproduces a known motion;
re-timing the materialisation to land on a word breaks the curve that makes it
work. Run the transition to completion, then start the voice.

That makes total runtime an OUTPUT: transition + (silence-trimmed) narration +
tail. Do not pick a round number first and then discover the line does not fit.

**Check the supplied track for leading silence before offsetting it.** Medhavy's
carried 0.88 s. Delaying it by 7.00 s would have put the first word at 7.88 s and
left a dead beat exactly where the sting is most exposed.

**And check that it says the brand's name.** The G2P reads spelling, so every
invented name comes out wrong: "Medhavy" synthesized as /mˈɛdhævi/, *med-HAV-ee*,
rhyming with *savvy*, for three cuts. Force it with `metadata.pronounce`
(`{"Medhavy": "mɛdˈhɑːviː"}`) and verify with the ASR — you cannot hear the file,
but the recognizer's spelling tells you what it sounds like. Punctuation is
direction too: a comma where the line wants a full stop leaves a 0.38 s hole that
reads as the synthesizer losing its place.

Worked example — Medhavy, 9.400 s (the shipped shape):

```
0.00-1.21    BUILD          camera pull-back + 42 arrivals; the M forms
1.21-2.47    GHOST HOLD
2.47-4.67    MATERIALISE
4.67-5.20    FULL COLOUR    the mark alone, resolved, holding
5.23-8.84    VOICE          "Medhavy AI. An AI-powered intelligent learning system."
  6.35-6.79    rule, in the pause after "AI."
  6.79-7.31    tagline fades up, under "AI-powered"
8.84-9.40    HOLD / OUT     fade from 9.16
```

Worked example — Medhavy, 11.500 s (the same fractions, longer clock):

```
0.00-1.10    BUILD          camera pull-back
1.10-3.08    GHOST HOLD
3.08-5.81    MATERIALISE
5.81-7.00    FULL COLOUR    the mark alone, resolved, holding
7.00-10.28   VOICE          "Medhavy AI, an AI-powered intelligent learning system."
  8.45-9.10    tagline fades up, under "AI-powered"
10.28-11.50  HOLD / OUT
```

## Diagnosing a sting that "looks cheap"

Check in this order:

1. **Does the mark arrive at full strength?** If yes, that is the bug. There is
   no ghost phase and nothing can materialise.
2. **Is there a chrome/gloss/bevel sweep?** A hard-edged metallic gradient
   crossing a flat mark is the single clearest tell of a stock template — and it
   renders the brand colour *wrong* for the whole time it passes.
3. **Does colour arrive during motion?** Then it reads as part of the motion
   rather than as an event.
4. **Do the PARTS travel, or does the camera carry the whole open?** Put the
   first 45 frames in a grid and look at one part across them. If it is in its
   final position in every frame, the mark is not being assembled — it is being
   flown past. This is the defect that survives all three checks above and still
   reads as "it just appears".
5. **Is the first frame empty?** A flat page for a third of a second is a dead
   beat at the most exposed moment in the piece.
6. **Does the LETTER form, or does it arrive finished?** The last one to survive,
   and the hardest to unsee once noticed: the parts can all be travelling
   correctly while the letterform itself slides in whole. Set `assembly.slices`.
7. **Does it say the brand's name correctly, and can you hear it?** Not a motion
   defect, but it is the one thing a viewer will actually remark on. Check the
   pronunciation with the ASR and check the master's audio bitrate — 12.9 kbps at
   24 kHz shipped once, and it made a correct performance sound cheap.

The Medhavy sting this skill was first used to fix had all three: it popped the
full lockup in 0.27 s, held, then swept a silver gradient across a black mark
from 2.80–4.00 s — turning the brand mark grey for 20% of the runtime.
