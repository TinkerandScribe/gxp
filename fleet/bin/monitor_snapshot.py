#!/usr/bin/env python3
"""Hash monitor-class config before/after a run (stdlib only; Plan A, Nov 9 item 2(b)).

Snapshot = for every agents/*/automations/*/automation.json whose tags include
"monitor": enabled, cron, sha256(prompt) and sorted recipients; plus, when
--alerts FILE is given, every entry of an external alert-list JSON export
(id, enabled, sorted recipients).

Any difference between two snapshots exits 1 unless --approval-turn ID is
supplied (a typed operator turn ID). Quiet / no-send rules never authorize
muting, re-routing or deleting a monitor.

Usage:
  python fleet/bin/monitor_snapshot.py snap --root DIR [--alerts FILE] --out before.json
  python fleet/bin/monitor_snapshot.py compare --before before.json --root DIR [--alerts FILE] [--approval-turn ID]
  python fleet/bin/monitor_snapshot.py --self-test
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True


def _recips(obj: dict) -> list[str]:
    r = obj.get("recipients", [])
    if isinstance(r, str):
        r = [r]
    return sorted(str(x).strip().lower() for x in r if str(x).strip()) if isinstance(r, list) else []


def snapshot(root: Path, alerts: Path | None = None) -> dict:
    snap: dict[str, dict] = {}
    for path in sorted(root.glob("agents/*/automations/*/automation.json")):
        try:
            cfg = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            snap[str(path.relative_to(root))] = {"error": "unreadable"}
            continue
        tags = cfg.get("tags", []) if isinstance(cfg, dict) else []
        if not isinstance(tags, list) or "monitor" not in tags:
            continue
        prompt = str(cfg.get("prompt", ""))
        snap[str(path.relative_to(root))] = {
            "enabled": bool(cfg.get("enabled", False)),
            "cron": cfg.get("cron"),
            "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
            "recipients": _recips(cfg),
        }
    if alerts is not None:
        try:
            data = json.loads(alerts.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            data = None
        if not isinstance(data, list):
            snap["alerts:" + alerts.name] = {"error": "unreadable"}
        else:
            for item in data:
                if isinstance(item, dict):
                    snap[f"alert:{item.get('id')}"] = {"enabled": bool(item.get("enabled", False)),
                                                       "recipients": _recips(item)}
    return snap


def compare(before: dict, after: dict, approval_turn: str | None) -> int:
    changed = sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))
    for k in changed:
        print(f"DIFF {k}: before={json.dumps(before.get(k), sort_keys=True)} after={json.dumps(after.get(k), sort_keys=True)}")
    if not changed:
        print("OK monitor config unchanged")
        return 0
    if approval_turn and approval_turn.strip():
        print(f"OK monitor config changed with operator approval turn {approval_turn.strip()}")
        return 0
    print("FAIL monitor config changed without --approval-turn (approval-card action)")
    return 1


def self_test() -> int:
    failed = 0
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        a = root / "agents" / "bot1" / "automations" / "watch" / "automation.json"
        a.parent.mkdir(parents=True)
        base = {"tags": ["monitor"], "enabled": True, "cron": "0 7 * * *",
                "prompt": "check the alert inbox", "recipients": ["owner@example.invalid"]}
        a.write_text(json.dumps(base), encoding="utf-8")
        before = snapshot(root)
        cases = []
        cases.append(("unchanged", dict(base), None, 0))
        cases.append(("disabled-monitor", dict(base, enabled=False), None, 1))
        cases.append(("disabled-monitor+approval", dict(base, enabled=False), "t1u", 0))
        cases.append(("recipient-emptied", dict(base, recipients=[]), None, 1))
        cases.append(("recipient-emptied+approval", dict(base, recipients=[]), "t1u", 0))
        for name, cfg, turn, want in cases:
            a.write_text(json.dumps(cfg), encoding="utf-8")
            got = compare(before, snapshot(root), turn)
            ok = got == want
            failed |= not ok
            print(f"{'OK  ' if ok else 'FAIL'} {name}: exit {got} (want {want})")
    print("monitor_snapshot self-test: " + ("FAIL" if failed else "PASS"))
    return 1 if failed else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Monitor-class config snapshot / compare")
    ap.add_argument("--self-test", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    s = sub.add_parser("snap")
    s.add_argument("--root", type=Path, required=True)
    s.add_argument("--alerts", type=Path)
    s.add_argument("--out", type=Path, required=True)
    c = sub.add_parser("compare")
    c.add_argument("--before", type=Path, required=True)
    c.add_argument("--root", type=Path, required=True)
    c.add_argument("--alerts", type=Path)
    c.add_argument("--approval-turn")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    if args.cmd == "snap":
        args.out.write_text(json.dumps(snapshot(args.root, args.alerts), indent=2, sort_keys=True), encoding="utf-8")
        print(f"wrote {args.out}")
        return 0
    if args.cmd == "compare":
        before = json.loads(args.before.read_text(encoding="utf-8"))
        return compare(before, snapshot(args.root, args.alerts), args.approval_turn)
    ap.error("pass --self-test, snap or compare")
    return 2


if __name__ == "__main__":
    sys.exit(main())
