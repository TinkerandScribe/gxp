#!/usr/bin/env bash
# Prove the code-quality harness ranks reference > starter.
set -euo pipefail
cd "$(dirname "$0")/.."
SCORE=core/evals/golden/agent-code-quality/harness/score_trial.py
TASK=01-parse-kv
BASE=core/evals/golden/agent-code-quality/tasks/$TASK

PY=python3
command -v python3 >/dev/null 2>&1 || PY=python

"$PY" "$SCORE" --task "$TASK" --result "$BASE/starter" --out /tmp/gxp-cq-starter.json
"$PY" "$SCORE" --task "$TASK" --result "$BASE/reference" --out /tmp/gxp-cq-ref.json

"$PY" - <<'PY'
import json
s=json.load(open("/tmp/gxp-cq-starter.json",encoding="utf-8"))
r=json.load(open("/tmp/gxp-cq-ref.json",encoding="utf-8"))
print(f"starter correctness={s['correctness']} ({s['tests_passed']}/{s['tests_total']})")
print(f"reference correctness={r['correctness']} ({r['tests_passed']}/{r['tests_total']})")
assert r["correctness"] == 1.0, "reference must be perfect"
assert s["correctness"] < r["correctness"], "starter must score below reference"
assert r["no_test_tamper"] and s["no_test_tamper"]
print("SELFTEST OK: harness separates weak starter from full reference")
PY

"$PY" core/evals/golden/agent-code-quality/harness/compare_scores.py \
  --a /tmp/gxp-cq-starter.json --b /tmp/gxp-cq-ref.json \
  --label-a starter --label-b reference
