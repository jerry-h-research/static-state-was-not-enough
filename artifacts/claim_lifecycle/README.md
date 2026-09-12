# Claim Lifecycle evidence package

This directory separates four different kinds of evidence that should not be conflated:

1. **Concept** — the original Personal-AI / interaction-learning framing that motivated the work.
2. **Implementation** — the sealed Claim Lifecycle engine chain used at the final checkpoint.
3. **Regression evidence** — a manifest-driven gate covering historical, targeted, adversarial, and application suites.
4. **Downstream usefulness measurement** — Formal P3.22 Q2, where the full System tied a lightweight Baseline 7/7 vs 7/7 (`NO_MEASURABLE_ADVANTAGE`).

## Source chain

The final engine was layered rather than copied into one monolithic file:

`R12B3 -> R13C1 -> R13C2`

- `source/claim_lifecycle_v0_1_4_18_R12B3.py` — main implementation body.
- `source/claim_lifecycle_v0_1_4_19_R13C1.py` — protects canonical claim-registry identity.
- `source/claim_lifecycle_v0_1_4_20_R13C2.py` — enforces strict boolean semantic discriminators at evidence admission.

The two small final patches are included here first. The larger R12B3 source and gate runner are tracked in the public-release audit as large raw artifacts to be added without changing their semantics.

## Regression gate

The frozen regression manifest defined **23 required suites**, including a **69/69 historical baseline aggregate**, and required fail-closed handling for missing or unparseable results. The final gate result was 23/23 PASS with no engine patch required.

The structured-result protocol was introduced so newer adversarial suites could emit machine-readable results instead of relying only on prose parsing.

## Formal P3.22 Q2

The formal comparison used a frozen behavioral gold and a frozen disposition contract. The contract defined in advance:

- seven unweighted primary checks;
- equal pass counts -> `NO_MEASURABLE_ADVANTAGE`;
- System greater -> `SYSTEM_MEASURABLE_ADVANTAGE`;
- Baseline greater -> `BASELINE_ADVANTAGE`;
- invalid identity/parity/two-arm execution -> `INVALID_MEASUREMENT`.

The executed evaluation was:

- System: **7/7**
- Baseline: **7/7**
- Disposition: **NO_MEASURABLE_ADVANTAGE**

This does **not** mean the two systems are globally equivalent. It means the additional lifecycle machinery did not produce measurable advantage on this prospectively frozen slice.

## Privacy / redaction

Private local filesystem usernames and machine paths are not needed to interpret the public result. Where raw Q2 artifacts are published, local repository roots may be replaced with `<LOCAL_REPO_ROOT>` and the filename will explicitly say `.redacted`. Original embedded SHA-256 identities are retained only as historical identities of the private frozen artifacts; they should not be interpreted as hashes of a redacted public copy.

Raw private conversation transcripts are not part of this package.
