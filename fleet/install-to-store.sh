#!/usr/bin/env bash
# Copy the fleet checker onto a store so it runs without a gxp checkout.
#
# Usage (from anywhere):
#   bash fleet/install-to-store.sh /home/box/shared/gxp
#
# Replaces bin/check.py, bin/append.py, bin/validate_ratings_chain.py,
# schema/job-contract.schema.json, README.md, and INSTALL.md. Creates jobs/,
# failures/, and regressions/ when
# missing. Creates ratings.jsonl and em-records.jsonl only when those files
# are absent. Never deletes or rewrites an existing ledger or capture.
set -euo pipefail

if [ "$#" -ne 1 ] || [ -z "$1" ]; then
  echo "usage: bash fleet/install-to-store.sh STORE_DIR" >&2
  exit 2
fi

STORE=$1
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPO=$(cd "$SCRIPT_DIR/.." && pwd)

mkdir -p "$STORE/bin" "$STORE/schema" "$STORE/jobs" "$STORE/failures" "$STORE/regressions"

install -m 775 "$REPO/fleet/bin/check.py" "$STORE/bin/check.py"
install -m 775 "$REPO/fleet/bin/append.py" "$STORE/bin/append.py"
install -m 775 "$REPO/scripts/validate-ratings-chain.py" "$STORE/bin/validate_ratings_chain.py"
install -m 664 "$REPO/core/templates/job-contract.schema.json" "$STORE/schema/job-contract.schema.json"
install -m 664 "$REPO/fleet/README.md" "$STORE/README.md"
install -m 664 "$REPO/fleet/INSTALL.md" "$STORE/INSTALL.md"

if [ ! -e "$STORE/ratings.jsonl" ]; then
  : > "$STORE/ratings.jsonl"
  chmod 664 "$STORE/ratings.jsonl"
fi
if [ ! -e "$STORE/em-records.jsonl" ]; then
  : > "$STORE/em-records.jsonl"
  chmod 664 "$STORE/em-records.jsonl"
fi

chmod 2775 "$STORE" "$STORE/bin" "$STORE/schema" "$STORE/jobs" "$STORE/failures" "$STORE/regressions"
