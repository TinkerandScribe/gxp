<#
.SYNOPSIS
    PowerShell-native version of check-core.sh for Windows users.
    Compares the Grok AI Workflow skill against the canonical core/ methodology.

.DESCRIPTION
    This script provides the same verification and anti-entropy functionality
    as check-core.sh but runs natively in PowerShell (no Git Bash required).

    It supports the same flags and the "last synced" marker + drift allowlist features.

.PARAMETER Quiet
    Minimal output, only summary and exit code.

.PARAMETER Strict
    Treat missing files and structural gaps as errors.

.PARAMETER Lenient
    Do not fail on diffs for critical files (good during active development).

.PARAMETER FullDiff
    Show full diffs instead of truncated ones.

.PARAMETER Help
    Show help.

.EXAMPLE
    .\check-core.ps1
    .\check-core.ps1 -Lenient
    .\check-core.ps1 -Strict -Quiet
#>

[CmdletBinding()]
param(
    [switch]$Quiet,
    [switch]$Strict,
    [switch]$Lenient,
    [switch]$FullDiff,
    [switch]$Help
)

if ($Help) {
    Get-Help $MyInvocation.MyCommand.Path -Full
    exit 0
}

# --- Path Resolution ---
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$AdapterRoot = Split-Path -Parent $ScriptDir
$RepoRoot = $AdapterRoot

# B3: copy-install robustness - if no full core/ (e.g. user copied only adapter dir), warn + exit 0 (non-fatal)
$coreCheck = Join-Path $RepoRoot "core"
if (-not (Test-Path $coreCheck)) {
    if (-not $Quiet) { Write-Host "[B3] copy-install mode detected (no core/ at $coreCheck) - warning only, exit 0" -ForegroundColor Yellow }
    exit 0
}

# Walk up to find .git
while ($RepoRoot -and -not (Test-Path (Join-Path $RepoRoot ".git"))) {
    $parent = Split-Path -Parent $RepoRoot
    if ($parent -eq $RepoRoot) { break }
    $RepoRoot = $parent
}

$CoreDir = Join-Path $RepoRoot "core"

if (-not (Test-Path $CoreDir)) {
    Write-Error "Could not locate core/ directory at $CoreDir"
    exit 1
}

# --- Colors ---
function Write-Colored {
    param($Text, $Color = "White")
    if ($Host.UI.SupportsVirtualTerminal) {
        $colors = @{
            "Green"  = "`e[32m"
            "Red"    = "`e[31m"
            "Yellow" = "`e[33m"
            "Bold"   = "`e[1m"
            "Reset"  = "`e[0m"
        }
        Write-Host ($colors[$Color] + $Text + $colors["Reset"]) -NoNewline
    } else {
        Write-Host $Text -ForegroundColor $Color -NoNewline
    }
}

function Log { param($Text, $Color = "White"); if (-not $Quiet) { Write-Colored "$Text`n" $Color } }

# --- Configuration ---
$CriticalFiles = @(
    @{ Core = "workflow.md"; Adapter = "instructions/workflow.md"; Label = "Workflow Definition" }
)

$OtherFiles = @(
    @{ Core = "templates/task-brief.md";     Adapter = "templates/task-brief.md";     Label = "Task Brief Template" },
    @{ Core = "templates/failure-capture.md";Adapter = "templates/failure-capture.md";Label = "Failure Capture Template" },
    @{ Core = "templates/weekly-refine.md";  Adapter = "templates/weekly-refine.md";  Label = "Weekly Refine Template" },
    @{ Core = "PROGRAM.template.md";         Adapter = "PROGRAM.template.md";         Label = "PROGRAM Template" },
    @{ Core = "ratings.jsonl";               Adapter = "ratings.jsonl";               Label = "Ratings Schema" },
    @{ Core = "rules/README.md";             Adapter = "rules/README.md";             Label = "Rules Philosophy" },
    @{ Core = "failures/README.md";          Adapter = "failures/README.md";          Label = "Failures Philosophy" }
)

# --- Last Synced Marker ---
$GrokWorkflow = Join-Path $AdapterRoot "instructions/workflow.md"
$LastSyncedSha = $null

if (Test-Path $GrokWorkflow) {
    $content = Get-Content $GrokWorkflow -Raw
    if ($content -match "Last synced from core:\s*([0-9a-fA-F]+)") {
        $LastSyncedSha = $matches[1]
    }
}

# --- Drift Allowlist ---
$AllowlistFile = Join-Path $AdapterRoot "sync/drift-allowlist.txt"
$Allowlist = @()

if (Test-Path $AllowlistFile) {
    Get-Content $AllowlistFile | ForEach-Object {
        $line = ($_ -split '#')[0].Trim()
        if ($line) { $Allowlist += $line }
    }
}

function Is-Allowed($label) {
    foreach ($pattern in $Allowlist) {
        if ($label -like "*$pattern*") { return $true }
    }
    return $false
}

# --- Comparison ---
$DiffCount = 0
$CriticalDiffCount = 0
$MissingCount = 0
$Warnings = @()

