# Related-Work Collision Matrix — 2026-09-12

**Status:** literature collision check performed before development baseline-skew execution.

This note narrows the claim space for the proposed Interaction Policy experiment. It is not a novelty claim and is based on the cited public paper/project descriptions available at the time of review.

| Work | Learns/uses individual preference from interaction | Context/scope-sensitive preference | Online/persistent adaptation | Measures user effort / interaction efficiency | Interaction behavior itself | Explicit exception / overreach / epistemic guardrail as primary test | Collision with current Experiment 3 |
|---|---|---|---|---|---|---|---|
| PrefEval (ICLR 2025) | Yes | Limited/contextual via long conversation | Tests prompting/feedback/RAG; not primarily a new online policy layer | Not primary | Preference following | No | Medium |
| Interact-to-Align / ALOE (COLING 2025) | Yes, including implicit preferences | Personalized via multi-turn interaction | Model trained for dynamic personalized alignment | Not central | Yes | No | High |
| CUPID (COLM 2025) | Yes | **Yes; central contribution** | Evaluates inference/application from prior interaction histories | Not primary | Personalized response generation | Contrastive/changing preferences, but not our safety tradeoff | **Very high** |
| Steerable Chatbots (2025) | Yes / calibrated or learned preference steering | Preference dimensions | Lightweight inference-time steering | User study includes usability/control burden motivation | Response preference expression | No | High for reducing prompt-specification burden |
| MultiSessionCollab (2026) | **Yes** | Long/short-term preference memory | **Persistent memory refined across sessions** | **Yes: task success, efficiency, reduced user effort** | Includes interaction preferences | Not primary | **Very high** |
| VARS (2026) | Yes | Long-term + short-term vectors | **Online update from user feedback** | **Yes: user effort and timeout** | Preference-aware retrieval/interaction | Not primary | **Very high** |
| PAHF (2026) | **Yes** | Idiosyncratic and drifting preferences | **Live pre-action clarification + post-action feedback + per-user memory** | Personalization error/adaptation speed | Agent action/clarification loop | Safety boundary not primary | **Very high** |
| PrefIx (ACL Findings 2026) | Yes | 31 settings / 14 interaction attributes | Preference-aware adaptation | UX + task accuracy | **Interaction behavior is central** | Not primarily epistemic/authorization overreach | **Very high** |
| Value of Information (ACL 2026) | Not user-personalization learning | Context-sensitive ambiguity/risk | Adaptive inference-time communication, not learned personal memory | **Explicitly balances user effort** | **Ask-vs-act communication policy** | Risk-sensitive but not preference-learning safety | High for ambiguity/ask-vs-act triad |

## Collision conclusion

The following broad claims are **not available** to this project as plausible novelty claims:

1. AI can learn user preferences from interaction.
2. Preferences can be contextual rather than global.
3. Persistent memory can improve long-term collaboration.
4. Personalization can reduce user effort even when raw task accuracy changes little.
5. Interaction behavior itself (confirmations, pacing, initiative, clarification) can be treated as a personalization target.
6. Ask-vs-act decisions can be optimized against ambiguity, risk, and user effort.

The current development triads therefore should **not** be interpreted as testing a new general mechanism of personalization or co-adaptation.

## Remaining narrower target worth testing

The potentially useful contribution is a bounded falsification question:

> Can a deliberately minimal, auditable, feedback-derived external interaction-policy state reduce explicit user operating burden beyond both a fresh baseline and a simple static heuristic, while demonstrating scope-sensitive transfer and refusing to let learned convenience/preferences override epistemic, clarification, or authorization boundaries?

Even this narrower target may overlap with details in the full papers and must not be called novel without deeper full-text comparison.

## Design implications before running development tasks

- Treat CUPID as the strongest warning against claiming context-sensitive preference inference as new.
- Treat MultiSessionCollab/VARS as the strongest warning against claiming reduced user effort from persistent preference learning as new.
- Treat PAHF as the strongest warning against claiming online feedback + memory personalization as new.
- Treat PrefIx as the strongest warning against claiming interaction-pattern personalization as new.
- Treat Value of Information as the strongest warning against using generic `ASK` vs `ACT` behavior as evidence of user-specific learning.
- Keep positive learning triads non-epistemic and genuinely user-specific.
- Keep epistemic/authorization/critical ambiguity tests as guardrail probes, not positive learning evidence.
- Compare B against a static heuristic C from the start.
- Preserve the ON/SHAM/OFF ablation if the goal is to attribute decision changes to feedback-derived state rather than artifact presence.

## Current disposition

**Proceed only as a narrow feasibility/falsification experiment, not as a novelty demonstration.**

The development baseline-skew screen remains useful because it tests whether the selected task material has room to reveal a feedback-dependent effect. If the task material is already dominated by generic model behavior or static heuristic C, drop it before sealed evaluation.

## Sources reviewed

- Zhao et al., *Do LLMs Recognize Your Preferences? Evaluating Personalized Preference Following in LLMs* (ICLR 2025 / PrefEval).
- Wu et al., *Aligning LLMs with Individual Preferences via Interaction* (COLING 2025).
- Kim et al., *CUPID: Evaluating Personalized and Contextualized Alignment of LLMs from Interactions* (COLM 2025).
- Bo et al., *Steerable Chatbots: Personalizing LLMs with Preference-Based Activation Steering* (2025).
- Mehri et al., *Learning User Preferences Through Interaction for Long-Term Collaboration* (2026 / MultiSessionCollab).
- Hao et al., *User Preference Modeling for Conversational LLM Agents: Weak Rewards from Retrieval-Augmented Interaction* (2026 / VARS).
- Liang et al., *Learning Personalized Agents from Human Feedback* (2026 / PAHF).
- Li et al., *PrefIx: Understand and Adapt to User Preference in Human-Agent Interaction* (ACL Findings 2026).
- Dong et al., *Value of Information: A Framework for Human-Agent Communication* (ACL 2026).
