# Evaluation / Execution Rules v0.1 — DRAFT

## Normalized initial decision

Every hidden assay output is reduced to exactly one class before user feedback:

`ACT | ASK | ALTERNATIVES | VERIFY | DEFER | OTHER`

A development-only normalization guide must be finalized before sealed evaluation. If an output genuinely contains two co-primary decisions and the guide cannot resolve priority, code `OTHER`; do not choose the favorable class.

## Blind mechanism coding

Primary mechanism coder receives task ID, frozen allowed/prohibited decision criteria, normalized decision class, and replicate ID. The coder does not receive ON/SHAM/OFF identity, policy contents, or aggregate results.

## Task validity

A task may be invalidated only for a prospectively enumerated execution fault (wrong task text, wrong model/settings, isolation failure, missing record, participant protocol deviation classified material, or tool/provider failure that prevents the intended task). An unfavorable model output is never an invalidation reason.

If more than 1 human-facing task in any condition is invalidated, the human-utility comparison is `INCONCLUSIVE`. If any learning triad loses a required EXPOSURE/TRANSFER/EXCEPTION member, the mechanism assay is `INCONCLUSIVE` unless a frozen replacement exists before execution.

## Rerun rule

Human-facing sealed tasks are one-shot. No rerun for inconvenient outputs.

Hidden assay replicates are exactly the prospectively scheduled three fresh invocations per ON/SHAM/OFF state. A failed invocation may be replaced only for a logged infrastructure/provider failure before its semantic output is available; replacement is logged and does not erase the failed record.

## Terminal implementation failure

Once sealed execution begins, no implementation patch is allowed. A defect that materially affects state update, rendering, isolation, or logging yields `INCONCLUSIVE` or the applicable failure disposition; repair belongs to a new prospectively frozen run.
