<#
.SYNOPSIS
    Scan host repos, optionally pull, refresh GXP .ai scaffold, commit, push.

.DESCRIPTION
    Discovers git repos under one or more roots (default: C:\Users\Reepicheep\Claude).
    By default only reports (dry-run). With -Apply, re-runs install-ai-from-core.ps1
    -Force for repos that already have .ai/workflow.md.

    Safety (defaults):
      - Dry-run unless -Apply
      - Only update repos that already have .ai/workflow.md (unless -Bootstrap)
      - git pull --ff-only only (skip on dirty / non-ff)
      - Commit only with -Commit, and only if the installer changed files
      - Push only with -Push (implies need -Commit); never force-push
      - Never force-push; never drop local work

.PARAMETER Roots
    One or more directories to scan for git repos. Default: C:\Users\Reepicheep\Claude

.PARAMETER Apply
    Write updates (run install-ai-from-core -Force). Without this, only report.

.PARAMETER Commit
    After a successful apply that changes files, create a commit in the host repo.

.PARAMETER Push
    After commit, push to the configured upstream (requires -Commit). Never --force.

.PARAMETER Bootstrap
    Also install GXP into git repos that do not yet have .ai/workflow.md.

.PARAMETER IncludeCursorRule
    Pass -IncludeCursorRule to install-ai-from-core.

.PARAMETER MaxDepth
    How deep under each root to look for .git directories (default 3).

.PARAMETER ExcludeNames
    Directory basenames to skip (default: gxp-public, node_modules, .git, dist, target).

.EXAMPLE
    # Report only (safe default)
    .\scripts\sync-gxp-hosts.ps1

.EXAMPLE
    # Update .ai on hosts that already use GXP
    .\scripts\sync-gxp-hosts.ps1 -Apply

.EXAMPLE
    # Update, commit, push
    .\scripts\sync-gxp-hosts.ps1 -Apply -Commit -Push
#>

[CmdletBinding()]
param(
    [string[]]$Roots = @("C:\Users\Reepicheep\Claude"),
    [switch]$Apply,
    [switch]$Commit,
    [switch]$Push,
    [switch]$Bootstrap,
    [switch]$IncludeCursorRule,
    [int]$MaxDepth = 3,
    [string[]]$ExcludeNames = @("gxp-public", "node_modules", ".git", "dist", "target", ".venv", "venv")
)

$ErrorActionPreference = "Stop"

if ($Push -and -not $Commit) {
    Write-Error "-Push requires -Commit"
    exit 2
}
if ($Commit -and -not $Apply) {
    Write-Error "-Commit requires -Apply"
    exit 2
}

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$gxpRoot = Split-Path -Parent $scriptDir
$installer = Join-Path $scriptDir "install-ai-from-core.ps1"
if (-not (Test-Path -LiteralPath $installer)) {
    Write-Error "Missing installer: $installer"
    exit 1
}
if (-not (Test-Path -LiteralPath (Join-Path $gxpRoot "core"))) {
    Write-Error "Not a GXP checkout (no core/): $gxpRoot"
    exit 1
}

function Test-IsGitRepo {
    param([string]$Path)
    Test-Path -LiteralPath (Join-Path $Path ".git")
}

