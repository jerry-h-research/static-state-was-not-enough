# Interaction Policy Experiment — Contract Attack Round 2

**Target:** `DRAFT_INTERACTION_POLICY_FALSIFICATION_CONTRACT_v0_2.md`  
**Purpose:** try to make v0.2 pass, fail, or become uninterpretable for reasons unrelated to genuine online interaction-policy learning.

## Summary

Round 1 closed several obvious loopholes, but v0.2 still contains design problems large enough to block freezing. The most important issue is that the protocol currently mixes two different questions:

1. **Mechanism question:** does persistent interaction-policy state causally change later decisions after feedback?
2. **Human-utility question:** does that change reduce the user's operating burden without harming trajectory quality?

With one human participant who cannot be reset, a simple A-vs-B block comparison cannot cleanly identify both at once.

## R2-A1 — N=1 carryover can mimic intervention benefit

### Attack
If the participant performs baseline tasks first and intervention tasks second, the human may become faster, more concise, or better calibrated simply from learning the task family. If intervention runs first, later baseline behavior may inherit what the human learned while interacting with the intervention.

Counterbalancing task-set labels does not reset the participant.

### Failure mode
`M1` and `M2` differences can reflect participant learning rather than policy-layer learning.

### Required repair
Separate **mechanism evidence** from **human-utility evidence**. Add a counterfactual policy-state ablation at post-feedback probe tasks so the same fresh task can be evaluated with accumulated policy state ON vs OFF before the participant sees the result. Treat the later N=1 user-burden comparison as feasibility evidence with explicit carryover uncertainty, not clean causal identification.

---

## R2-A2 — The temporal signature is too weak and cherry-pickable

### Attack
v0.2 requires only “at least one” pre-specified convention showing exposure -> improvement -> exception restraint. With 12 tasks and multiple convention types, one successful chain could occur by chance or because that convention was already favored by the base model.

### Failure mode
A single convenient success can satisfy the learning signature while most learned-policy behavior is absent or harmful.

### Required repair
Freeze multiple **learning triads** before execution. Each triad must contain:

1. an exposure/correction task;
2. a later transfer probe;
3. a near-neighbor exception probe.

Require success on a pre-specified minimum proportion of triads, not one example.

---

## R2-A3 — Aggregate M1/M2 comparison is under-specified

### Attack
The contract defines task-level tuples but not exactly how task-level tuples become condition-level M1/M2. Mean turns? Median? Total turns? Lexicographic aggregation? How are zero-burden tasks handled? How does the character materiality threshold apply across tasks?

### Failure mode
The final comparison rule can be selected after seeing results.

### Required repair
Freeze a single aggregation rule before execution. Prefer condition-level totals for primary disposition, with per-task distributions descriptive only.

---

## R2-A4 — Requiring both M1 and M2 to be strictly lower can create structural false negatives

### Attack
If the baseline already has zero correction turns on most or all tasks, a safe intervention cannot make `M2_intervention < M2_baseline`. The intervention could materially reduce specification burden while preserving zero correction burden and perfect trajectory quality, yet the contract would force `NO_PRACTICAL_ADVANTAGE`.

### Failure mode
The disposition rule can reject a real burden reduction simply because one burden component is at floor.

### Required repair
Define a primary **total operating burden** from specification + correction burden, while keeping M1 and M2 separately reported. Require total burden improvement with neither component materially worse. Preserve M3 and critical-failure gates unchanged.

---

## R2-A5 — User behavior remains an uncontrolled detector

### Attack
Even with blind coding, the participant decides whether to clarify, accept, challenge, or correct. The same model error may receive a correction in one condition and be silently tolerated in another.

### Failure mode
M1/M2 can reflect participant response strategy rather than system performance.

### Required repair
Before execution, freeze a **participant response policy** for evaluation tasks: when to answer clarifications, when to correct a wrong branch, and when to stop. Deviations must be logged and may force `INCONCLUSIVE` for the affected task.

---

## R2-A6 — M3 UNKNOWN exclusion can inflate quality

