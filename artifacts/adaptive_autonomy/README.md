# Adaptive Autonomy / Human Control-Burden Study

**Status:** RESEARCH REFRAME — not frozen, not executed.

This branch supersedes the earlier working interpretation of Experiment 3 as primarily an `Online Interaction Policy Learning` study.

## Why the reframe

Related-work collision checks found substantial prior work on:

- learning user preferences from interaction and feedback;
- persistent and context-sensitive personalization;
- interaction-behavior preferences;
- user-effort reduction from personalization;
- deciding when to ask vs act under ambiguity/risk;
- preference selectivity and over-personalization;
- long-horizon personalized safety.

Therefore this project should **not** claim novelty for those components.

## Remaining research target

The narrower question is:

> **As an adaptive AI takes over more interaction decisions and the user supplies less explicit control, how much user operating burden can be removed before trajectory integrity, context selectivity, epistemic boundaries, or authorization boundaries degrade?**

The research object is the joint relationship among:

`adaptive autonomy <-> human control burden <-> trajectory integrity`

The goal is not to invent another personalization algorithm. A known or deliberately minimal adaptive mechanism may be sufficient as an experimental vehicle.

## What a useful result could be

1. **Safe burden-reduction region:** adaptive autonomy measurably reduces explicit user control while preserving the frozen trajectory/guardrail criteria.
2. **Mechanism without product utility:** adaptation changes behavior, but does not materially reduce burden.
3. **Control-burden tradeoff:** burden falls only when overreach or trajectory defects increase.
4. **No adaptive advantage:** a simple static heuristic matches the adaptive condition.
5. **N=1 control-loop dependence:** benefit appears to rely materially on active participant monitoring/correction and therefore does not yet support ordinary-user productization.

All five are informative outcomes.

## Relation to earlier artifacts

The existing `artifacts/interaction_policy/` materials remain provenance for how this reframe was reached. They are not deleted or rewritten as if the earlier hypothesis never existed.

Reusable pieces include:

- A/B/C comparator structure;
- ON/SHAM/OFF mechanism ablation;
- operating-burden metric;
- trajectory-quality and critical-defect gates;
- policy-state isolation and leakage controls;
- prospective freeze discipline.

However, learning triads are now **measurement vehicles**, not evidence of a novel personalization mechanism.

## Next action

Before implementation, revise the falsification contract around the new primary research question. Then determine whether the existing development tasks actually span a useful autonomy/control-burden range. Do not run a sealed experiment under the old novelty framing.
