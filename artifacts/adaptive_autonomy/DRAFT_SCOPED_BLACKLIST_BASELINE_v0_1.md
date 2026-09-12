# Scoped Blacklist Baseline v0.1 (DRAFT)

**Purpose:** establish the smallest mechanism that can remember explicit rejection across tasks.

## 1. State

Each entry contains only:

- `context_class`
- `prohibited_mode`
- `exception_scope` (optional controlled label)
- `active`

No confidence score, no positive preference, no free-form rationale, no task answer, no factual proposition.

## 2. Update rule

On explicit rejection of interaction mode A in a valid mapped context:

- add or activate `(context_class, prohibited_mode=A)`;
- if participant feedback clearly marks only the current task as an exception, do not generalize;
- explicit later correction may deactivate or narrow the entry.

Silence/non-rejection never creates or strengthens an entry.

## 3. Decision rule

For a new task:

1. run the same frozen context/applicability mapping used by the adaptive condition;
2. apply the same invariant hard gates;
3. if an active blacklist entry matches and no exception/hard-gate conflict applies, remove the prohibited interaction mode from the base model's allowed decision set;
4. let the unchanged base model choose among the remaining allowed modes.

The blacklist does not select a preferred replacement mode.

## 4. Why this baseline matters

It tests whether the entire practical benefit can be explained by a trivial rule:

> remember what the user explicitly rejected and stop repeating it.

If this baseline matches a richer adaptive mechanism on control burden and trajectory integrity, the simpler blacklist is sufficient for this bounded study.

## 5. Required comparison

Any richer negative-first adaptive mechanism must share with BL:

- model/version/settings;
- base instruction;
- context/applicability mapping;
- hard gates;
- task set;
- participant protocol;
- rejection events.

It may claim additional complexity only if a prospectively defined capability beyond simple exclusion produces measurable benefit.
