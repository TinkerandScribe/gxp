#!/usr/bin/env bash
#
# check-core.sh for ChatGPT adapter
#
# Compares the ChatGPT AI Workflow adapter against the canonical methodology in core/.
# Lighter than Grok version since ChatGPT adapter is primarily instructions-based.
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

# Files we care about (core path:adapter path:label)
declare -a CRITICAL_FILES=(
    "workflow.md:instructions/workflow.md:Workflow Definition"
)

declare -a OTHER_FILES=(
    "templates/task-brief.md:templates/task-brief.md:Task Brief Template"
    "templates/failure-capture.md:templates/failure-capture.md:Failure Capture Template"
    "templates/weekly-refine.md:templates/weekly-refine.md:Weekly Refine Template"
    "PROGRAM.template.md:PROGRAM.template.md:PROGRAM Template"
    "ratings.jsonl:ratings.jsonl:Ratings Schema"
    "rules/README.md:rules/README.md:Rules Philosophy"
    "failures/README.md:failures/README.md:Failures Philosophy"
)

# --- Argument Parsing ---
QUIET=false
STRICT=false
FULL_DIFF=false
LENIENT=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --help)
            sed -n '3,20p' "$0" | sed 's/^# \?//'
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

# --- Path Resolution (robust, with B3 copy-install guard) ---
find_repo_root() {
    local dir="$1"
    while [ "$dir" != "/" ]; do
        if [ -d "$dir/.git" ] || [ -f "$dir/.git" ]; then
            echo "$dir"
            return 0
        fi
        dir="$(dirname "$dir")"
    done
    echo "$ADAPTER_ROOT/../../../.."
}

REPO_ROOT="$(find_repo_root "$ADAPTER_ROOT")"
CORE_DIR="$REPO_ROOT/core"

# B3: copy-install robustness
if [ ! -d "$CORE_DIR" ]; then
    if [ "$QUIET" != true ]; then
        echo "[B3] copy-install mode detected (no core/ at $CORE_DIR) - warning only, exit 0" >&2
    fi
    exit 0
fi

# --- Staleness marker (real SHA; bold markdown tolerant) ---
STALE_THRESHOLD="${GXP_STALE_THRESHOLD:-3}"
STALE_FAIL=0
LAST_SYNCED_SHA=""
MARKER_STATUS="missing"

parse_sync_marker() {
    local wf="$1"
    LAST_SYNCED_SHA=""
    MARKER_STATUS="missing"
    [ -f "$wf" ] || return 0
    local marker_line
    marker_line=$(grep -i "last synced from core" "$wf" | head -1 || true)
    if [ -z "$marker_line" ]; then
        MARKER_STATUS="missing"
        return 0
    fi
    if [[ "$marker_line" =~ [Ll]ast[[:space:]]+[Ss]ynced[[:space:]]+[Ff]rom[[:space:]]+[Cc]ore:(\*\*)?[[:space:]]*([0-9a-fA-F]{7,40}) ]]; then
        LAST_SYNCED_SHA="${BASH_REMATCH[2]}"
        MARKER_STATUS="ok"
    else
        MARKER_STATUS="malformed"
    fi
}

evaluate_staleness() {
    if [ "$MARKER_STATUS" = "missing" ]; then
        echo "FAIL   Sync marker missing (expected > **Last synced from core:** <sha> (YYYY-MM-DD))" >&2
        STALE_FAIL=1
        return 0
    fi
    if [ "$MARKER_STATUS" = "malformed" ]; then
        echo "FAIL   Sync marker malformed (need real hex SHA)" >&2
        STALE_FAIL=1
        return 0
    fi
    if ! command -v git >/dev/null 2>&1; then
        [ "$QUIET" != true ] && echo "WARN   git not available; skipping staleness count"
        return 0
    fi
    if ! git -C "$REPO_ROOT" rev-parse --verify "${LAST_SYNCED_SHA}^{commit}" >/dev/null 2>&1; then
        local shallow
        shallow=$(git -C "$REPO_ROOT" rev-parse --is-shallow-repository 2>/dev/null || echo "false")
        if [ "$shallow" = "true" ]; then
            [ "$QUIET" != true ] && echo "WARN   Sync marker SHA $LAST_SYNCED_SHA not in shallow history (not a hard fail)"
            return 0
        fi
        echo "FAIL   Sync marker SHA unresolvable: $LAST_SYNCED_SHA" >&2
        STALE_FAIL=1
        return 0
    fi
    local commits_since
    commits_since=$(git -C "$REPO_ROOT" rev-list --count "$LAST_SYNCED_SHA..HEAD" -- core/ 2>/dev/null || echo "?")
    if [ "$commits_since" = "?" ]; then
        [ "$QUIET" != true ] && echo "WARN   Could not count commits since $LAST_SYNCED_SHA"
        return 0
    fi
    if [ "$commits_since" -gt "$STALE_THRESHOLD" ]; then
        echo "FAIL   Core has advanced $commits_since commit(s) since sync marker $LAST_SYNCED_SHA (threshold $STALE_THRESHOLD)" >&2
        STALE_FAIL=1
        return 0
    fi
    if [ "$commits_since" -gt 0 ]; then
        [ "$QUIET" != true ] && echo "NOTE   Core has advanced $commits_since commit(s) since last recorded sync ($LAST_SYNCED_SHA) — within threshold $STALE_THRESHOLD"
    else
        [ "$QUIET" != true ] && echo "OK     Sync marker current ($LAST_SYNCED_SHA)"
    fi
}

