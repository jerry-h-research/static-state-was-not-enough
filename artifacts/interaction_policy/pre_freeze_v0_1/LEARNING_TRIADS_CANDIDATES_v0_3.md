# Learning Triads — Development Candidates v0.3

**Status: DRAFT DEVELOPMENT MATERIAL. Not sealed tasks.**

## Interpretation boundary

These triads do **not** test a novel model-internal learning mechanism. They test whether **feedback-derived external interaction-policy state** can selectively change later decisions and reduce user operating burden beyond fresh and static-heuristic baselines.

Two families are included:

- presentation/editing conventions;
- interaction-control conventions.

For every triad, both modes are reasonable before exposure. The exposure selects the participant-specific convention. Exception probes must disable transfer through context, not by explicitly saying “ignore my preference this time.”

## Triad P1 — Compression level

**Context class:** `FORMAT_SELECTION`
**Modes:** `SUMMARY_FIRST` vs `DETAIL_FIRST`

- **EXPOSURE:** a routine review task where both concise-first and detail-first responses are acceptable. Frozen feedback selects `SUMMARY_FIRST`.
- **TRANSFER:** a different routine review task with comparable stakes and complexity. Learned behavior should begin concise and expand only if needed.
- **EXCEPTION:** a task whose purpose is archival/audit completeness rather than quick decision support. The prompt does not explicitly mention the prior preference. Gold favors detail sufficient for auditability; blindly compressing is inappropriate transfer.

## Triad P2 — Edit scope

**Context class:** `ANALYSIS_VS_ACTION`
**Modes:** `MINIMAL_EDIT` vs `BROADER_REWRITE`

- **EXPOSURE:** a low-risk writing/code cleanup where either local repair or broader rewrite is acceptable. Frozen feedback selects minimal edit when the requested problem can be fixed locally.
- **TRANSFER:** a different artifact with a local defect and no architectural reason to rewrite. Learned behavior should preserve unaffected structure.
- **EXCEPTION:** an artifact where the defect is caused by a cross-cutting structural inconsistency and local patching would leave the stated acceptance criteria unmet. Gold favors broader rewrite/restructure based on task structure, without an explicit override sentence.

## Triad I1 — Recommendation initiative

**Context class:** `OPTION_PRESENTATION`
**Modes:** `RECOMMEND_ONE_FIRST` vs `PRESENT_OPTIONS_FIRST`

- **EXPOSURE:** a low-stakes choice with several defensible options. Frozen feedback selects one best recommendation first, with alternatives only if materially useful.
- **TRANSFER:** another low-stakes choice with enough information to make a defensible recommendation. Learned behavior should recommend one first.
- **EXCEPTION:** a choice where the available information supports two materially different options tied to unresolved user priorities, but neither priority is objectively dominant. Gold favors `ALTERNATIVES` rather than pretending one option is best. The task does not explicitly request multiple options.

## Triad I2 — Low-risk ambiguity handling

**Context class:** `CLARIFY_SCOPE`
**Modes:** `ASSUME_AND_ACT_WITH_STATED_ASSUMPTION` vs `ASK_FIRST`

- **EXPOSURE:** a reversible, low-cost task with two plausible interpretations that lead to harmless, easily reversible outputs. Frozen feedback selects assume-and-act with the assumption stated.
- **TRANSFER:** another reversible low-cost task with the same ambiguity structure. Learned behavior should act under a visible assumption rather than impose clarification burden.
- **EXCEPTION:** a superficially similar task where the unresolved interpretation changes an externally consequential or difficult-to-reverse outcome. Gold requires `ASK`/`DEFER` under the generic guardrail. No explicit “ask me first” instruction appears.

## Mechanism claim if these succeed

Maximum supported mechanism statement:

> Under the frozen protocol, feedback-derived external policy state altered later interaction decisions in a scope-sensitive direction beyond artifact-presence/no-state controls.

Not supported:

- the model internally learned the user;
- the mechanism is novel relative to existing personalization research;
- the state reconstructs long-running human-AI coordination;
- preference memory alone explains the original longitudinal phenomenon.

## Pre-seal rejection rule

Before sealed-task authoring, reject any candidate pattern if development-only probes show that:

- one mode is chosen overwhelmingly by fresh/static baselines without user feedback;
- exception status requires an explicit preference override to be obvious;
- the policy cannot be represented without task-semantic leakage;
- the exposure feedback reveals future test structure;
- the triad primarily tests factual correctness or generic safety rather than interaction convention.
