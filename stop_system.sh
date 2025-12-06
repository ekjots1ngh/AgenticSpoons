#!/bin/bash
echo "Stopping AgentSpoons..."
pkill -f enhanced_demo.py
pkill -f championship_dashboard.py
pkill -f rest_api.py
pkill -f websocket_server.py
echo "✅ All services stopped"
