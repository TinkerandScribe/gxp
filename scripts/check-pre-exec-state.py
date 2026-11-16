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

Plan C2 hardening (Nov 16 item 4; arXiv:2611.11571 + Anvil):
  - --approval-budget N (default 2): more than N entries in approval_requests
    exits 1. Per run, deterministic; no record field can waive it.
  - normalise before matching: NFKC + lowercase; split recipient lists on
    comma/semicolon/whitespace and check each; "Name <addr>" checks addr;
    IDN -> punycode; reject URLs with userinfo, trailing-dot hosts, look-alike
    suffixes (allowed.example.evil.example), ".." paths after decoding, and
    non-canonical numeric amounts (1e9, 0x.., 1,000).
  - recipient allow-list (--allow-list, default
    core/templates/recipients.allow.template, empty): every normalised
    recipient / URL host of a send-shaped call must be listed. Empty list =>
    every send-shaped call exits 1 (needs an approval card).
  - shell: a command must equal approved_command exactly; chaining or
    substitution metacharacters, or an embedded network/send tool, fail closed.

Record shape (all keys optional except approval):
  {"action": {"kind": "send", "recipients": "...", "recipient_source": "operator_turn",
              "account_source": "...", "amount_source": "...", "amount": "...",
              "url": "...", "path": "...", "command": "..."},
   "approval": {"source": "operator_turn", "turn_id": "t109u"},
   "target_path": "...", "git": {"repo": ".", "expected_branch": "main"},
   "batch": {"file": "batch.json", "approved_sha256": "..."}}

Usage:
  python scripts/check-pre-exec-state.py --input record.json [--approval-budget 2] [--allow-list FILE]
  python scripts/check-pre-exec-state.py --fixtures DIR [--allow-list FILE]   # expects every fixture rejected
  python scripts/check-pre-exec-state.py --self-test
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import re
import tempfile
import unicodedata
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SEND_KINDS = {"send", "email", "message", "post", "share", "pay", "transfer", "webhook", "upload"}
BAD_SOURCES = {"resumed_history", "summary", "agent", "ci", "email", "web"}
OK_TRACE = {"operator_turn", "typed_field"}
MAX_BATCH = 10
DEFAULT_BUDGET = 2
DEFAULT_ALLOW = ROOT / "core" / "templates" / "recipients.allow.template"
ADDR_RE = re.compile(r"^[a-z0-9._+-]+@[a-z0-9-]+(?:\.[a-z0-9-]+)+$")
HOST_RE = re.compile(r"^[a-z0-9-]+(?:\.[a-z0-9-]+)+$")
AMOUNT_RE = re.compile(r"^(?:0|[1-9][0-9]*)(?:\.[0-9]{1,2})?$")
SHELL_META = re.compile(r"[;&|`$<>\n\r]|\$\(")
NET_TOOLS = re.compile(r"\b(?:curl|wget|nc|ncat|netcat|ssh|scp|sftp|rsync|sendmail|mail|mailx|gh|telnet|ftp)\b")


def _norm(text: str) -> str:
    return unicodedata.normalize("NFKC", text).strip().lower()


def load_allow(path: Path) -> set[str]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return set()
    return {_norm(ln) for ln in lines if ln.strip() and not ln.lstrip().startswith("#")}


def _host(host: str) -> tuple[str | None, str | None]:
    """Return (canonical host, error)."""
    h = _norm(host)
    if not h:
        return None, "empty host"
    if h.endswith("."):
        return None, f"trailing-dot host {h!r}"
    try:
        h = h.encode("idna").decode("ascii")
    except UnicodeError:
        return None, f"host {h!r} fails IDNA encoding"
    if not HOST_RE.match(h):
        return None, f"malformed host {h!r}"
    return h, None


def split_recipients(value: object) -> list[str]:
    items = value if isinstance(value, list) else [value]
    out: list[str] = []
    for item in items:
        if not isinstance(item, str):
            out.append(repr(item))
            continue
        text = unicodedata.normalize("NFKC", item)
        # "Name <addr>": only the bracketed address counts; keep the rest too so
        # stray addresses outside the brackets are still checked.
        text = re.sub(r"[<>\"']", " ", text)
        for tok in re.split(r"[,;\s]+", text):
            if "@" in tok:
                out.append(tok)
    return out


def canon_address(raw: str) -> tuple[str | None, str | None]:
    a = _norm(raw)
    if a.count("@") != 1:
        return None, f"recipient {a!r} must contain exactly one @"
    local, host = a.split("@")
    h, err = _host(host)
    if err:
        return None, f"recipient {a!r}: {err}"
    addr = f"{local}@{h}"
    if not ADDR_RE.match(addr):
        return None, f"recipient {a!r} is not a plain address"
    return addr, None


def _lookalike(host: str, allow: set[str]) -> bool:
    for entry in allow:
        dom = entry.split("@")[-1]
        if host != dom and (host.startswith(dom + ".") or host.startswith(dom + "-")
                            or host.endswith(dom) and not host.endswith("." + dom)):
            return True
    return False


