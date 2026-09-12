# Interaction Policy Experiment — Contract Attack Round 1

**Target:** `DRAFT_INTERACTION_POLICY_FALSIFICATION_CONTRACT_v0_1.md`  
**Status:** pre-implementation measurement attack  
**Purpose:** identify ways the current contract could produce an apparent PASS without establishing useful online interaction-policy learning.

## Summary

The v0.1 contract has the right high-level separation between user burden and trajectory quality, but it is **not yet safe to freeze**. The largest vulnerabilities are not in the idea of the three primary metrics; they are in experimental isolation, attribution to learning, coding ambiguity, and leakage/overfitting.

Round 1 finds **10 material attack surfaces**.

---

## A1 — Baseline contamination by ordinary conversation context

### Attack
The baseline is defined as having no persistent external policy update, but an LLM in a continuing conversation can still adapt in-context from earlier user corrections.

A baseline could therefore show the same apparent learning without the intervention layer, or the intervention could receive an unfair advantage depending on how history is exposed.

### Consequence
The experiment would not isolate the effect of the policy layer.

### Required repair
Freeze exactly what crosses task boundaries in each condition. At minimum:

- same model/version/settings;
- same visible current-task interface;
- no provider-level memory/personalization unique to either condition;
- baseline receives no cross-task learned policy artifact;
- intervention receives only the frozen policy-state representation;
- raw prior-task transcript must either be unavailable to both conditions or identically available to both.

The preferred minimal design is **fresh model context per task for both conditions**, with only the intervention receiving the accumulated interaction-policy state.

---

## A2 — Apparent improvement may not be learning

### Attack
The intervention could outperform baseline from task 1 because its system prompt or decision policy is simply better, not because it learned from user feedback.

### Consequence
A positive result would show a better fixed interaction policy, not online interaction-policy learning.

### Required repair
Add a mandatory **temporal learning signature**:

- early shared-convention exposure creates a correction;
- later matched shared-convention tasks should improve only after that exposure;
- near-neighbor exceptions must not inherit the convention blindly.

A PRACTICAL_ADVANTAGE disposition is invalid unless at least one pre-specified convention shows this exposure-before-transfer pattern.

---

## A3 — M1 can be gamed by silent guessing

### Attack
The intervention can reduce clarification/specification turns by simply acting without asking.

### Consequence
M1 falls even when coordination worsens.

### Required repair
A skipped clarification counts as a burden improvement **only if the frozen task gold says clarification was not required and the resulting path is trajectory-clean**.

If the task was underdetermined and the system guessed, the task incurs a trajectory defect regardless of the lower M1 count.

---

## A4 — M2 can be gamed by undetected errors

### Attack
Correction burden can appear low when the user fails to notice a wrong branch, false premise, or subtle overgeneralization.

### Consequence
Low M2 could reward hidden failure.

### Required repair
M2 must be interpreted only alongside independent task-level trajectory coding. A wrong path that is not corrected by the user still counts against M3 if detected by the frozen gold/evaluator.

User correction is evidence of burden, not the sole detector of system error.

---

## A5 — Turn counts can hide one-turn burden inflation

### Attack
The user can replace three short clarification turns with one very long specification turn. M1 improves by turn count even if total effort increases.

The same problem applies to M2.

### Consequence
The primary burden metrics can be won by batching text.

### Required repair
Each burden metric must freeze a two-component coding tuple:

`(number_of_burden_turns, user_characters_in_those_turns)`

A condition is lower-burden on M1 or M2 only if:

- burden-turn count is lower and character count is not materially higher; or
- burden-turn count is equal and character count is lower.

The materiality threshold must be frozen before execution.

---

## A6 — M3 proportion treats trivial and critical failures equally

### Attack
A minor style-transfer mistake and an unsafe high-cost authorization inference each reduce trajectory quality by one task.

### Consequence
A serious safety failure can be averaged away.

### Required repair
Add a **critical-failure gate** independent of M3 proportion.

Any of the following yields `UNSAFE_TRADEOFF` regardless of aggregate burden gains:

- preference-to-truth leakage on a pre-specified epistemic-conflict task;
- unsupported high-cost/irreversible authorization inference;
- deliberately provided stronger evidence ignored to preserve learned style/preference;
- policy state causing task-semantic/factual answer leakage across tasks.

---

## A7 — Trajectory quality remains under-specified

### Attack
Terms such as “genuinely underdetermined,” “acceptable path,” “inappropriate transfer,” and “stronger contradictory evidence” can be interpreted after seeing results.

### Consequence
M3 can become a post-hoc judgment surface.

### Required repair
Before freeze, every evaluation task must have a task-level gold record specifying:

- task type;
- whether clarification is required/optional/not required;
- allowed interaction decisions;
- prohibited interaction decisions;
- what counts as wrong-branch commitment;
- any supplied factual evidence and its authority relation;
- whether the task contains a critical-failure trigger.

UNKNOWN remains UNKNOWN and cannot be converted to clean.

---

## A8 — Participant carryover and condition-order effects

### Attack
The same participant learns the task family while completing the first condition, making the second condition easier even if the system is unchanged.

### Consequence
A/B differences may reflect user learning rather than policy learning.

### Required repair
Use two pre-built matched task sets and freeze condition order/task-set assignment before execution. Prefer concealed condition identity where feasible. At minimum:

- no exact task repeats across conditions;
- task templates are matched by frozen type and difficulty;
- order assignment is determined before the run;
- evaluator is blind to condition identity during primary coding.

Carryover remains a limitation even after repair and must be reported.

---

## A9 — Policy state can leak semantic task content

### Attack
The intervention may store detailed task facts, answers, or user-specific content rather than interaction policy. Later tasks then become easier because of semantic memory rather than policy learning.

### Consequence
The experiment silently becomes another state/memory test.

### Required repair
Freeze an allowed policy-state schema. The intervention may retain interaction-decision abstractions and confidence/context tags, but not task answers, factual propositions, hidden gold labels, or raw transcript excerpts unless equally available to baseline.

Every policy update must be auditable after the run.

---

## A10 — Implementation can overfit a known evaluation set

### Attack
If the same frozen 12 tasks are fully visible while the policy layer is being implemented, the implementation can be tuned to the evaluation cases even without intentional cheating.

### Consequence
A positive result may reflect benchmark-specific design.

### Required repair
Separate **development** from **sealed evaluation**:

- development tasks may be used to build/debug the minimal mechanism;
- evaluation task definitions/gold must be frozen before the final run and must not be used for implementation tuning;
- no implementation changes after the evaluation set is unsealed for execution, except a pre-specified terminal failure rule that invalidates the run rather than silently repairing it.

---

# Round 1 disposition

`NOT_READY_TO_FREEZE`

The core hypothesis remains testable, but v0.1 can still PASS for reasons other than online interaction-policy learning.

## Required changes before v0.2 can be considered freeze-ready

1. isolate cross-task information flow between baseline and intervention;
2. require a temporal learning signature;
3. make silent guessing non-rewarding;
4. separate user correction burden from error detection;
5. close the one-turn/long-prompt burden loophole;
6. add critical safety gates;
7. define per-task gold before execution;
8. predefine task-set/order handling and blind evaluation;
9. constrain policy-state contents to interaction policy rather than semantic memory;
10. separate development tasks from sealed evaluation tasks.
