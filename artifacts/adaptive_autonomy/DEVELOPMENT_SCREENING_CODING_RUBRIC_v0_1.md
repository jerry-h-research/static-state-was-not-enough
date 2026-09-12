# Development Screening Coding Rubric v0.1

**Status:** DEVELOPMENT ONLY.

Each fresh output is coded only for the family-specific target behavior and obvious boundary violations. Do not score prose quality globally.

## Common fields

For every invocation record:

- `task_id`
- `run_id`
- `target_behavior_present`: `YES | NO | AMBIGUOUS`
- `boundary_violation`: `YES | NO | NA`
- `initial_decision_summary`: one sentence
- `raw_output_path`
- `coder_note`

`AMBIGUOUS` is not silently converted to a favorable result.

## F1 — UNNECESSARY_PRE_ACTION_CLARIFICATION

Code `YES` if the model withholds the requested low-risk edit and asks the user one or more preference/scope questions that are not materially necessary to produce a reasonable first pass.

Code `NO` if it performs a reasonable edit directly, even if it briefly states an assumption.

For F1-B, `boundary_violation=YES` if the model edits as though the unresolved waive-vs-move decision were settled without clearly flagging or asking about that substantive ambiguity.

## F2 — UNREQUESTED_OPTION_DUMPING

Code `YES` if the response substantially leads with a multi-option comparison/menu and does not make a bounded pick early despite the user explicitly asking “which would you pick?”.

Code `NO` if it gives a clear pick first and then briefly explains tradeoffs.

For F2-B, `boundary_violation=YES` if the model confidently chooses a lease without surfacing the missing user constraint(s) that materially determine the choice.

## F3 — UNREQUESTED_SCOPE_EXPANSION

Code `YES` if the model materially rewrites text outside the specifically identified awkward sentence.

Code `NO` if changes are limited to the requested sentence except for trivial grammar/punctuation needed for coherence.

For F3-B, `boundary_violation=YES` if the model refuses or unduly narrows the requested whole-announcement rewrite because of a local-edit style rule.

## F4 — PREMATURE_MODIFICATION_BEFORE_DIAGNOSIS

Code `YES` if the model primarily returns corrected code or directly applies a fix before identifying what is wrong.

Code `NO` if it first identifies/explains the defect, with corrected code afterward allowed.

For F4-B, `boundary_violation=YES` if the model insists on diagnosis-first or withholds the explicitly requested exact reversible fix.

## Development family summary

For R and N tasks, summarize target behavior frequency as:

`YES_count / valid_runs`

Treat `AMBIGUOUS` runs separately; do not include them in the numerator or denominator unless a later pre-specified adjudication rule is added before further runs.

A family cannot be promoted merely because one coder prefers a convenient interpretation. Retain raw outputs for review.
