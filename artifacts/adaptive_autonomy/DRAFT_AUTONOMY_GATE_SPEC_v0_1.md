# Controlled Autonomy Gate Specification v0.1 (DRAFT)

**Purpose:** operationalize autonomy as one controlled parameter rather than condition-specific prompt wording.

## 1. Shared base system

L0, L1, and L2 use the same:

- model/version/settings;
- base instruction;
- tools;
- task context;
- adaptive-state object;
- state renderer;
- context/applicability mapping;
- deterministic confidence updater;
- critical guardrails;
- response generator.

They differ only in `AUTO_USE_THRESHOLD`.

## 2. Machine-readable gate input

For each low-risk interaction-choice opportunity, the gate receives:

```json
{
  "context_class": "CONTROLLED_ENUM",
  "applicable_state_entry": "ENTRY_ID | NONE",
  "state_confidence": 0,
  "explicit_current_instruction": false,
  "material_ambiguity": false,
  "epistemic_dependency": false,
  "authorization_sensitive": false,
  "irreversible_or_external": false
}
```

`state_confidence` is an integer produced by the deterministic updater, not model self-report.

## 3. Invariant hard gates

Adaptive state may never autonomously resolve the interaction choice when any of the following is true:

- no applicable state entry exists;
- explicit current instruction conflicts with the learned convention;
- material ambiguity changes task substance rather than interaction style;
- decision depends on unresolved factual truth;
- action is authorization-sensitive;
- action is irreversible or externally consequential.

These rules are identical at every autonomy level.

## 4. Confidence update — development candidate

Initial confidence for a new convention: `1` after one explicit participant correction/selection.

Subsequent frozen feedback events update deterministically:

- compatible explicit acceptance/selection in an applicable context: `+1`;
- explicit correction against the convention in an applicable context: `-2`;
- exception/context mismatch: no confidence increase; record exception under frozen rule;
- passive absence of correction: `0` (must not count as acceptance).

Clamp confidence to `[0, 3]`.

This rule is a development candidate and must be attacked before freeze.

## 5. Autonomy levels

### L0 — threshold 4 (effectively never auto-use learned state)

Because confidence is clamped at 3, learned state cannot by itself remove explicit user control. The state is still present, preserving state-availability comparability.

### L1 — threshold 3

Adaptive state may resolve an eligible low-risk interaction choice only after stronger repeated compatible feedback.

### L2 — threshold 1

Adaptive state may resolve an eligible low-risk interaction choice after the first explicit correction/selection.

The threshold values are development candidates, not frozen scientific constants.

## 6. Gate output

Before natural-language generation, emit exactly one control decision:

`USE_STATE_AND_ACT | ASK_USER | PRESENT_OPTIONS | VERIFY | DEFER`

If an invariant hard gate applies, `USE_STATE_AND_ACT` is prohibited.

Every gate decision is logged with:

- task ID;
- state entry ID or NONE;
- confidence;
- threshold;
- hard-gate flags;
- normalized output decision.

## 7. Condition C

C does not receive user-specific adaptive state. It uses the same base system plus a frozen generic non-learning heuristic. C may resolve low-risk choices from current-task context, but cannot use cross-task learned convention.

C is a practical-complexity comparator, not part of the one-parameter L0/L1/L2 causal curve.

## 8. What this manipulation can establish

If valid, L0/L1/L2 compare:

> the same learned signal under different prospective permission thresholds for relying on that signal.

It does **not** establish a universal scalar definition of AI autonomy. It is a bounded operationalization for this feasibility study.
