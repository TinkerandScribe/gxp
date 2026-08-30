#!/usr/bin/env bash
#
# check-core.sh — lightweight presence + integrity check for adapters/grok-bot.
#
# This adapter does not ship a generated instructions/workflow.md. Checks are
# structural (required files, SKILL identity, Bot constraint markers) rather
# than a full workflow body diff.
#
# Usage (from anywhere):
#   bash adapters/grok-bot/sync/check-core.sh
#   bash sync/check-core.sh   # when cwd is adapters/grok-bot
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ADAPTER_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_ROOT="$(cd "$ADAPTER_ROOT/../.." && pwd)"
CORE_DIR="$REPO_ROOT/core"
fail=0

require() {
  if [ ! -e "$1" ]; then
    echo "  MISSING: ${1#$REPO_ROOT/}"
    fail=1
  else
    echo "  OK     ${1#$REPO_ROOT/}"
  fi
}

require_marker() {
  local file="$1"
  local marker="$2"
  if [ ! -f "$file" ] || ! grep -qF "$marker" "$file"; then
    echo "  MISSING MARKER in ${file#$REPO_ROOT/}: $marker"
    fail=1
  else
    echo "  OK     marker in ${file#$REPO_ROOT/}: $marker"
  fi
}

echo "=== Grok Bot adapter — Core Sync Check ==="
echo "Repo root: $REPO_ROOT"
echo "Core:      $CORE_DIR"
echo "Adapter:   $ADAPTER_ROOT"
echo ""

echo "1. Core methodology present"
require "$CORE_DIR/workflow.md"
require "$CORE_DIR/templates/task-brief.md"
echo ""

echo "2. Required adapter files"
require "$ADAPTER_ROOT/SKILL.md"
require "$ADAPTER_ROOT/README.md"
require "$ADAPTER_ROOT/GETTING_STARTED.md"
require "$ADAPTER_ROOT/instructions/cursor-handoff.md"
require "$ADAPTER_ROOT/sync/drift-allowlist.txt"
echo ""

echo "3. SKILL.md integrity (Bot-only identity)"
require_marker "$ADAPTER_ROOT/SKILL.md" "name: gxp-bot"
if [ -f "$ADAPTER_ROOT/SKILL.md" ] && grep -qE '^name:\s*gxp\s*$' "$ADAPTER_ROOT/SKILL.md"; then
  echo "  FAIL   SKILL.md name must not be bare 'gxp' (chat skill identity)"
  fail=1
else
  echo "  OK     SKILL.md does not use bare chat name 'gxp'"
fi
if [ -f "$ADAPTER_ROOT/SKILL.md" ] && grep -qE '^name:\s*gxp-build\s*$' "$ADAPTER_ROOT/SKILL.md"; then
  echo "  FAIL   SKILL.md name must not be 'gxp-build' (Build skill identity)"
  fail=1
else
  echo "  OK     SKILL.md does not use Build name 'gxp-build'"
fi
echo ""

echo "4. Grok Bot constraint markers"
require_marker "$ADAPTER_ROOT/SKILL.md" "Never clone"
require_marker "$ADAPTER_ROOT/SKILL.md" "Never edit repos"
require_marker "$ADAPTER_ROOT/SKILL.md" "widgets"
require_marker "$ADAPTER_ROOT/SKILL.md" "cursor-agent"
require_marker "$ADAPTER_ROOT/SKILL.md" "Cursor cloud agent"
require_marker "$ADAPTER_ROOT/README.md" "thin"
require_marker "$ADAPTER_ROOT/README.md" "local CLI"
require_marker "$ADAPTER_ROOT/GETTING_STARTED.md" "widget"
require_marker "$ADAPTER_ROOT/instructions/cursor-handoff.md" "Ideal State Criteria"
require_marker "$ADAPTER_ROOT/instructions/cursor-handoff.md" "cursor-agent"
echo ""

echo "5. Must not outsource verify to the operator"
# Chat adapter anti-pattern: instructing the human to run check-core before work.
if grep -nE 'Please run this command|tell the user to run|instruct the user to run' \
    "$ADAPTER_ROOT/SKILL.md" "$ADAPTER_ROOT/GETTING_STARTED.md" 2>/dev/null \
  | grep -E 'check-core' >/dev/null 2>&1; then
  echo "  FAIL   Bot docs must not tell the operator to run check-core.sh"
  fail=1
else
  echo "  OK     Bot docs do not instruct the operator to run check-core.sh"
fi
if ! grep -qF "Never tell the operator to run" "$ADAPTER_ROOT/SKILL.md"; then
  echo "  MISSING MARKER in SKILL.md: Never tell the operator to run"
  fail=1
else
  echo "  OK     marker in SKILL.md: Never tell the operator to run"
fi
echo ""

echo "6. No Grok Build personas in this adapter"
for p in gxp-researcher gxp-architect gxp-verifier; do
  if [ -e "$ADAPTER_ROOT/personas/$p.toml" ]; then
    echo "  FAIL   personas/$p.toml must not ship on grok-bot"
    fail=1
  else
    echo "  OK     no personas/$p.toml"
  fi
done
echo ""

echo "7. Isolation from chat / Build skill identities"
require_marker "$ADAPTER_ROOT/README.md" "gxp-ai-workflow"
require_marker "$ADAPTER_ROOT/GETTING_STARTED.md" "gxp-ai-workflow"
if grep -nE 'SkillTarget|SKILL_TARGET|TargetDir|TARGET_DIR' \
    "$ADAPTER_ROOT"/install-* 2>/dev/null \
  | grep -E 'gxp-ai-workflow|tinker-tools-ai-workflow|gxp-build' >/dev/null 2>&1; then
  echo "  FAIL   install script appears to target a protected skill path as write destination"
  fail=1
else
  echo "  OK     no install scripts targeting chat/Build skill paths"
fi
echo ""

if [ "$fail" -ne 0 ]; then
  echo "=== FAIL: Grok Bot adapter check-core ==="
  exit 1
fi
echo "=== PASS: Grok Bot adapter presence + integrity clean ==="