function Get-GitRepos {
    param([string[]]$SearchRoots, [int]$Depth, [string[]]$Exclude)

    $found = New-Object System.Collections.Generic.List[string]
    foreach ($root in $SearchRoots) {
        if (-not (Test-Path -LiteralPath $root)) {
            Write-Host "WARN: root missing: $root" -ForegroundColor Yellow
            continue
        }
        $rootAbs = (Resolve-Path -LiteralPath $root).Path
        # Include root itself if it is a git repo
        if (Test-IsGitRepo $rootAbs) {
            $found.Add($rootAbs) | Out-Null
        }
        # Enumerate subdirs up to MaxDepth
        $queue = [System.Collections.Generic.Queue[object]]::new()
        $queue.Enqueue([pscustomobject]@{ Path = $rootAbs; Level = 0 })
        while ($queue.Count -gt 0) {
            $item = $queue.Dequeue()
            if ($item.Level -ge $Depth) { continue }
            try {
                $dirs = Get-ChildItem -LiteralPath $item.Path -Directory -Force -ErrorAction Stop
            } catch {
                continue
            }
            foreach ($d in $dirs) {
                if ($Exclude -contains $d.Name) { continue }
                if ($d.Attributes -band [IO.FileAttributes]::ReparsePoint) { continue }
                $p = $d.FullName
                if (Test-IsGitRepo $p) {
                    $found.Add($p) | Out-Null
                    # Do not recurse into nested git repos
                    continue
                }
                $queue.Enqueue([pscustomobject]@{ Path = $p; Level = ($item.Level + 1) })
            }
        }
    }
    return ($found | Select-Object -Unique | Sort-Object)
}

function Invoke-Git {
    param([string]$Repo, [string[]]$GitArgs)
    $prev = Get-Location
    $oldEap = $ErrorActionPreference
    try {
        $ErrorActionPreference = "Continue"
        Set-Location -LiteralPath $Repo
        $output = & git @GitArgs 2>&1
        $code = $LASTEXITCODE
        $text = ($output | ForEach-Object { "$_" }) -join "`n"
        return [pscustomobject]@{
            Code = $code
            Output = $text.Trim()
        }
    } finally {
        $ErrorActionPreference = $oldEap
        Set-Location $prev
    }
}

function Get-RepoState {
    param([string]$Repo)
    $branch = (Invoke-Git $Repo @("rev-parse", "--abbrev-ref", "HEAD")).Output
    $porcelain = (Invoke-Git $Repo @("status", "--porcelain")).Output
    $dirty = -not [string]::IsNullOrWhiteSpace($porcelain)
    $upCheck = Invoke-Git $Repo @("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}")
    $hasUpstream = ($upCheck.Code -eq 0)
    $aheadBehind = "n/a"
    if ($hasUpstream) {
        $lr = Invoke-Git $Repo @("rev-list", "--left-right", "--count", "HEAD...@{u}")
        if ($lr.Code -eq 0) { $aheadBehind = ($lr.Output -replace "\s+", " ") }
    }
    $hasGxp = Test-Path -LiteralPath (Join-Path $Repo ".ai\workflow.md")
    return [pscustomobject]@{
        Branch = $branch
        Dirty = $dirty
        HasUpstream = $hasUpstream
        AheadBehind = $aheadBehind
        HasGxp = $hasGxp
    }
}

$mode = if ($Apply) { "APPLY" } else { "DRY-RUN" }
Write-Host "=== sync-gxp-hosts ($mode) ===" -ForegroundColor Cyan
Write-Host "GXP source: $gxpRoot"
Write-Host "Roots:      $($Roots -join '; ')"
Write-Host "MaxDepth:   $MaxDepth"
Write-Host "Bootstrap:  $Bootstrap"
Write-Host "Commit:     $Commit  Push: $Push  CursorRule: $IncludeCursorRule"
Write-Host ""

$repos = @(Get-GitRepos -SearchRoots $Roots -Depth $MaxDepth -Exclude $ExcludeNames)
# Always skip the gxp source checkout itself even if not excluded by name match on path
$repos = $repos | Where-Object {
    $p = $_
    try {
        $resolved = (Resolve-Path -LiteralPath $p).Path
        $gxpResolved = (Resolve-Path -LiteralPath $gxpRoot).Path
        $resolved -ne $gxpResolved
    } catch { $true }
}

Write-Host "Discovered $($repos.Count) git repo(s) (excluding gxp-public source)."
Write-Host ""

$results = New-Object System.Collections.Generic.List[object]
$fail = 0

