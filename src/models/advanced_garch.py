"""
Advanced GARCH Models with Multiple Variants
"""
import numpy as np
from scipy.optimize import minimize
from typing import Dict, Tuple
from loguru import logger

class AdvancedGARCH:
    """
    Multiple GARCH variants:
    - GARCH(1,1)
    - EGARCH (Exponential GARCH for asymmetry)
    - GJR-GARCH (captures leverage effect)
    """
    
    def __init__(self, returns: np.ndarray):
        self.returns = returns
        self.n = len(returns)
        
    def garch_11_likelihood(self, params: np.ndarray) -> float:
        """Negative log-likelihood for GARCH(1,1)"""
        omega, alpha, beta = params
        
        # Stationarity constraint
        if alpha + beta >= 1 or alpha < 0 or beta < 0 or omega < 0:
            return 1e10
        
        # Compute conditional variance
        variance = np.zeros(self.n)
        variance[0] = np.var(self.returns)
        
        for t in range(1, self.n):
            variance[t] = omega + alpha * self.returns[t-1]**2 + beta * variance[t-1]
        
        # Log-likelihood
        ll = -0.5 * np.sum(np.log(2 * np.pi * variance) + self.returns**2 / variance)
        
        return -ll  # Return negative for minimization
    
    def fit_garch_11(self) -> Dict:
        """Fit GARCH(1,1) using MLE"""
        # Initial guess
        x0 = [0.0001, 0.05, 0.90]
        
        # Bounds
        bounds = [(1e-6, 0.1), (0, 0.3), (0, 0.98)]
        
        # Optimize
        result = minimize(
            self.garch_11_likelihood,
            x0,
            method='L-BFGS-B',
            bounds=bounds
        )
        
        if result.success:
            omega, alpha, beta = result.x
            
            return {
                'omega': omega,
                'alpha': alpha,
                'beta': beta,
                'persistence': alpha + beta,
                'long_run_vol': np.sqrt(omega / (1 - alpha - beta)),
                'log_likelihood': -result.fun
            }
        else:
            logger.warning("GARCH optimization failed, using defaults")
            return {
                'omega': 0.0001,
                'alpha': 0.05,
                'beta': 0.90,
                'persistence': 0.95,
                'long_run_vol': 0.5,
                'log_likelihood': 0
            }
    
    def egarch_likelihood(self, params: np.ndarray) -> float:
        """
        EGARCH - captures asymmetry (bad news increases vol more)
        log(σ²_t) = ω + α|ε_{t-1}|/σ_{t-1} + γε_{t-1}/σ_{t-1} + βlog(σ²_{t-1})
        """
        omega, alpha, gamma, beta = params
        
        log_variance = np.zeros(self.n)
        log_variance[0] = np.log(np.var(self.returns))
        
        for t in range(1, self.n):
            z = self.returns[t-1] / np.exp(0.5 * log_variance[t-1])
            log_variance[t] = (omega + alpha * abs(z) + gamma * z + 
                             beta * log_variance[t-1])
        
        variance = np.exp(log_variance)
        ll = -0.5 * np.sum(np.log(2 * np.pi * variance) + self.returns**2 / variance)
        
        return -ll
    
    def fit_egarch(self) -> Dict:
        """Fit EGARCH model"""
        x0 = [0.01, 0.1, -0.05, 0.95]
        bounds = [(-1, 1), (0, 1), (-1, 1), (0, 0.999)]
        
        result = minimize(
            self.egarch_likelihood,
            x0,
            method='L-BFGS-B',
            bounds=bounds
        )
        
        if result.success:
            omega, alpha, gamma, beta = result.x
            return {
                'omega': omega,
                'alpha': alpha,
                'gamma': gamma,  # Asymmetry parameter
                'beta': beta,
                'leverage_effect': gamma < 0,  # Negative news increases vol more
                'log_likelihood': -result.fun
            }
        else:
            return None
    
    def forecast(self, params: Dict, horizon: int = 1) -> np.ndarray:
        """Multi-step GARCH forecast"""
        omega = params['omega']
        alpha = params['alpha']
        beta = params['beta']
        
        # Current variance
        current_var = omega / (1 - alpha - beta)
        
        # Forecast
        forecasts = np.zeros(horizon)
        for h in range(horizon):
            if h == 0:
                forecasts[h] = omega + (alpha + beta) * current_var
            else:
                forecasts[h] = omega + (alpha + beta) * forecasts[h-1]
        
        return np.sqrt(forecasts * 252)  # Annualize

