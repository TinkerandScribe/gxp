#!/usr/bin/env python3
"""Score an agent result directory on a frozen coding task.

Usage (from repo root):
  python core/evals/golden/agent-code-quality/harness/score_trial.py \\
    --task 01-parse-kv --result path/to/result_tree
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # agent-code-quality/
TASKS = ROOT / "tasks"


def sha256_tree(directory: Path) -> str:
    h = hashlib.sha256()
    if not directory.is_dir():
        return h.hexdigest()
    for path in sorted(directory.rglob("*")):
        if path.is_file():
            rel = path.relative_to(directory).as_posix()
            h.update(rel.encode())
            h.update(path.read_bytes())
    return h.hexdigest()


def list_files(directory: Path) -> set[str]:
    if not directory.is_dir():
        return set()
    return {p.relative_to(directory).as_posix() for p in directory.rglob("*") if p.is_file()}


def score_brief(path: Path | None) -> dict:
    """Optional process score — separate from code correctness."""
    if path is None or not path.is_file():
        return {"process_score": None, "process_notes": "no brief provided"}
    text = path.read_text(encoding="utf-8", errors="replace")
    checks = {
        "has_goal": bool(re.search(r"(?i)\bgoal\b", text)),
        "has_out_of_scope": bool(re.search(r"(?i)out of scope|out-of-scope", text)),
        "criteria_count_ge_4": len(re.findall(r"(?m)^\s*([-*]|\d+\.)\s+", text)) >= 4
        or len(re.findall(r"(?i)criteria", text)) >= 1
        and len(re.findall(r"(?m)^\s*-\s*\[[ xX]\]", text)) >= 4,
        "mentions_verify": bool(re.search(r"(?i)verif|test|assert", text)),
    }
    # Count checkbox-like or numbered binary-looking lines more loosely
    bullets = re.findall(r"(?m)^\s*-\s+.{8,}", text)
    checks["criteria_count_ge_4"] = len(bullets) >= 4 or checks["criteria_count_ge_4"]
    score = sum(1 for v in checks.values() if v) / max(len(checks), 1)
    return {"process_score": round(score, 3), "process_checks": checks}


def load_meta(task_id: str) -> dict:
    meta_path = TASKS / task_id / "meta.json"
    if meta_path.is_file():
        return json.loads(meta_path.read_text(encoding="utf-8"))
    # Backward-compatible default for 01-parse-kv
    return {"impl_file": "parse_kv.py", "env_var": "IMPL_PATH"}


def run_hidden_tests(task_id: str, result_dir: Path) -> tuple[float, int, int, str]:
    """Return (correctness, passed, total, log)."""
    task_dir = TASKS / task_id
    hidden = task_dir / "hidden_tests"
    if not hidden.is_dir():
        raise SystemExit(f"No hidden_tests for task {task_id}")

    meta = load_meta(task_id)
    impl_name = meta.get("impl_file", "parse_kv.py")
    env_var = meta.get("env_var", "IMPL_PATH")

    impl = result_dir / impl_name
    if not impl.is_file():
        candidates = list(result_dir.rglob(impl_name))
        if not candidates:
            return 0.0, 0, 0, f"missing {impl_name}"
        impl = candidates[0]

    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        for f in hidden.glob("test_*.py"):
            shutil.copy2(f, td_path / f.name)
        env = os.environ.copy()
        env[env_var] = str(impl.resolve())
        env["IMPL_PATH"] = str(impl.resolve())  # generic fallback
        # Also place a copy for default path resolution beside tests
        shutil.copy2(impl, td_path / impl_name)
        old = os.environ.copy()
        os.environ.update(env)
        try:
            loader = unittest.TestLoader()
            suite = loader.discover(str(td_path), pattern="test_*.py")
            buf_out = []

            class L(unittest.TextTestResult):
                def addSuccess(self, test):
                    super().addSuccess(test)
                    buf_out.append(f"PASS {test}")

                def addFailure(self, test, err):
                    super().addFailure(test, err)
                    buf_out.append(f"FAIL {test}: {err[1]}")

                def addError(self, test, err):
                    super().addError(test, err)
                    buf_out.append(f"ERROR {test}: {err[1]}")

            runner = unittest.TextTestRunner(
                verbosity=0, resultclass=L, stream=open(os.devnull, "w")
            )
            result = runner.run(suite)
        finally:
            os.environ.clear()
            os.environ.update(old)
        total = result.testsRun
        failed = len(result.failures) + len(result.errors)
        passed = total - failed
        correctness = (passed / total) if total else 0.0
        return correctness, passed, total, "\n".join(buf_out)


def score_scope(task_id: str, result_dir: Path, starter_dir: Path) -> dict:
    """Allow only files that existed in starter plus common new test files agent might add."""
    starter_files = list_files(starter_dir)
    result_files = list_files(result_dir)
    # Ignore __pycache__
    def clean(s: set[str]) -> set[str]:
        return {f for f in s if "__pycache__" not in f and not f.endswith(".pyc")}

    starter_files, result_files = clean(starter_files), clean(result_files)
    allowed_new_prefixes = ("test_", "tests/")
    extra = result_files - starter_files
    forbidden = {
        e
        for e in extra
        if not e.startswith(allowed_new_prefixes)
        and e not in starter_files
        and not e.endswith(".md")  # allow notes
    }
    # Overwriting hidden_tests is handled separately; if agent created hidden_tests, forbid
    forbidden |= {e for e in extra if e.startswith("hidden_tests/")}
    # Modified files that are outside starter set of paths
    scope_ok = len(forbidden) == 0
    return {
        "scope_ok": scope_ok,
        "extra_files": sorted(extra),
        "forbidden_extra": sorted(forbidden),
        "starter_file_count": len(starter_files),
        "result_file_count": len(result_files),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Score an agent coding trial")
    ap.add_argument("--task", required=True, help="Task id, e.g. 01-parse-kv")
    ap.add_argument("--result", required=True, type=Path, help="Result directory (edited starter)")
    ap.add_argument("--brief", type=Path, default=None, help="Optional GXP brief path")
    ap.add_argument("--out", type=Path, default=None, help="Write JSON score here")
    args = ap.parse_args()

    task_dir = TASKS / args.task
    if not task_dir.is_dir():
        print(f"Unknown task: {args.task}", file=sys.stderr)
        return 2

    starter = task_dir / "starter"
    hidden = task_dir / "hidden_tests"
    result = args.result.resolve()

    expected_hash = sha256_tree(hidden)
    # If result contains hidden_tests, hash must match expected
    result_hidden = result / "hidden_tests"
    if result_hidden.is_dir():
        got = sha256_tree(result_hidden)
        no_tamper = got == expected_hash
    else:
        # Scorer uses canonical hidden tests; agent didn't ship them — OK
        no_tamper = True

    correctness, passed, total, log = run_hidden_tests(args.task, result)
    scope = score_scope(args.task, result, starter)
    process = score_brief(args.brief)

    # Composite: never let process inflate code quality
    code_ok = no_tamper and scope["scope_ok"]
    report = {
        "task": args.task,
        "result": str(result),
        "correctness": round(correctness, 4),
        "tests_passed": passed,
        "tests_total": total,
        "no_test_tamper": no_tamper,
        "scope_ok": scope["scope_ok"],
        "scope": scope,
        "process": process,
        "primary_code_score": round(correctness if code_ok else 0.0, 4),
        "disqualified": (not no_tamper),
        "test_log": log,
    }

    text = json.dumps(report, indent=2)
    print(text)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        # Don't write full test_log noise unless wanted — keep full for debugging
        args.out.write_text(text, encoding="utf-8")
    return 0 if not report["disqualified"] else 1


if __name__ == "__main__":
    sys.exit(main())
