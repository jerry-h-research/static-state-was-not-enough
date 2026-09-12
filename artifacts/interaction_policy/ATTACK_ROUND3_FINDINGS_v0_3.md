# Interaction Policy Contract Attack — Round 3 Findings

**Target attacked:** `DRAFT_INTERACTION_POLICY_FALSIFICATION_CONTRACT_v0_3.md`

**Purpose:** try to produce an apparent positive result without demonstrating the intended mechanism, and identify remaining paths to post-hoc interpretation or condition leakage before freeze.

## Summary

v0.3 fixed the largest Round 2 problem by separating **mechanism evidence** from **human-utility evidence** and adding STATE-ON / STATE-OFF ablations. Round 3 found several remaining ways the mechanism assay could still false-positive.

The most serious issue is that `STATE-ON` differs from `STATE-OFF` in more than learned content: it also contains an extra artifact, extra tokens, explicit interaction-policy framing, and potentially hypothesis-revealing language. A difference between ON and OFF could therefore be caused by **prompt priming or artifact presence**, not online learning.

## Finding R3-A — ON/OFF confounds learned policy with artifact presence

### Attack
`STATE-ON` receives a policy artifact; `STATE-OFF` receives nothing. Even if the artifact contains no useful learned information, its mere presence can:

- remind the model to reason about interaction policy;
- induce more cautious or structured behavior;
- change token/context allocation;
- reveal that adaptation is expected.

### Consequence
An ON > OFF effect does not isolate the causal contribution of learned policy content.

### Required repair
Add a **STATE-SHAM** control with the same schema, rendering format, and comparable size as STATE-ON but without the relevant learned policy relation for that probe. Mechanism attribution requires ON to beat both OFF and SHAM in the predicted direction.

## Finding R3-B — Natural-language state can smuggle the hypothesis

### Attack
A policy entry such as:

> "When Jerry says X, prefer direct action unless Y"

can act as a prompt instruction rather than evidence of learned interaction policy. The system may simply obey a dynamically written prompt.

### Consequence
The experiment could demonstrate "LLMs follow injected instructions" rather than feedback-dependent learning.

### Required repair
Freeze a **canonical machine-readable renderer** before evaluation. State entries must use fixed fields and controlled vocabulary; no free-form rationale or task-specific prose may be injected into the evaluation prompt.

## Finding R3-C — Context taxonomy can leak task semantics indirectly

### Attack
Even if task answers are forbidden, a context/category label can encode them indirectly (`refund-risk-high`, `needs-two-options`, `ask-before-delete`).

### Consequence
The policy layer becomes a compressed answer/memory channel.

### Required repair
Freeze taxonomy on development data only and perform a **semantic leakage audit**. Evaluation-time entries may only reference pre-existing generic context labels. New labels, task-derived paraphrases, and answer-like category names are prohibited.

## Finding R3-D — Single-shot ablations are vulnerable to model stochasticity

### Attack
One ON output and one OFF output can differ by sampling noise, backend nondeterminism, or provider variance.

### Consequence
A lucky pair can be misread as a causal learning effect.

### Required repair
Human-facing evaluation remains one-shot, but the hidden mechanism assay must use a frozen number of independent replicate invocations per ON/OFF/SHAM probe. Probe-level mechanism coding is based on decision-class frequencies, not a single response.

## Finding R3-E — Triad success threshold is still undefined

### Attack
v0.3 requires at least three triads but leaves the success threshold to be frozen later. A permissive threshold can be chosen after seeing development behavior.

### Consequence
One or two favorable anecdotes could still support a branch-level learning claim.

### Required repair
Freeze both the number of sealed triads and the passing rule before implementation targets the sealed set. Round 3 recommends at least **four independent triads**, with a supermajority transfer criterion and zero critical exception failures.

## Finding R3-F — Author-designed gold can encode the desired theory

### Attack
The same researcher can design a task to make a preferred convention obviously useful, then label the paired exception according to the intended hypothesis.

### Consequence
The gold may test whether the task author can manufacture a learning signature rather than whether the mechanism handles a genuinely discriminative interaction problem.

### Required repair
Before sealing, every triad and gold record must receive **independent adversarial review** focused on ambiguity, matching, and whether the transfer/exception distinction is defensible without seeing condition outputs. Disagreement unresolved before execution means the task is removed, not adjudicated after results.

## Finding R3-G — Blind coding can fail if raw output reveals the condition

### Attack
STATE-ON outputs may mention learned preferences or sound systematically different, allowing a coder to infer condition identity.

### Consequence
"Blind" coding becomes nominal rather than real.

### Required repair
Primary mechanism coding should operate on a **normalized decision record** (`ACT`, `ASK`, `ALTERNATIVES`, `VERIFY`, `DEFER`) generated by a frozen extractor or independent preprocessing step. The primary coder should not see the policy artifact, condition label, or raw generation unless required for a pre-specified adjudication path.

## Finding R3-H — Simpler-baseline challenge occurs too late

### Attack
v0.3 permits a positive result first and only later challenges it with a simpler heuristic baseline.

### Consequence
A result may be publicized as support for adaptive learning before discovering that a fixed rule such as "ask on ambiguity, act otherwise" produces the same benefit.

### Required repair
Add the materially simpler baseline **inside the sealed feasibility design** rather than after it. The adaptive branch cannot receive `PRACTICAL_ADVANTAGE` unless it beats or shows a learning-specific signature unavailable to the simple static heuristic.

## Finding R3-I — Any tiny H1 reduction currently counts as success

### Attack
A one-turn improvement across the entire experiment can satisfy `H1_intervention < H1_baseline`.

### Consequence
Statistically/noisily trivial differences can be labeled practical advantage.

### Required repair
Freeze a **minimum practical-effect threshold** for H1 before execution. The exact value may remain conservative, but strict inequality alone is insufficient.

## Finding R3-J — Updater access boundary is not explicit

### Attack
The policy-state updater could accidentally see task gold, evaluator labels, or future role metadata during execution.

### Consequence
The state may encode privileged evaluation information even if the final renderer looks clean.

### Required repair
Freeze the updater input contract. It may receive only the current task interaction record and participant feedback permitted by the protocol. Gold labels, future tasks, matching metadata, and evaluation disposition are inaccessible.

## Round 3 disposition

**v0.3 should not be frozen.**

The main repairs required for v0.4 are:

1. three-way `STATE-ON / STATE-SHAM / STATE-OFF` mechanism control;
2. canonical fixed-schema state rendering;
3. development-only context taxonomy plus semantic-leakage audit;
4. replicated hidden ablations;
5. fixed triad count and pass threshold;
6. independent adversarial gold review;
7. normalized blind decision coding;
8. simpler heuristic baseline moved into the sealed design;
9. minimum practical-effect threshold for H1;
10. explicit updater information boundary.

If these repairs are incorporated, remaining uncertainty should be dominated less by measurement loopholes and more by the unavoidable limitations of an N-of-1 feasibility test.