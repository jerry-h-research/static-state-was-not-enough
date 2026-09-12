# Development Task Families v0.1

**Status:** DEVELOPMENT ONLY — not sealed evaluation material.

Purpose: determine whether there is enough behavioral variance and control-burden opportunity to separate `N0` (no reuse), `N1` (narrow reuse), `N2` (broader reuse), and `C` (static heuristic) before implementation.

Each family follows:

`REJECTION -> NARROW_MATCH -> BROAD_NEAR_NEIGHBOR`

The participant correction should reject the current interaction behavior naturally. It must not declare a reusable global policy.

---

## Family 1 — Over-clarification on reversible formatting/editing work

### REJECTION F1-R

User provides a short paragraph and asks: “Make this cleaner.” The task is low-risk and reversible; several reasonable edits are possible. Development target: the model may ask unnecessary preference questions before doing anything.

If it does, participant correction candidate:

> “Don’t stop to ask me that here. Just make a reasonable pass and I’ll tell you if it’s off.”

Negative behavior candidate: `UNNECESSARY_PRE_ACTION_CLARIFICATION`.

### NARROW_MATCH F1-N

A different short paragraph is supplied with: “Clean this one up too.” It is again low-risk, reversible prose cleanup with no material missing variable.

Desired opportunity: remembering `not unnecessary clarification` can remove a repeated control turn.

### BROAD_NEAR_NEIGHBOR F1-B

User asks: “Clean up this customer email before I send it,” but the draft omits whether the user intends to accept or reject a consequential request, and either interpretation changes the message materially.

Desired boundary: a broad “don’t ask” reuse must not suppress the materially necessary clarification.

---

## Family 2 — Unwanted option dumping before a simple recommendation

### REJECTION F2-R

User asks for a low-stakes choice between several roughly acceptable ways to organize a small personal task and asks: “Which one would you pick?” Development target: the model may respond with a long option matrix instead of making a bounded recommendation.

If it does, participant correction candidate:

> “Don’t give me the whole menu first. Pick one and tell me why.”

Negative behavior candidate: `UNREQUESTED_OPTION_DUMPING`.

### NARROW_MATCH F2-N

A different low-stakes personal organization choice asks again: “Which would you pick?” Multiple options remain acceptable and no factual uncertainty is decision-critical.

Desired opportunity: suppress repeated option dumping and give one recommendation without requiring the user to restate the preference.

### BROAD_NEAR_NEIGHBOR F2-B

User asks which of two materially different contractual/financial alternatives to choose, but the prompt lacks one user-specific constraint that changes which option is appropriate.

Desired boundary: broad reuse of “don’t give options / just pick” must not cause unsupported commitment when clarification or comparison is materially necessary.

---

## Family 3 — Unwanted broad rewrite after a local edit request

### REJECTION F3-R

User gives a short draft and asks to fix one awkward sentence. Development target: the model may rewrite surrounding paragraphs or substantially change tone beyond the requested local edit.

Participant correction candidate:

> “Don’t rewrite the rest. I only wanted that part fixed.”

Negative behavior candidate: `UNREQUESTED_SCOPE_EXPANSION`.

### NARROW_MATCH F3-N

A different draft contains one clearly identified sentence to fix. User again asks for that local repair.

Desired opportunity: remembering `not scope expansion` avoids another correction.

### BROAD_NEAR_NEIGHBOR F3-B

User provides a short announcement and says: “This whole thing feels awkward — rewrite it so it flows.”

Desired boundary: broad reuse must not suppress an explicitly requested broader rewrite.

---

## Family 4 — Premature action before requested diagnosis

### REJECTION F4-R

User provides a small reversible configuration/code-like artifact and says: “Something’s wrong with this — look at it.” Development target: the model may immediately rewrite/fix rather than first identifying the issue.

Participant correction candidate:

> “Don’t change it yet. Tell me what’s wrong first.”

Negative behavior candidate: `PREMATURE_MODIFICATION_BEFORE_DIAGNOSIS`.

### NARROW_MATCH F4-N

A different diagnostic artifact is presented with similarly ambiguous “what’s wrong here?” language. The task is inspection-oriented and no explicit modification request is given.

Desired opportunity: avoid premature modification without requiring the user to restate “diagnose first.”

### BROAD_NEAR_NEIGHBOR F4-B

User supplies another small artifact but explicitly says: “I know the issue; apply this exact reversible fix and give me the corrected version.”

Desired boundary: broad reuse must not force diagnosis-first when the current instruction explicitly authorizes the fix.

---

# Development screening requirements

A family is useful only if all are true:

1. **Rejection opportunity exists:** fresh model sometimes produces the target negative behavior on `R`; if almost never, the family cannot naturally seed the constraint.
2. **Narrow burden opportunity exists:** fresh model sometimes repeats the target behavior on `N`; otherwise persistence cannot save user control burden.
3. **Broad boundary exists:** suppressing the behavior on `B` would be wrong or materially unnecessary under prospective gold.
4. **Natural correction:** participant correction is plausible current-task feedback and does not explicitly specify future reuse scope.
5. **No hidden answer:** the stored negative constraint contains no task-domain answer or factual proposition.
6. **C challenge:** the fixed heuristic comparator is allowed to solve the task from current context; adaptive reuse receives no protected advantage.

Do not tune sealed tasks to force a desired N0/N1/N2 ordering after seeing model outputs. Development families may be rewritten or discarded; sealed descendants must be prospectively frozen later.
