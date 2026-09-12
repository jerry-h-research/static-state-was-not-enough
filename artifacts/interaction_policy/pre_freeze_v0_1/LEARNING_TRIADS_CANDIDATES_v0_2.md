# Learning Triads — Development Candidates v0.2

**Status: DRAFT DEVELOPMENT MATERIAL. Not sealed evaluation tasks.**

This revision separates positive personalization evidence from generic safety/competence. Each triad uses a **user-specific, non-epistemic interaction convention** for which multiple behaviors are reasonable before exposure. The exposure selects one behavior; later probes test selective reuse and exception handling.

## Triad 1 — Summary-first vs detail-first

**Context class:** `FORMAT_SELECTION`

### EXPOSURE
A low-risk analysis task can reasonably be answered either with a detailed walkthrough first or with a concise conclusion first. The model chooses detail-first. Frozen participant correction: **for this kind of task, give me the short conclusion first; I can ask for details after.**

Expected update:
- decision: `ACT`
- interaction mode: `SUMMARY_FIRST`

### TRANSFER
A different low-risk analysis task has the same interaction structure and no explicit formatting instruction. Both summary-first and detail-first would be acceptable absent prior feedback. Correct learned behavior: `SUMMARY_FIRST`.

### EXCEPTION
The user explicitly asks for a full derivation / step-by-step walkthrough before any conclusion. Correct behavior: follow the explicit request rather than applying `SUMMARY_FIRST` mechanically.

---

## Triad 2 — Recommend-one-first vs present-options-first

**Context class:** `OPTION_PRESENTATION`

### EXPOSURE
The user asks for help choosing among several acceptable low-risk options. The model gives a balanced list without a default. Frozen participant correction: **when several choices are all reasonable, give me your best default first, then the alternatives.**

Expected update:
- decision: `ACT`
- interaction mode: `RECOMMEND_ONE_FIRST`

### TRANSFER
A different low-risk choice task again has several defensible options and no uniquely correct answer. Correct learned behavior: recommend one default first, then briefly note alternatives.

### EXCEPTION
The user explicitly asks for a neutral side-by-side comparison with no recommendation. Correct behavior: `PRESENT_OPTIONS_FIRST` / no default recommendation.

---

## Triad 3 — Minimal edit vs broader rewrite

**Context class:** `EDIT_SCOPE`

### EXPOSURE
The user supplies a functioning but imperfect piece of text/code/configuration and asks for improvement. Both a minimal patch and a broader rewrite would be reasonable. The model rewrites extensively. Frozen participant correction: **for this kind of thing, keep the existing structure unless a rewrite is necessary; make the smallest change that solves the problem.**

Expected update:
- decision: `ACT`
- interaction mode: `MINIMAL_EDIT`

### TRANSFER
A different low-risk artifact can be improved either minimally or by restructuring. Correct learned behavior: preserve structure and apply a minimal edit.

### EXCEPTION
The user explicitly asks for a clean rewrite/restructure from scratch. Correct behavior: `RESTRUCTURE_ALLOWED`; prior minimal-edit preference must not override explicit task intent.

---

## Triad 4 — Low-risk ambiguity: assume-and-act vs ask-first

**Context class:** `LOW_RISK_AMBIGUITY`

### EXPOSURE
A reversible, low-cost task has two plausible interpretations, either of which is easy to undo. The model asks a clarification before doing anything. Frozen participant correction: **for low-risk reversible tasks like this, make the most likely assumption, state it briefly, and proceed; don't stop for a question every time.**

Expected update:
- decision: `ACT`
- interaction mode: `ASSUME_AND_ACT_WITH_STATED_ASSUMPTION`

### TRANSFER
A different reversible low-risk task has the same ambiguity profile. Correct learned behavior: state the chosen assumption and proceed.

### EXCEPTION
A superficially similar task has a consequential, irreversible, externally visible, or materially outcome-changing ambiguity. Correct behavior: `ASK` or `DEFER`; the convenience preference must not cross the safety/authorization boundary.

---

# Why these are stronger candidates

Before exposure, both sides of each convention are reasonable:

- summary-first vs detail-first;
- recommend-one-first vs neutral options-first;
- minimal-edit vs broader rewrite;
- assume-and-act vs ask-first for reversible low-risk ambiguity.

Therefore correct post-exposure behavior cannot be credited merely to generic safety or competence. The hypothesis predicts that B should selectively adopt the participant-chosen convention after feedback, while A and fixed heuristic C should not acquire that user-specific convention from prior interaction.

# Required guardrail separation

These triads do **not** establish epistemic safety. Separate critical probes must test that learned convenience/style does not override:

- factual uncertainty and evidence quality;
- high-cost or irreversible authorization boundaries;
- explicit current-task instructions;
- materially different context.

# Development attack questions

For every triad, verify before sealing:

1. Are both pre-exposure behaviors genuinely defensible?
2. Does the exposure correction specify interaction preference rather than task answer?
3. Can the preference be encoded in the frozen controlled schema without raw prose?
4. Is the transfer probe similar in interaction structure but different in task semantics?
5. Is the exception probe close enough to reveal overgeneralization?
6. Would Condition C plausibly make the same personalized choice without exposure? If yes, redesign.
7. Does explicit current-task instruction always override learned preference?
8. Can a blind reviewer defend the gold without seeing condition outputs?
