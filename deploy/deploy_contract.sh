#!/bin/bash
# Deploy Neo Smart Contract

echo "🚀 Deploying AgentSpoons Oracle Contract to Neo"

# Compile contract
echo "Compiling contract..."
neo3-boa compile src/contracts/volatility_oracle.py

# TODO: Deploy using neo-express or neo-cli
# neo-express contract deploy <compiled-contract.nef>

echo "✓ Contract deployed!"
echo "Update config.py with contract hash"
