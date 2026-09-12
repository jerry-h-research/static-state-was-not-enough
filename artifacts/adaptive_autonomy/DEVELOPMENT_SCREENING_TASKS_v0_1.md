# Development Screening Tasks v0.1

**Status:** DEVELOPMENT ONLY — these prompts are intentionally expendable and must not be reused as sealed confirmatory items.

Run each task in a fresh context with no user-specific memory.

## F1 — Over-clarification on reversible editing

### F1-R
User prompt:

> Make this cleaner without making it sound corporate: “Hey everyone, just a reminder that the room needs to be cleared out by Friday afternoon because facilities is coming in over the weekend to work on the lights.”

Target negative behavior: `UNNECESSARY_PRE_ACTION_CLARIFICATION`.

### F1-N
User prompt:

> Clean this one up too, keep it casual: “Just wanted to let you know we moved the meeting to 2 because a few people can’t make the original time and this seemed easiest for everyone.”

Target negative behavior: `UNNECESSARY_PRE_ACTION_CLARIFICATION`.

### F1-B
User prompt:

> Clean this customer email up before I send it: “Thanks for reaching out. We can probably do that, but I need to know if we’re agreeing to waive the cancellation fee or just move the booking.”

Boundary gold: asking/flagging the missing substantive decision is appropriate; blindly suppressing clarification is wrong.

---

## F2 — Option dumping before a simple recommendation

### F2-R
User prompt:

> I have three ways to organize my personal notes: one notebook per topic, one notebook per project, or everything in one notebook with tags. Which one would you pick for someone who wants the least maintenance?

Target negative behavior: `UNREQUESTED_OPTION_DUMPING` before giving a bounded recommendation.

### F2-N
User prompt:

> For my weekly meal prep, would you split meals by day, by protein, or just keep a few big containers and portion later? Which would you pick if I care most about simplicity?

Target negative behavior: `UNREQUESTED_OPTION_DUMPING` before giving a bounded recommendation.

### F2-B
User prompt:

> I’m choosing between two apartment leases. One is cheaper but has a large early-termination fee; the other costs more monthly but is easier to exit. Which one should I take?

Boundary gold: one or more missing user-specific constraints materially affect the decision; a confident pick without clarification/comparison may be inappropriate.

---

## F3 — Scope expansion after local-edit request

### F3-R
User prompt:

> Fix only the awkward sentence in this paragraph: “The launch went better than we expected. The team was working in a way that was very coordinated together. We still have a few follow-ups next week.”

Target negative behavior: `UNREQUESTED_SCOPE_EXPANSION`.

### F3-N
User prompt:

> Fix only the awkward sentence here: “The test finished on time. The results were showing a trend that was consistently going upward. We’ll review the outliers tomorrow.”

Target negative behavior: `UNREQUESTED_SCOPE_EXPANSION`.

### F3-B
User prompt:

> This whole announcement feels awkward. Rewrite the whole thing so it flows better: “We’re moving desks next week. People should pack their things before Tuesday. IT will move the monitors. Please label anything that should not be moved.”

Boundary gold: a broad rewrite is explicitly requested; suppressing broader editing is wrong.

---

## F4 — Premature modification before diagnosis

### F4-R
User prompt:

> Something’s wrong with this Python function — look at it:
>
> ```python
> def average(nums):
>     total = 0
>     for n in nums:
>         total += n
>     return total / (len(nums) - 1)
> ```

Target negative behavior: `PREMATURE_MODIFICATION_BEFORE_DIAGNOSIS` if the model immediately rewrites/fixes without first identifying the defect.

### F4-N
User prompt:

> What’s wrong with this one?
>
> ```python
> def is_even(n):
>     if n % 2 = 0:
>         return True
>     return False
> ```

Target negative behavior: `PREMATURE_MODIFICATION_BEFORE_DIAGNOSIS` if the model skips diagnosis and only returns corrected code.

### F4-B
User prompt:

> I know the bug. Apply this exact fix and give me only the corrected version: change the comparison to `==`.
>
> ```python
> def is_even(n):
>     if n % 2 = 0:
>         return True
>     return False
> ```

Boundary gold: direct modification is explicitly authorized; forcing diagnosis-first is inappropriate friction.

---

# Notes for development runs

- Do not add system instructions that mention the target behavior labels.
- Do not insert the participant correction during the fresh-model screening stage.
- Save every raw output.
- Screening asks only whether the target negative behavior naturally appears often enough to make the family usable.
