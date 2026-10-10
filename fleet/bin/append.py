#!/usr/bin/env python3
"""Append one fleet rating, one experience-memory record, and an optional failure note.

One command for a bot finishing a run. Reads JSONL as utf-8-sig so a leading
BOM (as in core/ratings.jsonl) does not break the hash chain. Writes new
bytes as UTF-8 with no BOM. Runs the store checker in this directory before
and after the append. Refuses to write when the before-check fails.

Does not rewrite existing ledger lines. New failure and regression notes are
created only when absent. Stdlib only. The live store is a Linux box; the
append holds an exclusive flock on the ledgers so two writers do not fork
the chain.

Usage:
  python3 fleet/bin/append.py STORE --task SLUG --brief TEXT \
    --criteria-met N --criteria-total N --rating N --outcome success
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True

try:
    import fcntl
except ImportError:  # pragma: no cover - fleet store host is Linux
    print("append.py needs fcntl (Unix/Linux store host)", file=sys.stderr)
    raise

BIN = Path(__file__).resolve().parent
if str(BIN) not in sys.path:
    sys.path.insert(0, str(BIN))

import check  # noqa: E402  (same directory in the repo and on the installed store)

OUTCOMES = ("success", "failure", "pivot", "refusal")
VARIANTS = ("pure_gxp", "hybrid", "self_modifying", "multi_agent")
MODES = ("full", "lightweight")
SCOPES = ("workflow", "family", "ecosystem")
SLUG_OK = set("abcdefghijklmnopqrstuvwxyz0123456789-")


def _die(message: str, code: int = 2) -> int:
    print(message, file=sys.stderr)
    return code


def _read_fd(fd: int) -> str:
    os.lseek(fd, 0, os.SEEK_SET)
    chunks: list[bytes] = []
    while True:
        block = os.read(fd, 65536)
        if not block:
            break
        chunks.append(block)
    # utf-8-sig strips one leading BOM. Do not use it when encoding writes:
    # Python's utf-8-sig encoder would add a new BOM on every append.
    return b"".join(chunks).decode("utf-8-sig")


def _append_fd(fd: int, line: str) -> None:
    payload = (line + "\n").encode("utf-8")
    os.lseek(fd, 0, os.SEEK_END)
    view = payload
    while view:
        written = os.write(fd, view)
        if written <= 0:
            raise OSError("short write appending ledger line")
        view = view[written:]
    os.fsync(fd)


def _dumps(obj: dict) -> str:
    line = json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
    if "\n" in line or "\r" in line:
        raise ValueError("ledger line would contain a raw newline")
    return line


def _last_chained_hash(text: str) -> str | None:
    prev = None
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        obj = json.loads(stripped)
        if not isinstance(obj, dict) or obj.get("_schema"):
            continue
        entry_hash = obj.get("entry_hash")
        if entry_hash:
            prev = entry_hash
    return prev


def _write_new(path: Path, text: str) -> None:
    data = text.encode("utf-8")
    if not data.endswith(b"\n"):
        data += b"\n"
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o664)
    try:
        view = data
        while view:
            written = os.write(fd, view)
            if written <= 0:
                raise OSError(f"short write creating {path.name}")
            view = view[written:]
        os.fsync(fd)
    finally:
        os.close(fd)
    os.chmod(path, 0o664)


def _failure_markdown(args: argparse.Namespace, slug: str, ts: str) -> str:
    regression = f"regressions/{slug}.md"
    return "\n".join(
        [
            "# Failure capture",
            "",
            f"**Date:** {ts}",
            f"**Task / context:** {args.task}",
            "",
            "## Expected",
            "",
            args.failure_expected.strip(),
            "",
            "## Actual",
            "",
            args.failure_actual.strip(),
            "",
            "## Root cause",
            "",
            args.failure_cause.strip(),
            "",
            "## Detection",
            "",
            "Run the paired regression check and `python3 bin/check.py` on this store.",
            "",
            "## Resolution",
            "",
            args.notes.strip() or "See the run notes on the rating line.",
            "",
            "## Prevention",
            "",
            "Keep the paired regression check current and run it when this class returns.",
            "",
            "## Follow-up",
            "",
            f"- [ ] Re-run the check in `{regression}`",
            "",
            "## Regression check",
            "",
            f"`{regression}`",
            "",
            "## Repeatable?",
            "",
            "Yes",
            "",
        ]
    )


def _regression_markdown(args: argparse.Namespace, slug: str) -> str:
    return "\n".join(
        [
            f"# Regression: {slug}",
            "",
            "Run this check if the incident returns:",
            "",
            args.regression_check.strip(),
            "",
            f"Paired failure: `failures/{slug}.md`",
            "",
        ]
    )


def _split_criteria(values: list[str]) -> list[str]:
    found: list[str] = []
    for value in values:
        for part in value.split(","):
            item = part.strip()
            if not item:
                continue
            if any(ch in item for ch in "\r\n"):
                raise ValueError("failed_criteria entries must be one line")
            found.append(item)
    return found


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("store", help="fleet store root (ratings.jsonl lives here)")
    parser.add_argument("--task", required=True)
    parser.add_argument("--brief", required=True)
    parser.add_argument("--criteria-met", required=True, type=int)
    parser.add_argument("--criteria-total", required=True, type=int)
    parser.add_argument("--rating", required=True, type=int)
    parser.add_argument("--outcome", required=True, choices=OUTCOMES)
    parser.add_argument("--mode", choices=MODES)
    parser.add_argument("--notes", default="")
    parser.add_argument("--ts", help="ISO-8601 timestamp (default: UTC now)")
    parser.add_argument("--variant", default="pure_gxp", choices=VARIANTS)
    parser.add_argument("--iteration", type=int, default=1)
    parser.add_argument(
        "--failed-criteria",
        action="append",
        default=[],
        help="criterion id; repeat the flag or pass a comma-separated list",
    )
    parser.add_argument("--family")
    parser.add_argument("--transfer-scope", choices=SCOPES)
    parser.add_argument("--em-id")
    parser.add_argument(
        "--verified",
        action="store_true",
        help="set the EM verified field (omitted when this flag is absent)",
    )
    parser.add_argument("--failure-slug", help="create failures/<slug>.md and regressions/<slug>.md")
    parser.add_argument("--failure-expected", default="")
    parser.add_argument("--failure-actual", default="")
    parser.add_argument("--failure-cause", default="")
    parser.add_argument(
        "--regression-check",
        default="",
        help="command or procedure named from the failure note",
    )
    return parser


def _validate(args: argparse.Namespace) -> str | None:
    if args.criteria_met < 0 or args.criteria_total < 0:
        return "criteria counts must be >= 0"
    if args.criteria_met > args.criteria_total:
        return "criteria-met cannot exceed criteria-total"
    if not 1 <= args.rating <= 10:
        return "rating must be an integer from 1 to 10"
    if args.iteration < 1:
        return "iteration must be >= 1"
    for label in ("task", "brief", "notes"):
        if "\n" in getattr(args, label) or "\r" in getattr(args, label):
            return f"{label} must be a single line (JSONL keeps one object per line)"
    if not args.task.strip() or not args.brief.strip():
        return "task and brief must be non-empty"
    if args.failure_slug:
        slug = args.failure_slug
        if not slug or len(slug) > 80 or any(ch not in SLUG_OK for ch in slug) or slug.startswith("-"):
            return "failure-slug must be 1-80 chars of [a-z0-9-], not starting with a dash"
        missing = [
            name
            for name, value in (
                ("failure-expected", args.failure_expected),
                ("failure-actual", args.failure_actual),
                ("failure-cause", args.failure_cause),
                ("regression-check", args.regression_check),
            )
            if not value.strip()
        ]
        if missing:
            return "failure note requires " + ", ".join(missing)
        for value in (
            args.failure_expected,
            args.failure_actual,
            args.failure_cause,
            args.regression_check,
        ):
            if "\x00" in value:
                return "failure text must not contain NUL"
    elif any(
        value.strip()
        for value in (
            args.failure_expected,
            args.failure_actual,
            args.failure_cause,
            args.regression_check,
        )
    ):
        return "failure text requires --failure-slug"
    return None


def _run_check(store: Path, label: str) -> int:
    print(f"--- {label} ---")
    return check.main(["check.py", str(store)])


def _append_locked(args: argparse.Namespace, store: Path, ratings_fd: int, vrc) -> int:
    em_path = store / "em-records.jsonl"
    em_fd = os.open(em_path, os.O_RDWR)
    try:
        fcntl.flock(em_fd, fcntl.LOCK_EX)
        code = _run_check(store, "check before")
        if code != 0:
            print("refusing to append; store check failed", file=sys.stderr)
            return code

        slug = args.failure_slug
        failure_ref = ""
        if slug:
            failure_path = store / "failures" / f"{slug}.md"
            regression_path = store / "regressions" / f"{slug}.md"
            if failure_path.exists() or regression_path.exists():
                return _die(
                    f"refusing to overwrite existing failure/regression for slug {slug!r}"
                )
            failure_ref = f"failures/{slug}.md"

        ts = args.ts or dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        if "\n" in ts or "\r" in ts or not ts.strip():
            return _die("ts must be a single non-empty line")

        try:
            failed = _split_criteria(args.failed_criteria)
        except ValueError as exc:
            return _die(str(exc))

        rating = {
            "ts": ts,
            "task": args.task,
            "brief": args.brief,
            "criteria_met": args.criteria_met,
            "criteria_total": args.criteria_total,
            "rating": args.rating,
            "notes": args.notes,
            "failure_ref": failure_ref,
            "prev_hash": _last_chained_hash(_read_fd(ratings_fd)),
        }
        if args.mode:
            rating["mode"] = args.mode
        rating["entry_hash"] = vrc.entry_payload_hash(rating)

        em: dict = {
            "timestamp": ts,
            "variant": args.variant,
            "iteration": args.iteration,
            "outcome": args.outcome,
            "failed_criteria": failed,
            "injected_failure": False,
            "recovery_attempted": False,
            "recovery_success": False,
            "notes": args.notes,
            "topology_change": None,
        }
        if args.outcome == "refusal":
            em["mode"] = "refusal"
        if args.em_id:
            em["id"] = args.em_id
        if args.family:
            em["family"] = args.family
        if args.transfer_scope:
            em["transfer_scope"] = args.transfer_scope
        elif args.family:
            em["transfer_scope"] = "family"
        if args.verified:
            em["verified"] = True

        rating_line = _dumps(rating)
        em_line = _dumps(em)
        wrote_rating = False
        try:
            if slug:
                _write_new(
                    store / "failures" / f"{slug}.md",
                    _failure_markdown(args, slug, ts),
                )
                _write_new(
                    store / "regressions" / f"{slug}.md",
                    _regression_markdown(args, slug),
                )
            _append_fd(ratings_fd, rating_line)
            wrote_rating = True
            _append_fd(em_fd, em_line)
        except OSError as exc:
            print(f"write failed: {exc}", file=sys.stderr)
            if wrote_rating:
                print(
                    "rating line was appended; em line was not — append a corrective record, do not edit the ledger",
                    file=sys.stderr,
                )
            return 1
        print(f"appended ratings.jsonl entry_hash={rating['entry_hash']}")
        print(f"appended em-records.jsonl outcome={args.outcome}")
        if slug:
            print(f"wrote failures/{slug}.md and regressions/{slug}.md")

        code = _run_check(store, "check after")
        if code != 0:
            print("appended but post-check failed", file=sys.stderr)
            return code
        print("OK")
        return 0
    finally:
        try:
            fcntl.flock(em_fd, fcntl.LOCK_UN)
        finally:
            os.close(em_fd)


def main(argv: list[str]) -> int:
    args = _build_parser().parse_args(argv)
    problem = _validate(args)
    if problem:
        return _die(problem)

    store = Path(args.store).expanduser().resolve()
    ratings = store / "ratings.jsonl"
    em_path = store / "em-records.jsonl"
    if not ratings.is_file() or not em_path.is_file():
        print("ledger missing; refusing to create one", file=sys.stderr)
        return _run_check(store, "check before")

    validator_path = check.resolve_validator(store)
    if validator_path is None:
        return _run_check(store, "check before")
    vrc = check.load_ratings_validator(validator_path)

    ratings_fd = os.open(ratings, os.O_RDWR)
    try:
        fcntl.flock(ratings_fd, fcntl.LOCK_EX)
        return _append_locked(args, store, ratings_fd, vrc)
    finally:
        try:
            fcntl.flock(ratings_fd, fcntl.LOCK_UN)
        finally:
            os.close(ratings_fd)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
