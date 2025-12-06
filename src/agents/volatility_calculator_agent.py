"""
Volatility Calculator Agent
"""
import asyncio
from datetime import datetime
from typing import Dict, Any
import pandas as pd
from loguru import logger

from .base_agent import BaseAgent
from .market_data_agent import MarketDataAgent
from src.models.volatility_engine import VolatilityEngine
from src.models.garch_forecaster import GARCHForecaster
from src.utils.database import AgentSpoonsDB

class VolatilityCalculatorAgent(BaseAgent):
    """Calculates various volatility metrics from market data"""
    
    def __init__(self, agent_id: str, wallet_address: str,
                 market_data_agent: MarketDataAgent,
                 db: AgentSpoonsDB):
        super().__init__(agent_id, wallet_address)
        self.market_data_agent = market_data_agent
        self.db = db
        self.volatility_results = {}
        self.execution_interval = 60  # Every 60 seconds
    
    async def execute(self) -> Dict[str, Any]:
        """Calculate volatility for all tracked pairs"""
        results = {}
        
        for pair in self.market_data_agent.token_pairs:
            try:
                # Get historical data
                df = self.market_data_agent.get_ohlcv_dataframe(pair, lookback=100)
                
                if len(df) < 30:
                    logger.warning(f"Insufficient data for {pair}: {len(df)} candles")
                    continue
                
                # Calculate volatilities
                vol_metrics = await self.calculate_volatilities(df, pair)
                
                # Save to database
                self.db.insert_volatility_metrics(pair, vol_metrics)
                
                # Store results
                results[pair] = vol_metrics
                self.volatility_results[pair] = vol_metrics
                
                logger.debug(f"{pair}: GK Vol={vol_metrics['garman_klass_vol']:.2%}")
                
            except Exception as e:
                logger.error(f"Error calculating vol for {pair}: {e}")
        
        return {
            'status': 'success',
            'pairs_calculated': len(results),
            'results': results
        }
    
    async def calculate_volatilities(self, df: pd.DataFrame, pair: str) -> Dict[str, Any]:
        """Calculate all volatility metrics for a pair"""
        
        # Initialize engines
        vol_engine = VolatilityEngine(df)
        
        # Historical volatility estimators
        close_to_close = vol_engine.close_to_close_vol(window=30)
        parkinson = vol_engine.parkinson_vol(window=30)
        garman_klass = vol_engine.garman_klass_vol(window=30)
        rogers_satchell = vol_engine.rogers_satchell_vol(window=30)
        yang_zhang = vol_engine.yang_zhang_vol(window=30)
        
        # GARCH forecast
        garch_forecast = 0.5  # Default
        garch_params = {}
        
        try:
            if len(vol_engine.returns) >= 50:
                garch = GARCHForecaster(vol_engine.returns)
                garch_params = garch.fit()
                garch_forecast = garch.forecast(horizon=1)
        except Exception as e:
            logger.warning(f"GARCH fitting failed for {pair}: {e}")
        
        # Calculate realized volatility (actual price movement)
        realized_vol = vol_engine.returns.tail(30).std() * (252 ** 0.5)
        
        return {
            'timestamp': datetime.now().isoformat(),
            'current_price': float(df['close'].iloc[-1]),
            'close_to_close_vol': float(close_to_close),
            'parkinson_vol': float(parkinson),
            'garman_klass_vol': float(garman_klass),
            'rogers_satchell_vol': float(rogers_satchell),
            'yang_zhang_vol': float(yang_zhang),
            'realized_vol_30d': float(realized_vol),
            'garch_forecast': float(garch_forecast),
            'garch_params': garch_params,
            'vol_regime': self.classify_vol_regime(float(realized_vol))
        }
    
    def classify_vol_regime(self, vol: float) -> str:
        """Classify current volatility regime"""
        if vol < 0.20:
            return 'low'
        elif vol < 0.50:
            return 'normal'
        elif vol < 0.80:
            return 'elevated'
        else:
            return 'high'
    
    def get_latest_volatility(self, pair: str) -> Dict[str, Any]:
        """Get most recent volatility calculation"""
        return self.volatility_results.get(pair, {})
    
    def get_vol_comparison(self, pair: str) -> Dict[str, float]:
        """Compare different vol estimators"""
        if pair not in self.volatility_results:
            return {}
        
        results = self.volatility_results[pair]
        
        return {
            'close_to_close': results.get('close_to_close_vol', 0),
            'parkinson': results.get('parkinson_vol', 0),
            'garman_klass': results.get('garman_klass_vol', 0),
            'yang_zhang': results.get('yang_zhang_vol', 0),
            'garch_forecast': results.get('garch_forecast', 0)
        }
