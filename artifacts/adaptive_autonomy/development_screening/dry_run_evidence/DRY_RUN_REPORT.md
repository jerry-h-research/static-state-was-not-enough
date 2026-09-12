# Development screening dry-run report

Offline test result: **9 tests passed**, exit code 0. Network connections were blocked during tests. Failure evidence records one preserved fake semantic response followed by a simulated provider failure, with no retry and 118 remaining invocations skipped. These are test fixtures, not screening outputs.

PASS: 12 unique tasks, 10 replicates each, 120 planned calls; **zero model calls executed**.

- PASS: `exact_source_transcription`
- PASS: `twelve_unique_task_ids`
- PASS: `ten_replicates_per_task`
- PASS: `exactly_120_planned_calls`
- PASS: `unique_output_paths`
- PASS: `unique_failure_paths`
- PASS: `only_exact_user_prompt_in_messages`
- PASS: `no_metadata_or_prior_context_in_request`
- PASS: `all_prompt_hashes_recorded`
- PASS: `zero_model_calls`

Prompts are exact transcriptions after removing Markdown blockquote markers and normalizing line endings to LF, with no terminal newline. Hashes use UTF-8 SHA-256. Model input consists only of one user prompt; research metadata stays in the manifest. Each request is independently constructed. No base instruction is added.

Planned provider/model/version: UNCONFIGURED; settings: `{}`. The handoff specifies none. These must be selected and a stateless provider adapter independently reviewed before future live execution. No live adapter is installed.

See `test_results.txt` and `failure_logging_evidence.json` for offline fake-provider validation. Planned raw/error paths are unpopulated; fake outputs are not screening results. The coding sheet has all judgment fields blank. No classifications or dispositions were computed.
