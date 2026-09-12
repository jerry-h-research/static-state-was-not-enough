# Learning-Triad Attack Round 1

**Target:** `LEARNING_TRIADS_CANDIDATES_v0_1.md`

## Finding T1 — Static heuristic C may solve all four candidates

Severity: **HIGH**

The current candidates mostly encode generic good interaction behavior already present in Condition C: clarify material ambiguity, verify uncertain facts, respect authorization boundaries, and avoid premature action. If C already chooses the same correct behavior from task text alone, B has little room to demonstrate feedback-dependent adaptation.

**Required repair:** at least some triads must contain a *user-specific but non-epistemic convention* that is not justified as a universal generic heuristic before exposure.

## Finding T2 — Triad 1 correction may be too globally cautious

Severity: **MEDIUM**

“Analyze before modification” can become a generic conservative rule. The exception helps, but a fixed heuristic could still encode it.

**Required repair:** define a narrower user-specific convention, such as a preference for diagnosis-first only for a frozen context class where either workflow is otherwise reasonable.

## Finding T3 — Triad 2 is mostly task ambiguity, not personalization

Severity: **HIGH**

Asking when a material variable is missing is generic competence. It tests whether the system recognizes underspecification, not whether feedback created a user-specific coordination policy.

**Required repair:** replace or redesign with a convention where two interaction styles are both objectively acceptable before exposure, but participant feedback selects one for later matched contexts.

## Finding T4 — Triad 3 is primarily epistemic safety

Severity: **MEDIUM**

Evidence checking is important as a guardrail but is poorly suited as positive evidence of personalized interaction-policy learning because Condition C should already verify unresolved decision-relevant facts.

**Required repair:** retain it as a critical safety/epistemic probe, not one of the four positive learning triads.

## Finding T5 — Triad 4 is primarily authorization safety

Severity: **MEDIUM**

Like Triad 3, this is a valuable critical probe but generic safe behavior should already handle it.

**Required repair:** move it to the critical-probe set. Do not count generic safety compliance as evidence that B learned a user-specific convention.

## Finding T6 — We need two distinct test families

Severity: **HIGH**

The current design is trying to make the same triads prove both personalization and safety. That encourages confusion.

**Required repair:** split the sealed material into:

1. **Learning triads** — user-specific, non-epistemic conventions where multiple behaviors are reasonable before exposure and feedback selects one.
2. **Critical guardrail probes** — factual uncertainty, authorization, high-stakes, and exception cases where learned preference must *not* override generic safety/epistemic rules.

## Round-1 disposition

**DO NOT SEAL current triads.**

The attack found a conceptual flaw before implementation: generic best-practice behavior could masquerade as learned personalization. The next candidate set should reserve positive mechanism evidence for conventions that cannot be inferred as universally correct from the task alone.
