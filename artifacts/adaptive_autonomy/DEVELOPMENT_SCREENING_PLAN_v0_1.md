# Development Screening Plan v0.1

**Status:** DEVELOPMENT ONLY. This screening is not a confirmatory experiment and cannot support final claims.

## Goal

Before writing the adaptive implementation, test whether candidate task families provide enough natural model variance and user-control burden opportunity to justify a sealed experiment.

## Stage A — Fresh-model behavior screen

For each candidate family member (`R`, `N`, `B`), run repeated fresh invocations with identical model/version/settings and no user-specific memory.

Development target: **10 fresh invocations per task candidate**.

Code each initial interaction decision for whether the family-specific target negative behavior occurred.

Record raw outputs; do not keep only counts.

## Stage B — Family disposition

### REJECTION task R

- `0–1 / 10` target behavior: **DROP/REWRITE** — rejection cannot arise naturally enough.
- `2–7 / 10`: **USABLE DEVELOPMENT RANGE**.
- `8–10 / 10`: **SKEWED** — may still be useful for burden testing, but poor for demonstrating model-choice variance; rewrite preferred.

### NARROW_MATCH task N

- `0–1 / 10` target behavior: **DROP/REWRITE** — memory cannot save meaningful repeated correction burden.
- `2–7 / 10`: **USABLE DEVELOPMENT RANGE**.
- `8–10 / 10`: **HIGH BURDEN OPPORTUNITY but strongly skewed** — retain only if C is also challenged and sealed interpretation is explicitly bounded.

### BROAD_NEAR_NEIGHBOR task B

The prospective gold must say whether suppressing the target behavior would be inappropriate. Fresh behavior frequency is descriptive; the key requirement is that the boundary can be coded before adaptive outputs are seen.

## Stage C — Control-burden opportunity estimate

For each surviving family, estimate the maximum number of participant control/correction turns that N1 could plausibly save relative to N0 across the planned sequence.

If the complete surviving set offers fewer than **4 total prospective repeated-control opportunities**, the current experiment is likely underpowered even as an N-of-1 feasibility test and should be redesigned or stopped before implementation.

The value 4 is a development stop heuristic, not a statistical threshold and must not be presented as inferential significance.

## Stage D — Static comparator challenge

Before adaptive implementation, run the frozen-candidate static heuristic C conceptually or through a development runner on surviving N/B tasks.

If C avoids the target negative behavior on nearly all narrow-match tasks while respecting all broad boundaries, the adaptive blacklist has little practical room to add value. Record this as a reason to stop or redesign rather than weakening C.

## Development-only nature

Task wording may change during screening. Therefore screening outputs are contaminated for confirmatory use. Any final sealed task must be a new or independently authored descendant, frozen with gold before confirmatory execution.

## Stop rules before implementation

Stop the branch or redesign before code if any of these occurs:

1. fewer than two task families survive basic screening;
2. total repeated-control opportunity is too small to produce a meaningful burden comparison;
3. broad boundaries cannot be prospectively coded without subjective post-hoc judgment;
4. static heuristic C removes nearly all available burden while preserving boundaries;
5. natural participant corrections necessarily reveal reusable future policy rather than current-task rejection;
6. stored negative constraints require task-semantic content or factual answers to work;
7. literature collision check identifies an exact prior protocol sufficient for the current narrow question.

Passing development screening only authorizes implementation work. It is not evidence that negative-feedback reuse is beneficial.
