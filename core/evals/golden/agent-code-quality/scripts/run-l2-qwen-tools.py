#!/usr/bin/env python3
"""Minimal tool-using Ollama loop for L2 task 09 (control or gxp).

Tools: list, read, write, run, done.
Usage (repo root):
  python .../run-l2-qwen-tools.py --arm control --workspace path/to/ws
  python .../run-l2-qwen-tools.py --arm gxp --workspace path/to/ws
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

MODEL = os.environ.get("GXP_QWEN_MODEL", "qwen3.6:27b")
URL = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434").rstrip("/") + "/api/chat"
MAX_STEPS = int(os.environ.get("GXP_L2_MAX_STEPS", "12"))
ROOT = Path(__file__).resolve().parents[5]
AQ = ROOT / "core/evals/golden/agent-code-quality"
DEFAULT_TASK = "09-rate-limit-service"


def chat(messages: list[dict]) -> str:
    payload = {
        "model": MODEL,
        "stream": False,
        "think": False,
        "options": {"temperature": 0.15, "num_predict": 4000},
        "messages": messages,
    }
    req = urllib.request.Request(
        URL,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=900) as resp:
        data = json.loads(resp.read().decode())
    msg = data.get("message") or {}
    content = msg.get("content") or ""
    if not content.strip():
        content = msg.get("thinking") or ""
    return content


def parse_action(text: str) -> dict | None:
    # Prefer fenced json
    m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.S)
    blob = m.group(1) if m else None
    if not blob:
        m2 = re.search(r"(\{[^{}]*\"action\"[^{}]*\})", text, re.S)
        blob = m2.group(1) if m2 else None
    if not blob:
        # multi-line json object
        m3 = re.search(r"\{[^{}]*\"action\"[\s\S]*\}", text)
        blob = m3.group(0) if m3 else None
    if not blob:
        return None
    try:
        return json.loads(blob)
    except json.JSONDecodeError:
        # try fix trailing commas
        try:
            return json.loads(re.sub(r",\s*}", "}", blob))
        except json.JSONDecodeError:
            return None


def safe_rel(ws: Path, rel: str) -> Path | None:
    rel = rel.replace("\\", "/").lstrip("/")
    if ".." in Path(rel).parts:
        return None
    p = (ws / rel).resolve()
    try:
        p.relative_to(ws.resolve())
    except ValueError:
        return None
    return p


def public_verify(ws: Path) -> tuple[bool, str]:
    """Run weak public tests. Returns (green, tool-style output)."""
    cmd = f"{sys.executable} -m unittest discover -s tests_public -v"
    try:
        r = subprocess.run(
            cmd,
            shell=True,
            cwd=str(ws),
            capture_output=True,
            text=True,
            timeout=60,
        )
        out = (r.stdout or "") + (r.stderr or "")
        return r.returncode == 0, f"exit={r.returncode}\n{out[:8000]}"
    except Exception as e:
        return False, f"ERROR: {e!r}"


def run_tool(ws: Path, action: dict, *, arm: str = "control") -> str:
    act = (action.get("action") or "").lower().strip()
    if act == "list":
        rel = action.get("path") or "."
        p = safe_rel(ws, rel)
        if not p or not p.exists():
            return f"ERROR: bad path {rel}"
        lines = []
        for root, dirs, files in os.walk(p):
            dirs[:] = [d for d in dirs if d != "__pycache__"]
            for f in files:
                if f.endswith(".pyc"):
                    continue
                fp = Path(root) / f
                lines.append(str(fp.relative_to(ws)).replace("\\", "/"))
        return "\n".join(sorted(lines)[:200]) or "(empty)"
    if act == "read":
        p = safe_rel(ws, action.get("path") or "")
        if not p or not p.is_file():
            return "ERROR: file not found"
        text = p.read_text(encoding="utf-8", errors="replace")
        return text[:12000]
    if act == "write":
        # public_green: never rewrite when public suite is already green (starter trap)
        if arm == "public_green":
            green, _ = public_verify(ws)
            if green:
                return (
                    "ERROR: public_green arm forbids writes while public tests pass. "
                    'Use {"action":"done"} now.'
                )
        p = safe_rel(ws, action.get("path") or "")
        content = action.get("content")
        if p is None or content is None:
            return "ERROR: need path and content"
        if "hidden_tests" in p.parts:
            return "ERROR: cannot write hidden_tests"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(str(content), encoding="utf-8")
        return f"OK wrote {p.relative_to(ws)} ({len(str(content))} chars)"
    if act == "run":
        cmd = action.get("cmd") or action.get("command") or ""
        if not cmd.strip():
            # default public verify
            green, out = public_verify(ws)
            return out
        if "unittest" not in cmd and "python" not in cmd:
            return "ERROR: only python/unittest commands allowed"
        try:
            r = subprocess.run(
                cmd,
                shell=True,
                cwd=str(ws),
                capture_output=True,
                text=True,
                timeout=60,
            )
            out = (r.stdout or "") + (r.stderr or "")
            return f"exit={r.returncode}\n{out[:8000]}"
        except Exception as e:
            return f"ERROR: {e!r}"
    if act == "done":
        return "DONE"
    return f"ERROR: unknown action {act}"


def system_prompt(arm: str, task_prompt: str) -> str:
    task = task_prompt
    base = f"""You fix a Python package in a workspace using tools.