# --- Drift Allowlist ---
ALLOWLIST_FILE="$ADAPTER_ROOT/sync/drift-allowlist.txt"
ALLOWLIST=()
if [ -f "$ALLOWLIST_FILE" ]; then
    while IFS= read -r line || [ -n "$line" ]; do
        line=$(echo "$line" | tr -d '\r' | cut -d'#' -f1 | xargs)
        [ -n "$line" ] && ALLOWLIST+=("$line")
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


# --- Workflow structural floor (intentional rewrites; not whole-file allowlist) ---
structure_fail_count=0

check_workflow_marker() {
    local file="$1" pattern="$2" label="$3"
    if grep -qiE "$pattern" "$file"; then
        if [ "$QUIET" != true ]; then
            echo "PASS   $label"
        fi
    else
        echo "FAIL   $label (marker not found)" >&2
        structure_fail_count=$((structure_fail_count + 1))
    fi
}

check_workflow_structure() {
    local wf="$1"
    if [ ! -f "$wf" ]; then
        echo "MISSING instructions/workflow.md" >&2
        structure_fail_count=$((structure_fail_count + 1))
        return 0
    fi
    if [ "$QUIET" != true ]; then
        echo "=== Workflow structural floor ==="
    fi
    local n
    for n in 0 1 2 3 4 5 6 7 8; do
        check_workflow_marker "$wf" "Phase[[:space:]]+$n([^0-9]|$)" "Phase $n present"
    done
    check_workflow_marker "$wf" "4[^[:alnum:]]+8" "4-8 binary criteria rule"
    check_workflow_marker "$wf" "anti[-[:space:]]?loop" "Anti-loop rule"
    check_workflow_marker "$wf" "deterministic" "Deterministic-first verification"
    check_workflow_marker "$wf" "criteria_met" "Ratings field criteria_met"
    check_workflow_marker "$wf" "criteria_total" "Ratings field criteria_total"
    check_workflow_marker "$wf" '`ts`' "Ratings field ts"
    check_workflow_marker "$wf" '`rating`' "Ratings field rating"
}

# --- Comparison ---
diff_count=0
critical_diff_count=0
missing_count=0

compare_file() {
    local core_rel="$1"
    local adapter_rel="$2"
    local label="$3"
    local required="${4:-false}"

    local core_file="$CORE_DIR/$core_rel"
    local adapter_file="$ADAPTER_ROOT/$adapter_rel"

    if [ ! -f "$core_file" ]; then
        if [ "$QUIET" != true ]; then
            echo "SKIP   $label (missing in core)"
        fi
        return 0
    fi

    if [ ! -f "$adapter_file" ]; then
        if is_allowed "$label"; then
            if [ "$QUIET" != true ]; then
                echo "ALLOW  $label (intentionally not present per drift-allowlist.txt)"
            fi
            return 0
        fi
        if [ "$required" = true ] || [ "$STRICT" = true ]; then
            echo "MISSING $label" >&2
            missing_count=$((missing_count + 1))
        elif [ "$QUIET" != true ]; then
            echo "NOTE   $label (not present in adapter - may be intentional)"
        fi
        return 0
    fi

    if cmp -s "$core_file" "$adapter_file"; then
        if [ "$QUIET" != true ]; then
            echo "OK     $label"
        fi
        return 0
    fi

    # Present files are byte-compared; allowlist only covers intentional absence.
    diff_count=$((diff_count + 1))
    if [ "$required" = true ]; then
        critical_diff_count=$((critical_diff_count + 1))
    fi

    if [ "$QUIET" != true ]; then
        echo "DIFF   $label"
        if [ "$FULL_DIFF" = true ]; then
            diff -u "$core_file" "$adapter_file" | head -80
        else
            echo "  (use --full-diff to see complete diff)"
        fi
        echo ""
    fi
    return 0
}

# --- Main ---
if [ "$QUIET" != true ]; then
    echo ""
    echo "=== ChatGPT AI Workflow Adapter — Core Sync Check (bash) ==="
    echo "Repo root: $REPO_ROOT"
    echo "Core:      $CORE_DIR"
    echo "Adapter:   $ADAPTER_ROOT"
    echo ""
fi

parse_sync_marker "$ADAPTER_ROOT/instructions/workflow.md"
evaluate_staleness

# Critical workflow: structural floor (not whole-file allowlist)
check_workflow_structure "$ADAPTER_ROOT/instructions/workflow.md"

# Other
for entry in "${OTHER_FILES[@]}"; do
    IFS=':' read -r core_rel adapter_rel label <<< "$entry"
    compare_file "$core_rel" "$adapter_rel" "$label"
done

# Summary
if [ "$QUIET" != true ]; then
    echo ""
    if [ $structure_fail_count -gt 0 ]; then
        echo "Found $structure_fail_count workflow structural failure(s)."
    fi
    if [ $diff_count -gt 0 ]; then
        echo "Found $diff_count difference(s) ($critical_diff_count critical)."
    fi
    if [ $missing_count -gt 0 ]; then
        echo "Found $missing_count missing file(s)."
    fi
fi

if { [ $structure_fail_count -gt 0 ] || [ $critical_diff_count -gt 0 ] || [ $STALE_FAIL -gt 0 ]; } && [ "$LENIENT" != true ]; then
    echo "ACTION REQUIRED: Fix workflow structural floor, sync marker, and/or critical diffs." >&2
    exit 1
elif [ $structure_fail_count -gt 0 ] || [ $STALE_FAIL -gt 0 ] || [ $diff_count -gt 0 ] || [ $missing_count -gt 0 ]; then
    if [ "$QUIET" != true ]; then
        echo "Some differences noted (allowed or minor)."
    fi
    exit 0
else
    if [ "$QUIET" != true ]; then
        echo "Adapter is structurally aligned with core."
    fi
    exit 0
fi