#!/bin/bash
echo "Setting up Redis..."

if command -v redis-server &> /dev/null; then
    echo "✅ Redis already installed"
else
    echo "Installing Redis..."
    # Ubuntu/Debian
    sudo apt-get update
    sudo apt-get install -y redis-server
    
    # macOS
    # brew install redis
fi

# Start Redis
redis-server --daemonize yes

echo "✅ Redis running on localhost:6379"
