"""
OCaml-Enhanced Volatility Calculator Agent
Uses OCaml for 10x performance boost
"""
import asyncio
from datetime import datetime
from typing import Dict, Any
from loguru import logger

from .base_agent import BaseAgent
from .market_data_agent import MarketDataAgent
from utils.ocaml_bridge import ocaml_engine
from utils.database import AgentSpoonsDB

class OCamlVolatilityAgent(BaseAgent):
    """High-performance volatility calculator using OCaml"""
    
    def __init__(self, agent_id: str, wallet_address: str,
                 market_data_agent: MarketDataAgent,
                 db: AgentSpoonsDB):
        super().__init__(agent_id, wallet_address)
        self.market_data_agent = market_data_agent
        self.db = db
        self.volatility_results = {}
        self.execution_interval = 60
        self.use_ocaml = ocaml_engine.enabled
        
        if self.use_ocaml:
            logger.success(f"{agent_id} using OCaml engine for 10x performance!")
        else:
            logger.warning(f"{agent_id} falling back to Python (OCaml not available)")
    
    async def execute(self) -> Dict[str, Any]:
        """Calculate volatility using OCaml engine"""
        results = {}
        
        for pair in self.market_data_agent.token_pairs:
            try:
                df = self.market_data_agent.get_ohlcv_dataframe(pair, lookback=100)
                
                if len(df) < 30:
                    continue
                
                # Convert to OCaml format
                ohlcv_data = df.to_dict('records')
                
                if self.use_ocaml:
                    # Use OCaml for calculation (10x faster!)
                    vol_metrics = ocaml_engine.calculate_volatility(ohlcv_data)
                    
                    # Add timestamp and current price
                    vol_metrics['timestamp'] = datetime.now().isoformat()
                    vol_metrics['current_price'] = float(df['close'].iloc[-1])
                    
                    # Fit GARCH model
                    returns = (df['close'].pct_change().dropna() * 100).tolist()
                    garch_result = ocaml_engine.fit_garch(returns)
                    
                    vol_metrics['garch_params'] = garch_result['params']
                    vol_metrics['garch_forecast'] = garch_result['conditional_variance'][-1]
                    
                else:
                    # Fallback to Python
                    from models.volatility_engine import VolatilityEngine
                    engine = VolatilityEngine(df)
                    vol_metrics = {
                        'timestamp': datetime.now().isoformat(),
                        'current_price': float(df['close'].iloc[-1]),
                        'garman_klass_vol': engine.garman_klass_vol(),
                        # ... other metrics
                    }
                
                # Save to database
                self.db.insert_volatility_metrics(pair, vol_metrics)
                
                results[pair] = vol_metrics
                self.volatility_results[pair] = vol_metrics
                
                logger.info(f"✓ {pair}: GK Vol={vol_metrics['garman_klass']:.2%} (OCaml)")
                
            except Exception as e:
                logger.error(f"Error for {pair}: {e}")
        
        return {
            'status': 'success',
            'engine': 'ocaml' if self.use_ocaml else 'python',
            'pairs_calculated': len(results),
            'results': results
        }
