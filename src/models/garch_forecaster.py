"""
GARCH Model for Volatility Forecasting
"""
import numpy as np
import pandas as pd
from arch import arch_model
from typing import Dict, Optional
from loguru import logger

class GARCHForecaster:
    """GARCH(1,1) volatility forecasting engine"""
    
    def __init__(self, returns: pd.Series):
        """
        Initialize GARCH model
        
        Args:
            returns: Series of log returns (not in percentage)
        """
        self.returns = returns * 100  # Convert to percentage for ARCH library
        self.model = None
        self.fitted = None
        self.params = {}
    
    def fit(self, p: int = 1, q: int = 1, verbose: bool = False) -> Dict:
        """
        Fit GARCH(p,q) model
        
        GARCH(1,1) equation:
        σ²_t = ω + α·ε²_(t-1) + β·σ²_(t-1)
        
        where:
        - ω (omega): long-term variance constant
        - α (alpha): reaction coefficient (ARCH term)
        - β (beta): persistence coefficient (GARCH term)
        """
        try:
            self.model = arch_model(
                self.returns,
                vol='Garch',
                p=p,  # GARCH lag order
                q=q,  # ARCH lag order
                mean='Constant',  # Can also use 'Zero', 'AR', etc.
                rescale=False
            )
            
            self.fitted = self.model.fit(disp='off' if not verbose else 'final')
            
            # Extract parameters
            self.params = {
                'omega': float(self.fitted.params['omega']),
                'alpha': float(self.fitted.params.get('alpha[1]', 0)),
                'beta': float(self.fitted.params.get('beta[1]', 0)),
                'mu': float(self.fitted.params.get('mu', 0)),
            }
            
            # Calculate persistence
            self.params['persistence'] = self.params['alpha'] + self.params['beta']
            
            # Long-run variance
            if self.params['persistence'] < 1:
                self.params['long_run_var'] = self.params['omega'] / (1 - self.params['persistence'])
            else:
                self.params['long_run_var'] = np.nan
            
            logger.debug(f"GARCH fitted - α={self.params['alpha']:.4f}, β={self.params['beta']:.4f}")
            
            return self.params
            
        except Exception as e:
            logger.error(f"GARCH fitting error: {e}")
            return {}
    
    def forecast(self, horizon: int = 1) -> float:
        """
        Forecast volatility for next 'horizon' periods
        
        Returns:
            Annualized volatility (as decimal, e.g., 0.50 = 50%)
        """
        if self.fitted is None:
            self.fit()
        
        try:
            # Get variance forecast
            forecast = self.fitted.forecast(horizon=horizon, reindex=False)
            variance = forecast.variance.values[-1, :]
            
            # Convert to annualized volatility
            # variance is in % terms, so divide by 100 to get decimal
            # Multiply by 252 for annualization, then sqrt
            annualized_vol = np.sqrt(variance.mean() * 252) / 100
            
            return float(annualized_vol)
            
        except Exception as e:
            logger.error(f"GARCH forecast error: {e}")
            return 0.5  # Default fallback
    
    def conditional_volatility(self) -> pd.Series:
        """Get conditional volatility time series"""
        if self.fitted is None:
            self.fit()
        
        # Returns annualized conditional volatility
        return np.sqrt(self.fitted.conditional_volatility ** 2 * 252) / 100
    
    def get_aic_bic(self) -> Dict[str, float]:
        """Get model selection criteria"""
        if self.fitted is None:
            return {}
        
        return {
            'aic': float(self.fitted.aic),
            'bic': float(self.fitted.bic),
            'loglikelihood': float(self.fitted.loglikelihood)
        }
    
    def simulate(self, n_steps: int = 252, n_simulations: int = 1000) -> np.ndarray:
        """
        Simulate future price paths using GARCH volatility
        
        Returns:
            Array of shape (n_simulations, n_steps) with simulated returns
        """
        if self.fitted is None:
            self.fit()
        
        simulations = self.fitted.forecast(horizon=n_steps, method='simulation', simulations=n_simulations)
        
        return simulations.simulations.values[0]  # Returns in percentage terms
