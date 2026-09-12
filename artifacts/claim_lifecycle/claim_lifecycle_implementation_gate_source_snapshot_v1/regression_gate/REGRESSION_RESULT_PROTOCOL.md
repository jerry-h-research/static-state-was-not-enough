# Structured Regression-Result Protocol

## Purpose and authority

This protocol defines machine-readable results for all new Claim Lifecycle regression and adversarial suites beginning with Round 8. Structured output prevents future gates from depending on expanding collections of human prose formats.

Human-readable stdout remains useful diagnostic evidence, but it is diagnostic only. The structured marker payload is the machine-authoritative suite result.

Historical Round 1–7 suites remain immutable and legacy-compatible. The universal gate must retain its legacy text adapters for those artifacts. New Round 8+ suites should emit this protocol natively.

## Marker

A compliant suite must emit exactly one stdout line beginning with:

```text
REGRESSION_RESULT_JSON:
```

One valid compact JSON object must immediately follow the colon on the same line. Diagnostic output may appear before the marker. A suite must not emit a second marker line.

Canonical form uses UTF-8, sorted object keys, and compact JSON separators:

```text
REGRESSION_RESULT_JSON:{"classifications":{},"counts":{"total":{"failed":0,"passed":1,"total":1}},"engine":"src/claim_lifecycle_v0_1_4_13_R5A1.py","schema_version":1,"status":"PASS","suite_id":"example.suite","verdict":null}
```

## Schema version 1

Every result object contains these fields:

| Field | Requirement |
|---|---|
| `schema_version` | Integer `1`. Boolean values are invalid. |
| `suite_id` | Non-empty string matching the suite ID in `REGRESSION_MANIFEST.json`. |
| `engine` | Non-empty repository-relative engine path or stable engine identifier. |
| `status` | Exactly `PASS` or `FAIL`. |
| `counts` | Object containing every metric relevant to the suite. |
| `verdict` | Structured verdict object or `null`. |
| `classifications` | Object containing explicit classification totals where applicable. |

Additional top-level diagnostic fields may be included if they are valid JSON. Consumers must use `schema_version` to select protocol semantics.

### Counts

Pass/fail metrics use:

```json
{
  "passed": 10,
  "total": 10,
  "failed": 0
}
```

All three values are nonnegative integers; booleans are invalid. The invariant is:

```text
passed + failed == total
```

An inherently scalar metric may be a nonnegative integer, for example:

```json
{
  "contract_robustness_observation": 0,
  "invalid_unreachable_setup": 0,
  "invalid_unjustified_metamorphic_relation": 0
}
```

### Verdict

Suites with a verdict use:

```json
{
  "label": "ROUND 8 FINAL VERDICT",
  "value": "NO REACHABLE CORE BYPASS CONFIRMED IN THIS BATCH"
}
```

Both values are non-empty strings. Suites without a verdict use `null`. Gates compare this object structurally and do not parse verdict prose.

### Classification mapping

New adversarial suites use these stable keys:

| Machine key | Human-readable classification |
|---|---|
| `core_pass` | `PASS (blocked/safe)` |
| `core_fail` | `FAIL (reachable core bypass)` |
| `expected_rejection` | `EXPECTED REJECTION` |
| `contract_robustness_observation` | `CONTRACT / ROBUSTNESS OBSERVATION` |
| `invalid_unreachable_setup` | `INVALID TEST / UNREACHABLE SETUP` |
| `invalid_unjustified_metamorphic_relation` | `INVALID TEST / UNJUSTIFIED METAMORPHIC RELATION` |

Classification values are nonnegative integer totals; booleans are invalid. Non-adversarial suites may use an empty `classifications` object.

## Example PASS result

```json
{
  "schema_version": 1,
  "suite_id": "adversarial.example",
  "engine": "src/claim_lifecycle_v0_1_4_13_R5A1.py",
  "status": "PASS",
  "counts": {
    "core": {
      "passed": 3,
      "total": 3,
      "failed": 0
    },
    "expected_rejection": {
      "passed": 1,
      "total": 1,
      "failed": 0
    }
  },
  "verdict": {
    "label": "EXAMPLE FINAL VERDICT",
    "value": "NO REACHABLE CORE BYPASS CONFIRMED IN THIS BATCH"
  },
  "classifications": {
    "core_pass": 3,
    "core_fail": 0,
    "expected_rejection": 1,
    "contract_robustness_observation": 0,
    "invalid_unreachable_setup": 0,
    "invalid_unjustified_metamorphic_relation": 0
  }
}
```

## Example FAIL result

```json
{
  "schema_version": 1,
  "suite_id": "adversarial.example",
  "engine": "src/claim_lifecycle_v0_1_4_13_R5A1.py",
  "status": "FAIL",
  "counts": {
    "core": {
      "passed": 2,
      "total": 3,
      "failed": 1
    }
  },
  "verdict": {
    "label": "EXAMPLE FINAL VERDICT",
    "value": "REACHABLE CORE BYPASS CANDIDATE(S) CONFIRMED"
  },
  "classifications": {
    "core_pass": 2,
    "core_fail": 1,
    "expected_rejection": 0,
    "contract_robustness_observation": 0,
    "invalid_unreachable_setup": 0,
    "invalid_unjustified_metamorphic_relation": 0
  }
}
```

## Helper API

Future suites should import:

```python
from regression_result import emit_result, validate_result
```

`validate_result(result)` raises `ResultValidationError` for malformed schema-version-1 data. `emit_result(result)` validates, emits deterministic compact JSON after the marker, and rejects a second emission in the same process.

## Fail-closed rule

When a manifest entry requires structured output, a missing marker, multiple markers, malformed JSON, schema mismatch, suite-ID mismatch, engine mismatch, invalid counts, invalid verdict, invalid classifications, or mismatch against manifest expectations must fail that suite. Process exit code alone is never sufficient evidence.

The current universal gate already recognizes one marker payload and reads structured `counts` and `verdict` values. Full protocol enforcement—including exactly-one-marker validation and the remaining identity/schema fields—belongs in a future small generic gate compatibility patch when the first manifest suite declares structured output. Historical legacy parsing must remain available.

## Versioning

Backward-compatible clarifications may retain schema version 1. Any incompatible change to required fields, field meanings, count semantics, verdict semantics, or classification semantics requires incrementing `schema_version`. Gates must reject unsupported schema versions rather than guessing.
