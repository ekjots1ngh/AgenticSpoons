# 🥄 AgentSpoons - Decentralized Volatility Oracle

Multi-agent system for calculating and publishing volatility data on Neo blockchain.

## Features
- Real-time volatility calculation (GARCH, Parkinson, Garman-Klass)
- Implied volatility surface construction
- Black-Scholes pricing & Greeks
- Statistical arbitrage detection
- Neo blockchain integration

## Setup
```bash
# Clone and setup
git clone <your-repo>
cd agentspoons
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Run
python src/main.py
```

## Architecture
- **Agent 1**: Market Data Collector
- **Agent 2**: Volatility Calculator
- **Agent 3**: Implied Vol Engine
- **Agent 4**: Oracle Publisher (Neo)
- **Agent 5**: Arbitrage Detector

## Tech Stack
- Python 3.10+
- Neo N3 Blockchain
- SpoonOS Components
- NumPy, SciPy, pandas
- ARCH (GARCH models)
- Plotly/Dash (dashboard)

Built for Neo Hackathon 2024
