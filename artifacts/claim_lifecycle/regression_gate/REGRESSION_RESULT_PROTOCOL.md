# Structured Regression-Result Protocol

## Purpose and authority

This protocol defines machine-readable results for new Claim Lifecycle regression and adversarial suites beginning with Round 8. Human-readable stdout remains useful diagnostic evidence, but the structured marker payload is the machine-authoritative suite result. Historical Round 1-7 suites remain immutable and legacy-compatible.

## Marker

A compliant suite emits exactly one stdout line beginning with:

```text
REGRESSION_RESULT_JSON:
```

One valid compact JSON object immediately follows the colon on the same line.

## Schema version 1

Required fields:

| Field | Requirement |
|---|---|
| `schema_version` | Integer `1`; booleans invalid |
| `suite_id` | Non-empty string matching the manifest |
| `engine` | Non-empty repository-relative engine path or stable identifier |
| `status` | Exactly `PASS` or `FAIL` |
| `counts` | Object containing relevant metrics |
| `verdict` | Structured verdict object or `null` |
| `classifications` | Explicit classification totals where applicable |

Pass/fail count objects must contain `passed`, `total`, and `failed`, all nonnegative integers, with `passed + failed == total`.

Stable adversarial classification keys include `core_pass`, `core_fail`, `expected_rejection`, `contract_robustness_observation`, `invalid_unreachable_setup`, and `invalid_unjustified_metamorphic_relation`.

## Fail-closed rule

When a manifest entry requires structured output, a missing marker, multiple markers, malformed JSON, schema mismatch, suite-ID mismatch, engine mismatch, invalid counts, invalid verdict, invalid classifications, or mismatch against manifest expectations must fail that suite. Process exit code alone is never sufficient evidence.

The public copy is a concise rendering of the frozen protocol; the original private protocol additionally contains worked PASS/FAIL examples and helper-API documentation.
