#!/usr/bin/env python3
"""Tests for fleet/bin/append.py.

Covers an empty store, an appended hash chain, and a BOM-prefixed ledger
(including a copy of core/ratings.jsonl). Also checks the optional failure
note, a refused append when the checker is already red, and the installed
store copy with no checkout on the parent path.
"""
from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True

REPO = Path(__file__).resolve().parents[1]
APPEND = REPO / "fleet" / "bin" / "append.py"
CHECK = REPO / "fleet" / "bin" / "check.py"
VALIDATOR = REPO / "scripts" / "validate-ratings-chain.py"
CORE_RATINGS = REPO / "core" / "ratings.jsonl"
BOM = b"\xef\xbb\xbf"
NOTES = 'cost is $YELLOW and a "quote" \\\\ path \u03c4'


def _load_validator():
    spec = importlib.util.spec_from_file_location("gxp_validate_ratings_chain", VALIDATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load ratings validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


VRC = _load_validator()


def _make_store(root: Path, ratings: bytes = b"") -> Path:
    store = root / "store"
    for name in ("jobs", "failures", "regressions"):
        directory = store / name
        directory.mkdir(parents=True)
        (directory / ".gitkeep").write_bytes(b"")
    (store / "ratings.jsonl").write_bytes(ratings)
    (store / "em-records.jsonl").write_bytes(b"")
    return store


def _run(cmd: list[str], env: dict | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, capture_output=True, text=True, env=env)


def _append(store: Path, extra: list[str], script: Path = APPEND, env: dict | None = None):
    cmd = [
        sys.executable,
        str(script),
        str(store),
        "--task",
        "fleet-append",
        "--brief",
        "writer test",
        "--criteria-met",
        "1",
        "--criteria-total",
        "1",
        "--rating",
        "8",
        "--mode",
        "lightweight",
        "--outcome",
        "success",
        "--notes",
        NOTES,
        *extra,
    ]
    return _run(cmd, env=env)


def _lines(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8-sig")
    found = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        found.append(json.loads(stripped))
    return found


def _chained(path: Path) -> list[dict]:
    return [obj for obj in _lines(path) if obj.get("entry_hash") and not obj.get("_schema")]


def _assert_chain(path: Path) -> None:
    result = _run([sys.executable, str(VALIDATOR), str(path)])
    if result.returncode != 0:
        raise AssertionError(result.stderr or result.stdout)
    prev = None
    for obj in _chained(path):
        if VRC.entry_payload_hash(obj) != obj["entry_hash"]:
            raise AssertionError("entry_hash does not match payload")
        if prev is not None and obj.get("prev_hash") != prev:
            raise AssertionError(f"prev_hash {obj.get('prev_hash')} != {prev}")
        prev = obj["entry_hash"]


def _assert_check(store: Path, script: Path = CHECK) -> None:
    result = _run([sys.executable, str(script), str(store)])
    if result.returncode != 0:
        raise AssertionError(result.stdout + result.stderr)


def test_empty_store() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        store = _make_store(Path(tmp))
        result = _append(store, ["--ts", "2026-10-10T00:00:00Z", "--family", "fleet", "--verified"])
        if result.returncode != 0:
            raise AssertionError(result.stdout + result.stderr)
        if "--- check before ---" not in result.stdout or "--- check after ---" not in result.stdout:
            raise AssertionError("writer did not run the checker before and after")
        if not result.stdout.strip().endswith("OK"):
            raise AssertionError(result.stdout)
        raw = (store / "ratings.jsonl").read_bytes()
        if raw.startswith(BOM):
            raise AssertionError("empty-store append introduced a BOM")
        ratings = _lines(store / "ratings.jsonl")
        if len(ratings) != 1:
            raise AssertionError(f"expected 1 rating, got {len(ratings)}")
        row = ratings[0]
        if row["prev_hash"] is not None:
            raise AssertionError(f"genesis prev_hash should be null, got {row['prev_hash']!r}")
        if row["notes"] != NOTES or row["rating"] != 8:
            raise AssertionError(f"rating fields not round-tripped: {row}")
        em = _lines(store / "em-records.jsonl")
        if len(em) != 1 or em[0]["outcome"] != "success" or em[0]["failed_criteria"] != []:
            raise AssertionError(f"em record missing required fields: {em}")
        if em[0].get("family") != "fleet" or em[0].get("transfer_scope") != "family" or em[0].get("verified") is not True:
            raise AssertionError(f"optional em fields missing: {em[0]}")
        _assert_chain(store / "ratings.jsonl")
        _assert_check(store)


def test_appended_chain() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        store = _make_store(Path(tmp))
        first = _append(store, ["--ts", "2026-10-10T00:00:01Z", "--task", "chain-1"])
        if first.returncode != 0:
            raise AssertionError(first.stdout + first.stderr)
        second = _append(
            store,
            ["--ts", "2026-10-10T00:00:02Z", "--task", "chain-2", "--rating", "6", "--criteria-met", "0"],
        )
        if second.returncode != 0:
            raise AssertionError(second.stdout + second.stderr)
        chained = _chained(store / "ratings.jsonl")
        if len(chained) != 2:
            raise AssertionError(f"expected 2 chained rows, got {len(chained)}")
        if chained[1]["prev_hash"] != chained[0]["entry_hash"]:
            raise AssertionError("second row does not chain to the first")
        if chained[0]["prev_hash"] is not None:
            raise AssertionError("first row is not genesis")
        _assert_chain(store / "ratings.jsonl")
        _assert_check(store)


def _bom_parent_line() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        parent = {
            "ts": "2026-10-09T00:00:00Z",
            "task": "bom-parent",
            "brief": "prefixed",
            "criteria_met": 1,
            "criteria_total": 1,
            "rating": 7,
            "notes": "parent",
            "failure_ref": "",
            "prev_hash": None,
        }
        parent["entry_hash"] = VRC.entry_payload_hash(parent)
        line = json.dumps(parent, ensure_ascii=False, separators=(",", ":")) + "\n"
        blob = BOM + line.encode("utf-8")
        store = _make_store(Path(tmp), ratings=blob)
        # A utf-8 read keeps the BOM on line 1, which is the bug the writer must survive.
        utf8_line = (store / "ratings.jsonl").read_text(encoding="utf-8").splitlines()[0]
        try:
            json.loads(utf8_line)
        except json.JSONDecodeError:
            pass
        else:
            raise AssertionError("fixture line was valid under utf-8; BOM did not prefix it")
        result = _append(store, ["--ts", "2026-10-10T00:00:03Z", "--task", "bom-child"])
        if result.returncode != 0:
            raise AssertionError(result.stdout + result.stderr)
        data = (store / "ratings.jsonl").read_bytes()
        if not data.startswith(BOM) or data.count(BOM) != 1:
            raise AssertionError("writer rewrote or duplicated the leading BOM")
        chained = _chained(store / "ratings.jsonl")
        if len(chained) != 2 or chained[1]["prev_hash"] != parent["entry_hash"]:
            raise AssertionError(f"BOM parent was not the chain head: {chained}")
        _assert_chain(store / "ratings.jsonl")
        _assert_check(store)


def _bom_core_ratings_copy() -> None:
    original = CORE_RATINGS.read_bytes()
    if not original.startswith(BOM):
        raise AssertionError("core/ratings.jsonl no longer starts with a UTF-8 BOM")
    with tempfile.TemporaryDirectory() as tmp:
        store = _make_store(Path(tmp), ratings=original)
        before = _chained(store / "ratings.jsonl")
        if not before:
            raise AssertionError("core/ratings.jsonl has no chained rows to extend")
        parent_hash = before[-1]["entry_hash"]
        result = _append(store, ["--ts", "2026-10-10T00:00:04Z", "--task", "after-core"])
        if result.returncode != 0:
            raise AssertionError(result.stdout + result.stderr)
        data = (store / "ratings.jsonl").read_bytes()
        if not data.startswith(BOM) or data.count(BOM) != 1:
            raise AssertionError("core ledger BOM was not preserved")
        chained = _chained(store / "ratings.jsonl")
        if chained[-1]["prev_hash"] != parent_hash or chained[-1]["task"] != "after-core":
            raise AssertionError("append did not chain from the last core entry_hash")
        _assert_chain(store / "ratings.jsonl")
        _assert_check(store)


def test_bom_prefixed_file() -> None:
    _bom_parent_line()
    _bom_core_ratings_copy()


def test_refusal_sets_em_mode() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        store = _make_store(Path(tmp))
        result = _append(
            store,
            ["--ts", "2026-10-10T00:00:10Z", "--outcome", "refusal", "--task", "refused-run"],
        )
        if result.returncode != 0:
            raise AssertionError(result.stdout + result.stderr)
        em = _lines(store / "em-records.jsonl")
        if len(em) != 1 or em[0]["outcome"] != "refusal" or em[0].get("mode") != "refusal":
            raise AssertionError(f"refusal record was not marked: {em}")
        if _lines(store / "ratings.jsonl")[0]["failure_ref"] != "":
            raise AssertionError("refusal without a failure slug should leave failure_ref empty")


def test_failure_note_and_regression() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        store = _make_store(Path(tmp))
        result = _append(
            store,
            [
                "--ts",
                "2026-10-10T00:00:05Z",
                "--outcome",
                "failure",
                "--rating",
                "4",
                "--criteria-met",
                "0",
                "--failed-criteria",
                "chain-intact,bom-safe",
                "--failure-slug",
                "bom-append",
                "--failure-expected",
                "ledger accepts a BOM",
                "--failure-actual",
                "utf-8 read raised JSONDecodeError",
                "--failure-cause",
                "snippet opened the file as utf-8",
                "--regression-check",
                "python3 scripts/test-fleet-append.py",
            ],
        )
        if result.returncode != 0:
            raise AssertionError(result.stdout + result.stderr)
        failure = (store / "failures" / "bom-append.md").read_text(encoding="utf-8")
        regression = (store / "regressions" / "bom-append.md").read_text(encoding="utf-8")
        if "regressions/bom-append.md" not in failure:
            raise AssertionError("failure note does not name its regression path")
        if "python3 scripts/test-fleet-append.py" not in regression:
            raise AssertionError("regression note missing the check")
        if not failure.strip() or not regression.strip():
            raise AssertionError("failure or regression note is empty")
        row = _lines(store / "ratings.jsonl")[-1]
        if row["failure_ref"] != "failures/bom-append.md":
            raise AssertionError(f"failure_ref not set: {row['failure_ref']!r}")
        em = _lines(store / "em-records.jsonl")[-1]
        if em["outcome"] != "failure" or em["failed_criteria"] != ["chain-intact", "bom-safe"]:
            raise AssertionError(f"em failure fields wrong: {em}")
        mode = (store / "failures" / "bom-append.md").stat().st_mode & 0o777
        if mode != 0o664:
            raise AssertionError(f"failure note mode {oct(mode)} != 0o664")
        again = _append(
            store,
            [
                "--ts",
                "2026-10-10T00:00:06Z",
                "--failure-slug",
                "bom-append",
                "--failure-expected",
                "x",
                "--failure-actual",
                "y",
                "--failure-cause",
                "z",
                "--regression-check",
                "true",
            ],
        )
        if again.returncode == 0:
            raise AssertionError("second failure slug was overwritten")
        if len(_lines(store / "ratings.jsonl")) != 1:
            raise AssertionError("refused failure append still wrote a rating")
        _assert_check(store)


def test_refuses_when_check_fails() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        store = _make_store(Path(tmp), ratings=b"{not json\n")
        before = (store / "ratings.jsonl").read_bytes()
        result = _append(store, ["--ts", "2026-10-10T00:00:07Z"])
        if result.returncode == 0:
            raise AssertionError("append succeeded on an invalid ledger")
        if (store / "ratings.jsonl").read_bytes() != before:
            raise AssertionError("refused append changed the ledger")
        if _lines(store / "em-records.jsonl"):
            raise AssertionError("refused append wrote an em record")
        broken = _make_store(Path(tmp) / "nl")
        # non-empty file with no trailing newline fails the existing checker
        (broken / "ratings.jsonl").write_bytes(b'{"a": 1}')
        snapshot = (broken / "ratings.jsonl").read_bytes()
        refused = _append(broken, ["--ts", "2026-10-10T00:00:08Z"])
        if refused.returncode == 0:
            raise AssertionError("append succeeded without a trailing newline")
        if (broken / "ratings.jsonl").read_bytes() != snapshot:
            raise AssertionError("newline refusal changed the ledger")


def test_installed_store_without_checkout() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        store = Path(tmp) / "store"
        install = _run(["bash", str(REPO / "fleet" / "install-to-store.sh"), str(store)])
        if install.returncode != 0:
            raise AssertionError(install.stderr or install.stdout)
        script = store / "bin" / "append.py"
        if not script.is_file():
            raise AssertionError("install-to-store.sh did not copy bin/append.py")
        mode = script.stat().st_mode & 0o777
        if mode != 0o775:
            raise AssertionError(f"installed append.py mode {oct(mode)} != 0o775")
        probe = _run(
            [
                sys.executable,
                "-c",
                "import sys\n"
                "from pathlib import Path\n"
                "script = Path(sys.argv[1]).resolve()\n"
                "for candidate in script.parents:\n"
                "    if (candidate / 'scripts' / 'validate-ratings-chain.py').is_file():\n"
                "        raise SystemExit('parent walk reaches a checkout at %s' % candidate)\n",
                str(script),
            ]
        )
        if probe.returncode != 0:
            raise AssertionError(probe.stdout + probe.stderr)
        env = os.environ.copy()
        env.pop("GXP_REPO", None)
        result = _append(
            store,
            ["--ts", "2026-10-10T00:00:09Z", "--task", "installed-append"],
            script=script,
            env=env,
        )
        if result.returncode != 0:
            raise AssertionError(result.stdout + result.stderr)
        if "installed-append" not in (store / "ratings.jsonl").read_text(encoding="utf-8-sig"):
            raise AssertionError("installed writer did not append")
        _assert_chain(store / "ratings.jsonl")
        installed_check = store / "bin" / "check.py"
        _assert_check(store, script=installed_check)
        again = _run(["bash", str(REPO / "fleet" / "install-to-store.sh"), str(store)])
        if again.returncode != 0:
            raise AssertionError(again.stderr or again.stdout)
        if "installed-append" not in (store / "ratings.jsonl").read_text(encoding="utf-8-sig"):
            raise AssertionError("reinstall rewrote the ledger")


def test_readme_points_at_writer() -> None:
    readme = (REPO / "fleet" / "README.md").read_text(encoding="utf-8")
    if "fleet/bin/append.py" not in readme or "bin/append.py" not in readme:
        raise AssertionError("fleet README does not point at the writer")
    if "for l in open" in readme or 'encoding="utf-8"' in readme:
        raise AssertionError("fleet README still contains the utf-8 append snippet")


def main() -> int:
    tests = [
        test_empty_store,
        test_appended_chain,
        test_bom_prefixed_file,
        test_refusal_sets_em_mode,
        test_failure_note_and_regression,
        test_refuses_when_check_fails,
        test_installed_store_without_checkout,
        test_readme_points_at_writer,
    ]
    failed = 0
    for test in tests:
        try:
            test()
        except Exception as exc:
            failed += 1
            print(f"FAIL {test.__name__}: {exc}")
        else:
            print(f"OK {test.__name__}")
    print(f"fleet append tests: {len(tests) - failed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
