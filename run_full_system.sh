#!/bin/bash

echo "======================================================================"
echo "🚀 AGENTSPOONS - FULL SYSTEM STARTUP"
echo "======================================================================"

# Kill any existing processes
pkill -f enhanced_demo.py
pkill -f championship_dashboard.py
pkill -f rest_api.py
pkill -f websocket_server.py

# Create necessary directories
mkdir -p data logs wallets reports models

# Start services
echo "Starting data generator..."
python src/enhanced_demo.py > logs/data_generator.log 2>&1 &
sleep 5

echo "Starting dashboard..."
python src/championship_dashboard.py > logs/dashboard.log 2>&1 &

echo "Starting API..."
python src/api/rest_api.py > logs/api.log 2>&1 &

echo "Starting WebSocket server..."
python src/api/websocket_server.py > logs/websocket.log 2>&1 &

echo ""
echo "======================================================================"
echo "✅ ALL SERVICES RUNNING!"
echo "======================================================================"
echo "📊 Dashboard:  http://localhost:8050"
echo "📡 API:        http://localhost:8000/docs"
echo "🔌 WebSocket:  ws://localhost:8765"
echo ""
echo "📝 Logs:"
echo "   tail -f logs/data_generator.log"
echo "   tail -f logs/dashboard.log"
echo "   tail -f logs/api.log"
echo ""
echo "🛑 Stop all:   ./stop_system.sh"
echo "======================================================================"
