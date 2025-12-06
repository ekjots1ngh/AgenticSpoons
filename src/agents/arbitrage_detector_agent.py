"""
Volatility Arbitrage Detection Agent
"""
import asyncio
from datetime import datetime
from typing import Dict, Any, List
from loguru import logger

from .base_agent import BaseAgent
from .volatility_calculator_agent import VolatilityCalculatorAgent
from .implied_vol_agent import ImpliedVolAgent

class ArbitrageDetectorAgent(BaseAgent):
    """Detects volatility arbitrage opportunities"""
    
    def __init__(self, agent_id: str, wallet_address: str,
                 vol_calculator: VolatilityCalculatorAgent,
                 implied_vol_agent: ImpliedVolAgent,
                 threshold: float = 0.10):
        super().__init__(agent_id, wallet_address)
        self.vol_calculator = vol_calculator
        self.implied_vol_agent = implied_vol_agent
        self.threshold = threshold  # 10% difference threshold
        self.opportunities = []
        self.execution_interval = 180  # Every 3 minutes
    
    async def execute(self) -> Dict[str, Any]:
        """Detect arbitrage opportunities"""
        opportunities = []
        
        for pair in self.vol_calculator.market_data_agent.token_pairs:
            try:
                # Get realized volatility
                vol_data = self.vol_calculator.get_latest_volatility(pair)
                
                if not vol_data:
                    continue
                
                realized_vol = vol_data.get('garman_klass_vol', 0)
                garch_forecast = vol_data.get('garch_forecast', 0)
                
                # Get implied volatility
                if pair in self.implied_vol_agent.vol_surfaces:
                    surface = self.implied_vol_agent.vol_surfaces[pair]
                    spot = vol_data.get('current_price', 0)
                    
                    # Get ATM implied vol for 30-day maturity
                    atm_term = surface.get_atm_term_structure(spot)
                    implied_vol = atm_term.get(30/365, 0)
                    
                    if implied_vol == 0:
                        continue
                    
                    # Calculate spread
                    vol_spread = implied_vol - realized_vol
                    vol_spread_pct = vol_spread / realized_vol
                    
                    # Check for arbitrage opportunity
                    if abs(vol_spread_pct) > self.threshold:
                        opportunity = self.create_opportunity(
                            pair, spot, realized_vol, implied_vol,
                            garch_forecast, vol_spread, vol_spread_pct
                        )
                        opportunities.append(opportunity)
                        
                        logger.info(f"🎯 Arbitrage opportunity in {pair}: "
                                  f"IV={implied_vol:.2%} vs RV={realized_vol:.2%} "
                                  f"({vol_spread_pct:+.1%})")
                
            except Exception as e:
                logger.error(f"Error detecting arbitrage for {pair}: {e}")
        
        self.opportunities = opportunities
        
        return {
            'status': 'success',
            'opportunities_found': len(opportunities),
            'opportunities': opportunities
        }
    
    def create_opportunity(self, pair: str, spot: float,
                          realized_vol: float, implied_vol: float,
                          garch_forecast: float, spread: float,
                          spread_pct: float) -> Dict[str, Any]:
        """Create arbitrage opportunity object"""
        
        # Determine strategy
        if implied_vol > realized_vol:
            strategy = 'sell_volatility'  # Sell straddle/strangle
            direction = 'short'
            reasoning = f"IV ({implied_vol:.2%}) is {spread_pct:.1%} higher than RV ({realized_vol:.2%})"
        else:
            strategy = 'buy_volatility'  # Buy straddle/strangle
            direction = 'long'
            reasoning = f"IV ({implied_vol:.2%}) is {abs(spread_pct):.1%} lower than RV ({realized_vol:.2%})"
        
        # Calculate confidence score
        confidence = self.calculate_confidence(
            spread_pct, realized_vol, implied_vol, garch_forecast
        )
        
        return {
            'pair': pair,
            'timestamp': datetime.now().isoformat(),
            'spot_price': spot,
            'realized_vol': realized_vol,
            'implied_vol': implied_vol,
            'garch_forecast': garch_forecast,
            'vol_spread': spread,
            'vol_spread_pct': spread_pct,
            'strategy': strategy,
            'direction': direction,
            'confidence': confidence,
            'reasoning': reasoning,
            'recommended_action': self.get_recommended_action(strategy, confidence)
        }
    
    def calculate_confidence(self, spread_pct: float, rv: float,
                            iv: float, garch: float) -> float:
        """
        Calculate confidence score (0-100)
        
        Factors:
        - Size of spread
        - GARCH forecast alignment
        - Volatility regime
        """
        score = 0.0
        
        # Spread size (max 40 points)
        spread_score = min(abs(spread_pct) / 0.5, 1.0) * 40
        score += spread_score
        
        # GARCH alignment (max 30 points)
        if abs(iv - rv) > 0.05:  # Significant difference
            if (iv > rv and garch > rv) or (iv < rv and garch < rv):
                score += 30  # GARCH agrees with realized vol
            elif (iv > rv and garch < iv) or (iv < rv and garch > iv):
                score += 15  # GARCH is between IV and RV
        
        # Regime stability (max 30 points)
        # Higher scores for normal volatility regimes
        if 0.3 < rv < 0.8:
            score += 30
        elif 0.2 < rv < 1.0:
            score += 20
        else:
            score += 10
        
        return min(score, 100.0)
    
    def get_recommended_action(self, strategy: str, confidence: float) -> str:
        """Get recommended action based on strategy and confidence"""
        if confidence < 40:
            return 'monitor'
        elif confidence < 70:
            return f'{strategy}_small_size'
        else:
            return f'{strategy}_full_size'
    
    def get_opportunities(self, min_confidence: float = 0) -> List[Dict]:
        """Get all opportunities above confidence threshold"""
        return [
            opp for opp in self.opportunities
            if opp['confidence'] >= min_confidence
        ]
    
    def get_best_opportunity(self) -> Dict:
        """Get highest confidence opportunity"""
        if not self.opportunities:
            return {}
        
        return max(self.opportunities, key=lambda x: x['confidence'])
