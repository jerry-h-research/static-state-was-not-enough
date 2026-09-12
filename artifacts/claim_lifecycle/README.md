# Claim Lifecycle evidence package

Claim Lifecycle was a bounded prototype for a specific long-horizon failure mode: **a model-generated interpretation can remain coherent, be repeatedly reused, and gradually acquire behavior-governing authority without acquiring independent evidence.** The design goal was therefore not simply to remember more. It was to preserve the difference between what was said, who or what introduced it, what evidence supports it, whether that evidence remains valid, and whether a claim is still safe to reuse.

At the implementation level, the prototype tracked claim provenance and semantic status; evidence identity, source identity, scope, freshness, entailment, and invalidation; revision relationships; dependency graphs; contradiction and re-audit state; and restrictions on reuse of quarantined or terminal claims. Repetition, AI agreement, user endorsement, and premise reuse were deliberately kept separate from independent evidential support.

This directory separates four kinds of evidence that should not be conflated:

1. **Historical concept** — the earlier Personal-AI / interaction-learning framing that motivated the work. It is context, not validated architecture.
2. **Implementation** — the final layered Claim Lifecycle engine snapshot (`R12B3 -> R13C1 -> R13C2`).
3. **Regression evidence** — a manifest-driven gate covering historical, targeted, adversarial, and application suites.
4. **Downstream usefulness measurement** — Formal P3.22 Q2, where the full System tied a lightweight Baseline 7/7 vs 7/7 (`NO_MEASURABLE_ADVANTAGE`).

The important distinction is:

> **Engineering integrity was tested separately from downstream usefulness.**

A prototype can survive adversarial regression and still fail to show additional practical value over a simpler baseline. That is what happened here.

## 1. Historical concept

The English reconstruction of the early **Personal AI — Interaction Learning Architecture v0.1** diagram is available in [`historical_concept/`](historical_concept/).

It predates the later Claim Lifecycle experiments and should **not** be interpreted as experimental evidence or a validated architecture. Its role is to show the earlier framing: temporary user/interaction/claim state, provenance, evidence checking, re-audit, and an explicit error-amplification path.

## 2. Implementation snapshot

The final engine was layered rather than copied into one monolithic file:

`R12B3 -> R13C1 -> R13C2`

The public implementation and gate source snapshot is here:

[`claim_lifecycle_implementation_gate_source_snapshot_v1/`](claim_lifecycle_implementation_gate_source_snapshot_v1/)

The snapshot contains the three engine files plus the gate runner, frozen regression manifest, structured-result helper, and result protocol. It is intentionally labeled a **source snapshot**, not a self-contained reproduction package: the historical `tests/` and `phase2_tests/` corpus referenced by the manifest is not included.

For the dependency relationship and frozen identities, also see [`source/SOURCE_CHAIN.md`](source/SOURCE_CHAIN.md).

## 3. Regression gate

The frozen regression manifest defined **23 required suites**, including a **69/69 historical baseline aggregate**, and required fail-closed handling for missing or unparseable results. The final gate result was **23/23 PASS** with no engine patch required.

Public gate documentation:

- [`regression_gate/GATE_MANIFEST_SUMMARY.md`](regression_gate/GATE_MANIFEST_SUMMARY.md)
- [`regression_gate/REGRESSION_RESULT_PROTOCOL.md`](regression_gate/REGRESSION_RESULT_PROTOCOL.md)
- gate source inside the [implementation snapshot](claim_lifecycle_implementation_gate_source_snapshot_v1/regression_gate/)

These results support bounded engineering claims only. They do not by themselves establish that the machinery improves user-facing outcomes.

## 4. Formal P3.22 Q2 — downstream usefulness

The formal comparison asked a narrower question: **when semantic candidate input is held constant, does the full lifecycle-governance System produce more downstream utility than a lightweight Baseline?**

The comparison used a frozen behavioral gold and frozen disposition contract before execution. The disposition rule treated equal primary-check counts as `NO_MEASURABLE_ADVANTAGE`; equality was not defined as global equivalence.

Public evidence:

- [`formal_q2/BEHAVIORAL_GOLD.json`](formal_q2/BEHAVIORAL_GOLD.json)
- [`formal_q2/DISPOSITION_CONTRACT.json`](formal_q2/DISPOSITION_CONTRACT.json)
- [`formal_q2/EVALUATION_RESULT.redacted.json`](formal_q2/EVALUATION_RESULT.redacted.json)

Executed evaluation:

- System: **7/7**
- Baseline: **7/7**
- Disposition: **NO_MEASURABLE_ADVANTAGE**

The lightweight Baseline preserved enough origin, qualification, evidence metadata, latest-value replacement, and response-time epistemic caution to satisfy the same seven primary checks in this slice.

This is the critical negative result of the Claim Lifecycle branch:

> **More elaborate semantic governance did not produce measurable downstream advantage on the frozen Q2 slice.**

That result is one reason the broader project moved away from assuming that a more sophisticated static state architecture was the missing answer.

## 5. Capability-access note

The participant-author reports no prior programming background sufficient to independently implement this prototype. The project nevertheless produced executable code, regression/adversarial tests, reviewed repairs, frozen evaluation contracts, and machine evidence through a human-AI-tool workflow.

This is an N-of-1 capability-access observation, **not** evidence that programming expertise is unnecessary and not a controlled estimate of productivity uplift.

## 6. Privacy and interpretation boundary

Private local filesystem usernames, machine paths, raw private conversation transcripts, screenshots, account details, and third-party personal information are not part of this public package. Where needed, public Q2 derivatives redact local repository roots.

Do not infer from this package that:

- Claim Lifecycle is a general solution to long-term AI memory or alignment;
- the 23-suite gate establishes downstream usefulness;
- the 7/7 tie establishes global System/Baseline equivalence;
- the historical concept diagram is a validated architecture;
- the source snapshot alone reproduces the full historical gate without the omitted test corpus.
