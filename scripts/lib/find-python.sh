# shellcheck shell=bash
# Resolve a working Python interpreter into PY.
#
# Usage (from any script under scripts/ or adapters/):
#   # shellcheck source=../lib/find-python.sh
#   source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/../lib/find-python.sh"
#   # or for adapters/cowork:
#   source "$REPO_ROOT/scripts/lib/find-python.sh"
#   "$PY" ...
#
# Probes executability (not mere existence). On Windows Git Bash, `python3` may
# be the Microsoft Store stub — see core/failures/windows-git-bash-python3-store-stub.md.

gxp_find_python() {
  local candidate
  for candidate in python3 python; do
    if command -v "$candidate" >/dev/null 2>&1 && "$candidate" -c "" >/dev/null 2>&1; then
      PY="$candidate"
      return 0
    fi
  done
  echo "gxp_find_python: no executable python3/python on PATH" >&2
  return 1
}

# Set PY when this file is sourced (not when executed directly).
# With `set -e` in the caller, failure aborts the caller (desired).
if [[ "${BASH_SOURCE[0]}" != "${0}" ]]; then
  gxp_find_python
fi
