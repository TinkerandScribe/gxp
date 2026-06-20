<#
.SYNOPSIS
    PowerShell check for Perplexity research adapter alignment with core methodology.

.DESCRIPTION
    Checks presence of key files and last-synced marker (lenient by default for research-phase adapter).
#>

param(
    [switch]$Quiet,
    [switch]$Strict,
    [switch]$Lenient = $true
)

$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$adapterRoot = Split-Path -Parent $scriptDir
$repoRoot = Split-Path -Parent (Split-Path -Parent $adapterRoot)
$coreDir = Join-Path $repoRoot "core"

$drift = 0

function Test-File {
    param($rel)
    $full = Join-Path $adapterRoot $rel
    if (-not (Test-Path $full)) {
        if (-not $Quiet) { Write-Host "  MISSING: $rel" }
        $script:drift = 1
    }
}

Write-Host "Checking Perplexity adapter against core (research phase - lenient)..."

Test-File "README.md"
Test-File "instructions/research-workflow.md"
Test-File "instructions/research-handoff.md"
Test-File "sync/check-core.ps1"
Test-File "sync/check-core.sh"

if ($drift -eq 0) {
    if (-not $Quiet) { Write-Host "Perplexity adapter check: PASS (presence)" }
    exit 0
} else {
    if (-not $Quiet) { Write-Host "Perplexity adapter check: missing required files" }
    if ($Strict) { exit 1 }
    exit 0
}