foreach ($repo in $repos) {
    $name = Split-Path -Leaf $repo
    $state = Get-RepoState $repo
    $action = "skip"
    $detail = ""
    $changed = $false

    if (-not $state.HasGxp -and -not $Bootstrap) {
        $action = "no-gxp"
        $detail = "no .ai/workflow.md (use -Bootstrap to install)"
        $results.Add([pscustomobject]@{ Repo = $name; Path = $repo; Action = $action; Detail = $detail; Branch = $state.Branch; Dirty = $state.Dirty }) | Out-Null
        continue
    }

    # Pull first when applying (or always attempt in dry-run report)
    $pullNote = ""
    if ($state.Dirty) {
        if ($Apply -and ($Commit -or $Push)) {
            $action = "skip-dirty"
            $detail = "dirty worktree; clean or commit host changes first"
            $results.Add([pscustomobject]@{ Repo = $name; Path = $repo; Action = $action; Detail = $detail; Branch = $state.Branch; Dirty = $state.Dirty }) | Out-Null
            continue
        }
        $pullNote = "dirty (pull skipped)"
    } elseif ($state.HasUpstream) {
        if ($Apply) {
            $fetch = Invoke-Git $repo @("fetch", "origin")
            $pull = Invoke-Git $repo @("pull", "--ff-only")
            if ($pull.Code -ne 0) {
                $action = "skip-pull"
                $detail = "ff-only pull failed: $($pull.Output)"
                $fail++
                $results.Add([pscustomobject]@{ Repo = $name; Path = $repo; Action = $action; Detail = $detail; Branch = $state.Branch; Dirty = $state.Dirty }) | Out-Null
                continue
            }
            $pullNote = "pulled ff-only"
        } else {
            $pullNote = "would pull ff-only (ahead/behind $($state.AheadBehind))"
        }
    } else {
        $pullNote = "no upstream"
    }

    # Installer
    $installArgs = @{
        TargetRepo = $repo
        Force = $true
    }
    if ($IncludeCursorRule) { $installArgs.IncludeCursorRule = $true }
    if (-not $Apply) { $installArgs.DryRun = $true }

    $beforeStatus = ""
    if ($Apply) {
        $beforeStatus = (Invoke-Git $repo @("status", "--porcelain")).Output
    }

    Write-Host "--- $name ---" -ForegroundColor DarkCyan
    Write-Host "  path: $repo"
    Write-Host "  $pullNote"

    try {
        & $installer @installArgs
        $installOk = $true
    } catch {
        $installOk = $false
        $detail = "installer error: $_"
        $fail++
        $action = "fail-install"
        $results.Add([pscustomobject]@{ Repo = $name; Path = $repo; Action = $action; Detail = $detail; Branch = $state.Branch; Dirty = $state.Dirty }) | Out-Null
        continue
    }

    if (-not $Apply) {
        $action = if ($state.HasGxp) { "would-update" } else { "would-bootstrap" }
        $detail = $pullNote
        $results.Add([pscustomobject]@{ Repo = $name; Path = $repo; Action = $action; Detail = $detail; Branch = $state.Branch; Dirty = $state.Dirty }) | Out-Null
        continue
    }

    $afterStatus = (Invoke-Git $repo @("status", "--porcelain")).Output
    $changed = ($afterStatus -ne $beforeStatus) -and (-not [string]::IsNullOrWhiteSpace($afterStatus))
    # More reliable: any .ai or cursor rule changes
    $diffStat = Invoke-Git $repo @("diff", "--stat", "HEAD")
    $untracked = Invoke-Git $repo @("ls-files", "--others", "--exclude-standard")
    $hasDiff = (-not [string]::IsNullOrWhiteSpace($diffStat.Output)) -or (-not [string]::IsNullOrWhiteSpace($untracked.Output))

    if (-not $hasDiff) {
        $action = "unchanged"
        $detail = "$pullNote; scaffold already current"
        $results.Add([pscustomobject]@{ Repo = $name; Path = $repo; Action = $action; Detail = $detail; Branch = $state.Branch; Dirty = $false }) | Out-Null
        continue
    }

    if (-not $Commit) {
        $action = "updated-uncommitted"
        $detail = "$pullNote; files changed (pass -Commit to commit)"
        $results.Add([pscustomobject]@{ Repo = $name; Path = $repo; Action = $action; Detail = $detail; Branch = $state.Branch; Dirty = $true }) | Out-Null
        continue
    }

    # Stage only GXP-related paths
    $pathsToAdd = @()
    if (Test-Path (Join-Path $repo ".ai")) { $pathsToAdd += ".ai" }
    if (Test-Path (Join-Path $repo ".cursor\rules\ai-workflow.mdc")) { $pathsToAdd += ".cursor/rules/ai-workflow.mdc" }
    foreach ($p in $pathsToAdd) {
        $null = Invoke-Git $repo @("add", "--", $p)
    }
    $staged = Invoke-Git $repo @("diff", "--cached", "--name-only")
    if ([string]::IsNullOrWhiteSpace($staged.Output)) {
        $action = "updated-uncommitted"
        $detail = "changes present but nothing staged under .ai/ (manual review)"
        $results.Add([pscustomobject]@{ Repo = $name; Path = $repo; Action = $action; Detail = $detail; Branch = $state.Branch; Dirty = $true }) | Out-Null
        continue
    }

    $msg = @"
chore(gxp): refresh .ai scaffold from upstream GXP core

Synced via scripts/sync-gxp-hosts from gxp-public. Preserves PROGRAM.md and ratings.jsonl.
"@
    # Use -F via temp file for reliable multiline on Windows
    $msgFile = Join-Path $env:TEMP ("gxp-host-commit-" + [guid]::NewGuid().ToString("n") + ".txt")
    [System.IO.File]::WriteAllText($msgFile, $msg.Trim() + "`n")
    $c = Invoke-Git $repo @("commit", "-F", $msgFile)
    Remove-Item -LiteralPath $msgFile -Force -ErrorAction SilentlyContinue
    if ($c.Code -ne 0) {
        $action = "fail-commit"
        $detail = $c.Output
        $fail++
        $results.Add([pscustomobject]@{ Repo = $name; Path = $repo; Action = $action; Detail = $detail; Branch = $state.Branch; Dirty = $true }) | Out-Null
        continue
    }

    if ($Push) {
        $st = Get-RepoState $repo
        if (-not $st.HasUpstream) {
            $action = "committed-no-push"
            $detail = "committed; no upstream configured"
            $results.Add([pscustomobject]@{ Repo = $name; Path = $repo; Action = $action; Detail = $detail; Branch = $st.Branch; Dirty = $false }) | Out-Null
            continue
        }
        $push = Invoke-Git $repo @("push")
        if ($push.Code -ne 0) {
            $action = "fail-push"
            $detail = $push.Output
            $fail++
            $results.Add([pscustomobject]@{ Repo = $name; Path = $repo; Action = $action; Detail = $detail; Branch = $st.Branch; Dirty = $false }) | Out-Null
            continue
        }
        $action = "committed-pushed"
        $detail = "ok"
    } else {
        $action = "committed"
        $detail = "local commit only (pass -Push to push)"
    }

    $results.Add([pscustomobject]@{ Repo = $name; Path = $repo; Action = $action; Detail = $detail; Branch = (Get-RepoState $repo).Branch; Dirty = $false }) | Out-Null
}

Write-Host ""
Write-Host "=== Summary ===" -ForegroundColor Cyan
$results | Format-Table -AutoSize Repo, Action, Branch, Dirty, Detail
Write-Host "Total: $($results.Count)  Failures: $fail  Mode: $mode"
if ($fail -gt 0) { exit 1 }
exit 0
