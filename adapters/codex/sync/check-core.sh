#!/usr/bin/env bash
# Validate that the Codex adapter has its required delivery files and core still exists.
set -euo pipefail

adapter_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
repo_root="$(cd "$adapter_dir/../.." && pwd)"
fail=0

require() {
  if [ ! -e "$1" ]; then
    echo "MISSING: ${1#$repo_root/}"
    fail=1
  fi
}

require "$repo_root/core/workflow.md"
require "$repo_root/core/templates/task-brief.md"
require "$adapter_dir/README.md"
require "$adapter_dir/AGENTS.addendum.md"
require "$adapter_dir/instructions/codex-handoff.md"
require "$adapter_dir/TEST_PROMPT.md"

# Lightweight content floors (presence-only is not enough for hollow handoffs)
require_marker() {
  local file="$1"
  local marker="$2"
  if [ ! -f "$file" ] || ! grep -qF "$marker" "$file"; then
    echo "MISSING MARKER in ${file#$repo_root/}: $marker"
    fail=1
  fi
}

require_marker "$adapter_dir/instructions/codex-handoff.md" "Ideal State Criteria"
require_marker "$adapter_dir/instructions/codex-handoff.md" "Verification plan"
require_marker "$adapter_dir/AGENTS.addendum.md" "without its output"
require_marker "$adapter_dir/AGENTS.addendum.md" "concurrent writers"

if [ "$fail" -ne 0 ]; then
  exit 1
fi

echo "PASS: Codex adapter files, markers, and core methodology are present"
