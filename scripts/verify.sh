#!/usr/bin/env bash
# GXP adapter-parity check.
# Confirms each adapter still ships its required files and runs any adapter
# sync checks that are present. Portable (bash); no project-specific test suite.
# Usage: bash scripts/verify.sh
set -euo pipefail

cd "$(dirname "$0")/.."
echo "=== GXP adapter parity check ==="
echo "Running from: $(pwd)"
fail=0

require() {
  if [ ! -e "$1" ]; then
    echo "  MISSING: $1"
    fail=1
  fi
}

echo ""
echo "1. Core methodology files"
for f in core/workflow.md core/routing.md core/PROGRAM.template.md \
         core/templates/task-brief.md core/templates/failure-capture.md \
         core/rules core/failures; do
  require "$f"
done

echo ""
echo "2. Required adapter files"
require adapters/cursor/ai-workflow/rule.mdc
require adapters/grok/ai-workflow/SKILL.md
require adapters/claude/ai-workflow/custom-instructions.md
require adapters/chatgpt/ai-workflow/custom-instructions.md
require adapters/chatgpt/ai-workflow/instructions/workflow.md
require adapters/chatgpt/ai-workflow/TEST_PROMPT.md
require adapters/codex/README.md
require adapters/codex/AGENTS.addendum.md
require adapters/codex/instructions/codex-handoff.md
require adapters/codex/TEST_PROMPT.md
require adapters/grok-build/SKILL.md
require adapters/grok-build/install-grok-build.ps1
require adapters/grok-build/install-grok-build.sh
require adapters/grok-build/personas/gxp-researcher.toml
require adapters/grok-build/personas/gxp-architect.toml
require adapters/grok-build/personas/gxp-verifier.toml
require adapters/grok-build/personas/composer-coder.toml
require adapters/grok-build/personas/grok-native-planner.toml
require adapters/grok-bot/SKILL.md
require adapters/grok-bot/README.md
require adapters/grok-bot/GETTING_STARTED.md
require adapters/perplexity/ai-workflow/SKILL.md
require adapters/cowork/plugin-src/.claude-plugin/plugin.json

echo ""
echo "3. Adapter sync checks (run when present; unjustified drift fails the build)"
for sh in adapters/*/ai-workflow/sync/check-core.sh adapters/*/sync/check-core.sh; do
  [ -e "$sh" ] || continue
  echo "   - $sh"
  if ! bash "$sh"; then
    echo "     FAIL: $sh reported drift or errors"
    fail=1
  fi
done

echo ""
echo "4. gxp-refine selftest (run when present; marker regressions fail the build)"
if [ -f scripts/eval-gxp-refine-selftest.sh ]; then
  echo "   - scripts/eval-gxp-refine-selftest.sh"
  if ! bash scripts/eval-gxp-refine-selftest.sh; then
    echo "     FAIL: gxp-refine selftest reported errors"
    fail=1
  fi
fi

echo ""
echo "5. Generated adapter workflows in sync"
# shellcheck source=scripts/lib/find-python.sh
source scripts/lib/find-python.sh
echo "   - scripts/generate-adapter-workflows.py --check (python: $PY)"
if ! "$PY" scripts/generate-adapter-workflows.py --check; then
  echo "     FAIL: generate-adapter-workflows.py --check reported drift"
  fail=1
fi

echo ""
echo "6. Job contract (schema, acyclic graph, one owner, COMMIT/clock, sealed)"
echo "   - scripts/validate-job-contract.py (python: $PY)"
if ! "$PY" scripts/validate-job-contract.py \
  --positive core/templates/job-contract.example.json \
  --positive scripts/fixtures/job-contract/hold-on-tau1.json \
  --positive scripts/fixtures/job-contract/hold-on-tau4.json \
  --positive scripts/fixtures/job-contract/refuse-on-tau2.json \
  --positive scripts/fixtures/job-contract/refuse-on-tau4.json \
  --positive scripts/fixtures/job-contract/none-on-tau1.json \
  --positive scripts/fixtures/job-contract/none-on-tau4.json \
  --negative schema=scripts/fixtures/job-contract/bad-lane.json \
  --negative cycle=scripts/fixtures/job-contract/cycle.json \
  --negative isc_work_owner=scripts/fixtures/job-contract/two-work-owners.json \
  --negative isc_work_owner=scripts/fixtures/job-contract/zero-work-owner.json \
  --negative isc_owner_bot=scripts/fixtures/job-contract/split-owner-bot.json \
  --negative decision_clock=scripts/fixtures/job-contract/commit-on-tau1.json \
  --negative decision_clock=scripts/fixtures/job-contract/commit-on-tau2.json \
  --negative sealed_pending=scripts/fixtures/job-contract/sealed-pending.json \
  --negative sealed_ref=scripts/fixtures/job-contract/sealed-by-work.json
