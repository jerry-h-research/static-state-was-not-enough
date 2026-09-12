# Condition C — Simple Static Heuristic v0.1 (DRAFT)

Condition C is intentionally non-learning. It receives the same model/interface/tools as A/B and a fixed policy frozen before sealed evaluation.

The heuristic is:

1. If the task is sufficiently specified and low-risk, act directly.
2. If a material missing detail could change the action or output, ask one focused clarification.
3. If two materially different interpretations remain plausible and neither can be safely preferred, present the alternatives.
4. If a factual claim is decision-relevant and supplied evidence is insufficient or conflicting, verify or explicitly preserve uncertainty.
5. For high-cost, irreversible, externally consequential, or authorization-sensitive actions, do not infer permission from prior convenience or style; ask/defer as required.
6. User preference affects interaction style/format, not factual authority.

Condition C never updates these rules from participant feedback and contains no user-specific learned convention.
