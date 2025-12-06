# AgentSpoons - Stop All Services (Windows)

Write-Host "Stopping AgentSpoons..." -ForegroundColor Yellow
Stop-Process -Name python -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1
Write-Host "✅ All services stopped" -ForegroundColor Green
