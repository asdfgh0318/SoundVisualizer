# First-time setup for SoundVisualizer on Windows (PowerShell 5.1+).
# Creates a Python venv, installs server + frontend deps, runs tests, builds frontend.
# Linux/macOS users: use scripts/setup.sh instead.

$ErrorActionPreference = "Stop"
Set-Location (Join-Path $PSScriptRoot "..")

function Step($msg) { Write-Host ""; Write-Host "==> $msg" -ForegroundColor Green }
function Warn($msg) { Write-Host "WARN: $msg" -ForegroundColor Yellow }
function Fail($msg) { Write-Host "FAIL: $msg" -ForegroundColor Red; exit 1 }

Step "Detected platform: Windows"

# --- Python 3.12+ ---
$python = $null
foreach ($cmd in @("python3.12", "python")) {
    if (Get-Command $cmd -ErrorAction SilentlyContinue) {
        $ver = & $cmd --version 2>&1
        if ($ver -match "Python 3\.(\d+)" -and [int]$Matches[1] -ge 12) {
            $python = $cmd
            break
        }
    }
}
if (-not $python) {
    Fail "Python 3.12+ not found on PATH. Install via 'winget install Python.Python.3.12' or python.org and reopen PowerShell."
}
Step "Python: $(& $python --version)"

# --- Node 22 ---
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Fail "node not found. Install Node 22 from nodejs.org or via 'winget install OpenJS.NodeJS.LTS'."
}
$nodeVer = node -v
Step "Node: $nodeVer"
if ($nodeVer -notlike "v22.*") {
    Warn ".nvmrc pins Node 22; you're on $nodeVer - frontend should still work but is untested."
}

# --- Python venv + deps ---
Step "Setting up Python venv at .venv/"
if (-not (Test-Path .venv)) { & $python -m venv .venv }
$venvPython = ".venv\Scripts\python.exe"
& $venvPython -m pip install --upgrade pip --quiet
& $venvPython -m pip install -e ".[dev]" --quiet

# --- Frontend deps ---
Step "Installing frontend dependencies"
npm install --silent

# --- Smoke checks ---
Step "Running server test suite"
& $venvPython -m pytest server/tests/ -q

Step "Building frontend bundle"
npm run build | Out-Null

# --- Done ---
Write-Host ""
Write-Host "Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Run the app:"
Write-Host "  Terminal 1:  .venv\Scripts\uvicorn.exe server.main:app --reload --port 8000"
Write-Host "  Terminal 2:  npm run dev"
Write-Host "  Open:        http://localhost:5173"
Write-Host ""
Write-Host "Populate demo data without hardware:"
Write-Host "  curl.exe -X POST http://localhost:8000/dev/seed"
Write-Host ""
Write-Host "Heads up: hardware integration (Tyto serial, udev rules, multi-mic capture)" -ForegroundColor Yellow
Write-Host "  is Linux-tested only. Frontend dev, fake captures, and Results tabs" -ForegroundColor Yellow
Write-Host "  (FFT/Polar/Custom) work fully on Windows." -ForegroundColor Yellow
