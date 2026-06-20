#!/usr/bin/env bash
#
# install-grok-skill.sh
#
# Installs or updates the GXP skill into ~/.grok/skills/
#
# Usage:
#   bash sync/install-grok-skill.sh [--force]
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ADAPTER_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"   # Points to the ai-workflow folder when run from sync/
TARGET_DIR="$HOME/.grok/skills/gxp-ai-workflow"

echo "Installing Grok AI Workflow skill..."
echo "Source: $ADAPTER_ROOT"
echo "Target: $TARGET_DIR"

if [ -d "$TARGET_DIR" ]; then
    if [[ "${1:-}" != "--force" && "${1:-}" != "-f" ]]; then
        read -p "Target already exists. Overwrite? (y/N) " response
        if [[ ! "$response" =~ ^[Yy]$ ]]; then
            echo "Installation cancelled."
            exit 0
        fi
    fi
    rm -rf "$TARGET_DIR"
fi

# Try symlink first (best for development)
if ln -s "$ADAPTER_ROOT" "$TARGET_DIR" 2>/dev/null; then
    echo "Created symlink at $TARGET_DIR"
    echo "Changes in this repo will be immediately visible to Grok."
else
    # Fallback to copy
    cp -r "$ADAPTER_ROOT" "$TARGET_DIR"
    echo "Copied skill to $TARGET_DIR (not symlinked)"
    echo "Re-run this script after updates."
fi

echo
echo "Done! The skill is now available under the short name 'gxp' (recommended) or 'gxp-ai-workflow' in your Grok chats."
echo "Recommended: Run the check script after installation:"
echo "  bash sync/check-core.sh"
echo ""
echo "For even easier access, source gxp.ps1 (or create shell aliases)."
echo "See GETTING_STARTED.md for instructions."
