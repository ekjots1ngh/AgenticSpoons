"""
Volatility Models Module
Contains advanced GARCH models and backtesting infrastructure
"""

from .advanced_garch import (
    AdvancedGARCH,
    VolatilityBacktest,
    VolArbitrageStrategy
)

__all__ = [
    'AdvancedGARCH',
    'VolatilityBacktest',
    'VolArbitrageStrategy'
]

__version__ = '1.0.0'
