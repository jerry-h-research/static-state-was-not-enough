# Interaction Policy — Pre-Freeze Artifact Pack v0.1

**Status: DRAFT. Nothing in this directory is frozen or executed.**

This pack begins resolving the concrete blockers identified by the v0.5 freeze-readiness review. It intentionally defines the smallest implementation/evaluation interfaces before code is written.

Included now:

- `POLICY_STATE_SCHEMA.json` — controlled adaptive-state fields, vocabulary, and forbidden content.
- `CANONICAL_RENDERER_SPEC.md` — fixed rendering and updater information boundary.
- `STATIC_HEURISTIC_C.md` — materially simpler non-learning comparator.
- `PARTICIPANT_RESPONSE_PROTOCOL.md` — constraints on participant behavior.
- `EVALUATION_RULES.md` — normalization, blind coding, invalidation, rerun, and terminal-failure rules.

Still required before freeze:

1. four concrete learning triads;
2. matched A/B/C task variants;
3. task-level gold and frozen participant clarification/correction records;
4. separate critical probes if needed (`NOVEL`, `VERIFY`, `HIGH_STAKES`);
5. independent adversarial gold review;
6. frozen SHAM generation rule and concrete assay schedule;
7. semantic-leakage review of the schema/taxonomy;
8. final model/version/settings and condition order/mapping.

No intervention implementation should target the sealed evaluation tasks until this pack and the contract are formally frozen.
