<#
.SYNOPSIS
    Installs or updates the GXP skill into your local Grok skills directory.

.DESCRIPTION
    Copies (or symlinks when possible) this Grok adapter into:
    $HOME\.grok\skills\gxp-ai-workflow

    This makes the skill available in your Grok chats.

.PARAMETER Force
    Overwrite existing installation without prompting.

.EXAMPLE
    .\install-grok-skill.ps1
    .\install-grok-skill.ps1 -Force
#>

[CmdletBinding()]
param(
    [switch]$Force
)

$SourceDir = Split-Path -Parent $PSScriptRoot   # When run from the sync/ folder, this points to the ai-workflow folder itself
$TargetDir = Join-Path $HOME ".grok\skills\gxp-ai-workflow"

Write-Host "Installing Grok AI Workflow skill..." -ForegroundColor Cyan
Write-Host "Source: $SourceDir"
Write-Host "Target: $TargetDir"

if (Test-Path $TargetDir) {
    if (-not $Force) {
        $response = Read-Host "Target already exists. Overwrite? (y/N)"
        if ($response -ne 'y' -and $response -ne 'Y') {
            Write-Host "Installation cancelled." -ForegroundColor Yellow
            exit 0
        }
    }
    Remove-Item $TargetDir -Recurse -Force
}

try {
    # Try to create a junction (symlink-like) on Windows for easier updates
    $parent = Split-Path -Parent $TargetDir
    New-Item -ItemType Directory -Force -Path $parent | Out-Null

    cmd /c "mklink /J `"$TargetDir`" `"$SourceDir`"" 2>$null | Out-Null

    if (Test-Path $TargetDir) {
        Write-Host "Created directory junction (live link) at $TargetDir" -ForegroundColor Green
        Write-Host "Changes in this repo will be immediately visible to Grok."
    } else {
        # Fallback to copy
        Copy-Item $SourceDir $TargetDir -Recurse -Force
        Write-Host "Copied skill to $TargetDir (not linked)" -ForegroundColor Yellow
        Write-Host "Re-run this script after updates, or use -Force."
    }
} catch {
    # Final fallback
    Copy-Item $SourceDir $TargetDir -Recurse -Force
    Write-Host "Copied skill to $TargetDir" -ForegroundColor Yellow
}

Write-Host "`nDone! The skill should now be available under the short name 'gxp' (recommended) or 'gxp-ai-workflow' in your Grok chats." -ForegroundColor Green
Write-Host "Recommended: Run the check script after installation:"
Write-Host "  .\sync\check-core.ps1" -ForegroundColor Cyan
Write-Host ""
Write-Host "For even easier access, source gxp.ps1 in your profile." -ForegroundColor Yellow
Write-Host "See GETTING_STARTED.md for instructions." -ForegroundColor Yellow
