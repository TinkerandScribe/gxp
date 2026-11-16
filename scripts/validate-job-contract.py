#!/usr/bin/env python3
"""Validate a cross-bot job contract.

Schema: core/templates/job-contract.schema.json (a JSON Schema subset enforced
here with the stdlib — no jsonschema package).

After schema conformance, the semantic checks are:

- task graph (depends_on) is acyclic and every dependency names a task
- each criterion has exactly one owning work task
- each criterion owner_bot is exactly one bot id
- decision COMMIT is legal only when clock is τ4
- HOLD and REFUSE are legal on τ1, τ2, and τ4; otherwise decision is none
- a criterion with sealed_by set is not pending, and sealed_by names a gate
  task whose covers_isc includes that criterion
- ESCALATE (legal on τ1/τ2/τ4) needs escalation_packet with non-empty
  blocker_evidence, progress_summary and verification_status
- a passed criterion needs non-empty verify_cmds and evidence_refs with at
  least one kind "raw" ref; summary-only evidence is rejected
  (summary_only_evidence; arXiv:2611.18471)
- every residual_failing_tests entry appears in verify_cmds
- a task may not widen the allowed_paths / allowed_tools of a task it
  depends_on (subagent_scope_widening)

Task type names follow TaskType in Intelligent-Internet/zenith
zenith_harness/models.py (Apache-2.0). This script does not vendor that
project. The single work owner is the contract form of "one owning node":
validate and gate may list the same criterion in covers_isc and are not a
second work owner.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCHEMA = ROOT / "core" / "templates" / "job-contract.schema.json"

BOT_ID = re.compile(r"^[A-Za-z][A-Za-z0-9_-]*$")
TAU4 = "\u03c44"

ANNOTATIONS = {
    "$schema",
    "$id",
    "title",
    "description",
    "$comment",
    "examples",
    "default",
}
IMPLEMENTED = ANNOTATIONS | {
    "type",
    "enum",
    "const",
    "required",
    "properties",
    "additionalProperties",
    "items",
    "minLength",
    "maxLength",
    "minimum",
    "maximum",
    "minItems",
    "maxItems",
    "pattern",
    "anyOf",
}


def _is_type(instance: object, name: str) -> bool:
    if name == "null":
        return instance is None
    if name == "string":
        return isinstance(instance, str)
    if name == "integer":
        return isinstance(instance, int) and not isinstance(instance, bool)
    if name == "number":
        return isinstance(instance, (int, float)) and not isinstance(instance, bool)
    if name == "boolean":
        return isinstance(instance, bool)
    if name == "array":
        return isinstance(instance, list)
    if name == "object":
        return isinstance(instance, dict)
    return False


def _type_ok(instance: object, expected: object) -> bool:
    names = expected if isinstance(expected, list) else [expected]
    return any(isinstance(n, str) and _is_type(instance, n) for n in names)


def schema_errors(schema: object, instance: object, path: str = "$") -> list[str]:
    """Return schema error messages. Empty means the instance conforms."""
    if not isinstance(schema, dict):
        return [f"{path}: schema is not an object"]
    unknown = set(schema) - IMPLEMENTED
    if unknown:
        return [f"{path}: unsupported schema keywords {sorted(unknown)}"]

    if "anyOf" in schema:
        branches = schema["anyOf"]
        if not isinstance(branches, list) or not branches:
            return [f"{path}: anyOf must be a non-empty array"]
        if any(not schema_errors(branch, instance, path) for branch in branches):
            return []
        return [f"{path}: does not match anyOf"]

    errors: list[str] = []
    if "const" in schema and instance != schema["const"]:
        errors.append(f"{path}: expected const {schema['const']!r}")
    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{path}: {instance!r} not in {schema['enum']!r}")
    if "type" in schema and not _type_ok(instance, schema["type"]):
        errors.append(f"{path}: expected type {schema['type']!r}")
        return errors

    if isinstance(instance, str):
        if "minLength" in schema and len(instance) < schema["minLength"]:
            errors.append(f"{path}: shorter than minLength {schema['minLength']}")
        if "maxLength" in schema and len(instance) > schema["maxLength"]:
            errors.append(f"{path}: longer than maxLength {schema['maxLength']}")
        if "pattern" in schema and re.fullmatch(schema["pattern"], instance) is None:
            errors.append(f"{path}: does not match pattern {schema['pattern']}")

    if isinstance(instance, (int, float)) and not isinstance(instance, bool):
        if "minimum" in schema and instance < schema["minimum"]:
            errors.append(f"{path}: below minimum {schema['minimum']}")
        if "maximum" in schema and instance > schema["maximum"]:
            errors.append(f"{path}: above maximum {schema['maximum']}")

    if isinstance(instance, list):
        if "minItems" in schema and len(instance) < schema["minItems"]:
            errors.append(f"{path}: fewer than minItems {schema['minItems']}")
        if "maxItems" in schema and len(instance) > schema["maxItems"]:
            errors.append(f"{path}: more than maxItems {schema['maxItems']}")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for i, item in enumerate(instance):
                errors.extend(schema_errors(item_schema, item, f"{path}[{i}]"))

    if isinstance(instance, dict):
        required = schema.get("required", [])
        if isinstance(required, list):
            for key in required:
                if key not in instance:
                    errors.append(f"{path}: missing required {key!r}")
        properties = schema.get("properties", {})
        if not isinstance(properties, dict):
            properties = {}
        additional = schema.get("additionalProperties", True)
        for key, value in instance.items():
            if key in properties:
                errors.extend(schema_errors(properties[key], value, f"{path}.{key}"))
            elif additional is False:
                errors.append(f"{path}: unexpected property {key!r}")
            elif isinstance(additional, dict):
                errors.extend(schema_errors(additional, value, f"{path}.{key}"))
    return errors


def _cycle(tasks: list[dict]) -> list[str] | None:
    graph = {t["id"]: list(t["depends_on"]) for t in tasks}
    color = {i: 0 for i in graph}
    stack: list[str] = []

    def dfs(node: str) -> list[str] | None:
        color[node] = 1
        stack.append(node)
        for dep in graph[node]:
            if dep not in graph:
                continue
            if color[dep] == 1:
                start = stack.index(dep)
                return stack[start:] + [dep]
            if color[dep] == 0:
                found = dfs(dep)
                if found:
                    return found
        stack.pop()
        color[node] = 2
        return None

    for node in graph:
        if color[node] == 0:
            found = dfs(node)
            if found:
                return found
    return None


def semantic_errors(doc: object) -> list[tuple[str, str]]:
    if not isinstance(doc, dict):
        return [("schema", "document is not an object")]
    errors: list[tuple[str, str]] = []
    isc = doc.get("isc")
    tasks = doc.get("tasks")
    if not isinstance(isc, list) or not isinstance(tasks, list):
        return [("schema", "isc and tasks must be arrays")]

    isc_ids: list[str] = []
    for item in isc:
        if isinstance(item, dict) and isinstance(item.get("id"), str):
            isc_ids.append(item["id"])
    if len(isc_ids) != len(set(isc_ids)):
        errors.append(("duplicate_id", "duplicate criterion id"))
    task_ids: list[str] = []
    for task in tasks:
        if isinstance(task, dict) and isinstance(task.get("id"), str):
            task_ids.append(task["id"])
    if len(task_ids) != len(set(task_ids)):
        errors.append(("duplicate_id", "duplicate task id"))

    by_id = {
        t["id"]: t
        for t in tasks
        if isinstance(t, dict) and isinstance(t.get("id"), str)
    }
    known_isc = set(isc_ids)

    for task in tasks:
        if not isinstance(task, dict):
            continue
        tid = task.get("id")
        deps = task.get("depends_on")
        covers = task.get("covers_isc")
        if not isinstance(deps, list) or not isinstance(covers, list):
            continue
        for dep in deps:
            if dep not in by_id:
                errors.append(("dangling_dep", f"task {tid} depends_on unknown {dep}"))
        for cid in covers:
            if cid not in known_isc:
                errors.append(("covers_ref", f"task {tid} covers unknown criterion {cid}"))

    cycle = _cycle([t for t in tasks if isinstance(t, dict) and isinstance(t.get("id"), str)])
    if cycle:
        errors.append(("cycle", "task graph cycle: " + " -> ".join(cycle)))

    owners: dict[str, list[str]] = {cid: [] for cid in isc_ids}
    for task in tasks:
        if not isinstance(task, dict) or task.get("type") != "work":
            continue
        tid = task.get("id")
        covers = task.get("covers_isc")
        if not isinstance(tid, str) or not isinstance(covers, list):
            continue
        for cid in covers:
            if cid in owners and isinstance(cid, str):
                owners[cid].append(tid)
    for cid, work_ids in owners.items():
        if len(work_ids) != 1:
            errors.append(
                (
                    "isc_work_owner",
                    f"criterion {cid} has {len(work_ids)} work owners ({work_ids}); expected 1",
                )
            )

    job_owner = doc.get("owner_bot")
    if not isinstance(job_owner, str) or BOT_ID.fullmatch(job_owner) is None:
        errors.append(("owner_bot", "job owner_bot must be exactly one bot id"))
    for item in isc:
        if not isinstance(item, dict):
            continue
        owner = item.get("owner_bot")
        cid = item.get("id")
        if not isinstance(owner, str) or BOT_ID.fullmatch(owner) is None:
            errors.append(
                (
                    "isc_owner_bot",
                    f"criterion {cid} owner_bot must be exactly one bot id",
                )
            )
        sealed = item.get("sealed_by")
        status = item.get("status")
        if sealed is None:
            continue
        if status == "pending":
            errors.append(
                (
                    "sealed_pending",
                    f"criterion {cid} is sealed by {sealed} but status is pending",
                )
            )
        gate = by_id.get(sealed) if isinstance(sealed, str) else None
        covers = gate.get("covers_isc") if isinstance(gate, dict) else None
        if (
            not isinstance(gate, dict)
            or gate.get("type") != "gate"
            or not isinstance(covers, list)
            or cid not in covers
        ):
            errors.append(
                (
                    "sealed_ref",
                    f"criterion {cid} sealed_by {sealed!r} is not a gate task covering it",
                )
            )

    decision = doc.get("decision")
    clock = doc.get("clock")
    if decision == "COMMIT" and clock != TAU4:
        errors.append(
            (
                "decision_clock",
                f"decision COMMIT requires clock {TAU4} (criteria-text change); got {clock!r}",
            )
        )
    if decision == "ESCALATE":
        packet = doc.get("escalation_packet")
        if not isinstance(packet, dict) or not _escalation_complete(packet):
            errors.append(
                (
                    "escalate_packet",
                    "decision ESCALATE requires escalation_packet with non-empty "
                    "blocker_evidence, progress_summary and verification_status",
                )
            )
    errors.extend(_evidence_errors(doc, isc))
    errors.extend(_scope_errors(tasks, by_id))
    return errors


def _escalation_complete(packet: dict) -> bool:
    blockers = packet.get("blocker_evidence")
    if not isinstance(blockers, list) or not any(
        isinstance(b, str) and b.strip() for b in blockers
    ):
        return False
    for key in ("progress_summary", "verification_status"):
        val = packet.get(key)
        if not isinstance(val, str) or not val.strip():
            return False
    return True


def _ref_kind(ref: object) -> str | None:
    """raw | summary | None (malformed). Legacy bare strings count as raw."""
    if isinstance(ref, str):
        return "raw" if ref.strip() and not any(c.isspace() for c in ref) else None
    if isinstance(ref, dict) and ref.get("kind") in ("raw", "summary"):
        return ref["kind"]
    return None


def _evidence_errors(doc: dict, isc: list) -> list[tuple[str, str]]:
    """Passed criteria need verify_cmds and >=1 raw evidence ref (Plan B)."""
    errors: list[tuple[str, str]] = []
    top_cmds = doc.get("verify_cmds") if isinstance(doc.get("verify_cmds"), list) else []
    top_refs = doc.get("evidence_refs") if isinstance(doc.get("evidence_refs"), list) else []
    all_cmds: list[str] = [c for c in top_cmds if isinstance(c, str)]
    any_passed = False
    for item in isc:
        if not isinstance(item, dict):
            continue
        own_cmds = item.get("verify_cmds")
        if isinstance(own_cmds, list):
            all_cmds.extend(c for c in own_cmds if isinstance(c, str))
        if item.get("status") != "passed":
            continue
        any_passed = True
        cid = item.get("id")
        cmds = own_cmds if isinstance(own_cmds, list) else top_cmds
        refs = item.get("evidence_refs")
        refs = refs if isinstance(refs, list) else top_refs
        if not [c for c in cmds if isinstance(c, str) and c.strip()]:
            errors.append(("passed_no_verify", f"criterion {cid} is passed with empty verify_cmds"))
        if not refs:
            errors.append(("passed_no_evidence", f"criterion {cid} is passed with empty evidence_refs"))
            continue
        kinds = [_ref_kind(r) for r in refs]
        if "raw" not in kinds:
            errors.append(
                (
                    "summary_only_evidence",
                    f"criterion {cid} is passed but has no raw evidence_ref "
                    "(summary-only evidence is UNVERIFIED)",
                )
            )
    residual = doc.get("residual_failing_tests")
    if isinstance(residual, list):
        for test in residual:
            if not isinstance(test, str):
                continue
            if not any(test in cmd for cmd in all_cmds):
                errors.append(
                    (
                        "residual_uncovered",
                        f"residual_failing_tests entry {test!r} is not in any verify_cmds",
                    )
                )
        if residual and any_passed and any(
            not any(t in c for c in all_cmds) for t in residual if isinstance(t, str)
        ):
            errors.append(
                (
                    "residual_passed",
                    "a criterion is passed while a residual failing test is not covered by verify_cmds",
                )
            )
    return errors


def _scope_errors(tasks: list, by_id: dict) -> list[tuple[str, str]]:
    """A child task may not widen a parent's allowed_paths / allowed_tools."""
    errors: list[tuple[str, str]] = []
    for task in tasks:
        if not isinstance(task, dict):
            continue
        deps = task.get("depends_on") if isinstance(task.get("depends_on"), list) else []
        for dep in deps:
            parent = by_id.get(dep)
            if not isinstance(parent, dict):
                continue
            for key in ("allowed_paths", "allowed_tools"):
                p_scope = parent.get(key)
                c_scope = task.get(key)
                if not isinstance(p_scope, list) or not isinstance(c_scope, list):
                    continue
                extra = sorted(set(c_scope) - set(p_scope))
                if extra:
                    errors.append(
                        (
                            "subagent_scope_widening",
                            f"task {task.get('id')} {key} widens parent {dep}: {extra}",
                        )
                    )
    return errors


