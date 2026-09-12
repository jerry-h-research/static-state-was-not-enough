# Learning-Triad Attack Round 2 — v0.2

**Target:** `LEARNING_TRIADS_CANDIDATES_v0_2.md`

## External-context note

Recent personalization work makes the novelty boundary stricter than the initial project framing assumed. In particular, PAHF (2026) explicitly studies continual personalization from live pre/post-action feedback using per-user memory, while CUPID (2025) evaluates context-dependent preferences inferred from interaction histories. Therefore, merely showing that an agent can remember and reapply a user preference is not sufficient to establish a distinctive research contribution here.

The bounded value of this experiment must instead come from the narrower question: **can a minimal controlled interaction-policy state reduce operating burden while transferring selectively, resisting exceptions, and remaining subordinate to epistemic/safety guardrails?**

## Finding T7 — Triads 1–3 can collapse into style/profile memory

Severity: **HIGH**

`SUMMARY_FIRST`, `RECOMMEND_ONE_FIRST`, and `MINIMAL_EDIT` are legitimate user preferences, but storing and reapplying them may demonstrate only explicit preference memory. That is already close to established personalization benchmarks.

**Repair:** do not interpret successful triads as evidence of a novel mechanism. Treat them as mechanism sanity checks for feedback-dependent policy retrieval. The practical claim must remain burden reduction + selective scope control + guardrail preservation.

## Finding T8 — Exception probes must require context-sensitive reversal, not explicit override

Severity: **HIGH**

If an exception task literally says “give me full detail this time,” any competent model can override stored preference. That does not test whether the learned policy has a useful scope model.

**Repair:** exception probes should differ by contextual cues frozen in the task, with no explicit statement that the learned convention should be disabled. Gold must justify why the exception context changes the preferred interaction mode.

## Finding T9 — Triad 4 risks rewarding aggressive guessing

Severity: **HIGH**

`ASSUME_AND_ACT_WITH_STATED_ASSUMPTION` can reduce burden simply by asking fewer questions. It is useful only in genuinely low-risk ambiguity where either branch is reversible and the assumption is visible.

**Repair:** keep this triad only if exposure/transfer tasks have two harmless plausible branches and the exception contains a materially consequential ambiguity that triggers the generic guardrail. The exception should be scored as guardrail dominance, not personalization failure.

## Finding T10 — Condition C may infer common stylistic defaults

Severity: **MEDIUM**

Some preferences (summary-first, minimal edit) are common defaults. If C happens to choose them, B has little observable room to improve.

**Repair:** A/B/C task variants should be authored so that both preference modes are reasonable and neither is strongly cued as the conventional default. Development runs may be used to reject candidates with extreme baseline skew before sealing, but final evaluation tasks must remain untouched.

## Finding T11 — Policy vocabulary itself can leak the hypothesis

Severity: **MEDIUM**

A state field literally named `SUMMARY_FIRST` can act like a direct instruction. That is unavoidable to some degree, but it means ON-vs-OFF demonstrates the effect of a learned symbolic preference artifact, not an internal learned policy in the model.

**Repair:** state the mechanism claim narrowly: feedback-derived external policy state causally changes downstream decisions. Do not describe this as model-internal learning. SHAM remains necessary to control artifact presence.

## Finding T12 — Four triads should span more than presentation style

Severity: **MEDIUM**

If all successful triads concern formatting/presentation, practical burden reduction may not generalize to coordination decisions.

**Repair:** preserve at least two presentation/editing conventions and at least two interaction-control conventions. Triad 4 supplies one interaction-control candidate; a second should concern initiative/option handling without crossing into epistemic safety.

## Round-2 disposition

**REVISE BEFORE CONCRETE SEALED TASK AUTHORING.**

The v0.2 split between personalization and guardrails is sound, but the interpretation boundary must be narrowed. Successful preference retrieval is not by itself novel; the experiment is valuable only if it demonstrates selective feedback-dependent policy use with measurable operating-burden benefit beyond a static heuristic, while guardrails dominate when required.
