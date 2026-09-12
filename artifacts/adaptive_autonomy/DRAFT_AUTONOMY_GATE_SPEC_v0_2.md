# Controlled Autonomy Gate Specification v0.2 (DRAFT)

**Status:** DRAFT — revised after Confidence/Gating Attack Round 2.

## 1. Shared base system

L0, L1, and L2 use the same model/version/settings, base instruction, tools, task context, adaptive-state object, renderer, context taxonomy, hard guardrails, and response generator.

They differ only in the minimum **evidence regime** required before a reusable learned convention may resolve an eligible low-risk interaction choice without explicit user control.

The LLM never sees the autonomy regime label, numeric threshold, or controller rationale.

## 2. State representation

Each learned interaction convention contains only controlled fields:

```json
{
  "entry_id": "opaque ID",
  "context_class": "CONTROLLED_ENUM",
  "interaction_mode": "CONTROLLED_ENUM",
  "scope": "LOCAL_ONLY | REUSABLE_WITHIN_CLASS",
  "evidence": "WEAK | STRONG | CONTESTED",
  "exception": false,
  "revision_of": null
}
```

No free-form rationale, task answer, factual proposition, raw transcript, hidden label, future-task information, or model-generated confidence text is allowed.

## 3. Feedback events that may update reusable state

Only **explicit interaction-level feedback** can affect reusable-state evidence.

Eligible examples:

- participant explicitly selects one of two otherwise-valid interaction modes for this context class;
- participant explicitly states that the convention should apply to similar tasks in the same class;
- participant explicitly rejects/reverses a previously reusable convention.

Ineligible for reusable evidence:

- passive absence of correction;
- task success by itself;
- generic praise;
- model self-assessment;
- factual agreement;
- inferred satisfaction.

## 4. Evidence-state update rule

### New feedback

- one explicit reusable interaction-level selection -> `WEAK`;
- a second compatible explicit reusable selection in a distinct task within the same frozen context class -> `STRONG`;
- explicit contradiction/reversal in an applicable context -> `CONTESTED` immediately;
- explicit resolution after `CONTESTED` creates a revised entry under a frozen revision rule.

Arithmetic accumulation is not used.

### Local-only feedback

A task-specific correction that does not explicitly support cross-task reuse is stored as `LOCAL_ONLY` and cannot authorize cross-task auto-use at any autonomy level.

## 5. Context applicability

Before the autonomy regime is consulted, a frozen applicability function returns:

`MATCH | NO_MATCH`

The applicability function uses only the frozen coarse interaction context taxonomy. It must not create task-derived labels or encode answer semantics.

A state entry is eligible only when:

- `scope = REUSABLE_WITHIN_CLASS`;
- `context_match = MATCH`;
- `evidence != CONTESTED`;
- no explicit exception blocks the current context.

## 6. Invariant hard gates

Even an eligible learned convention cannot auto-resolve the interaction choice if any hard gate is true:

- explicit current-task instruction conflicts with the learned convention;
- material ambiguity affects task substance rather than interaction style;
- unresolved factual truth controls the decision;
- authorization is required;
- action is irreversible or externally consequential;
- applicable safety/verification rule requires user or external confirmation.

These gates are identical in L0/L1/L2.

## 7. Ordered autonomy regimes

### L0 — RETAIN_CONTROL

Never auto-use learned state to remove explicit user control. Eligible state may inform internal reasoning but cannot authorize autonomous resolution of the interaction choice.

### L1 — STRONG_EVIDENCE_AUTO

Auto-use is permitted only when:

`REUSABLE_WITHIN_CLASS + STRONG + MATCH + HARD_GATES_PASS`

### L2 — WEAK_EVIDENCE_AUTO

Auto-use is permitted when:

`REUSABLE_WITHIN_CLASS + (WEAK or STRONG) + MATCH + HARD_GATES_PASS`

These are ordered policy regimes, not equally spaced numeric levels.

## 8. Deterministic controller output

Before natural-language generation, the controller emits one normalized decision:

`USE_STATE_AND_ACT | ASK_USER | PRESENT_OPTIONS | VERIFY | DEFER`

The autonomy regime affects only whether `USE_STATE_AND_ACT` is permitted for the current low-risk interaction choice.

The LLM receives the task plus the controller-authorized action mode; it does not receive the regime label, evidence arithmetic, or threshold metadata.

## 9. Audit log

Every decision records:

- task ID;
- matched state entry ID or NONE;
- scope;
- evidence state;
- context match;
- hard-gate flags;
- autonomy regime;
- controller output;
- state mutation, if any.

For blinded downstream evaluation, regime/state labels are withheld from primary coders.

## 10. Condition C

C receives no user-specific adaptive state. It uses the identical base model/system plus a frozen generic non-learning heuristic. C may resolve low-risk interaction choices from current-task information alone.

C is a complexity/practical comparator, not part of the one-variable L0/L1/L2 autonomy manipulation.

## 11. Remaining development risks

Before freeze, attack:

- whether explicit `REUSABLE` feedback makes the experiment too artificial;
- whether two compatible selections are enough to call evidence `STRONG`;
- whether context matching is sufficiently coarse to avoid semantic leakage yet specific enough to support useful reuse;
- whether L2 burden reduction is mechanically guaranteed on the chosen task set;
- whether L0/L1/L2 remain distinguishable after static heuristic C is made strong.

This v0.2 is not ready for sealed execution.
