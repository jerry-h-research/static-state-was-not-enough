# Research Note — Selective-Correction Interaction Pattern

**Date:** 2026-09-12
**Status:** motivating observation / design input, not an established mechanism.

The motivating long-running interaction is not well described by explicit preference declaration. The participant reports that they generally do not proactively state reusable preferences such as “I prefer this response style in similar tasks.” Instead, they observe the model response and explicitly reject/correct it when it is bad enough to warrant intervention. Acceptable responses are usually followed by continuation rather than explicit endorsement.

This creates asymmetric observable feedback:

- negative feedback/correction is often explicit;
- positive preference endorsement is often absent;
- continuation without correction may be compatible with acceptance, indifference, inattention, low importance, or unnoticed error.

Therefore:

`non-rejection != explicit acceptance`

but treating all non-rejection as permanently zero information may also fail to represent the natural interaction process.

A candidate framing for study design is **selective-correction / rejection-driven calibration**: candidate interaction conventions are proposed by system behavior; explicit rejection removes or narrows them; repeated non-rejection under comparable, observable correction opportunities may provide only weak survival evidence.

This note does not claim that the described process is novel, causal, or sufficient to explain the existing long-running pair. It exists to prevent the experiment from requiring an artificial explicit-preference protocol that would recreate prompt engineering rather than model the motivating interaction.