function Compare-File {
    param($CoreRel, $AdapterRel, $Label, $Required = $false)

    $coreFile = Join-Path $CoreDir $CoreRel
    $adapterFile = Join-Path $AdapterRoot $AdapterRel

    if (-not (Test-Path $coreFile)) {
        Log "SKIP   $Label (missing in core)" "Yellow"
        return
    }

    if (-not (Test-Path $adapterFile)) {
        if (Is-Allowed $Label) {
            Log "ALLOW  $Label (intentionally not present per drift-allowlist.txt)" "Yellow"
            return
        }
        if ($Required -or $Strict) {
            Log "MISSING $Label" "Red"
            $script:MissingCount++
        } else {
            Log "NOTE   $Label (not present in adapter - may be intentional)" "Yellow"
        }
        return
    }

    $coreContent = Get-Content $coreFile -Raw -ErrorAction SilentlyContinue
    $adapterContent = Get-Content $adapterFile -Raw -ErrorAction SilentlyContinue

    if ($coreContent -eq $adapterContent) {
        Log "OK     $Label" "Green"
        return
    }

    if (Is-Allowed $Label) {
        Log "ALLOW  $Label (intentionally diverged per drift-allowlist.txt)" "Yellow"
        return
    }

    $script:DiffCount++
    $isCritical = $CriticalFiles | Where-Object { $_.Label -eq $Label }
    if ($isCritical) { $script:CriticalDiffCount++ }

    Log "DIFF   $Label" "Red"

    # Better diff output
    $coreLines = $coreContent -split "`r?`n"
    $adapterLines = $adapterContent -split "`r?`n"

    if ($FullDiff) {
        Log "  --- core/$CoreRel"
        Log "  +++ adapter/$AdapterRel"
        $maxLines = [Math]::Max($coreLines.Count, $adapterLines.Count)
        for ($i = 0; $i -lt $maxLines -and $i -lt 80; $i++) {
            $c = if ($i -lt $coreLines.Count) { $coreLines[$i] } else { "" }
            $a = if ($i -lt $adapterLines.Count) { $adapterLines[$i] } else { "" }
            if ($c -ne $a) {
                if ($c) { Log "  - $c" "Red" }
                if ($a) { Log "  + $a" "Green" }
            } else {
                Log "    $c"
            }
        }
        if ($maxLines -gt 80) { Log "  ... (truncated)" "Yellow" }
    } else {
        # Show first few differing lines
        $shown = 0
        for ($i = 0; $i -lt $coreLines.Count -and $shown -lt 8; $i++) {
            $c = $coreLines[$i]
            $a = if ($i -lt $adapterLines.Count) { $adapterLines[$i] } else { "" }
            if ($c -ne $a) {
                Log "  - $c" "Red"
                if ($a) { Log "  + $a" "Green" }
                $shown++
            }
        }
        Log "  (use -FullDiff to see complete diff)" "Yellow"
    }
    Log ""
}

# --- Main Execution ---
if (-not $Quiet) {
    Write-Host "`n=== Grok AI Workflow — Core Sync Check (PowerShell) ===" -ForegroundColor Cyan
    Write-Host "Repo root: $RepoRoot"
    Write-Host "Core:      $CoreDir"
    Write-Host "Adapter:   $AdapterRoot`n"
}

# Last synced note
if ($LastSyncedSha) {
    try {
        $commitsSince = git -C $RepoRoot rev-list --count "$LastSyncedSha..HEAD" -- core/ 2>$null
        if ($commitsSince -and $commitsSince -ne "0") {
            Log "NOTE   Core has advanced $commitsSince commit(s) since last recorded sync ($LastSyncedSha)" "Yellow"
        }
    } catch {}
}

# Critical
Write-Host "`n=== Critical Methodology ===" -ForegroundColor Cyan
foreach ($item in $CriticalFiles) {
    Compare-File $item.Core $item.Adapter $item.Label $true
}

# Templates + Philosophy
Write-Host "`n=== Templates and Philosophy ===" -ForegroundColor Cyan
foreach ($item in $OtherFiles) {
    Compare-File $item.Core $item.Adapter $item.Label $false
}

# SKILL integrity
Write-Host "`n=== Grok Skill Integrity ===" -ForegroundColor Cyan
$skillFile = Join-Path $AdapterRoot "SKILL.md"
if (Test-Path $skillFile) {
    if (Select-String -Path $skillFile -Pattern "check-core" -Quiet) {
        Log "OK     SKILL.md contains sync instruction" "Green"
    } else {
        Log "WARN   SKILL.md is missing reference to check-core" "Yellow"
        $Warnings += "SKILL.md should instruct users to run the sync check"
    }
} else {
    Log "MISSING SKILL.md" "Red"
    $MissingCount++
}

# Summary
Write-Host "`n=== Summary ===" -ForegroundColor Cyan

$exitCode = 0

if ($CriticalDiffCount -gt 0) {
    if ($Lenient) {
        Log "! $CriticalDiffCount critical file(s) differ (lenient mode)" "Yellow"
    } else {
        Log "✗ $CriticalDiffCount critical file(s) differ from core." "Red"
        $exitCode = 1
    }
}

if ($DiffCount -gt $CriticalDiffCount) {
    Log "✗ $($DiffCount - $CriticalDiffCount) non-critical file(s) differ from core." "Red"
}

if ($MissingCount -gt 0) {
    if ($Strict) {
        Log "✗ $MissingCount required file(s) missing from adapter." "Red"
        $exitCode = 1
    } else {
        Log "✗ $MissingCount file(s) missing (use -Strict to fail on these)." "Yellow"
    }
}

if ($DiffCount -eq 0 -and $MissingCount -eq 0 -and $CriticalDiffCount -eq 0) {
    Log "✓ All checked items are in sync with core (or explicitly allowed)." "Green"
    $exitCode = 0
}

if ($Warnings.Count -gt 0) {
    foreach ($w in $Warnings) { Log "! $w" "Yellow" }
}

Write-Host "`nRun with -Lenient during active development of the Grok adapter."
Write-Host "Run with -Strict before important work for maximum enforcement."

exit $exitCode
