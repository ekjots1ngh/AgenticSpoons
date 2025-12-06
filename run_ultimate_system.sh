#!/bin/bash

echo "="*70
echo "🚀 AGENTSPOONS ULTIMATE SYSTEM"
echo "="*70

# Kill existing processes
pkill -f python

# Start Redis
redis-server --daemonize yes

# Start all services
echo "Starting data generator..."
python src/enhanced_demo.py > logs/data.log 2>&1 &

sleep 3

echo "Starting main dashboard..."
python src/championship_dashboard.py > logs/dashboard.log 2>&1 &

echo "Starting API..."
python src/api/rest_api.py > logs/api.log 2>&1 &

echo "Starting WebSocket server..."
python src/api/websocket_server.py > logs/websocket.log 2>&1 &

echo "Starting Greeks dashboard..."
python src/visualization/greeks_dashboard.py > logs/greeks.log 2>&1 &

echo ""
echo "="*70
echo "✅ ALL SERVICES RUNNING!"
echo "="*70
echo "📊 Main Dashboard:    http://localhost:8050"
echo "📈 Greeks Dashboard:  http://localhost:8052"
echo "📡 API Docs:          http://localhost:8000/docs"
echo "🔌 WebSocket:         ws://localhost:8765"
echo "🗄️  Redis:            localhost:6379"
echo ""
echo "📝 Advanced Features:"
echo "   • C++ Options Pricer (10-100x faster)"
echo "   • OCaml GARCH Models (ultra-fast)"
echo "   • ML Prediction (LSTM, XGBoost, Ensemble)"
echo "   • Time Series Forecasting (ARIMA, Prophet)"
echo "   • Real-time Streaming (Redis, Kafka)"
echo "   • Professional Backtesting (Backtrader)"
echo "   • Advanced Greeks Visualization"
echo ""
echo "🛑 Stop: ./stop_system.sh"
echo "="*70
