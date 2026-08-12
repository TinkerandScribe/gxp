#!/usr/bin/env bash
#
# sync-gxp-hosts.sh — scan host repos, optionally pull + refresh GXP .ai, commit, push.
#
# Defaults (safe):
#   - Dry-run report only (no writes) unless --apply
#   - Only touch repos that already have .ai/workflow.md (unless --bootstrap)
#   - pull --ff-only; skip dirty when committing; never force-push
#
# Usage:
#   bash scripts/sync-gxp-hosts.sh
#   bash scripts/sync-gxp-hosts.sh --apply
#   bash scripts/sync-gxp-hosts.sh --apply --commit --push
#   bash scripts/sync-gxp-hosts.sh --roots "$HOME/Claude" --apply --commit
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GXP_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
INSTALLER="$SCRIPT_DIR/install-ai-from-core.sh"

APPLY=0
COMMIT=0
PUSH=0
BOOTSTRAP=0
INCLUDE_CURSOR=0
MAX_DEPTH=3
ROOTS=()
EXCLUDE_REGEX='/(gxp-public|node_modules|\.git|dist|target|\.venv|venv)(/|$)'

# Default root: $HOME/Claude when present; otherwise require --roots
DEFAULT_ROOT=""
if [ -d "$HOME/Claude" ]; then
  DEFAULT_ROOT="$HOME/Claude"
fi

usage() {
  sed -n '2,20p' "$0" | sed 's/^# \?//'
  exit 0
}

while [ $# -gt 0 ]; do
  case "$1" in
    --apply) APPLY=1; shift ;;
    --commit) COMMIT=1; shift ;;
    --push) PUSH=1; shift ;;
    --bootstrap) BOOTSTRAP=1; shift ;;
    --include-cursor-rule) INCLUDE_CURSOR=1; shift ;;
    --max-depth) MAX_DEPTH="$2"; shift 2 ;;
    --roots)
      shift
      while [ $# -gt 0 ] && [[ "$1" != --* ]]; do ROOTS+=("$1"); shift; done
      ;;
    -h|--help) usage ;;
    *) echo "Unknown option: $1" >&2; exit 2 ;;
  esac
done

if [ "$PUSH" = "1" ] && [ "$COMMIT" != "1" ]; then
  echo "--push requires --commit" >&2; exit 2
fi
if [ "$COMMIT" = "1" ] && [ "$APPLY" != "1" ]; then
  echo "--commit requires --apply" >&2; exit 2
fi

