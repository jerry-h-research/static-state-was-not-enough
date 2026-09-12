# Sealed source chain

The final bounded Claim Lifecycle engine was built as a three-file inheritance chain:

1. `claim_lifecycle_v0_1_4_18_R12B3.py` — base implementation snapshot (40,098 bytes in the frozen Q2 authorization).
2. `claim_lifecycle_v0_1_4_19_R13C1.py` — loads R12B3 and protects canonical claim-registry identity (3,760 bytes).
3. `claim_lifecycle_v0_1_4_20_R13C2.py` — loads R13C1 and requires strict Boolean semantic discriminators at evidence admission (710 bytes).

Frozen SHA-256 identities from the Formal Q2 authorization:

- R12B3: `ac8f4de0fe7b4d8e781b56dd2a8f8f49a2a2694ad92aea88721f293ec99f41e9`
- R13C1: `56a8df9f98474cca287cbee1c11790193cdb46d70946b4d43d7754314fa307b1`
- R13C2: `7d763c70b5d717310d517cf677efad5b0f4e6ebfb3d8ca6f0c62f1ab20556d7f`

## Important reproducibility note

The source files are dependency-linked; R13C2 is not a standalone implementation. The public research claims in this repository therefore do **not** treat a single final patch file as sufficient reproduction evidence.

The v0.3 public package documents the exact frozen identities and the machine-test/evaluation chain. A complete executable source/test snapshot is a separate reproducibility artifact and is not required to interpret the reported null/negative results.
