<#
.SYNOPSIS
    Installs Grok Build GXP personas, named workflows, and optionally the gxp-build skill.

.DESCRIPTION
    Default: copies personas from this adapter into:
      $HOME\.grok\personas\*.toml
    and copies runnable workflows (*.rhai) into:
      $HOME\.grok\workflows\

    Optional (-InstallSkill): junctions/copies this adapter to:
      $HOME\.grok\skills\gxp-build

    NEVER touches chat skill paths:
      $HOME\.grok\skills\gxp-ai-workflow
      $HOME\.grok\skills\tinker-tools-ai-workflow

.PARAMETER Force
    Overwrite existing personas, workflows, and (if installing) the gxp-build skill without prompting.

.PARAMETER SkipPersonas
    Do not install/update ~/.grok/personas/*.toml

.PARAMETER SkipWorkflows
    Do not install/update ~/.grok/workflows/*.rhai

.PARAMETER InstallSkill
    Install the Build skill as ~/.grok/skills/gxp-build (junction preferred, copy fallback).
    Default is OFF — personas + workflows only.

.EXAMPLE
    .\install-grok-build.ps1
    .\install-grok-build.ps1 -Force
    .\install-grok-build.ps1 -Force -InstallSkill
    .\install-grok-build.ps1 -Force -SkipPersonas -SkipWorkflows -InstallSkill
#>

[CmdletBinding()]
param(
    [switch]$Force,
    [switch]$SkipPersonas,
    [switch]$SkipWorkflows,
    [switch]$InstallSkill
)

$ErrorActionPreference = "Stop"

$AdapterRoot = $PSScriptRoot
$SkillsRoot = Join-Path $HOME ".grok\skills"
$SkillTarget = Join-Path $SkillsRoot "gxp-build"
$PersonasDir = Join-Path $HOME ".grok\personas"
$PersonasSrc = Join-Path $AdapterRoot "personas"
$WorkflowsDir = Join-Path $HOME ".grok\workflows"
$WorkflowsSrc = Join-Path $AdapterRoot "workflows"

# Hard-deny list: never create, remove, or rewrite these paths.
$ProtectedSkillNames = @("gxp-ai-workflow", "tinker-tools-ai-workflow")

function Assert-NotProtectedSkillPath {
    param([Parameter(Mandatory)][string]$Path)
    $leaf = Split-Path -Leaf $Path
    if ($ProtectedSkillNames -contains $leaf) {
        throw "Refusing to write protected chat skill path: $Path"
    }
    foreach ($name in $ProtectedSkillNames) {
        $protected = Join-Path $SkillsRoot $name
        if ($Path -eq $protected) {
            throw "Refusing to write protected chat skill path: $Path"
        }
    }
}

function New-SkillJunction {
    param(
        [Parameter(Mandatory)][string]$LinkPath,
        [Parameter(Mandatory)][string]$TargetPath,
        [string]$Label = "skill"
    )

    Assert-NotProtectedSkillPath -Path $LinkPath

    if (Test-Path $LinkPath) {
        if (-not $Force) {
            $response = Read-Host "Target already exists at $LinkPath. Overwrite? (y/N)"
            if ($response -ne 'y' -and $response -ne 'Y') {
                Write-Host "Skipped $Label ($LinkPath)." -ForegroundColor Yellow
                return $false
            }
        }
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

function Install-GxpBuildPersonas {
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

function Install-GxpBuildWorkflows {
    if (-not (Test-Path $WorkflowsSrc)) {
        Write-Host "No workflows source at $WorkflowsSrc - skipping workflows." -ForegroundColor Yellow
        return
    }

    if (-not (Test-Path $WorkflowsDir)) {
        New-Item -ItemType Directory -Force -Path $WorkflowsDir | Out-Null
    }

    $copied = 0
    Get-ChildItem -Path $WorkflowsSrc -Filter "*.rhai" | ForEach-Object {
        $dest = Join-Path $WorkflowsDir $_.Name
        if ((Test-Path $dest) -and -not $Force) {
            $response = Read-Host "Workflow $($_.Name) exists. Overwrite? (y/N)"
            if ($response -ne 'y' -and $response -ne 'Y') {
                Write-Host "  skipped $($_.Name)" -ForegroundColor Yellow
                return
            }
        }
        Copy-Item $_.FullName $dest -Force
        $copied++
        Write-Host "  workflow: $($_.Name)" -ForegroundColor Green
    }
    Write-Host "Installed $copied workflow file(s) into $WorkflowsDir" -ForegroundColor Cyan
    Write-Host "  names: gxp-heavy-front-half, gxp-layer2-verify (see workflows/README.md)" -ForegroundColor DarkGray
}

Write-Host "Installing Grok Build GXP adapter..." -ForegroundColor Cyan
Write-Host "Source: $AdapterRoot"
Write-Host "Personas target: $PersonasDir"
Write-Host "Workflows target: $WorkflowsDir"
if ($InstallSkill) {
    Write-Host "Skill target: $SkillTarget (opt-in)"
} else {
    Write-Host "Skill: skipped (default personas+workflows; pass -InstallSkill to add gxp-build)"
}

if (-not $SkipPersonas) {
    Write-Host "`nInstalling GXP Build personas..." -ForegroundColor Cyan
    Install-GxpBuildPersonas
} else {
    Write-Host "`nSkipping personas (-SkipPersonas)." -ForegroundColor Yellow
}

if (-not $SkipWorkflows) {
    Write-Host "`nInstalling GXP named workflows (*.rhai)..." -ForegroundColor Cyan
    Install-GxpBuildWorkflows
} else {
    Write-Host "`nSkipping workflows (-SkipWorkflows)." -ForegroundColor Yellow
}

if ($InstallSkill) {
    Write-Host "`nInstalling gxp-build skill (opt-in)..." -ForegroundColor Cyan
    Assert-NotProtectedSkillPath -Path $SkillTarget
    $ok = New-SkillJunction -LinkPath $SkillTarget -TargetPath $AdapterRoot -Label "gxp-build"
    if (-not $ok) {
        Write-Host "Skill install cancelled." -ForegroundColor Yellow
    }
}

Write-Host "`nDone." -ForegroundColor Green
Write-Host "Protected (never touched): gxp-ai-workflow, tinker-tools-ai-workflow"
Write-Host "Personas (if installed): /personas in Grok Build - gxp-researcher, gxp-architect, gxp-verifier, grok-native-planner, composer-coder."
Write-Host "Workflows (if installed): /workflow gxp-heavy-front-half | gxp-layer2-verify"
if ($InstallSkill) {
    Write-Host "Skill short name: gxp-build (folder ~/.grok/skills/gxp-build)"
}
Write-Host "See INSTALL.md and README.md." -ForegroundColor Yellow
