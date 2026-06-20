#!/usr/bin/env bash
# GXP adapter-parity check.
# Confirms each adapter still ships its required files and runs any adapter
# sync checks that are present. Portable (bash); no project-specific test suite.
# Usage: bash scripts/verify.sh
set -euo pipefail

cd "$(dirname "$0")/.."
echo "=== GXP adapter parity check ==="
echo "Running from: $(pwd)"
fail=0

require() {
  if [ ! -e "$1" ]; then
    echo "  MISSING: $1"
    fail=1
  fi
}

echo ""
echo "1. Core methodology files"
for f in core/workflow.md core/routing.md core/PROGRAM.template.md \
         core/templates/task-brief.md core/templates/failure-capture.md \
         core/rules core/failures; do
  require "$f"
done

echo ""
echo "2. Required adapter files"
require adapters/cursor/ai-workflow/rule.mdc
require adapters/grok/ai-workflow/SKILL.md
require adapters/claude/ai-workflow/custom-instructions.md
require adapters/perplexity/ai-workflow/SKILL.md
require adapters/cowork/plugin-src/.claude-plugin/plugin.json

echo ""
echo "3. Adapter sync checks (run when present)"
for sh in adapters/*/ai-workflow/sync/check-core.sh; do
  [ -e "$sh" ] || continue
  echo "   - $sh"
  bash "$sh" || echo "     (drift reported — review above)"
done

echo ""
if [ "$fail" -ne 0 ]; then
  echo "=== FAIL: one or more required files are missing ==="
  exit 1
fi
echo "=== PASS: all required files present ==="
