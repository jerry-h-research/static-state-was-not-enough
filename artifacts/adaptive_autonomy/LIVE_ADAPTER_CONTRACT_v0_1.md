# Live Adapter Contract v0.1

**Status:** DRAFT CONTRACT — provider-specific adapter not yet implemented.

The existing screening runner owns scheduling, isolation, output reservation, stop-on-failure behavior, and raw-output persistence. The provider adapter must remain deliberately thin.

## Adapter interface

The adapter factory returns a fresh callable for one invocation only.

Input schema:

```json
{
  "model": "exact requested model identifier",
  "model_version": "frozen version/snapshot record",
  "settings": {},
  "messages": [
    {"role": "user", "content": "exact screening prompt"}
  ]
}
```

Output:

- exactly one complete semantic response string;
- no classification, normalization, rewriting, summarization, or retry.

## Forbidden adapter behavior

The adapter must not:

- add system/developer/research instructions;
- add task IDs, family labels, gold, rubric, or coding instructions to model-visible input;
- reuse a conversation/thread/session across invocations;
- persist provider response text into provider memory;
- fetch previous runs to inform the next call;
- retry because the response is undesirable, short, long, surprising, or semantically inconvenient;
- silently switch model identifiers;
- silently alter sampling/reasoning settings;
- expose API credentials in logs or exception text written to evidence;
- classify the response before the raw semantic text has been durably saved.

## Required adapter behavior

The adapter must:

1. construct one fresh provider request per factory instance;
2. transmit only the exact user prompt plus provider-required transport parameters;
3. request the frozen model/configuration exactly;
4. return the provider semantic text unchanged;
5. expose separately loggable non-semantic metadata when available without mixing it into raw output;
6. surface provider/network errors to the runner so the existing stop-on-first-failure rule applies;
7. verify that credentials exist before a live call but never print their value;
8. make absence of a requested immutable model/version a hard preflight failure rather than falling back.

## Preflight

Before any 120-call authorization, adapter-specific offline tests must prove:

- exact payload construction;
- no hidden prompt fields;
- fresh client/session construction;
- credential redaction;
- no semantic retry;
- model mismatch/fallback rejection;
- raw text passthrough;
- provider metadata separated from semantic output;
- failure propagation to the runner.

A single optional **connectivity/model-identity probe** may later be separately authorized after review. Such a probe is not part of the 120 screening outputs and must be logged as infrastructure validation only.

## Authorization boundary

Implementing and offline-testing an adapter does **not** authorize network use.

`ADAPTER_IMPLEMENTATION = ALLOWED AFTER PROVIDER SELECTION`

`CONNECTIVITY_PROBE = NOT YET AUTHORIZED`

`120_CALL_SCREENING = NOT YET AUTHORIZED`
