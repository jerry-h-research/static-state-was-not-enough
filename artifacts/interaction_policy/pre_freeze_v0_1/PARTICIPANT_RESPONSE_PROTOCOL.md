# Participant Response Protocol v0.1 — DRAFT

This protocol constrains the N-of-1 participant during human-facing tasks.

- Begin each task using only the frozen task prompt. Do not volunteer additional explanation unless the task explicitly contains it.
- When the model asks a permitted clarification, answer only the requested dimension using the task's frozen participant-answer record.
- When the model commits to a frozen wrong branch, issue the frozen correction for that task at the first allowed opportunity.
- Do not coach the model toward the experimental hypothesis, mention condition identity, or describe prior policy state.
- Do not reward verbosity or agreement by itself. Judge whether the interaction decision is acceptable under the frozen task record.
- For partially acceptable outputs, follow the task-specific frozen rule: `ACCEPT`, `CORRECT`, or `STOP`.
- Stop immediately if a critical-defect rule requires termination.
- Log any accidental extra information, paraphrase, skipped correction, or protocol deviation. Do not silently repair it.

The exact clarification answers and correction messages must be frozen per task before sealed execution. Material deviations are handled only by the pre-frozen invalidation rule.
