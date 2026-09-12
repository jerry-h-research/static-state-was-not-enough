# Claim Lifecycle — Implementation and Gate Source Snapshot

This public snapshot exposes the final layered engine implementation and the manifest-driven regression-gate source.

## Engine chain
`R12B3 -> R13C1 -> R13C2`

- `source/claim_lifecycle_v0_1_4_18_R12B3.py` — main implementation body.
- `source/claim_lifecycle_v0_1_4_19_R13C1.py` — protects canonical claim-registry identity.
- `source/claim_lifecycle_v0_1_4_20_R13C2.py` — requires strict boolean semantic discriminators at evidence admission.

## Gate source
- `regression_gate/run_gate.py`
- `regression_gate/REGRESSION_MANIFEST.json`
- `regression_gate/regression_result.py`
- `regression_gate/REGRESSION_RESULT_PROTOCOL.md`

## Reproducibility boundary
This is a source snapshot, not a self-contained 23-suite reproduction package. The frozen manifest references historical `tests/` and `phase2_tests/` artifacts that are not included here. Running `run_gate.py` from this snapshot alone is therefore expected to fail on missing suite files.

Published gate outputs and Formal P3.22 Q2 evidence remain the authoritative evidence for the reported bounded results.
