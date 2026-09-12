# Literature Collision Update — BenchPreS / OP-Bench / PerMemSafe

**Date:** 2026-09-12

**Status:** pre-execution collision check. No Experiment 3 development baseline run has been executed yet.

## New high-severity collision

The remaining Experiment 3 framing must be narrowed further after identifying work that directly studies when personalization should *not* be applied.

### BenchPreS (2026)

BenchPreS formalizes **context-aware preference selectivity** for persistent-memory LLMs: apply stored preferences when contextually appropriate and suppress them when inappropriate. It reports an adherence/selectivity tension: models that apply preferences more strongly also tend to misapply them more strongly. This directly overlaps the project's proposed `TRANSFER -> EXCEPTION` framing.

Implication: **"learn a preference and know when not to apply it" is not a novel research question.** The project's exception probes may still be useful as controls, but they cannot carry a novelty claim by themselves.

Primary source: arXiv:2603.16557; LG AI Research publication page.

### OP-Bench (2026)

OP-Bench formalizes over-personalization in memory-augmented conversational agents, including irrelevance, repetition, and sycophancy, and proposes a filtering mechanism to reduce inappropriate memory use while preserving personalization.

Implication: **"personalization can overreach because memory is over-retrieved/over-attended" is already an explicit benchmark target.**

Primary source: arXiv:2601.13722.

### PerMemSafe (Findings of ACL 2026)

PerMemSafe evaluates implicit personalized safety in long-horizon self-evolving agents and reports substantial safety limitations even for strong systems. It proposes a risk-aware memory framework that improves personalized safety while maintaining helpfulness.

Implication: **"long-horizon personalization introduces user-specific safety risks" is also established research territory.** Generic safety probes cannot be presented as a new contribution.

Primary source: ACL Anthology 2026.findings-acl.320.

## Updated claim boundary

The following are now explicitly retired as potential novelty claims for Experiment 3:

- online learning of user preferences from feedback;
- persistent preference memory;
- context-dependent preference application;
- preference suppression on exceptions;
- over-personalization as a failure mode;
- personalized long-horizon safety as a general problem;
- generic ambiguity/risk-based ASK-vs-ACT control;
- user-effort reduction from personalization.

## What may still remain worth testing

A narrower bounded question may still be experimentally useful even if it is not novel:

> Can a minimal feedback-derived external interaction-policy layer reduce **explicit user-control burden** relative to both a fresh baseline and a simple static heuristic, while preserving context-sensitive selectivity and critical epistemic/authorization boundaries?

The distinctive value, if any, would be in the **joint falsification protocol**, not in any one component:

1. explicit operating-burden threshold;
2. adaptive vs fresh vs static-heuristic human-facing comparison;
3. feedback-dependent ON/SHAM/OFF causal ablation;
4. selective transfer / suppression controls;
5. critical epistemic and authorization gates;
6. a willingness to classify the mechanism as unnecessary if the static heuristic matches it.

This must not be described as novel until a fuller literature review confirms that the exact joint evaluation has not already been done.

## Decision before implementation

**Do not start Codex implementation yet.**

The current development tasks may still be used for a cheap baseline-skew screen, but only as measurement-material development. Before sealed evaluation, the research question and contract should be revised to cite BenchPreS, OP-Bench, PerMemSafe, and the previously identified personalization/user-effort literature.

If a later source already evaluates the same joint trade-off (burden reduction + adaptive preference use + overreach/selectivity + causal adaptive-state ablation against a static heuristic), Experiment 3 should be killed or reframed rather than duplicated unknowingly.
