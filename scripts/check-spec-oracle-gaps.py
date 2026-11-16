#!/usr/bin/env python3
"""Find test oracles the brief never stated (stdlib only; Plan B).

Scans named test files for asserted string literals, routes, CLI flags and
imported / referenced exported symbols, and reports each one absent from the
brief text. Agent-written tests that assert things the brief never said are a
spec-oracle gap: the test encodes the implementer's guess, not the request.

Exit 1 if any gap is found, 0 otherwise.

Usage:
  python scripts/check-spec-oracle-gaps.py --brief brief.md --tests tests/test_x.py [...] [--ignore TOKEN ...]
  python scripts/check-spec-oracle-gaps.py --self-test
"""
from __future__ import annotations

import argparse
import re
import sys
import tempfile
from pathlib import Path

STR_RE = re.compile(r"""(?P<q>['"])(?P<s>(?:\\.|(?!(?P=q)).)*)(?P=q)""")
ROUTE_RE = re.compile(r"""['"](/[A-Za-z0-9_\-/{}:.]+)['"]""")
FLAG_RE = re.compile(r"""(?<![\w-])(--[a-z][a-z0-9-]+)""")
IMPORT_RE = re.compile(r"^[ \t]*from[ \t]+[\w.]+[ \t]+import[ \t]+\(?([\w, \t]+)\)?", re.M)
ATTR_RE = re.compile(r"\b(?:mod|module|lib|app|api)\.([A-Za-z_]\w*)\(")


def oracle_tokens(test_text: str) -> set[str]:
    toks: set[str] = set()
    for line in test_text.splitlines():
        if "assert" in line or "raises" in line:
            for m in STR_RE.finditer(line):
                s = m.group("s")
                if len(s) >= 3 and re.search(r"[A-Za-z]", s):
                    toks.add(s)
    toks.update(ROUTE_RE.findall(test_text))
    toks.update(FLAG_RE.findall(test_text))
    for m in IMPORT_RE.finditer(test_text):
        for name in m.group(1).replace("\n", " ").split(","):
            name = name.strip()
            if name and not name.startswith("_") and name not in {"annotations"}:
                toks.add(name)
    toks.update(ATTR_RE.findall(test_text))
    return toks


def gaps(brief: str, tests: list[str], ignore: set[str]) -> list[str]:
    found: set[str] = set()
    for t in tests:
        found |= oracle_tokens(t)
    return sorted(tok for tok in found if tok not in ignore and tok not in brief)


def run(brief_path: Path, test_paths: list[Path], ignore: set[str]) -> int:
    brief = brief_path.read_text(encoding="utf-8")
    missing = gaps(brief, [p.read_text(encoding="utf-8") for p in test_paths], ignore)
    for tok in missing:
        print(f"GAP test asserts {tok!r} which the brief never states")
    print("FAIL" if missing else "OK")
    return 1 if missing else 0


def self_test() -> int:
    brief = "Add parse_window(spec) to window.py. CLI flag --tz selects the zone. Route /api/window returns 'ok'."
    good = ("from window import parse_window\n"
            "def test_a():\n    assert parse_window('9-5') == 'ok'\n"
            "def test_cli():\n    run(['--tz', 'UTC'])\n    get('/api/window')\n")
    bad = good + "def test_b():\n    assert parse_window('x') == 'overnight-wrap'\n    run(['--strict'])\n"
    failed = 0
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp)
        (p / "brief.md").write_text(brief, encoding="utf-8")
        (p / "test_good.py").write_text(good, encoding="utf-8")
        (p / "test_bad.py").write_text(bad, encoding="utf-8")
        for name, test, want in (("stated-oracles", "test_good.py", 0), ("unstated-symbol", "test_bad.py", 1)):
            got = run(p / "brief.md", [p / test], {"UTC", "9-5"})
            ok = got == want
            failed |= not ok
            print(f"{'OK  ' if ok else 'FAIL'} {name}: exit {got} (want {want})")
    print("check-spec-oracle-gaps self-test: " + ("FAIL" if failed else "PASS"))
    return 1 if failed else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Report test oracles absent from the brief")
    ap.add_argument("--brief", type=Path)
    ap.add_argument("--tests", type=Path, nargs="+")
    ap.add_argument("--ignore", nargs="*", default=[])
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    if not args.brief or not args.tests:
        ap.error("pass --brief and --tests, or --self-test")
    return run(args.brief, args.tests, set(args.ignore))


if __name__ == "__main__":
    sys.exit(main())
