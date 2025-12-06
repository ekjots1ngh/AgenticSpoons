"""
Benchmark OCaml vs Python performance
"""
import time
import numpy as np
import pandas as pd
from src.utils.ocaml_bridge import ocaml_engine
from src.models.volatility_engine import VolatilityEngine


def generate_test_data(n=1000):
    """Generate synthetic OHLCV data"""
    dates = pd.date_range(end=pd.Timestamp.now(), periods=n, freq='1h')
    prices = 15.0 * np.exp(np.cumsum(np.random.normal(0, 0.02, n)))
    
    df = pd.DataFrame({
        'timestamp': dates,
        'open': prices * np.random.uniform(0.99, 1.01, n),
        'high': prices * np.random.uniform(1.00, 1.02, n),
        'low': prices * np.random.uniform(0.98, 1.00, n),
        'close': prices,
        'volume': np.random.uniform(10000, 100000, n)
    })
    
    return df

print("🏁 AgentSpoons: OCaml vs Python Performance Benchmark\n")
print("="*60)

# Generate test data
df = generate_test_data(1000)
ohlcv_data = df.to_dict('records')

# Benchmark Python
print("\n1️⃣  Python Volatility Calculation")
python_engine = VolatilityEngine(df)

start = time.time()
for _ in range(100):
    vol = python_engine.garman_klass_vol()
python_time = time.time() - start

print(f"   100 iterations: {python_time:.3f}s")
print(f"   Per iteration: {python_time*10:.2f}ms")

# Benchmark OCaml
if ocaml_engine.enabled:
    print("\n2️⃣  OCaml Volatility Calculation")
    
    start = time.time()
    for _ in range(100):
        vol = ocaml_engine.calculate_volatility(ohlcv_data)
    ocaml_time = time.time() - start
    
    print(f"   100 iterations: {ocaml_time:.3f}s")
    print(f"   Per iteration: {ocaml_time*10:.2f}ms")
    
    print("\n" + "="*60)
    print(f"🚀 OCaml is {python_time/ocaml_time:.1f}x FASTER than Python!")
    print("="*60)

else:
    print("\n❌ OCaml engine not available")
    print("   Build with: cd ocaml-engine && dune build")

# Benchmark Greeks calculation
print("\n3️⃣  Greeks Calculation Benchmark")

from src.models.black_scholes import BlackScholesEngine

params = {'S': 15.0, 'K': 16.0, 'T': 0.25, 'r': 0.05, 'sigma': 0.5}

start = time.time()
for _ in range(10000):
    delta = BlackScholesEngine.delta_call(**params)
python_greeks_time = time.time() - start

print(f"   Python: {python_greeks_time:.3f}s for 10k calculations")

if ocaml_engine.enabled:
    start = time.time()
    for _ in range(10000):
        greeks = ocaml_engine.calculate_greeks(
            spot=15.0, strike=16.0, maturity=0.25,
            risk_free_rate=0.05, volatility=0.5
        )
    ocaml_greeks_time = time.time() - start
    
    print(f"   OCaml: {ocaml_greeks_time:.3f}s for 10k calculations")
    print(f"   🚀 OCaml is {python_greeks_time/ocaml_greeks_time:.1f}x FASTER!")

print("\n" + "="*60)
print("💡 For production deployment, OCaml provides:")
print("   - 10-100x faster numerical computation")  
print("   - Type safety (catch bugs at compile time)")
print("   - Used by Jane Street for HFT systems")
print("="*60)
