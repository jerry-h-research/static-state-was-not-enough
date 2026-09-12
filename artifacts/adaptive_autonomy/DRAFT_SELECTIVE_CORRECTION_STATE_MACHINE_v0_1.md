# Selective-Correction State Machine v0.1 (DRAFT)

**Status:** development candidate; not frozen or implemented.

## 1. Goal

Represent naturally revealed interaction conventions without requiring the user to explicitly declare a reusable preference or write a policy for the AI.

The machine must preserve the asymmetry:

- explicit rejection/correction is strong evidence;
- explicit endorsement, if it occurs, is strong evidence;
- non-rejection is never labeled acceptance;
- repeated non-rejection may count only as weak **survival evidence** when a correction opportunity was genuinely observable.

## 2. Candidate convention states

`UNSEEN -> CANDIDATE -> SURVIVING -> ESTABLISHED`

Any reusable state may transition to:

`CONTESTED` or `LOCAL_ONLY`.

These labels describe interaction-policy evidence only. They carry no factual authority.

## 3. Creating a candidate

A convention may become `CANDIDATE` after either:

1. an explicit correction selects interaction behavior B over behavior A for the current task; or
2. an explicit endorsement selects B.

The updater stores only the controlled interaction mode/context class permitted by the frozen schema, never the raw task proposition or answer.

A single event does not establish broad reuse.

## 4. Correction opportunity

Non-rejection can be considered only when all frozen opportunity conditions are true:

- the model visibly exercised the candidate convention;
- the participant received the resulting output;
- the participant had a protocol-defined opportunity to correct before the task closed;
- the task outcome did not conceal whether the convention was exercised;
- no material protocol deviation occurred;
- external gold does not identify a latent critical defect that the participant failed to notice.

If any condition fails, the event is `NO_EVIDENCE`.

## 5. Survival evidence

A qualifying non-rejection event is recorded as:

`SURVIVED_OPPORTUNITY`

not `ACCEPTED`.

Development candidate transitions:

- `CANDIDATE + 1 independent SURVIVED_OPPORTUNITY -> SURVIVING`
- `SURVIVING + 1 additional independent SURVIVED_OPPORTUNITY -> ESTABLISHED`

The two survival opportunities must occur on different task instances prospectively mapped to the same context class.

These counts are design candidates and require attack before freeze.

## 6. Explicit negative feedback

An explicit rejection/correction in a context where the convention was applied has priority over accumulated survival evidence.

- if feedback indicates the convention was wrong for this context class generally: `-> CONTESTED`;
- if feedback indicates only the present task is an exception: retain broader state but record a frozen-scope exception / `LOCAL_ONLY` override as permitted by schema;
- no numeric averaging may allow multiple prior silent survivals to overpower a current explicit correction.

## 7. Explicit positive feedback

If the participant spontaneously gives an explicit reusable endorsement, record it separately as `EXPLICIT_POSITIVE`. It may strengthen evidence under a pre-frozen rule, but the sealed protocol must not solicit such endorsement merely to make the system learnable.

## 8. Passive continuation is not always observable feedback

The following must not count as survival evidence by default:

- the user moves on without having seen the relevant behavior clearly;
- the user cannot reasonably know the output is defective;
- the task is too low-importance for correction behavior to be interpretable;
- the model's choice is hidden inside a long response;
- the participant protocol prevented correction;
- the interaction ended before a correction opportunity.

## 9. Autonomy gate mapping — development candidate

Use the same learned state for all autonomy levels.

- `L0`: never auto-use a convention to remove explicit control.
- `L1`: auto-use only `ESTABLISHED` conventions when context matches and all invariant hard gates pass.
- `L2`: auto-use `SURVIVING` or `ESTABLISHED` conventions under the same match/hard-gate rules.

`CANDIDATE`, `CONTESTED`, and `LOCAL_ONLY` do not authorize cross-task autonomous reuse.

Thus L1/L2 differ only in how much weak survival evidence is required before explicit control can be removed.

## 10. Safety / epistemic invariant

Survival evidence changes only permission to reuse a low-risk interaction convention. It cannot increase confidence in factual propositions, user beliefs, external evidence, or authorization.

A latent externally coded critical defect invalidates the corresponding survival opportunity even if the participant did not object.

## 11. What this can and cannot test

This state machine can test a bounded question:

> how much rejection/survival evidence is required before a system may safely stop asking for explicit control over a low-risk interaction convention?

It cannot establish that silence means preference, that the user consciously endorses the surviving convention, that this is how commercial models internally learn, or that the process explains the existing long-running interaction.

## 12. Required next attack

Before implementation, attack:

- whether `SURVIVED_OPPORTUNITY` is still too ambiguous to count as evidence;
- whether two survival opportunities are arbitrary or gameable;
- whether the protocol itself changes natural correction behavior;
- whether participant visibility can be operationalized without forcing artificial feedback;
- whether `ESTABLISHED` is an overclaiming label and should be renamed;
- whether L1/L2 have enough task opportunities to produce measurable burden separation without constructing the result into the task sequence.
