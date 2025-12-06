# Complete hackathon demo script
# PowerShell version

Write-Host "🥄 AgentSpoons Hackathon Demo" -ForegroundColor Cyan
Write-Host "==============================" -ForegroundColor Cyan

# Check Python version
$pythonVersion = python --version
Write-Host "✓ Python: $pythonVersion" -ForegroundColor Green

# Activate venv
& ".\venv\Scripts\Activate.ps1"

# Start agents in background
Write-Host "Starting multi-agent system..." -ForegroundColor Yellow
$agentsJob = Start-Job -ScriptBlock { 
    Set-Location $using:PWD
    & ".\venv\Scripts\python.exe" src/main.py 
}

# Wait for data collection
Write-Host "Collecting initial data (60 seconds)..." -ForegroundColor Yellow
Start-Sleep -Seconds 60

# Start dashboard
Write-Host "Starting dashboard on http://localhost:8050" -ForegroundColor Yellow
$dashboardJob = Start-Job -ScriptBlock { 
    Set-Location $using:PWD
    & ".\venv\Scripts\python.exe" src/dashboard/advanced_app.py 
}

Write-Host ""
Write-Host "==============================" -ForegroundColor Green
Write-Host "✓ AgentSpoons is running!" -ForegroundColor Green
Write-Host "==============================" -ForegroundColor Green
Write-Host "Dashboard: http://localhost:8050" -ForegroundColor Cyan
Write-Host "Agents Job ID: $($agentsJob.Id)" -ForegroundColor Gray
Write-Host "Dashboard Job ID: $($dashboardJob.Id)" -ForegroundColor Gray
Write-Host ""
Write-Host "Press Ctrl+C to stop all services" -ForegroundColor Yellow

# Wait for interrupt
try {
    while ($true) {
        Start-Sleep -Seconds 1
    }
}
finally {
    Write-Host "`nStopping services..." -ForegroundColor Yellow
    Stop-Job -Id $agentsJob.Id
    Stop-Job -Id $dashboardJob.Id
    Remove-Job -Id $agentsJob.Id
    Remove-Job -Id $dashboardJob.Id
    Write-Host "✓ All services stopped" -ForegroundColor Green
}
