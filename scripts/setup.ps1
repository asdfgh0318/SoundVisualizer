# First-time setup for SoundVisualizer on Windows (PowerShell).
# Creates a Python venv, installs server + frontend deps, runs tests, builds frontend.
# Linux/macOS users: use scripts/setup.sh instead.

$ErrorActionPreference = "Stop"
Set-Location (Join-Path $PSScriptRoot "..")

function Step($msg) { Write-Host ""; Write-Host "==> $msg" -ForegroundColor Green }
function Warn($msg) { Write-Host "WARN: $msg" -ForegroundColor Yellow }
function Fail($msg) { Write-Host "FAIL: $msg" -ForegroundColor Red; exit 1 }

Step "Detected platform: Windows"

# --- Python 3.12 ---
$python = $null
foreach ($candidate in @("python3.12", "py -3.12", "python")) {
    try {
        $verOk = & cmd /c "$candidate -c `"import sys; sys.exit(0 if sys.version_info >= (3, 12) else 1)`"" 2>$null
        if ($LASTEXITCODE -eq 0) { $python = $candidate; break }
    } catch { }
}
if (-not $python) { Fail "Python 3.12+ not found. Install from python.org or via 'winget install Python.Python.3.12'." }
Step "Python: $(cmd /c "$python --version")"

# --- Node 22 ---
try { $nodeVer = node -v } catch { Fail "node not found. Install Node 22 from nodejs.org or via 'winget install OpenJS.NodeJS.LTS'." }
Step "Node: $nodeVer"
if ($nodeVer -notlike "v22.*") { Warn ".nvmrc pins Node 22; you're on $nodeVer — frontend should still work but is untested." }

# --- Python venv + deps ---
Step "Setting up Python venv at .venv/"
if (-not (Test-Path .venv)) { & cmd /c "$python -m venv .venv" }
& .venv\Scripts\python.exe -m pip install --upgrade pip --quiet
& .venv\Scripts\python.exe -m pip install -e ".[dev]" --quiet

# --- Frontend deps ---
Step "Installing frontend dependencies"
npm install --silent

# --- Smoke checks ---
Step "Running server test suite"
& .venv\Scripts\python.exe -m pytest server/tests/ -q

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
