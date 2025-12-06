"""
Run volatility backtests and generate report
"""
import json
import numpy as np
from src.models.advanced_garch import AdvancedGARCH, VolatilityBacktest, VolArbitrageStrategy

print("="*70)
print("📊 AGENTSPOONS BACKTEST ENGINE")
print("="*70)

# Load data
try:
    with open('data/results.json', 'r') as f:
        data = json.load(f)
except FileNotFoundError:
    print("❌ data/results.json not found. Run system first.")
    exit(1)

neo_data = [d for d in data if d.get('pair') == 'NEO/USDT']

if len(neo_data) < 100:
    print(f"❌ Need at least 100 data points. Have {len(neo_data)}. Run system longer.")
    exit(1)

# Extract returns
prices = [d['price'] for d in neo_data]
returns = np.diff(np.log(prices))

print(f"\n✅ Loaded {len(returns)} returns for backtesting")

# Test 1: GARCH Model
print("\n1️⃣  GARCH(1,1) Model Fitting")
print("-" * 70)
garch = AdvancedGARCH(returns)
params = garch.fit_garch_11()

print(f"   ω (omega):     {params['omega']:.6f}")
print(f"   α (alpha):     {params['alpha']:.4f}")
print(f"   β (beta):      {params['beta']:.4f}")
print(f"   Persistence:   {params['persistence']:.4f}")
print(f"   Long-run Vol:  {params['long_run_vol']:.2%}")
print(f"   Log-Likelihood: {params['log_likelihood']:.2f}")

# Test 2: Forecast Accuracy
print("\n2️⃣  Volatility Forecast Backtest")
print("-" * 70)

if len(returns) > 300:
    backtest = VolatilityBacktest(returns, window=252)
    results = backtest.rolling_forecast_test()
    
    print(f"   RMSE:          {results['rmse']:.4f}")
    print(f"   MAE:           {results['mae']:.4f}")
    print(f"   Directional:   {results['directional_accuracy']:.2%}")
    print(f"   N Forecasts:   {results['n_forecasts']}")
else:
    print(f"   ⏳ Need more data for forecast backtest (300+ points, have {len(returns)})")

# Test 3: Trading Strategy
print("\n3️⃣  Volatility Arbitrage Strategy")
print("-" * 70)

strategy = VolArbitrageStrategy(neo_data)
strat_results = strategy.run_backtest(threshold=0.05)

if 'error' not in strat_results:
    print(f"   Total P&L:     ${strat_results['total_pnl']:.2f}")
    print(f"   Trades:        {strat_results['n_trades']}")
    print(f"   Win Rate:      {strat_results['win_rate']:.2%}")
    print(f"   Sharpe Ratio:  {strat_results['sharpe_ratio']:.2f}")
    print(f"   Max Drawdown:  ${strat_results['max_drawdown']:.2f}")
else:
    print(f"   {strat_results['error']}")

print("\n" + "="*70)
print("💡 Interpretation:")
print("   • Sharpe > 1.0 = Good strategy")
print("   • Win Rate > 55% = Profitable edge")
print("   • Directional > 60% = Forecast skill")
print("="*70)
