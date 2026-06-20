#!/usr/bin/env bash
#
# check-core.sh for Perplexity research adapter
#
# Presence and basic staleness check (lenient for research-phase adapter).
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ADAPTER_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

QUIET=false
STRICT=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --help) sed -n '3,12p' "$0" | sed 's/^# \?//'; exit 0 ;;
        --quiet) QUIET=true; shift ;;
        --strict) STRICT=true; shift ;;
        *) echo "Unknown option"; exit 1 ;;
    esac
done

DRIFT=0

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
check "sync/check-core.ps1"
check "sync/check-core.sh"

if [ "$DRIFT" -eq 0 ]; then
    [ "$QUIET" = false ] && echo "Perplexity adapter check: PASS (presence/staleness)"
    exit 0
else
    [ "$QUIET" = false ] && echo "Perplexity adapter check: missing components"
    [ "$STRICT" = true ] && exit 1
    exit 0
fi
