<#
.SYNOPSIS
    GXP (Guided eXecution Protocol) Helper Functions

    Source this file in your PowerShell profile for convenient access to the GXP skill.

.EXAMPLE
    . "$HOME\path\to\gxp\adapters\grok\ai-workflow\gxp.ps1"

    # Then use:
    gxp-check
    gxp-open
    gxp-test
#>

$script:GxpRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

function gxp-check {
    <#
    .SYNOPSIS
        Run the GXP core sync check (PowerShell version recommended on Windows).
    #>
    $checkScript = Join-Path $script:GxpRoot "sync\check-core.ps1"
    if (Test-Path $checkScript) {
        & $checkScript @args
    } else {
        Write-Warning "check-core.ps1 not found at $checkScript"
    }
}

function gxp-open {
    <#
    .SYNOPSIS
        Open the GXP skill folder in Explorer.
    #>
    Invoke-Item $script:GxpRoot
}

function gxp-test {
    <#
    .SYNOPSIS
        Print a good test prompt you can copy into a Grok chat.
    #>
    $testFile = Join-Path $script:GxpRoot "TEST_PROMPT.md"
    if (Test-Path $testFile) {
        Get-Content $testFile | Select-String -Pattern '### Quick' -Context 0, 20
    } else {
        Write-Host "Use gxp" -ForegroundColor Cyan
        Write-Host "Run the sync check: .\sync\check-core.ps1" -ForegroundColor Cyan
    }
}

function gxp-install {
    <#
    .SYNOPSIS
        Re-run the GXP skill installer (useful after pulling updates).
    #>
    $installScript = Join-Path $script:GxpRoot "sync\install-grok-skill.ps1"
    if (Test-Path $installScript) {
        & $installScript @args
    } else {
        Write-Warning "install-grok-skill.ps1 not found"
    }
}

function gxp-root {
    <#
    .SYNOPSIS
        Change directory into the GXP skill folder.
    #>
    Set-Location $script:GxpRoot
    Write-Host "Now in: $script:GxpRoot" -ForegroundColor Green
}

function gxp-edit {
    <#
    .SYNOPSIS
        Quickly open key GXP files for editing.
    #>
    $files = @(
        (Join-Path $script:GxpRoot "SKILL.md"),
        (Join-Path $script:GxpRoot "instructions\workflow.md"),
        (Join-Path $script:GxpRoot "sync\drift-allowlist.txt")
    )

    foreach ($file in $files) {
        if (Test-Path $file) {
            notepad $file
        }
    }
}

function gxp-new-brief {
    <#
    .SYNOPSIS
        Open a fresh copy of the task brief template for a new task.
    #>
    # Fixed per B1 in implementation-plan-2026-06-09.md: relative to skill dir
    $template = Join-Path $script:GxpRoot "..\..\..\core\templates\task-brief.md"

    if (Test-Path $template) {
        $tempFile = [System.IO.Path]::GetTempFileName() -replace '\.tmp$', '.md'
        Copy-Item $template $tempFile
        notepad $tempFile
        Write-Host "Opened new task brief template at: $tempFile" -ForegroundColor Cyan
    } else {
        Write-Warning "Could not find task-brief.md template at $template"
    }
}

# New recommended way to call GXP tools (subcommand style for clarity):
#   gxp check
#   gxp open
#   gxp test
#   etc.
#
# Old flat names (gxp-check, etc.) still work for backward compatibility.

function gxp {
    <#
    .SYNOPSIS
        Unified entrypoint for GXP (ai-workflow) management tools.
        Use `gxp <tool>` for the clean, discoverable way to call tools.
    #>
    [CmdletBinding()]
    param(
        [Parameter(Position = 0)]
        [string]$Tool = "check",

        [Parameter(ValueFromRemainingArguments = $true)]
        $Arguments
    )

    $toolLower = $Tool.ToLower()

    switch ($toolLower) {
        "check"      { gxp-check @Arguments }
        "open"       { gxp-open @Arguments }
        "test"       { gxp-test @Arguments }
        "install"    { gxp-install @Arguments }
        "root"       { gxp-root @Arguments }
        "cd"         { gxp-root @Arguments }
        "edit"       { gxp-edit @Arguments }
        "new-brief"  { gxp-new-brief @Arguments }
        "brief"      { gxp-new-brief @Arguments }
        "help"       { Show-GxpHelp }
        default {
            Write-Host "Unknown GXP tool: '$Tool'" -ForegroundColor Yellow
            Show-GxpHelp
        }
    }
}

function Show-GxpHelp {
    Write-Host "GXP tools (ai-workflow helpers). Call as: gxp <tool>" -ForegroundColor Green
    Write-Host ""
    Write-Host "  check      → Run sync check against core methodology" -ForegroundColor Cyan
    Write-Host "  open       → Open the GXP skill folder" -ForegroundColor Cyan
    Write-Host "  test       → Show a good test prompt for Grok" -ForegroundColor Cyan
    Write-Host "  install    → Re-install or repair the skill" -ForegroundColor Cyan
    Write-Host "  root / cd  → cd into the skill folder" -ForegroundColor Cyan
    Write-Host "  edit       → Open key workflow files for editing" -ForegroundColor Cyan
    Write-Host "  new-brief  → Start a fresh task brief from the template" -ForegroundColor Cyan
    Write-Host "  help       → This message"
    Write-Host ""
    Write-Host "Legacy flat commands (still work): gxp-check, gxp-open, ..." -ForegroundColor DarkGray
    Write-Host ""
    Write-Host "Tip: Source this in your profile for permanent access:" -ForegroundColor Yellow
    Write-Host ". '$script:GxpRoot\gxp.ps1'" -ForegroundColor Yellow
}

# Convenience alias for the old "just run check" behavior
Set-Alias gxp-check gxp-check -ErrorAction SilentlyContinue  # ensure the function exists
# Keep old flat names working by leaving the original functions in place.

Write-Host "GXP helpers loaded." -ForegroundColor Green
Write-Host "Recommended: use the subcommand style →  gxp check | gxp open | gxp new-brief | gxp help" -ForegroundColor Cyan
Write-Host "Legacy also available: gxp-check, gxp-open, etc." -ForegroundColor DarkGray
Write-Host ""
