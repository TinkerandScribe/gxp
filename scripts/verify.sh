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
require adapters/chatgpt/ai-workflow/custom-instructions.md
require adapters/chatgpt/ai-workflow/instructions/workflow.md
require adapters/chatgpt/ai-workflow/TEST_PROMPT.md
require adapters/codex/README.md
require adapters/codex/AGENTS.addendum.md
require adapters/codex/instructions/codex-handoff.md
require adapters/codex/TEST_PROMPT.md
require adapters/grok-build/SKILL.md
require adapters/grok-build/install-grok-build.ps1
require adapters/grok-build/install-grok-build.sh
require adapters/grok-build/personas/gxp-researcher.toml
require adapters/grok-build/personas/gxp-architect.toml
require adapters/grok-build/personas/gxp-verifier.toml
require adapters/grok-build/personas/composer-coder.toml
require adapters/grok-build/personas/grok-native-planner.toml
require adapters/perplexity/ai-workflow/SKILL.md
require adapters/cowork/plugin-src/.claude-plugin/plugin.json

echo ""
echo "3. Adapter sync checks (run when present; unjustified drift fails the build)"
for sh in adapters/*/ai-workflow/sync/check-core.sh adapters/*/sync/check-core.sh; do
  [ -e "$sh" ] || continue
  echo "   - $sh"
  if ! bash "$sh"; then
    echo "     FAIL: $sh reported drift or errors"
    fail=1
  fi
done

echo ""
echo "4. gxp-refine selftest (run when present; marker regressions fail the build)"
if [ -f scripts/eval-gxp-refine-selftest.sh ]; then
  echo "   - scripts/eval-gxp-refine-selftest.sh"
  if ! bash scripts/eval-gxp-refine-selftest.sh; then
    echo "     FAIL: gxp-refine selftest reported errors"
    fail=1
  fi
fi

echo ""
echo "5. Generated adapter workflows in sync"
# shellcheck source=scripts/lib/find-python.sh
source scripts/lib/find-python.sh
echo "   - scripts/generate-adapter-workflows.py --check (python: $PY)"
if ! "$PY" scripts/generate-adapter-workflows.py --check; then
  echo "     FAIL: generate-adapter-workflows.py --check reported drift"
  fail=1
fi

echo ""
if [ "$fail" -ne 0 ]; then
  echo "=== FAIL: missing required files, adapter drift, gen-check drift, or gxp-refine selftest (see above) ==="
  exit 1
fi
echo "=== PASS: required files present, adapter sync checks clean, gen-check clean, gxp-refine selftest clean ==="
