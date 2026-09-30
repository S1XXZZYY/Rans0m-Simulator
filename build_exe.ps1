param([string]$OutputDirectory = "release")

$ErrorActionPreference = "Stop"

$projectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -LiteralPath $projectDir
$releaseDir = [IO.Path]::GetFullPath((Join-Path $projectDir $OutputDirectory))
if (-not $releaseDir.StartsWith($projectDir + "\", [StringComparison]::OrdinalIgnoreCase)) {
    throw "Build output must be inside the project directory"
}

# Package the checked-in image/audio/font files without regenerating or
# modifying them. Asset generators are explicit development tools.
python .\doors_ransom.py --self-test
