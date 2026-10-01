#!/usr/bin/env python3
"""Integrity check for the shared GXP fleet records store (stdlib only).

Usage: python3 fleet/bin/check.py [STORE_ROOT]
  STORE_ROOT defaults to the parent of this bin/ directory
  (fleet/ in the repo, /home/box/shared/gxp after install).

The ratings hash chain is scripts/validate-ratings-chain.py. Job contracts
are checked for the top-level "required" fields of
core/templates/job-contract.schema.json. Both files are resolved in this
order: $GXP_REPO, a parent directory that is a gxp checkout, then the
store copies bin/validate_ratings_chain.py and schema/job-contract.schema.json.
Inside this repo the parent walk hits the checkout. An installed store with
no checkout uses the copies fleet/install-to-store.sh places beside the
checker. Stdlib only; the repo tree does not vendor those copies under fleet/.

Checks:
  1. every line of every *.jsonl under the store parses as a JSON object
     (blank lines and lines starting with '#' are skipped, matching gxp's validator);
  2. ratings.jsonl hash chain, via the repo validator;
  3. jobs/*/contract.json parses as a JSON object; required fields come from
     the repo job-contract schema; job_id (if present) must equal the folder name;
  4. every file under failures/ and regressions/ is a non-empty .md file.
Exit 0 when clean; exit 1 with a concise report otherwise.
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
IGNORED = {".gitkeep", ".keep"}
RATINGS_REL = Path("scripts") / "validate-ratings-chain.py"
SCHEMA_REL = Path("core") / "templates" / "job-contract.schema.json"
STORE_VALIDATOR_NAME = "validate_ratings_chain.py"
STORE_SCHEMA_REL = Path("schema") / "job-contract.schema.json"


def _first_file(candidates: list[Path]) -> Path | None:
    seen: set[Path] = set()
    for path in candidates:
        resolved = path.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        if resolved.is_file():
            return resolved
    return None


def _checkout_roots() -> list[Path]:
    """$GXP_REPO first, then parents of this file (nearest first)."""
    roots: list[Path] = []
    env = os.environ.get("GXP_REPO")
    if env:
        roots.append(Path(env).expanduser().resolve())
    roots.extend(HERE.parents)
    return roots


def resolve_validator(store: Path) -> Path | None:
    candidates = [root / RATINGS_REL for root in _checkout_roots()]
    candidates.append(HERE / STORE_VALIDATOR_NAME)
    candidates.append(store / "bin" / STORE_VALIDATOR_NAME)
    return _first_file(candidates)


def resolve_schema(store: Path) -> Path | None:
    candidates = [root / SCHEMA_REL for root in _checkout_roots()]
    candidates.append(HERE.parent / STORE_SCHEMA_REL)
    candidates.append(store / STORE_SCHEMA_REL)
    return _first_file(candidates)


def load_ratings_validator(path: Path):
    spec = importlib.util.spec_from_file_location("gxp_validate_ratings_chain", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_jsonl(root: Path, errs: list[str]) -> set[Path]:
    bad: set[Path] = set()
    for path in sorted(root.rglob("*.jsonl")):
        rel = path.relative_to(root)
        try:
            text = path.read_text(encoding="utf-8-sig")
        except OSError as exc:
            errs.append(f"{rel}: unreadable ({exc})")
            bad.add(path)
            continue
        if text and not text.endswith("\n"):
            errs.append(f"{rel}: missing trailing newline (next append would corrupt last line)")
        for i, line in enumerate(text.splitlines(), 1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            try:
                obj = json.loads(stripped)
            except json.JSONDecodeError as exc:
                errs.append(f"{rel}:{i}: invalid JSON ({exc.msg})")
                bad.add(path)
                continue
            if not isinstance(obj, dict):
                errs.append(f"{rel}:{i}: line is not a JSON object")
                bad.add(path)
    return bad


def check_ratings_chain(root: Path, bad_jsonl: set[Path], errs: list[str], vrc) -> str:
    path = root / "ratings.jsonl"
    if not path.exists():
        errs.append("ratings.jsonl: missing")
        return "missing"
    if path in bad_jsonl:
        return "skipped (unparseable lines)"
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            rc = vrc.main(path)
        except Exception as exc:
            rc = 1
            print(f"validator crashed: {exc}", file=sys.stderr)
    if rc != 0:
        errs.append(f"ratings.jsonl chain: {err.getvalue().strip() or 'failed'}")
        return "FAIL"
    return out.getvalue().strip()


def load_required_fields(path: Path | None, errs: list[str]) -> tuple[list[str] | None, str]:
    mode = "basic required-field check (stdlib)"
    if path is None:
        errs.append(
            "schema: cannot find core/templates/job-contract.schema.json "
            "(tried $GXP_REPO, parent directories, and schema/job-contract.schema.json)"
        )
        return None, "missing schema"
    try:
        schema = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        errs.append(f"{path}: unreadable ({exc})")
        return None, "broken schema"
    if not isinstance(schema, dict):
        errs.append(f"{path}: schema is not a JSON object")
        return None, "broken schema"
    required = schema.get("required", [])
    if not isinstance(required, list) or not all(isinstance(item, str) for item in required):
        errs.append(f"{path}: required is not a list of strings")
        return None, "broken schema"
    return required, mode


def check_jobs(root: Path, errs: list[str], required: list[str] | None) -> int:
    jobs = root / "jobs"
    count = 0
    if not jobs.is_dir():
        errs.append("jobs/: missing")
        return 0
    for entry in sorted(jobs.iterdir()):
        if entry.name in IGNORED:
            continue
        if not entry.is_dir():
            errs.append(f"jobs/{entry.name}: stray file (expected one folder per job_id)")
            continue
        count += 1
        contract = entry / "contract.json"
        rel = f"jobs/{entry.name}/contract.json"
        if not contract.exists():
            errs.append(f"{rel}: missing")
            continue
        try:
            obj = json.loads(contract.read_text(encoding="utf-8-sig"))
        except (OSError, json.JSONDecodeError) as exc:
            errs.append(f"{rel}: invalid JSON ({exc})")
            continue
        if not isinstance(obj, dict):
            errs.append(f"{rel}: not a JSON object")
            continue
        if "job_id" in obj and obj["job_id"] != entry.name:
            errs.append(f"{rel}: job_id {obj['job_id']!r} != folder name {entry.name!r}")
        if required is not None:
            missing = [key for key in required if key not in obj]
            if missing:
                errs.append(f"{rel}: missing required field(s): {', '.join(missing)}")
    return count


def check_md_dirs(root: Path, errs: list[str]) -> int:
    count = 0
    for sub in ("failures", "regressions"):
        directory = root / sub
        if not directory.is_dir():
            errs.append(f"{sub}/: missing")
            continue
        for path in sorted(directory.rglob("*")):
            if path.is_dir() or path.name in IGNORED:
                continue
            count += 1
            rel = path.relative_to(root)
            if path.suffix.lower() != ".md":
                errs.append(f"{rel}: not a .md file")
                continue
            try:
                body = path.read_text(encoding="utf-8-sig")
            except OSError as exc:
                errs.append(f"{rel}: unreadable ({exc})")
                continue
            if not body.strip():
                errs.append(f"{rel}: empty")
    return count


def main(argv: list[str]) -> int:
    root = Path(argv[1]).resolve() if len(argv) > 1 else HERE.parent
    errs: list[str] = []
    vrc = None
    validator_path = resolve_validator(root)
    if validator_path is None:
        errs.append(
            "repo: cannot find scripts/validate-ratings-chain.py "
            "(tried $GXP_REPO, parent directories, and bin/validate_ratings_chain.py)"
        )
    else:
        try:
            vrc = load_ratings_validator(validator_path)
        except Exception as exc:
            errs.append(f"repo: failed to load {validator_path} ({exc})")
    required, mode = load_required_fields(resolve_schema(root), errs)

    bad = check_jsonl(root, errs)
    if vrc is None:
        chain = "skipped (ratings validator unavailable)"
        if not (root / "ratings.jsonl").exists():
            errs.append("ratings.jsonl: missing")
    else:
        chain = check_ratings_chain(root, bad, errs, vrc)
    n_jobs = check_jobs(root, errs, required)
    n_md = check_md_dirs(root, errs)
    print(f"store: {root}")
    print(f"ratings chain: {chain}")
    print(f"jobs: {n_jobs} checked; schema: {mode}")
    print(f"failures/regressions entries: {n_md}")
    if errs:
        print(f"FAIL ({len(errs)} problem(s)):")
        for err in errs:
            print(f"  - {err}")
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
