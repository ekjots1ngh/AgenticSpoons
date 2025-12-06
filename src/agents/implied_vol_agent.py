"""
Implied Volatility and Greeks Calculator Agent
"""
import asyncio
from datetime import datetime
from typing import Dict, Any, List
import numpy as np
from loguru import logger

from .base_agent import BaseAgent
from .market_data_agent import MarketDataAgent
from models.black_scholes import BlackScholesEngine
from models.volatility_surface import VolatilitySurface

class ImpliedVolAgent(BaseAgent):
    """Calculates implied volatility surfaces and option Greeks"""
    
    def __init__(self, agent_id: str, wallet_address: str,
                 market_data_agent: MarketDataAgent,
                 risk_free_rate: float = 0.05):
        super().__init__(agent_id, wallet_address)
        self.market_data_agent = market_data_agent
        self.risk_free_rate = risk_free_rate
        self.vol_surfaces = {}
        self.execution_interval = 120  # Every 2 minutes
    
    async def execute(self) -> Dict[str, Any]:
        """Build volatility surfaces for all pairs"""
        results = {}
        
        for pair in self.market_data_agent.token_pairs:
            try:
                df = self.market_data_agent.get_ohlcv_dataframe(pair)
                
                if df.empty:
                    continue
                
                spot_price = float(df['close'].iloc[-1])
                
                # Generate options grid
                options_grid = self.generate_options_grid(spot_price)
                
                # Build surface
                vol_surface = VolatilitySurface()
                vol_surface.spot_price = spot_price
                
                for option in options_grid:
                    K, T, market_price = option['strike'], option['maturity'], option['price']
                    
                    try:
                        iv = BlackScholesEngine.implied_volatility(
                            market_price, spot_price, K, T,
                            self.risk_free_rate, option['type']
                        )
                        vol_surface.add_point(K, T, iv)
                    except:
                        continue
                
                # Build the surface
                vol_surface.build_surface(method='cubic')
                self.vol_surfaces[pair] = vol_surface
                
                # Calculate metrics
                atm_term_structure = vol_surface.get_atm_term_structure(spot_price)
                skew_30d = vol_surface.calculate_skew(30/365)
                smile_curvature = vol_surface.calculate_smile_curvature(30/365)
                
                results[pair] = {
                    'spot_price': spot_price,
                    'atm_vol_1w': atm_term_structure.get(7/365, None),
                    'atm_vol_1m': atm_term_structure.get(30/365, None),
                    'atm_vol_3m': atm_term_structure.get(90/365, None),
                    'atm_vol_6m': atm_term_structure.get(180/365, None),
                    'vol_skew_30d': skew_30d,
                    'smile_curvature_30d': smile_curvature,
                    'surface_points': len(vol_surface.strikes),
                    'surface_stats': vol_surface.get_summary_stats()
                }
                
                logger.success(f"{pair} surface: {len(vol_surface.strikes)} points, "
                             f"ATM 1M vol={atm_term_structure.get(30/365, 0):.2%}")
                
            except Exception as e:
                logger.error(f"Error building surface for {pair}: {e}")
        
        return {
            'status': 'success',
            'surfaces_built': len(results),
            'results': results
        }
    
    def generate_options_grid(self, spot_price: float) -> List[Dict]:
        """
        Generate synthetic options grid
        
        In production, replace with actual options data from Neo options DEX
        For demo, we create realistic synthetic option prices
        """
        options = []
        
        # Strike range: 70% to 130% of spot in 5% increments
        strike_percentages = np.arange(0.70, 1.35, 0.05)
        strikes = spot_price * strike_percentages
        
        # Maturities: 1 week to 6 months
        maturities_days = [7, 14, 30, 60, 90, 180]
        maturities = [d/365 for d in maturities_days]
        
        for K in strikes:
            for T in maturities:
                # Simulate realistic vol smile
                moneyness = K / spot_price
                
                # Base volatility increases with maturity (term structure)
                base_vol = 0.60 + 0.10 * T  # 60-70% base vol
                
                # Add volatility smile (higher for OTM options)
                if moneyness < 0.95:  # OTM puts
                    vol = base_vol * (1 + 0.15 * (0.95 - moneyness))
                elif moneyness > 1.05:  # OTM calls
                    vol = base_vol * (1 + 0.08 * (moneyness - 1.05))
                else:  # ATM
                    vol = base_vol
                
                # Add some randomness
                vol *= np.random.uniform(0.95, 1.05)
                
                # Price options using Black-Scholes
                call_price = BlackScholesEngine.call_price(
                    spot_price, K, T, self.risk_free_rate, vol
                )
                put_price = BlackScholesEngine.put_price(
                    spot_price, K, T, self.risk_free_rate, vol
                )
                
                options.append({
                    'strike': K,
                    'maturity': T,
                    'type': 'call',
                    'price': call_price,
                    'true_vol': vol  # For validation
                })
                options.append({
                    'strike': K,
                    'maturity': T,
                    'type': 'put',
                    'price': put_price,
                    'true_vol': vol
                })
        
        return options
    
    def get_greeks(self, pair: str, strike: float, maturity: float,
                   option_type: str = 'call') -> Dict[str, float]:
        """Calculate all Greeks for a specific option"""
        df = self.market_data_agent.get_ohlcv_dataframe(pair)
        
        if df.empty:
            return {}
        
        S = float(df['close'].iloc[-1])
        
        # Get IV from surface
        if pair in self.vol_surfaces:
            sigma = self.vol_surfaces[pair].get_vol(strike, maturity)
            if sigma is None:
                sigma = 0.5
        else:
            sigma = 0.5
        
        greeks = {
            'spot': S,
            'strike': strike,
            'maturity': maturity,
            'sigma': sigma,
            'delta': BlackScholesEngine.delta_call(S, strike, maturity, self.risk_free_rate, sigma)
                     if option_type == 'call'
                     else BlackScholesEngine.delta_put(S, strike, maturity, self.risk_free_rate, sigma),
            'gamma': BlackScholesEngine.gamma(S, strike, maturity, self.risk_free_rate, sigma),
            'vega': BlackScholesEngine.vega(S, strike, maturity, self.risk_free_rate, sigma),
            'theta': BlackScholesEngine.theta_call(S, strike, maturity, self.risk_free_rate, sigma),
            'rho': BlackScholesEngine.rho_call(S, strike, maturity, self.risk_free_rate, sigma),
        }
        
        # Add option price
        if option_type == 'call':
            greeks['price'] = BlackScholesEngine.call_price(S, strike, maturity, self.risk_free_rate, sigma)
        else:
            greeks['price'] = BlackScholesEngine.put_price(S, strike, maturity, self.risk_free_rate, sigma)
        
        return greeks
    
    def get_atm_greeks(self, pair: str, maturity: float = 30/365) -> Dict[str, float]:
        """Get Greeks for ATM option"""
        df = self.market_data_agent.get_ohlcv_dataframe(pair)
        
        if df.empty:
            return {}
        
        spot = float(df['close'].iloc[-1])
        
        return self.get_greeks(pair, spot, maturity, 'call')
