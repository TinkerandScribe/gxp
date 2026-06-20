#!/usr/bin/env bash
#
# check-core.sh — drift check for the Cowork adapter.
#
# Under the option-(a) source-of-truth model, the adapter does not check in
# copies of core/workflow.md or the templates — they're pulled at build time.
# So the drift check is **shape-based**, not byte-based:
#
#   1. The core/ files the build script depends on still exist.
#   2. The four SKILL.md files have well-formed YAML frontmatter.
#   3. Each skill's frontmatter `name` matches its directory.
#   4. No `description` field contains `<...>` XML-tag patterns.
#   5. plugin.json parses as JSON.
#
# Usage: bash adapters/cowork/sync/check-core.sh
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ADAPTER_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_ROOT="$(cd "$ADAPTER_ROOT/../.." && pwd)"
CORE_DIR="$REPO_ROOT/core"
SRC_DIR="$ADAPTER_ROOT/plugin-src"

fail() { echo "  - $1" >&2; FAILED=1; }
pass() { echo "  + $1"; }
FAILED=0

echo "[cowork check-core] core inputs exist..."
for f in \
    "workflow.md" \
    "templates/task-brief.md" \
    "templates/failure-capture.md" \
    "rules/01-no-secrets-in-git.md" \
    "rules/02-local-context-never-committed.md"
do
    if [[ -f "$CORE_DIR/$f" ]]; then
        pass "core/$f"
    else
        fail "core/$f missing"
    fi
done

echo "[cowork check-core] plugin.json parses..."
if python3 -c "import json,sys; json.load(open(sys.argv[1]))" "$SRC_DIR/.claude-plugin/plugin.json" 2>/dev/null; then
    pass "plugin-src/.claude-plugin/plugin.json"
else
    fail "plugin-src/.claude-plugin/plugin.json: invalid JSON"
fi

echo "[cowork check-core] SKILL.md frontmatter..."
python3 - "$SRC_DIR" <<'PY' || FAILED=1
import os, re, sys
src = sys.argv[1]
xml_tag = re.compile(r'<[A-Za-z][^>]*>')
errors = []
skills_dir = os.path.join(src, "skills")
if not os.path.isdir(skills_dir):
    print(f"  - {skills_dir} not a directory", file=sys.stderr); sys.exit(1)
for skill_dir in sorted(os.listdir(skills_dir)):
    p = os.path.join(skills_dir, skill_dir, "SKILL.md")
    if not os.path.exists(p):
        errors.append(f"missing {p}"); continue
    txt = open(p).read()
    if not txt.startswith("---"):
        errors.append(f"{p}: no YAML frontmatter"); continue
    end = txt.find("\n---", 3)
    if end == -1:
        errors.append(f"{p}: unterminated frontmatter"); continue
    fm = txt[3:end]
    name_match = re.search(r'^name:\s*(\S+)', fm, re.MULTILINE)
    desc_match = re.search(r'^description:\s*(.+?)(?=\n\S|\Z)', fm, re.MULTILINE | re.DOTALL)
    if not name_match or name_match.group(1) != skill_dir:
        errors.append(f"{p}: frontmatter name does not match dir {skill_dir!r}")
    if not desc_match:
        errors.append(f"{p}: missing description"); continue
    desc = desc_match.group(1)
    if xml_tag.search(desc):
        errors.append(f"{p}: description contains XML-tag-like substring (Cowork validator rejects this)")
if errors:
    for e in errors: print("  - " + e, file=sys.stderr)
    sys.exit(1)
print("  + all four SKILL.md frontmatters OK")
PY

if [[ $FAILED -ne 0 ]]; then
    echo "[cowork check-core] FAIL"
    exit 1
fi
echo "[cowork check-core] PASS"
