#!/usr/bin/env bash
# Compare process guarantees: BEFORE_REF (default v1.1.3) vs AFTER_REF (default HEAD).
# Writes Markdown + JSON under core/evals/canaries/gxp-version-comparison/.
set -euo pipefail
cd "$(dirname "$0")/.."

BEFORE_REF="${1:-v1.1.3}"
AFTER_REF="${2:-HEAD}"
OUT_DIR="core/evals/canaries/gxp-version-comparison"
mkdir -p "$OUT_DIR"

tmpdir="$(mktemp -d)"
cleanup() { rm -rf "$tmpdir"; }
trap cleanup EXIT

extract_tree() {
  local ref="$1" dest="$2"
  mkdir -p "$dest"
  git archive "$ref" \
    adapters/claude/ai-workflow/instructions/workflow.md \
    adapters/claude/ai-workflow/sync/check-core.sh \
    adapters/claude/ai-workflow/sync/drift-allowlist.txt \
    adapters/grok/ai-workflow/instructions/workflow.md \
    adapters/grok/ai-workflow/sync/check-core.sh \
    adapters/chatgpt/ai-workflow/instructions/workflow.md \
    scripts/verify.sh \
    core/workflow.md \
    2>/dev/null | tar -x -C "$dest" || true
}

score_tree() {
  local root="$1" label="$2"
  local wf="$root/adapters/claude/ai-workflow/instructions/workflow.md"
  local check="$root/adapters/claude/ai-workflow/sync/check-core.sh"
  local allow="$root/adapters/claude/ai-workflow/sync/drift-allowlist.txt"
  local gwf="$root/adapters/grok/ai-workflow/instructions/workflow.md"
  local gcheck="$root/adapters/grok/ai-workflow/sync/check-core.sh"
  local corew="$root/core/workflow.md"
  local verify="$root/scripts/verify.sh"

  declare -A R

  # 1. Claude workflow has Phase 8
  if [ -f "$wf" ] && grep -qE 'Phase[[:space:]]+8' "$wf"; then R[phase8]=1; else R[phase8]=0; fi
  # 2. Claude workflow lists ratings field ts
  if [ -f "$wf" ] && grep -q 'criteria_met' "$wf" && grep -q '`ts`' "$wf"; then R[ratings_fields]=1; else R[ratings_fields]=0; fi
  # 3. Claude workflow version header v1.1 (not v1.0)
  if [ -f "$wf" ] && grep -qE '\(v1\.1\)' "$wf"; then R[version_header]=1; else R[version_header]=0; fi
  # 4. check-core has structural floor (Phase markers)
  if [ -f "$check" ] && grep -q 'check_workflow_structure\|Phase[[:space:]]\+8 present\|structural floor' "$check"; then R[structural_floor]=1; else R[structural_floor]=0; fi
  # 5. Workflow Definition not whole-file allowlisted
  if [ -f "$allow" ] && grep -qiE 'Workflow Definition|^workflow\.md' "$allow"; then R[no_wholefile_allow]=0; else R[no_wholefile_allow]=1; fi
  # 6. Bold-tolerant sync marker regex (look for optional ** after core:)
  if { [ -f "$check" ] && grep -qF '(\*\*)?' "$check"; } || { [ -f "$gcheck" ] && grep -qF '(\*\*)?' "$gcheck"; }; then
    R[bold_marker_regex]=1
  else
    R[bold_marker_regex]=0
  fi
  # 7. Stale threshold hard-fail present
  if { [ -f "$check" ] && grep -q 'STALE_THRESHOLD\|StaleThreshold\|threshold' "$check"; } || { [ -f "$gcheck" ] && grep -q 'STALE_THRESHOLD' "$gcheck"; }; then R[stale_threshold]=1; else R[stale_threshold]=0; fi
  # 8. Real SHA marker on claude workflow
  if [ -f "$wf" ] && grep -qiE 'Last synced from core:\*\*[[:space:]]*[0-9a-fA-F]{7,}' "$wf"; then R[real_sha_marker]=1; else R[real_sha_marker]=0; fi
  # 9. Grok workflow states 4-8 criteria
  if [ -f "$gwf" ] && grep -qE '4.–8|4-8|4–8' "$gwf"; then R[grok_48]=1; else R[grok_48]=0; fi
  # 10. Core workflow still has Phase 8 (sanity)
  if [ -f "$corew" ] && grep -q 'Phase 8' "$corew"; then R[core_phase8]=1; else R[core_phase8]=0; fi
  # 11. CI workflow exists only on after typically — check in live tree for after
  R[ci_workflow]=0
  # 12. verify.sh fails on structural delete (behavioral) — run if tree is live after only
  R[neg_drift_behavioral]=0

  local keys=(phase8 ratings_fields version_header structural_floor no_wholefile_allow bold_marker_regex stale_threshold real_sha_marker grok_48 core_phase8)
  local sum=0
  for k in "${keys[@]}"; do sum=$((sum + R[$k])); done
  echo "$label total_partial=$sum/${#keys[@]}"

  # emit lines for report
  for k in "${keys[@]}"; do
    echo "RESULT $label $k ${R[$k]}"
  done
}