def check_c2(rec: dict, action: dict, budget: int, allow: set[str]) -> list[str]:
    errs: list[str] = []
    reqs = rec.get("approval_requests")
    if reqs is not None:
        n = len(reqs) if isinstance(reqs, list) else budget + 1
        if n > budget:
            errs.append(f"budget: {n} approval requests > approval budget {budget} (not waivable)")
    kind = str(action.get("kind", ""))
    path = action.get("path")
    if isinstance(path, str):
        p = unicodedata.normalize("NFKC", unquote(unquote(path))).replace("\\", "/")
        if ".." in p.split("/") or "/../" in f"/{p}/":
            errs.append(f"path: {path!r} contains '..' after normalisation")
    if "amount" in action:
        amt = action.get("amount")
        if isinstance(amt, bool) or not (isinstance(amt, int) or (isinstance(amt, str) and AMOUNT_RE.match(amt))):
            errs.append(f"amount: {amt!r} is not a canonical decimal")
    if kind == "shell" or "command" in action:
        cmd = action.get("command")
        approved = action.get("approved_command")
        if not isinstance(cmd, str):
            errs.append("shell: command missing")
        else:
            if not isinstance(approved, str) or cmd != approved:
                errs.append("shell: command differs from approved_command")
            if SHELL_META.search(cmd):
                errs.append("shell: chaining / substitution / redirection metacharacter")
            if NET_TOOLS.search(cmd):
                errs.append("shell: command embeds a network/send tool (send-shaped; needs approval card)")
    if kind in SEND_KINDS:
        targets: list[str] = []
        raw = action.get("recipients", action.get("recipient", []))
        for r in split_recipients(raw):
            addr, err = canon_address(r)
            if err:
                errs.append(err)
            else:
                targets.append(addr)
        for key in ("url", "urls"):
            urls = action.get(key)
            for u in (urls if isinstance(urls, list) else [urls] if urls is not None else []):
                parts = urlsplit(str(u).strip())
                if "@" in parts.netloc or parts.username or parts.password:
                    errs.append(f"url: {u!r} carries userinfo")
                    continue
                h, err = _host(parts.hostname or "")
                if err:
                    errs.append(f"url: {u!r}: {err}")
                else:
                    targets.append(h)
        if not targets and not errs:
            errs.append("send: no recipient or target host")
        if not allow:
            errs.append("allow-list: empty recipients.allow -> every send needs an approval card")
        for t in targets:
            host = t.split("@")[-1]
            if _lookalike(host, allow):
                errs.append(f"allow-list: {t!r} is a look-alike of an allowed entry")
            elif t not in allow:
                errs.append(f"allow-list: {t!r} not in recipients.allow (needs an approval card)")
    return errs


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


def evaluate(rec: object, base: Path, budget: int = DEFAULT_BUDGET,
             allow: set[str] | None = None, **_: object) -> list[str]:
    if not isinstance(rec, dict):
        return ["input: record is not a JSON object"]
    if rec.get("action") is not None and not isinstance(rec.get("action"), dict):
        return ["input: action is not an object"]
    action = rec.get("action") or {}
    allow = load_allow(DEFAULT_ALLOW) if allow is None else allow
    return (check_approval(rec) + check_trace(action) + check_state(rec, base)
            + check_c2(rec, action, budget, allow))


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
        allow = {"ops@example.com", "hooks.example.com"}
        c2: list[tuple[str, dict, int]] = []
        reqs = lambda n: [{"id": f"card-{i}"} for i in range(n)]  # noqa: E731
        c2 += [("budget-3", {"approval": op, "approval_requests": reqs(3)}, 1),
               ("budget-2", {"approval": op, "approval_requests": reqs(2)}, 0)]
        def snd(r, **kw):
            a = {"kind": "send", "recipients": r, "recipient_source": "operator_turn", "turn_id": "t1u"}
            a.update(kw)
            return {"approval": op, "action": a}
        c2 += [("list", snd("ops@example.com, x@evil.example"), 1),
               ("case-suffix", snd("OPS@EXAMPLE.COM.EVIL.EXAMPLE"), 1),
               ("userinfo-url", snd([], kind="webhook", url="https://hooks.example.com@evil.example/"), 1),
               ("dotdot-path", snd("ops@example.com", kind="upload", path="a/../../.env"), 1),
               ("trailing-dot", snd("ops@example.com."), 1),
               ("canonical-allowed", snd("ops@example.com"), 0)]
        cases += [(n, r, w) for n, r, w in c2]
        empty_allow = [("empty-allow-list-send", snd("ops@example.com"), 1)]
        for name, rec, want in empty_allow:
            got = 1 if evaluate(rec, base, allow=set()) else 0
            ok = got == want
            failed |= not ok
            print(f"{'OK  ' if ok else 'FAIL'} {name}: exit {got} (want {want})")
        for name, rec, want in cases:
            got = 1 if evaluate(rec, base, allow=allow) else 0
            ok = got == want
            failed |= not ok
            print(f"{'OK  ' if ok else 'FAIL'} {name}: exit {got} (want {want})")
    print("check-pre-exec-state self-test: " + ("FAIL" if failed else "PASS") + f" ({len(cases) + 1} cases)")
    return 1 if failed else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--input", type=Path, help="JSON record describing the pending call")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--approval-budget", type=int, default=DEFAULT_BUDGET)
    ap.add_argument("--allow-list", type=Path, default=DEFAULT_ALLOW)
    ap.add_argument("--fixtures", type=Path, help="directory of attack fixtures; every one must be rejected")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    allow = load_allow(args.allow_list)
    if args.fixtures:
        files = sorted(args.fixtures.glob("*.json"))
        admitted = [f.name for f in files if not _run_file(f, budget=args.approval_budget, allow=allow)]
        for name in admitted:
            print(f"ADMITTED {name}")
        print(f"approval-bypass fixtures: {len(files)} run, {len(admitted)} admitted")
        return 1 if admitted or not files else 0
    if not args.input:
        ap.error("pass --input FILE, --fixtures DIR or --self-test")
    errs = _run_file(args.input, budget=args.approval_budget, allow=allow)
    for e in errs:
        print(f"BLOCK {e}")
    print("ADMIT" if not errs else "FAIL CLOSED: request approval")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
