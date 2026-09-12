"""Manifest-driven universal regression gate.

This gate answers whether current behavior satisfies REGRESSION_MANIFEST.json.
It does not prove repository integrity; that separate trust boundary belongs to
verify_integrity.cmd and the user's locally created integrity baseline.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any

from regression_result import ResultValidationError, validate_result


ROOT = Path(__file__).resolve().parent
MANIFEST_PATH = ROOT / "REGRESSION_MANIFEST.json"
RAW_PATH = ROOT / "GATE_RAW_RESULT.txt"
RESULT_PATH = ROOT / "GATE_RESULT.json"
SUPPORTED_SCHEMA_VERSIONS = {1}
SUPPORTED_EXECUTION_MODES = {
    "direct",
    "in_memory_engine_prefix_retarget",
    "in_memory_engine_filename_retarget",
    "in_memory_engine_filename_retarget_or_direct",
    "in_memory_engine_filename_retarget_derived_source",
}
SUPPORTED_RESULT_PROTOCOLS = {"legacy", "structured_v1"}
STRUCTURED_RESULT_MARKER = "REGRESSION_RESULT_JSON:"

# Explicit generic legacy-output compatibility debt. Future suites can emit a
# JSON object after STRUCTURED_RESULT_MARKER and bypass these prose adapters.
LEGACY_SCALAR_LABELS = {
    "contract_robustness_observation": "CONTRACT / ROBUSTNESS OBSERVATION",
    "invalid_unreachable_setup": "INVALID TEST / UNREACHABLE SETUP",
    "invalid_unjustified_metamorphic_relation": "INVALID TEST / UNJUSTIFIED METAMORPHIC RELATION",
}


class GateError(RuntimeError):
    pass


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_relative_path(value: Any, field: str) -> tuple[str, Path]:
    if not isinstance(value, str) or not value.strip():
        raise GateError(f"{field} must be a non-empty project-relative path")
    pure = PurePosixPath(value.replace("\\", "/"))
    if pure.is_absolute() or ".." in pure.parts or not pure.parts or pure.parts[0] in {"", "."}:
        raise GateError(f"{field} is not a safe project-relative path: {value!r}")
    normalized = pure.as_posix()
    resolved = (ROOT / Path(*pure.parts)).resolve()
    try:
        resolved.relative_to(ROOT)
    except ValueError as exc:
        raise GateError(f"{field} escapes project root: {value!r}") from exc
    return normalized, resolved


def load_manifest() -> dict[str, Any]:
    try:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise GateError("REGRESSION_MANIFEST.json is missing") from exc
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise GateError(f"REGRESSION_MANIFEST.json is invalid: {exc}") from exc
    if not isinstance(manifest, dict):
        raise GateError("manifest root must be a JSON object")
    return manifest


def validate_count(name: str, value: Any) -> None:
    if isinstance(value, bool):
        raise GateError(f"expected_counts.{name} must not be boolean")
    if isinstance(value, int):
        if value < 0:
            raise GateError(f"expected_counts.{name} must be nonnegative")
        return
    if not isinstance(value, dict) or set(value) != {"passed", "total", "failed"}:
        raise GateError(f"expected_counts.{name} must be a count object or nonnegative integer")
    if any(not isinstance(value[k], int) or isinstance(value[k], bool) or value[k] < 0 for k in value):
        raise GateError(f"expected_counts.{name} contains an invalid integer")
    if value["passed"] + value["failed"] != value["total"]:
        raise GateError(f"expected_counts.{name} does not satisfy passed + failed = total")


def validate_manifest(manifest: dict[str, Any]) -> tuple[dict[str, Any], Path]:
    required = {"schema_version", "project", "checkpoint", "engine", "suites", "global_requirements"}
    missing = sorted(required - set(manifest))
    if missing:
        raise GateError("manifest missing field(s): " + ", ".join(missing))
    if manifest["schema_version"] not in SUPPORTED_SCHEMA_VERSIONS:
        raise GateError(f"unsupported schema_version: {manifest['schema_version']!r}")
    if not isinstance(manifest["checkpoint"], str) or not manifest["checkpoint"]:
        raise GateError("manifest checkpoint must be a non-empty string")
    engine_rel, engine_path = safe_relative_path(manifest["engine"], "manifest.engine")
    if not engine_path.is_file():
        raise GateError(f"engine is missing: {engine_rel}")
    suites = manifest["suites"]
    if not isinstance(suites, list) or not suites:
        raise GateError("manifest suites must be a non-empty array")

    seen = set()
    normalized_suites = []
    for index, original in enumerate(suites):
        if not isinstance(original, dict):
            raise GateError(f"suite {index} must be an object")
        suite = dict(original)
        for field in ("id", "path", "execution_mode", "expected_exit_code", "expected_counts",
                      "required_verdict", "retarget_engine_if_needed"):
            if field not in suite:
                raise GateError(f"suite {index} missing field: {field}")
        if not isinstance(suite["id"], str) or not suite["id"] or suite["id"] in seen:
            raise GateError(f"suite {index} has missing or duplicate id: {suite['id']!r}")
        seen.add(suite["id"])
        suite["path"], suite_path = safe_relative_path(suite["path"], f"suite {suite['id']}.path")
        if not suite_path.is_file():
            raise GateError(f"suite file is missing: {suite['path']}")
        if suite["execution_mode"] not in SUPPORTED_EXECUTION_MODES:
            raise GateError(f"suite {suite['id']} has unknown execution_mode: {suite['execution_mode']!r}")
        if suite["execution_mode"] == "in_memory_engine_filename_retarget_derived_source":
            if "source_artifact" not in suite:
                raise GateError(f"suite {suite['id']} missing field: source_artifact")
            suite["source_artifact"], source_artifact_path = safe_relative_path(
                suite["source_artifact"], f"suite {suite['id']}.source_artifact"
            )
            if not source_artifact_path.is_file():
                raise GateError(f"suite source artifact is missing: {suite['source_artifact']}")
        if not isinstance(suite["expected_exit_code"], int) or isinstance(suite["expected_exit_code"], bool):
            raise GateError(f"suite {suite['id']} expected_exit_code must be an integer")
        if not isinstance(suite["retarget_engine_if_needed"], bool):
            raise GateError(f"suite {suite['id']} retarget_engine_if_needed must be boolean")
        result_protocol = suite.get("result_protocol", "legacy")
        if result_protocol not in SUPPORTED_RESULT_PROTOCOLS:
            raise GateError(f"suite {suite['id']} has unknown result_protocol: {result_protocol!r}")
        suite["result_protocol"] = result_protocol
        if not isinstance(suite["expected_counts"], dict) or not suite["expected_counts"]:
            raise GateError(f"suite {suite['id']} expected_counts must be a non-empty object")
        for metric, value in suite["expected_counts"].items():
            validate_count(metric, value)
        verdict = suite["required_verdict"]
        if verdict is not None:
            if (not isinstance(verdict, dict) or set(verdict) != {"label", "value"}
                    or any(not isinstance(verdict[k], str) or not verdict[k] for k in verdict)):
                raise GateError(f"suite {suite['id']} required_verdict is invalid")
        normalized_suites.append(suite)

    globals_ = manifest["global_requirements"]
    if not isinstance(globals_, dict):
        raise GateError("global_requirements must be an object")
    if globals_.get("suite_count") != len(normalized_suites):
        raise GateError("global suite_count does not match suites array length")
    aggregate = globals_.get("historical_baseline_aggregate")
    if not isinstance(aggregate, dict) or not isinstance(aggregate.get("suite_ids"), list):
        raise GateError("historical_baseline_aggregate is invalid")
    if not set(aggregate["suite_ids"]).issubset(seen):
        raise GateError("historical_baseline_aggregate references unknown suite IDs")
    validate_count("historical_baseline_aggregate", {
        "passed": aggregate.get("passed"), "total": aggregate.get("total"), "failed": aggregate.get("failed")
    })
    manifest = dict(manifest)
    manifest["engine"] = engine_rel
    manifest["suites"] = normalized_suites
    return manifest, engine_path


def engine_prefix(engine_path: Path) -> str:
    text = engine_path.read_text(encoding="utf-8")
    marker = "\nresults=[]"
    if marker not in text:
        raise GateError("current engine definition/self-test boundary not found")
    return text.split(marker, 1)[0]


def run_python_child(script_path: Path) -> subprocess.CompletedProcess[str]:
    """Run every suite process with bytecode creation disabled explicitly."""
    child_environment = os.environ.copy()
    child_environment["PYTHONDONTWRITEBYTECODE"] = "1"
    existing_pythonpath = child_environment.get("PYTHONPATH")
    child_environment["PYTHONPATH"] = str(ROOT) + (
        os.pathsep + existing_pythonpath if existing_pythonpath else ""
    )
    return subprocess.run(
        [sys.executable, "-B", str(script_path)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        env=child_environment,
    )


def temporary_run(text: str, suite_path: Path) -> subprocess.CompletedProcess[str]:
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False, encoding="utf-8", newline="\n",
            dir=suite_path.parent
        ) as stream:
            stream.write(text)
            temporary = Path(stream.name)
        return run_python_child(temporary)
    finally:
        if temporary is not None:
            try:
                temporary.unlink()
            except OSError:
                pass


def retarget_prefix_text(suite_path: Path, current_prefix: str) -> str:
    text = suite_path.read_text(encoding="utf-8")
    match = re.search(r"(?m)^ns\s*=\s*\{\}\s*;\s*exec\(PREFIX,\s*ns\)", text)
    if not match:
        raise GateError(f"legacy PREFIX execution boundary not found in {suite_path.name}")
    return "PREFIX=" + repr(current_prefix) + "\n" + text[match.start():]


def retarget_filename_text(suite_path: Path, engine_name: str, optional: bool) -> str | None:
    text = suite_path.read_text(encoding="utf-8")
    names = sorted(set(re.findall(r"claim_lifecycle_v0_1_4_[A-Za-z0-9_]+\.py", text)))
    if not names:
        if optional:
            return None
        raise GateError(f"embedded engine filename not found in {suite_path.name}")
    for old in names:
        text = text.replace(old, engine_name)
    return text


def retarget_derived_source_text(suite_path: Path, source_artifact: Path, engine_name: str) -> str:
    text = suite_path.read_text(encoding="utf-8")
    retargeted_source = retarget_filename_text(source_artifact, engine_name, optional=False)
    pattern = r'(?m)^(source\s*=\s*[A-Za-z_]\w*\.read_text\(encoding=["\']utf-8["\']\))$'
    matches = list(re.finditer(pattern, text))
    if len(matches) != 1:
        raise GateError(
            f"derived-source execution boundary count {len(matches)} != 1 in {suite_path.name}"
        )
    return text[:matches[0].start()] + "source = " + repr(retargeted_source) + text[matches[0].end():]


def execute_suite(suite: dict[str, Any], engine_path: Path, current_prefix: str) -> subprocess.CompletedProcess[str]:
    _, suite_path = safe_relative_path(suite["path"], f"suite {suite['id']}.path")
    mode = suite["execution_mode"]
    if mode == "direct":
        return run_python_child(suite_path)
    if mode == "in_memory_engine_prefix_retarget":
        return temporary_run(retarget_prefix_text(suite_path, current_prefix), suite_path)
    if mode == "in_memory_engine_filename_retarget_derived_source":
        _, source_artifact = safe_relative_path(
            suite["source_artifact"], f"suite {suite['id']}.source_artifact"
        )
        return temporary_run(
            retarget_derived_source_text(suite_path, source_artifact, engine_path.name), suite_path
        )
    optional = mode == "in_memory_engine_filename_retarget_or_direct"
    text = retarget_filename_text(suite_path, engine_path.name, optional)
    if text is None:
        return run_python_child(suite_path)
    return temporary_run(text, suite_path)


def structured_result(stdout: str) -> dict[str, Any] | None:
    """Legacy-compatible optional marker reader; first marker wins."""
    for line in stdout.splitlines():
        if line.startswith(STRUCTURED_RESULT_MARKER):
            payload = line[len(STRUCTURED_RESULT_MARKER):].strip()
            try:
                value = json.loads(payload)
            except json.JSONDecodeError as exc:
                raise GateError(f"invalid structured suite result JSON: {exc}") from exc
            if not isinstance(value, dict):
                raise GateError("structured suite result must be a JSON object")
            return value
    return None


def structured_v1_result(suite: dict[str, Any], stdout: str, manifest_engine: str) -> tuple[dict[str, Any] | None, list[dict[str, Any]], list[str]]:
    """Fail-closed protocol-v1 extraction and gate-context validation."""
    checks = []
    failures = []
    marker_lines = [line for line in stdout.splitlines() if line.startswith(STRUCTURED_RESULT_MARKER)]
    marker_ok = len(marker_lines) == 1
    checks.append({"name": "marker_count", "expected": 1, "actual": len(marker_lines),
                   "status": "PASS" if marker_ok else "FAIL"})
    if not marker_ok:
        failures.append(f"structured_v1 marker count {len(marker_lines)} != 1")
        return None, checks, failures

    raw_payload = marker_lines[0][len(STRUCTURED_RESULT_MARKER):]
    if not raw_payload.startswith("{"):
        checks.append({"name": "structured_json", "expected": "JSON object immediately after marker",
                       "actual": raw_payload[:20], "status": "FAIL"})
        failures.append("structured_v1 payload does not begin immediately after the marker")
        return None, checks, failures
    payload = raw_payload
    try:
        result = json.loads(payload)
    except json.JSONDecodeError as exc:
        checks.append({"name": "structured_json", "expected": "valid JSON object",
                       "actual": f"invalid JSON: {exc}", "status": "FAIL"})
        failures.append(f"structured_v1 payload is invalid JSON: {exc}")
        return None, checks, failures
    object_ok = isinstance(result, dict)
    checks.append({"name": "structured_json", "expected": "JSON object",
                   "actual": type(result).__name__, "status": "PASS" if object_ok else "FAIL"})
    if not object_ok:
        failures.append("structured_v1 payload is not a JSON object")
        return None, checks, failures

    try:
        validate_result(result)
        schema_ok = True
        schema_actual = result.get("schema_version")
    except ResultValidationError as exc:
        schema_ok = False
        schema_actual = result.get("schema_version")
        failures.append(f"structured_v1 schema violation: {exc}")
    checks.append({"name": "schema_version", "expected": 1, "actual": schema_actual,
                   "status": "PASS" if schema_ok and schema_actual == 1 else "FAIL"})

    suite_id_ok = isinstance(result.get("suite_id"), str) and result.get("suite_id") == suite["id"]
    checks.append({"name": "suite_id", "expected": suite["id"], "actual": result.get("suite_id"),
                   "status": "PASS" if suite_id_ok else "FAIL"})
    if not suite_id_ok:
        failures.append(f"structured suite_id {result.get('suite_id')!r} != manifest id {suite['id']!r}")

    engine_ok = isinstance(result.get("engine"), str) and result.get("engine") == manifest_engine
    checks.append({"name": "engine", "expected": manifest_engine, "actual": result.get("engine"),
                   "status": "PASS" if engine_ok else "FAIL"})
    if not engine_ok:
        failures.append(f"structured engine {result.get('engine')!r} != manifest engine {manifest_engine!r}")

    status_ok = result.get("status") == "PASS"
    checks.append({"name": "structured_status", "expected": "PASS", "actual": result.get("status"),
                   "status": "PASS" if status_ok else "FAIL"})
    if not status_ok:
        failures.append(f"structured status is {result.get('status')!r}, not PASS")

    consistency_failures = classification_consistency_failures(result)
    checks.append({"name": "classifications_consistency", "expected": "consistent",
                   "actual": consistency_failures or "consistent",
                   "status": "PASS" if not consistency_failures else "FAIL"})
    failures.extend(consistency_failures)
    return result, checks, failures


def classification_consistency_failures(result: dict[str, Any]) -> list[str]:
    counts = result.get("counts")
    classifications = result.get("classifications")
    if not isinstance(counts, dict) or not isinstance(classifications, dict):
        return ["structured classifications/counts are unavailable for consistency validation"]
    comparisons = {
        "core_pass": ("core", "passed"),
        "core_fail": ("core", "failed"),
        "expected_rejection": ("expected_rejection", "passed"),
        "contract_robustness_observation": ("contract_robustness_observation", None),
        "invalid_unreachable_setup": ("invalid_unreachable_setup", None),
        "invalid_unjustified_metamorphic_relation": ("invalid_unjustified_metamorphic_relation", None),
    }
    failures = []
    for classification, (metric, member) in comparisons.items():
        if classification not in classifications or metric not in counts:
            continue
        metric_value = counts[metric]
        expected = metric_value.get(member) if member and isinstance(metric_value, dict) else metric_value
        actual = classifications[classification]
        if actual != expected:
            failures.append(
                f"classification/count mismatch: {classification}={actual!r}, counts.{metric}"
                f"{'.' + member if member else ''}={expected!r}"
            )
    return failures


def legacy_triplet(metric: str, stdout: str) -> dict[str, int] | None:
    patterns = {
        "total": [
            r"TOTAL:\s*(\d+)\s*/\s*(\d+)\s+PASS(?:,\s*(\d+)\s+FAIL)?",
            r"(?m)^.*dedicated regression:\s*(\d+)\s*/\s*(\d+)\s+PASS(?:,\s*(\d+)\s+FAIL)?$",
            r"Ran\s+(\d+)\s+tests?\b",
        ],
        "core": [
            r"CORE TOTAL:\s*(\d+)\s*/\s*(\d+)\s+PASS,\s*(\d+)\s+FAIL",
            r"CORE PASS \(blocked/safe\):\s*(\d+)\s*/\s*(\d+)",
        ],
        "expected_behavior": [r"EXPECTED TOTAL:\s*(\d+)\s*/\s*(\d+)\s+PASS(?:,\s*(\d+)\s+FAIL)?"],
        "expected_rejection": [r"EXPECTED REJECTION:\s*(\d+)\s*/\s*(\d+)"],
    }
    for index, pattern in enumerate(patterns.get(metric, [])):
        match = re.search(pattern, stdout)
        if not match:
            continue
        if metric == "total" and index == 2:
            passed = total = int(match.group(1))
        else:
            passed, total = int(match.group(1)), int(match.group(2))
        if metric == "core" and index == 1:
            failed_match = re.search(r"CORE FAIL \(reachable bypass\):\s*(\d+)\s*/\s*(\d+)", stdout)
            if not failed_match or int(failed_match.group(2)) != total:
                return None
            failed = int(failed_match.group(1))
        elif match.lastindex and match.lastindex >= 3 and match.group(3) is not None:
            failed = int(match.group(3))
        else:
            failed = total - passed
        return {"passed": passed, "total": total, "failed": failed}
    return None


def parse_metric(metric: str, stdout: str, structured: dict[str, Any] | None,
                 allow_legacy: bool = True) -> Any:
    if structured is not None:
        counts = structured.get("counts")
        if isinstance(counts, dict) and metric in counts:
            return counts[metric]
    if not allow_legacy:
        return None
    triplet = legacy_triplet(metric, stdout)
    if triplet is not None:
        return triplet
    label = LEGACY_SCALAR_LABELS.get(metric)
    if label:
        match = re.search(re.escape(label) + r":\s*(\d+)", stdout)
        return int(match.group(1)) if match else None
    return None


def check_suite(suite: dict[str, Any], process: subprocess.CompletedProcess[str],
                manifest_engine: str) -> dict[str, Any]:
    checks = []
    failures = []
    exit_ok = process.returncode == suite["expected_exit_code"]
    checks.append({"name": "exit_code", "expected": suite["expected_exit_code"],
                   "actual": process.returncode, "status": "PASS" if exit_ok else "FAIL"})
    if not exit_ok:
        failures.append(f"exit code {process.returncode} != expected {suite['expected_exit_code']}")

    protocol = suite["result_protocol"]
    if protocol == "structured_v1":
        structured, structured_checks, structured_failures = structured_v1_result(
            suite, process.stdout, manifest_engine
        )
        checks.extend(structured_checks)
        failures.extend(structured_failures)
    else:
        try:
            structured = structured_result(process.stdout)
        except GateError as exc:
            structured = None
            failures.append(str(exc))
    for metric, expected in suite["expected_counts"].items():
        legacy_output = process.stdout + "\n" + process.stderr
        actual = parse_metric(metric, legacy_output, structured, allow_legacy=protocol == "legacy")
        ok = actual == expected
        checks.append({"name": f"count:{metric}", "expected": expected, "actual": actual,
                       "status": "PASS" if ok else "FAIL"})
        if not ok:
            failures.append(f"count {metric} actual={actual!r} expected={expected!r}")

    verdict = suite["required_verdict"]
    if verdict is not None:
        structured_verdict = structured.get("verdict") if structured else None
        if structured_verdict is not None:
            actual_verdict = structured_verdict
            ok = actual_verdict == verdict
        elif protocol == "structured_v1":
            actual_verdict = None
            ok = False
        else:
            pattern = re.escape(verdict["label"]) + r":\s*" + re.escape(verdict["value"])
            ok = re.search(pattern, process.stdout) is not None
            actual_verdict = verdict if ok else None
        checks.append({"name": "required_verdict", "expected": verdict, "actual": actual_verdict,
                       "status": "PASS" if ok else "FAIL"})
        if not ok:
            failures.append("required verdict was not verified")

    return {
        "id": suite["id"],
        "path": suite["path"],
        "execution_mode": suite["execution_mode"],
        "status": "PASS" if not failures else "FAIL",
        "exit_code": process.returncode,
        "expected_exit_code": suite["expected_exit_code"],
        "checks": checks,
        "failure_reasons": failures,
        "stdout": process.stdout,
        "stderr": process.stderr,
    }


def actual_metric(result: dict[str, Any], metric: str) -> Any:
    for check in result["checks"]:
        if check["name"] == f"count:{metric}":
            return check["actual"]
    return None


def evaluate_globals(manifest: dict[str, Any], results: list[dict[str, Any]]) -> dict[str, Any]:
    expected = manifest["global_requirements"]
    checks = []
    by_id = {item["id"]: item for item in results}
    all_pass = len(results) == len(manifest["suites"]) and all(item["status"] == "PASS" for item in results)
    checks.append({"name": "all_suites_required", "expected": bool(expected.get("all_suites_required")),
                   "actual": all_pass, "status": "PASS" if expected.get("all_suites_required") is True and all_pass else "FAIL"})
    count_ok = len(results) == expected.get("suite_count")
    checks.append({"name": "suite_count", "expected": expected.get("suite_count"), "actual": len(results),
                   "status": "PASS" if count_ok else "FAIL"})
    fail_closed_ok = expected.get("fail_closed_on_missing_or_unparseable_result") is True
    checks.append({"name": "fail_closed_on_missing_or_unparseable_result", "expected": True,
                   "actual": fail_closed_ok, "status": "PASS" if fail_closed_ok else "FAIL"})

    aggregate = expected["historical_baseline_aggregate"]
    actual = {"passed": 0, "total": 0, "failed": 0}
    aggregate_ok = True
    for suite_id in aggregate["suite_ids"]:
        metric = actual_metric(by_id.get(suite_id, {}), "total") if suite_id in by_id else None
        if not isinstance(metric, dict):
            aggregate_ok = False
            continue
        for key in actual:
            actual[key] += metric[key]
    required_aggregate = {key: aggregate[key] for key in actual}
    aggregate_ok = aggregate_ok and actual == required_aggregate
    checks.append({"name": "historical_baseline_aggregate", "expected": required_aggregate,
                   "actual": actual, "status": "PASS" if aggregate_ok else "FAIL"})

    configured_final = expected.get("final_gate")
    final_shape_ok = configured_final == {
        "pass": True, "checkpoint_remains_green": True, "engine_patch_required": False
    }
    checks.append({"name": "final_gate_requirement", "expected": configured_final,
                   "actual": {"pass": all_pass and aggregate_ok,
                              "checkpoint_remains_green": all_pass and aggregate_ok,
                              "engine_patch_required": False if all_pass and aggregate_ok else None},
                   "status": "PASS" if final_shape_ok and all_pass and aggregate_ok else "FAIL"})
    return {"status": "PASS" if all(c["status"] == "PASS" for c in checks) else "FAIL", "checks": checks}


def serializable_suite(result: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in result.items() if key not in {"stdout", "stderr", "execution_mode"}}


def write_outputs(gate: dict[str, Any], full_results: list[dict[str, Any]], fatal: str | None = None) -> None:
    lines = ["=" * 104, "MANIFEST-DRIVEN UNIVERSAL REGRESSION GATE", "=" * 104]
    if fatal:
        lines.extend(["MANIFEST VALIDATION: FAIL", fatal])
    for result in full_results:
        lines.extend([
            f"SUITE ID: {result['id']}",
            f"SUITE PATH: {result['path']}",
            f"EXECUTION MODE: {result['execution_mode']}",
            f"EXIT CODE: {result['exit_code']}",
            "CAPTURED STDOUT:", result["stdout"],
            "CAPTURED STDERR:", result["stderr"],
            "PARSED CHECKS:", json.dumps(result["checks"], indent=2, ensure_ascii=False),
            f"SUITE RESULT: {result['status']}",
            "FAILURE REASONS: " + json.dumps(result["failure_reasons"], ensure_ascii=False),
            "-" * 104,
        ])
    lines.extend(["GLOBAL REQUIREMENTS:", json.dumps(gate["global_requirements"], indent=2, ensure_ascii=False),
                  f"FINAL STATUS: {gate['status']}", "=" * 104])
    RAW_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    RESULT_PATH.write_text(json.dumps(gate, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def run_gate() -> int:
    started = utc_now()
    full_results = []
    fatal = None
    try:
        manifest, engine_path = validate_manifest(load_manifest())
        current_prefix = engine_prefix(engine_path)
        for suite in manifest["suites"]:
            try:
                process = execute_suite(suite, engine_path, current_prefix)
                result = check_suite(suite, process, manifest["engine"])
            except Exception as exc:
                result = {
                    "id": suite["id"], "path": suite["path"],
                    "execution_mode": suite["execution_mode"], "status": "FAIL",
                    "exit_code": None, "expected_exit_code": suite["expected_exit_code"],
                    "checks": [], "failure_reasons": [f"safe execution failed: {type(exc).__name__}: {exc}"],
                    "stdout": "", "stderr": "",
                }
            full_results.append(result)
        global_result = evaluate_globals(manifest, full_results)
        status = "PASS" if all(r["status"] == "PASS" for r in full_results) and global_result["status"] == "PASS" else "FAIL"
        checkpoint, engine = manifest["checkpoint"], manifest["engine"]
        manifest_sha = sha256_file(MANIFEST_PATH)
    except Exception as exc:
        fatal = f"{type(exc).__name__}: {exc}"
        status, checkpoint, engine = "FAIL", None, None
        manifest_sha = sha256_file(MANIFEST_PATH) if MANIFEST_PATH.is_file() else None
        global_result = {"status": "FAIL", "checks": [{"name": "manifest_validation", "status": "FAIL", "reason": fatal}]}

    gate = {
        "schema_version": 1,
        "checkpoint": checkpoint,
        "engine": engine,
        "manifest_sha256": manifest_sha,
        "started_at": started,
        "finished_at": utc_now(),
        "status": status,
        "suite_total": len(full_results),
        "suite_pass": sum(r["status"] == "PASS" for r in full_results),
        "suite_fail": sum(r["status"] == "FAIL" for r in full_results),
        "suites": [serializable_suite(r) for r in full_results],
        "global_requirements": global_result,
    }
    write_outputs(gate, full_results, fatal)
    print("=" * 40)
    print(f"UNIVERSAL REGRESSION GATE: {status}")
    print(f"Checkpoint: {checkpoint}")
    print(f"Suites: {gate['suite_pass']}/{gate['suite_total']} PASS")
    print("Engine patch required: NO" if status == "PASS" else "Review required")
    print("=" * 40)
    return 0 if status == "PASS" else 1


def main(argv: list[str]) -> int:
    if len(argv) == 2 and argv[1] == "--validate-manifest":
        manifest, _ = validate_manifest(load_manifest())
        print(f"MANIFEST VALID: {len(manifest['suites'])} suites, checkpoint {manifest['checkpoint']}")
        return 0
    if len(argv) != 1:
        print("Usage: python run_gate.py [--validate-manifest]", file=sys.stderr)
        return 2
    return run_gate()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