# Behavioral: negative drift on LIVE tree for AFTER only
behavioral_after() {
  local WF="adapters/claude/ai-workflow/instructions/workflow.md"
  if [ ! -f "$WF" ] || [ ! -f scripts/verify.sh ]; then
    echo "RESULT AFTER neg_drift_behavioral 0"
    return
  fi
  cp "$WF" "$WF.__eval_bak"
  awk '
    BEGIN { skip=0 }
    /^#{2,3}[[:space:]]+Phase[[:space:]]+8([^0-9]|$)/ { skip=1; next }
    /^#{2,3}[[:space:]]+/ && skip==1 { skip=0 }
    skip==0 { print }
  ' "$WF" > "$WF.__eval_tmp"
  mv "$WF.__eval_tmp" "$WF"
  set +e
  bash scripts/verify.sh >/dev/null 2>&1
  local code=$?
  set -e
  mv "$WF.__eval_bak" "$WF"
  if [ "$code" -ne 0 ]; then
    echo "RESULT AFTER neg_drift_behavioral 1"
  else
    echo "RESULT AFTER neg_drift_behavioral 0"
  fi
  # restore clean
  bash scripts/verify.sh >/dev/null 2>&1 || true
}

# Behavioral: same mutation on BEFORE tree extracted to temp
behavioral_before() {
  local root="$1"
  local WF="$root/adapters/claude/ai-workflow/instructions/workflow.md"
  local check="$root/adapters/claude/ai-workflow/sync/check-core.sh"
  if [ ! -f "$WF" ] || [ ! -f "$check" ]; then
    echo "RESULT BEFORE neg_drift_behavioral 0"
    return
  fi
  # At v1.1.3, whole-file allowlist means workflow drift never fails.
  # Simulate: delete Phase 8 if present; if never present, append junk "Phase drift".
  cp "$WF" "$WF.bak"
  if grep -qE 'Phase[[:space:]]+8' "$WF"; then
    awk '
      BEGIN { skip=0 }
      /^#{2,3}[[:space:]]+Phase[[:space:]]+8([^0-9]|$)/ { skip=1; next }
      /^#{2,3}[[:space:]]+/ && skip==1 { skip=0 }
      skip==0 { print }
    ' "$WF" > "$WF.tmp" && mv "$WF.tmp" "$WF"
  else
    echo "" >> "$WF"
    echo "### Phase DRIFT injected by eval" >> "$WF"
  fi
  set +e
  # Run only claude check from extracted tree — need CORE from live repo
  # Copy live core next to extracted adapters structure by using live REPO with before check
  # Simpler: run before check-core against live core but before workflow+check scripts
  REPO="$(pwd)"
  # temporarily swap files
  LIVE_WF="adapters/claude/ai-workflow/instructions/workflow.md"
  LIVE_CHECK="adapters/claude/ai-workflow/sync/check-core.sh"
  LIVE_ALLOW="adapters/claude/ai-workflow/sync/drift-allowlist.txt"
  cp "$LIVE_WF" "$tmpdir/live_wf.bak"
  cp "$LIVE_CHECK" "$tmpdir/live_check.bak"
  cp "$LIVE_ALLOW" "$tmpdir/live_allow.bak" 2>/dev/null || true
  cp "$WF" "$LIVE_WF"
  cp "$check" "$LIVE_CHECK"
  if [ -f "$root/adapters/claude/ai-workflow/sync/drift-allowlist.txt" ]; then
    cp "$root/adapters/claude/ai-workflow/sync/drift-allowlist.txt" "$LIVE_ALLOW"
  fi
  bash "$LIVE_CHECK" >/dev/null 2>&1
  local code=$?
  mv "$tmpdir/live_wf.bak" "$LIVE_WF"
  mv "$tmpdir/live_check.bak" "$LIVE_CHECK"
  if [ -f "$tmpdir/live_allow.bak" ]; then mv "$tmpdir/live_allow.bak" "$LIVE_ALLOW"; fi
  set -e
  mv "$WF.bak" "$WF"
  # For before: fail means detection works (1); pass means silent (0 for detection capability)
  # Result key = "detects_induced_drift" — 1 if check exits non-zero
  if [ "$code" -ne 0 ]; then
    echo "RESULT BEFORE neg_drift_behavioral 1"
  else
    echo "RESULT BEFORE neg_drift_behavioral 0"
  fi
}

