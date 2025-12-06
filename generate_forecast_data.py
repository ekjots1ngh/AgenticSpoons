"""
Generate synthetic time series data for forecasting tests
"""
import numpy as np
import json
from datetime import datetime, timedelta

def generate_synthetic_volatility(n_points=200):
    """Generate realistic volatility time series"""
    
    # Base volatility with trend
    t = np.linspace(0, 10, n_points)
    trend = 0.20 + 0.05 * np.sin(t / 2)
    
    # Add seasonality (intraday pattern)
    seasonality = 0.03 * np.sin(2 * np.pi * t / 24)
    
    # Add GARCH-like clustering
    returns = np.random.normal(0, 0.02, n_points)
    volatility = np.zeros(n_points)
    volatility[0] = 0.20
    
    # GARCH(1,1) simulation
    for i in range(1, n_points):
        volatility[i] = (0.00001 + 
                        0.05 * returns[i-1]**2 + 
                        0.90 * volatility[i-1])
    
    # Combine components
    realized_vol = np.sqrt(trend + seasonality + volatility)
    
    # Add noise
    realized_vol += np.random.normal(0, 0.01, n_points)
    realized_vol = np.clip(realized_vol, 0.05, 0.80)
    
    return realized_vol

# Generate data
print("Generating synthetic data for forecasting tests...")

n_points = 200
base_time = datetime.now() - timedelta(minutes=5*n_points)

data = []

for i in range(n_points):
    timestamp = base_time + timedelta(minutes=5*i)
    
    volatility = generate_synthetic_volatility(n_points)[i]
    
    data.append({
        'timestamp': timestamp.isoformat(),
        'pair': 'NEO/USDT',
        'price': 15.0 + np.random.randn() * 0.5,
        'realized_vol': float(volatility),
        'implied_vol': float(volatility * 1.1),
        'garch_forecast': float(volatility * 1.05),
        'spread': abs(np.random.randn() * 0.02)
    })

# Save
with open('data/results.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"✅ Generated {n_points} data points")
print("   Saved to data/results.json")
print("\nNow run: python src/forecasting/time_series_models.py")
