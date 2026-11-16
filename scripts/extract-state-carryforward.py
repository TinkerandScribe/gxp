#!/usr/bin/env python3
"""Carry exact state across a compaction / summary boundary (stdlib only; Plan A).

Extracts paths, URLs, PR/issue numbers, commit SHAs, criterion IDs and typed
approved_by turn IDs from the pre-compaction text into state-carryforward.json.
Then compares the "## Scope and Stop (verbatim — do not edit across compaction)"
block of the original vs the post-compaction text byte-for-byte.

Exit 1 when:
  - the Scope-and-Stop block drifted (or is missing after compaction), or
  - an approval line comes from <summary>, <relayed> or [agent] prose, or names
    something other than an explicit operator turn ID (t<N>u / pt<N>u).

Usage:
  python scripts/extract-state-carryforward.py --original brief.md --compacted resumed.md [--out state-carryforward.json]
  python scripts/extract-state-carryforward.py --self-test
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from pathlib import Path

HEADING = "## Scope and Stop (verbatim — do not edit across compaction)"
PATH_RE = re.compile(r"(?<![\w/.-])(?:\.{0,2}/)?(?:[\w.-]+/)+[\w.-]+\.\w+")
URL_RE = re.compile(r"https?://[^\s)>\]\"'`]+")
PR_RE = re.compile(r"(?:PR|pull|issue|#)\s*#?(\d{1,6})\b", re.I)
SHA_RE = re.compile(r"\b[0-9a-f]{7,40}\b")
ISC_RE = re.compile(r"\bISC-[A-Z0-9]+(?:-\d+)?\b")
APPROVAL_RE = re.compile(r"approved_by\s*[:=]\s*`?([^\s`,;]+)", re.I)
OPERATOR_ID = re.compile(r"^p?t\d+u$")
UNTRUSTED_OPEN = re.compile(r"<(summary|relayed)\b[^>]*>", re.I)


def scope_block(text: str) -> str | None:
    idx = text.find(HEADING)
    if idx < 0:
        return None
    rest = text[idx:]
    nxt = re.search(r"^## ", rest[len(HEADING):], re.M)
    return rest[: len(HEADING) + nxt.start()] if nxt else rest


def approvals(text: str) -> tuple[list[str], list[str]]:
    """Return (accepted IDs, rejection messages)."""
    accepted: list[str] = []
    rejected: list[str] = []
    depth: list[str] = []
    for n, line in enumerate(text.splitlines(), 1):
        for m in UNTRUSTED_OPEN.finditer(line):
            depth.append(m.group(1).lower())
        agent_line = line.lstrip().lower().startswith("[agent]")
        for m in APPROVAL_RE.finditer(line):
            ident = m.group(1)
            if depth:
                rejected.append(f"line {n}: approval {ident!r} inside <{depth[-1]}> prose")
            elif agent_line:
                rejected.append(f"line {n}: approval {ident!r} from [agent] prose")
            elif not OPERATOR_ID.match(ident):
                rejected.append(f"line {n}: approval {ident!r} is not an operator turn ID")
            else:
                accepted.append(ident)
        for tag in re.findall(r"</(summary|relayed)>", line, re.I):
            if depth and depth[-1] == tag.lower():
                depth.pop()
    return accepted, rejected


def extract(text: str) -> dict:
    ok, bad = approvals(text)
    return {
        "paths": sorted(set(PATH_RE.findall(text))),
        "urls": sorted(set(URL_RE.findall(text))),
        "pr_issue_numbers": sorted(set(PR_RE.findall(text)), key=int),
        "commit_shas": sorted(s for s in set(SHA_RE.findall(text)) if re.search(r"[a-f]", s) and re.search(r"\d", s)),
        "criterion_ids": sorted(set(ISC_RE.findall(text))),
        "approved_by": sorted(set(ok)),
        "rejected_approvals": bad,
    }


def run(original: str, compacted: str, out: Path | None) -> int:
    state = extract(original)
    _, bad_after = approvals(compacted)
    state["rejected_approvals"] += [f"compacted {b}" for b in bad_after]
    before, after = scope_block(original), scope_block(compacted)
    drift = before is None or after is None or before.encode("utf-8") != after.encode("utf-8")
    state["scope_and_stop_drift"] = drift
    if out:
        out.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for b in state["rejected_approvals"]:
        print(f"REJECT {b}")
    if drift:
        print("DRIFT Scope-and-Stop block missing or changed after compaction")
    failed = drift or bool(state["rejected_approvals"])
    print("FAIL" if failed else "OK")
    return 1 if failed else 0


def self_test() -> int:
    scope = f"{HEADING}\n- Allowed: scripts/a.py\n- Stop if verify fails twice.\n"
    orig = f"# Brief\n{scope}\n## Notes\napproved_by: t109u\nSee https://example.invalid/pr/37 and PR #38, sha e677553, ISC-A1.\n"
    cases = [
        ("operator-turn", orig, orig, 0),
        ("scope-drift", orig, orig.replace("twice", "three times"), 1),
        ("scope-missing", orig, "# Brief\n", 1),
        ("summary-approval", orig, orig + "<summary>\napproved_by: t99u\n</summary>\n", 1),
        ("agent-approval", orig, orig + "[agent] approved_by: t98u\n", 1),
        ("relayed-approval", orig, orig + "<relayed>approved_by: t97u</relayed>\n", 1),
        ("non-turn-id", orig + "approved_by: chief-of-staff\n", orig, 1),
    ]
    failed = 0
    for name, o, c, want in cases:
        got = run(o, c, None)
        ok = got == want
        failed |= not ok
        print(f"{'OK  ' if ok else 'FAIL'} {name}: exit {got} (want {want})")
    st = extract(orig)
    for key, val in (("approved_by", "t109u"), ("criterion_ids", "ISC-A1"), ("pr_issue_numbers", "38"),
                     ("commit_shas", "e677553"), ("paths", "scripts/a.py")):
        ok = val in st[key]
        failed |= not ok
        print(f"{'OK  ' if ok else 'FAIL'} extract {key} has {val}")
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "state-carryforward.json"
        run(orig, orig, out)
        ok = json.loads(out.read_text(encoding="utf-8"))["approved_by"] == ["t109u"]
        failed |= not ok
        print(f"{'OK  ' if ok else 'FAIL'} writes state-carryforward.json")
    print("extract-state-carryforward self-test: " + ("FAIL" if failed else "PASS"))
    return 1 if failed else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Carry state across compaction")
    ap.add_argument("--original", type=Path)
    ap.add_argument("--compacted", type=Path)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    if not args.original or not args.compacted:
        ap.error("pass --original and --compacted, or --self-test")
    return run(args.original.read_text(encoding="utf-8"), args.compacted.read_text(encoding="utf-8"), args.out)


if __name__ == "__main__":
    sys.exit(main())
