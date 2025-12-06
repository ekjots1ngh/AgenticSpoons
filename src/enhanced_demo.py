"""
Enhanced data generator with realistic volatility clustering
"""
import asyncio
import numpy as np
from datetime import datetime
import json
import os

class AdvancedDataGenerator:
    def __init__(self):
        self.current_price = {"NEO/USDT": 15.0, "GAS/USDT": 3.5}
        self.history = {"NEO/USDT": [], "GAS/USDT": []}
        self.vol_state = 0.5  # Current volatility level
        
        # Generate initial history
        print("Generating initial data...")
        for _ in range(60):
            for pair in ["NEO/USDT", "GAS/USDT"]:
                self._generate_tick(pair)
        print("Initial 60 candles created")
        
    def _generate_tick(self, pair):
        """Generate realistic tick with volatility clustering"""
        price = self.current_price[pair]
        
        # Volatility clustering - vol changes slowly
        self.vol_state += np.random.normal(0, 0.05)
        self.vol_state = np.clip(self.vol_state, 0.3, 0.8)  # Keep in realistic range
        
        # Price change with current volatility
        change = np.random.normal(0, self.vol_state / np.sqrt(252))
        new_price = price * (1 + change)
        self.current_price[pair] = new_price
        
        # Generate OHLC with realistic relationships
        high = new_price * np.random.uniform(1.000, 1.005)
        low = new_price * np.random.uniform(0.995, 1.000)
        open_price = price * np.random.uniform(0.998, 1.002)
        
        candle = {
            'timestamp': datetime.now().isoformat(),
            'open': round(open_price, 2),
            'high': round(high, 2),
            'low': round(low, 2),
            'close': round(new_price, 2),
            'volume': round(np.random.uniform(50000, 150000), 2)
        }
        
        self.history[pair].append(candle)
        if len(self.history[pair]) > 200:
            self.history[pair] = self.history[pair][-200:]
        
        return candle
    
    def calculate_volatility(self, candles):
        """Garman-Klass volatility"""
        if len(candles) < 5:
            return 0.5
        
        gk = []
        for c in candles[-30:]:
            hl = np.log(c['high'] / c['low'])
            co = np.log(c['close'] / c['open'])
            gk.append(0.5 * hl**2 - (2*np.log(2)-1) * co**2)
        
        return np.sqrt(252 * np.mean(gk))
    
    async def run(self):
        """Main loop"""
        os.makedirs('data', exist_ok=True)
        results = []
        
        print("AgentSpoons Enhanced System Starting...")
        print("="*70)
        
        iteration = 0
        while True:
            iteration += 1
            print(f"\n[{iteration}] {datetime.now().strftime('%H:%M:%S')}")
            
            for pair in ["NEO/USDT", "GAS/USDT"]:
                candle = self._generate_tick(pair)
                vol = self.calculate_volatility(self.history[pair])
                
                # GARCH forecast (with mean reversion)
                long_run_vol = 0.5
                garch_forecast = 0.9 * vol + 0.1 * long_run_vol + np.random.normal(0, 0.02)
                garch_forecast = np.clip(garch_forecast, 0.3, 0.8)
                
                # Implied vol (tends to be higher, with smile)
                implied_vol = vol * np.random.uniform(1.08, 1.15)
                
                result = {
                    'pair': pair,
                    'timestamp': datetime.now().isoformat(),
                    'price': candle['close'],
                    'realized_vol': round(vol, 4),
                    'garch_forecast': round(garch_forecast, 4),
                    'implied_vol': round(implied_vol, 4),
                    'spread': round(implied_vol - vol, 4)
                }
                
                results.append(result)
                
                status = 'RED' if abs(result['spread']) > 0.1 else 'GREEN'
                print(f"{status} {pair}: ${candle['close']:.2f} | "
                      f"RV={vol:.1%} | IV={implied_vol:.1%} | "
                      f"Spread={result['spread']:.1%}")
            
            # Save immediately
            try:
                with open('data/results.json', 'w') as f:
                    json.dump(results[-200:], f, indent=2)
            except Exception as e:
                print(f"Error saving: {e}")
            
            await asyncio.sleep(3)  # Update every 3 seconds

if __name__ == "__main__":
    system = AdvancedDataGenerator()
    asyncio.run(system.run())
