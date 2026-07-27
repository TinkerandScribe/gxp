#!/usr/bin/env bash
#
# install-grok-build.sh
#
# Default: install personas into ~/.grok/personas/*.toml
# Optional: --install-skill junctions/copies this adapter to ~/.grok/skills/gxp-build
#
# NEVER touches chat skill paths:
#   ~/.grok/skills/gxp-ai-workflow
#   ~/.grok/skills/tinker-tools-ai-workflow
#
# Usage:
#   bash install-grok-build.sh
#   bash install-grok-build.sh --force
#   bash install-grok-build.sh --force --install-skill
#   bash install-grok-build.sh --force --skip-personas --install-skill
#

set -euo pipefail

FORCE=0
SKIP_PERSONAS=0
INSTALL_SKILL=0
for arg in "$@"; do
  case "$arg" in
    --force|-f) FORCE=1 ;;
    --skip-personas) SKIP_PERSONAS=1 ;;
    --install-skill) INSTALL_SKILL=1 ;;
    -h|--help)
      echo "Usage: bash install-grok-build.sh [--force] [--skip-personas] [--install-skill]"
      echo "  Default: personas only. --install-skill adds ~/.grok/skills/gxp-build only."
      echo "  Never writes gxp-ai-workflow or tinker-tools-ai-workflow."
      exit 0
      ;;
    *)
      echo "Unknown argument: $arg" >&2
      echo "Usage: bash install-grok-build.sh [--force] [--skip-personas] [--install-skill]" >&2
      exit 2
      ;;
  esac
done

ADAPTER_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_ROOT="$HOME/.grok/skills"
SKILL_TARGET="$SKILLS_ROOT/gxp-build"
PERSONAS_DIR="$HOME/.grok/personas"
PERSONAS_SRC="$ADAPTER_ROOT/personas"

assert_not_protected() {
  local path="$1"
  local leaf
  leaf="$(basename "$path")"
  case "$leaf" in
    gxp-ai-workflow|tinker-tools-ai-workflow)
      echo "Refusing to write protected chat skill path: $path" >&2
      exit 1
      ;;
  esac
}

link_or_copy() {
  local link_path="$1"
  local target_path="$2"
  local label="$3"

  assert_not_protected "$link_path"

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

echo "Installing Grok Build GXP adapter..."
echo "Source: $ADAPTER_ROOT"
echo "Personas target: $PERSONAS_DIR"
if [ "$INSTALL_SKILL" -eq 1 ]; then
  echo "Skill target: $SKILL_TARGET (opt-in)"
else
  echo "Skill: skipped (default personas-only; pass --install-skill to add gxp-build)"
fi

if [ "$SKIP_PERSONAS" -ne 1 ]; then
  echo
  echo "Installing GXP Build personas..."
  install_personas
else
  echo
  echo "Skipping personas (--skip-personas)."
fi

if [ "$INSTALL_SKILL" -eq 1 ]; then
  echo
  echo "Installing gxp-build skill (opt-in)..."
  assert_not_protected "$SKILL_TARGET"
  link_or_copy "$SKILL_TARGET" "$ADAPTER_ROOT" "gxp-build" || echo "Skill install cancelled."
fi

echo
echo "Done."
echo "Protected (never touched): gxp-ai-workflow, tinker-tools-ai-workflow"
echo "Personas (if installed): /personas in Grok Build - gxp-researcher, gxp-architect, gxp-verifier, grok-native-planner, composer-coder."
if [ "$INSTALL_SKILL" -eq 1 ]; then
  echo "Skill short name: gxp-build (folder ~/.grok/skills/gxp-build)"
fi
echo "See INSTALL.md and README.md."
