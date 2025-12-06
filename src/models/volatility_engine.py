"""
Volatility Calculation Engine
"""
import numpy as np
import pandas as pd
from scipy.stats import norm
from scipy.optimize import newton
from typing import Optional

class VolatilityEngine:
    """Core volatility calculation engine"""
    
    def __init__(self, data: pd.DataFrame):
        """
        data: DataFrame with columns ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        """
        self.data = data
        self.returns = np.log(data['close'] / data['close'].shift(1)).dropna()
    
    def close_to_close_vol(self, window: int = 30) -> float:
        """
        Standard historical volatility
        Formula: σ = sqrt(252) * std(log returns)
        """
        if len(self.returns) < window:
            return np.nan
        return float(self.returns.tail(window).std() * np.sqrt(252))
    
    def parkinson_vol(self, window: int = 30) -> float:
        """
        Parkinson volatility - uses high-low range
        More efficient than close-to-close
        """
        if len(self.data) < window:
            return np.nan
        
        hl = np.log(self.data['high'] / self.data['low']).tail(window)
        return float(np.sqrt(252 / (4 * np.log(2)) * (hl ** 2).mean()))
    
    def garman_klass_vol(self, window: int = 30) -> float:
        """
        Garman-Klass volatility - uses OHLC
        Best unbiased OHLC estimator
        """
        if len(self.data) < window:
            return np.nan
        
        df = self.data.tail(window)
        hl = np.log(df['high'] / df['low']) ** 2
        co = np.log(df['close'] / df['open']) ** 2
        
        gk = 0.5 * hl - (2 * np.log(2) - 1) * co
        return float(np.sqrt(252 * gk.mean()))
    
    def rogers_satchell_vol(self, window: int = 30) -> float:
        """
        Rogers-Satchell volatility - allows for drift
        """
        if len(self.data) < window:
            return np.nan
        
        df = self.data.tail(window)
        hc = np.log(df['high'] / df['close'])
        ho = np.log(df['high'] / df['open'])
        lc = np.log(df['low'] / df['close'])
        lo = np.log(df['low'] / df['open'])
        
        rs = hc * ho + lc * lo
        return float(np.sqrt(252 * rs.mean()))
    
    def yang_zhang_vol(self, window: int = 30) -> float:
        """
        Yang-Zhang volatility - combines multiple estimators
        Most accurate historical volatility estimator
        """
        if len(self.data) < window:
            return np.nan
        
        df = self.data.tail(window)
        
        # Overnight volatility
        ho = np.log(df['open'] / df['close'].shift(1))
        overnight_vol = ho.var()
        
        # Open to close volatility (Rogers-Satchell)
        hc = np.log(df['high'] / df['close'])
        ho = np.log(df['high'] / df['open'])
        lc = np.log(df['low'] / df['close'])
        lo = np.log(df['low'] / df['open'])
        rs = (hc * ho + lc * lo).mean()
        
        # Close to close volatility
        cc = np.log(df['close'] / df['close'].shift(1))
        close_vol = cc.var()
        
        # Yang-Zhang combination
        k = 0.34 / (1.34 + (window + 1) / (window - 1))
        yz = overnight_vol + k * close_vol + (1 - k) * rs
        
        return float(np.sqrt(252 * yz))
