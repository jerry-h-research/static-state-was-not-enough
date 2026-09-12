# Adaptive Autonomy — Attack Round 3: Non-Rejection Evidence

**Target:** `DRAFT_SELECTIVE_CORRECTION_STATE_MACHINE_v0_1.md`

**Question:** Can repeated non-rejection safely justify removing explicit user control?

## Finding N1 — Non-rejection remains fundamentally ambiguous

Severity: **HIGH**

Even under a visible correction opportunity, failure to object can mean acceptance, indifference, low task importance, fatigue, inattention, unnoticed error, or willingness to tolerate a suboptimal result. The protocol can improve observability but cannot identify the participant's latent preference from silence alone.

**Consequence:** `SURVIVED_OPPORTUNITY` must not be treated as positive preference evidence strong enough, by itself, to establish a reusable convention.

## Finding N2 — Repeated silence can amplify the wrong behavior

Severity: **HIGH**

If a participant fails to notice one bad behavior and the system interprets silence as survival evidence, the behavior becomes more likely to be reused, which creates more opportunities for the same unnoticed behavior to persist. This is exactly the kind of self-reinforcing loop the broader project is trying to avoid.

**Required repair:** silent/non-rejected behavior may not autonomously increase reusable preference authority.

## Finding N3 — Ordinary users make the ambiguity worse, not better

Severity: **HIGH**

The motivating participant is unusually willing to reject bad outputs. A passive or low-monitoring user is more likely to leave errors uncorrected. Therefore a mechanism that is safe only when silence is highly informative would generalize in the wrong direction for the product question.

## Finding N4 — Soliciting confirmation would recreate the burden we are trying to remove

Severity: **HIGH**

The obvious repair—ask "do you want me to keep doing this?"—creates explicit preference-elicitation burden and partially collapses the study back toward prompt-driven personalization.

This is not prohibited as a comparator, but it cannot be the only path to a low-burden system.

## Finding N5 — Negative feedback is much more identifiable than positive silence

Severity: **HIGH / PRODUCTIVE**

Explicit rejection can safely support claims such as:

- this behavior was unacceptable here;
- avoid repeating this exact interaction failure under matched conditions;
- narrow a previously broad candidate rule.

It cannot by itself identify one globally preferred alternative, but it can **prune the action space**.

This suggests a different mechanism:

`learn what not to repeat` rather than `infer what the user prefers from silence`.

## Finding N6 — Burden reduction may come from elimination, not preference estimation

Severity: **HIGH / PRODUCTIVE**

If repeated explicit rejections remove known-bad interaction choices, the system can reduce future clarification/correction burden by avoiding them. Among the remaining allowed choices, a generic static heuristic can choose the action.

This gives a cleaner hybrid:

`explicit negative feedback -> prohibited/narrowed interaction choices`

plus

`current-task static heuristic -> choose among remaining valid choices`

No positive meaning is assigned to silence.

## Finding N7 — This changes what L1/L2 should vary

Severity: **HIGH**

The previous L1/L2 difference was how much silent survival evidence was required before autonomous reuse. That manipulation is no longer defensible.

A cleaner autonomy manipulation is how aggressively the system may use **negative-feedback-derived exclusions** to narrow the choice set across matched contexts:

- conservative: only exact/specific exclusion reuse;
- broader: reuse exclusion within a pre-frozen context class.

Hard epistemic/authorization/irreversibility gates remain invariant.

## Finding N8 — Negative-only learning can still overgeneralize

Severity: **HIGH**

A rejection can be local to one task. If the system generalizes "don't do A" too broadly, it may suppress a valid behavior elsewhere. Therefore the experiment still needs matched transfer and exception probes, but they now test the scope of **negative constraints**, not inferred positive preference.

## Round-3 disposition

**REJECT `SURVIVED_OPPORTUNITY` AS AUTONOMY-AUTHORIZING EVIDENCE.**

Do not let silence accumulate into reusable preference authority in the first feasibility implementation.

Proceed, if at all, with a simpler negative-first design:

1. explicit rejection creates a candidate exclusion/narrowing rule;
2. silence does not strengthen it;
3. cross-task reuse is allowed only under a prospectively frozen scope rule;
4. current-task static heuristics select among remaining non-excluded options;
5. explicit contradictory feedback narrows/removes the exclusion immediately;
6. the experiment tests whether negative-only calibration can reduce repeated control burden without suppressing valid behavior.

This is more conservative than the motivating natural interaction, but it avoids converting silence into authority before that assumption has evidence.
