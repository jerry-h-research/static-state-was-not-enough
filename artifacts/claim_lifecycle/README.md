# Claim Lifecycle evidence package

This directory separates four kinds of evidence that should not be conflated:

1. **Concept** — the Personal-AI / interaction-learning framing that motivated the work.
2. **Implementation identity** — the sealed Claim Lifecycle engine chain used at the final checkpoint.
3. **Regression evidence** — a manifest-driven gate covering historical, targeted, adversarial, and application suites.
4. **Downstream usefulness measurement** — Formal P3.22 Q2, where the full System tied a lightweight Baseline 7/7 vs 7/7 (`NO_MEASURABLE_ADVANTAGE`).

## Source chain

The final engine was layered rather than copied into one monolithic file:

`R12B3 -> R13C1 -> R13C2`

See [`source/SOURCE_CHAIN.md`](source/SOURCE_CHAIN.md) for the frozen file identities and dependency relationship.

The executable source bundle is intentionally treated as a separate reproducibility artifact. The research note does not imply that the final 710-byte R13C2 patch is a standalone implementation.

## Regression gate

The frozen regression manifest defined **23 required suites**, including a **69/69 historical baseline aggregate**, and required fail-closed handling for missing or unparseable results. The final gate result was 23/23 PASS with no engine patch required.

See [`regression_gate/GATE_MANIFEST_SUMMARY.md`](regression_gate/GATE_MANIFEST_SUMMARY.md) and [`regression_gate/REGRESSION_RESULT_PROTOCOL.md`](regression_gate/REGRESSION_RESULT_PROTOCOL.md).

## Formal P3.22 Q2

The formal comparison used a frozen behavioral gold and a frozen disposition contract. The contract defined in advance seven unweighted primary checks and the result mapping before execution.

Public evidence:

- [`formal_q2/BEHAVIORAL_GOLD.json`](formal_q2/BEHAVIORAL_GOLD.json)
- [`formal_q2/DISPOSITION_CONTRACT.json`](formal_q2/DISPOSITION_CONTRACT.json)
- [`formal_q2/EVALUATION_RESULT.redacted.json`](formal_q2/EVALUATION_RESULT.redacted.json)

Executed evaluation:

- System: **7/7**
- Baseline: **7/7**
- Disposition: **NO_MEASURABLE_ADVANTAGE**

This does **not** mean the systems are globally equivalent. It means the additional lifecycle machinery did not produce measurable advantage on this prospectively frozen slice.

## Privacy / redaction

Private local filesystem usernames and machine paths are not needed to interpret the public result. Redacted derivatives remove local repository roots. Raw private conversation transcripts are not part of this package.
