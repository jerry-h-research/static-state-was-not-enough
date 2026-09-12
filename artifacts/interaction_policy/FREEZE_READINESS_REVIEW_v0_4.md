# Interaction Policy Experiment — Freeze-Readiness Review of v0.4

**Review purpose:** determine whether the falsification contract is still missing a major measurement safeguard, or whether the remaining work is specification rather than conceptual repair.

## Overall judgment

v0.4 is **close to freeze-ready as a contract**, but it is **not yet ready to freeze the experiment** because several supporting artifacts named by the contract do not yet exist: the fixed heuristic comparator, the policy-state schema/renderer, the sealed triads, task-level gold, the participant response protocol, and the coding/invalidation rules.

The review did **not** identify another loophole on the scale of Rounds 1–3. The remaining issues are mostly threshold justification, execution burden, and ensuring that the experiment tests the hypothesis rather than the sophistication of the protocol.

## 1. Is the design now too complex?

### Finding

The design is substantially more complex than the original idea, but most of the added structure now has a direct reason:

- A distinguishes fresh/no-learning behavior.
- B tests adaptive feedback-derived policy state.
- C tests whether a simple static heuristic is sufficient.
- ON/SHAM/OFF separates learned content from artifact-presence effects.
- TRANSFER/EXCEPTION pairs distinguish useful generalization from indiscriminate reuse.
- H1/H2 separates usability from safety/trajectory quality.

Removing any one of these would reopen a previously identified confound.

### Decision

Do **not** add further architectural controls unless a concrete loophole is identified. From this point onward, prefer simplifying implementation rather than expanding the contract.

## 2. Are the numerical thresholds arbitrary?

### 20% H1 threshold

Yes, 20% is a prospective **smallest-effect-of-practical-interest choice**, not a statistically derived constant. That is acceptable for an N-of-1 feasibility study only if it is described that way.

However, a relative threshold alone can still be trivial when total burden is small. Therefore v0.5 should add an **absolute guard**: B must improve by at least two total operating-burden turns versus each comparator as well as meeting the relative threshold.

This makes the practical criterion:

`H1_turns_B <= 0.80 * comparator` **and** `H1_turns_B <= comparator - 2`

for both A and C.

The exact 20% / two-turn choice remains conventional and must be reported as preselected rather than discovered from data.

### 3-of-4 triads

This is also a prospective robustness rule rather than an inferential statistic. Four triads with a 3-of-4 pass criterion is preferable to one anecdotal success while still allowing one triad to fail. The result must not be reported as a population success rate.

### Three hidden-assay replicates

Three replicates are a coarse stability check, not a statistical sample. Their purpose is to prevent a single stochastic completion from creating a mechanism claim. This is acceptable for feasibility if the limitation is explicit.

## 3. Can the same core question be answered more simply?

### Considered simpler design

A two-condition A/B experiment without C or SHAM would be much shorter.

### Why it is insufficient

It would not distinguish:

- online learning from a better fixed interaction rule;
- learned policy content from the generic effect of adding an extra prompt artifact;
- useful transfer from indiscriminate convention reuse.

These were exactly the major confounds found in prior attack rounds.

### Decision

Keep A/B/C and ON/SHAM/OFF, but keep the intervention implementation itself minimal.

## 4. Remaining freeze blockers

The contract should not be frozen until these concrete artifacts exist and are independently checked:

1. **Policy-state schema** — exact fields, controlled vocabularies, size bound.
2. **Canonical renderer** — deterministic serialization of policy state.
3. **Updater contract** — exactly what feedback can change which fields.
4. **Comparator C** — one fixed non-learning heuristic policy.
5. **Four learning triads** — exposure, transfer, exception tasks with matched A/B/C variants.
6. **Critical probes** — epistemic conflict / high-stakes / verification tasks if included.
7. **Task-level gold** — allowed/prohibited initial decisions and defect rules.
8. **Independent adversarial gold review** — completed before outputs exist.
9. **Participant response protocol** — fixed correction/clarification behavior.
10. **Blind coding + normalization rules** — especially mapping free-form model outputs to decision classes.
11. **Task invalidation / missing evidence rules.**
12. **Condition order and matched-set mapping.**
13. **Model/settings/memory-isolation record.**

Until these exist, freezing the prose contract alone would create false confidence.

## 5. One remaining conceptual risk

The experiment can show that a **designed policy-state mechanism** learns useful interaction conventions. It cannot by itself establish that this is what produced the original long-running Jerry–AI interaction.

Therefore even a positive result must remain:

> bounded feasibility of one engineered online-calibration mechanism

not:

> causal explanation of the historical long-running interaction.

v0.4 already states this boundary and it should remain unchanged.

## 6. Freeze-readiness disposition

**Disposition: CONTRACT_NEAR_FREEZE_READY — SUPPORTING_ARTIFACTS_NOT_READY**

No further attack round is justified merely to add more abstract safeguards.

The next work should be to instantiate the pre-freeze artifacts above. If that process reveals a real loophole, revise the contract. Otherwise freeze after the artifacts and thresholds are reviewed together.
