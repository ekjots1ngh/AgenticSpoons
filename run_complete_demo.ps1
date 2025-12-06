# AgentSpoons - Complete Demo Script (Windows)
# Runs all system components to generate impressive demo data

$ErrorActionPreference = "Continue"

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "🚀 AGENTSPOONS - COMPLETE SYSTEM DEMO" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Step 1: Generate Demo Data
Write-Host "📊 Step 1/8: Generating impressive demo data..." -ForegroundColor Yellow
$demoProcess = Start-Process -FilePath ".\venv\Scripts\python.exe" -ArgumentList "src/enhanced_demo.py" `
    -NoNewWindow -PassThru
Start-Sleep -Seconds 10
Stop-Process -Id $demoProcess.Id -Force -ErrorAction SilentlyContinue
Write-Host "✅ Demo data generated" -ForegroundColor Green
Write-Host ""

# Step 2: Train ML Model
Write-Host "🤖 Step 2/8: Training ML volatility prediction model..." -ForegroundColor Yellow
python src/ml/volatility_predictor.py
Write-Host "✅ ML model trained" -ForegroundColor Green
Write-Host ""

# Step 3: Run Backtest
Write-Host "📈 Step 3/8: Running backtest..." -ForegroundColor Yellow
if (Test-Path "run_backtest.py") {
    python run_backtest.py
    Write-Host "✅ Backtest complete" -ForegroundColor Green
} else {
    Write-Host "⚠️  Backtest script not found, skipping..." -ForegroundColor Yellow
}
Write-Host ""

# Step 4: Generate PDF Report
Write-Host "📄 Step 4/8: Generating PDF report..." -ForegroundColor Yellow
python src/reports/pdf_generator.py
Write-Host "✅ PDF report generated" -ForegroundColor Green
Write-Host ""

# Step 5: Create 3D Volatility Surface
Write-Host "🎨 Step 5/8: Creating 3D volatility surface..." -ForegroundColor Yellow
python -c @"
from src.visualization.vol_surface_3d import VolatilitySurface3D
import plotly.offline as pyo
surf = VolatilitySurface3D()
fig = surf.generate_sample_surface()
pyo.plot(fig, filename='data/vol_surface.html', auto_open=False)
print('✅ 3D surface created: data/vol_surface.html')
"@
Write-Host ""

# Step 6: Setup Neo Wallet
Write-Host "🔐 Step 6/8: Setting up Neo wallet..." -ForegroundColor Yellow
if (Test-Path "setup_neo.py") {
    python setup_neo.py
    Write-Host "✅ Neo wallet configured" -ForegroundColor Green
} else {
    Write-Host "⚠️  Neo setup script not found, skipping..." -ForegroundColor Yellow
}
Write-Host ""

# Step 7: Start Services
Write-Host "🌐 Step 7/8: Starting all services..." -ForegroundColor Yellow
.\run_full_system.ps1
Write-Host ""

# Step 8: Test API Endpoints
Write-Host "🧪 Step 8/8: Testing API endpoints..." -ForegroundColor Yellow
Start-Sleep -Seconds 5  # Wait for services to start

Write-Host "Testing health endpoint..." -ForegroundColor Cyan
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get
    $health | ConvertTo-Json
} catch {
    Write-Host "⚠️  API not ready yet" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Testing volatility endpoint..." -ForegroundColor Cyan
try {
    $vol = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/volatility/NEO-USDT" -Method Get
    $vol | ConvertTo-Json
} catch {
    Write-Host "⚠️  API not ready yet" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "✅ DEMO COMPLETE!" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📊 Generated Assets:" -ForegroundColor Yellow
Write-Host "   • data/results.json - Market data"
Write-Host "   • models/ml_vol_predictor.pkl - Trained ML model"
Write-Host "   • reports/volatility_report_*.pdf - PDF report"
Write-Host "   • data/vol_surface.html - 3D visualization"
Write-Host ""
Write-Host "🌐 Running Services:" -ForegroundColor Yellow
Write-Host "   • Dashboard:  http://localhost:8050" -ForegroundColor White
Write-Host "   • API:        http://localhost:8000/docs" -ForegroundColor White
Write-Host "   • WebSocket:  ws://localhost:8765" -ForegroundColor White
Write-Host ""
Write-Host "📝 View Logs:" -ForegroundColor Yellow
Write-Host "   Get-Content logs/data_generator.log -Wait"
Write-Host "   Get-Content logs/dashboard.log -Wait"
Write-Host "   Get-Content logs/api.log -Wait"
Write-Host ""
Write-Host "🛑 Stop Services:" -ForegroundColor Red
Write-Host "   .\stop_system.ps1"
Write-Host "======================================================================" -ForegroundColor Cyan
