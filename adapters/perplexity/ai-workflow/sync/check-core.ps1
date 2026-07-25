<#
.SYNOPSIS
    PowerShell check for Perplexity research adapter: presence + real sync-marker staleness.
#>

param(
    [switch]$Quiet,
    [switch]$Strict,
    [int]$StaleThreshold = 3
)

$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$adapterRoot = Split-Path -Parent $scriptDir
$repoRoot = $adapterRoot
while ($repoRoot -and -not (Test-Path (Join-Path $repoRoot ".git"))) {
    $parent = Split-Path -Parent $repoRoot
    if ($parent -eq $repoRoot) { break }
    $repoRoot = $parent
}

$drift = 0
$staleFail = 0

function Test-File {
    param($rel)
    $full = Join-Path $adapterRoot $rel
    if (-not (Test-Path $full)) {
        if (-not $Quiet) { Write-Host "  MISSING: $rel" }
        $script:drift = 1
    }
}

Write-Host "Checking Perplexity adapter (presence + staleness)..."

Test-File "README.md"
Test-File "instructions/research-workflow.md"
Test-File "instructions/research-handoff.md"
Test-File "instructions/workflow.md"
Test-File "sync/check-core.ps1"
Test-File "sync/check-core.sh"

# Trust-boundary markers (research-stage adapter — must stay durable)
$ho = Join-Path $adapterRoot "instructions/research-handoff.md"
if (Test-Path $ho) {
    $hoText = Get-Content -Raw $ho
    foreach ($needle in @("Verified findings", "Inferences", "Open questions", "Explicit non-claims", "Research-stage only")) {
        if ($hoText -notlike "*$needle*") {
            if (-not $Quiet) { Write-Host "  MISSING marker in research-handoff.md: $needle" }
            $script:drift = 1
        }
    }
}
$skill = Join-Path $adapterRoot "SKILL.md"
if (Test-Path $skill) {
    $sk = Get-Content -Raw $skill
    if ($sk -notmatch "false local-verify|No false local-verify") {
        if (-not $Quiet) { Write-Host "  MISSING marker in SKILL.md: false local-verify" }
        $script:drift = 1
    }
}

$wf = Join-Path $adapterRoot "instructions/workflow.md"
$sha = $null
$status = "missing"
if (Test-Path $wf) {
    $line = (Select-String -Path $wf -Pattern "last synced from core" -SimpleMatch | Select-Object -First 1).Line
    if (-not $line) {
        $status = "missing"
    } elseif ($line -match 'Last\s+synced\s+from\s+core:(?:\*\*)?\s*([0-9a-fA-F]{7,40})') {
        $sha = $Matches[1]
        $status = "ok"
    } else {
        $status = "malformed"
    }
}

if ($status -ne "ok") {
    Write-Host "FAIL   Sync marker $status" -ForegroundColor Red
    $staleFail = 1
} else {
    $resolved = $false
    try {
        git -C $repoRoot rev-parse --verify "$sha^{commit}" 2>$null | Out-Null
        if ($LASTEXITCODE -eq 0) { $resolved = $true }
    } catch {}
    if (-not $resolved) {
        $shallow = "false"
        try { $shallow = (git -C $repoRoot rev-parse --is-shallow-repository 2>$null) } catch {}
        if ($shallow -eq "true") {
            if (-not $Quiet) { Write-Host "WARN   Sync marker SHA not in shallow history" }
        } else {
            Write-Host "FAIL   Sync marker SHA unresolvable: $sha" -ForegroundColor Red
            $staleFail = 1
        }
    } else {
        $count = git -C $repoRoot rev-list --count "$sha..HEAD" -- core/ 2>$null
        if ($count -and [int]$count -gt $StaleThreshold) {
            Write-Host "FAIL   Core advanced $count commit(s) since marker (threshold $StaleThreshold)" -ForegroundColor Red
            $staleFail = 1
        } elseif ($count -and [int]$count -gt 0) {
            if (-not $Quiet) { Write-Host "NOTE   Core advanced $count commit(s) since marker (within threshold)" }
        } else {
            if (-not $Quiet) { Write-Host "OK     Sync marker current ($sha)" }
        }
    }
}

if ($drift -eq 0 -and $staleFail -eq 0) {
    if (-not $Quiet) { Write-Host "Perplexity adapter check: PASS (presence + staleness)" }
    exit 0
}
if (-not $Quiet) { Write-Host "Perplexity adapter check: FAIL" }
exit 1
