#!/usr/bin/env bash
#
# check-core.sh for Perplexity research adapter
# Presence check + real sync-marker staleness (same marker format as other adapters).
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ADAPTER_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

find_repo_root() {
    local dir="$1"
    while [ "$dir" != "/" ]; do
        if [ -d "$dir/.git" ] || [ -f "$dir/.git" ]; then
            echo "$dir"
            return 0
        fi
        dir="$(dirname "$dir")"
    done
    echo "$ADAPTER_ROOT/../../.."
}

REPO_ROOT="$(find_repo_root "$ADAPTER_ROOT")"
QUIET=false
STRICT=false
STALE_THRESHOLD="${GXP_STALE_THRESHOLD:-3}"
STALE_FAIL=0
DRIFT=0

while [[ $# -gt 0 ]]; do
    case "$1" in
        --help) sed -n '3,12p' "$0" | sed 's/^# \?//'; exit 0 ;;
        --quiet) QUIET=true; shift ;;
        --strict) STRICT=true; shift ;;
        --stale-threshold) STALE_THRESHOLD="$2"; shift 2 ;;
        *) echo "Unknown option"; exit 1 ;;
    esac
done

check() {
    if [ ! -f "$ADAPTER_ROOT/$1" ]; then
        [ "$QUIET" = false ] && echo "  MISSING: $1"
        DRIFT=1
    fi
}

[ "$QUIET" = false ] && echo "Checking Perplexity adapter (research phase)..."

check "README.md"
check "instructions/research-workflow.md"
check "instructions/research-handoff.md"
check "instructions/workflow.md"
check "sync/check-core.ps1"
check "sync/check-core.sh"

# Trust-boundary markers (research-stage adapter — must stay durable)
HO="$ADAPTER_ROOT/instructions/research-handoff.md"
if [ -f "$HO" ]; then
    for needle in "Verified findings" "Inferences" "Open questions" "Explicit non-claims" "Research-stage only"; do
        if ! grep -qF "$needle" "$HO"; then
            [ "$QUIET" = false ] && echo "  MISSING marker in research-handoff.md: $needle"
            DRIFT=1
        fi
    done
fi
if [ -f "$ADAPTER_ROOT/SKILL.md" ]; then
    if ! grep -qF "No false local-verify" "$ADAPTER_ROOT/SKILL.md" \
        && ! grep -qF "false local-verify" "$ADAPTER_ROOT/SKILL.md"; then
        [ "$QUIET" = false ] && echo "  MISSING marker in SKILL.md: false local-verify"
        DRIFT=1
    fi
fi

LAST_SYNCED_SHA=""
MARKER_STATUS="missing"
WF="$ADAPTER_ROOT/instructions/workflow.md"
if [ -f "$WF" ]; then
    marker_line=$(grep -i "last synced from core" "$WF" | head -1 || true)
    if [ -z "$marker_line" ]; then
        MARKER_STATUS="missing"
    elif [[ "$marker_line" =~ [Ll]ast[[:space:]]+[Ss]ynced[[:space:]]+[Ff]rom[[:space:]]+[Cc]ore:(\*\*)?[[:space:]]*([0-9a-fA-F]{7,40}) ]]; then
        LAST_SYNCED_SHA="${BASH_REMATCH[2]}"
        MARKER_STATUS="ok"
    else
        MARKER_STATUS="malformed"
    fi
fi

if [ "$MARKER_STATUS" = "missing" ] || [ "$MARKER_STATUS" = "malformed" ]; then
    echo "FAIL   Sync marker $MARKER_STATUS on instructions/workflow.md" >&2
    STALE_FAIL=1
elif command -v git >/dev/null 2>&1; then
    if ! git -C "$REPO_ROOT" rev-parse --verify "${LAST_SYNCED_SHA}^{commit}" >/dev/null 2>&1; then
        shallow=$(git -C "$REPO_ROOT" rev-parse --is-shallow-repository 2>/dev/null || echo "false")
        if [ "$shallow" = "true" ]; then
            [ "$QUIET" = false ] && echo "WARN   Sync marker SHA not in shallow history"
        else
            echo "FAIL   Sync marker SHA unresolvable: $LAST_SYNCED_SHA" >&2
            STALE_FAIL=1
        fi
    else
        commits_since=$(git -C "$REPO_ROOT" rev-list --count "$LAST_SYNCED_SHA..HEAD" -- core/ 2>/dev/null || echo "?")
        if [ "$commits_since" != "?" ] && [ "$commits_since" -gt "$STALE_THRESHOLD" ]; then
            echo "FAIL   Core advanced $commits_since commit(s) since marker (threshold $STALE_THRESHOLD)" >&2
            STALE_FAIL=1
        elif [ "$commits_since" != "?" ] && [ "$commits_since" -gt 0 ]; then
            [ "$QUIET" = false ] && echo "NOTE   Core advanced $commits_since commit(s) since marker (within threshold)"
        else
            [ "$QUIET" = false ] && echo "OK     Sync marker current ($LAST_SYNCED_SHA)"
        fi
    fi
fi

if [ "$DRIFT" -eq 0 ] && [ "$STALE_FAIL" -eq 0 ]; then
    [ "$QUIET" = false ] && echo "Perplexity adapter check: PASS (presence + staleness)"
    exit 0
fi
[ "$QUIET" = false ] && echo "Perplexity adapter check: FAIL"
exit 1
