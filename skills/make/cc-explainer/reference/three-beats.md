> **Retired 2026-09-08 (Bear): the SKEPTIC beat.** The four-moves section below is kept as doctrine only; no cc-explainer renders it. Skepticism lives in every VERIFY step and the verdict's falsifiable line. CONDUCT and HUMAN stand.

# The three closing-block beats — doctrine, distilled

Each CC video turns on its own session before the recap. Three beats, three
courses, one question each. This is the working doctrine; the chapter pointers
are where the beat author goes when a session raises something this page
doesn't cover.

---

## SKEPTIC — "Is it actually done?"

**Source:** `info-7375-computational-skepticism-for-ai/chapters/_expanded-four-moves.md`
(the four moves), `08-validating-agentic-ai-when-autonomous-systems-misbehave.md`
(why agents are different), `09-delegation-trust-and-the-supervisory-role.md`
(the handoff condition as a contract).

**The one sentence.** Claude's completion report is an *artifact*; whether
the thing is done is a fact about the *world*; the beat's job is to refuse to
let the first stand in for the second.

**Why agents are different (ch. 8).** Three things change when the system
acts instead of predicts. The loss is open-ended — bounded only by the
agent's effective scope, so *you cannot bound the failure cost without
bounding the access*. The audit trail is the artifact — the action has
happened, you cannot re-run it, and the agent's own report of what it did can
be wrong (the Ash case: "email deleted" reported, email still on the server).
And the failure modes are new: right about what it did, wrong about what it
should have done; acting on inputs it should not have; reporting completion
when the *local* state matched completion and the *effective* scope never
reached it. *Looks-fine-from-here is not a defense.*

**The four moves, as commands she runs:**

