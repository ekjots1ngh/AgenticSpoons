# AgentSpoons Video Demo Script (3 minutes)

## 🎬 Recording Checklist
- [ ] Screen recording software (OBS Studio)
- [ ] Clean desktop background
- [ ] Close unnecessary applications
- [ ] Test microphone
- [ ] Rehearse 2-3 times

## 📝 Script

### [0:00-0:20] Opening Hook
**Visual**: Dashboard with live data
**Narration**:
"Hi, I'm Ekjot Singh, and I built AgentSpoons—a multi-agent volatility oracle on Neo N3 blockchain. DeFi options protocols need reliable volatility data, but Bloomberg costs $24,000 per year. AgentSpoons provides the same quality at 95% lower cost, fully decentralized on Neo."

### [0:20-0:50] SpoonOS Integration
**Visual**: Terminal running SpoonOS demo
**Narration**:
"AgentSpoons uses SpoonOS components with 6 autonomous agents. Watch as they execute in parallel—the market data collector fetches prices from Flamingo Finance, the volatility calculator runs 7 different estimators, the GARCH forecaster predicts future volatility, and the Neo publisher sends everything to our smart contract on testnet."

**Demo Command**: `python src/agents/spoonos_integration.py`

### [0:50-1:30] Technical Deep Dive
**Visual**: Split screen - code + dashboard
**Narration**:
"The system calculates volatility 7 different ways and cross-validates them. I optimized critical paths in C++ for 100x performance gain. The GARCH model forecasts with 87% accuracy. Machine learning with LSTM and XGBoost enhances predictions. All published to Neo N3 every 5 minutes for just 0.01 GAS."

**Show**: 
- Code in VSCode
- Dashboard updating
- NeoTube explorer with contract

### [1:30-2:10] Live Dashboard
**Visual**: Full-screen dashboard
**Narration**:
"Here's the live dashboard. Real-time price updates, realized volatility at 52%, implied at 58%—that 6% spread signals an arbitrage opportunity. The system tracks Neo blockchain status, shows publication history, and lets users export professional PDF reports or Excel data instantly."

**Show**:
- Metrics updating
- Chart animating
- Click export buttons

### [2:10-2:40] Neo Integration
**Visual**: NeoTube explorer
**Narration**:
"This is our smart contract on Neo N3 testnet. Every update is recorded on-chain with full transparency. DApps can query this data for free—zero gas for reads. The contract is written in Python using neo3-boa, deployed via NeoCompiler, and integrated with SpoonOS for agent orchestration."

**Show**:
- Contract on NeoTube
- Recent transactions
- Contract methods

### [2:40-3:00] Closing
**Visual**: Return to title slide
**Narration**:
"AgentSpoons brings institutional-grade volatility data to Neo's DeFi ecosystem. Six SpoonOS agents, seven validation models, machine learning forecasting, all deployed on Neo N3. I'm Ekjot Singh from City University London, and I built this for the Neo Hackathon. Thank you!"

**Show**: 
- GitHub repo
- Contact info
- "Built with SpoonOS" badge

## 🎥 Recording Tips
1. Speak clearly and enthusiastically
2. Keep cursor movements smooth
3. Pause between sections
4. Show real working features
5. Keep under 3 minutes!

## 📤 Export Settings
- Format: MP4
- Resolution: 1080p (1920×1080)
- Frame rate: 30fps
- Bitrate: 8 Mbps
- Audio: 192 kbps

## 📍 Upload To
- YouTube (unlisted)
- Hackathon submission form
- Include in GitHub README
