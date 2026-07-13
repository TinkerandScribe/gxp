#!/usr/bin/env bash
# Prove the code-quality harness ranks reference > starter.
set -euo pipefail
cd "$(dirname "$0")/.."
SCORE=core/evals/golden/agent-code-quality/harness/score_trial.py
TASK=01-parse-kv
BASE=core/evals/golden/agent-code-quality/tasks/$TASK

PY=python3
command -v python3 >/dev/null 2>&1 || PY=python

for TASK in 01-parse-kv 02-slugify 03-merge-intervals; do
  BASE="core/evals/golden/agent-code-quality/tasks/$TASK"
  echo "=== selftest $TASK ==="
  "$PY" "$SCORE" --task "$TASK" --result "$BASE/starter" --out "/tmp/gxp-cq-starter-$TASK.json"
  "$PY" "$SCORE" --task "$TASK" --result "$BASE/reference" --out "/tmp/gxp-cq-ref-$TASK.json"
  "$PY" - "$TASK" <<'PY'
import json, sys
task = sys.argv[1]
s=json.load(open(f"/tmp/gxp-cq-starter-{task}.json",encoding="utf-8"))
r=json.load(open(f"/tmp/gxp-cq-ref-{task}.json",encoding="utf-8"))
print(f"  starter={s['correctness']}  reference={r['correctness']}")
assert r["correctness"] == 1.0, f"{task}: reference must be perfect"
assert s["correctness"] < r["correctness"], f"{task}: starter must score below reference"
print(f"  OK {task}")
PY
done
echo "SELFTEST OK: all tasks separate starter from reference"
