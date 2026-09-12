# Live Provider / Model Selection Gate v0.1

**Status:** PRE-LIVE DESIGN GATE. No provider/model is authorized yet.

The development screening runner passed dry-run review. Before any live screening call is authorized, the exact provider/model configuration must satisfy all requirements below and be written into a frozen run config.

## Required properties

1. **Programmatic fresh invocation:** each call can be issued as a new stateless request with no conversation carryover.
2. **No provider-side personalization/memory:** memory/personalization must be disabled, absent, or demonstrably not part of the API request path.
3. **Stable model identity:** use an immutable snapshot/version when available. If only a rolling alias exists, record that limitation before the run and do not mix dates/aliases across the same screening package.
4. **Exact settings recorded:** all supported sampling/reasoning/output settings used by the provider must be logged. Unsupported settings must remain absent rather than silently emulated.
5. **No hidden research prompt:** model input is exactly the task user prompt plus only provider-required transport fields. No rubric, gold, family label, prior output, or research explanation may be sent.
6. **Raw semantic response preserved:** save provider output text unchanged before any coding/classification.
7. **No automatic semantic retry:** a provider/network failure stops the run under the existing runner rule; an inconvenient semantic answer is never retried.
8. **One adapter instance per invocation:** no local conversation/session object may be reused between calls.
9. **Usage/accounting metadata logged separately:** request ID, reported model ID/version, token usage, and provider timestamps may be logged outside model-visible content when available.
10. **Credential isolation:** API keys/tokens come from environment or local secret storage and are never written to repository files, manifests, raw outputs, or committed evidence.

## Sampling requirement

This is a behavioral-variance development screen, so the chosen settings must not intentionally force deterministic identical outputs unless the target model itself only supports deterministic behavior. The exact supported sampling controls, if any, are provider-specific and must be frozen after adapter selection.

Ten replicates estimate observed behavior frequency under one fixed configuration; they are not statistical population estimates.

## Selection record required before live authorization

Create a run-selection record containing:

- provider;
- API/SDK endpoint family;
- exact model identifier requested;
- exact model identifier returned/reported, if available;
- snapshot/version semantics;
- all request settings;
- whether provider-side memory exists on this API path and how it is excluded;
- credential source (e.g. environment variable name only, never value);
- date/time window in which all 120 calls will be completed;
- cost/rate-limit notes;
- adapter file SHA and test SHA.

## Current disposition

`LIVE_SCREENING_AUTHORIZED = NO`

The next authorized action is adapter implementation and offline conformance testing for a selected provider/model. No live research-model call is authorized by this document.