### Attack
v0.2 excludes UNKNOWN tasks from both numerator and denominator. If difficult or ambiguous failures disproportionately become UNKNOWN, M3 can improve as evidence quality worsens.

### Failure mode
The intervention can appear trajectory-clean because hard cases disappear from the denominator.

### Required repair
Final sealed evaluation tasks must have adjudicated gold before execution. Post-run coding UNKNOWN should count as **not clean for the primary M3 denominator**, unless the task itself is formally invalidated under a pre-frozen protocol. Too many invalidated tasks yield `INCONCLUSIVE`.

---

## R2-A7 — Critical tasks need severity separation from ordinary M3

### Attack
A high-cost authorization failure and a harmless unnecessary clarification are both currently represented inside M3, even though the former is qualitatively more severe.

### Failure mode
A high average trajectory score can obscure a serious but non-listed defect.

### Required repair
Keep M3 as a proportion, but freeze a broader **critical-defect taxonomy**. Any critical defect fails the safety gate regardless of aggregate M3.

---

## R2-A8 — “Matched non-identical task sets” can hide difficulty imbalance

### Attack
With only 12 tasks per condition, small differences in ambiguity or task difficulty can dominate M1/M2/M3.

### Failure mode
Condition effects can actually be task-set effects.

### Required repair
Each A/B task pair must have a frozen matching record covering task type, ambiguity class, required decision, expected burden opportunity, and criticality. Matching should be reviewed before execution without access to eventual condition outcomes.

---

## R2-A9 — Task order randomization can break the causal learning structure

### Attack
A pure random order could place transfer or exception probes before the exposure that is supposed to teach the convention.

### Failure mode
The experiment could fail because the required learning opportunity never existed.

### Required repair
Freeze **ordered role slots**: exposure must precede transfer and exception probes within each learning triad. Randomization may occur only among tasks occupying equivalent causal roles.

---

## R2-A10 — Base-model prior can masquerade as learned policy

### Attack
A post-feedback transfer probe may simply match what the base model would have done anyway. Observing correct behavior after exposure does not prove the policy state caused it.

### Failure mode
Temporal order is mistaken for causal contribution.

### Required repair
For each sealed post-feedback probe, generate a hidden **policy-state ablation twin** in the same fresh context: one run with accumulated policy state, one with the state removed. Compare the model's initial interaction decision before participant feedback. A learning claim requires pre-specified ON-vs-OFF decision differences aligned with the learned convention while preserving correct exception behavior.

---

## R2-A11 — Policy state can overfit evaluation ontology without leaking literal task answers

### Attack
Even if raw task semantics are prohibited, state could accumulate extremely specific context tags or exception patterns that effectively encode the sealed benchmark structure.

### Failure mode
The layer becomes a benchmark-specific lookup system rather than a general interaction policy.

### Required repair
Freeze a compact policy schema and maximum state complexity before sealed evaluation. No new context taxonomy may be invented after evaluation begins. Policy entries must be interpretable at a category level broader than a single task instance.

---

## R2-A12 — Hosted-model drift and stochasticity can swamp a 12-task comparison

### Attack
If provider behavior changes between blocks, or stochastic outputs vary materially, apparent learning differences may not be attributable to policy state.

### Failure mode
Small N differences become model-service noise.

### Required repair
Run paired ON/OFF ablation probes as close in time as practical with identical model/version/settings, record timestamps and model identifiers, and treat provider/version changes during the run as protocol violations. Human-facing A/B comparisons remain feasibility evidence rather than precision estimates.

---

# Round 2 disposition

**v0.2 is NOT ready to freeze.**

The strongest required change is conceptual: split evidence into two layers.

### Layer 1 — Mechanism evidence
Does accumulated policy state causally alter later initial decisions in the predicted direction after feedback, while respecting exceptions?

Use pre-specified learning triads plus hidden ON/OFF policy-state ablations.

### Layer 2 — Human-utility evidence
Does the human-facing intervention reduce total operating burden without worsening trajectory quality or triggering critical defects?

Treat N=1 user-burden results as bounded feasibility evidence with carryover limitations.

Only if both layers are positive should the branch advance beyond N=1 feasibility.
