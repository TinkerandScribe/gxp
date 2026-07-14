#!/usr/bin/env python3
"""Score L2 tool-loop transcripts (agent_tool_log.jsonl).

Metrics (binary or rates; do NOT replace hidden correctness):

- phase0_hit: read under .ai/ (PROGRAM, rules, or failures) before first
  write to service/ product code
- tool_verify_ran: ran public unittest (or unittest discover tests_public)
- brief_written: wrote BRIEF.md
- handoff_written: wrote HANDOFF.md
- service_writes: count of writes under service/
- steps: number of log events

Usage (repo root):
  python core/evals/golden/agent-code-quality/harness/score_transcript.py \\
    --log path/to/agent_tool_log.jsonl
  python .../score_transcript.py --scan-trials  # all logs under trials/
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRIALS = ROOT / "trials"


def load_events(path: Path) -> list[dict]:
    events = []
    if not path.is_file():
        return events
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return events


def _action(ev: dict) -> dict:
    a = ev.get("action")
    return a if isinstance(a, dict) else {}


def _path(act: dict) -> str:
    # Do not use str.lstrip("./") — that strips any mix of dots/slashes
    # and turns ".ai/foo" into "ai/foo".
    p = str(act.get("path") or "").replace("\\", "/")
    while p.startswith("./"):
        p = p[2:]
    return p


def score_log(path: Path) -> dict:
    events = load_events(path)
    reads_ai = []
    first_service_write_step = None
    verify_steps = []
    brief = False
    handoff = False
    service_writes = 0
    preflight_public_green = False

    for ev in events:
        if ev.get("auto") == "public_green_preflight":
            preflight_public_green = bool(ev.get("green"))
        act = _action(ev)
        name = str(act.get("action") or "").lower()
        p = _path(act)
        step = ev.get("step")

        if name == "read" and (p.startswith(".ai/") or p == ".ai"):
            reads_ai.append(step)
        if name == "list" and (p == ".ai" or p.startswith(".ai")):
            reads_ai.append(step)

        if name == "write":
            if p == "BRIEF.md" or p.endswith("/BRIEF.md"):
                brief = True
            if p == "HANDOFF.md" or p.endswith("/HANDOFF.md"):
                handoff = True
            if p.startswith("service/"):
                service_writes += 1
                if first_service_write_step is None:
                    first_service_write_step = step

        if name == "run":
            cmd = str(act.get("cmd") or act.get("command") or "")
            obs = str(ev.get("obs_preview") or ev.get("obs") or "")
            if "unittest" in cmd or "tests_public" in cmd or (
                not cmd.strip() and "exit=" in obs
            ):
                verify_steps.append(step)
            # empty cmd uses public_verify in runner
            if not cmd.strip() and name == "run":
                verify_steps.append(step)

    phase0_hit = False
    if reads_ai:
        if first_service_write_step is None:
            phase0_hit = True  # read .ai, never wrote service
        else:
            # any .ai read strictly before first service write
            phase0_hit = any(
                (s is not None and first_service_write_step is not None and s < first_service_write_step)
                or (s is not None and first_service_write_step is None)
                for s in reads_ai
            )
            # also count .ai list/read at lower step numbers
            try:
                phase0_hit = min(s for s in reads_ai if s is not None) < first_service_write_step
            except ValueError:
                phase0_hit = False

    # public_green preflight with zero service writes still counts phase0 N/A
    if preflight_public_green and service_writes == 0:
        phase0_hit = False  # did not exercise Phase 0 fix path
        phase0_note = "skipped_preflight_green"
    else:
        phase0_note = None

    tool_verify_ran = len(verify_steps) > 0 or preflight_public_green

    return {
        "log": str(path),
        "steps": len(events),
        "phase0_hit": phase0_hit,
        "phase0_note": phase0_note,
        "tool_verify_ran": tool_verify_ran,
        "brief_written": brief,
        "handoff_written": handoff,
        "service_writes": service_writes,
        "verify_runs": len(set(verify_steps)),
        "ai_reads": len(reads_ai),
        "preflight_public_green": preflight_public_green,
    }


def scan_trials() -> list[dict]:
    rows = []
    if not TRIALS.is_dir():
        return rows
    for log in sorted(TRIALS.rglob("agent_tool_log.jsonl")):
        row = score_log(log)
        try:
            rel = log.relative_to(TRIALS)
            parts = rel.parts
            # trials/<trial>/results/<model>/<arm>/...
            trial = parts[0] if parts else ""
            model = parts[2] if len(parts) > 2 else ""
            arm = parts[3] if len(parts) > 3 else ""
            row["trial"] = trial
            row["model"] = model
            row["arm"] = arm
            row["rel"] = str(rel).replace("\\", "/")
        except ValueError:
            pass
        rows.append(row)
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description="Score L2 agent tool transcripts")
    ap.add_argument("--log", type=Path, default=None)
    ap.add_argument("--scan-trials", action="store_true")
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    if args.scan_trials:
        rows = scan_trials()
    elif args.log:
        rows = [score_log(args.log)]
    else:
        print("need --log or --scan-trials", file=sys.stderr)
        return 2

    text = json.dumps(rows, indent=2)
    print(text)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
