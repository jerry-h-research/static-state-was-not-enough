# Claim Lifecycle — Public Engineering Summary

Claim Lifecycle was a bounded semantic-state integrity prototype for tracking provenance, epistemic status, authority, revision/invalidation, derivation lineage, independent roots, scope/version, reuse eligibility, and stale descendants.

## Bounded evidence ladder

- Architecture correctness: **STRONG BOUNDED EVIDENCE**
- Minimum legal usefulness: **ESTABLISHED**
- Assertion-authority advantage: **OBSERVED in R06**
- Target binding: **INDEPENDENT FAILURE SURFACE ESTABLISHED**
- Wrong valid target propagation: **ESTABLISHED at oracle-normalized adapter level**
- P3.22 Mode-A implementation qualification: **COMPLETE through C1-R2**

## Evidence drill-down

Start with the [Claim Lifecycle evidence index](README.md). It separates the conceptual origin, implementation chain, regression gate, and Formal P3.22 Q2 downstream measurement.

Key public evidence now includes:

- [Formal Q2 behavioral gold](formal_q2/BEHAVIORAL_GOLD.json)
- [Formal Q2 disposition contract](formal_q2/DISPOSITION_CONTRACT.json)
- [Formal Q2 evaluation result](formal_q2/EVALUATION_RESULT.redacted.json)
- [Regression-gate manifest summary](regression_gate/GATE_MANIFEST_SUMMARY.md)
- [Structured regression-result protocol](regression_gate/REGRESSION_RESULT_PROTOCOL.md)

## Capability-access note

The participant-author reports no prior programming background sufficient to independently implement this prototype. The human-AI-tool workflow nevertheless produced executable code, tests, reviewed repairs, evaluation contracts, and machine evidence.

This is a case report, not a controlled claim that programming expertise is unnecessary.

## Critical negative result

When downstream usefulness was finally tested in Formal P3.22 Q2, the full System tied the lightweight Baseline **7/7 vs 7/7**. Engineering sophistication therefore cannot be treated as evidence of additional user-facing utility.
