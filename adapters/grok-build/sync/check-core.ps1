<#
.SYNOPSIS
    Lightweight presence + integrity check for the Grok Build adapter.

.DESCRIPTION
    Windows-friendly wrapper. Prefer the bash twin when available
    (Git Bash / WSL); this script mirrors the same required-file and
    persona model checks without a full workflow.md diff.

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

Write-Host "=== Grok Build adapter - Core Sync Check (PowerShell) ==="
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
    "INSTALL.md",
    "README.md",
    "install-grok-build.ps1",
    "install-grok-build.sh",
    "personas\gxp-researcher.toml",
    "personas\gxp-architect.toml",
    "personas\gxp-verifier.toml",
    "personas\composer-coder.toml",
    "personas\grok-native-planner.toml",
    "workflows\gxp-heavy-front-half.rhai",
    "workflows\gxp-layer2-verify.rhai",
    "workflows\README.md",
    "sync\drift-allowlist.txt"
)
foreach ($rel in $required) {
    Require-Path (Join-Path $AdapterRoot $rel) $rel
}
Write-Host ""

Write-Host "3. SKILL.md integrity"
Require-Marker (Join-Path $AdapterRoot "SKILL.md") "name: gxp-build"
Write-Host ""

Write-Host '4. Persona model convention (model = "grok-build")'
$personas = @(
    "gxp-researcher",
    "gxp-architect",
    "gxp-verifier",
    "composer-coder",
    "grok-native-planner"
)
foreach ($p in $personas) {
    $f = Join-Path $AdapterRoot ("personas\" + $p + ".toml")
    if (-not (Test-Path -LiteralPath $f)) {
        Write-Host ("  MISSING: personas/" + $p + ".toml") -ForegroundColor Red
        $fail = 1
        continue
    }
    $content = Get-Content -LiteralPath $f -Raw
    if ($content -notmatch '(?m)^\s*model\s*=\s*"grok-build"') {
        Write-Host ("  FAIL   personas/" + $p + '.toml: expected model = "grok-build"') -ForegroundColor Red
        $fail = 1
    } else {
        Write-Host ("  OK     personas/" + $p + '.toml model = "grok-build"')
    }
}
Write-Host ""

if ($fail -ne 0) {
    Write-Host "=== FAIL: Grok Build adapter check-core ===" -ForegroundColor Red
    exit 1
}
Write-Host "=== PASS: Grok Build adapter presence + integrity clean ===" -ForegroundColor Green
