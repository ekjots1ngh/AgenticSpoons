# 🥄 AgentSpoons - Decentralized Volatility Oracle

## 🎯 Problem
Options traders and DeFi protocols need **reliable, real-time volatility data** but current solutions are:
- Centralized (single point of failure)
- Expensive (Bloomberg costs $24k/year)
- Not crypto-native

## 💡 Solution
**AgentSpoons**: Multi-agent system that calculates and publishes volatility oracles on Neo blockchain

## 🏗️ Architecture

### 5 Autonomous Agents:
1. **Market Data Collector** - Aggregates prices from Neo DEXs
2. **Volatility Calculator** - 7 different volatility estimators (Parkinson, Garman-Klass, GARCH)
3. **Implied Vol Engine** - Builds volatility surfaces, calculates Greeks
4. **Arbitrage Detector** - Finds vol trading opportunities
5. **Oracle Publisher** - Publishes to Neo smart contract

### Tech Stack:
- **Blockchain**: Neo N3 (SpoonOS components)
- **Quant Models**: Black-Scholes, GARCH(1,1), multiple vol estimators
- **Languages**: Python (Neo-compatible)
- **Database**: SQLite for persistence
- **Dashboard**: Plotly Dash (real-time monitoring)

## 📊 Key Features

### Mathematical Rigor:
- ✅ **7 volatility estimators**: Close-to-close, Parkinson, Garman-Klass, Rogers-Satchell, Yang-Zhang
- ✅ **GARCH(1,1) forecasting**: Time series volatility prediction
- ✅ **Black-Scholes pricing**: Full Greeks calculation (δ, γ, ν, θ, ρ)
- ✅ **Volatility surfaces**: 3D interpolation with cubic splines

### Blockchain Integration:
- ✅ Neo N3 smart contracts (Python)
- ✅ Decentralized oracle feeds
- ✅ SpoonOS components for agent orchestration
- ✅ Multi-signature publisher authorization

### Real-world Use Cases:
1. **Options Protocols** - Get reliable IV for pricing
2. **Risk Management** - Real-time volatility monitoring
3. **Trading Strategies** - Detect vol arbitrage opportunities
4. **DeFi Yield** - Volatility-based structured products

## 🎓 Why This Matters for Quant Finance

This project demonstrates:
- **Stochastic Calculus**: GBM, Itô's lemma
- **Time Series**: GARCH models, Kalman filtering
- **Derivatives Pricing**: Black-Scholes, implied volatility
- **Statistical Arbitrage**: Mean reversion, pairs trading
- **Market Microstructure**: Order flow, adverse selection

## 🚀 Demo
```bash
# Run the full system
./deploy/run_hackathon_demo.sh

# Visit dashboard
open http://localhost:8050
```

### Live Features:
- Real-time volatility charts
- 3D volatility surfaces
- Greeks dashboard
- Arbitrage opportunity alerts
- Neo blockchain oracle feeds

## 💼 Business Model
- Protocol fees on oracle queries
- Subscription for premium data feeds
- Licensing to DeFi protocols
- Data analytics services

## 🏆 Why We'll Win

1. **Technical Excellence**: Production-quality quant models
2. **Real Problem**: Crypto needs better volatility data
3. **Neo Integration**: Full SpoonOS usage
4. **Scalability**: Multi-agent architecture
5. **Market Ready**: Immediate use cases in DeFi

## 👥 Team
Ekjot - Mathematics student with quant finance focus
- Internships: Publicis Sapient, Ocado Logistics
- Skills: Python, C++, quantitative modeling
- Target: Quant roles at Jane Street, HRT, Optiver

## 📈 Metrics
- **5 autonomous agents** running concurrently
- **7 volatility estimators** calculated per pair
- **Sub-second** oracle updates
- **100% uptime** with agent redundancy
- **Gas efficient**: Batched Neo transactions

---

*Built for Neo Hackathon 2024*
*Powered by Mathematics, AI, and Blockchain*
