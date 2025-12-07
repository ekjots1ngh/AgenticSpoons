# AgentSpoons Demo Video Script (3 minutes)

## [0:00-0:20] Hook & Problem (20s)
**Visual**: Show expensive Bloomberg terminal, then cross it out
**Narration**: 
"DeFi options protocols need reliable volatility data. Traditional providers like Bloomberg cost $24,000 per year and create centralized points of failure. What if we could provide institutional-quality volatility data, decentralized on Neo blockchain, at 95% lower cost?"

## [0:20-0:40] Solution Introduction (20s)
**Visual**: AgentSpoons logo animation, then architecture diagram
**Narration**:
"AgentSpoons is a multi-agent autonomous system that calculates real-time cryptocurrency volatility using seven cross-validated models, GARCH forecasting, and machine learning—all published to Neo N3 blockchain every 5 minutes."

## [0:40-1:40] Live Demo (60s)
**Visual**: Screen recording of dashboard
**Narration**:
"Here's the live system. Five autonomous agents work in parallel:
- Agent 1 collects prices from DEXs every 30 seconds
- Agent 2 calculates volatility using 7 different estimators
- Agent 3 builds implied volatility surfaces
- Agent 4 detects arbitrage opportunities
- Agent 5 publishes everything to Neo blockchain

[Point to dashboard] You can see realized volatility at 52%, implied at 58%—that 6% spread represents a trading opportunity. The GARCH model forecasts volatility will increase to 54% tomorrow."

## [1:40-2:20] Neo Integration (40s)
**Visual**: NeoTube explorer showing contract
**Narration**:
"This is the live Neo N3 smart contract. Every 5 minutes, new volatility data is published on-chain. Any DApp can query this for free—zero gas for reads. 

[Show code] The contract stores price, realized vol, implied vol, and timestamp. DeFi protocols use this to price options, manage risk, and build derivatives.

[Show transaction] Here's a real transaction—0.01 GAS to update, about 30 cents. That's 99% cheaper than centralized oracles."

## [2:20-2:50] Technical Excellence (30s)
**Visual**: Code editor, then benchmark charts
**Narration**:
"I optimized critical paths in C++ and OCaml, achieving 10 to 100 times speedup. The system processes over 1,000 calculations per second with sub-50 millisecond latency.

Professional backtesting shows 87% forecast accuracy and a Sharpe ratio of 1.82. I built this with 95% test coverage, comprehensive documentation, and a full CI/CD pipeline."

## [2:50-3:00] Close (10s)
**Visual**: Contact info and GitHub
**Narration**:
"AgentSpoons enables a $10 million options market on Neo while reducing costs by 95%. I'm Ekjot Singh, mathematics student at City University London, and I built this to demonstrate production-grade quantitative system design. Thank you."

---

# Recording Checklist:
- [ ] Record in 1080p minimum
- [ ] Use clear microphone (no background noise)
- [ ] Show live dashboard with real data updating
- [ ] Show Neo contract on NeoTube explorer
- [ ] Show actual code in editor
- [ ] Display GitHub repo at end
- [ ] Keep total under 3 minutes
- [ ] Export as MP4

# Tools:
- OBS Studio (free, best for screen recording)
- Audacity (audio editing)
- DaVinci Resolve (video editing, free)

# Pro Tips:
1. **Practice run**: Record 2-3 practice versions first
2. **Energy**: Speak with enthusiasm but not too fast
3. **Visuals**: Show REAL working demo, not slides
4. **Timing**: Use a timer visible on screen
5. **B-roll**: Record extra footage of dashboard/code
6. **Audio**: Record in quiet room, use pop filter
7. **Editing**: Cut any pauses longer than 2 seconds
8. **Export**: H.264, 1080p, 30fps, MP4 format

# What to Show On-Screen:
- **Dashboard**: Live volatility calculations updating
- **NeoTube**: Your deployed contract with transactions
- **Code**: Neo smart contract source (volatility_oracle.py)
- **SpoonOS**: Multi-agent orchestration demo
- **Terminal**: Live publishing demo running
- **GitHub**: Final slide with repo link

# Upload:
- YouTube as "unlisted" (not private, not public)
- Title: "AgentSpoons - Decentralized Volatility Oracle on Neo N3"
- Include in hackathon submission
