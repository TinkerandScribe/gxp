#!/usr/bin/env bash
# Named verify for the Jev Choice Router experiment (opt-in; not part of root verify.sh).
# Soft spike: no live Jev / MCP / network.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$ROOT/../.." && pwd)"
cd "$REPO_ROOT"

# shellcheck source=../../scripts/lib/find-python.sh
source "$REPO_ROOT/scripts/lib/find-python.sh"

echo "=== jev-choice-router named verify ==="
echo "python: $PY"

export PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}"
# Flag off during verify so the Jev path stays unused.
unset CHOICE_ROUTER || true
export CHOICE_ROUTER=0

echo ""
echo "1. unit tests"
"$PY" -m unittest discover -s "$ROOT/tests" -v

echo ""
echo "2. guardrail: core/workflow.md unchanged vs main"
if git rev-parse --verify main >/dev/null 2>&1; then
  BASE_REF="main"
elif git rev-parse --verify origin/main >/dev/null 2>&1; then
  BASE_REF="origin/main"
else
  echo "  skip: no main ref"
  BASE_REF=""
fi
if [ -n "$BASE_REF" ]; then
  git diff --exit-code "$BASE_REF" -- core/workflow.md
  echo "  ok (empty diff vs $BASE_REF)"
  echo ""
  echo "3. guardrail: experiment files only"
  extra="$(git diff --name-only "$BASE_REF" | grep -v '^experiments/jev-choice-router/' || true)"
  if [ -n "$extra" ]; then
    echo "  FAIL: changes outside experiments/jev-choice-router/:"
    echo "$extra"
    exit 1
  fi
  echo "  ok"
fi

echo ""
echo "4. no Pilot B package import"
if grep -R --include='*.py' -nE '^(from|import) jev_pilot_b' "$ROOT"; then
  echo "  FAIL: jev_pilot_b import"
  exit 1
fi
echo "  ok"

echo ""
echo "5. cue-list policy_v1 / Pilot B hooks absent from cascade"
if grep -n 'policy_v1' "$ROOT/jev_choice_router/cascade.py"; then
  echo "  FAIL: cascade.py must not mention policy_v1"
  exit 1
fi
if grep -nE 'empty_artifact|incomplete_evidence|contradictory_markers|gate_g1' \
  "$ROOT/jev_choice_router/cascade.py" \
  "$ROOT/jev_choice_router/hooks.py" \
  "$ROOT/jev_choice_router/providers/rules.py"; then
  echo "  FAIL: Pilot B G1 hook names leaked into choice-router rules/cascade"
  exit 1
fi
echo "  ok"

echo ""
echo "6. no network / live Jev in package"
if grep -R --include='*.py' -nE 'urllib|urlopen|http\.client|socket\.create_connection' \
  "$ROOT/jev_choice_router"; then
  echo "  FAIL: network client in package"
  exit 1
fi
if grep -R --include='*.py' -nE 'CallDynamicTool|jev_classify\(' "$ROOT/jev_choice_router" "$ROOT/tests" "$ROOT/scripts"; then
  echo "  FAIL: live jev_classify invocation"
  exit 1
fi
echo "  ok (no live Jev)"

echo ""
echo "7. opt-in flag documented"
if ! grep -q 'CHOICE_ROUTER' "$ROOT/README.md" "$ROOT/.env.example"; then
  echo "  FAIL: CHOICE_ROUTER missing from README / .env.example"
  exit 1
fi
echo "  ok"

echo ""
echo "=== PASS: jev-choice-router tests + isolation guardrails ==="
