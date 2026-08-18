<#
.SYNOPSIS
    Lightweight presence + integrity check for the Grok Bot adapter.

.DESCRIPTION
    Windows-friendly wrapper. Prefer the bash twin when available
    (Git Bash / WSL); this script mirrors the same required-file and
    Bot constraint checks without a full workflow.md diff.

.EXAMPLE
    .\sync\check-core.ps1
#>

[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$AdapterRoot = Split-Path -Parent $PSScriptRoot
$RepoRoot = (Resolve-Path (Join-Path $AdapterRoot "..\..")).Path
$CoreDir = Join-Path $RepoRoot "core"
$fail = 0

function Require-Path {
    param([string]$Path, [string]$Label = $Path)
    if (-not (Test-Path -LiteralPath $Path)) {
        Write-Host ("  MISSING: " + $Label) -ForegroundColor Red
        $script:fail = 1
    } else {
        Write-Host ("  OK     " + $Label)
    }
}

function Require-Marker {
    param([string]$Path, [string]$Marker)
    $found = $false
    if (Test-Path -LiteralPath $Path) {
        $found = Select-String -Path $Path -SimpleMatch -Pattern $Marker -Quiet
    }
    if (-not $found) {
        Write-Host ("  MISSING MARKER in " + $Path + " : " + $Marker) -ForegroundColor Red
        $script:fail = 1
    } else {
        Write-Host ("  OK     marker: " + $Marker)
    }
}

Write-Host "=== Grok Bot adapter - Core Sync Check (PowerShell) ==="
Write-Host ("Repo root: " + $RepoRoot)
Write-Host ("Adapter:   " + $AdapterRoot)
Write-Host ""

Write-Host "1. Core methodology present"
Require-Path (Join-Path $CoreDir "workflow.md") "core/workflow.md"
Require-Path (Join-Path $CoreDir "templates\task-brief.md") "core/templates/task-brief.md"
Write-Host ""

Write-Host "2. Required adapter files"
$required = @(
    "SKILL.md",
    "README.md",
    "GETTING_STARTED.md",
    "instructions\cursor-handoff.md",
    "sync\drift-allowlist.txt"
)
foreach ($rel in $required) {
    Require-Path (Join-Path $AdapterRoot $rel) $rel
}
Write-Host ""

Write-Host "3. SKILL.md integrity"
Require-Marker (Join-Path $AdapterRoot "SKILL.md") "name: gxp-bot"
$skillPath = Join-Path $AdapterRoot "SKILL.md"
if (Test-Path -LiteralPath $skillPath) {
    $skill = Get-Content -LiteralPath $skillPath -Raw
    if ($skill -match '(?m)^name:\s*gxp\s*$') {
        Write-Host "  FAIL   SKILL.md name must not be bare 'gxp'" -ForegroundColor Red
        $fail = 1
    } else {
        Write-Host "  OK     SKILL.md does not use bare chat name 'gxp'"
    }
    if ($skill -match '(?m)^name:\s*gxp-build\s*$') {
        Write-Host "  FAIL   SKILL.md name must not be 'gxp-build'" -ForegroundColor Red
        $fail = 1
    } else {
        Write-Host "  OK     SKILL.md does not use Build name 'gxp-build'"
    }
}
Write-Host ""

Write-Host "4. Grok Bot constraint markers"
Require-Marker (Join-Path $AdapterRoot "SKILL.md") "Never clone"
Require-Marker (Join-Path $AdapterRoot "SKILL.md") "Never edit repos"
Require-Marker (Join-Path $AdapterRoot "SKILL.md") "widgets"
Require-Marker (Join-Path $AdapterRoot "SKILL.md") "cursor-agent"
Require-Marker (Join-Path $AdapterRoot "SKILL.md") "Cursor cloud agent"
Require-Marker (Join-Path $AdapterRoot "README.md") "thin"
Require-Marker (Join-Path $AdapterRoot "README.md") "local CLI"
Require-Marker (Join-Path $AdapterRoot "GETTING_STARTED.md") "widget"
Require-Marker (Join-Path $AdapterRoot "instructions\cursor-handoff.md") "Ideal State Criteria"
Require-Marker (Join-Path $AdapterRoot "instructions\cursor-handoff.md") "cursor-agent"
Write-Host ""

Write-Host "5. Must not outsource verify to the operator"
Require-Marker (Join-Path $AdapterRoot "SKILL.md") "Never tell the operator to run"
Write-Host ""

Write-Host "6. No Grok Build personas in this adapter"
$personas = @("gxp-researcher", "gxp-architect", "gxp-verifier")
foreach ($p in $personas) {
    $f = Join-Path $AdapterRoot ("personas\" + $p + ".toml")
    if (Test-Path -LiteralPath $f) {
        Write-Host ("  FAIL   personas/" + $p + ".toml must not ship on grok-bot") -ForegroundColor Red
        $fail = 1
    } else {
        Write-Host ("  OK     no personas/" + $p + ".toml")
    }
}
Write-Host ""

if ($fail -ne 0) {
    Write-Host "=== FAIL: Grok Bot adapter check-core ===" -ForegroundColor Red
    exit 1
}
Write-Host "=== PASS: Grok Bot adapter presence + integrity clean ===" -ForegroundColor Green
