# Negative-First Calibration v0.1 (DRAFT)

**Status:** development candidate; not frozen or implemented.

## 1. Design principle

Do not infer positive reusable preference from silence.

Use explicit negative feedback only to learn **what interaction behavior should not be repeated under a controlled scope**. Among remaining permissible behaviors, use the same generic static current-task heuristic across conditions.

The mechanism is therefore:

`explicit rejection -> exclusion / narrowing constraint -> future choice-set pruning`

not:

`silence -> inferred preference -> stronger autonomous reuse`.

## 2. State schema

Each negative-feedback-derived entry contains only:

- `entry_id`
- `context_class`
- `prohibited_interaction_mode`
- `scope_level`
- `status`
- `exception_flag`
- `revision_of`

Allowed `scope_level` values:

- `EXACT_PATTERN_ONLY`
- `WITHIN_FROZEN_CLASS`

Allowed `status` values:

- `ACTIVE`
- `CONTESTED`
- `RETIRED`

No factual proposition, task answer, raw user prose, or positive preference claim may be stored.

## 3. Creating an exclusion

An exclusion may be created only from explicit participant rejection/correction where the rejected interaction behavior is observable and normalizable under the frozen interaction-mode vocabulary.

The updater records the rejected behavior; it does **not** infer the participant's globally preferred alternative unless that alternative is separately explicit and the protocol prospectively permits it.

## 4. Silence

No response, continuation, or absence of correction causes:

- no scope expansion;
- no confidence increase;
- no positive preference claim;
- no change in exclusion authority.

Silence is logged only for completeness if needed.

## 5. Current-task decision

For each task:

1. apply invariant hard gates (epistemic, authorization, irreversibility, material ambiguity, explicit current instruction);
2. obtain candidate low-risk interaction choices from the frozen decision set;
3. remove choices prohibited by applicable ACTIVE exclusions;
4. let the same static current-task heuristic choose among remaining choices;
5. if exclusions remove all safe candidates, ask/present alternatives rather than inventing a preference.

## 6. Autonomy conditions — development candidate

All conditions receive the same negative-feedback state object and same current-task heuristic.

### L0 — No cross-task exclusion reuse

Negative feedback may correct the current task but does not prune future task choices.

### L1 — Exact-pattern reuse

An ACTIVE exclusion may prune a future choice only when the frozen matcher identifies an `EXACT_PATTERN_ONLY` match.

### L2 — Within-class reuse

An ACTIVE exclusion may prune a future choice anywhere within the same prospectively frozen context class unless an exception/hard gate blocks reuse.

Thus the autonomy dimension is the **scope over which explicit negative feedback may reduce future user control burden**.

## 7. Transfer / exception logic

A useful transfer probe should contain a later task where repeating the explicitly rejected behavior would reasonably recreate the same interaction failure.

An exception probe should contain a near-neighbor task where the previously rejected behavior is valid or preferable.

Success requires reducing repeated correction/control burden on transfer probes **without suppressing the valid behavior on exception probes**.

## 8. Burden accounting

Count both:

- pre-action user control turns (clarification/specification/confirmation);
- post-action repair turns (corrections after wrong interaction choice).

Negative-first calibration is useful only if total burden falls, not merely if the system asks fewer questions while producing more corrections.

## 9. Integrity rule

Any overgeneralized exclusion that blocks an explicitly required, evidence-required, authorization-required, or otherwise gold-valid behavior counts against trajectory integrity. Critical hard-gate failures retain the existing critical-defect treatment.

## 10. What a positive result would mean

A positive bounded result would show only that explicit rejection history, represented as scoped negative constraints, can reduce repeated interaction-control burden without degrading measured trajectory integrity under this protocol.

It would not show:

- that silence encodes preference;
- that the system learned the user's full preferences;
- that ordinary users will provide enough corrective feedback;
- that this mechanism explains the existing long-running interaction;
- novelty relative to all preference-learning literature.

## 11. Why this is worth testing

This design directly tests a conservative version of the motivating behavior: the user need not proactively specify a policy or endorse good outputs; they only reject bad-enough interaction behavior. The system attempts to avoid making the same interaction mistake again.

If even this conservative negative-first mechanism cannot reduce burden without harmful overgeneralization, the case for reducing explicit control through implicit/selective correction becomes substantially weaker.

## 12. Next attack

Before implementation, attack:

- whether `EXACT_PATTERN_ONLY` vs `WITHIN_FROZEN_CLASS` produces a meaningful autonomy curve or merely a matcher benchmark;
- whether exclusions can reduce burden if the static heuristic already avoids repeated errors;
- whether enough repeated interaction opportunities exist without artificially constructing the task sequence;
- whether negative-only calibration can ever capture the motivating improvement pattern, or only prevent recurrence of obvious mistakes;
- whether a simpler cache/blacklist baseline would fully reproduce the effect.
