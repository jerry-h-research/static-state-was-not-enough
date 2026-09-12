# Methods and Evidence Discipline

This is an exploratory longitudinal N-of-1 research package, not a population study.

## Evidence controls used
- Prospective freeze rules before key comparisons.
- Independent review at multiple design/implementation stages.
- Separation of engineering correctness from downstream usefulness.
- Frozen one-shot Formal P3.22 Q2 comparison.
- PCB-1 blind quality evaluation and blind primary event coding before mapping reveal.
- UNKNOWN/missing evidence was not converted into PASS.
- Negative/null results were preserved rather than post-hoc rescued.
- A later research liquidation classified claims as SUPPORTED, NEGATIVE, OPEN, NOT_WORTH_TESTING_NOW, or RETIRED.

## Public-release policy
v0.3 intentionally excludes raw private transcripts, personal identifiers, account details, local machine paths, third-party information, and the full historical test corpus. The public package exposes aggregate/frozen outcomes, bounded engineering summaries, selected formal evaluation artifacts, a layered Claim Lifecycle implementation/gate source snapshot, and an explicitly historical concept diagram.

The source snapshot is not represented as a self-contained reproduction package because the frozen regression manifest references omitted historical `tests/` and `phase2_tests/` files.

## Interpretation rule
A result marked ENGINEERING-VERIFIED does not imply product usefulness. A naturalistic observation does not imply causal generalization. A null result is not equivalence outside the tested slice. A historical concept artifact is not a validated architecture.