then
  echo "     FAIL: job contract validator"
  fail=1
fi

echo ""
echo "7. Fleet store check (empty layout, positive fixture, negative fixtures)"
echo "   - fleet/bin/check.py (python: $PY)"
unset GXP_REPO
if [ -e fleet/bin/validate_ratings_chain.py ] || [ -e fleet/bin/validate-ratings-chain.py ]; then
  echo "     FAIL: ratings validator must be imported from scripts/, not vendored under fleet/bin"
  fail=1
fi
if ! "$PY" fleet/bin/check.py fleet; then
  echo "     FAIL: empty fleet store"
  fail=1
fi
if ! "$PY" fleet/bin/check.py scripts/fixtures/fleet/positive; then
  echo "     FAIL: positive fleet fixture"
  fail=1
fi
fleet_neg() {
  local token="$1"
  local root="$2"
  local out code
  set +e
  out=$("$PY" fleet/bin/check.py "$root" 2>&1)
  code=$?
  set -e
  if [ "$code" -eq 0 ]; then
    echo "     FAIL: $root exited 0; expected: $token"
    fail=1
    return
  fi
  if ! printf '%s\n' "$out" | grep -qF -- "$token"; then
    echo "     FAIL: $root did not report: $token"
    printf '%s\n' "$out"
    fail=1
    return
  fi
  echo "     OK negative $root"
}
fleet_neg "entry_hash mismatch" scripts/fixtures/fleet/tampered-hash
fleet_neg "invalid JSON" scripts/fixtures/fleet/bad-jsonl
fleet_neg "!= folder name" scripts/fixtures/fleet/job-id-mismatch
fleet_neg "missing required field" scripts/fixtures/fleet/missing-required
fleet_neg "blank.md: empty" scripts/fixtures/fleet/empty-md
fleet_neg "not a .md file" scripts/fixtures/fleet/non-md

echo "   - installed checker, no checkout on the parent path, GXP_REPO unset"
install_tmp=$(mktemp -d)
if ! (
  set -euo pipefail
  store="$install_tmp/store"
  bash fleet/install-to-store.sh "$store"
  "$PY" -c '
import sys
from pathlib import Path
script = Path(sys.argv[1]).resolve()
for candidate in script.parents:
    if (candidate / "scripts" / "validate-ratings-chain.py").is_file():
        raise SystemExit("parent walk reaches a checkout at %s" % candidate)
' "$store/bin/check.py"
  env -u GXP_REPO "$PY" "$store/bin/check.py" "$store"
  printf 'sentinel-ledger\n' > "$store/ratings.jsonl"
  bash fleet/install-to-store.sh "$store"
  grep -qF 'sentinel-ledger' "$store/ratings.jsonl"
  test -f "$store/bin/validate_ratings_chain.py"
  test -f "$store/schema/job-contract.schema.json"
); then
  echo "     FAIL: installed fleet checker (temp store without a checkout)"
  fail=1
else
  echo "     OK installed empty store"
fi
rm -rf "$install_tmp"

echo ""
if [ "$fail" -ne 0 ]; then
  echo "=== FAIL: missing required files, adapter drift, gen-check drift, gxp-refine selftest, job contract, or fleet store (see above) ==="
  exit 1
fi
echo "=== PASS: required files present, adapter sync checks clean, gen-check clean, gxp-refine selftest clean, job contract clean, fleet store clean ==="
