#!/usr/bin/env bash
# Structural selftest for gxp-refine v0 (marker / discoverability / fail-closed checks).
# Usage (Windows: Git Bash or WSL): bash scripts/eval-gxp-refine-selftest.sh
set -euo pipefail
cd "$(dirname "$0")/.."

fail=0
pass() { echo "  PASS: $1"; }
fail_msg() { echo "  FAIL: $1"; fail=1; }

require_file() {
  if [ -f "$1" ]; then pass "exists $1"; else fail_msg "missing $1"; fi
}

require_marker() {
  local file="$1" marker="$2"
  if [ ! -f "$file" ]; then
    fail_msg "cannot grep missing file $file for [$marker]"
    return
  fi
  if grep -Fq -- "$marker" "$file"; then
    pass "marker in $file: $marker"
  else
    fail_msg "missing marker in $file: $marker"
  fi
}

forbid_marker() {
  local file="$1" marker="$2"
  if [ ! -f "$file" ]; then
    fail_msg "cannot grep missing file $file for forbidden [$marker]"
    return
  fi
  if grep -Fq -- "$marker" "$file"; then
    fail_msg "forbidden marker in $file: $marker"
  else
    pass "forbidden absent in $file: $marker"
  fi
}

echo "=== gxp-refine selftest ==="

echo ""
echo "1. Required files"
require_file "core/templates/gxp-refine-run.md"
require_file "core/docs/gxp-refine.md"
require_file "adapters/cursor/ai-workflow/GXP_REFINE.md"
require_file "core/tasks/gxp-refine-design.md"

echo ""
echo "2. Run template markers (mutation budget, gates, operator-only, no auto-merge)"
TPL="core/templates/gxp-refine-run.md"
require_marker "$TPL" "Mutation budget = 1"
require_marker "$TPL" "GATE 1"
require_marker "$TPL" "GATE 2"
require_marker "$TPL" "operator-invoked only"
require_marker "$TPL" "No auto-apply"
require_marker "$TPL" "No auto-merge"

echo ""
echo "3. How-to links design + template + Windows verify/selftest"
HOWTO="core/docs/gxp-refine.md"
require_marker "$HOWTO" "gxp-refine-design.md"
require_marker "$HOWTO" "gxp-refine-run.md"
require_marker "$HOWTO" "bash scripts/verify.sh"
require_marker "$HOWTO" "bash scripts/eval-gxp-refine-selftest.sh"
require_marker "$HOWTO" "Git Bash"

echo ""
echo "4. Invocable surface: explicit trigger; no forbidden framing"
INV="adapters/cursor/ai-workflow/GXP_REFINE.md"
require_marker "$INV" "gxp-refine"
require_marker "$INV" "run gxp-refine"
require_marker "$INV" "Operator-invoked only"
require_marker "$INV" "No auto-apply"
require_marker "$INV" "No auto-merge"
forbid_marker "$INV" "gxp-rsi"
forbid_marker "$INV" "gxp-auto"
forbid_marker "$INV" "auto-merge promote"
forbid_marker "$INV" "unattended self-rewrite"

echo ""
echo "5. Ordinary START_SESSION must not auto-enter gxp-refine"
START="adapters/cursor/ai-workflow/START_SESSION.md"
if [ -f "$START" ]; then
  if grep -Eqi 'OPERATOR REQUEST:[[:space:]]*gxp-refine|enter gxp-refine|run gxp-refine' "$START"; then
    # Allow an explicit "does not enter" disclaimer.
    if grep -Eqi 'does \*\*not\*\* enter|does not enter|must \*\*not\*\* enter|must not enter' "$START"; then
      pass "START_SESSION disclaims gxp-refine auto-entry"
    else
      fail_msg "START_SESSION appears to invoke gxp-refine without a disclaimer"
    fi
  else
    pass "START_SESSION does not invoke gxp-refine"
  fi
else
  fail_msg "missing $START"
fi

echo ""
echo "6. Negative check: removing a required marker must fail detection"
NEG_FILE="$(mktemp)"
trap 'rm -f "$NEG_FILE"' EXIT
cp "$TPL" "$NEG_FILE"
# Strip GATE 1 marker lines — detection must notice.
# portable: recreate without GATE 1 heading text
grep -Fv "GATE 1" "$TPL" > "$NEG_FILE" || true
if grep -Fq -- "GATE 1" "$NEG_FILE"; then
  fail_msg "negative setup failed (GATE 1 still present)"
else
  if grep -Fq -- "GATE 1" "$TPL"; then
    pass "negative: live template has GATE 1; stripped copy does not"
  else
    fail_msg "live template missing GATE 1 (cannot prove negative)"
  fi
fi

echo ""
if [ "$fail" -ne 0 ]; then
  echo "=== FAIL: gxp-refine selftest ==="
  exit 1
fi
echo "=== PASS: gxp-refine selftest ==="
