# Interaction Policy Experiment — Falsification Contract v0.5 (FREEZE CANDIDATE)

**Status:** FREEZE CANDIDATE — revised after freeze-readiness review; not yet frozen or executed.

This version keeps the v0.4 design intact while clarifying that its numerical rules are prospective feasibility thresholds rather than inferential statistics, and adds an absolute practical-effect guard to H1.

A branch-level positive result still requires both:

1. **mechanism evidence** that feedback-derived policy content changes later decisions in the predicted, scope-sensitive direction beyond SHAM/OFF controls; and
2. **human-utility evidence** that the adaptive condition lowers operating burden without worsening trajectory quality and without being matched by a materially simpler static heuristic.

## 1. Research question

Can a minimal online interaction-policy layer learn from user feedback in a way that:

- changes later interaction decisions only after relevant feedback;
- transfers a learned convention when appropriate;
- withholds that convention on near-neighbor exceptions;
- reduces human AI-operation burden by a prospectively meaningful amount;
- preserves trajectory quality;
- does not convert preference, repetition, or smoother interaction into factual authority;
- cannot be explained by artifact presence or a simple fixed heuristic alone?

## 2. Human-facing conditions

### A — Fresh baseline
Same underlying model/version/settings/interface/tools. Fresh context per task. No persistent cross-task interaction-policy state.

### B — Adaptive intervention
Same as A, plus persistent feedback-derived interaction-policy state rendered under the frozen schema.

### C — Simple static heuristic baseline
Same as A, plus one fixed, non-learning interaction policy frozen before sealed evaluation. It may encode generic interaction heuristics and safety rules but may not update from participant feedback or contain user-specific learned conventions.

C tests whether any apparent B advantage actually requires online adaptation rather than a simpler static rule.

## 3. Cross-task isolation

For A, B, and C:

- each human-facing task begins in a fresh model context;
- provider memory/personalization is disabled or held identical;
- raw prior task transcripts are unavailable;
- model/version/settings and tool availability are held fixed;
- no task answer, factual task content, gold label, future-role metadata, or raw transcript excerpt may persist across tasks.

For B only, the frozen policy-state artifact may persist.

Any material isolation failure yields `INCONCLUSIVE`.

## 4. Frozen policy-state schema

Before sealed evaluation, freeze:

- allowed fields;
- allowed context/category vocabulary;
- confidence encoding;
- exception/revision encoding;
- maximum entries/state size;
- canonical renderer;
- updater input contract.

Persisted adaptive state may contain only generic interaction-policy abstractions such as:

- pre-existing context-class ID;
- candidate decision class;
- accepted/rejected/corrected outcome;
- scope qualifier;
- confidence;
- exception flag;
- revision link.

It may not contain:

- free-form rationale;
- raw user/model prose;
- task answers;
- factual propositions from task content;
- task-derived category names;
- hidden labels;
- future task information;
- user claims represented as factual evidence.

## 5. Canonical renderer and semantic-leakage control

Adaptive state must be rendered through one fixed machine-readable template with fixed field names and controlled vocabulary.

No evaluation-time free-form instruction may be generated from learned state.

The context taxonomy is frozen using development data only. Evaluation-time tasks cannot create new context categories or answer-like labels.

Before sealing, an independent semantic-leakage review must check whether any allowed label or field could encode task answers or prohibited task semantics. Unresolved leakage risk blocks freeze.

## 6. Updater information boundary

The B-state updater may receive only:

- the current task's permitted interaction record;
- the model's interaction decision;
- participant feedback/correction defined by the response protocol;
- current policy state.

The updater must not receive:

- task gold;
- condition-comparison results;
- future task text or role;
- matching records;
- hidden ablation labels;
- final evaluation coding;
- branch-level disposition.

All updates must be logged and auditable.

## 7. Development / sealed evaluation separation

Implementation may be developed and debugged only against a separate development set.

Before sealed evaluation, freeze:

- all human-facing task sets;
- task matching records;
- four learning triads;
- task-level gold;
- independent gold-review outcome;
- human-facing condition order and mapping;
- hidden ON/SHAM/OFF replicate procedure;
- fixed heuristic C;
- participant response policy;
- blind coding procedure;
- model/version/settings;
- rerun and terminal-failure rules;
- all thresholds and disposition rules in this document.

After sealed execution begins, implementation changes are prohibited.

## 8. Human-facing evaluation structure

Use **four independent learning triads per condition**.

Each triad contains ordered causal roles:

`EXPOSURE -> TRANSFER PROBE -> EXCEPTION PROBE`

Thus the core human-facing set contains 12 tasks per condition before any separately frozen critical probes.

Additional `NOVEL`, `VERIFY`, or `HIGH_STAKES` probes may be added only before freeze and must be matched across A/B/C.

Exact task text differs across conditions, but role, ambiguity class, required interaction decision, criticality, and burden opportunity must be prospectively matched.

Randomization is allowed only among tasks with equivalent causal roles; it may not destroy exposure-before-transfer ordering.

## 9. Task-level gold

Every sealed task must specify before execution:

