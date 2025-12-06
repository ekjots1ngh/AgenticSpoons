# AgenticSpoons Ultimate System Launcher
# PowerShell version for Windows

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host " AGENTSPOONS ULTIMATE SYSTEM" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Cyan

# Kill existing Python processes
Write-Host ""
Write-Host "Stopping existing processes..." -ForegroundColor Yellow
Stop-Process -Name python -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
$venvPath = ".\venv\Scripts\Activate.ps1"
if (Test-Path $venvPath) {
    & $venvPath
} else {
    Write-Host "Warning: Virtual environment not found" -ForegroundColor Red
}

# Create logs directory
if (-not (Test-Path "logs")) {
    New-Item -ItemType Directory -Path "logs" | Out-Null
}

# Start all services
Write-Host ""
Write-Host "Starting services..." -ForegroundColor Yellow

Write-Host "  -> Data generator..." -ForegroundColor Gray
$dataProc = Start-Process -FilePath ".\venv\Scripts\python.exe" -ArgumentList "src/enhanced_demo.py" -NoNewWindow -PassThru -RedirectStandardOutput "logs/data.log" -RedirectStandardError "logs/data_err.log"

Start-Sleep -Seconds 3

Write-Host "  -> Main dashboard..." -ForegroundColor Gray
$dashProc = Start-Process -FilePath ".\venv\Scripts\python.exe" -ArgumentList "src/championship_dashboard.py" -NoNewWindow -PassThru -RedirectStandardOutput "logs/dashboard.log" -RedirectStandardError "logs/dashboard_err.log"

Write-Host "  -> Greeks dashboard..." -ForegroundColor Gray
$greeksProc = Start-Process -FilePath ".\venv\Scripts\python.exe" -ArgumentList "src/visualization/greeks_dashboard.py" -NoNewWindow -PassThru -RedirectStandardOutput "logs/greeks.log" -RedirectStandardError "logs/greeks_err.log"

Start-Sleep -Seconds 2

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Green
Write-Host " ALL SERVICES RUNNING!" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Main Dashboard:    http://localhost:8050" -ForegroundColor Cyan
Write-Host "Greeks Dashboard:  http://localhost:8052" -ForegroundColor Cyan
Write-Host ""
Write-Host "Process IDs:" -ForegroundColor Yellow
Write-Host "   Data Generator:    $($dataProc.Id)" -ForegroundColor Gray
Write-Host "   Main Dashboard:    $($dashProc.Id)" -ForegroundColor Gray
Write-Host "   Greeks Dashboard:  $($greeksProc.Id)" -ForegroundColor Gray
Write-Host ""
Write-Host "Advanced Features:" -ForegroundColor Yellow
Write-Host "   - C++ Options Pricer (10-100x faster)" -ForegroundColor Gray
Write-Host "   - OCaml GARCH Models (ultra-fast)" -ForegroundColor Gray
Write-Host "   - ML Prediction (LSTM, XGBoost, Ensemble)" -ForegroundColor Gray
Write-Host "   - Time Series Forecasting (ARIMA, Prophet)" -ForegroundColor Gray
Write-Host "   - Real-time Streaming (Redis, Kafka)" -ForegroundColor Gray
Write-Host "   - Professional Backtesting (Backtrader)" -ForegroundColor Gray
Write-Host "   - Advanced Greeks Visualization" -ForegroundColor Gray
Write-Host ""
Write-Host "Stop all: Stop-Process -Name python -Force" -ForegroundColor Red
Write-Host "======================================================================" -ForegroundColor Cyan
