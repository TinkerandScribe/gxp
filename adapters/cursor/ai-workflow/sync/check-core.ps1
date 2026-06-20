<#
.SYNOPSIS
    Structural drift check for the Cursor adapter against core/workflow.md.

.DESCRIPTION
    Checks that rule.mdc still contains the structural markers required for the
    current workflow version. This is NOT a text diff -- intentional compression
    is allowed and expected. Checks for required phrases only.

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File sync\check-core.ps1
#>

$ErrorActionPreference = "Stop"

$scriptDir  = Split-Path -Parent $MyInvocation.MyCommand.Path
$adapterDir = Split-Path -Parent $scriptDir
$rulePath   = Join-Path $adapterDir "rule.mdc"

$passed  = 0
$failed  = 0
$results = @()

function Test-Marker {
    param([string]$Pattern, [string]$Label)
    $content = Get-Content $rulePath -Raw
    if ($content -match $Pattern) {
        $script:results += [PSCustomObject]@{ Status = "PASS"; Label = $Label }
        $script:passed++
    } else {
        $script:results += [PSCustomObject]@{ Status = "FAIL"; Label = $Label }
        $script:failed++
    }
}

Test-Marker "L3/L4 bounded agent"       "L3/L4 bounded agent reference"
Test-Marker "4[^a-z0-9]8"              "4-8 criteria rule (hyphen or dash)"
Test-Marker "anti-loop"                 "Anti-loop phase reference"
Test-Marker "deterministic"             "Deterministic verification order"
Test-Marker "ratings\.jsonl"            "ratings.jsonl reference"
Test-Marker "handoff"                   "Handoff phase reference"
Test-Marker "v1\."                      "Version string present"
Test-Marker "PowerShell"               "PowerShell environment note"
Test-Marker "verification output"       "Verification output contract"
Test-Marker "Composer"                  "Composer usage guidance"
Test-Marker "Phase -1"                  "Capability gate section"
Test-Marker "Capability & Permission"   "Capability gate title"
Test-Marker "PROGRAM\.md"               "PROGRAM.md verification pointer"
Test-Marker "Repo-local Cursor"         "Preserve local rules note"

Write-Host ""
Write-Host "=== Cursor Adapter Drift Check ==="
Write-Host ""
foreach ($r in $results) {
    $color = if ($r.Status -eq "PASS") { "Green" } else { "Red" }
    Write-Host ("  [{0}] {1}" -f $r.Status, $r.Label) -ForegroundColor $color
}
Write-Host ""
Write-Host "  Passed: $passed  Failed: $failed"
Write-Host ""

if ($failed -gt 0) {
    Write-Host "ACTION REQUIRED: Update rule.mdc to restore missing markers." -ForegroundColor Yellow
    exit 1
} else {
    Write-Host "Adapter is structurally aligned with core." -ForegroundColor Green
    exit 0
}
