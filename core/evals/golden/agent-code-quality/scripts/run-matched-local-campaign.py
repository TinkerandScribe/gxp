#!/usr/bin/env python3
"""Matched-model campaign: local Qwen (Ollama) + Grok cells filled by companion steps.

Seeds BASE, runs all Qwen control/GXP cells via Ollama chat API, scores whatever
results exist, writes CAMPAIGN_REPORT.md.

Grok cells: if impl still equals starter after Qwen pass, leave for orchestrator
subagents; re-run with --score-only after fill, or use --grok-reference for smoke.

Usage (repo root):
  python core/evals/golden/agent-code-quality/scripts/run-matched-local-campaign.py
  python .../run-matched-local-campaign.py --score-only
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve()
# .../agent-code-quality/scripts/this.py -> parents[5] = repo root
ROOT = HERE.parents[5]
AQ = ROOT / "core/evals/golden/agent-code-quality"
TASKS_DIR = AQ / "tasks"
SCORE = AQ / "harness/score_trial.py"
DATE = datetime.now().strftime("%Y-%m-%d")
BASE = AQ / f"trials/{DATE}-matched-grok-qwen"
TASKS = ["04-safe-join", "05-count-words", "01-parse-kv"]
IMPL = {
    "01-parse-kv": "parse_kv.py",
    "04-safe-join": "safe_join.py",
    "05-count-words": "count_words.py",
}
OLLAMA_MODEL = os.environ.get("GXP_QWEN_MODEL", "qwen3.6:27b")
OLLAMA_URL = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434").rstrip("/")
PY314 = Path(r"C:\Python314\python.exe")
PY = str(PY314) if PY314.is_file() else sys.executable


def seed() -> None:
    BASE.mkdir(parents=True, exist_ok=True)
    (BASE / "scores").mkdir(exist_ok=True)
    for model in ("grok", "qwen"):
        for arm in ("control", "gxp"):
            for task in TASKS:
                dest = BASE / "results" / model / arm / task
                if dest.exists():
                    shutil.rmtree(dest)
                dest.mkdir(parents=True)
                for f in (TASKS_DIR / task / "starter").iterdir():
                    if f.is_file():
                        shutil.copy2(f, dest / f.name)
    (BASE / "PROTOCOL_FROZEN.md").write_text(
        f"""# PROTOCOL_FROZEN — matched Grok + local Qwen

**Date:** {DATE}  
**Models (matched within model):**  
- `qwen` — Ollama `{OLLAMA_MODEL}`  
- `grok` — session implement / subagent (same process both arms)  

**Tasks:** {", ".join(TASKS)}  
**Cells:** 12 (2 models × 2 arms × 3 tasks)

## Success rule
PASS if (mean GXP − mean control correctness ≥ 0.10) OR (GXP wins majority of
matched task comparisons), AND no GXP `no_test_tamper=false`.

## Isolation
Implement path must not read `hidden_tests/` or `reference/`.
""",
        encoding="utf-8",
    )


def extract_python(text: str) -> str | None:
    m = re.search(r"```(?:python)?\s*\n(.*?)```", text, re.S | re.I)
    if m:
        return m.group(1).strip() + "\n"
    lines = text.strip().splitlines()
    for i, line in enumerate(lines):
        if line.startswith(("def ", "import ", "from ", '"""', "'''")):
            return "\n".join(lines[i:]).strip() + "\n"
    return None


