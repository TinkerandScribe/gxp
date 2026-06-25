<#
.SYNOPSIS
    PowerShell-native check for the ChatGPT AI Workflow adapter against core/ methodology.

.DESCRIPTION
    Compares the ChatGPT-optimized instructions against the canonical core/ methodology.
    Supports the same flags as the Claude version for consistency.
    Includes B3 copy-install robustness (warn + exit 0 if no core/).

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

$coreCheck = Join-Path $RepoRoot "core"
if (-not (Test-Path $coreCheck)) {
    if (-not $Quiet) { Write-Host "[B3] copy-install mode detected (no core/ at $coreCheck) - warning only, exit 0" -ForegroundColor Yellow }
    exit 0
}

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

$ChatGptWorkflow = Join-Path $AdapterRoot "instructions/workflow.md"
$LastSyncedSha = $null

if (Test-Path $ChatGptWorkflow) {
    $content = Get-Content $ChatGptWorkflow -Raw
    if ($content -match "Last synced from core:\s*([0-9a-fA-F]+)") {
        $LastSyncedSha = $matches[1]
    }
}

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

$DiffCount = 0
$CriticalDiffCount = 0
$MissingCount = 0

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
    if (-not $FullDiff) {
        Log "  (use -FullDiff to see complete diff)" "Yellow"
    }
    Log ""
}

if (-not $Quiet) {
    Write-Host "`n=== ChatGPT AI Workflow Adapter - Core Sync Check (PowerShell) ===" -ForegroundColor Cyan
    Write-Host "Repo root: $RepoRoot"
    Write-Host "Core:      $CoreDir"
    Write-Host "Adapter:   $AdapterRoot`n"
}

if ($LastSyncedSha) {
    try {
        $commitsSince = git -C $RepoRoot rev-list --count "$LastSyncedSha..HEAD" -- core/ 2>$null
        if ($commitsSince -and $commitsSince -ne "0") {
            Log "NOTE   Core has advanced $commitsSince commit(s) since last recorded sync ($LastSyncedSha)" "Yellow"
        }
    } catch {}
}

foreach ($f in $CriticalFiles) {
    Compare-File $f.Core $f.Adapter $f.Label $true
}

foreach ($f in $OtherFiles) {
    Compare-File $f.Core $f.Adapter $f.Label
}

Write-Host ""
if ($DiffCount -gt 0) {
    Write-Host "Found $DiffCount difference(s) ($($CriticalDiffCount) critical)." -ForegroundColor Yellow
}
if ($MissingCount -gt 0) {
    Write-Host "Found $MissingCount missing file(s)." -ForegroundColor Yellow
}

if ($CriticalDiffCount -gt 0 -and -not $Lenient) {
    Write-Host "ACTION REQUIRED: Review and align critical differences with core/." -ForegroundColor Red
    exit 1
} elseif ($DiffCount -gt 0 -or $MissingCount -gt 0) {
    Write-Host "Some differences noted (allowed or minor)." -ForegroundColor Yellow
    exit 0
} else {
    Write-Host "Adapter is structurally aligned with core." -ForegroundColor Green
    exit 0
}