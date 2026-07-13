#!/usr/bin/env bash
# Refresh "Last synced from core" markers to the latest commit that touched core/.
# Usage: bash scripts/update-sync-markers.sh
set -euo pipefail
cd "$(dirname "$0")/.."

SHA="$(git rev-list -1 HEAD -- core/)"
DATE="$(git log -1 --format=%cs "$SHA")"
MARKER="> **Last synced from core:** ${SHA} (${DATE})"

echo "core tip: $SHA ($DATE)"

update_file() {
  local f="$1"
  if [ ! -f "$f" ]; then
    echo "  skip missing $f"
    return
  fi
  if grep -qi 'last synced from core' "$f"; then
    # Replace existing marker line (bold or plain).
    local tmp
    tmp="$(mktemp)"
    awk -v m="$MARKER" '
      BEGIN { done=0 }
      tolower($0) ~ /last synced from core/ && !done {
        print m
        done=1
        next
      }
      { print }
    ' "$f" > "$tmp"
    mv "$tmp" "$f"
    echo "  updated $f"
  else
    # Insert after first heading line.
    local tmp
    tmp="$(mktemp)"
    awk -v m="$MARKER" '
      NR==1 { print; print ""; print m; next }
      { print }
    ' "$f" > "$tmp"
    mv "$tmp" "$f"
    echo "  inserted $f"
  fi
}

update_file adapters/claude/ai-workflow/instructions/workflow.md
update_file adapters/chatgpt/ai-workflow/instructions/workflow.md
update_file adapters/grok/ai-workflow/instructions/workflow.md
update_file adapters/perplexity/ai-workflow/instructions/workflow.md

echo "done"
