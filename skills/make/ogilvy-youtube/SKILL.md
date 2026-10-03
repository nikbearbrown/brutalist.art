---
name: ogilvy-youtube
description: >-
  Write or improve YouTube titles, descriptions, hashtags, and keyword tags for
  finished Brutalist films. Use when preparing or revising a film's sibling
  YouTube `.md`, when `post` needs upload-ready metadata, or when the user asks
  for clearer, benefit-led, search-aware film copy. This skill writes metadata;
  it does not render, stage, upload, publish, or change factual claims.
---

# Ogilvy YouTube — earn the click, then repay it

Turn a finished film into clear, credible YouTube metadata. The copy should make
one useful promise, state what the viewer will understand or be able to do, and
then deliver enough evidence to deserve attention.

This is Ogilvy's clarity adapted to educational films—not an imitation of his
voice. Prefer specific nouns, active verbs, concrete stakes, and proof over
theatrical advertising language.

## Establish the brief

Read the film before writing. Use, in this order when present:

1. `beat_sheet.json` or the active beat sheet: title, cold open, question,
   terms, verdict, Your Turn, measured beat offsets, audience, and brand.
2. The transcript or `.srt`: what the film actually says.
3. `SOURCES.md`, `FACTCHECK.md`, and experiment records: what the copy may claim.
4. The relevant brand file under `brands/` and the source skill's `SKILL.md`.
5. The existing sibling `<slug>.md`: preserve useful chapters, links, credits,
   disclosures, and deliberate limits.

If the film lives in one of Bear's six active course repositories, read
[`references/course-positioning.md`](references/course-positioning.md). Use its
course-specific promise, audience outcome, proof pattern, vocabulary, and claim
boundaries when choosing the title and search terms. Do not reduce every course
to generic “AI education.”

Before drafting, be able to state privately:

- the film's single differentiator—why this treatment is worth watching instead
  of a generic explanation;
- the viewer outcome—what becomes clearer, easier, safer, or possible;
- the proof—the experiment, mechanism, demonstration, source, or worked example
  that earns the promise.

If the film does not support a differentiator, do not manufacture one. Use the
most concrete learning outcome supported by the film.

## Write the package

### Title

- Maximum 100 characters; aim for 45–70 when clarity survives.
- Name the subject in language a viewer would search for.
- Lead with the tension, result, or useful distinction—not the series name.
- Favor one promise. Do not splice two headlines with stacked punctuation.
- Use title case sparingly and naturally. No all-caps shouting, emoji, or empty
  adjectives such as “revolutionary,” “ultimate,” “powerful,” or “game-changing.”
- A question must be genuinely answered by the film. Never use a false question
  whose answer is merely “watch to find out.”
- Add a series suffix only when it helps recognition and the title remains clear.

Generate several candidates internally, then choose one. Output only the chosen
title unless the user asks for options.

### Description

The first 125 characters are the search/feed snippet. Make them a complete hook
with the primary topic and viewer payoff. Do not repeat the title word for word
and do not open with the brand name.

Use this order when the film supports it:

1. **Hook:** one or two sentences containing the primary search phrase naturally.
2. **Payoff:** what the film demonstrates, explains, tests, or helps the viewer do.
3. **Specifics:** mechanisms, examples, numbers, trade-offs, or limits that make
   this film distinct. Translate features into outcomes.
4. **Your Turn:** preserve the film's paste-ready prompt or concrete next action.
5. **Chapters:** for films longer than eight minutes, include measured timestamps;
   use them for shorter films when the beat structure materially helps navigation.
   The first timestamp must be `0:00` and every label must describe the section.
6. **Sources and links:** preserve verified URLs and descriptive labels. Never
   invent a source, endorsement, affiliation, playlist, or related-video URL.
7. **Credits and disclosure:** retain narrator, course, production, synthetic
   media, and “deliberately not claimed” language when applicable.
8. **Hashtags and keyword tags:** place them at the bottom.

Aim for 200–300 words before chapters, sources, and disclosures when the source
material can support that length. Short films may be shorter. Never pad thin
material to hit a count.

Markdown is the staging format, but the body must flatten cleanly to YouTube:
use simple headings, plain URLs, short paragraphs, and ordinary bullet lists.
Do not leave authoring notes, placeholders, HTML, tables, or Markdown title
headings in the uploaded description.

### Hashtags

- Use 3–5 relevant hashtags at the bottom.
- Include the subject, series or brand, and audience/category when useful.
- Prefer specific tags such as `#ClaudeCode` or `#GodotEngine` over generic
  reach bait such as `#Viral` or `#Trending`.
- Do not duplicate near-identical variants or make unsupported affiliation tags.

### YouTube keyword tags

- Provide 10–15 comma-separated phrases after a `SEO KEYWORD TAGS` label.
- Start with the exact primary topic, then add natural long-tail phrases,
  alternate terminology, series/course terms, and the creator or brand.
- Every phrase must describe content actually present in the film.
- Keep the combined YouTube tag payload within 500 characters.
- Tags support misspellings and topic classification; they are not a place to
  stuff unrelated popular terms.

## Editorial laws

- Clarity before cleverness. If a witty line hides the subject, cut it.
- Outcomes before features. Explain what a tool or method lets the viewer do.
- Credibility before hype. Use a number only when the film or source proves it.
- One claim at a time. Split sentences carrying multiple competing promises.
- Preserve uncertainty and boundaries. “Tested once,” “pending,” “AI-generated,”
  and “not legal advice” are meaningful facts, not copy problems to smooth over.
- Do not claim endorsement by Anthropic, Figma, Godot, YouTube, a university, or
  another organization unless the source material explicitly establishes it.
- Do not silently change the film's conclusion, audience, brand voice, or factual
  scope to make a stronger headline.

## Output contract

For a reel at `<reel>/` with slug `<slug>`, write or refresh `<slug>.md`:

```markdown
# [Chosen title]

[Hook and description body]

## Your Turn

[Concrete next action or paste-ready prompt]

## Chapters

0:00 [Specific section label]

## Sources and Credits

[Verified links, credits, disclosures, and limits]

#PrimaryTopic #SeriesOrBrand #Audience

## SEO Keyword Tags

[10–15 comma-separated phrases]
```

Omit a section only when the film provides no honest content for it. When
refreshing an existing file, retain verified operational material even if the
prose around it changes.

## Final check

Before handing off the file, verify:

- the title and first 125 characters say what the film is about;
- the description promises only what the film delivers;
- chapter timestamps come from measured offsets and increase monotonically;
- every URL, number, credit, and affiliation is supported;
- hashtags number 3–5 and keyword tags number 10–15;
- the keyword tag payload is at most 500 characters;
- no placeholder, duplicate title heading, hollow adjective, or invented link
  will reach YouTube.

Stop after writing and checking the metadata unless the user separately asks to
stage or publish the film.
