"""
Real-time data generator for AgentSpoons
Simple, reliable, no dependencies on complex features
"""
import json
import time
from datetime import datetime
import numpy as np
from pathlib import Path


class SimpleDataGenerator:
    """Generate realistic volatility data"""

    def __init__(self):
        self.data_file = Path('data/live_data.json')
        self.data_file.parent.mkdir(exist_ok=True)

        # Initialize state
        self.price = 15.23
        self.rv = 0.52
        self.iv = 0.58

        # History for charts
        self.price_history = []
        self.rv_history = []
        self.iv_history = []
        self.timestamps = []

    def generate_tick(self):
        """Generate one data point"""

        # Random walk for price
        self.price *= (1 + np.random.normal(0, 0.002))
        self.price = max(10, min(20, self.price))  # Keep in range

        # Random walk for volatility
        self.rv += np.random.normal(0, 0.005)
        self.rv = max(0.3, min(0.8, self.rv))

        # IV follows RV but with spread
        spread = np.random.uniform(0.05, 0.12)
        self.iv = self.rv * (1 + spread)

        # Store in history
        now = datetime.now()
        self.price_history.append(self.price)
        self.rv_history.append(self.rv)
        self.iv_history.append(self.iv)
        self.timestamps.append(now.isoformat())

        # Keep only last 100 points
        if len(self.price_history) > 100:
            self.price_history.pop(0)
            self.rv_history.pop(0)
            self.iv_history.pop(0)
            self.timestamps.pop(0)

        # Calculate metrics
        price_change = (
            (
                (self.price - self.price_history[-2])
                / self.price_history[-2]
                * 100
            )
            if len(self.price_history) > 1
            else 0
        )
        spread = self.iv - self.rv

        # Create data object
        data = {
            'timestamp': now.isoformat(),
            'price': round(self.price, 2),
            'price_change': round(price_change, 2),
            'realized_vol': round(self.rv, 4),
            'implied_vol': round(self.iv, 4),
            'spread': round(spread, 4),
            'garch_forecast': round(self.rv * np.random.uniform(0.98, 1.05), 4),
            'history': {
                'timestamps': self.timestamps[-50:],  # Last 50 for charts
                'prices': [round(p, 2) for p in self.price_history[-50:]],
                'rv': [round(v, 4) for v in self.rv_history[-50:]],
                'iv': [round(v, 4) for v in self.iv_history[-50:]],
            },
        }

        return data

    def save_data(self, data):
        """Save to JSON file"""
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)

    def run_forever(self, interval=2):
        """Run continuously"""
        print("🚀 Data generator started")
        print(f"📁 Writing to: {self.data_file}")
        print(f"⏱️  Update interval: {interval}s")
        print("Press Ctrl+C to stop\n")

        try:
            while True:
                data = self.generate_tick()
                self.save_data(data)

                # Print status
                print(
                    f"[{data['timestamp'][:19]}] "
                    f"Price: ${data['price']:.2f} "
                    f"({data['price_change']:+.2f}%) | "
                    f"RV: {data['realized_vol']:.2%} | "
                    f"IV: {data['implied_vol']:.2%} | "
                    f"Spread: {data['spread']:.2%}"
                )

                time.sleep(interval)

        except KeyboardInterrupt:
            print("\n✅ Data generator stopped")


if __name__ == "__main__":
    generator = SimpleDataGenerator()
    generator.run_forever(interval=2)
