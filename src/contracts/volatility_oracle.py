"""
Neo N3 Smart Contract - Volatility Oracle
Compile with: neo3-boa compile volatility_oracle.py
"""
from typing import Any
from boa3.builtin import NeoMetadata, metadata, public
from boa3.builtin.contract import Nep17TransferEvent, abort
from boa3.builtin.interop.runtime import check_witness, calling_script_hash
from boa3.builtin.interop.storage import get, put, delete
from boa3.builtin.type import UInt160

# Contract metadata
@metadata
def manifest_metadata() -> NeoMetadata:
    meta = NeoMetadata()
    meta.author = "AgentSpoons Team"
    meta.description = "Decentralized Volatility Oracle for Neo"
    meta.email = "team@agentspoons.io"
    return meta

# Storage keys
OWNER_KEY = b'owner'
ORACLE_PREFIX = b'oracle_'
PUBLISHER_PREFIX = b'publisher_'

@public
def _deploy(data: Any, update: bool):
    """
    Initializes the contract on deployment
    """
    if not update:
        # Set contract owner
        tx = calling_script_hash
        put(OWNER_KEY, tx)

@public
def get_owner() -> UInt160:
    """Get contract owner"""
    return UInt160(get(OWNER_KEY))

@public
def update_volatility(pair: str, spot_price: int, realized_vol: int, 
                      implied_vol: int, garch_forecast: int, 
                      timestamp: int) -> bool:
    """
    Update volatility data for a trading pair
    
    Args:
        pair: Trading pair (e.g., "NEO/USDT")
        spot_price: Current spot price (scaled by 10^8)
        realized_vol: Realized volatility (scaled by 10^8, e.g., 0.5 = 50000000)
        implied_vol: Implied volatility (scaled by 10^8)
        garch_forecast: GARCH forecast (scaled by 10^8)
        timestamp: Unix timestamp
    
    Returns:
        True if successful
    """
    # Verify caller is authorized publisher
    caller = calling_script_hash
    publisher_key = PUBLISHER_PREFIX + caller
    
    if get(publisher_key) is None:
        abort()
    
    # Store volatility data
    oracle_key = ORACLE_PREFIX + pair.encode()
    
    data = {
        'pair': pair,
        'spot_price': spot_price,
        'realized_vol': realized_vol,
        'implied_vol': implied_vol,
        'garch_forecast': garch_forecast,
        'timestamp': timestamp,
        'publisher': caller
    }
    
    # Serialize and store (simplified - use proper serialization in production)
    put(oracle_key, str(data).encode())
    
    return True

@public
def get_volatility(pair: str) -> str:
    """
    Get latest volatility data for a pair
    
    Args:
        pair: Trading pair
    
    Returns:
        Volatility data as string
    """
    oracle_key = ORACLE_PREFIX + pair.encode()
    data = get(oracle_key)
    
    if data is None:
        return ""
    
    return data.decode()

@public
def add_publisher(publisher: UInt160) -> bool:
    """
    Add authorized oracle publisher (owner only)
    
    Args:
        publisher: Address to authorize
    """
    owner = UInt160(get(OWNER_KEY))
    
    if not check_witness(owner):
        abort()
    
    publisher_key = PUBLISHER_PREFIX + publisher
    put(publisher_key, b'1')
    
    return True

@public
def remove_publisher(publisher: UInt160) -> bool:
    """
    Remove oracle publisher (owner only)
    """
    owner = UInt160(get(OWNER_KEY))
    
    if not check_witness(owner):
        abort()
    
    publisher_key = PUBLISHER_PREFIX + address
    delete(publisher_key)
    
    return True

@public
def is_publisher(address: UInt160) -> bool:
    """Check if address is authorized publisher"""
    publisher_key = PUBLISHER_PREFIX + address
    return get(publisher_key) is not None
