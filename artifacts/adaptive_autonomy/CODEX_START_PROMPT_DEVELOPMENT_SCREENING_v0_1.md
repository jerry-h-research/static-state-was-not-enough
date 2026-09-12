# Codex Start Prompt — Development Screening v0.1

Use the repository `jerry-h-research/static-state-was-not-enough`.

Read these files in full before changing anything:

1. `artifacts/adaptive_autonomy/CODEX_HANDOFF_DEVELOPMENT_SCREENING_v0_1.md`
2. `artifacts/adaptive_autonomy/DEVELOPMENT_SCREENING_TASKS_v0_1.md`
3. `artifacts/adaptive_autonomy/DEVELOPMENT_SCREENING_CODING_RUBRIC_v0_1.md`
4. `artifacts/adaptive_autonomy/DEVELOPMENT_SCREENING_PLAN_v0_1.md`
5. `artifacts/adaptive_autonomy/EXPERIMENT_DIRECTION_DECISION_v0_1.md`

## Authorized action only

Implement the **development fresh-model screening runner** and produce a **dry-run evidence package**.

Do **not** execute the 120 model calls yet.
Do **not** implement N0/N1/N2 adaptive reuse.
Do **not** modify task wording, coding rubric, thresholds, gold logic, or research design.
Do **not** add personalization/memory across invocations.

## Runner requirements

The runner must:

- load exactly the 12 development task prompts from the task file or from a generated machine-readable task file whose contents are an exact transcription;
- schedule exactly 10 fresh invocations per task (`12 x 10 = 120` planned calls);
- guarantee fresh isolated context for every invocation;
- send only the task prompt plus one identical frozen base instruction if required by the provider interface;
- never send coding rubric, family labels, target-negative-behavior labels, expected classifications, or research hypotheses to the model;
- record model name/version/settings, task ID, replicate ID, prompt hash, timestamp/order, success/failure status, and output path;
- save every raw output separately without overwriting previous outputs;
- log provider/API failures separately from semantic outputs;
- support `--dry-run` that makes zero model calls and instead validates the complete schedule and paths;
- default to dry-run or otherwise require an explicit execution flag for live calls.

## Required dry-run evidence

Produce machine-readable and human-readable evidence showing:

- 12 unique task IDs loaded;
- 10 replicates scheduled for each task;
- exactly 120 total planned calls;
- zero calls executed in dry-run;
- output paths are unique for all 120 scheduled calls;
- no prior-task conversation/context is passed between calls;
- no rubric/gold/target labels appear in model input;
- all task prompt hashes are recorded;
- planned model/settings are printed but no live request is sent.

## Files to return

Return at minimum:

- the runner source code;
- machine-readable task manifest if one is generated;
- dry-run manifest/output;
- `DRY_RUN_REPORT.md` summarizing validation results;
- any unit tests or validation script used to prove the runner obeys the scope.

Place development runner artifacts under a clearly named development directory; do not overwrite research-design documents.

## Stop condition

After the dry-run evidence package is complete, **stop**. Do not run live screening calls until the dry-run package has been independently reviewed and explicit authorization is given.

In your final response, report exactly what files you created/changed, the dry-run validation result, and any unresolved blocker. Do not claim screening results because no live calls are authorized in this step.
