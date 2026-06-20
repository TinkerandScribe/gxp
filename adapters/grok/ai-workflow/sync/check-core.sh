#!/usr/bin/env bash
#
# check-core.sh
#
# Compares the Grok AI Workflow skill against the canonical methodology in core/.
# Designed for power users who want to stay aligned without being blocked by
# intentional Grok-specific optimizations.
#
# Usage:
#   bash sync/check-core.sh [options]
#
# Options:
#   --help       Show this help
#   --quiet      Only show summary and exit code
#   --strict     Treat missing adapter files and structural differences as errors
#   --full-diff  Show full diffs instead of truncated ones
#   --lenient    Do not fail on diffs for critical files (useful during active development)
#
set -euo pipefail

# --- Configuration ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ADAPTER_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_ROOT=""
CORE_DIR=""

# Files we care about comparing (core path → adapter path)
# Format: "core/relative/path:adapter/relative/path:label"
declare -a CRITICAL_FILES=(
    "workflow.md:instructions/workflow.md:Workflow Definition"
)

declare -a TEMPLATE_FILES=(
    "templates/task-brief.md:templates/task-brief.md:Task Brief Template"
    "templates/failure-capture.md:templates/failure-capture.md:Failure Capture Template"
    "templates/weekly-refine.md:templates/weekly-refine.md:Weekly Refine Template"
)

# --- Argument Parsing ---
QUIET=false
STRICT=false
FULL_DIFF=false
LENIENT=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --help)
            sed -n '3,25p' "$0" | sed 's/^# \?//'
            exit 0
            ;;
        --quiet)     QUIET=true; shift ;;
        --strict)    STRICT=true; shift ;;
        --full-diff) FULL_DIFF=true; shift ;;
        --lenient)   LENIENT=true; shift ;;
        *)
            echo "Unknown option: $1" >&2
            echo "Use --help for usage." >&2
            exit 2
            ;;
    esac
done

# --- Path Resolution (robust) ---
find_repo_root() {
    local dir="$1"
    while [ "$dir" != "/" ]; do
        if [ -d "$dir/.git" ] || [ -f "$dir/.git" ]; then
            echo "$dir"
            return 0
        fi
        dir="$(dirname "$dir")"
    done
    # Fallback: assume we're inside the repo
    echo "$ADAPTER_ROOT/../../../.."
}

REPO_ROOT="$(find_repo_root "$ADAPTER_ROOT")"
CORE_DIR="$REPO_ROOT/core"

if [ ! -d "$CORE_DIR" ]; then
    echo "ERROR: Could not locate core/ directory." >&2
    echo "Expected it at: $CORE_DIR" >&2
    echo "Are you running this from inside a clone of gxp?" >&2
    exit 1
fi

# --- Last Synced Marker Detection ---
GROK_WORKFLOW="$ADAPTER_ROOT/instructions/workflow.md"
LAST_SYNCED_SHA=""

if [ -f "$GROK_WORKFLOW" ]; then
    marker_line=$(grep -i "last synced from core" "$GROK_WORKFLOW" | head -1 || true)
    if [[ "$marker_line" =~ Last\ synced\ from\ core:\ ([0-9a-fA-F]+) ]]; then
        LAST_SYNCED_SHA="${BASH_REMATCH[1]}"
    fi
fi

if [ -n "$LAST_SYNCED_SHA" ]; then
    if command -v git >/dev/null 2>&1 && git -C "$REPO_ROOT" rev-parse --verify "$LAST_SYNCED_SHA" >/dev/null 2>&1; then
        commits_since=$(git -C "$REPO_ROOT" rev-list --count "$LAST_SYNCED_SHA..HEAD" -- core/ 2>/dev/null || echo "?")
        if [ "$commits_since" != "0" ] && [ "$commits_since" != "?" ]; then
            log "${YELLOW}NOTE${RESET}   Core has advanced $commits_since commit(s) since last recorded sync ($LAST_SYNCED_SHA)"
        fi
    fi
fi

