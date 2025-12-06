#!/bin/bash
# AgentSpoons - Complete Demo Script
# Runs all system components to generate impressive demo data

set -e  # Exit on error

echo "======================================================================"
echo "🚀 AGENTSPOONS - COMPLETE SYSTEM DEMO"
echo "======================================================================"
echo ""

# Step 1: Generate Demo Data
echo "📊 Step 1/8: Generating impressive demo data..."
python src/enhanced_demo.py &
DEMO_PID=$!
sleep 10
kill $DEMO_PID 2>/dev/null || true
echo "✅ Demo data generated"
echo ""

# Step 2: Train ML Model
echo "🤖 Step 2/8: Training ML volatility prediction model..."
python src/ml/volatility_predictor.py
echo "✅ ML model trained"
echo ""

# Step 3: Run Backtest
echo "📈 Step 3/8: Running backtest..."
if [ -f "run_backtest.py" ]; then
    python run_backtest.py
    echo "✅ Backtest complete"
else
    echo "⚠️  Backtest script not found, skipping..."
fi
echo ""

# Step 4: Generate PDF Report
echo "📄 Step 4/8: Generating PDF report..."
python src/reports/pdf_generator.py
echo "✅ PDF report generated"
echo ""

# Step 5: Create 3D Volatility Surface
echo "🎨 Step 5/8: Creating 3D volatility surface..."
python -c "
from src.visualization.vol_surface_3d import VolatilitySurface3D
import plotly.offline as pyo
surf = VolatilitySurface3D()
fig = surf.generate_sample_surface()
pyo.plot(fig, filename='data/vol_surface.html', auto_open=False)
print('✅ 3D surface created: data/vol_surface.html')
"
echo ""

# Step 6: Setup Neo Wallet
echo "🔐 Step 6/8: Setting up Neo wallet..."
if [ -f "setup_neo.py" ]; then
    python setup_neo.py
    echo "✅ Neo wallet configured"
else
    echo "⚠️  Neo setup script not found, skipping..."
fi
echo ""

# Step 7: Start Services
echo "🌐 Step 7/8: Starting all services..."
./run_full_system.sh
echo ""

# Step 8: Test API Endpoints
echo "🧪 Step 8/8: Testing API endpoints..."
sleep 5  # Wait for services to start

echo "Testing health endpoint..."
curl -s http://localhost:8000/health | python -m json.tool || echo "⚠️  API not ready yet"

echo ""
echo "Testing volatility endpoint..."
curl -s http://localhost:8000/api/v1/volatility/NEO-USDT | python -m json.tool || echo "⚠️  API not ready yet"

echo ""
echo "======================================================================"
echo "✅ DEMO COMPLETE!"
echo "======================================================================"
echo ""
echo "📊 Generated Assets:"
echo "   • data/results.json - Market data"
echo "   • models/ml_vol_predictor.pkl - Trained ML model"
echo "   • reports/volatility_report_*.pdf - PDF report"
echo "   • data/vol_surface.html - 3D visualization"
echo ""
echo "🌐 Running Services:"
echo "   • Dashboard:  http://localhost:8050"
echo "   • API:        http://localhost:8000/docs"
echo "   • WebSocket:  ws://localhost:8765"
echo ""
echo "📝 View Logs:"
echo "   tail -f logs/data_generator.log"
echo "   tail -f logs/dashboard.log"
echo "   tail -f logs/api.log"
echo ""
echo "🛑 Stop Services:"
echo "   ./stop_system.sh"
echo "======================================================================"
