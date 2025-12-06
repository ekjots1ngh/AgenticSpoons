# AgentSpoons - Full System Startup (Windows)

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "🚀 AGENTSPOONS - FULL SYSTEM STARTUP" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Cyan

# Kill any existing processes
Write-Host "Stopping existing processes..." -ForegroundColor Yellow
Stop-Process -Name python -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

# Create necessary directories
Write-Host "Creating directories..." -ForegroundColor Yellow
@('data', 'logs', 'wallets', 'reports', 'models') | ForEach-Object {
    if (-not (Test-Path $_)) {
        New-Item -ItemType Directory -Path $_ | Out-Null
    }
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# Start services
Write-Host "Starting data generator..." -ForegroundColor Yellow
$dataGen = Start-Process -FilePath ".\venv\Scripts\python.exe" -ArgumentList "src/enhanced_demo.py" `
    -NoNewWindow -PassThru -RedirectStandardOutput "logs/data_generator.log" -RedirectStandardError "logs/data_generator.err"
Start-Sleep -Seconds 5

Write-Host "Starting dashboard..." -ForegroundColor Yellow
$dashboard = Start-Process -FilePath ".\venv\Scripts\python.exe" -ArgumentList "src/championship_dashboard.py" `
    -NoNewWindow -PassThru -RedirectStandardOutput "logs/dashboard.log" -RedirectStandardError "logs/dashboard.err"

Write-Host "Starting API..." -ForegroundColor Yellow
$api = Start-Process -FilePath ".\venv\Scripts\python.exe" -ArgumentList "src/api/rest_api.py" `
    -NoNewWindow -PassThru -RedirectStandardOutput "logs/api.log" -RedirectStandardError "logs/api.err"

Write-Host "Starting WebSocket server..." -ForegroundColor Yellow
$websocket = Start-Process -FilePath ".\venv\Scripts\python.exe" -ArgumentList "src/api/websocket_server.py" `
    -NoNewWindow -PassThru -RedirectStandardOutput "logs/websocket.log" -RedirectStandardError "logs/websocket.err"

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "✅ ALL SERVICES RUNNING!" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "📊 Dashboard:  http://localhost:8050" -ForegroundColor White
Write-Host "📡 API:        http://localhost:8000/docs" -ForegroundColor White
Write-Host "🔌 WebSocket:  ws://localhost:8765" -ForegroundColor White
Write-Host ""
Write-Host "📝 Process IDs:" -ForegroundColor Yellow
Write-Host "   Data Generator: $($dataGen.Id)"
Write-Host "   Dashboard:      $($dashboard.Id)"
Write-Host "   API:            $($api.Id)"
Write-Host "   WebSocket:      $($websocket.Id)"
Write-Host ""
Write-Host "📝 Logs:" -ForegroundColor Yellow
Write-Host "   Get-Content logs/data_generator.log -Wait"
Write-Host "   Get-Content logs/dashboard.log -Wait"
Write-Host "   Get-Content logs/api.log -Wait"
Write-Host ""
Write-Host "🛑 Stop all:   .\stop_system.ps1" -ForegroundColor Red
Write-Host "======================================================================" -ForegroundColor Cyan
