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

.PARAMETER DryRun
    Print what would happen without writing files.

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
    [switch]$DryRun,
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

if (-not (Test-Path -LiteralPath $TargetRepo)) {
    if ($DryRun) {
        # Preview only — do not create the missing target.
        $targetAbs = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($TargetRepo)
    } else {
        Write-Error "Target directory does not exist: $TargetRepo"
        exit 1
    }
} else {
    $targetAbs = (Resolve-Path -LiteralPath $TargetRepo).Path
}
$aiDir     = Join-Path $targetAbs ".ai"

$created = 0
$updated = 0
$skipped = 0

function Ensure-Dir([string]$path) {
    if ($DryRun) { return }
    if (-not (Test-Path $path)) { New-Item -ItemType Directory -Path $path | Out-Null }
}

function Copy-Scaffold {
    param([string]$Src, [string]$Dest, [switch]$Preserve)
    $rel = $Dest.Replace($targetAbs + "\", "").Replace($targetAbs + "/", "")
    if ($DryRun) {
        if (Test-Path $Dest) {
            if ($Preserve) { Write-Host "  - $rel (would preserve)"; $script:skipped++; return }
            if ($Force) {
                if ((Test-Path $Src) -and (Get-FileHash $Src).Hash -eq (Get-FileHash $Dest).Hash) {
                    Write-Host "  - $rel (would skip unchanged)"; $script:skipped++
                } else { Write-Host "  ~ $rel (would update)"; $script:updated++ }
                return
            }
            Write-Host "  - $rel (would skip exists)"; $script:skipped++; return
        }
        Write-Host "  + $rel (would create)"; $script:created++; return
    }
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
    $rel = $path.Replace($targetAbs + "\", "").Replace($targetAbs + "/", "")
    $keep = Join-Path $path ".gitkeep"
    if ($DryRun) {
        if (-not (Test-Path $keep)) {
            Write-Host "  + $rel/.gitkeep (would create)"
            $script:created++
        }
        return
    }
    Ensure-Dir $path
    if (-not (Test-Path $keep)) {
        New-Item -ItemType File -Path $keep -Force | Out-Null
        Write-Host "  + $rel/.gitkeep"
        $script:created++
    }
}

function Copy-TreeScaffold([string]$SrcDir, [string]$DestDir) {
    if (-not (Test-Path $SrcDir)) { return }
    Ensure-Dir $DestDir
    Get-ChildItem -LiteralPath $SrcDir -Recurse -File | ForEach-Object {
        $rel = $_.FullName.Substring($SrcDir.Length).TrimStart('\', '/')
        Copy-Scaffold $_.FullName (Join-Path $DestDir $rel)
    }
}

Write-Host "Installing .ai scaffold from core/"
Write-Host "  target: $targetAbs"
if ($Force) { Write-Host "  mode:   force (overwrite changed templates)" }
if ($DryRun) { Write-Host "  mode:   dry-run (no writes)" }
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

Copy-TreeScaffold (Join-Path $coreDir "templates") (Join-Path $aiDir "templates")
Copy-TreeScaffold (Join-Path $coreDir "docs") (Join-Path $aiDir "docs")

if ($IncludeCursorRule) {
    $ruleSrc = Join-Path $repoRoot "adapters\cursor\ai-workflow\rule.mdc"
    $cursorInstaller = Join-Path $repoRoot "adapters\cursor\ai-workflow\sync\install-cursor-rule.ps1"
    if ($DryRun) {
        # install-cursor-rule.ps1 has no -DryRun; preview via Copy-Scaffold only.
        if (Test-Path $ruleSrc) {
            Write-Host ""
            Write-Host "Installing Cursor rule..."
            Copy-Scaffold $ruleSrc (Join-Path $targetAbs ".cursor\rules\ai-workflow.mdc")
        }
    } elseif (Test-Path $cursorInstaller) {
        Write-Host ""
        Write-Host "Installing Cursor rule..."
        & $cursorInstaller -TargetRepo $targetAbs -Force:$Force
    } elseif (Test-Path $ruleSrc) {
        Write-Host ""
        Write-Host "Installing Cursor rule..."
        Copy-Scaffold $ruleSrc (Join-Path $targetAbs ".cursor\rules\ai-workflow.mdc")
    }
}

# Suggest .ai/tmp/ in gitignore
$gitignore = Join-Path $targetAbs ".gitignore"
if ((-not $DryRun) -and (Test-Path $gitignore)) {
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
