"""
Market Data Collection Agent - WITH DATABASE
"""
import asyncio
from datetime import datetime
from typing import Dict, Any, List
import pandas as pd
import numpy as np
from loguru import logger

from .base_agent import BaseAgent
from src.utils.database import AgentSpoonsDB

class MarketDataAgent(BaseAgent):
    """Collects price data from Neo DEXs"""
    
    def __init__(self, agent_id: str, wallet_address: str,
                 token_pairs: List[str], dex_endpoints: List[str],
                 db: AgentSpoonsDB):
        super().__init__(agent_id, wallet_address)
        self.token_pairs = token_pairs
        self.dex_endpoints = dex_endpoints
        self.price_history = {}
        self.db = db
        self.execution_interval = 30  # 30 seconds
        
        logger.info(f"Tracking pairs: {token_pairs}")
    
    async def execute(self) -> Dict[str, Any]:
        """Fetch latest price data"""
        collected_data = {}
        
        for pair in self.token_pairs:
            try:
                prices = await self.fetch_from_dexs(pair)
                
                if prices:
                    aggregated = self.aggregate_prices(prices)
                    
                    if pair not in self.price_history:
                        self.price_history[pair] = []
                    
                    candle = {
                        'timestamp': datetime.now(),
                        'open': aggregated['open'],
                        'high': aggregated['high'],
                        'low': aggregated['low'],
                        'close': aggregated['close'],
                        'volume': aggregated['volume']
                    }
                    
                    self.price_history[pair].append(candle)
                    
                    # Save to database
                    self.db.insert_market_data(pair, candle)
                    
                    # Keep last 1000 candles
                    if len(self.price_history[pair]) > 1000:
                        self.price_history[pair] = self.price_history[pair][-1000:]
                    
                    collected_data[pair] = aggregated
                    
            except Exception as e:
                logger.error(f"Error fetching {pair}: {e}")
        
        return {
            'status': 'success',
            'pairs_collected': len(collected_data),
            'data': collected_data
        }
    
    async def fetch_from_dexs(self, pair: str) -> List[Dict]:
        """Fetch from multiple DEXs (mock implementation for now)"""
        prices = []
        
        # TODO: Replace with actual Neo DEX API calls
        # For hackathon demo, generate realistic mock data
        base_price = 15.0 if 'NEO' in pair else 3.5
        
        for _ in self.dex_endpoints:
            prices.append({
                'open': base_price * np.random.uniform(0.98, 1.02),
                'high': base_price * np.random.uniform(1.00, 1.05),
                'low': base_price * np.random.uniform(0.95, 1.00),
                'close': base_price * np.random.uniform(0.98, 1.02),
                'volume': np.random.uniform(10000, 100000)
            })
        
        return prices
    
    def aggregate_prices(self, prices: List[Dict]) -> Dict:
        """Aggregate using VWAP"""
        total_volume = sum(p['volume'] for p in prices)
        
        if total_volume == 0:
            return {
                'open': np.mean([p['open'] for p in prices]),
                'high': np.max([p['high'] for p in prices]),
                'low': np.min([p['low'] for p in prices]),
                'close': np.mean([p['close'] for p in prices]),
                'volume': 0
            }
        
        vwap = sum(p['close'] * p['volume'] for p in prices) / total_volume
        
        return {
            'open': np.mean([p['open'] for p in prices]),
            'high': np.max([p['high'] for p in prices]),
            'low': np.min([p['low'] for p in prices]),
            'close': vwap,
            'volume': total_volume
        }
    
    def get_ohlcv_dataframe(self, pair: str, lookback: int = 100) -> pd.DataFrame:
        """Get historical data as DataFrame"""
        if pair not in self.price_history or not self.price_history[pair]:
            return pd.DataFrame()
        
        data = self.price_history[pair][-lookback:]
        return pd.DataFrame(data)
