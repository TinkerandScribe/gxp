<#
.SYNOPSIS
    Installs the Cursor AI Workflow adapter rule into a target repository.

.PARAMETER TargetRepo
    Path to the target repository root. Defaults to current directory.

.PARAMETER Force
    Overwrite an existing ai-workflow.mdc without prompting.

.PARAMETER IncludeSecurityTemplate
    Also copy security.mdc.template to .cursor/rules/security.mdc if missing.

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File install-cursor-rule.ps1

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File install-cursor-rule.ps1 -TargetRepo C:\repos\my-project -Force -IncludeSecurityTemplate
#>

param(
    [string]$TargetRepo = (Get-Location).Path,
    [switch]$Force,
    [switch]$IncludeSecurityTemplate
)

$ErrorActionPreference = "Stop"

$scriptDir   = Split-Path -Parent $MyInvocation.MyCommand.Path
$adapterDir  = Split-Path -Parent $scriptDir
$sourcePath  = Join-Path $adapterDir "rule.mdc"
$securitySrc = Join-Path $adapterDir "security.mdc.template"

if (-not (Test-Path $sourcePath)) {
    Write-Error "Cannot find rule.mdc at: $sourcePath"
    exit 1
}

$destDir  = Join-Path $TargetRepo ".cursor\rules"
$destPath = Join-Path $destDir "ai-workflow.mdc"
$securityDest = Join-Path $destDir "security.mdc"

if (-not (Test-Path $destDir)) {
    Write-Host "Creating: $destDir"
    New-Item -ItemType Directory -Path $destDir | Out-Null
}

$otherRules = @()
if (Test-Path $destDir) {
    $otherRules = Get-ChildItem $destDir -Filter "*.mdc" -File |
        Where-Object { $_.Name -ne "ai-workflow.mdc" } |
        Select-Object -ExpandProperty Name
}

if ((Test-Path $destPath) -and -not $Force) {
    $confirm = Read-Host "ai-workflow.mdc already exists. Overwrite? (y/N)"
    if ($confirm -ne "y" -and $confirm -ne "Y") {
        Write-Host "Aborted. Use -Force to skip this prompt."
        exit 0
    }
}

Copy-Item $sourcePath $destPath -Force
Write-Host ""
Write-Host "Installed: $destPath"
Write-Host ""
Write-Host "Note: Only ai-workflow.mdc was installed or overwritten."
if ($otherRules.Count -gt 0) {
    Write-Host "Preserved other .cursor/rules files:"
    foreach ($r in $otherRules) { Write-Host "  - $r" }
}
if ((Test-Path $securityDest) -and $Force) {
    Write-Host "Preserved existing security.mdc (not overwritten by -Force)."
}

if ($IncludeSecurityTemplate) {
    if (-not (Test-Path $securitySrc)) {
        Write-Warning "security.mdc.template not found at $securitySrc"
    } elseif (Test-Path $securityDest) {
        Write-Host "security.mdc already exists - skipped (customize manually if needed)."
    } else {
        Copy-Item $securitySrc $securityDest
        Write-Host "Installed: $securityDest (from template - edit for this repo)"
    }
}

Write-Host ""
Write-Host "Next steps:"
Write-Host "  1. Verify Cursor picks it up: open a chat and paste TEST_PROMPT.md."
Write-Host "  2. Install .ai/ scaffold: scripts/install-ai-from-core.ps1 (from gxp repo)"
Write-Host "  3. Fill in .ai/PROGRAM.md with this project's verification commands."
Write-Host "  4. Add .ai/tmp/ to .gitignore if using ephemeral audit artifacts."
Write-Host ""
