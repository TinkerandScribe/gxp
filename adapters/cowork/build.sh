#!/usr/bin/env bash
#
# build.sh -- assemble adapters/cowork/dist/gxp.plugin from plugin-src/ + core/.
#
# Source-of-truth model: option (a). plugin-src/ holds only adapter-authored
# content; this script pulls core/workflow.md, the templates, and the rules
# into each skill's references/ folder, then zips into dist/gxp.plugin.
#
# Usage:
#   bash adapters/cowork/build.sh           # build
#   bash adapters/cowork/build.sh --clean   # remove stage first
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ADAPTER_ROOT="$SCRIPT_DIR"
REPO_ROOT="$(cd "$ADAPTER_ROOT/../.." && pwd)"
CORE_DIR="$REPO_ROOT/core"
SRC_DIR="$ADAPTER_ROOT/plugin-src"
DIST_DIR="$ADAPTER_ROOT/dist"
STAGE_DIR="$DIST_DIR/stage"

CLEAN=false
for arg in "$@"; do
    case "$arg" in
        --clean) CLEAN=true ;;
        --help|-h) sed -n '3,15p' "$0" | sed 's/^# \?//'; exit 0 ;;
        *) echo "Unknown arg: $arg" >&2; exit 2 ;;
    esac
done

echo "[cowork build] repo root:    $REPO_ROOT"
echo "[cowork build] adapter root: $ADAPTER_ROOT"
echo "[cowork build] core dir:     $CORE_DIR"

# 1. Sanity-check core inputs exist
required=(
    "workflow.md"
    "templates/task-brief.md"
    "templates/failure-capture.md"
    "rules/01-no-secrets-in-git.md"
    "rules/02-local-context-never-committed.md"
)
for f in "${required[@]}"; do
    if [[ ! -f "$CORE_DIR/$f" ]]; then
        echo "[cowork build] FAIL: missing $CORE_DIR/$f" >&2
        exit 1
    fi
done

# 2. Reset stage
if $CLEAN || [[ -d "$STAGE_DIR" ]]; then
    rm -rf "$STAGE_DIR"
fi
mkdir -p "$STAGE_DIR"

# 3. Copy plugin-src to stage (tar preserves dotfiles)
( cd "$SRC_DIR" && tar -cf - . ) | ( cd "$STAGE_DIR" && tar -xf - )

# 4. Pull canonical references from core
WF_REFS="$STAGE_DIR/skills/gxp-workflow/references"
BRIEF_REFS="$STAGE_DIR/skills/gxp-brief/references"
FAIL_REFS="$STAGE_DIR/skills/gxp-failure-capture/references"
mkdir -p "$BRIEF_REFS" "$FAIL_REFS"

cp "$CORE_DIR/workflow.md"                                "$WF_REFS/workflow.md"
cp "$CORE_DIR/templates/task-brief.md"                    "$WF_REFS/task-brief-template.md"
cp "$CORE_DIR/templates/failure-capture.md"               "$WF_REFS/failure-capture-template.md"
cp "$CORE_DIR/rules/01-no-secrets-in-git.md"              "$WF_REFS/rule-01-no-secrets-in-git.md"
cp "$CORE_DIR/rules/02-local-context-never-committed.md"  "$WF_REFS/rule-02-local-context-never-committed.md"
cp "$CORE_DIR/templates/task-brief.md"                    "$BRIEF_REFS/task-brief-template.md"
cp "$CORE_DIR/templates/failure-capture.md"               "$FAIL_REFS/failure-capture-template.md"

# 5. Validate SKILL.md frontmatter
echo "[cowork build] validating SKILL.md frontmatter..."
python3 - "$STAGE_DIR" <<'PY'
import os, re, sys
stage = sys.argv[1]
errors = []
xml_tag = re.compile(r'<[A-Za-z][^>]*>')
for skill_dir in sorted(os.listdir(os.path.join(stage, "skills"))):
    p = os.path.join(stage, "skills", skill_dir, "SKILL.md")
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
print("  + all SKILL.md frontmatter OK")
PY

# 6. Validate plugin.json parses
python3 -c "import json,sys; json.load(open(sys.argv[1]))" "$STAGE_DIR/.claude-plugin/plugin.json"
echo "[cowork build]   + plugin.json parses"

# 7. Zip into dist/gxp.plugin (build in tempdir, atomic copy)
PLUGIN_PATH="$DIST_DIR/gxp.plugin"
TMP_ZIP="$(mktemp -t gxp-plugin-XXXXXX.zip)"
trap 'rm -f "$TMP_ZIP"' EXIT
# zip refuses to write into the empty placeholder mktemp creates; delete it first.
rm -f "$TMP_ZIP"
pushd "$STAGE_DIR" >/dev/null
zip -qr "$TMP_ZIP" . -x "*.DS_Store"
popd >/dev/null
mkdir -p "$DIST_DIR"
cp -f "$TMP_ZIP" "$PLUGIN_PATH"
SIZE=$(stat -c%s "$PLUGIN_PATH" 2>/dev/null || stat -f%z "$PLUGIN_PATH")
echo "[cowork build] wrote: $PLUGIN_PATH ($SIZE bytes)"

# 8. Tidy stage
rm -rf "$STAGE_DIR"
echo "[cowork build] done."