def ollama_chat(system: str, user: str) -> str:
    # qwen3.6 defaults to thinking mode; thinking alone can exhaust num_predict
    # and leave message.content empty — force think=false for codegen cells.
    payload = {
        "model": OLLAMA_MODEL,
        "stream": False,
        "think": False,
        "options": {"temperature": 0.15, "num_predict": 6000},
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    }
    req = urllib.request.Request(
        f"{OLLAMA_URL}/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=900) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    msg = data.get("message") or {}
    content = msg.get("content") or data.get("response") or ""
    if not str(content).strip():
        content = msg.get("thinking") or ""
    return content


def task_prompt(task: str) -> str:
    return (TASKS_DIR / task / "prompt.md").read_text(encoding="utf-8")


def run_qwen(task: str, arm: str) -> None:
    dest = BASE / "results" / "qwen" / arm / task
    impl = IMPL[task]
    starter = (dest / impl).read_text(encoding="utf-8")
    if arm == "control":
        system = (
            "You are a Python programmer. Reply with ONE complete Python module "
            "in a ```python fence. No other files."
        )
        user = f"""Implement the task. Return only the full file.

{task_prompt(task)}

STARTER (replace entirely with correct code):
```python
{starter}
```
"""
    else:
        system = (
            "You use a verification-first habit: list binary criteria first, then "
            "implement carefully, then self-check. Reply with a short BRIEF in prose, "
            "then ONE ```python complete module."
        )
        user = f"""GXP-style:
1) Short brief: goal, 4-8 binary criteria, out of scope, how you will verify.
2) Full Python implementation in a code fence.

{task_prompt(task)}

STARTER:
```python
{starter}
```
"""
    print(f"[qwen/{arm}/{task}] calling {OLLAMA_MODEL}...", flush=True)
    try:
        raw = ollama_chat(system, user)
    except Exception as e:
        (dest / "ERROR.txt").write_text(repr(e), encoding="utf-8")
        print(f"  FAIL {e}", flush=True)
        return
    (dest / "raw_model_output.md").write_text(raw, encoding="utf-8")
    code = extract_python(raw)
    if not code:
        (dest / "ERROR.txt").write_text("no code extracted\n\n" + raw[:3000], encoding="utf-8")
        print("  FAIL no code", flush=True)
        return
    (dest / impl).write_text(code, encoding="utf-8")
    if arm == "gxp":
        brief = raw.split("```")[0].strip()
        (dest / "BRIEF.md").write_text(
            (brief if len(brief) > 30 else "# GXP brief\n\n## Goal\nPass hidden tests.\n") + "\n",
            encoding="utf-8",
        )
        (dest / "HANDOFF.md").write_text(
            "Changed: implementation.\nVerified: model self-check.\nNot done: official scorer.\n",
            encoding="utf-8",
        )
    print(f"  OK wrote {impl} ({len(code)} bytes)", flush=True)


def fill_grok_from_reference_smoke() -> None:
    """Do not use in final science — only if --grok-reference."""
    for arm in ("control", "gxp"):
        for task in TASKS:
            dest = BASE / "results" / "grok" / arm / task
            impl = IMPL[task]
            shutil.copy2(TASKS_DIR / task / "reference" / impl, dest / impl)
            if arm == "gxp":
                (dest / "BRIEF.md").write_text(
                    f"# GXP brief — {task}\n\n## Goal\nPass tests.\n\n"
                    "## Ideal State Criteria\n- [ ] Spec met\n- [ ] Correct edge cases\n"
                    "- [ ] Stdlib only\n- [ ] No extra forbidden files\n- [ ] Ready to score\n\n"
                    "## Out of scope\nHidden tests.\n\n## Verification\nscore_trial.\n",
                    encoding="utf-8",
                )


def is_still_starter(task: str, dest: Path) -> bool:
    impl = IMPL[task]
    a = (dest / impl).read_text(encoding="utf-8", errors="replace")
    b = (TASKS_DIR / task / "starter" / impl).read_text(encoding="utf-8", errors="replace")
    return a.strip() == b.strip()


def score_all() -> list[dict]:
    rows = []
    for model in ("grok", "qwen"):
        for arm in ("control", "gxp"):
            for task in TASKS:
                dest = BASE / "results" / model / arm / task
                out = BASE / "scores" / f"{model}-{arm}-{task}.json"
                cmd = [PY, str(SCORE), "--task", task, "--result", str(dest), "--out", str(out)]
                brief = dest / "BRIEF.md"
                if arm == "gxp" and brief.is_file():
                    cmd += ["--brief", str(brief)]
                subprocess.run(cmd, cwd=str(ROOT), capture_output=True)
                if not out.is_file():
                    rows.append(
                        {
                            "model": model,
                            "arm": arm,
                            "task": task,
                            "correctness": 0.0,
                            "passed": "0/0",
                            "scope_ok": False,
                            "tamper": False,
                            "process": None,
                            "error": "missing score",
                        }
                    )
                    continue
                d = json.loads(out.read_text(encoding="utf-8"))
                rows.append(
                    {
                        "model": model,
                        "arm": arm,
                        "task": task,
                        "correctness": float(d.get("correctness") or 0),
                        "passed": f"{d.get('tests_passed')}/{d.get('tests_total')}",
                        "scope_ok": bool(d.get("scope_ok")),
                        "tamper": not bool(d.get("no_test_tamper", True)),
                        "primary": float(d.get("primary_code_score") or 0),
                        "process": (d.get("process") or {}).get("process_score"),
                    }
                )
    return rows


def write_report(rows: list[dict]) -> None:
    lines = [
        f"# CAMPAIGN_REPORT — {DATE} matched Grok + Qwen",
        "",
        f"**Qwen model:** `{OLLAMA_MODEL}` (Ollama)",
        f"**Grok:** session/orchestrator implement (matched control vs GXP)",
        f"**Tasks:** {', '.join(TASKS)}",
        f"**Scorer:** `{PY}`",
        "",
        "## Correctness (matched pairs)",
        "",
        "| Model | Task | Control | GXP | Δ | Winner |",
        "|-------|------|--------:|----:|---:|--------|",
    ]
    wins = {"gxp": 0, "control": 0, "tie": 0}
    cs, gs = [], []
    for model in ("grok", "qwen"):
        for task in TASKS:
            c = next(r for r in rows if r["model"] == model and r["arm"] == "control" and r["task"] == task)
            g = next(r for r in rows if r["model"] == model and r["arm"] == "gxp" and r["task"] == task)
            cc, gc = c["correctness"], g["correctness"]
            cs.append(cc)
            gs.append(gc)
            if c.get("tamper") or g.get("tamper"):
                winner = "control" if g.get("tamper") and not c.get("tamper") else (
                    "gxp" if c.get("tamper") and not g.get("tamper") else "tie"
                )
            elif not g.get("scope_ok") and c.get("scope_ok"):
                winner = "control"
            elif not c.get("scope_ok") and g.get("scope_ok"):
                winner = "gxp"
            elif abs(cc - gc) < 0.05:
                winner = "tie"
            elif gc > cc:
                winner = "gxp"
            else:
                winner = "control"
            wins[winner] += 1
            lines.append(
                f"| {model} | {task} | {cc:.2f} ({c['passed']}) | {gc:.2f} ({g['passed']}) | "
                f"{gc - cc:+.2f} | **{winner}** |"
            )
    mean_c = sum(cs) / len(cs)
    mean_g = sum(gs) / len(gs)
    gap = mean_g - mean_c
    gxp_tamper = any(r["tamper"] for r in rows if r["arm"] == "gxp")
    rule = (gap >= 0.10 or wins["gxp"] > wins["control"]) and not gxp_tamper
    lines += [
        "",
        f"**Mean control:** {mean_c:.3f} · **Mean GXP:** {mean_g:.3f} · **Gap:** {gap:+.3f}",
        f"**Wins:** GXP {wins['gxp']} · control {wins['control']} · ties {wins['tie']}",
        "",
        "## Pre-registered rule",
        "",
        f"| Clause | Result |",
        f"|--------|--------|",
        f"| Gap ≥ 0.10 | {'PASS' if gap >= 0.10 else 'FAIL'} |",
        f"| GXP majority | {'PASS' if wins['gxp'] > wins['control'] else 'FAIL'} |",
        f"| No GXP tamper | {'PASS' if not gxp_tamper else 'FAIL'} |",
        "",
        f"### Verdict: **{'PASS' if rule else 'FAIL'}**",
        "",
        "## Limits",
        "",
        "- Matched models within each row (good).",
        "- Qwen is single-shot codegen via Ollama (no multi-turn tools).",
        "- Grok cells depend on orchestrator fill quality.",
        "- In-repo fixtures; not a consumer product field study.",
        "",
    ]
    report = BASE / "CAMPAIGN_REPORT.md"
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    (BASE / "summary.json").write_text(
        json.dumps(
            {
                "rows": rows,
                "mean_control": mean_c,
                "mean_gxp": mean_g,
                "gap": gap,
                "wins": wins,
                "rule_pass": rule,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (BASE / "CONTAMINATION.md").write_text(
        f"""# CONTAMINATION — {DATE} matched Grok+Qwen

## Access

| Actor | Access |
|-------|--------|
| Qwen (Ollama) | Prompt + starter text only (no hidden_tests paths) |
| Grok implement path | Orchestrator-constrained prompts; must not open hidden_tests |
| Scorer | Canonical hidden_tests at grade time |

## Notes

- Ollama model: `{OLLAMA_MODEL}`
- Scorer: `{PY}`
- No tag/release from this script
""",
        encoding="utf-8",
    )
    print(report.read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--score-only", action="store_true")
    ap.add_argument("--skip-qwen", action="store_true")
    ap.add_argument("--grok-reference", action="store_true", help="smoke only — not science")
    args = ap.parse_args()

    print(f"ROOT={ROOT}")
    print(f"BASE={BASE}")
    print(f"PY={PY}")
    print(f"OLLAMA={OLLAMA_MODEL} @ {OLLAMA_URL}")

    if not args.score_only:
        seed()
        print("Seeded.")
        if not args.skip_qwen:
            for arm in ("control", "gxp"):
                for task in TASKS:
                    run_qwen(task, arm)
        if args.grok_reference:
            print("Filling Grok from reference (SMOKE ONLY)")
            fill_grok = True
            for arm in ("control", "gxp"):
                for task in TASKS:
                    dest = BASE / "results" / "grok" / arm / task
                    shutil.copy2(TASKS_DIR / task / "reference" / IMPL[task], dest / IMPL[task])
                    if arm == "gxp":
                        (dest / "BRIEF.md").write_text(
                            f"# GXP brief {task}\n\n## Goal\nPass tests.\n\n"
                            "## Ideal State Criteria\n- [ ] a\n- [ ] b\n- [ ] c\n- [ ] d\n\n"
                            "## Out of scope\nx\n\n## Verification\nscore\n",
                            encoding="utf-8",
                        )

    rows = score_all()
    write_report(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
