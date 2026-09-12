"""Dependency-free structured regression-result validation and emission.

This helper is intended for new regression and adversarial suites. Historical
Round 1-7 suites remain immutable and continue to use the universal gate's
legacy output adapters.
"""

from __future__ import annotations

import json
import sys
from typing import Any, Mapping


SCHEMA_VERSION = 1
MARKER = "REGRESSION_RESULT_JSON:"
REQUIRED_FIELDS = {
    "schema_version",
    "suite_id",
    "engine",
    "status",
    "counts",
    "verdict",
    "classifications",
}

CLASSIFICATION_KEYS = {
    "core_pass",
    "core_fail",
    "expected_rejection",
    "contract_robustness_observation",
    "invalid_unreachable_setup",
    "invalid_unjustified_metamorphic_relation",
}

_emitted = False


class ResultValidationError(ValueError):
    """Raised when a structured regression result violates protocol v1."""


def _is_nonnegative_integer(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _validate_count_metric(name: str, value: Any) -> None:
    if _is_nonnegative_integer(value):
        return
    if not isinstance(value, Mapping):
        raise ResultValidationError(
            f"counts.{name} must be a nonnegative integer or pass/fail count object"
        )
    if set(value) != {"passed", "total", "failed"}:
        raise ResultValidationError(
            f"counts.{name} must contain exactly passed, total, and failed"
        )
    if any(not _is_nonnegative_integer(value[key]) for key in ("passed", "total", "failed")):
        raise ResultValidationError(f"counts.{name} contains an invalid integer")
    if value["passed"] + value["failed"] != value["total"]:
        raise ResultValidationError(
            f"counts.{name} must satisfy passed + failed == total"
        )


def validate_result(result: Any) -> None:
    """Validate one schema-version-1 result or raise ResultValidationError."""

    if not isinstance(result, Mapping):
        raise ResultValidationError("result must be an object")
    missing = sorted(REQUIRED_FIELDS - set(result))
    if missing:
        raise ResultValidationError("missing required field(s): " + ", ".join(missing))

    schema_version = result["schema_version"]
    if isinstance(schema_version, bool) or schema_version != SCHEMA_VERSION:
        raise ResultValidationError(f"schema_version must be {SCHEMA_VERSION}")
    if not isinstance(result["suite_id"], str) or not result["suite_id"].strip():
        raise ResultValidationError("suite_id must be a non-empty string")
    if not isinstance(result["engine"], str) or not result["engine"].strip():
        raise ResultValidationError("engine must be a non-empty string")
    if result["status"] not in {"PASS", "FAIL"}:
        raise ResultValidationError("status must be exactly PASS or FAIL")

    counts = result["counts"]
    if not isinstance(counts, Mapping):
        raise ResultValidationError("counts must be an object")
    for name, value in counts.items():
        if not isinstance(name, str) or not name:
            raise ResultValidationError("count metric keys must be non-empty strings")
        _validate_count_metric(name, value)

    verdict = result["verdict"]
    if verdict is not None:
        if not isinstance(verdict, Mapping) or set(verdict) != {"label", "value"}:
            raise ResultValidationError("verdict must be null or contain exactly label and value")
        if any(not isinstance(verdict[key], str) or not verdict[key] for key in ("label", "value")):
            raise ResultValidationError("verdict label and value must be non-empty strings")

    classifications = result["classifications"]
    if not isinstance(classifications, Mapping):
        raise ResultValidationError("classifications must be an object")
    unknown = sorted(set(classifications) - CLASSIFICATION_KEYS)
    if unknown:
        raise ResultValidationError("unknown classification key(s): " + ", ".join(unknown))
    for key, value in classifications.items():
        if not _is_nonnegative_integer(value):
            raise ResultValidationError(
                f"classifications.{key} must be a nonnegative integer"
            )

    try:
        json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    except (TypeError, ValueError) as exc:
        raise ResultValidationError(f"result is not JSON-serializable: {exc}") from exc


def emit_result(result: Any) -> None:
    """Validate and emit exactly one canonical protocol marker line."""

    global _emitted
    if _emitted:
        raise ResultValidationError("a structured result marker was already emitted")
    validate_result(result)
    payload = json.dumps(
        result,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    sys.stdout.write(MARKER + payload + "\n")
    sys.stdout.flush()
    _emitted = True


__all__ = [
    "CLASSIFICATION_KEYS",
    "MARKER",
    "ResultValidationError",
    "SCHEMA_VERSION",
    "emit_result",
    "validate_result",
]
