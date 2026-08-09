#!/usr/bin/env bash
#
# check-core.sh — lightweight presence + integrity check for adapters/grok-build.
#
# This adapter does not ship a generated instructions/workflow.md. Checks are
# structural (required files, SKILL frontmatter name, persona model convention)
# rather than a full workflow body diff.
#
# Usage (from anywhere):
#   bash adapters/grok-build/sync/check-core.sh
#   bash sync/check-core.sh   # when cwd is adapters/grok-build
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

echo "=== Grok Build adapter — Core Sync Check ==="
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
require "$ADAPTER_ROOT/INSTALL.md"
require "$ADAPTER_ROOT/README.md"
require "$ADAPTER_ROOT/install-grok-build.ps1"
require "$ADAPTER_ROOT/install-grok-build.sh"
require "$ADAPTER_ROOT/personas/gxp-researcher.toml"
require "$ADAPTER_ROOT/personas/gxp-architect.toml"
require "$ADAPTER_ROOT/personas/gxp-verifier.toml"
require "$ADAPTER_ROOT/personas/composer-coder.toml"
require "$ADAPTER_ROOT/personas/grok-native-planner.toml"
require "$ADAPTER_ROOT/workflows/gxp-heavy-front-half.rhai"
require "$ADAPTER_ROOT/workflows/gxp-layer2-verify.rhai"
require "$ADAPTER_ROOT/workflows/README.md"
require "$ADAPTER_ROOT/sync/drift-allowlist.txt"
echo ""

echo "3. SKILL.md integrity (Build-only identity)"
require_marker "$ADAPTER_ROOT/SKILL.md" "name: gxp-build"
# Must not claim the chat skill primary name as its own frontmatter name.
if [ -f "$ADAPTER_ROOT/SKILL.md" ] && grep -qE '^name:\s*gxp\s*$' "$ADAPTER_ROOT/SKILL.md"; then
  echo "  FAIL   SKILL.md name must not be bare 'gxp' (chat skill identity)"
  fail=1
else
  echo "  OK     SKILL.md does not use bare chat name 'gxp'"
fi
echo ""

echo "4. Persona model convention (model = \"grok-build\")"
for p in gxp-researcher gxp-architect gxp-verifier composer-coder grok-native-planner; do
  f="$ADAPTER_ROOT/personas/$p.toml"
  if [ ! -f "$f" ]; then
    echo "  MISSING: personas/$p.toml"
    fail=1
    continue
  fi
  if ! grep -qE '^model\s*=\s*"grok-build"' "$f"; then
    echo "  FAIL   personas/$p.toml: expected model = \"grok-build\""
    fail=1
  else
    echo "  OK     personas/$p.toml model = \"grok-build\""
  fi
done
echo ""

echo "5. Install isolation markers (docs + install scripts)"
require_marker "$ADAPTER_ROOT/INSTALL.md" "gxp-ai-workflow"
require_marker "$ADAPTER_ROOT/install-grok-build.ps1" "gxp-ai-workflow"
require_marker "$ADAPTER_ROOT/install-grok-build.sh" "gxp-ai-workflow"
# Write targets must never be the chat skill folders (only gxp-build / deny lists).
if grep -nE 'SkillTarget|SKILL_TARGET|TargetDir|TARGET_DIR' "$ADAPTER_ROOT/install-grok-build.ps1" "$ADAPTER_ROOT/install-grok-build.sh" 2>/dev/null \
  | grep -E 'gxp-ai-workflow|tinker-tools-ai-workflow' >/dev/null 2>&1; then
  echo "  FAIL   install script appears to target a protected chat skill path as write destination"
  fail=1
else
  echo "  OK     install scripts do not set chat skill paths as write targets"
fi
echo ""

if [ "$fail" -ne 0 ]; then
  echo "=== FAIL: Grok Build adapter check-core ==="
  exit 1
fi
echo "=== PASS: Grok Build adapter presence + integrity clean ==="