echo "=== Extracting $BEFORE_REF and $AFTER_REF ==="
extract_tree "$BEFORE_REF" "$tmpdir/before"
extract_tree "$AFTER_REF" "$tmpdir/after"

RESULTS_FILE="$OUT_DIR/process-guarantees-raw.txt"
: > "$RESULTS_FILE"

{
  score_tree "$tmpdir/before" "BEFORE"
  score_tree "$tmpdir/after" "AFTER"
  behavioral_before "$tmpdir/before"
  behavioral_after
} | tee -a "$RESULTS_FILE"

# Build markdown report
# shellcheck source=lib/find-python.sh
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/lib/find-python.sh"
"$PY" - "$OUT_DIR" "$BEFORE_REF" "$AFTER_REF" <<'PY'
import sys, re, json
from pathlib import Path
from collections import defaultdict

out_dir = Path(sys.argv[1])
before_ref, after_ref = sys.argv[2], sys.argv[3]
raw = (out_dir / "process-guarantees-raw.txt").read_text(encoding="utf-8")
scores = defaultdict(dict)
for line in raw.splitlines():
    m = re.match(r"RESULT (BEFORE|AFTER) (\S+) ([01])", line)
    if m:
        scores[m.group(1)][m.group(2)] = int(m.group(3))

labels = {
    "phase8": "Claude workflow documents Phase 8 (Handoff)",
    "ratings_fields": "Claude workflow lists ratings fields (ts, criteria_met)",
    "version_header": "Claude workflow version header is v1.1",
    "structural_floor": "Claude check-core enforces structural floor",
    "no_wholefile_allow": "No whole-file Workflow Definition allowlist",
    "bold_marker_regex": "Sync-marker regex tolerates bold markdown",
    "stale_threshold": "Staleness threshold hard-fail present",
    "real_sha_marker": "Claude workflow has real hex sync marker",
    "grok_48": "Grok workflow states 4–8 criteria rule",
    "core_phase8": "core/workflow.md has Phase 8",
    "neg_drift_behavioral": "Induced workflow drift makes check fail",
}

keys = list(labels.keys())
# ensure keys exist
for side in ("BEFORE", "AFTER"):
    for k in keys:
        scores[side].setdefault(k, 0)

b_sum = sum(scores["BEFORE"][k] for k in keys)
a_sum = sum(scores["AFTER"][k] for k in keys)
n = len(keys)

rows = []
improved = 0
regressed = 0
for k in keys:
    b, a = scores["BEFORE"][k], scores["AFTER"][k]
    delta = a - b
    if delta > 0: improved += 1
    if delta < 0: regressed += 1
    mark = {1: "yes", 0: "no"}[b], {1: "yes", 0: "no"}[a]
    d = "↑" if delta > 0 else ("↓" if delta < 0 else "·")
    rows.append(f"| {labels[k]} | {mark[0]} | {mark[1]} | {d} |")

md = f"""# Process-guarantee scorecard

**Before:** `{before_ref}`  
**After:** `{after_ref}`  
**Generated by:** `scripts/eval-gxp-process-guarantees.sh`

## Totals

| Side | Score |
|---|---|
| Before | **{b_sum}/{n}** |
| After | **{a_sum}/{n}** |
| Net checks improved | **{improved}** (regressed: {regressed}) |

## Per-check

| Guarantee | Before | After | Δ |
|---|---|---|---|
""" + "\n".join(rows) + f"""

## Interpretation

These checks measure **enforceable process guarantees** (can the methodology
detect/prevent silent failure modes), not free-form prose quality of a coding agent.

- A higher score means more of the GXP loop is **machine-checkable** or **explicitly
  required in adapter text**.
- Behavioral row `Induced workflow drift makes check fail` is the key "does this
  improve real detection" signal.
"""
(out_dir / "process-guarantees.md").write_text(md, encoding="utf-8")
(out_dir / "process-guarantees.json").write_text(
    json.dumps({"before_ref": before_ref, "after_ref": after_ref, "before": scores["BEFORE"], "after": scores["AFTER"], "before_total": b_sum, "after_total": a_sum, "n": n}, indent=2),
    encoding="utf-8",
)
print(md)
print(f"Wrote {out_dir}/process-guarantees.md and .json")
PY