# --- Drift Allowlist ---
ALLOWLIST_FILE="$ADAPTER_ROOT/sync/drift-allowlist.txt"
declare -a ALLOWLIST=()

if [ -f "$ALLOWLIST_FILE" ]; then
    while IFS= read -r line || [ -n "$line" ]; do
        line=$(echo "$line" | sed 's/#.*//' | xargs)   # strip comments and trim
        [ -z "$line" ] && continue
        ALLOWLIST+=("$line")
    done < "$ALLOWLIST_FILE"
fi

is_allowed() {
    local label="$1"
    for pattern in "${ALLOWLIST[@]}"; do
        if [[ "$label" == *"$pattern"* ]]; then
            return 0
        fi
    done
    return 1
}

# --- Helpers ---
has_color() {
    [ -t 1 ] && [ "${TERM:-}" != "dumb" ]
}

if has_color; then
    GREEN="\033[32m"
    RED="\033[31m"
    YELLOW="\033[33m"
    BOLD="\033[1m"
    RESET="\033[0m"
else
    GREEN=""; RED=""; YELLOW=""; BOLD=""; RESET=""
fi

print_header() {
    $QUIET && return
    echo
    echo -e "${BOLD}=== $1 ===${RESET}"
}

log() {
    $QUIET && return
    echo -e "$1"
}

DIFF_COUNT=0
MISSING_COUNT=0
CRITICAL_DIFF_COUNT=0
WARNINGS=()

record_diff() {
    DIFF_COUNT=$((DIFF_COUNT + 1))
}

record_missing() {
    MISSING_COUNT=$((MISSING_COUNT + 1))
}

# --- Comparison Function ---
compare_file() {
    local core_rel="$1"
    local adapter_rel="$2"
    local label="$3"
    local required="${4:-true}"

    local core_file="$CORE_DIR/$core_rel"
    local adapter_file="$ADAPTER_ROOT/$adapter_rel"

    if [ ! -f "$core_file" ]; then
        log "${YELLOW}SKIP${RESET}  $label (missing in core)"
        return
    fi

    if [ ! -f "$adapter_file" ]; then
        if is_allowed "$label"; then
            log "${YELLOW}ALLOW${RESET} $label (intentionally not present per drift-allowlist.txt)"
            return
        fi
        if [ "$required" = "true" ] || [ "$STRICT" = true ]; then
            log "${RED}MISSING${RESET} $label"
            log "        Core:    $core_file"
            log "        Adapter: (does not exist)"
            record_missing
        else
            log "${YELLOW}NOTE${RESET}   $label (not present in adapter — may be intentional)"
        fi
        return
    fi

    if diff -q "$core_file" "$adapter_file" >/dev/null 2>&1; then
        log "${GREEN}OK${RESET}    $label"
        return
    fi

    # Files differ — check allowlist first
    if is_allowed "$label"; then
        log "${YELLOW}ALLOW${RESET} $label (intentionally diverged per drift-allowlist.txt)"
        return
    fi

    # Files differ
    record_diff

    # Track critical diffs separately for stricter default behavior
    for crit in "${CRITICAL_FILES[@]}"; do
        if [[ "$crit" == *":$adapter_rel:"* ]]; then
            CRITICAL_DIFF_COUNT=$((CRITICAL_DIFF_COUNT + 1))
            break
        fi
    done

    log "${RED}DIFF${RESET}  $label"

    if [ "$QUIET" = true ]; then
        return
    fi

    if [ "$FULL_DIFF" = true ]; then
        if command -v git >/dev/null 2>&1 && git -C "$REPO_ROOT" diff --no-color --no-ext-diff -- "$core_file" "$adapter_file" >/dev/null 2>&1; then
            git -C "$REPO_ROOT" diff --no-color --no-ext-diff -- "$core_file" "$adapter_file"
        else
            diff -u "$core_file" "$adapter_file"
        fi
    else
        if command -v git >/dev/null 2>&1; then
            git -C "$REPO_ROOT" diff --no-color --no-ext-diff --unified=1 -- "$core_file" "$adapter_file" | head -30
        else
            diff -u "$core_file" "$adapter_file" | head -25
        fi
        echo "    (use --full-diff to see complete diff)"
    fi
    echo
}

