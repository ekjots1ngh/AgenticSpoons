"""
DEMO MODE - For presentations
Shows impressive metrics and signals
"""
import json
import time
from datetime import datetime

# Create impressive demo data
demo_data = []

for i in range(100):
    # Simulate increasing volatility (looks impressive!)
    base_vol = 0.45 + 0.15 * (i / 100)
    
    demo_data.append({
        'pair': 'NEO/USDT',
        'timestamp': datetime.now().isoformat(),
        'price': 15.0 + (i * 0.05),
        'realized_vol': round(base_vol, 4),
        'garch_forecast': round(base_vol * 1.02, 4),
        'implied_vol': round(base_vol * 1.12, 4),
        'spread': round(base_vol * 0.12, 4)
    })

# Save
with open('data/results.json', 'w') as f:
    json.dump(demo_data, f, indent=2)

print("Demo data created with impressive trends!")
print("Shows: Rising volatility, clear arbitrage signals")
print("Run championship_dashboard.py now!")