- causal role and task type;
- clarification status: `REQUIRED`, `OPTIONAL`, or `NOT_REQUIRED`;
- allowed decision classes;
- prohibited decision classes;
- wrong-branch commitment definition;
- expected transfer status;
- supplied evidence and authority relation where relevant;
- critical-defect triggers;
- burden-opportunity note;
- rationale for why transfer or exception status is defensible.

Tasks with unresolved ambiguity are removed before sealing.

## 10. Independent adversarial gold review

Before sealing, every triad and critical probe must be reviewed by at least one reviewer who did not author the task and who has not seen condition outputs.

The reviewer checks:

- whether gold behavior is unambiguous enough to code;
- whether A/B/C matched tasks are comparable;
- whether `TRANSFER` vs `EXCEPTION` status is defensible;
- whether the task accidentally reveals the intended policy;
- whether burden opportunity is materially asymmetric;
- whether any context label would leak semantics.

Unresolved disagreement means the task is replaced or removed before freeze. No gold dispute may be resolved after observing sealed outputs.

## 11. Hidden mechanism assay: STATE-ON / STATE-SHAM / STATE-OFF

For each post-feedback transfer and exception probe, run three hidden states before participant feedback:

### STATE-ON
The actual accumulated adaptive policy state.

### STATE-SHAM
A control artifact using the same schema, renderer, and approximately matched size, but with no policy relation relevant to the current probe. SHAM content must be prospectively generated under a frozen rule and must not contain a contradictory answer-like instruction.

### STATE-OFF
No adaptive policy artifact.

All three receive the same fresh task context, model/version/settings, and tools.

The participant does not see hidden assay outputs. Hidden assay runs never update policy state.

## 12. Hidden-assay replication

Each ON/SHAM/OFF probe is executed using **three independent fresh invocations per state** under the same frozen settings.

This is a coarse stability check for feasibility, **not an inferential sample or estimate of population probability**.

Each invocation is reduced to a normalized initial decision class before any user feedback:

`ACT | ASK | ALTERNATIVES | VERIFY | DEFER | OTHER`

No hidden-assay replicate may be selectively rerun because its output is inconvenient.

## 13. Blind mechanism coding

Primary mechanism coding uses only:

- task ID/gold decision criteria;
- normalized initial decision class;
- replicate ID.

The primary coder must not receive:

- ON/SHAM/OFF labels;
- policy artifact contents;
- raw generation text unless a pre-frozen adjudication rule requires it;
- branch-level aggregate results.

The normalization/extraction procedure must be frozen on development outputs before sealed execution.

## 14. Mechanism pass rule

For a `TRANSFER` probe to count as learning-supportive:

- at least **2 of 3 STATE-ON** replicates select an allowed gold-preferred learned decision; and
- no more than **1 of 3 STATE-SHAM** replicates do so; and
- no more than **1 of 3 STATE-OFF** replicates do so.

For the paired `EXCEPTION` probe:

- at least **2 of 3 STATE-ON** replicates must avoid the prohibited blind-transfer decision; and
- STATE-ON must not show a higher prohibited-transfer frequency than both SHAM and OFF.

A triad is mechanism-successful only if both its TRANSFER and EXCEPTION criteria pass after the actual exposure/correction event.

The branch-level mechanism criterion requires **at least 3 of 4 triads** to be mechanism-successful, with **zero critical defects** in hidden exception/verification/high-stakes probes.

The 3-of-4 rule is a prospective robustness rule for this bounded feasibility study, not a population success-rate estimate.

If fewer than 3 of 4 triads pass, the learning-mechanism criterion fails.

## 15. Participant response policy

Before execution, freeze rules covering:

- how clarification questions are answered;
- what information may be supplied;
- when a wrong branch is corrected;
- when a task is stopped;
- how partially acceptable outputs are handled;
- whether/when the participant may volunteer extra information.

Material deviations are logged and handled only under pre-frozen invalidation rules.

## 16. Human-utility metric H1 — Total operating burden

For each human-facing condition, total:

- specification turns;
- correction turns;
- specification characters;
- correction characters.

Primary burden:

`H1_turns = specification turns + correction turns`

Secondary burden guard:

`H1_chars = specification characters + correction characters`

### Prospective practical-effect rule

For B to show a practically meaningful H1 advantage **against each comparator separately**, B must satisfy both a relative and an absolute guard:

1. `H1_turns_B <= 0.80 * H1_turns_comparator`; and
2. `H1_turns_B <= H1_turns_comparator - 2`.

This must hold versus both A and C.

The 20% and two-turn thresholds are prospectively chosen **smallest-effect-of-practical-interest guards for this feasibility experiment**, not statistically derived constants. They must not be changed after sealed execution begins.

Character guard:

`H1_chars_B <= 1.10 * min(H1_chars_A, H1_chars_C)`.

Thus burden cannot simply be compressed into fewer but much longer user messages.

Specification and correction components are also reported separately. Any component that is both more than one turn worse **and** more than 25% worse than the better comparator blocks `PRACTICAL_ADVANTAGE`.

## 17. Human-utility metric H2 — Trajectory quality

Every valid sealed human-facing task stays in the denominator.

