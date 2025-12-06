# 3-Minute Winning Demo Script

## [0:00-0:30] HOOK
"Options markets need reliable volatility data. Without it, they can't price contracts. Current solutions cost $24,000/year and are centralized. AgentSpoons solves this with autonomous agents on Neo blockchain."

## [0:30-1:30] LIVE DEMO
[OPEN DASHBOARD - FULL SCREEN]

"This is live data, updating every 3 seconds:

[POINT TO METRICS]
- NEO price: $15.23
- Realized volatility: 52% (calculated from price history)
- Implied volatility: 58% (from options market)
- Spread: 6% - this is an arbitrage signal

[POINT TO CHARTS]
- Green line: actual historical volatility
- Red line: what the market thinks volatility will be
- When red > green, it's a trading opportunity

[WATCH NUMBERS UPDATE]
See - it just updated. This is live."

## [1:30-2:00] TECHNICAL
"Under the hood:
- 5 autonomous agents collecting data, calculating volatility
- GARCH(1,1) model for forecasting - same as used at hedge funds
- Black-Scholes engine with full Greeks
- Published to Neo smart contract every 5 minutes

[SHOW TERMINAL]
Here's the system running - you can see the agents working."

## [2:00-2:30] NEO INTEGRATION
"Our Neo smart contract stores this data on-chain. Any DApp can query:
```python
volatility = contract.get_volatility('NEO/USDT')
# Returns: {'realized': 0.52, 'implied': 0.58}
```

Use cases:
- Options DEXs price contracts
- Lending protocols adjust collateral
- New volatility derivatives"

## [2:30-3:00] CLOSE
"Why this wins:
1. Solves real problem - DeFi needs this
2. Production-quality implementation
3. Native Neo integration
4. Clear revenue model - $0.30 per query
5. I'm a math student targeting quant roles - this demonstrates I can build real systems

Questions?"

---

## BODY LANGUAGE:
- Stand confidently
- Make eye contact
- Point at screen when explaining
- Smile when showing live updates
- Slow down when explaining technical parts

## ENERGY LEVEL:
- Start: HIGH (hook them)
- Middle: STEADY (explain clearly)
- End: HIGH (confident close)

## IF TECHNICAL QUESTIONS:
"Great question - let me show you the code..."
[Be ready to show: GARCH model, volatility calculation, smart contract]
