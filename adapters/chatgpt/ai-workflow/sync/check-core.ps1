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

while ($RepoRoot -and -not (Test-Path (Join-Path $RepoRoot ".git"))) {
    $parent = Split-Path -Parent $RepoRoot
    if ($parent -eq $RepoRoot) { break }
    $RepoRoot = $parent
}

$CoreDir = Join-Path $RepoRoot "core"

# B3: copy-install robustness - if no core/ at the resolved root (e.g. user copied
# only the adapter dir), warn + exit 0 (non-fatal)
if (-not (Test-Path $CoreDir)) {
    if (-not $Quiet) { Write-Host "[B3] copy-install mode detected (no core/ at $CoreDir) - warning only, exit 0" -ForegroundColor Yellow }
    exit 0
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
        $line = (($_ -split '#')[0] -replace "`r", '').Trim()
        if ($line) { $Allowlist += $line }
    }
}

function Is-Allowed($label) {
    foreach ($pattern in $Allowlist) {
        if ($label -like "*$pattern*") { return $true }
    }
    return $false
}

# --- Workflow structural floor (intentional rewrites; not whole-file allowlist) ---
$script:StructureFailCount = 0

function Test-WorkflowMarker {
    param($File, $Pattern, $Label)
    if (Select-String -Path $File -Pattern $Pattern -Quiet) {
        Log "PASS   $Label" "Green"
    } else {
        Log "FAIL   $Label (marker not found)" "Red"
        $script:StructureFailCount++
    }
}


# --- Staleness marker (real SHA; bold markdown tolerant) ---
$script:StaleFailCount = 0
$script:StaleThreshold = if ($env:GXP_STALE_THRESHOLD) { [int]$env:GXP_STALE_THRESHOLD } else { 3 }

function Test-SyncMarker {
    param($WorkflowPath)
    if (-not (Test-Path $WorkflowPath)) {
        Log "FAIL   Sync marker missing (no workflow file)" "Red"
        $script:StaleFailCount++
        return
    }
    $hit = Select-String -Path $WorkflowPath -Pattern "last synced from core" | Select-Object -First 1
    if (-not $hit) {
        Log "FAIL   Sync marker missing" "Red"
        $script:StaleFailCount++
        return
    }
    $line = $hit.Line
    if ($line -notmatch 'Last\s+synced\s+from\s+core:(?:\*\*)?\s*([0-9a-fA-F]{7,40})') {
        Log "FAIL   Sync marker malformed (need real hex SHA)" "Red"
        $script:StaleFailCount++
        return
    }
    $sha = $Matches[1]
    $resolved = $false
    try {
        git -C $RepoRoot rev-parse --verify ($sha + '^{commit}') 2>$null | Out-Null
        if ($LASTEXITCODE -eq 0) { $resolved = $true }
    } catch {}
    if (-not $resolved) {
        $shallow = "false"
        try { $shallow = (git -C $RepoRoot rev-parse --is-shallow-repository 2>$null) } catch {}
        if ($shallow -eq "true") {
            Log "WARN   Sync marker SHA not in shallow history" "Yellow"
            return
        }
        Log "FAIL   Sync marker SHA unresolvable: $sha" "Red"
        $script:StaleFailCount++
        return
    }
    $count = git -C $RepoRoot rev-list --count ($sha + '..HEAD') -- core/ 2>$null
    if ($count -and [int]$count -gt $script:StaleThreshold) {
        Log "FAIL   Core advanced $count commit(s) since marker (threshold $($script:StaleThreshold))" "Red"
        $script:StaleFailCount++
        return
    }
    if ($count -and [int]$count -gt 0) {
        Log "NOTE   Core advanced $count commit(s) since marker (within threshold)" "Yellow"
    } else {
        Log "OK     Sync marker current ($sha)" "Green"
    }
}


function Test-WorkflowStructure {
    param($WorkflowPath)
    if (-not (Test-Path $WorkflowPath)) {
        Log "MISSING instructions/workflow.md" "Red"
        $script:StructureFailCount++
        return
    }
    if (-not $Quiet) { Write-Host "=== Workflow structural floor ===" -ForegroundColor Cyan }
    foreach ($n in 0..8) {
        Test-WorkflowMarker $WorkflowPath "Phase\s+$n([^0-9]|$)" "Phase $n present"
    }
    Test-WorkflowMarker $WorkflowPath "4[^a-zA-Z0-9]+8" "4-8 binary criteria rule"
    Test-WorkflowMarker $WorkflowPath "anti[- ]?loop" "Anti-loop rule"
    Test-WorkflowMarker $WorkflowPath "deterministic" "Deterministic-first verification"
    Test-WorkflowMarker $WorkflowPath "criteria_met" "Ratings field criteria_met"
    Test-WorkflowMarker $WorkflowPath "criteria_total" "Ratings field criteria_total"
    Test-WorkflowMarker $WorkflowPath '`ts`' "Ratings field ts"
    Test-WorkflowMarker $WorkflowPath '`rating`' "Ratings field rating"
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

    # Present files are byte-compared; allowlist only covers intentional absence.
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

# Critical workflow: structural floor (not whole-file allowlist)
Test-SyncMarker (Join-Path $AdapterRoot "instructions/workflow.md")
Test-WorkflowStructure (Join-Path $AdapterRoot "instructions/workflow.md")

foreach ($f in $OtherFiles) {
    Compare-File $f.Core $f.Adapter $f.Label
}

Write-Host ""
if ($script:StaleFailCount -gt 0) {
    if ($Lenient) {
        Log "! Sync marker stale or invalid (lenient mode)" "Yellow"
    } else {
        Log "x Sync marker stale or invalid." "Red"
        $exitCode = 1
    }
}

if ($script:StructureFailCount -gt 0) {
    Write-Host "Found $($script:StructureFailCount) workflow structural failure(s)." -ForegroundColor Yellow
}
if ($DiffCount -gt 0) {
    Write-Host "Found $DiffCount difference(s) ($($CriticalDiffCount) critical)." -ForegroundColor Yellow
}
if ($MissingCount -gt 0) {
    Write-Host "Found $MissingCount missing file(s)." -ForegroundColor Yellow
}

if (($script:StructureFailCount -gt 0 -or $script:StaleFailCount -gt 0 -or $CriticalDiffCount -gt 0) -and -not $Lenient) {
    Write-Host "ACTION REQUIRED: Fix workflow structural floor and/or critical diffs." -ForegroundColor Red
    exit 1
} elseif ($script:StructureFailCount -gt 0 -or $script:StaleFailCount -gt 0 -or $DiffCount -gt 0 -or $MissingCount -gt 0) {
    Write-Host "Some differences noted (allowed or minor)." -ForegroundColor Yellow
    exit 0
} else {
    Write-Host "Adapter is structurally aligned with core." -ForegroundColor Green
    exit 0
}
