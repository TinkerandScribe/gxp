#!/usr/bin/env bash
# Seed workspaces for an operator-led blind campaign (Claude + Cursor).
# Usage (from gxp repo root):
#   bash core/evals/golden/agent-code-quality/scripts/seed-operator-blind.sh
#   bash .../seed-operator-blind.sh 2026-07-14   # optional date stamp
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"
cd "$ROOT"

DATE="${1:-$(date +%Y-%m-%d)}"
AQ="core/evals/golden/agent-code-quality"
BASE="$AQ/trials/${DATE}-operator-blind"
TOOLS=(claude cursor)
ARMS=(control gxp)
TASKS=(01-parse-kv 04-safe-join 05-count-words)

mkdir -p "$BASE/scores"

for tool in "${TOOLS[@]}"; do
  for arm in "${ARMS[@]}"; do
    for task in "${TASKS[@]}"; do
      dest="$BASE/results/$tool/$arm/$task"
      mkdir -p "$dest"
      # starter only — never copy reference or hidden_tests
      cp -R "$AQ/tasks/$task/starter/." "$dest/"
    done
  done
done

PROTO="$BASE/PROTOCOL_FROZEN.md"
if [[ ! -f "$PROTO" ]]; then
  cat > "$PROTO" <<EOF
# PROTOCOL_FROZEN — operator-blind campaign

**Date stamp:** $DATE  
**Created:** $(date -Iseconds 2>/dev/null || date)  
**Harness:** core/evals/golden/agent-code-quality  
**Entrypoint:** OPERATOR_RUNBOOK.md  

## Models / tools (fill before implement)

| Label | Product / model (fill in) |
|-------|---------------------------|
| claude | e.g. Claude Code / Sonnet … |
| cursor | e.g. Cursor Auto / Composer … |

## Matrix

- Tools: claude, cursor  
- Arms: control, gxp  
- Tasks: 01-parse-kv, 04-safe-join, 05-count-words  
- Sessions: 12  

## Budget (per trial)

- Wall clock: 15 minutes **or**  
- Tool turns: ~40  

## Pre-registered success rule

PASS if (GXP mean correctness − control mean ≥ 0.10)  
OR (GXP wins a majority of task-level comparisons among non-disqualified scope_ok trials)  
AND no GXP trial fails tamper / scope_ok for win eligibility.  
Otherwise FAIL. No marketing claim on FAIL or on all-1.0 ceiling.

## Contamination

Implement chats: only prompts/control.md or prompts/gxp.md + task prompt.md + DEST.  
No hidden_tests, reference, or score_trial until all 12 claim-done.

## Operator notes

(fill anything else before starting)
EOF
fi

echo "BASE=$BASE"
echo "Seeded tools=${TOOLS[*]} arms=${ARMS[*]} tasks=${TASKS[*]}"
echo "Next: edit $PROTO then open implement chats per OPERATOR_RUNBOOK.md Phase B"
