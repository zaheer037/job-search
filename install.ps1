<#
    One-command setup for the job application workspace (Windows).

        .\install.ps1              set everything up
        .\install.ps1 -Check       verify an existing install

    Windows blocks symlink creation unless Developer Mode is on or the shell is
    elevated, so this wrapper passes --copy by default: the per-runtime
    projections become real copies, and `--check` content-compares them so drift
    is reported rather than silently kept. Pass -Symlink to opt back in once
    Developer Mode is enabled.
#>
[CmdletBinding()]
param(
    [switch]$Check,
    [switch]$SkipDeps,
    [switch]$Symlink,
    [switch]$NoColor
)

$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot

$python = $null
foreach ($candidate in @('python', 'python3', 'py')) {
    $cmd = Get-Command $candidate -ErrorAction SilentlyContinue
    if (-not $cmd) { continue }
    & $candidate -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)' 2>$null
    if ($LASTEXITCODE -eq 0) { $python = $candidate; break }
}

if (-not $python) {
    Write-Error "Python 3.10+ is required and was not found on PATH. Install it from https://www.python.org/downloads/ and re-run .\install.ps1"
    exit 1
}

$args = @('tools/install.py')
if ($Check)    { $args += '--check' }
if ($SkipDeps) { $args += '--skip-deps' }
if ($NoColor)  { $args += '--no-color' }
if (-not $Symlink) { $args += '--copy' }

& $python @args
exit $LASTEXITCODE
