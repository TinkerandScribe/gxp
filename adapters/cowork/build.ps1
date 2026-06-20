# build.ps1 — assemble adapters/cowork/dist/gxp.plugin from plugin-src/ + core/.
#
# Source-of-truth model: option (a).
#   - plugin-src/ contains only adapter-authored content (SKILL.md, plugin.json,
#     plugin README, ratings-schema.md, rules-summary.md).
#   - This script copies the canonical workflow + templates + rules from core/
#     into each skill's references/ folder, then zips into dist/gxp.plugin.
#
# Usage:
#   powershell -NoProfile -ExecutionPolicy Bypass -File adapters/cowork/build.ps1
#   powershell -NoProfile -ExecutionPolicy Bypass -File adapters/cowork/build.ps1 -Clean

[CmdletBinding()]
param(
    [switch]$Clean
)

$ErrorActionPreference = 'Stop'

$ScriptDir   = $PSScriptRoot
$AdapterRoot = $ScriptDir
$RepoRoot    = Resolve-Path (Join-Path $AdapterRoot '..\..') | Select-Object -ExpandProperty Path
$CoreDir     = Join-Path $RepoRoot 'core'
$SrcDir      = Join-Path $AdapterRoot 'plugin-src'
$DistDir     = Join-Path $AdapterRoot 'dist'
$StageDir    = Join-Path $DistDir   'stage'

Write-Host "[cowork build] repo root:    $RepoRoot"
Write-Host "[cowork build] adapter root: $AdapterRoot"
Write-Host "[cowork build] core dir:     $CoreDir"

# --- 1. Sanity-check core/ inputs exist ---------------------------------------
$requiredCore = @(
    'workflow.md',
    'templates\task-brief.md',
    'templates\failure-capture.md',
    'rules\01-no-secrets-in-git.md',
    'rules\02-local-context-never-committed.md'
)
foreach ($f in $requiredCore) {
    $p = Join-Path $CoreDir $f
    if (-not (Test-Path $p)) { throw "[cowork build] missing $p" }
}

# --- 2. Reset dist/ ------------------------------------------------------------
if ($Clean -or (Test-Path $StageDir)) {
    Remove-Item -Recurse -Force $StageDir -ErrorAction SilentlyContinue
}
New-Item -ItemType Directory -Force -Path $StageDir | Out-Null

# --- 3. Copy plugin-src/ to stage ---------------------------------------------
Copy-Item -Recurse -Force -Path (Join-Path $SrcDir '*') -Destination $StageDir
# robocopy alternative if needed, but Copy-Item -Recurse is fine for this size.
# Manually ensure .claude-plugin gets copied (Copy-Item -Recurse handles it).

# --- 4. Pull canonical references from core/ ----------------------------------
$WfRefs    = Join-Path $StageDir 'skills\gxp-workflow\references'
$BriefRefs = Join-Path $StageDir 'skills\gxp-brief\references'
$FailRefs  = Join-Path $StageDir 'skills\gxp-failure-capture\references'
New-Item -ItemType Directory -Force -Path $BriefRefs,$FailRefs | Out-Null

Copy-Item (Join-Path $CoreDir 'workflow.md')                                 (Join-Path $WfRefs 'workflow.md') -Force
Copy-Item (Join-Path $CoreDir 'templates\task-brief.md')                     (Join-Path $WfRefs 'task-brief-template.md') -Force
Copy-Item (Join-Path $CoreDir 'templates\failure-capture.md')                (Join-Path $WfRefs 'failure-capture-template.md') -Force
Copy-Item (Join-Path $CoreDir 'rules\01-no-secrets-in-git.md')               (Join-Path $WfRefs 'rule-01-no-secrets-in-git.md') -Force
Copy-Item (Join-Path $CoreDir 'rules\02-local-context-never-committed.md')   (Join-Path $WfRefs 'rule-02-local-context-never-committed.md') -Force

Copy-Item (Join-Path $CoreDir 'templates\task-brief.md')                     (Join-Path $BriefRefs 'task-brief-template.md') -Force
Copy-Item (Join-Path $CoreDir 'templates\failure-capture.md')                (Join-Path $FailRefs 'failure-capture-template.md') -Force

# --- 5. Validate SKILL.md frontmatter -----------------------------------------
Write-Host "[cowork build] validating SKILL.md frontmatter..."
$validator = @'
import json, os, re, sys
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
'@
$tmpValidator = Join-Path $env:TEMP "cowork-validate-$([guid]::NewGuid().ToString()).py"
Set-Content -Path $tmpValidator -Value $validator -Encoding UTF8
try {
    & python $tmpValidator $StageDir
    if ($LASTEXITCODE -ne 0) { throw "frontmatter validation failed" }
} finally {
    Remove-Item -Force $tmpValidator -ErrorAction SilentlyContinue
}

# --- 6. Validate plugin.json --------------------------------------------------
& python -c "import json,sys; json.load(open(sys.argv[1]))" (Join-Path $StageDir '.claude-plugin\plugin.json')
if ($LASTEXITCODE -ne 0) { throw "plugin.json failed JSON validation" }
Write-Host "[cowork build]   + plugin.json parses"

# --- 7. Zip into dist/gxp.plugin ----------------------------------------------
# Build the zip in a tempdir, then copy over the final location. Compress-Archive's
# in-place overwrite can fail in restricted environments (sandboxed mounts, etc.);
# building elsewhere + a single overwrite is portable.
$PluginPath = Join-Path $DistDir 'gxp.plugin'
$TmpZip = Join-Path $env:TEMP ("gxp-plugin-" + [guid]::NewGuid().ToString() + ".zip")
try {
    Compress-Archive -Path (Join-Path $StageDir '*') -DestinationPath $TmpZip -Force
    if (-not (Test-Path $DistDir)) { New-Item -ItemType Directory -Force -Path $DistDir | Out-Null }
    Copy-Item -Force $TmpZip $PluginPath
} finally {
    if (Test-Path $TmpZip) { Remove-Item -Force $TmpZip }
}
$size = (Get-Item $PluginPath).Length
Write-Host "[cowork build] wrote: $PluginPath ($size bytes)"

# --- 8. Tidy stage/ -----------------------------------------------------------
Remove-Item -Recurse -Force $StageDir

Write-Host "[cowork build] done."
