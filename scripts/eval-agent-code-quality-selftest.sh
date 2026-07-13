#!/usr/bin/env bash
# Prove the code-quality harness ranks reference > starter.
set -euo pipefail
cd "$(dirname "$0")/.."
SCORE=core/evals/golden/agent-code-quality/harness/score_trial.py
TASK=01-parse-kv
BASE=core/evals/golden/agent-code-quality/tasks/$TASK

# Probe executability, not just existence — on Windows, `command -v python3`
# matches the Microsoft Store stub, which cannot run (see cowork check-core fix).
PY=python3
"$PY" -c "" >/dev/null 2>&1 || PY=python

# One temp dir, passed to python via argv — hardcoding /tmp inside the heredoc
# breaks on Git Bash/Windows, where bash converts /tmp in *arguments* to the
# Windows temp path but python sees the literal string unconverted.
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

for TASK in 01-parse-kv 02-slugify 03-merge-intervals; do
  BASE="core/evals/golden/agent-code-quality/tasks/$TASK"
  echo "=== selftest $TASK ==="
  "$PY" "$SCORE" --task "$TASK" --result "$BASE/starter" --out "$TMP_DIR/starter-$TASK.json"
  "$PY" "$SCORE" --task "$TASK" --result "$BASE/reference" --out "$TMP_DIR/ref-$TASK.json"
  "$PY" - "$TASK" "$TMP_DIR" <<'PY'
import json, os, sys
task, tmp = sys.argv[1], sys.argv[2]
s=json.load(open(os.path.join(tmp, f"starter-{task}.json"),encoding="utf-8"))
r=json.load(open(os.path.join(tmp, f"ref-{task}.json"),encoding="utf-8"))
print(f"  starter={s['correctness']}  reference={r['correctness']}")
assert r["correctness"] == 1.0, f"{task}: reference must be perfect"
assert s["correctness"] < r["correctness"], f"{task}: starter must score below reference"
print(f"  OK {task}")
PY
done
echo "SELFTEST OK: all tasks separate starter from reference"
