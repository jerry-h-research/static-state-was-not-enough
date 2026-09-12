# Adaptive Autonomy — Attack Round 4

**Target:** `DRAFT_NEGATIVE_FIRST_CALIBRATION_v0_1.md`

**Question:** Does negative-first calibration add anything beyond a simple blacklist/cache of rejected behaviors?

## Finding B1 — A blacklist may reproduce the intended benefit

Severity: **HIGH**

If the mechanism is only:

`user rejects behavior A -> do not use A again in similar tasks`

then a fixed per-user blacklist indexed by context class may be sufficient. This would make a richer adaptive-autonomy mechanism unnecessary.

**Required comparison:** add a minimal blacklist baseline that stores only:

- frozen context-class ID;
- prohibited interaction mode;
- optional narrow exception tag;
- active/inactive flag.

No confidence, no preference inference, no positive learning, no free-form rationale.

## Finding B2 — “Contextual reuse” is where complexity can sneak back in

Severity: **HIGH**

A blacklist appears simple only if context matching is already solved. If a learned rejection requires a sophisticated classifier to determine applicability, the complexity has merely moved into the matcher.

**Required repair:** the adaptive and blacklist conditions must share the exact same frozen context/applicability function. The only allowed difference is how each condition uses negative evidence after matching.

## Finding B3 — Negative-first can become equivalent to blacklist plus exception list

Severity: **HIGH**

If every correction either adds a prohibition or adds an exception, the mechanism may collapse to:

`blacklist + scoped exceptions`.

That is not a failure; it is a simpler explanation.

**Kill rule:** if the minimal blacklist+exception baseline matches burden and integrity, prefer it and retire the more complex mechanism for this study.

## Finding B4 — A blacklist can overgeneralize just as badly

Severity: **MEDIUM**

A broad rejection such as “don’t ask me this every time” can be incorrectly applied in tasks where clarification becomes materially necessary.

This means the key test is not whether a blacklist remembers rejection, but whether **scope and hard gates prevent a past negative from suppressing a necessary future question**.

**Required probes:** include near-neighbor tasks where the formerly rejected behavior becomes correct/required because task conditions change.

## Finding B5 — “Do not repeat the rejected behavior” may fail when multiple alternatives exist

Severity: **MEDIUM**

Rejecting A does not identify which of B/C/D should replace it. A blacklist only removes A; a richer policy might rank alternatives.

However, if the task can be solved adequately by eliminating A and letting the base model choose among the rest, the blacklist remains sufficient.

**Required measurement:** do not credit richer adaptation unless it reduces burden or wrong branches beyond blacklist elimination alone.

## Finding B6 — Correction semantics can leak the preferred answer

Severity: **HIGH**

If the participant says “don’t do A; do B instead,” then both adaptive and blacklist mechanisms effectively receive an explicit positive instruction. The experiment would no longer isolate negative-first calibration.

**Required task design:** distinguish:

- **pure rejection:** “not A” / “don’t do that here”;
- **rejection with replacement:** “not A, use B.”

Primary negative-first evidence should include pure-rejection cases where the system must avoid repeating the known bad path without being handed a reusable positive policy.

## Finding B7 — Negative-first may reduce repeat mistakes without reducing control burden

Severity: **HIGH**

Avoiding a previously rejected path is useful, but if the system then asks the user what to do every time, correction recurrence falls while total control burden does not.

**Interpretation rule:** repeat-error reduction is secondary. The branch is practically useful only if total control burden falls without integrity loss versus both explicit-control and blacklist baselines.

## Finding B8 — The blacklist baseline should be promoted to a first-class comparator

Severity: **HIGH**

The prior static comparator C is too generic for this specific mechanism question.

**Required design:** use at least:

- `L0` — explicit-control / no cross-task reuse;
- `BL` — minimal scoped blacklist from explicit rejection;
- `AA` — negative-first adaptive mechanism, if it differs materially from BL;
- optional generic static heuristic comparator only if it answers a separate question.

## Round-4 disposition

**NEGATIVE-FIRST DOES NOT YET JUSTIFY A DISTINCT MECHANISM.**

The current idea may collapse to a scoped blacklist, and that outcome should be welcomed rather than engineered around. The next design step is to define the smallest blacklist comparator first, then specify exactly one capability the adaptive mechanism has that the blacklist does not. If no such capability produces measurable benefit under matched scope/hard gates, stop at the blacklist.
