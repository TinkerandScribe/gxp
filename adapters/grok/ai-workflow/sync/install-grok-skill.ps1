<#
.SYNOPSIS
    Installs or updates the GXP skill (and optional personas) into local Grok paths.

.DESCRIPTION
    Links this Grok adapter into:
      $HOME\.grok\skills\gxp-ai-workflow

    Also re-points the legacy skill path (if present or always as alias):
      $HOME\.grok\skills\tinker-tools-ai-workflow
    so chats that still load the old folder name get the current GXP skill.

    Optionally installs example personas into:
      $HOME\.grok\personas\*.toml
    (Grok discovers file-based personas there; a bare file named "personas" is fixed.)

.PARAMETER Force
    Overwrite existing skill install and refresh personas without prompting.

.PARAMETER SkipPersonas
    Do not install/update ~/.grok/personas/*.toml

.EXAMPLE
    .\install-grok-skill.ps1
    .\install-grok-skill.ps1 -Force
    .\install-grok-skill.ps1 -Force -SkipPersonas
#>

[CmdletBinding()]
param(
    [switch]$Force,
    [switch]$SkipPersonas
)

$ErrorActionPreference = "Stop"

$SourceDir = Split-Path -Parent $PSScriptRoot   # ai-workflow folder
$SkillsRoot = Join-Path $HOME ".grok\skills"
$TargetDir = Join-Path $SkillsRoot "gxp-ai-workflow"
$LegacyDir = Join-Path $SkillsRoot "tinker-tools-ai-workflow"
$PersonasDir = Join-Path $HOME ".grok\personas"
$PersonasSrc = Join-Path $SourceDir "examples\grok-build-strategy\personas"

function New-SkillJunction {
    param(
        [Parameter(Mandatory)][string]$LinkPath,
        [Parameter(Mandatory)][string]$TargetPath,
        [string]$Label = "skill"
    )

    if (Test-Path $LinkPath) {
        if (-not $Force) {
            $response = Read-Host "Target already exists at $LinkPath. Overwrite? (y/N)"
            if ($response -ne 'y' -and $response -ne 'Y') {
                Write-Host "Skipped $Label ($LinkPath)." -ForegroundColor Yellow
                return $false
            }
        }
        # Junctions and dirs: -Force remove
        Remove-Item $LinkPath -Recurse -Force
    }

    $parent = Split-Path -Parent $LinkPath
    New-Item -ItemType Directory -Force -Path $parent | Out-Null

    $null = cmd /c "mklink /J `"$LinkPath`" `"$TargetPath`"" 2>&1
    if (Test-Path $LinkPath) {
        Write-Host "Linked $Label -> $LinkPath" -ForegroundColor Green
        return $true
    }

    Copy-Item $TargetPath $LinkPath -Recurse -Force
    Write-Host "Copied $Label to $LinkPath (not linked)" -ForegroundColor Yellow
    return $true
}

function Install-GxpPersonas {
    if (-not (Test-Path $PersonasSrc)) {
        Write-Host "No personas source at $PersonasSrc - skipping personas." -ForegroundColor Yellow
        return
    }

    # Grok expects ~/.grok/personas/*.toml - a plain file named "personas" breaks discovery.
    if (Test-Path $PersonasDir) {
        $item = Get-Item $PersonasDir -Force
        if (-not $item.PSIsContainer) {
            $backup = Join-Path $HOME (".grok\personas.file-backup-{0}.toml" -f (Get-Date -Format "yyyyMMdd-HHmmss"))
            Move-Item -LiteralPath $PersonasDir -Destination $backup -Force
            Write-Host "Moved mis-shaped personas file to $backup" -ForegroundColor Yellow
            New-Item -ItemType Directory -Force -Path $PersonasDir | Out-Null
        }
    } else {
        New-Item -ItemType Directory -Force -Path $PersonasDir | Out-Null
    }

    $copied = 0
    Get-ChildItem -Path $PersonasSrc -Filter "*.toml" | ForEach-Object {
        $dest = Join-Path $PersonasDir $_.Name
        if ((Test-Path $dest) -and -not $Force) {
            $response = Read-Host "Persona $($_.Name) exists. Overwrite? (y/N)"
            if ($response -ne 'y' -and $response -ne 'Y') {
                Write-Host "  skipped $($_.Name)" -ForegroundColor Yellow
                return
            }
        }
        Copy-Item $_.FullName $dest -Force
        $copied++
        Write-Host "  persona: $($_.Name)" -ForegroundColor Green
    }
    Write-Host "Installed $copied persona file(s) into $PersonasDir" -ForegroundColor Cyan
}

Write-Host "Installing Grok AI Workflow skill..." -ForegroundColor Cyan
Write-Host "Source: $SourceDir"
Write-Host "Target: $TargetDir"
Write-Host "Legacy alias: $LegacyDir"

$ok = New-SkillJunction -LinkPath $TargetDir -TargetPath $SourceDir -Label "gxp-ai-workflow"
if (-not $ok) {
    Write-Host "Primary skill install cancelled." -ForegroundColor Yellow
    exit 0
}

# Always keep legacy folder name pointed at the same adapter so "gxp" skill discovery
# that still resolves tinker-tools-ai-workflow is not stale.
$null = New-SkillJunction -LinkPath $LegacyDir -TargetPath $SourceDir -Label "tinker-tools-ai-workflow (legacy alias)"

if (-not $SkipPersonas) {
    Write-Host "`nInstalling GXP example personas..." -ForegroundColor Cyan
    Install-GxpPersonas
}

Write-Host "`nDone! Skill short name: 'gxp' (or 'gxp-ai-workflow')." -ForegroundColor Green
Write-Host "Changes in this repo are live via junction(s)."
Write-Host "Recommended check:"
Write-Host "  .\sync\check-core.ps1" -ForegroundColor Cyan
Write-Host "Personas (if installed): /personas in Grok Build - expect gxp-researcher, gxp-architect, gxp-verifier, grok-native-planner, composer-coder."
Write-Host "See GETTING_STARTED.md for Plan Mode + GXP usage." -ForegroundColor Yellow
