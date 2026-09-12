# Final regression-gate manifest summary

Checkpoint: `v0.1.4.21-P3S3`  
Sealed engine: `src/claim_lifecycle_v0_1_4_20_R13C2.py`

The frozen manifest required **23 suites**. Categories included historical baseline, targeted regressions, adversarial regressions, and an application-level revision-provenance contract.

## Historical baseline

The four historical baseline suites were required to aggregate to:

- passed: **69**
- total: **69**
- failed: **0**

Historical artifacts were not rewritten. Older suites were retargeted in memory to the current engine where required.

## Later targeted/adversarial coverage

The manifest includes targeted or adversarial coverage for:

- A1-A4 targeted regressions
- ownership isolation
- terminal/revision behavior
- state-machine/metamorphic attacks
- cross-claim/cross-lifecycle contamination
- history/provenance laundering
- duplicate-source consistency
- authoritative monotonic store time
- evidence-ID authority
- active source-revocation discovery
- finite numeric evidence admission
- canonical claim-registry authority
- strict boolean-domain evidence admission
- Phase 3 Stage 3 revision-provenance contract

## Global requirements

- all suites required: **true**
- suite count: **23**
- fail closed on missing/unparseable result: **true**
- historical baseline aggregate: **69/69**
- final gate requirement: PASS / checkpoint remains green / no engine patch required

The corresponding final gate result reported **23/23 suites PASS**.

The full frozen manifest is intentionally not paraphrased as a new result; this file is a public navigation summary of the machine manifest used at the final checkpoint.
