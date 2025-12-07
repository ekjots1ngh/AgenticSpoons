"""
Neo N3 Smart Contract: Volatility Oracle

This contract provides on-chain volatility data for trading pairs.
Simplified version compatible with boa3 v1.4.1
"""

from typing import Any
from boa3.sc.types import UInt160
from boa3.sc.runtime import script_container, check_witness, time
from boa3.sc import storage

OWNER_KEY = b'owner'
DATA_PREFIX = b'vol_'


def update_volatility(pair: str, price: int, realized_vol: int, implied_vol: int) -> bool:
    """
    Update volatility data for a trading pair
    
    Args:
        pair: Trading pair (e.g. "NEO/USDT")
        price: Price scaled by 10^8
        realized_vol: Realized volatility scaled by 10^8
        implied_vol: Implied volatility scaled by 10^8
    
    Returns:
        True if successful, False otherwise
    """
    owner = storage.get_uint160(OWNER_KEY)
    if owner is None:
        return False
    
    if not check_witness(owner):
        return False
    
    # Store data as pipe-separated values
    timestamp = time
    data_str = f"{price}|{realized_vol}|{implied_vol}|{timestamp}"
    key = b'vol_' + pair.encode()
    storage.put(key, data_str.encode())
    
    return True


def get_volatility(pair: str) -> str:
    """
    Retrieve volatility data for a pair
    
    Args:
        pair: Trading pair
    
    Returns:
        Data string in format "price|realized_vol|implied_vol|timestamp"
        or empty string if not found
    """
    key = b'vol_' + pair.encode()
    data = storage.get(key)
    
    if data is None:
        return ""
    
    return data.decode()


def verify() -> bool:
    """Simple verification that contract is working"""
    return True


def set_owner(new_owner: UInt160) -> bool:
    """Set the contract owner (requires witness from current owner)"""
    owner = storage.get(OWNER_KEY)
    if owner is None:
        # First time setting owner
        storage.put(OWNER_KEY, new_owner)
        return True
    
    if not check_witness(owner):
        return False
    
    storage.put(OWNER_KEY, new_owner)
    return True


def get_owner() -> UInt160:
    """Get the current contract owner"""
    owner = storage.get_uint160(OWNER_KEY)
    if owner is None:
        return UInt160()
    return owner
