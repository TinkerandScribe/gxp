#!/usr/bin/env bash
# Install the GXP .ai/ workflow scaffold from core/ into a target repo.
# Bash port of install-ai-from-core.ps1 (Mac/Linux/Git-Bash).
#
# By default creates missing files only. With --force, overwrites template files
# when content differs. Always preserves an existing .ai/PROGRAM.md and
# .ai/ratings.jsonl.
#
# Usage:
#   bash scripts/install-ai-from-core.sh [TARGET_REPO] [--force] [--include-cursor-rule]
#   bash scripts/install-ai-from-core.sh ../my-app --force
set -euo pipefail

TARGET="."
FORCE=0
INCLUDE_CURSOR=0
for arg in "$@"; do
  case "$arg" in
    --force) FORCE=1 ;;
    --include-cursor-rule) INCLUDE_CURSOR=1 ;;
    -*) echo "Unknown option: $arg" >&2; exit 2 ;;
    *) TARGET="$arg" ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CORE="$REPO_ROOT/core"
[ -d "$CORE" ] || { echo "Cannot find core/ at $CORE (run from the GXP repo)" >&2; exit 1; }

TARGET_ABS="$(cd "$TARGET" && pwd)"
AI="$TARGET_ABS/.ai"
created=0; updated=0; skipped=0

copy_scaffold() {  # $1=src  $2=dest  $3=preserve(0/1)
  local src="$1" dest="$2" preserve="${3:-0}" rel="${2#$TARGET_ABS/}"
  mkdir -p "$(dirname "$dest")"
  if [ -e "$dest" ]; then
    if [ "$preserve" = "1" ]; then echo "  - $rel (user file, preserved)"; skipped=$((skipped+1)); return; fi
    if [ "$FORCE" = "1" ]; then
      if cmp -s "$src" "$dest"; then echo "  - $rel (unchanged)"; skipped=$((skipped+1));
      else cp "$src" "$dest"; echo "  ~ $rel"; updated=$((updated+1)); fi
      return
    fi
    echo "  - $rel (exists)"; skipped=$((skipped+1)); return
  fi
  cp "$src" "$dest"; echo "  + $rel"; created=$((created+1))
}

ensure_empty_dir() {  # $1=dir
  mkdir -p "$1"
  [ -e "$1/.gitkeep" ] || { : > "$1/.gitkeep"; echo "  + ${1#$TARGET_ABS/}/.gitkeep"; created=$((created+1)); }
}

echo "Installing .ai scaffold from core/"
echo "  target: $TARGET_ABS"
[ "$FORCE" = "1" ] && echo "  mode:   force (overwrite changed templates)"
echo ""

mkdir -p "$AI"
copy_scaffold "$CORE/PROGRAM.template.md" "$AI/PROGRAM.md" 1
copy_scaffold "$CORE/workflow.md"         "$AI/workflow.md" 0
copy_scaffold "$CORE/routing.md"          "$AI/routing.md" 0
copy_scaffold "$CORE/ratings.jsonl"       "$AI/ratings.jsonl" 1

for sub in rules failures wiki evals; do
  [ -d "$CORE/$sub" ] || continue
  mkdir -p "$AI/$sub"
  find "$CORE/$sub" -maxdepth 1 -type f | while read -r f; do
    copy_scaffold "$f" "$AI/$sub/$(basename "$f")" 0
  done
done

ensure_empty_dir "$AI/evals/golden"
ensure_empty_dir "$AI/evals/regressions"
ensure_empty_dir "$AI/evals/canaries"

if [ -d "$CORE/templates" ]; then
  mkdir -p "$AI/templates"
  find "$CORE/templates" -maxdepth 1 -type f | while read -r f; do
    copy_scaffold "$f" "$AI/templates/$(basename "$f")" 0
  done
fi

if [ "$INCLUDE_CURSOR" = "1" ]; then
  RULE_SRC="$REPO_ROOT/adapters/cursor/ai-workflow/rule.mdc"
  if [ -e "$RULE_SRC" ]; then
    echo ""; echo "Installing Cursor rule..."
    mkdir -p "$TARGET_ABS/.cursor/rules"
    copy_scaffold "$RULE_SRC" "$TARGET_ABS/.cursor/rules/ai-workflow.mdc" 0
  fi
fi

echo ""
echo "Summary: created=$created updated=$updated skipped=$skipped"
echo ""
echo "Next steps:"
echo "  1. Edit .ai/PROGRAM.md with this project's verification commands."
echo "  2. Optional: add '.ai/tmp/' to .gitignore for ephemeral audit artifacts."
echo "  3. Paste core/docs/root-addenda into AGENTS.md / CLAUDE.md if desired."
