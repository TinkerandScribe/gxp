#!/usr/bin/env bash
# Named verify for the Jev Pilot B experiment (opt-in; not part of root verify.sh).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$ROOT/../.." && pwd)"
cd "$REPO_ROOT"

# shellcheck source=../../scripts/lib/find-python.sh
source "$REPO_ROOT/scripts/lib/find-python.sh"

echo "=== jev-pilot-b named verify ==="
echo "python: $PY"

export PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}"
echo ""
echo "1. unit tests"
"$PY" -m unittest discover -s "$ROOT/tests" -v

echo ""
echo "2. guardrail: core/workflow.md and adapters/grok-bot unchanged vs main"
if git rev-parse --verify main >/dev/null 2>&1; then
  BASE_REF="main"
elif git rev-parse --verify origin/main >/dev/null 2>&1; then
  BASE_REF="origin/main"
else
  echo "  skip: no main ref"
  BASE_REF=""
fi
if [ -n "$BASE_REF" ]; then
  git diff --exit-code "$BASE_REF" -- core/workflow.md adapters/grok-bot
  echo "  ok (empty diff vs $BASE_REF)"
  echo ""
  echo "3. guardrail: experiment files only"
  extra="$(git diff --name-only "$BASE_REF" | grep -v '^experiments/jev-pilot-b/' || true)"
  if [ -n "$extra" ]; then
    echo "  FAIL: changes outside experiments/jev-pilot-b/:"
    echo "$extra"
    exit 1
  fi
  echo "  ok"
fi

echo ""
echo "=== PASS: jev-pilot-b tests + isolation guardrails ==="
