"""
Comprehensive test suite for volatility models
"""
import pytest
import numpy as np
from hypothesis import given, strategies as st

from src.models.volatility_engine import VolatilityEstimators
from src.models.garch_forecaster import GARCHForecaster
from src.models.black_scholes import BlackScholesModel

class TestVolatilityEstimators:
    """Test all volatility estimators"""
    
    def test_close_to_close(self):
        """Test basic close-to-close volatility"""
        prices = np.array([100, 102, 101, 103, 102])
        vol = VolatilityEstimators.close_to_close(prices)
        
        assert vol > 0, "Volatility must be positive"
        assert vol < 1.0, "Volatility seems unreasonably high"
    
    def test_garman_klass(self):
        """Test Garman-Klass estimator"""
        ohlc = [
            (100, 105, 98, 102),
            (102, 106, 100, 104),
            (104, 108, 102, 105)
        ]
        
        vol = VolatilityEstimators.garman_klass(ohlc)
        
        assert vol > 0
        assert isinstance(vol, float)
    
    @given(st.lists(st.floats(min_value=50, max_value=150), min_size=30, max_size=100))
    def test_volatility_properties(self, prices):
        """Property-based testing with Hypothesis"""
        prices_array = np.array(prices)
        
        # Volatility should be positive
        vol = VolatilityEstimators.close_to_close(prices_array)
        assert vol >= 0
        
        # Should be scale-invariant
        scaled_prices = prices_array * 2
        scaled_vol = VolatilityEstimators.close_to_close(scaled_prices)
        assert abs(vol - scaled_vol) < 0.01

class TestGARCH:
    """Test GARCH model"""
    
    def test_garch_fit(self):
        """Test GARCH model fitting"""
        np.random.seed(42)
        returns = np.random.normal(0, 0.02, 500)
        
        garch = GARCHForecaster()
        params = garch.fit(returns)
        
        assert 'omega' in params
        assert 'alpha' in params
        assert 'beta' in params
        
        # Check stationarity
        assert params['alpha'] + params['beta'] < 1
    
    def test_garch_forecast(self):
        """Test GARCH forecasting"""
        np.random.seed(42)
        returns = np.random.normal(0, 0.02, 500)
        
        garch = GARCHForecaster()
        garch.fit(returns)
        
        forecast = garch.forecast(horizon=10)
        
        assert len(forecast) == 10
        assert all(f > 0 for f in forecast)

class TestBlackScholes:
    """Test Black-Scholes model"""
    
    def test_call_price(self):
        """Test call option pricing"""
        bs = BlackScholesModel(S=100, K=100, T=1, r=0.05, sigma=0.2)
        call_price = bs.call_price()
        
        assert call_price > 0
        assert call_price < 100  # Can't be worth more than stock
    
    def test_put_call_parity(self):
        """Test put-call parity relationship"""
        S, K, T, r, sigma = 100, 100, 1, 0.05, 0.2
        
        bs = BlackScholesModel(S, K, T, r, sigma)
        
        call = bs.call_price()
        put = bs.put_price()
        
        # Put-call parity: C - P = S - K*e^(-rT)
        lhs = call - put
        rhs = S - K * np.exp(-r * T)
        
        assert abs(lhs - rhs) < 0.01
    
    def test_greeks_range(self):
        """Test Greeks are in reasonable ranges"""
        bs = BlackScholesModel(S=100, K=100, T=0.5, r=0.05, sigma=0.2)
        
        delta = bs.delta('call')
        gamma = bs.gamma()
        vega = bs.vega()
        
        assert 0 <= delta <= 1  # Call delta
        assert gamma >= 0       # Always positive
        assert vega >= 0        # Always positive
    
    @pytest.mark.parametrize("S,K,expected_delta", [
        (120, 100, 0.9),   # Deep ITM
        (100, 100, 0.5),   # ATM
        (80, 100, 0.1),    # Deep OTM
    ])
    def test_delta_moneyness(self, S, K, expected_delta):
        """Test delta varies with moneyness"""
        bs = BlackScholesModel(S, K, T=1, r=0.05, sigma=0.2)
        delta = bs.delta('call')
        
        # Allow 20% tolerance
        assert abs(delta - expected_delta) < 0.2

class TestIntegration:
    """Integration tests"""
    
    @pytest.mark.asyncio
    async def test_full_pipeline(self):
        """Test complete data pipeline"""
        # This would test the full agent system
        pass

# Performance tests
class TestPerformance:
    """Performance benchmarks"""
    
    def test_volatility_calculation_speed(self, benchmark):
        """Benchmark volatility calculation"""
        prices = np.random.randn(1000) * 0.02 + 100
        
        result = benchmark(VolatilityEstimators.close_to_close, prices)
        
        assert result > 0
    
    def test_black_scholes_speed(self, benchmark):
        """Benchmark Black-Scholes pricing"""
        def price_option():
            bs = BlackScholesModel(100, 100, 1, 0.05, 0.2)
            return bs.call_price()
        
        result = benchmark(price_option)
        
        assert result > 0

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=src", "--cov-report=html"])