| Move | The tool | In the terminal |
|---|---|---|
| **Descartes — radical doubt** | *What would have to be true for this claim to be wrong?* Not a mood; a checklist. Enumerate the ways "done" could be false, then go look at each. (Knight Capital: the deploy "succeeded" on seven of eight servers.) | The second file. The test that exercises the path the diff touched. `git diff --stat` against what she expected to change. |
| **Hume — the limit of induction** | *Is this confidence about the world, or only about the record so far?* Every prior success adds zero guarantee to this one. (Taleb's turkey; Zillow Offers; Google Flu Trends.) | The input that differs from the ones Claude saw — the empty case, the unicode case, the file it never opened. |
| **Popper — falsifiability** | *State, in advance and in measurable terms, what failure looks like — then go looking for exactly that.* Confirmations are cheap; a system produces them all day. (The Epic Sepsis Model was never validated, only unrefuted.) | She names the failing input *before* she runs it. Then runs it. |
| **Plato — artifact vs world** | *What is the artifact? What is the world? What is the relationship?* The diff is a shadow; the running system is the wall. (COVID X-ray models keyed on hospital markers, not lungs.) | She runs it. `npm test`, the endpoint, the render. Never grades the diff as if it were the program. |

**What the beat must not do.** Describe verification. The moves are commands
or they are rhetoric that arrived in technical clothing. NO-SOURCE-NO-VERDICT:
each ✓/✗ points at output on screen.

**Ch. 9's contribution — the handoff condition.** The unit of trust is not
the partition (Claude does X, I do Y); it is the *contract*: what must be true
about Claude's output before the next step is allowed to begin. That is the
bridge into the CONDUCT beat.

---

## BUILD SHOWN — the precondition for the score (build films)

Added 2026-09-09 (Bear). On a film that builds something, CONDUCT is not the
first time the viewer sees the whole: two slots precede it — BFLOW (the flow
and whatever other diagram the build needs, drawn with the session's real
names) and BSHOW (the output, real and running). The Boondoggle Score then
scores work the viewer has just watched run, so "who did what" lands on a
concrete thing and the handoff conditions can be checked against the output on
screen. Contracts and surfaces are in `SKILL.md` (§ THE BUILD, SHOWN). Concept
films (the 101 tiers) do not arm it.

## CONDUCT — the Boondoggle Score

**Source:** `info-7375-conducting-ai/chapters/02-the-solve-verify-asymmetry.md`
(the claim the book rests on), `04–13` (the five capacities, two chapters
each), `15-the-plausibility-audit.md` (the adversarial auditor and the Gap
Account); the Gru consultant spec (pasted into the session that created this
skill; the Boondoggle Score format and prompt-writing principles are its
core).

**The one sentence.** Programming as conducting — Gru does not build the
rocket; Gru designs the mission, assigns the minions, checks their work,
decides what the mission *is*, and is accountable for the outcome.

**The asymmetry (ch. 2), stated with its own limit.** Solving and verifying
are different operations, not one harder one. When a model generates it
samples the likely continuation; when asked to verify it *samples again from
the same distribution that produced the error* — self-verification is more
retrieval against the landscape that contained the mistake (Stechly,
Valmeekam & Kambhampati). Verification that matters requires grounding in the
specific domain reality — does this package exist in the registry, does this
test test the thing — and that grounding is outside what approximate retrieval
contains. Faster solving widens the SOLVE channel; the VERIFY gate stays
human-sized; the gap *deepens*. The book flags this as a **wager, not a
theorem** (P vs NP is an analogy, bounded twice; reasoning models are the live
counter-case). The beat inherits that honesty: she says it is the working
assumption, not a proof.

**The five supervisory capacities** — the labels every human step carries:

| | Capacity | The move | Chapter |
|---|---|---|---|
| `[PA]` | Plausibility Auditing | hearing the wrong note *before* verification — the diff that is plausible and wrong | 4–5 |
| `[PF]` | Problem Formulation | deciding what the mission is before Claude sees it; the `/v0` sentence: *[THING] is a [WHAT] inserted [WHERE] that produces [OUTPUT]* | 6–7 |
| `[TO]` | Tool Orchestration | which Claude task, in what order, with what context and trust — plan mode, a subagent, `/clear`, a hook | 8–9 |
| `[IJ]` | Interpretive Judgment | supplying meaning and accountability the output cannot supply — the test passes, and it is testing the wrong thing | 10–11 |
| `[EI]` | Executive Integration | holding several threads toward one goal; noticing when one output means another task must re-engage | 12–13 |

**The score.** Two simultaneous parts. MINION PART: Claude's steps, each
with the prompt that drove it — *a complete specification, not a delegation*
("Write the User model" is not a prompt). GRU PART: her steps, each labelled
with the capacity exercised and an action specific enough to be a checklist
item ("verify every entity in the schema maps to a named need; flag any
entity that exists only to serve another entity"). Every Claude step is
followed by a **handoff condition** — testable, never "looks good". Steps
are ordered by dependency. A capacity that appears zero times is named as a
gap: *a boondoggle with no `[PA]` assumes Claude is always right.*

**The dangerous middle** — the beat rings one step in terracotta: Claude
generating an architectural decision from an incomplete spec; Claude
expanding scope past the task; plausible-but-domain-wrong content;
Claude-on-Claude verification sharing the same blind spot. That step is where
all the damage lives — between what she meant and what the minion understood.

**Labor heuristics (Gru).** Claude: scaffolding from a complete spec, tests
from documented criteria, format transforms, boilerplate, finding
inconsistencies against explicit rules, variations for review. Human: whether
this is the right problem; whether the output is plausible given knowledge
not in the prompt; signing her name; integrating threads; choosing among
variations; noticing what is *missing* that Claude cannot know is missing;
deciding when to stop.

---

## HUMAN — the ledger

**Source:** `info-7375-irreducibly-human/chapters/04-tier-4-metacognitive-and-supervisory.md`
(the tier AI cannot supply about itself), `00-introduction.md` (the seven
tiers), `RUBRIC-WORKSHEET.md` (the coding rule: assign by which tier's
*human* capacity the work exercises — not by whether AI can do it today).

**The one sentence.** A system that could accurately report its own
uncertainty in every case would not hallucinate — so the failure and the
inability to flag the failure are the same fact, and the entire metacognitive
burden falls on the human.

**Type 1 / Type 2 (Lee et al., 2025).** Type 1 is discrimination — the
machine's predictive job, and it is superhuman at it. Type 2 is *metacognitive
sensitivity* — accurately assessing how much confidence a Type 1 answer
deserves. An AI with lower accuracy but honest uncertainty produces better
team outcomes than a more accurate, overconfident one. Current models are
weak at Type 2. So the Type 2 task — for her work *and* for evaluating the
machine's — is entirely hers.

**The inverted signal.** Humans slow down when a speaker hedges. These
systems grow *more* fluent and assertive exactly when fabricating (Cash et
al., 2025). The absence of expressed uncertainty is not evidence of accuracy;
given the inversion, it may be the opposite. That is why the SKEPTIC beat
cannot be replaced by asking Claude whether it is sure. (The New York
attorney checked his fabricated citations by asking the same chatbot; it
assured him twice.)

**The volume trap.** Generation scales ten-fold; verification does not. The
verification *rate* falls while the error rate holds — more unverified
output, not less error. The ledger's MUST rows are the ones that do not speed
up when the solver does.

**Plausibility auditing** needs four things she either has or doesn't: deep
domain knowledge (you cannot audit a claim you lack the background to
evaluate — *the capacity you offload the production of is the one you must
retain to audit the product*); calibrated skepticism (what *this* machine
gets wrong in *this* domain); source-verification habits (the primary, not
the summary); internal-consistency checking. It breaks when the error is
outside her domain, when fluency is mistaken for accuracy, under the volume
trap, and whenever she assumes the machine knows its own limits.

**The verdict is supervise.** Not "do not use". The machine does real Type 1
work. Every output crosses a desk where a human performs the Type 2 task the
machine cannot. Verification is not the residue of the process; it is the
part with consequence in it — the solver faces no court, no patient, no
refund; the verifier signs.

**Filling the ledger — from the session, not from principle.**

| Column | Row | Comes from |
|---|---|---|
| HUMAN · MUST | decide what "done" means | the Popper move she ran |
| HUMAN · MUST | sign the diff | the CHANGE beat she read |
| HUMAN · MUST | catch the confident error | the `[PA]` step in the score |
| HUMAN · SHOULD | read the tree before the diff · write the failure case first | the `[TO]` / `[PF]` steps |
| AI · CAN | scaffold from a spec · draft tests from criteria · find every call site | the MINION PART |
| AI · SHOULD | plan mode on a new repo · hand back a plan, not a change | the `[TO]` decisions |

She closes on one sentence: what she would not delegate next time, and why.
The recursive point, if the episode can carry it: *knowing when to distrust
the machine is itself a Tier 4 act* — the capacity the taxonomy describes is
the one needed to apply it, and it is the one the machine cannot lend.
