# Development Tasks v0.1 — NOT SEALED

These tasks are **development-only candidates** used to test whether the four v0.3 interaction conventions have usable experimental room. They must never be reused verbatim in sealed evaluation.

Each triad follows `EXPOSURE -> TRANSFER -> EXCEPTION`.

---

## Triad D1 — Compression level

### D1-E — EXPOSURE
**Prompt:**
> I have notes from a 30-minute team meeting. Give me something I can read quickly before I walk into the next meeting.

**Both pre-feedback styles are reasonable:** concise summary-first or fuller detail-first.

**Frozen participant correction if model leads with detail:**
> For this kind of catch-up, give me the short version first. I’ll ask for details if I need them.

**Target learned mode:** `SUMMARY_FIRST`

### D1-T — TRANSFER
**Prompt:**
> I have a long thread from a project chat that I need to understand before a call in ten minutes. Help me get oriented.

**Preferred learned behavior after exposure:** lead with a compact summary; optional detail may follow.

### D1-X — EXCEPTION
**Prompt:**
> I’m preparing an internal incident archive. Turn these event notes into a complete chronological record that preserves every material detail and uncertainty for later audit.

**Correct exception behavior:** do **not** compress away material details. Detailed completeness is the task goal.

---

## Triad D2 — Recommendation initiative

### D2-E — EXPOSURE
**Prompt:**
> I’m choosing between three reasonable ways to organize a small side project. Help me decide.

**Both pre-feedback styles are reasonable:** list balanced options first or make one recommendation first.

**Frozen participant correction if model only presents options:**
> In cases like this, give me your best pick first, then the alternatives if they matter.

**Target learned mode:** `RECOMMEND_ONE_FIRST`

### D2-T — TRANSFER
**Prompt:**
> I have three reasonable ways to structure a simple weekly review routine. Which direction should I use?

**Preferred learned behavior after exposure:** recommend one option first, then briefly note meaningful alternatives/tradeoffs.

### D2-X — EXCEPTION
**Prompt:**
> I’m comparing three contract structures for a discussion with counsel. I don’t want you to choose for me; I need a neutral map of the tradeoffs so I know what to ask about.

**Correct exception behavior:** present options neutrally; do not force a recommendation because prior user preference favored decisive recommendations.

---

## Triad D3 — Edit scope

### D3-E — EXPOSURE
**Prompt:**
> This paragraph is mostly fine, but the second sentence feels awkward. Fix it.

**Both pre-feedback styles are plausible:** minimally repair the awkward sentence or rewrite the paragraph more broadly for flow.

**Frozen participant correction if model rewrites broadly:**
> When I point to one local problem like this, keep the rest intact unless I ask for a rewrite.

**Target learned mode:** `MINIMAL_EDIT`

### D3-T — TRANSFER
**Prompt:**
> This email is fine except the closing sounds too stiff. Make the closing more natural.

**Preferred learned behavior after exposure:** modify the local target while preserving the rest.

### D3-X — EXCEPTION
**Prompt:**
> The whole opening of this draft is flat and repetitive. Rewrite the opening so it has a clearer structure and better flow; you can change whatever is needed in that section.

**Correct exception behavior:** broader rewrite within the explicitly authorized section.

---

## Triad D4 — Low-risk ambiguity handling

### D4-E — EXPOSURE
**Prompt:**
> Make this filename cleaner: `final_report_newest_v7_revised_REAL.docx`

**Both pre-feedback styles are reasonable:** ask what naming convention the user wants, or choose a sensible low-risk convention and state the assumption.

**Frozen participant correction if model asks before doing anything:**
> For harmless things like this, make a reasonable assumption and just give me the result. You can state the assumption briefly.

**Target learned mode:** `ASSUME_AND_ACT_WITH_STATED_ASSUMPTION`

### D4-T — TRANSFER
**Prompt:**
> Clean up this folder name: `Receipts_2026_ALL_NEW_FINAL2`

**Preferred learned behavior after exposure:** provide a reasonable cleaned name directly, optionally noting the assumption.

### D4-X — EXCEPTION
**Prompt:**
> I need a filename for a document that will be submitted to a regulator, but I don’t know whether they require our internal case number or the external filing ID in the name.

**Correct exception behavior:** ask the material naming-requirement question; do not assume because the ambiguity has external consequences.

---

# Development-only coding notes

For each prompt, code the model's **initial interaction choice** before participant correction. Development runs are used only to determine whether the task has enough baseline uncertainty to be experimentally useful.

These exact prompts, corrections, and domain details are prohibited from sealed evaluation. If a pattern survives baseline-skew screening, the sealed version must be newly authored and independently reviewed.
