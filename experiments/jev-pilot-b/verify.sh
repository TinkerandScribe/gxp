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
echo "4. named path incomplete_evidence in README + this script"
if ! grep -q 'incomplete_evidence' "$ROOT/README.md"; then
  echo "  FAIL: README missing incomplete_evidence path name"
  exit 1
fi
if ! grep -q 'incomplete_evidence' "$ROOT/verify.sh"; then
  echo "  FAIL: verify.sh missing incomplete_evidence path name"
  exit 1
fi
echo "  ok (incomplete_evidence)"

echo ""
echo "5. cue-list policy_v1 stays UNSHIPPED (not in default cascade)"
policy_hits="$(grep -n 'policy_v1' "$ROOT/jev_pilot_b/cascade.py" "$ROOT/jev_pilot_b/providers/rules.py" "$ROOT/jev_pilot_b/hooks.py" || true)"
policy_bad="$(printf '%s\n' "$policy_hits" | grep -v UNSHIPPED || true)"
if [ -n "$policy_bad" ]; then
  echo "  FAIL: policy_v1 referenced outside an UNSHIPPED note"
  echo "$policy_bad"
  exit 1
fi
if grep -q 'policy_v1' "$ROOT/jev_pilot_b/cascade.py"; then
  echo "  FAIL: cascade.py must not mention policy_v1"
  exit 1
fi
if ! grep -q 'UNSHIPPED' "$ROOT/README.md"; then
  echo "  FAIL: README must mark policy_v1 UNSHIPPED"
  exit 1
fi
echo "  ok (policy_v1 UNSHIPPED)"

echo ""
echo "6. spike B label audit covers the eight holdout ids"
AUDIT="$ROOT/docs/spike_b_label_audit.md"
if [ ! -f "$AUDIT" ]; then
  echo "  FAIL: missing $AUDIT"
  exit 1
fi
for id in 042 048 083 104 105 106 107 108; do
  if ! grep -q "$id" "$AUDIT"; then
    echo "  FAIL: audit missing id $id"
    exit 1
  fi
done
echo "  ok (×8 ids in docs/spike_b_label_audit.md)"

echo ""
echo "=== PASS: jev-pilot-b tests + isolation guardrails ==="