Reply each turn with ONE JSON object only (optional ```json fence):
{{"action":"list"|"read"|"write"|"run"|"done", "path":"...", "content":"...", "cmd":"..."}}

Tools:
- list: path relative (default .)
- read: path
- write: path + content (full file)
- run: cmd string, cwd=workspace (prefer: python -m unittest discover -s tests_public -v)
- done: when finished

Rules: stdlib only; no hidden_tests; fix service/ bugs from the task.

TASK:
{task}
"""
    if arm == "gxp":
        base += """
GXP mode:
1) First list and read .ai/PROGRAM.md, rules, failures.
2) Write BRIEF.md with goal, 4-8 binary criteria, out of scope, verification.
3) Fix code against prompt + failure notes; public tests alone are NOT enough.
4) Run public tests; re-check criteria (fail-closed config, isolation, window).
5) Write HANDOFF.md; then action done.
"""
    elif arm == "public_green":
        base += """
PUBLIC-GREEN control mode (strict):
1) Run: python -m unittest discover -s tests_public -v
2) If exit=0, IMMEDIATELY action done. Do not edit service/ further.
3) Only edit if public tests fail; stop as soon as they pass again.
4) Do not invent edge-case tests. Do not rewrite "for quality."
"""
    else:
        base += """
Control mode: fix the package with tools. No formal brief required.
Run public tests before done.
"""
    return base


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--arm",
        choices=["control", "gxp", "public_green"],
        required=True,
    )
    ap.add_argument("--workspace", type=Path, required=True)
    ap.add_argument(
        "--task",
        default=DEFAULT_TASK,
        help="task id under agent-code-quality/tasks (for prompt.md)",
    )
    ap.add_argument(
        "--prompt-file",
        default="",
        help="override prompt path (e.g. tasks/10-.../prompt.short.md)",
    )
    args = ap.parse_args()
    ws = args.workspace.resolve()
    if not ws.is_dir():
        print("bad workspace", ws)
        return 2
    if args.prompt_file.strip():
        prompt_path = Path(args.prompt_file)
        if not prompt_path.is_file():
            prompt_path = ROOT / args.prompt_file
        if not prompt_path.is_file():
            prompt_path = AQ / args.prompt_file
    else:
        prompt_path = AQ / "tasks" / args.task / "prompt.md"
    if not prompt_path.is_file():
        print("missing task prompt", prompt_path)
        return 2
    task_prompt = prompt_path.read_text(encoding="utf-8")

    if args.arm == "public_green":
        user0 = (
            f"Workspace ready at {ws.name}. "
            "Run public unittest first. If green, done immediately."
        )
    elif args.arm == "gxp":
        user0 = (
            f"Workspace ready at {ws.name}. "
            "Start Phase 0: list and read .ai/, then BRIEF, then fix fully."
        )
    else:
        user0 = (
            f"Workspace is ready at {ws.name}. Start by listing files, then fix the service."
        )

    log_path = ws / "agent_tool_log.jsonl"
    if log_path.exists():
        log_path.unlink()

    # public_green preflight: if weak public suite already green, stop with zero edits
    if args.arm == "public_green":
        green, out = public_verify(ws)
        with log_path.open("a", encoding="utf-8") as f:
            f.write(
                json.dumps(
                    {
                        "step": 0,
                        "auto": "public_green_preflight",
                        "green": green,
                        "obs_preview": out[:500],
                    }
                )
                + "\n"
            )
        if green:
            (ws / "ARM_NOTE.md").write_text(
                "public_green: preflight public verify exit=0; zero writes enforced\n",
                encoding="utf-8",
            )
            print("  PREFLIGHT AUTO-DONE public_green (already green)", flush=True)
            return 0

    messages = [
        {"role": "system", "content": system_prompt(args.arm, task_prompt)},
        {"role": "user", "content": user0},
    ]

    for step in range(1, MAX_STEPS + 1):
        print(f"[{args.arm} step {step}] calling {MODEL}...", flush=True)
        try:
            raw = chat(messages)
        except Exception as e:
            print("chat fail", e)
            (ws / "ERROR.txt").write_text(repr(e), encoding="utf-8")
            return 1
        (ws / "raw_last_model.md").write_text(raw, encoding="utf-8")
        action = parse_action(raw)
        if not action:
            obs = "ERROR: could not parse JSON action. Reply with only one JSON action object."
            print("  parse fail", flush=True)
        else:
            print(f"  action={action.get('action')} path={action.get('path')}", flush=True)
            obs = run_tool(ws, action, arm=args.arm)
            if (action.get("action") or "").lower() == "done":
                with log_path.open("a", encoding="utf-8") as f:
                    f.write(json.dumps({"step": step, "action": action, "obs": obs[:500]}) + "\n")
                print("  DONE", flush=True)
                return 0
            # public_green: hard stop as soon as public verify is green
            if args.arm == "public_green" and obs.startswith("exit=0"):
                with log_path.open("a", encoding="utf-8") as f:
                    f.write(
                        json.dumps(
                            {
                                "step": step,
                                "action": action,
                                "obs_preview": obs[:500],
                                "auto": "public_green_stop_on_exit_0",
                            }
                        )
                        + "\n"
                    )
                print("  AUTO-DONE public_green (public verify exit=0)", flush=True)
                (ws / "ARM_NOTE.md").write_text(
                    "public_green: auto-stopped after public verify exit=0\n",
                    encoding="utf-8",
                )
                return 0
        with log_path.open("a", encoding="utf-8") as f:
            f.write(
                json.dumps(
                    {
                        "step": step,
                        "raw_preview": raw[:500],
                        "action": action,
                        "obs_preview": obs[:1000],
                    }
                )
                + "\n"
            )
        messages.append({"role": "assistant", "content": raw})
        follow = f"TOOL_RESULT:\n{obs}\n\nNext: one JSON action only."
        if args.arm == "public_green" and obs.startswith("exit=0"):
            follow += "\nPublic tests GREEN. You MUST reply {\"action\":\"done\"} now."
        if args.arm == "public_green" and obs.startswith("ERROR: public_green"):
            follow += "\nWrites blocked. Reply {\"action\":\"done\"} now."
        messages.append({"role": "user", "content": follow})

    print("max steps", flush=True)
    (ws / "ERROR.txt").write_text("max steps without done\n", encoding="utf-8")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
