#!/usr/bin/env bash
#
# check-core.sh for Cursor adapter
#
# Compares the Cursor AI Workflow adapter against the canonical methodology in core/.
#
# Usage:
#   bash sync/check-core.sh [options]
#
# Options:
#   --help       Show this help
#   --quiet      Only show summary and exit code
#   --strict     Treat missing files as errors
#   --lenient    Do not fail on diffs for critical files
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ADAPTER_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_ROOT="$(cd "$ADAPTER_ROOT/../../.." && pwd)"
CORE_DIR="$REPO_ROOT/core"

QUIET=false
STRICT=false
LENIENT=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --help)
            sed -n '3,15p' "$0" | sed 's/^# \?//'
            exit 0
            ;;
        --quiet) QUIET=true; shift ;;
        --strict) STRICT=true; shift ;;
        --lenient) LENIENT=true; shift ;;
        *) echo "Unknown option $1"; exit 1 ;;
    esac
done

DRIFT=0

check_file() {
    local core_rel="$1"
    local adapter_rel="$2"
    local label="$3"
    local core_path="$CORE_DIR/$core_rel"
    local adapter_path="$ADAPTER_ROOT/$adapter_rel"

    if [ ! -f "$adapter_path" ]; then
        echo "  MISSING: $label ($adapter_rel)"
        DRIFT=1
        return
    fi

    if [ -f "$core_path" ]; then
        if ! cmp -s "$core_path" "$adapter_path"; then
            if [ "$LENIENT" = false ]; then
                echo "  DIFF: $label"
                DRIFT=1
            else
                echo "  DIFF (lenient): $label"
            fi
        fi
    fi
}

echo "Checking Cursor adapter against core (structural markers, not text diff)..."

# rule.mdc is a deliberate compressed adaptation of core/workflow.md (see
# drift-allowlist.txt: "Verbatim match is not the goal"), so a byte-compare
# would always fail. Mirror check-core.ps1's structural marker checks instead.
RULE_PATH="$ADAPTER_ROOT/rule.mdc"

check_marker() {
    local pattern="$1"
    local label="$2"
    if grep -qiE "$pattern" "$RULE_PATH"; then
        if [ "$QUIET" = false ]; then echo "  PASS: $label"; fi
    else
        echo "  FAIL: $label (marker not found in rule.mdc: $pattern)"
        DRIFT=1
    fi
}

if [ ! -f "$RULE_PATH" ]; then
    echo "  MISSING: rule.mdc"
    DRIFT=1
else
    check_marker "L3/L4 bounded agent"     "L3/L4 bounded agent reference"
    check_marker "4[^a-z0-9]8"             "4-8 criteria rule (hyphen or dash)"
    check_marker "anti-loop"               "Anti-loop phase reference"
    check_marker "deterministic"           "Deterministic verification order"
    check_marker "ratings\.jsonl"          "ratings.jsonl reference"
    check_marker "handoff"                 "Handoff phase reference"
    check_marker "v1\."                    "Version string present"
    check_marker "PowerShell"              "PowerShell environment note"
    check_marker "verification output"     "Verification output contract"
    check_marker "Composer"                "Composer usage guidance"
    check_marker "Phase -1"                "Capability gate section"
    check_marker "Capability & Permission" "Capability gate title"
    check_marker "PROGRAM\.md"             "PROGRAM.md verification pointer"
    check_marker "Repo-local Cursor"       "Preserve local rules note"
fi

# Required support files
check_file "" "sync/install-cursor-rule.ps1" "install script"
check_file "" "sync/check-core.ps1" "ps1 check script"

# Check for sh version (new)
if [ ! -f "$ADAPTER_ROOT/sync/check-core.sh" ]; then
    echo "  MISSING: sync/check-core.sh (bash version for non-Windows)"
    DRIFT=1
fi

if [ "$DRIFT" -eq 0 ]; then
    echo "Cursor adapter check: PASS"
    exit 0
else
    echo "Cursor adapter check: DRIFT or missing (exit 1 unless lenient)"
    if [ "$STRICT" = true ] || [ "$LENIENT" = false ]; then
        exit 1
    fi
    exit 0
fi
