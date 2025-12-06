"""
Quick test script to verify all components work
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from src.models.volatility_engine import VolatilityEngine
from src.models.black_scholes import BlackScholesEngine
from src.models.garch_forecaster import GARCHForecaster
from src.models.volatility_surface import VolatilitySurface

def generate_test_data(n=100):
    """Generate synthetic OHLCV data"""
    dates = pd.date_range(end=datetime.now(), periods=n, freq='1h')
    
    # Simulate GBM
    S0 = 15.0
    mu = 0.0001
    sigma = 0.02
    
    returns = np.random.normal(mu, sigma, n)
    prices = S0 * np.exp(np.cumsum(returns))
    
    df = pd.DataFrame({
        'timestamp': dates,
        'open': prices * np.random.uniform(0.99, 1.01, n),
        'high': prices * np.random.uniform(1.00, 1.02, n),
        'low': prices * np.random.uniform(0.98, 1.00, n),
        'close': prices,
        'volume': np.random.uniform(10000, 100000, n)
    })
    
    return df

def test_volatility_engine():
    """Test volatility calculations"""
    print("\n" + "="*60)
    print("Testing Volatility Engine")
    print("="*60)
    
    df = generate_test_data(100)
    engine = VolatilityEngine(df)
    
    print(f"Close-to-Close Vol: {engine.close_to_close_vol():.2%}")
    print(f"Parkinson Vol:      {engine.parkinson_vol():.2%}")
    print(f"Garman-Klass Vol:   {engine.garman_klass_vol():.2%}")
    print(f"Yang-Zhang Vol:     {engine.yang_zhang_vol():.2%}")
    print("✓ Volatility engine working!")

def test_black_scholes():
    """Test BS pricing and IV calculation"""
    print("\n" + "="*60)
    print("Testing Black-Scholes Engine")
    print("="*60)
    
    S, K, T, r, sigma = 15.0, 15.0, 0.25, 0.05, 0.50
    
    call_price = BlackScholesEngine.call_price(S, K, T, r, sigma)
    put_price = BlackScholesEngine.put_price(S, K, T, r, sigma)
    
    print(f"Call Price: ${call_price:.2f}")
    print(f"Put Price:  ${put_price:.2f}")
    
    # Test IV calculation
    iv = BlackScholesEngine.implied_volatility(call_price, S, K, T, r, 'call')
    print(f"Implied Vol (should be ~{sigma:.2%}): {iv:.2%}")
    
    # Test Greeks
    delta = BlackScholesEngine.delta_call(S, K, T, r, sigma)
    gamma = BlackScholesEngine.gamma(S, K, T, r, sigma)
    vega = BlackScholesEngine.vega(S, K, T, r, sigma)
    
    print(f"Delta: {delta:.4f}")
    print(f"Gamma: {gamma:.4f}")
    print(f"Vega:  {vega:.4f}")
    print("✓ Black-Scholes engine working!")

def test_garch():
    """Test GARCH forecasting"""
    print("\n" + "="*60)
    print("Testing GARCH Forecaster")
    print("="*60)
    
    df = generate_test_data(200)
    engine = VolatilityEngine(df)
    
    garch = GARCHForecaster(engine.returns)
    params = garch.fit()
    
    print(f"GARCH Parameters:")
    print(f"  ω (omega): {params['omega']:.6f}")
    print(f"  α (alpha): {params['alpha']:.4f}")
    print(f"  β (beta):  {params['beta']:.4f}")
    print(f"  Persistence: {params['persistence']:.4f}")
    
    forecast = garch.forecast(horizon=1)
    print(f"1-day forecast: {forecast:.2%}")
    print("✓ GARCH forecaster working!")

def test_vol_surface():
    """Test volatility surface"""
    print("\n" + "="*60)
    print("Testing Volatility Surface")
    print("="*60)
    
    surface = VolatilitySurface()
    spot = 15.0
    
    # Add synthetic points
    strikes = [12, 13, 14, 15, 16, 17, 18]
    maturities = [0.08, 0.25, 0.5]  # 1M, 3M, 6M
    
    for K in strikes:
        for T in maturities:
            moneyness = K / spot
            vol = 0.50 + 0.1 * abs(1 - moneyness)  # Simple smile
            surface.add_point(K, T, vol)
    
    surface.spot_price = spot
    surface.build_surface()
    
    atm_term = surface.get_atm_term_structure(spot)
    print(f"ATM Term Structure:")
    for T, vol in atm_term.items():
        print(f"  {T*365:.0f} days: {vol:.2%}")
    
    skew = surface.calculate_skew(0.25)
    print(f"3M Vol Skew: {skew:.2%}")
    print("✓ Volatility surface working!")

if __name__ == "__main__":
    print("\n🧪 Running AgentSpoons Component Tests\n")
    
    test_volatility_engine()
    test_black_scholes()
    test_garch()
    test_vol_surface()
    
    print("\n" + "="*60)
    print("✅ All tests passed! System ready.")
    print("="*60)
    print("\nRun the full system with: python src/main.py")
