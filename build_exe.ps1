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
if ($LASTEXITCODE -ne 0) { throw "Resource self-test failed" }
python .\doors_ransom.py --runtime-self-test
if ($LASTEXITCODE -ne 0) { throw "Source runtime self-test failed" }
python .\security_behavior_test.py
if ($LASTEXITCODE -ne 0) { throw "Security behavior regression test failed" }
python .\ransom_setting.py --self-test
if ($LASTEXITCODE -ne 0) { throw "Settings source self-test failed" }
python .\honeypot_hotkey_test.py
if ($LASTEXITCODE -ne 0) { throw "Honeypot/hotkey regression test failed" }

python -m PyInstaller `
    --noconfirm `
    --clean `
    --distpath "$releaseDir" `
    --workpath "$projectDir\build" `
    "$projectDir\ransom.spec"
if ($LASTEXITCODE -ne 0) { throw "PyInstaller build failed" }
