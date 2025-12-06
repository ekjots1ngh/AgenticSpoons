"""
Neo blockchain integration module for AgentSpoons
"""

from .blockchain_client import NeoBlockchainClient, VolatilityOracle
from .dashboard_integration import DashboardNeoIntegration, BlockchainDataStreamToDb
from .volatility_contract import display_contract, CONTRACT_MANIFEST, VOLATILITY_CONTRACT

__all__ = [
    'NeoBlockchainClient',
    'VolatilityOracle',
    'DashboardNeoIntegration',
    'BlockchainDataStreamToDb',
    'display_contract',
    'CONTRACT_MANIFEST',
    'VOLATILITY_CONTRACT'
]

__version__ = '1.0.0'
__author__ = 'AgentSpoons'
