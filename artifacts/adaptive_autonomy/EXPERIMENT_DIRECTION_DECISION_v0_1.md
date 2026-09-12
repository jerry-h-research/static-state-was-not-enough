# Experiment Direction Decision v0.1

**Status:** design decision before task screening; not frozen execution protocol.

## Decision

For the first Adaptive Autonomy / Human Control-Burden feasibility experiment, **do not implement a richer adaptive learner**.

Use the minimal **scoped negative-constraint mechanism** as the adaptive intervention.

## Why

The richer-mechanism necessity review found no additional capability that is both:

1. required to answer the current bounded research question; and
2. clearly distinct from positive-preference inference, semantic overgeneralization, or capabilities already representable by the simple scoped blacklist.

Adding complexity now would make attribution harder and recreate the architecture-first failure mode the project is trying to avoid.

## Narrow experimental question

> After a user explicitly rejects an interaction behavior, can scoped reuse of that negative constraint reduce later explicit control/correction burden without causing inappropriate cross-context suppression, trajectory degradation, or critical-boundary failures?

## Conditions — development target

### N0 — no cross-task reuse

Explicit rejection repairs the current task only. No negative constraint persists to later fresh tasks.

### N1 — narrow scoped reuse

The rejected interaction behavior is prohibited only in a prospectively defined narrow context pattern/class.

### N2 — broader scoped reuse

The same rejected behavior is prohibited across the broader prospectively defined parent context class.

### C — fixed generic heuristic

No user-specific rejection memory. Uses only current-task context and frozen generic rules.

N0/N1/N2 share the same model, base prompt, renderer, rejection record, and critical guardrails. They differ only in the prospectively defined scope at which the explicit negative constraint is allowed to suppress a behavior.

## Primary curve

Report:

`scope of negative reuse -> user control burden -> trajectory integrity`

A useful boundary pattern would be:

- N1 removes repeated corrections without integrity loss;
- N2 removes more burden but begins suppressing behavior in contexts where it should remain available.

This would be a bounded scope/overreach result, not evidence for a new personalization mechanism.

## Immediate next step

Do **not** write implementation code yet.

Create development task families in which:

1. an initial task naturally produces an interaction behavior that the participant can explicitly reject;
2. a later narrow-match task would benefit from remembering `not A`;
3. a broader near-neighbor task should *not* necessarily inherit `not A`;
4. the participant correction can be phrased as a natural current-task rejection rather than an explicit reusable policy declaration;
5. the base model has genuine behavioral variance, so the task is not predetermined.

Then run baseline-skew / burden-opportunity screening. If no task family creates measurable separation among N0/N1/N2/C, stop before implementation.
