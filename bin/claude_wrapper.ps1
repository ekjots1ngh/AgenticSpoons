$ErrorActionPreference = "Stop"

function Resolve-ClaudeExecutable {
    param(
        [string[]]$Candidates
    )

    foreach ($candidate in $Candidates) {
        if ([string]::IsNullOrWhiteSpace($candidate)) {
            continue
        }

        $expanded = [Environment]::ExpandEnvironmentVariables($candidate)
        if (-not (Test-Path $expanded)) {
            continue
        }

        $directExe = Join-Path $expanded "claude.exe"
        if (Test-Path $directExe) {
            return $directExe
        }

        $match = Get-ChildItem -Path $expanded -Filter "claude.exe" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($match) {
            return $match.FullName
        }
    }

    return $null
}

$candidateRoots = @(
    $env:CLAUDE_HOME,
    "$env:LOCALAPPDATA\\Programs\\Claude",
    "$env:LOCALAPPDATA\\Programs\\Anthropic",
    "$env:LOCALAPPDATA\\Programs",
    "$env:ProgramFiles\\Claude",
    "$env:ProgramFiles\\Anthropic",
    "$env:ProgramFiles(x86)\\Claude",
    "$env:ProgramFiles(x86)\\Anthropic"
)

$claudeExe = Resolve-ClaudeExecutable -Candidates $candidateRoots

if (-not $claudeExe) {
    Write-Error "Unable to locate claude.exe. Install the Claude CLI with 'winget install anthropic.claude' or set CLAUDE_HOME to the installation directory."
    exit 1
}

$claudeDir = Split-Path -Parent $claudeExe
$pathParts = $env:PATH -split ';'
$normalizedParts = $pathParts | ForEach-Object { $_.Trim().TrimEnd('\') }
$normalizedDir = $claudeDir.TrimEnd('\')
if (-not ($normalizedParts -contains $normalizedDir)) {
    $env:PATH = "$claudeDir;$env:PATH"
}

if (-not $env:CLAUDE_API_KEY) {
    $dotenvPath = Join-Path $PSScriptRoot "..\.env"
    if (Test-Path $dotenvPath) {
        foreach ($line in Get-Content $dotenvPath) {
            if ($line -match '^\s*CLAUDE_API_KEY\s*=\s*(.+)\s*$') {
                $env:CLAUDE_API_KEY = $Matches[1].Trim('"'' ')
                break
            }
        }
    }
}

if (-not $env:CLAUDE_API_KEY) {
    Write-Warning "CLAUDE_API_KEY is not set. Set it in your environment or add CLAUDE_API_KEY=your_key to .env before running the CLI."
}

& $claudeExe @args
exit $LASTEXITCODE
