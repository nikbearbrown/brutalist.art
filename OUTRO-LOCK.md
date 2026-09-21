# OUTRO LOCK — @NikBearBrown outro card

*Locked spec for the claude-liam / @NikBearBrown outro card. Applies to claude-liam reels ONLY.
Same lock family as VOICE-LOCK.md. When any rule conflicts, this wins for the outro.*

## Scope
Only claude-liam / @NikBearBrown reels (slug `claude-liam-*`). Other channels — hai, medhavy,
musinique, youtubers, and non-Claude brands (brownblue / bears-doodles) — have their OWN outros
and NEVER get this card, handle, or mascot.

## The three locked elements
1. TITLE — exact restatement of the video's title. Never invent a tagline or subtitle. NO subline, ever.
2. HANDLE — `@NikBearBrown`, HARDCODED. Never derived from a persona / skin / channel variable.
   It is the one channel. (This is the bug that shipped `@Musinique` — the handle is a constant,
   not a lookup.)
3. MASCOT — ONE of the 18 blessed crisp-safe animations (mascot-anim-gallery-v2, ported to
   Remotion; translate / scale / flip only, NO rotation; canonical SVG at
   books/brutalist-art/svg/claude/svg/claude-mascot.svg). Small, UNDER the handle.

## Randomness — seeded, deterministic
Mascot (one of 18) and polarity (black-on-white / white-on-black) are picked at random SEEDED BY
THE REEL SLUG — stable per video, varied across videos. Never Math.random at render.

## Voice — the card is SPOKEN, never scored (locked 2026-09-18, Bear)
**No jingle. No music. No sound effect. Ever.** The stock `svg/claude/mp3/` jingles are retired
from every claude-liam outro; do not seed one, copy one, or "keep it quiet under the voice".
Liam (Kokoro `am_onyx`, per VOICE-LOCK.md) re-reads the exact title, then the handle, spoken:

    narration_text = "<exact title>. At Nik Bear Brown."

The beat clock is that narration plus a 1.0 s tail hold on the card (silence, not music), so
the card never cuts on the last syllable. `kind: "outro_voice"`. Any beat sheet still carrying
`kind: "outro_jingle"`, `jingle_source`, or `audio/outro-jingle.mp3` is out of lock and must be
rebuilt before staging.

## No double-branding
One handle per beat. The cold-open composer already shows the Claude box; do not add a second
@NikBearBrown there. The handle belongs on the outro card.
