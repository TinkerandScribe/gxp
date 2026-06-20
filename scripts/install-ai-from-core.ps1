<#
.SYNOPSIS
    Installs the .ai workflow scaffold from the GXP core/ into a target repo.

.DESCRIPTION
    Copies core/ into a target repo as the portable .ai/ layout.
    By default creates missing files only. With -Force, overwrites template
    files when content differs. Always preserves .ai/PROGRAM.md and
    .ai/ratings.jsonl if they already exist.

.PARAMETER TargetRepo
    Target repository root. Defaults to current directory.

.PARAMETER Force
    Overwrite existing scaffold template files (not PROGRAM.md or ratings body).

.PARAMETER IncludeCursorRule
    Also install adapters/cursor/ai-workflow/rule.mdc to .cursor/rules/

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File scripts/install-ai-from-core.ps1 -TargetRepo C:\repos\my-app

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File scripts/install-ai-from-core.ps1 -Force -IncludeCursorRule
#>

param(
    [string]$TargetRepo = (Get-Location).Path,
    [switch]$Force,
    [switch]$IncludeCursorRule
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot  = Split-Path -Parent $scriptDir
$coreDir   = Join-Path $repoRoot "core"

if (-not (Test-Path $coreDir)) {
    Write-Error "Cannot find core/ at $coreDir (run from the GXP repo)"
    exit 1
}

$targetAbs = (Resolve-Path $TargetRepo).Path
$aiDir     = Join-Path $targetAbs ".ai"

$created = 0
$updated = 0
$skipped = 0

function Ensure-Dir([string]$path) {
    if (-not (Test-Path $path)) { New-Item -ItemType Directory -Path $path | Out-Null }
}

function Copy-Scaffold {
    param([string]$Src, [string]$Dest, [switch]$Preserve)
    $rel = $Dest.Replace($targetAbs + "\", "").Replace($targetAbs + "/", "")
    Ensure-Dir (Split-Path -Parent $Dest)
    if (Test-Path $Dest) {
        if ($Preserve) {
            Write-Host "  - $rel (user file, preserved)"
            $script:skipped++
            return
        }
        if ($Force) {
            if ((Get-FileHash $Src).Hash -eq (Get-FileHash $Dest).Hash) {
                Write-Host "  - $rel (unchanged)"
                $script:skipped++
            } else {
                Copy-Item $Src $Dest -Force
                Write-Host "  ~ $rel"
                $script:updated++
            }
            return
        }
        Write-Host "  - $rel (exists)"
        $script:skipped++
        return
    }
    Copy-Item $Src $Dest -Force
    Write-Host "  + $rel"
    $script:created++
}

function Ensure-EmptyDir([string]$path) {
    Ensure-Dir $path
    $rel = $path.Replace($targetAbs + "\", "")
    $keep = Join-Path $path ".gitkeep"
    if (-not (Test-Path $path)) {
        Write-Host "  + $rel/"
        $script:created++
    }
    if (-not (Test-Path $keep)) {
        New-Item -ItemType File -Path $keep -Force | Out-Null
        Write-Host "  + $rel/.gitkeep"
        $script:created++
    }
}

Write-Host "Installing .ai scaffold from core/"
Write-Host "  target: $targetAbs"
if ($Force) { Write-Host "  mode:   force (overwrite changed templates)" }
Write-Host ""

Ensure-Dir $aiDir

Copy-Scaffold (Join-Path $coreDir "PROGRAM.template.md") (Join-Path $aiDir "PROGRAM.md") -Preserve
Copy-Scaffold (Join-Path $coreDir "workflow.md") (Join-Path $aiDir "workflow.md")
Copy-Scaffold (Join-Path $coreDir "routing.md") (Join-Path $aiDir "routing.md")
Copy-Scaffold (Join-Path $coreDir "ratings.jsonl") (Join-Path $aiDir "ratings.jsonl") -Preserve

foreach ($sub in @("rules", "failures", "wiki", "evals")) {
    $subCore = Join-Path $coreDir $sub
    $subAi   = Join-Path $aiDir $sub
    if (-not (Test-Path $subCore)) { continue }
    Ensure-Dir $subAi
    Get-ChildItem $subCore -File | ForEach-Object {
        Copy-Scaffold $_.FullName (Join-Path $subAi $_.Name)
    }
}

Ensure-EmptyDir (Join-Path $aiDir "evals\golden")
Ensure-EmptyDir (Join-Path $aiDir "evals\regressions")
Ensure-EmptyDir (Join-Path $aiDir "evals\canaries")

$tplDir = Join-Path $coreDir "templates"
if (Test-Path $tplDir) {
    $aiTpl = Join-Path $aiDir "templates"
    Ensure-Dir $aiTpl
    Get-ChildItem $tplDir -File | ForEach-Object {
        Copy-Scaffold $_.FullName (Join-Path $aiTpl $_.Name)
    }
}

if ($IncludeCursorRule) {
    $cursorInstaller = Join-Path $repoRoot "adapters\cursor\ai-workflow\sync\install-cursor-rule.ps1"
    if (Test-Path $cursorInstaller) {
        Write-Host ""
        Write-Host "Installing Cursor rule..."
        $cursorArgs = @("-TargetRepo", $targetAbs)
        if ($Force) { $cursorArgs += "-Force" }
        & $cursorInstaller @cursorArgs
    }
}

# Suggest .ai/tmp/ in gitignore
$gitignore = Join-Path $targetAbs ".gitignore"
if (Test-Path $gitignore) {
    $gi = Get-Content $gitignore -Raw
    if ($gi -notmatch '\.ai/tmp') {
        Write-Host ""
        Write-Host "Tip: add '.ai/tmp/' to .gitignore for ephemeral audit artifacts (optional)."
    }
}

Write-Host ""
Write-Host "Summary: created=$created updated=$updated skipped=$skipped"
Write-Host ""
Write-Host "Next steps:"
Write-Host "  1. Edit .ai/PROGRAM.md with verification commands."
Write-Host "  2. Optional: install-cursor-rule.ps1 -IncludeSecurityTemplate"
Write-Host "  3. Paste core/docs/root-addenda into AGENTS.md / CLAUDE.md if desired."
Write-Host ""