# --- Main Checks ---
print_header "Grok AI Workflow — Core Sync Check"
log "Repo root: $REPO_ROOT"
log "Core:      $CORE_DIR"
log "Adapter:   $ADAPTER_ROOT"
echo

print_header "Critical Methodology"
compare_file "workflow.md" "instructions/workflow.md" "Workflow Definition" "true"

print_header "Templates"
for item in "${TEMPLATE_FILES[@]}"; do
    IFS=':' read -r core_rel adapter_rel label <<< "$item"
    compare_file "$core_rel" "$adapter_rel" "$label" "false"
done

print_header "Supporting Files"
compare_file "PROGRAM.template.md" "PROGRAM.template.md" "PROGRAM Template" "false"
compare_file "ratings.jsonl" "ratings.jsonl" "Ratings Schema" "false"

print_header "Core Philosophy"
compare_file "rules/README.md"   "rules/README.md"   "Rules Philosophy"   "false"
compare_file "failures/README.md" "failures/README.md" "Failures Philosophy" "false"

# --- SKILL.md sanity check ---
print_header "Grok Skill Integrity"
if [ -f "$ADAPTER_ROOT/SKILL.md" ]; then
    if grep -q "check-core.sh" "$ADAPTER_ROOT/SKILL.md"; then
        log "${GREEN}OK${RESET}    SKILL.md contains sync instruction"
    else
        log "${YELLOW}WARN${RESET}  SKILL.md is missing reference to check-core.sh"
        WARNINGS+=("SKILL.md should instruct users to run sync/check-core.sh before major work")
    fi
else
    log "${RED}MISSING${RESET} SKILL.md"
    record_missing
fi

# --- Summary ---
echo
print_header "Summary"

CRITICAL_FAILURE=false
if [ "$CRITICAL_DIFF_COUNT" -gt 0 ] && [ "$LENIENT" = false ]; then
    CRITICAL_FAILURE=true
fi

if [ "$DIFF_COUNT" -eq 0 ] && [ "$MISSING_COUNT" -eq 0 ] && [ "$CRITICAL_FAILURE" = false ]; then
    log "${GREEN}✓ All checked files are in sync with core.${RESET}"
    EXIT_CODE=0
else
    if [ "$CRITICAL_DIFF_COUNT" -gt 0 ]; then
        if [ "$LENIENT" = true ]; then
            log "${YELLOW}! $CRITICAL_DIFF_COUNT critical file(s) differ from core (lenient mode).${RESET}"
        else
            log "${RED}✗ $CRITICAL_DIFF_COUNT critical file(s) differ from core.${RESET}"
        fi
    fi
    if [ "$DIFF_COUNT" -gt "$CRITICAL_DIFF_COUNT" ]; then
        log "${RED}✗ $((DIFF_COUNT - CRITICAL_DIFF_COUNT)) non-critical file(s) differ from core.${RESET}"
    fi
    if [ "$MISSING_COUNT" -gt 0 ]; then
        log "${RED}✗ $MISSING_COUNT required file(s) missing from adapter.${RESET}"
    fi

    if [ "$CRITICAL_FAILURE" = true ]; then
        EXIT_CODE=1
    elif [ "$STRICT" = true ] && [ "$MISSING_COUNT" -gt 0 ]; then
        EXIT_CODE=1
    else
        EXIT_CODE=0
    fi
fi

if [ "${#WARNINGS[@]}" -gt 0 ]; then
    echo
    for w in "${WARNINGS[@]}"; do
        log "${YELLOW}!${RESET} $w"
    done
fi

echo
log "This check is intentionally focused. For important work, also review recent commits in core/."

if [ "$EXIT_CODE" -ne 0 ]; then
    echo
    log "Recommendation:"
    log "  • Review the diffs above"
    log "  • Decide whether to port changes from core or document intentional divergence"
    log "  • Re-run this script after updates"
fi

exit "$EXIT_CODE"