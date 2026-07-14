#!/usr/bin/env bash
# Score all trials under an operator-blind BASE directory.
# Usage (from gxp repo root):
#   bash core/evals/golden/agent-code-quality/scripts/score-operator-blind.sh \
#     core/evals/golden/agent-code-quality/trials/YYYY-MM-DD-operator-blind
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"
cd "$ROOT"

# shellcheck source=../../../../scripts/lib/find-python.sh
if [[ -f scripts/lib/find-python.sh ]]; then
  source scripts/lib/find-python.sh
else
  PY=python3
  "$PY" -c "" >/dev/null 2>&1 || PY=python
fi

BASE="${1:-}"
if [[ -z "$BASE" || ! -d "$BASE/results" ]]; then
  echo "Usage: $0 <path-to-*-operator-blind>" >&2
  echo "  (directory must contain results/)" >&2
  exit 2
fi

SCORE=core/evals/golden/agent-code-quality/harness/score_trial.py
mkdir -p "$BASE/scores"

shopt -s nullglob
count=0
for result_dir in "$BASE"/results/*/*/*; do
  [[ -d "$result_dir" ]] || continue
  # .../results/<tool>/<arm>/<task>
  task="$(basename "$result_dir")"
  arm="$(basename "$(dirname "$result_dir")")"
  tool="$(basename "$(dirname "$(dirname "$result_dir")")")"
  out="$BASE/scores/${tool}-${arm}-${task}.json"
  echo "Scoring $tool $arm $task ..."
  if [[ "$arm" == "gxp" && -f "$result_dir/BRIEF.md" ]]; then
    "$PY" "$SCORE" --task "$task" --result "$result_dir" --brief "$result_dir/BRIEF.md" --out "$out"
  else
    "$PY" "$SCORE" --task "$task" --result "$result_dir" --out "$out"
  fi
  count=$((count + 1))
done

echo "Scored $count trial(s) into $BASE/scores/"
echo "Next: write CAMPAIGN_REPORT.md and CONTAMINATION.md from those JSONs (see OPERATOR_RUNBOOK.md Phase C)."