class VolatilityBacktest:
    """Backtest volatility forecasting accuracy"""
    
    def __init__(self, returns: np.ndarray, window: int = 252):
        self.returns = returns
        self.window = window
    
    def rolling_forecast_test(self) -> Dict:
        """Rolling window backtest"""
        n = len(self.returns)
        forecasts = []
        realized = []
        
        for i in range(self.window, n - 21):  # Leave 21 days for realized vol
            # Fit on window
            train_returns = self.returns[i-self.window:i]
            garch = AdvancedGARCH(train_returns)
            params = garch.fit_garch_11()
            
            # Forecast next 21 days
            forecast_vol = garch.forecast(params, horizon=1)[0]
            forecasts.append(forecast_vol)
            
            # Calculate realized vol over next 21 days
            future_returns = self.returns[i:i+21]
            realized_vol = np.std(future_returns) * np.sqrt(252)
            realized.append(realized_vol)
        
        forecasts = np.array(forecasts)
        realized = np.array(realized)
        
        # Evaluation metrics
        mse = np.mean((forecasts - realized)**2)
        mae = np.mean(np.abs(forecasts - realized))
        directional_accuracy = np.mean((forecasts[1:] > forecasts[:-1]) == 
                                      (realized[1:] > realized[:-1]))
        
        return {
            'mse': mse,
            'mae': mae,
            'rmse': np.sqrt(mse),
            'directional_accuracy': directional_accuracy,
            'n_forecasts': len(forecasts)
        }

class VolArbitrageStrategy:
    """Volatility arbitrage backtester"""
    
    def __init__(self, data):
        self.data = data
        self.trades = []
    
    def run_backtest(self, threshold: float = 0.10) -> Dict:
        """
        Strategy: Buy vol when IV < RV, sell when IV > RV
        """
        pnl = []
        
        for i in range(len(self.data)):
            if 'implied_vol' not in self.data[i] or 'realized_vol' not in self.data[i]:
                continue
            
            iv = self.data[i]['implied_vol']
            rv = self.data[i]['realized_vol']
            
            if iv == 0 or rv == 0:
                continue
            
            spread = (iv - rv) / rv
            
            if abs(spread) > threshold:
                # Simplified P&L calculation
                # In reality: Would trade variance swaps or options
                trade_pnl = -spread * 100  # Simplified
                pnl.append(trade_pnl)
                
                self.trades.append({
                    'timestamp': self.data[i].get('timestamp'),
                    'spread': spread,
                    'pnl': trade_pnl
                })
        
        if len(pnl) == 0:
            return {'error': 'No trades executed'}
        
        pnl = np.array(pnl)
        
        return {
            'total_pnl': np.sum(pnl),
            'n_trades': len(pnl),
            'win_rate': len(pnl[pnl > 0]) / len(pnl),
            'avg_win': np.mean(pnl[pnl > 0]) if len(pnl[pnl > 0]) > 0 else 0,
            'avg_loss': np.mean(pnl[pnl < 0]) if len(pnl[pnl < 0]) > 0 else 0,
            'sharpe_ratio': np.mean(pnl) / np.std(pnl) * np.sqrt(252) if np.std(pnl) > 0 else 0,
            'max_drawdown': self.calculate_max_drawdown(pnl)
        }
    
    def calculate_max_drawdown(self, pnl: np.ndarray) -> float:
        """Calculate maximum drawdown"""
        cumulative = np.cumsum(pnl)
        running_max = np.maximum.accumulate(cumulative)
        drawdown = (cumulative - running_max)
        return float(np.min(drawdown))