def validate_document(schema: dict, doc: object) -> list[tuple[str, str]]:
    structural = schema_errors(schema, doc)
    if structural:
        return [("schema", msg) for msg in structural]
    return semantic_errors(doc)


def _load(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def _print_errors(path: Path, errors: list[tuple[str, str]]) -> None:
    for code, msg in errors:
        print(f"ERROR {code}: {path}: {msg}", file=sys.stderr)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate cross-bot job contracts")
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    parser.add_argument(
        "--positive",
        action="append",
        default=[],
        type=Path,
        help="Contract that must validate (repeatable)",
    )
    parser.add_argument(
        "--negative",
        action="append",
        default=[],
        help="CODE=PATH; file must fail and include CODE (repeatable)",
    )
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help="Additional contracts that must validate",
    )
    args = parser.parse_args(argv)

    schema_path = args.schema
    try:
        schema = _load(schema_path)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR schema: cannot load {schema_path}: {exc}", file=sys.stderr)
        return 1
    if not isinstance(schema, dict):
        print(f"ERROR schema: {schema_path} is not an object", file=sys.stderr)
        return 1

    failed = 0
    positives = list(args.positive) + list(args.paths)
    for path in positives:
        try:
            doc = _load(path)
        except (OSError, json.JSONDecodeError) as exc:
            print(f"ERROR schema: {path}: {exc}", file=sys.stderr)
            failed = 1
            continue
        errors = validate_document(schema, doc)
        if errors:
            _print_errors(path, errors)
            failed = 1
        else:
            print(f"OK   {path}")

    for item in args.negative:
        if "=" not in item:
            print(f"ERROR usage: --negative expects CODE=PATH, got {item!r}", file=sys.stderr)
            failed = 1
            continue
        code, raw = item.split("=", 1)
        path = Path(raw)
        try:
            doc = _load(path)
        except (OSError, json.JSONDecodeError) as exc:
            print(f"ERROR schema: {path}: {exc}", file=sys.stderr)
            failed = 1
            continue
        errors = validate_document(schema, doc)
        codes = {c for c, _ in errors}
        if code in codes:
            print(f"OK   negative {code} {path}")
        else:
            got = ", ".join(sorted(codes)) if codes else "no errors"
            print(
                f"ERROR negative: {path}: expected {code}, got {got}",
                file=sys.stderr,
            )
            _print_errors(path, errors)
            failed = 1

    if not positives and not args.negative:
        parser.error("pass at least one contract or --negative CODE=PATH")
    return failed


if __name__ == "__main__":
    sys.exit(main())
