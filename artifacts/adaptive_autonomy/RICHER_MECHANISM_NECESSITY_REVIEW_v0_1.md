# Richer-Mechanism Necessity Review v0.1

**Question:** What capability would a richer adaptive mechanism add beyond the scoped blacklist baseline without silently reintroducing positive-preference inference?

## Candidate extra capabilities considered

### 1. Negative-constraint generalization across semantically similar contexts

A richer mechanism could infer that a rejection in one task applies to another task whose context label is not identical.

**Problem:** this requires semantic applicability inference, which is exactly where overgeneralization risk enters. A frozen broader context taxonomy can give the blacklist the same capability without requiring a richer learner.

**Disposition:** not sufficient justification.

### 2. Automatic scope contraction after an exception

A richer mechanism could learn that a negative constraint is broad except for a newly observed exception.

**Problem:** a scoped blacklist can represent explicit exception labels deterministically. If the exception is inferred rather than explicit, the richer mechanism again introduces semantic generalization that must be separately justified.

**Disposition:** representable by simple baseline; not sufficient justification.

### 3. Choosing the best remaining behavior after excluding a rejected one

A richer mechanism could rank alternatives after removing the rejected behavior.

**Problem:** ranking alternatives is positive preference learning unless it is based solely on current-task evidence. The base model can already choose among remaining allowed behaviors from current context.

**Disposition:** do not add as learned cross-task capability.

### 4. Learning combinations/interactions among multiple negative constraints

A richer mechanism could learn that `not A` and `not B` jointly imply C in a context.

**Problem:** this is effectively positive policy induction from negative examples. It may be useful, but it is a different hypothesis and reopens the exact inference/safety problem the current branch intentionally narrowed away from.

**Disposition:** out of scope for first feasibility study.

### 5. Decay / forgetting of stale negative constraints

A richer mechanism could weaken old constraints automatically.

**Problem:** useful for long-horizon preference drift, but unnecessary for a short bounded feasibility study and already related to existing personalization literature.

**Disposition:** defer.

### 6. Confidence weighting of negative constraints

A richer mechanism could distinguish weak vs strong rejections.

**Problem:** unless feedback intensity is explicitly observable under a frozen protocol, confidence becomes model interpretation. For the first test, explicit rejection can be binary.

**Disposition:** defer.

## Review conclusion

No extra capability currently survives the necessity test strongly enough to justify a richer adaptive mechanism for the first bounded experiment.

The simplest defensible experimental vehicle is therefore the **scoped negative-constraint / blacklist mechanism** itself.

This is not a claim that blacklist-style adaptation explains the motivating long-running interaction. It is a deliberate minimal intervention for the narrower question:

> Can reusing explicit negative interaction feedback remove future user-control burden without creating scope overreach or integrity loss?

If even this minimal mechanism cannot show a bounded safe benefit, richer mechanisms are not justified by this branch. If it does show benefit, richer mechanisms may be studied later only when a specific additional capability and failure mode are prospectively defined.
