#!/bin/bash
# Complete hackathon demo script

echo "🥄 AgentSpoons Hackathon Demo"
echo "=============================="

# Check Python version
python_version=$(python3 --version)
echo "✓ Python: $python_version"

# Activate venv
source venv/bin/activate

# Start agents in background
echo "Starting multi-agent system..."
python src/main.py &
AGENTS_PID=$!

# Wait for data collection
echo "Collecting initial data (60 seconds)..."
sleep 60

# Start dashboard
echo "Starting dashboard on http://localhost:8050"
python src/dashboard/advanced_app.py &
DASHBOARD_PID=$!

echo ""
echo "=============================="
echo "✓ AgentSpoons is running!"
echo "=============================="
echo "Dashboard: http://localhost:8050"
echo "Agents PID: $AGENTS_PID"
echo "Dashboard PID: $DASHBOARD_PID"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for interrupt
trap "kill $AGENTS_PID $DASHBOARD_PID; exit" INT
wait