if [ ${#ROOTS[@]} -eq 0 ]; then
  if [ -n "$DEFAULT_ROOT" ]; then
    ROOTS=("$DEFAULT_ROOT")
  else
    echo "No roots given and no default Claude directory found. Use --roots DIR" >&2
    exit 2
  fi
fi

[ -x "$INSTALLER" ] || [ -f "$INSTALLER" ] || { echo "Missing $INSTALLER" >&2; exit 1; }
[ -d "$GXP_ROOT/core" ] || { echo "Not a GXP checkout: $GXP_ROOT" >&2; exit 1; }

# Collect git repos under roots (depth-limited, skip excluded names / nested repos)
discover_repos() {
  local root depth
  for root in "${ROOTS[@]}"; do
    [ -d "$root" ] || { echo "WARN: root missing: $root" >&2; continue; }
    root="$(cd "$root" && pwd)"
    if [ -d "$root/.git" ] || [ -f "$root/.git" ]; then
      echo "$root"
    fi
    # find depth: MaxDepth levels of directories
    find "$root" -mindepth 1 -maxdepth "$MAX_DEPTH" \( -type d -name .git -o -type f -name .git \) 2>/dev/null \
      | while read -r g; do
          repo="$(dirname "$g")"
          case "$repo" in
            "$GXP_ROOT") continue ;;
          esac
          if echo "$repo" | grep -Eq "$EXCLUDE_REGEX"; then
            continue
          fi
          echo "$repo"
        done
  done | sort -u
}

mapfile -t REPOS < <(discover_repos)
# Filter gxp source
FILTERED=()
for r in "${REPOS[@]+"${REPOS[@]}"}"; do
  [ -z "${r:-}" ] && continue
  [ "$r" = "$GXP_ROOT" ] && continue
  FILTERED+=("$r")
done
REPOS=("${FILTERED[@]+"${FILTERED[@]}"}")

MODE="DRY-RUN"
[ "$APPLY" = "1" ] && MODE="APPLY"

echo "=== sync-gxp-hosts ($MODE) ==="
echo "GXP source: $GXP_ROOT"
echo "Roots:      ${ROOTS[*]}"
echo "MaxDepth:   $MAX_DEPTH"
echo "Repos:     ${#REPOS[@]}"
echo ""

fail=0
summary_file="$(mktemp)"
trap 'rm -f "$summary_file"' EXIT

for repo in "${REPOS[@]+"${REPOS[@]}"}"; do
  [ -z "${repo:-}" ] && continue
  name="$(basename "$repo")"
  has_gxp=0
  [ -f "$repo/.ai/workflow.md" ] && has_gxp=1

  if [ "$has_gxp" != "1" ] && [ "$BOOTSTRAP" != "1" ]; then
    echo "$name|no-gxp|no .ai/workflow.md" >>"$summary_file"
    continue
  fi

  dirty=0
  if [ -n "$(git -C "$repo" status --porcelain 2>/dev/null || true)" ]; then
    dirty=1
  fi

  if [ "$APPLY" = "1" ] && { [ "$COMMIT" = "1" ] || [ "$PUSH" = "1" ]; } && [ "$dirty" = "1" ]; then
    echo "$name|skip-dirty|dirty worktree" >>"$summary_file"
    continue
  fi

  pull_note="no-upstream"
  if git -C "$repo" rev-parse --abbrev-ref --symbolic-full-name '@{u}' >/dev/null 2>&1; then
    if [ "$APPLY" = "1" ]; then
      if [ "$dirty" = "1" ]; then
        pull_note="dirty (pull skipped)"
      else
        git -C "$repo" fetch origin >/dev/null 2>&1 || true
        if git -C "$repo" pull --ff-only >/dev/null 2>&1; then
          pull_note="pulled ff-only"
        else
          echo "$name|skip-pull|ff-only pull failed" >>"$summary_file"
          fail=$((fail + 1))
          continue
        fi
      fi
    else
      ab="$(git -C "$repo" rev-list --left-right --count 'HEAD...@{u}' 2>/dev/null || echo '?')"
      pull_note="would pull ff-only (ahead/behind $ab)"
    fi
  fi

  echo "--- $name ---"
  echo "  path: $repo"
  echo "  $pull_note"

  install_args=("$repo" --force)
  [ "$INCLUDE_CURSOR" = "1" ] && install_args+=(--include-cursor-rule)
  [ "$APPLY" != "1" ] && install_args+=(--dry-run)

  if ! bash "$INSTALLER" "${install_args[@]}"; then
    echo "$name|fail-install|installer failed" >>"$summary_file"
    fail=$((fail + 1))
    continue
  fi

  if [ "$APPLY" != "1" ]; then
    if [ "$has_gxp" = "1" ]; then
      echo "$name|would-update|$pull_note" >>"$summary_file"
    else
      echo "$name|would-bootstrap|$pull_note" >>"$summary_file"
    fi
    continue
  fi

  if [ -z "$(git -C "$repo" status --porcelain 2>/dev/null || true)" ]; then
    echo "$name|unchanged|$pull_note; scaffold already current" >>"$summary_file"
    continue
  fi

  if [ "$COMMIT" != "1" ]; then
    echo "$name|updated-uncommitted|$pull_note; pass --commit to commit" >>"$summary_file"
    continue
  fi

  git -C "$repo" add -- .ai 2>/dev/null || true
  [ -f "$repo/.cursor/rules/ai-workflow.mdc" ] && git -C "$repo" add -- .cursor/rules/ai-workflow.mdc || true

  if [ -z "$(git -C "$repo" diff --cached --name-only 2>/dev/null || true)" ]; then
    echo "$name|updated-uncommitted|nothing staged under .ai/" >>"$summary_file"
    continue
  fi

  msg_file="$(mktemp)"
  cat >"$msg_file" <<'EOF'
chore(gxp): refresh .ai scaffold from upstream GXP core

Synced via scripts/sync-gxp-hosts from gxp-public. Preserves PROGRAM.md and ratings.jsonl.
EOF
  if ! git -C "$repo" commit -F "$msg_file"; then
    rm -f "$msg_file"
    echo "$name|fail-commit|commit failed" >>"$summary_file"
    fail=$((fail + 1))
    continue
  fi
  rm -f "$msg_file"

  if [ "$PUSH" = "1" ]; then
    if ! git -C "$repo" rev-parse --abbrev-ref --symbolic-full-name '@{u}' >/dev/null 2>&1; then
      echo "$name|committed-no-push|no upstream" >>"$summary_file"
      continue
    fi
    if ! git -C "$repo" push; then
      echo "$name|fail-push|push failed" >>"$summary_file"
      fail=$((fail + 1))
      continue
    fi
    echo "$name|committed-pushed|ok" >>"$summary_file"
  else
    echo "$name|committed|local only (pass --push)" >>"$summary_file"
  fi
done

echo ""
echo "=== Summary ==="
if [ -s "$summary_file" ]; then
  column -t -s '|' "$summary_file" 2>/dev/null || cat "$summary_file"
else
  echo "(no repos found)"
fi
echo "Failures: $fail  Mode: $MODE"
[ "$fail" -eq 0 ] || exit 1
exit 0
