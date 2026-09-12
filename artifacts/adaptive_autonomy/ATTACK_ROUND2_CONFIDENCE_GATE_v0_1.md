# Adaptive Autonomy — Attack Round 2: Confidence / Gating

**Target:** `DRAFT_AUTONOMY_GATE_SPEC_v0_1.md`

## Finding C1 — Confidence score is doing too many jobs

Severity: **HIGH**

The draft uses one scalar `state_confidence` to stand in for at least three different things:

1. how consistently the user has expressed a convention;
2. how applicable that convention is to the current context;
3. how much permission the system has to act without confirmation.

These are not equivalent. A convention may be highly stable but inapplicable to the current task. Collapsing them creates false autonomy.

**Repair:** separate `preference_strength` from `context_match`. The autonomy gate may act only when both independent criteria pass.

## Finding C2 — +1 / -2 is arbitrary and can manufacture the curve

Severity: **HIGH**

The exact update weights determine how quickly L1/L2 cross the autonomy threshold. A different weight schedule can change the apparent safe region without any change in user behavior.

**Repair:** do not treat the score magnitude itself as a substantive construct. Use a small ordinal evidence state based on explicit event counts, and report raw supporting/contradicting events alongside any derived level.

## Finding C3 — One explicit correction may not imply permission to auto-apply later

Severity: **HIGH**

A correction can be task-specific. L2 threshold=1 risks interpreting a single local correction as a reusable convention.

**Repair:** a reusable convention requires an explicit `REUSABLE` signal under the frozen participant protocol or two compatible explicit selections across distinct development contexts. Single-task corrections remain `LOCAL_ONLY` and cannot unlock cross-task autonomy.

## Finding C4 — Passive non-correction is correctly excluded, but explicit acceptance is still ambiguous

Severity: **MEDIUM**

A user can accept an output because it is good enough, not because they endorse the interaction convention.

**Repair:** only feedback events explicitly about the interaction choice can update reusable-state strength. Task-success feedback alone does not count.

## Finding C5 — Context matching can leak the answer

Severity: **HIGH**

If the context classifier sees rich task semantics and chooses a highly specific label, it can effectively smuggle task meaning into the state-selection process.

**Repair:** freeze a coarse context taxonomy and a deterministic or separately evaluated mapping. Context labels must be interaction-level, not answer-level. Add a leakage review and require that the same label can validly cover multiple semantically different tasks.

## Finding C6 — Threshold 4/3/1 creates uneven evidence spacing

Severity: **MEDIUM**

With a 0–3 scale, L0=4 and L1=3 are structurally different from L2=1. The curve is not evenly interpretable, and there is no threshold-2 condition.

**Repair:** stop treating levels as a continuous mathematical scale. Define them as ordered policy regimes (`RETAIN_CONTROL`, `STRONG_EVIDENCE_AUTO`, `WEAK_EVIDENCE_AUTO`) rather than implying equal intervals.

## Finding C7 — The current gate cannot distinguish “state says X” from “state says do not infer”

Severity: **MEDIUM**

Some feedback should create negative policy knowledge: for example, “do not generalize this beyond this narrow context.”

**Repair:** represent scope explicitly as `LOCAL_ONLY | REUSABLE_WITHIN_CLASS`, and allow explicit exception records. The gate must check scope before any strength threshold.

## Finding C8 — Contradictory feedback needs immediate demotion, not arithmetic smoothing

Severity: **HIGH**

If the user explicitly reverses a prior convention, a cumulative score could remain high enough to continue auto-using stale behavior.

**Repair:** latest explicit contradiction in an applicable context should force `CONTESTED` state and suspend auto-use until a new explicit resolution event occurs. Do not rely only on score subtraction.

## Finding C9 — Autonomy burden can be reduced by asking fewer questions even when the learned state is irrelevant

Severity: **HIGH**

A permissive gate may still choose `USE_STATE_AND_ACT` because the model can rationalize weak relevance.

**Repair:** log and score a separate `state-relevance decision` before the autonomy threshold is applied. If no prospectively valid applicable entry exists, autonomy level cannot change the decision.

## Finding C10 — Same learned state across L0/L1/L2 is necessary but not sufficient

Severity: **MEDIUM**

If different levels expose different rendered metadata (e.g. threshold or confidence wording), the model can still respond differently due to prompt cues.

**Repair:** keep threshold evaluation outside the LLM. The model receives only the selected allowed action mode after a deterministic controller decides whether state use is permitted. The LLM must not see numeric thresholds or regime labels.

## Round-2 disposition

**The scalar-confidence design should be replaced before implementation.**

The better abstraction is not “confidence 0–3”, but a small audited state machine separating:

- `scope`: LOCAL_ONLY vs REUSABLE_WITHIN_CLASS;
- `evidence`: WEAK vs STRONG vs CONTESTED;
- `context_match`: MATCH vs NO_MATCH;
- `hard_gate`: PASS vs BLOCK.

Autonomy level then changes only the minimum evidence regime required for autonomous use:

- L0: never auto-use;
- L1: auto-use only when `REUSABLE_WITHIN_CLASS + STRONG + MATCH + PASS`;
- L2: auto-use when `REUSABLE_WITHIN_CLASS + (WEAK or STRONG) + MATCH + PASS`.

This preserves the intended manipulation while removing the arbitrary arithmetic score from the core mechanism.
