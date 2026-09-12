# Canonical Renderer / Updater Boundary v0.1 — DRAFT

The adaptive policy state must be rendered identically on every evaluation invocation. No learned free-form prose is permitted.

## Renderer

For each active entry, emit exactly these fields in this order:

`ENTRY_ID | CONTEXT_CLASS | DECISION | OUTCOME | SCOPE | CONFIDENCE | EXCEPTION | REVISION_OF`

Entries are sorted by `ENTRY_ID`. Missing `REVISION_OF` is rendered as `NONE`. No explanation, rationale, task text, factual proposition, or natural-language paraphrase may be appended.

A fixed header may explain the controlled vocabulary once. The header itself is identical for STATE-ON and STATE-SHAM and is frozen before evaluation.

## Context selection

The context classifier may choose only from the vocabulary frozen in `POLICY_STATE_SCHEMA.json`. It may not create a new category from evaluation-task semantics.

## Updater input

The updater may receive only the current permitted interaction record, normalized model interaction decision, participant feedback under the frozen response protocol, and current policy state.

It must not receive task gold, future tasks, condition-comparison results, hidden assay labels, final coding, or branch disposition.

## Audit rule

Every mutation emits an append-only log containing prior-state hash, normalized updater inputs, operation (`ADD`, `REVISE`, `MARK_EXCEPTION`, `NO_UPDATE`), resulting-state hash, and timestamp/order index.
