"""
AgentSpoons - Minimal Demo Version
Everything in one file for hackathon
"""
import asyncio
import json
from datetime import datetime
from typing import Dict, List

import numpy as np
import pandas as pd


class DataGenerator:
    """Generate realistic-looking crypto price data"""

    def __init__(self):
        self.current_price = {"NEO/USDT": 15.0, "GAS/USDT": 3.5}
        self.history: Dict[str, List[Dict]] = {"NEO/USDT": [], "GAS/USDT": []}

    def generate_tick(self, pair: str) -> Dict:
        """Generate one price candle"""
        price = self.current_price[pair]

        change = np.random.normal(0, 0.02)
        new_price = price * (1 + change)
        self.current_price[pair] = new_price

        candle = {
            "timestamp": datetime.utcnow().isoformat(),
            "open": price * np.random.uniform(0.99, 1.01),
            "high": new_price * np.random.uniform(1.00, 1.02),
            "low": new_price * np.random.uniform(0.98, 1.00),
            "close": new_price,
            "volume": float(np.random.uniform(10_000, 100_000)),
        }

        self.history[pair].append(candle)
        if len(self.history[pair]) > 240:
            self.history[pair] = self.history[pair][-240:]

        return candle


def realized_vol(df: pd.DataFrame) -> float:
    """Annualized realized volatility from close-to-close returns"""
    returns = df["close"].pct_change().dropna()
    if returns.empty:
        return 0.0
    return float(returns.std() * np.sqrt(365))


def garman_klass_vol(df: pd.DataFrame) -> float:
    """Garman-Klass OHLC volatility"""
    if len(df) < 2:
        return 0.0
    log_hl = np.log(df["high"] / df["low"]) ** 2
    log_co = np.log(df["close"] / df["open"]) ** 2
    return float(np.sqrt((0.5 * log_hl - (2 * np.log(2) - 1) * log_co).mean()) * np.sqrt(365))


def summarize(pair: str, candles: List[Dict]) -> Dict:
    """Summarize latest metrics for a pair"""
    df = pd.DataFrame(candles)
    latest = candles[-1]
    return {
        "pair": pair,
        "timestamp": latest["timestamp"],
        "price": float(latest["close"]),
        "realized_vol": realized_vol(df),
        "garman_klass_vol": garman_klass_vol(df),
        "sample_size": len(df),
    }


class SimpleDemo:
    """Minimal orchestrator that generates data and prints metrics"""

    def __init__(self):
        self.pairs = ["NEO/USDT", "GAS/USDT"]
        self.generator = DataGenerator()

    async def run_once(self) -> Dict[str, Dict]:
        results = {}
        for pair in self.pairs:
            self.generator.generate_tick(pair)
            candles = self.generator.history[pair]
            if len(candles) >= 30:
                results[pair] = summarize(pair, candles)
        return results

    async def run(self, iterations: int = 10, delay: float = 0.5):
        for i in range(iterations):
            results = await self.run_once()
            if results:
                print(json.dumps({"iteration": i + 1, "results": results}, indent=2))
            await asyncio.sleep(delay)


def main():
    demo = SimpleDemo()
    asyncio.run(demo.run())


if __name__ == "__main__":
    main()
