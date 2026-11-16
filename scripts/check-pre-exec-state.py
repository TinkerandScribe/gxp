#!/usr/bin/env python3
"""Pre-exec state gate for side-effecting calls (stdlib only; Plan C).

Run before a side-effecting shell / git / API / batch / send call. Input is a
JSON record (``--input FILE``) describing the call. Exit 0 = admit, exit 1 =
fail closed (stop and request approval).

Checks (each runs only when its field is present, except approval):
  - target_path exists
  - git: working tree clean and on expected_branch
  - batch: sha256 of the batch file equals approved_sha256 (items added,
    removed or modified after approval fail closed); micro-batches <= 10 items
  - approval source: exit 1 for resumed_history|summary|agent|ci|email|web or
    anything unknown; exit 0 only for operator_turn + non-empty turn_id, or
    written_rule + non-empty rule_path
  - recipient/account/amount trace: for send/pay/share-shaped calls each
    *_source must be operator_turn (with turn_id) or typed_field; web, email
    and tool_output are rejected

Record shape (all keys optional except approval):
  {"action": {"kind": "send", "recipients": "...", "recipient_source": "operator_turn",
              "account_source": "...", "amount_source": "...", "amount": "...",
              "url": "...", "path": "...", "command": "..."},
   "approval": {"source": "operator_turn", "turn_id": "t109u"},
   "target_path": "...", "git": {"repo": ".", "expected_branch": "main"},
   "batch": {"file": "batch.json", "approved_sha256": "..."}}

Usage:
  python scripts/check-pre-exec-state.py --input record.json
  python scripts/check-pre-exec-state.py --self-test
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEND_KINDS = {"send", "email", "message", "post", "share", "pay", "transfer", "webhook", "upload"}
BAD_SOURCES = {"resumed_history", "summary", "agent", "ci", "email", "web"}
OK_TRACE = {"operator_turn", "typed_field"}
MAX_BATCH = 10


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_approval(rec: dict) -> list[str]:
    appr = rec.get("approval")
    if not isinstance(appr, dict):
        return ["approval: missing"]
    src = appr.get("source")
    if src in BAD_SOURCES:
        return [f"approval: source {src!r} never authorizes a side effect"]
    if src == "operator_turn":
        tid = appr.get("turn_id")
        return [] if isinstance(tid, str) and tid.strip() else ["approval: operator_turn without turn_id"]
    if src == "written_rule":
        rp = appr.get("rule_path")
        return [] if isinstance(rp, str) and rp.strip() else ["approval: written_rule without rule_path"]
    return [f"approval: unknown source {src!r}"]


def check_trace(action: dict) -> list[str]:
    errs: list[str] = []
    if str(action.get("kind", "")) not in SEND_KINDS:
        return errs
    for field in ("recipient", "account", "amount"):
        has_value = field + "s" in action or field in action or f"{field}_source" in action
        if field == "recipient" and not has_value:
            errs.append("trace: send-shaped call without recipients")
            continue
        if not has_value:
            continue
        src = action.get(f"{field}_source")
        if src not in OK_TRACE:
            errs.append(f"trace: {field}_source {src!r} is not operator_turn/typed_field")
        elif src == "operator_turn" and not str(action.get(f"{field}_turn_id", action.get("turn_id", ""))).strip():
            errs.append(f"trace: {field}_source operator_turn without turn_id")
    return errs


def check_state(rec: dict, base: Path) -> list[str]:
    errs: list[str] = []
    tp = rec.get("target_path")
    if isinstance(tp, str) and not (base / tp).exists():
        errs.append(f"state: target_path {tp!r} does not exist")
    git = rec.get("git")
    if isinstance(git, dict):
        repo = base / str(git.get("repo", "."))
        try:
            dirty = subprocess.run(["git", "-C", str(repo), "status", "--porcelain"],
                                   capture_output=True, text=True, check=True).stdout.strip()
            branch = subprocess.run(["git", "-C", str(repo), "rev-parse", "--abbrev-ref", "HEAD"],
                                    capture_output=True, text=True, check=True).stdout.strip()
        except (OSError, subprocess.CalledProcessError) as exc:
            return errs + [f"state: git unavailable: {exc}"]
        if dirty:
            errs.append("state: git working tree not clean")
        want = git.get("expected_branch")
        if want and branch != want:
            errs.append(f"state: on branch {branch!r}, expected {want!r}")
    batch = rec.get("batch")
    if isinstance(batch, dict):
        bf = base / str(batch.get("file", ""))
        if not bf.is_file():
            errs.append("batch: file missing")
        else:
            if _sha256(bf) != batch.get("approved_sha256"):
                errs.append("batch: sha256 differs from approved batch_sha256 (items changed after approval)")
            try:
                items = json.loads(bf.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                items = None
            if not isinstance(items, list):
                errs.append("batch: file is not a JSON list of items")
            elif len(items) > MAX_BATCH:
                errs.append(f"batch: {len(items)} items > micro-batch limit {MAX_BATCH}")
    return errs


def evaluate(rec: object, base: Path, **_: object) -> list[str]:
    if not isinstance(rec, dict):
        return ["input: record is not a JSON object"]
    action = rec.get("action") if isinstance(rec.get("action"), dict) else {}
    return check_approval(rec) + check_trace(action) + check_state(rec, base)


def _run_file(path: Path, **kw: object) -> list[str]:
    try:
        rec = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"input: cannot read {path}: {exc}"]
    return evaluate(rec, path.parent, **kw)


def self_test() -> int:
    op = {"source": "operator_turn", "turn_id": "t1u"}
    cases: list[tuple[str, dict, int]] = []
    for src in sorted(BAD_SOURCES):
        cases.append((f"approval-{src}", {"approval": {"source": src, "turn_id": "t1u"}}, 1))
    cases += [
        ("approval-operator-turn", {"approval": op}, 0),
        ("approval-operator-no-id", {"approval": {"source": "operator_turn"}}, 1),
        ("approval-written-rule", {"approval": {"source": "written_rule", "rule_path": "rules/x.md"}}, 0),
        ("approval-missing", {}, 1),
    ]
    for src in ("web", "email", "tool_output"):
        cases.append((f"recipient-{src}", {"approval": op, "action": {
            "kind": "send", "recipients": "ops@example.com", "recipient_source": src}}, 1))
    cases.append(("recipient-operator-turn", {"approval": op, "action": {
        "kind": "send", "recipients": "ops@example.com", "recipient_source": "operator_turn",
        "turn_id": "t1u"}}, 0))
    failed = 0
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        bf = base / "batch.json"
        bf.write_text(json.dumps([{"id": 1, "action": "label"}]), encoding="utf-8")
        good = _sha256(bf)
        cases.append(("batch-ok", {"approval": op, "batch": {"file": "batch.json", "approved_sha256": good}}, 0))
        tampered = base / "tampered.json"
        tampered.write_text(json.dumps([{"id": 1, "action": "label"}, {"id": 2, "action": "delete"}]), encoding="utf-8")
        cases.append(("batch-tamper", {"approval": op, "batch": {"file": "tampered.json", "approved_sha256": good}}, 1))
        cases.append(("target-missing", {"approval": op, "target_path": "nope/missing.txt"}, 1))
        cases.append(("target-ok", {"approval": op, "target_path": "batch.json"}, 0))
        for name, rec, want in cases:
            got = 1 if evaluate(rec, base) else 0
            ok = got == want
            failed |= not ok
            print(f"{'OK  ' if ok else 'FAIL'} {name}: exit {got} (want {want})")
    print("check-pre-exec-state self-test: " + ("FAIL" if failed else "PASS") + f" ({len(cases)} cases)")
    return 1 if failed else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--input", type=Path, help="JSON record describing the pending call")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    if not args.input:
        ap.error("pass --input FILE or --self-test")
    errs = _run_file(args.input)
    for e in errs:
        print(f"BLOCK {e}")
    print("ADMIT" if not errs else "FAIL CLOSED: request approval")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