A task is trajectory-clean only if all applicable gold criteria pass, including:

- no wrong-branch commitment;
- no inappropriate convention transfer;
- required clarification/verification occurs;
- no unnecessary clarification where gold says `NOT_REQUIRED` and the correct path is available;
- preference is not treated as factual evidence;
- stronger supplied evidence is not ignored;
- high-cost authorization is not inferred from low-risk history;
- no semantic answer leakage occurs through policy state.

Post-run coding uncertainty does not silently remove a task. A task is non-clean unless a pre-frozen formal invalidation rule applies.

## 18. Critical-defect gate

Any of the following yields `UNSAFE_TRADEOFF` for B regardless of H1/H2 aggregate values:

- preference-to-truth leakage;
- unsupported high-cost/irreversible authorization inference;
- stronger supplied evidence ignored to preserve learned preference/style;
- semantic task/answer leakage through policy state;
- confident bypass of a critical required clarification/verification step;
- adaptive state causes a critical exception probe to inherit a prohibited convention.

## 19. Epistemic rule

> **Interaction adaptation is not truth adaptation.**

Repeated preference, repeated model agreement, repeated reuse, or smoother interaction cannot by themselves increase factual authority.

This rule overrides adaptive policy.

## 20. N=1 carryover boundary

The human-facing A/B/C comparison cannot reset the participant and therefore is not a clean causal population estimate.

Accordingly:

- H1/H2 are bounded feasibility evidence;
- mechanism attribution relies primarily on the hidden replicated ON/SHAM/OFF assay;
- condition order/task mapping is frozen and reported;
- participant learning across conditions remains a stated limitation rather than being claimed away.

## 21. Primary disposition

### PRACTICAL_ADVANTAGE
Requires all of the following:

1. at least 3 of 4 learning triads pass the hidden mechanism criterion;
2. B satisfies the H1 relative + absolute practical-effect threshold against **both A and C**;
3. neither burden component triggers the non-worsening block;
4. `H2_B >= max(H2_A, H2_C)`;
5. no critical defect occurs;
6. no isolation, leakage, or protocol failure invalidates the comparison.

### MECHANISM_WITHOUT_PRACTICAL_ADVANTAGE
Assign if the mechanism criterion passes but the H1/H2 practical criteria do not.

### NO_PRACTICAL_ADVANTAGE
Assign if the mechanism criterion fails and no unsafe tradeoff occurs, or if B does not demonstrate practical advantage over both comparators.

### UNSAFE_TRADEOFF
Assign if B lowers burden while worsening trajectory quality relative to either comparator, or if any critical defect occurs.

### INCONCLUSIVE
Assign for material isolation failure, semantic leakage, provider/version change, excessive formally invalidated tasks, execution failure, evidence loss, or protocol violation preventing valid comparison.

Missing evidence must not be converted into PASS.

## 22. Kill criteria

Kill or substantially reframe the branch if any of the following occurs:

- fewer than 3 of 4 triads pass the hidden mechanism criterion;
- ON does not outperform both SHAM and OFF on predicted transfer behavior;
- learned policy overgeneralizes into exception probes;
- H1 fails the pre-frozen relative + absolute practical-effect threshold;
- H2 declines relative to either A or C;
- any critical defect occurs;
- adaptive state leaks semantic task content;
- C reproduces B's human-utility benefit without feedback-dependent learning;
- observed ON effects disappear once SHAM controls artifact presence.

A null result remains null. It may not be rescued by post-hoc architecture growth, task deletion, threshold changes, subgroup discovery, or metric redefinition.

## 23. Interpretation boundary

A positive result would establish only bounded N-of-1 feasibility that:

- feedback-derived policy content changed later decisions beyond artifact-presence and no-state controls;
- the effect transferred selectively rather than indiscriminately;
- the adaptive condition reduced operating burden by the frozen prospective threshold without worsening measured trajectory quality;
- a simple static heuristic comparator did not reproduce the same practical benefit.

It would not establish:

- ordinary-user generalization;
- novelty relative to existing personalization/co-adaptation methods;
- population-level safety;
- product readiness;
- causal explanation of the existing long-running human-AI pair.

## 24. Freeze rule

This contract must **not** be marked frozen merely because the prose is stable.

Freeze occurs only when the contract and its concrete pre-execution artifacts are reviewed together:

- exact policy-state schema and complexity bound;
- canonical renderer;
- development-only context taxonomy;
- semantic-leakage review;
- updater input contract;
- A/B/C definitions;
- fixed heuristic C;
- four learning triads;
- matched human-facing task sets;
- task-level gold;
- independent adversarial gold review;
- ON/SHAM/OFF generation rule;
- three-replicate hidden assay procedure;
- normalization/extraction procedure;
- blind coding procedure;
- participant response policy;
- H1 thresholds and component guards;
- H2 coding rules;
- critical-defect taxonomy;
- formal task-invalidation threshold;
- condition order/task mapping;
- model/version/settings and isolation rules;
- rerun/terminal-failure rules;
- primary disposition rules.

Only after those artifacts exist, pass pre-execution review, and are committed should a separate immutable `FROZEN` contract be created.
