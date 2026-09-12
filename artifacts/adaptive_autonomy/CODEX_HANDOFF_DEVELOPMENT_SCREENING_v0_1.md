# Codex Handoff — Development Screening v0.1

## Scope

Implement **only** the development fresh-model screening harness. Do not implement N0/N1/N2 adaptive persistence yet. Do not redesign the research protocol.

Read these files first:

1. `DEVELOPMENT_SCREENING_PLAN_v0_1.md`
2. `DEVELOPMENT_SCREENING_TASKS_v0_1.md`
3. `DEVELOPMENT_SCREENING_CODING_RUBRIC_v0_1.md`
4. `DEVELOPMENT_TASK_FAMILIES_v0_1.md`
5. `EXPERIMENT_DIRECTION_DECISION_v0_1.md`

## Required implementation

Create a small runner that:

- loads the 12 development prompts from a machine-readable fixture;
- executes each prompt in a fresh isolated model invocation;
- runs exactly 10 invocations per task candidate unless interrupted by provider failure;
- keeps model/version/settings identical across runs;
- disables or avoids cross-run conversation state and user-specific memory;
- stores every raw response separately;
- writes a manifest with task ID, run ID, model/version/settings, timestamp/order, success/failure, and raw-output path;
- never sends target labels, gold labels, family IDs, or coding criteria to the model;
- does not automatically classify outputs using an LLM unless a separate explicitly marked development-only coder is requested later.

## Preferred outputs

```text
artifacts/adaptive_autonomy/development_screening_run_01/
  manifest.jsonl
  config.json
  raw/
    F1-R_01.txt
    ...
  README.md
```

Also create a deterministic helper that emits a blank coding sheet (CSV or JSONL) with the common rubric fields but **does not fill target_behavior_present**.

## Non-goals

Do not:

- implement adaptive memory;
- implement scoped blacklist reuse;
- modify task wording;
- tune prompts after seeing outputs;
- add hidden system prompts intended to make the target behaviors appear;
- decide KEEP/REWRITE/DROP automatically;
- delete failed runs;
- replace inconvenient semantic outputs with reruns.

Provider/infrastructure failures may be retried only if no usable semantic output was returned, and the failed attempt must remain logged.

## Acceptance checks

Before any real API/model run, provide a dry-run mode that proves:

1. all 12 task IDs load;
2. planned invocation count is 120 total;
3. each invocation receives only the intended user prompt plus the shared frozen base configuration;
4. output paths are unique;
5. no prior response is passed to the next invocation;
6. labels/rubric text are absent from model input;
7. failed-attempt logging works.

Return the implementation and dry-run evidence. Do not execute the 120-call screening unless explicitly authorized after review.
