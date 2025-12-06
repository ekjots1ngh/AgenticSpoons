"""
AgentSpoons - FIXED Demo Version
"""
import asyncio
import json
import os
from datetime import datetime

import numpy as np


class DataGenerator:
    def __init__(self):
        self.current_price = {"NEO/USDT": 15.0, "GAS/USDT": 3.5}
        self.history = {"NEO/USDT": [], "GAS/USDT": []}

    def generate_tick(self, pair):
        price = self.current_price[pair]
        change = np.random.normal(0, 0.02)
        new_price = price * (1 + change)
        self.current_price[pair] = new_price

        candle = {
            "timestamp": datetime.now().isoformat(),
            "open": price * np.random.uniform(0.99, 1.01),
            "high": new_price * np.random.uniform(1.00, 1.02),
            "low": new_price * np.random.uniform(0.98, 1.00),
            "close": new_price,
            "volume": np.random.uniform(50000, 150000),
        }

        self.history[pair].append(candle)
        if len(self.history[pair]) > 100:
            self.history[pair] = self.history[pair][-100:]

        return candle


class SimpleVolCalculator:
    @staticmethod
    def calculate(candles):
        if len(candles) < 2:
            return 0.5

        gk = []
        for c in candles[-min(30, len(candles)) :]:
            hl = np.log(c["high"] / c["low"])
            co = np.log(c["close"] / c["open"])
            gk.append(0.5 * hl ** 2 - (2 * np.log(2) - 1) * co ** 2)

        if not gk:
            return 0.5

        mean_gk = max(np.mean(gk), 1e-6)
        return float(np.sqrt(252 * mean_gk) + 1e-4)


class AgentSpoons:
    def __init__(self):
        self.data_gen = DataGenerator()
        self.vol_calc = SimpleVolCalculator()
        self.results = []

        os.makedirs("data", exist_ok=True)

        print("Generating initial data...")
        for _ in range(50):
            for pair in ["NEO/USDT", "GAS/USDT"]:
                self.data_gen.generate_tick(pair)
        print("Initial data ready")

    async def run_cycle(self):
        for pair in ["NEO/USDT", "GAS/USDT"]:
            candle = self.data_gen.generate_tick(pair)
            vol = self.vol_calc.calculate(self.data_gen.history[pair])
            garch_forecast = vol * np.random.uniform(0.95, 1.05)
            implied_vol = vol * np.random.uniform(1.05, 1.15)

            result = {
                "pair": pair,
                "timestamp": datetime.now().isoformat(),
                "price": round(candle["close"], 2),
                "realized_vol": round(vol, 4),
                "garch_forecast": round(garch_forecast, 4),
                "implied_vol": round(implied_vol, 4),
                "spread": round(implied_vol - vol, 4),
            }

            self.results.append(result)

            print(f"OK {pair}: ${result['price']:.2f} | RV={vol:.1%} | IV={implied_vol:.1%}")

        try:
            with open("data/results.json", "w") as f:
                json.dump(self.results[-100:], f, indent=2)
        except Exception as e:
            print(f"Error saving: {e}")

    async def run(self):
        print("AgentSpoons Starting...")
        print("=" * 60)

        iteration = 0
        while True:
            iteration += 1
            print(f"\n[Iteration {iteration}] {datetime.now().strftime('%H:%M:%S')}")

            await self.run_cycle()
            await asyncio.sleep(3)


if __name__ == "__main__":
    system = AgentSpoons()
    asyncio.run(system.run())
