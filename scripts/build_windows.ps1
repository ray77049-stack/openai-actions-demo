param(
  [string]$Python = "python",
  [string]$ExeName = "offline-monitor"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path ".venv")) {
  & $Python -m venv .venv
}

.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt

if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }

pyinstaller --noconfirm --clean --windowed --name $ExeName app/main.py

Write-Host "Build complete: dist/$ExeName/$ExeName.exe"
