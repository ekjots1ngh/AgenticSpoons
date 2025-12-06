"""
Black-Scholes Pricing and Greeks Engine
"""
import numpy as np
from scipy.stats import norm
from typing import Optional

class BlackScholesEngine:
    """Black-Scholes pricing and Greeks calculations"""
    
    @staticmethod
    def d1(S: float, K: float, T: float, r: float, sigma: float) -> float:
        """Calculate d1 parameter"""
        return (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    
    @staticmethod
    def d2(S: float, K: float, T: float, r: float, sigma: float) -> float:
        """Calculate d2 parameter"""
        return BlackScholesEngine.d1(S, K, T, r, sigma) - sigma*np.sqrt(T)
    
    @staticmethod
    def call_price(S: float, K: float, T: float, r: float, sigma: float) -> float:
        """
        European call option price
        
        Args:
            S: Spot price
            K: Strike price
            T: Time to maturity (years)
            r: Risk-free rate
            sigma: Volatility (annualized)
        """
        d1 = BlackScholesEngine.d1(S, K, T, r, sigma)
        d2 = BlackScholesEngine.d2(S, K, T, r, sigma)
        
        return float(S * norm.cdf(d1) - K * np.exp(-r*T) * norm.cdf(d2))
    
    @staticmethod
    def put_price(S: float, K: float, T: float, r: float, sigma: float) -> float:
        """European put option price"""
        d1 = BlackScholesEngine.d1(S, K, T, r, sigma)
        d2 = BlackScholesEngine.d2(S, K, T, r, sigma)
        
        return float(K * np.exp(-r*T) * norm.cdf(-d2) - S * norm.cdf(-d1))
    
    @staticmethod
    def implied_volatility(option_price: float, S: float, K: float, T: float, 
                          r: float, option_type: str = 'call',
                          initial_guess: float = 0.3, 
                          max_iterations: int = 100,
                          tolerance: float = 1e-6) -> float:
        """
        Calculate implied volatility using Newton-Raphson method
        """
        sigma = initial_guess
        
        for i in range(max_iterations):
            if option_type == 'call':
                price = BlackScholesEngine.call_price(S, K, T, r, sigma)
            else:
                price = BlackScholesEngine.put_price(S, K, T, r, sigma)
            
            vega = BlackScholesEngine.vega(S, K, T, r, sigma)
            
            if vega < 1e-10:  # Avoid division by zero
                break
            
            diff = option_price - price
            
            if abs(diff) < tolerance:
                return float(sigma)
            
            # Newton-Raphson update
            sigma = sigma + diff / vega
            
            # Keep sigma in reasonable bounds
            sigma = max(0.001, min(sigma, 5.0))
        
        return float(sigma)
    
    @staticmethod
    def vega(S: float, K: float, T: float, r: float, sigma: float) -> float:
        """Vega: sensitivity to volatility"""
        d1 = BlackScholesEngine.d1(S, K, T, r, sigma)
        return float(S * norm.pdf(d1) * np.sqrt(T))
    
    @staticmethod
    def delta_call(S: float, K: float, T: float, r: float, sigma: float) -> float:
        """Call delta"""
        d1 = BlackScholesEngine.d1(S, K, T, r, sigma)
        return float(norm.cdf(d1))
    
    @staticmethod
    def delta_put(S: float, K: float, T: float, r: float, sigma: float) -> float:
        """Put delta"""
        d1 = BlackScholesEngine.d1(S, K, T, r, sigma)
        return float(norm.cdf(d1) - 1)
    
    @staticmethod
    def gamma(S: float, K: float, T: float, r: float, sigma: float) -> float:
        """Gamma (same for calls and puts)"""
        d1 = BlackScholesEngine.d1(S, K, T, r, sigma)
        return float(norm.pdf(d1) / (S * sigma * np.sqrt(T)))
    
    @staticmethod
    def theta_call(S: float, K: float, T: float, r: float, sigma: float) -> float:
        """Call theta (daily)"""
        d1 = BlackScholesEngine.d1(S, K, T, r, sigma)
        d2 = BlackScholesEngine.d2(S, K, T, r, sigma)
        
        term1 = -(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T))
        term2 = -r * K * np.exp(-r*T) * norm.cdf(d2)
        
        return float((term1 + term2) / 365)
    
    @staticmethod
    def rho_call(S: float, K: float, T: float, r: float, sigma: float) -> float:
        """Call rho (per 1% change in r)"""
        d2 = BlackScholesEngine.d2(S, K, T, r, sigma)
        return float(K * T * np.exp(-r*T) * norm.cdf(d2) / 100)
