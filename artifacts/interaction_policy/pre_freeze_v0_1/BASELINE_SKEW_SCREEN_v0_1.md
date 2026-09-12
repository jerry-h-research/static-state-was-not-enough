# Baseline-Skew Screen v0.1 — DEVELOPMENT ONLY

Purpose: reject task patterns where a fresh model already strongly prefers the eventual learned behavior, leaving too little room to attribute later behavior to feedback-derived policy state.

## Screen conditions

Use fresh context only. No adaptive state, no participant history, no Condition C heuristic, no prior triad exposure.

For each development prompt in `DEVELOPMENT_TASKS_v0_1.md`, run **10 independent fresh invocations** under the same model/version/settings intended for development.

Normalize the initial interaction behavior to the relevant binary/multiclass choice before any participant correction.

Examples:
- `SUMMARY_FIRST` vs `DETAIL_FIRST`
- `RECOMMEND_ONE_FIRST` vs `PRESENT_OPTIONS_FIRST`
- `MINIMAL_EDIT` vs `BROADER_REWRITE`
- `ASSUME_AND_ACT_WITH_STATED_ASSUMPTION` vs `ASK_FIRST`

## Exclusion rule

A candidate EXPOSURE/TRANSFER pattern is **too baseline-skewed** for sealed use if the fresh baseline selects the eventual learned target mode in **8 or more of 10** invocations.

A candidate is also rejected if the opposite mode appears in 8 or more of 10 invocations and the task wording is judged to strongly cue that mode; the goal is not to reverse-engineer a model quirk but to preserve genuine pre-feedback ambiguity.

Preferred development zone:
- neither competing reasonable mode exceeds 7/10;
- no single wording cue obviously reveals the intended user preference;
- outputs remain codable without reading future correction text.

## Exception-screen rule

For EXCEPTION tasks, the correct exception behavior should be dominant enough to support a defensible gold, but not because the prompt literally negates the learned preference.

Reject an exception candidate if:
- its wording explicitly says “do not follow my usual preference” or equivalent;
- it reveals the experiment structure;
- the gold depends on hidden author intent rather than task semantics;
- correct behavior is ambiguous across reasonable reviewers.

## Condition C check

After fresh-baseline screening, run the fixed static heuristic C on the surviving development tasks.

A triad is a weak candidate if C already reproduces the full desired pattern across EXPOSURE-independent TRANSFER and EXCEPTION behavior without any user-specific feedback.

Such a triad may still serve as a guardrail or usability probe, but it should not be counted as primary evidence of adaptive user-specific learning.

## Output record

For each development task, record:
- task ID;
- model/version/settings;
- 10 normalized fresh-baseline decisions;
- counts by decision class/mode;
- skew disposition: `KEEP`, `REWRITE`, or `DROP`;
- Condition C initial decision;
- reviewer note explaining any rewrite/drop decision.

Development skew results are not final experimental evidence and must be kept separate from sealed results.
