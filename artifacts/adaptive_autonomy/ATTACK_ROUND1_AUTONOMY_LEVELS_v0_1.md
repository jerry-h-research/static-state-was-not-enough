# Adaptive Autonomy Contract — Attack Round 1

**Target:** `DRAFT_ADAPTIVE_AUTONOMY_FALSIFICATION_CONTRACT_v0_1.md`

**Focus:** Can L0/L1/L2 be interpreted as controlled autonomy levels rather than three differently worded prompts?

## Finding A1 — Autonomy is not yet an independently manipulable variable

Severity: **HIGH**

The draft describes L0/L1/L2 behaviorally, but an implementation could realize them as three system prompts with different wording/caution. Any observed curve could then be caused by prompt framing rather than adaptive autonomy.

**Required repair:** all conditions must share one identical base instruction. Autonomy must be implemented by a small machine-readable control object whose fields differ prospectively across levels.

## Finding A2 — L1 vs L2 currently changes more than one dimension

Severity: **HIGH**

The draft allows L2 to use broader scope *or* lower confidence. Changing both scope and threshold prevents interpretation of which autonomy dimension caused burden/integrity changes.

**Required repair:** first feasibility study varies exactly one autonomy gate. Keep scope taxonomy, state content, renderer, model prompt, and safety gates fixed.

Recommended first gate: **minimum adaptive-state confidence required to resolve a low-risk interaction choice without explicit user confirmation**.

## Finding A3 — L0 and C can collapse into the same comparator

Severity: **MEDIUM**

L0 defaults toward explicit control; C uses generic static heuristics. Depending on task construction, both may make identical decisions, creating redundant conditions without adding evidence.

**Required repair:** distinguish their purposes prospectively. L0 is an intentionally conservative control-retention policy. C is the strongest simple non-learning heuristic allowed to infer low-risk choices from current task context alone. If development screening shows no behavioral separation, drop one before freeze rather than preserving redundant arms.

## Finding A4 — Learned-state availability is confounded with autonomy level

Severity: **HIGH**

If L0 has no adaptive state while L1/L2 do, the human-facing comparison simultaneously varies state availability and permission to act on it.

**Required repair:** for the autonomy-curve assay, provide the same adaptive-state object to L0/L1/L2 but vary only the frozen autonomy gate governing whether state may resolve the current interaction choice. Keep a separate no-state/static comparator for practical benchmarking.

This makes the conceptual comparison:

`same learned signal + different permission to rely on it`

rather than:

`no learned signal vs learned signal`.

## Finding A5 — “Autonomy” must be observable at the decision boundary

Severity: **HIGH**

A model can produce verbose language that obscures whether it actually exercised autonomy.

**Required repair:** before natural-language response generation, require a normalized interaction-control decision such as:

`USE_STATE_AND_ACT | ASK_USER | PRESENT_OPTIONS | VERIFY | DEFER`

and log the gate inputs that authorized that decision. Natural-language style cannot define autonomy level.

## Finding A6 — L2 could appear better simply because it ignores the participant

Severity: **HIGH**

Lower confirmation threshold mechanically reduces pre-action burden. Without an explicit displaced-burden accounting rule, L2 can win by guessing more often and relying on correction later.

**Required repair:** primary burden must include both pre-action control and post-action repair. Report displaced burden separately and require integrity non-worsening.

## Finding A7 — Confidence is currently underspecified

Severity: **HIGH**

If confidence is produced by the model in free-form fashion, the intervention can move the goalposts. If confidence simply counts repeated acceptance, it may become a proxy for exposure frequency rather than applicability.

**Required repair:** freeze a deterministic confidence update rule based only on allowed feedback events. Confidence cannot be self-reported by the language model during sealed evaluation.

## Finding A8 — Context applicability must be fixed before the autonomy gate

Severity: **HIGH**

A low confidence threshold is meaningless if the model can freely declare that any learned convention applies to the current task.

**Required repair:** use a frozen context-class/applicability function or controlled label mapping developed before sealing. The autonomy gate consumes applicability; it does not invent it.

## Finding A9 — Critical guardrails should not vary with autonomy level

Severity: **HIGH**

If L2 is allowed to relax epistemic, authorization, or irreversible-action gates, the study becomes an intentionally unsafe-policy comparison rather than a useful autonomy-boundary test.

**Required repair:** critical guardrails are invariant hard gates across L0/L1/L2/C. Autonomy varies only inside the pre-defined low-risk interaction-choice region.

## Finding A10 — A single confidence threshold may still be too artificial

Severity: **MEDIUM**

A threshold experiment is clean, but may only show a property of the chosen state-confidence mechanism rather than a general human-control principle.

**Interpretation constraint:** even a clean result should be described as a bounded operating curve for this mechanism/protocol, not a universal autonomy law.

## Round-1 disposition

**DO NOT IMPLEMENT v0.1 AS WRITTEN.**

The core idea survives, but L0/L1/L2 must be rebuilt as one shared policy with one controlled autonomy parameter. The cleanest first feasibility manipulation is a deterministic confirmation threshold over the same learned state, with invariant applicability and safety gates.
