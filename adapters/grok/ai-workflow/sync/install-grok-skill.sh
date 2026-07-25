#!/usr/bin/env bash
#
# install-grok-skill.sh
#
# Installs or updates the GXP skill into ~/.grok/skills/ and optionally
# installs example personas into ~/.grok/personas/*.toml
#
# Usage:
#   bash sync/install-grok-skill.sh [--force] [--skip-personas]
#

set -euo pipefail

FORCE=0
SKIP_PERSONAS=0
for arg in "$@"; do
  case "$arg" in
    --force|-f) FORCE=1 ;;
    --skip-personas) SKIP_PERSONAS=1 ;;
    -h|--help)
      echo "Usage: bash sync/install-grok-skill.sh [--force] [--skip-personas]"
      exit 0
      ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ADAPTER_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"   # ai-workflow folder
SKILLS_ROOT="$HOME/.grok/skills"
TARGET_DIR="$SKILLS_ROOT/gxp-ai-workflow"
LEGACY_DIR="$SKILLS_ROOT/tinker-tools-ai-workflow"
PERSONAS_DIR="$HOME/.grok/personas"
PERSONAS_SRC="$ADAPTER_ROOT/examples/grok-build-strategy/personas"

link_or_copy() {
  local link_path="$1"
  local target_path="$2"
  local label="$3"

  if [ -e "$link_path" ] || [ -L "$link_path" ]; then
    if [ "$FORCE" -ne 1 ]; then
      read -r -p "Target already exists at $link_path. Overwrite? (y/N) " response
      if [[ ! "$response" =~ ^[Yy]$ ]]; then
        echo "Skipped $label ($link_path)."
        return 1
      fi
    fi
    rm -rf "$link_path"
  fi

  mkdir -p "$(dirname "$link_path")"

  if ln -s "$target_path" "$link_path" 2>/dev/null; then
    echo "Linked $label -> $link_path"
  else
    cp -r "$target_path" "$link_path"
    echo "Copied $label to $link_path (not symlinked)"
  fi
  return 0
}

install_personas() {
  if [ ! -d "$PERSONAS_SRC" ]; then
    echo "No personas source at $PERSONAS_SRC - skipping personas."
    return 0
  fi

  # Grok expects ~/.grok/personas/*.toml - a bare file named "personas" breaks discovery.
  if [ -e "$PERSONAS_DIR" ] && [ ! -d "$PERSONAS_DIR" ]; then
    backup="$HOME/.grok/personas.file-backup-$(date +%Y%m%d-%H%M%S).toml"
    mv "$PERSONAS_DIR" "$backup"
    echo "Moved mis-shaped personas file to $backup"
  fi
  mkdir -p "$PERSONAS_DIR"

  local n=0
  for f in "$PERSONAS_SRC"/*.toml; do
    [ -f "$f" ] || continue
    base="$(basename "$f")"
    dest="$PERSONAS_DIR/$base"
    if [ -e "$dest" ] && [ "$FORCE" -ne 1 ]; then
      read -r -p "Persona $base exists. Overwrite? (y/N) " response
      if [[ ! "$response" =~ ^[Yy]$ ]]; then
        echo "  skipped $base"
        continue
      fi
    fi
    cp "$f" "$dest"
    echo "  persona: $base"
    n=$((n + 1))
  done
  echo "Installed $n persona file(s) into $PERSONAS_DIR"
}

echo "Installing Grok AI Workflow skill..."
echo "Source: $ADAPTER_ROOT"
echo "Target: $TARGET_DIR"
echo "Legacy alias: $LEGACY_DIR"

if ! link_or_copy "$TARGET_DIR" "$ADAPTER_ROOT" "gxp-ai-workflow"; then
  echo "Primary skill install cancelled."
  exit 0
fi

# Keep legacy folder name pointed at the same adapter so old discovery paths stay current.
link_or_copy "$LEGACY_DIR" "$ADAPTER_ROOT" "tinker-tools-ai-workflow (legacy alias)" || true

if [ "$SKIP_PERSONAS" -ne 1 ]; then
  echo
  echo "Installing GXP example personas..."
  install_personas
fi

echo
echo "Done! Skill short name: 'gxp' (or 'gxp-ai-workflow')."
echo "Recommended: bash sync/check-core.sh"
echo "Personas (if installed): /personas in Grok Build - gxp-researcher, gxp-architect, gxp-verifier, grok-native-planner, composer-coder."
echo "See GETTING_STARTED.md for Plan Mode + GXP usage."
