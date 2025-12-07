"""
Neo N3 Smart Contract: Volatility Oracle (Simplified)

This is a minimal working example to verify boa3 compilation works.
"""

from typing import Any
from boa3.sc.types import UInt160
from boa3.sc.runtime import script_container, check_witness, time, notify
from boa3.sc import storage

OWNER_KEY = b'owner'
DATA_PREFIX = b'vol_'


def _deploy(data: Any, update: bool):
    """Initialize contract on first deploy"""
    if not update:
        storage.put(OWNER_KEY, script_container.sender)


def update_volatility(pair: str, price: int, realized_vol: int, implied_vol: int) -> bool:
    """Update volatility data for a trading pair"""
    owner = storage.get(OWNER_KEY)
    if owner is None or not check_witness(owner):
        return False
    
    # Store data as pipe-separated values
    timestamp = time
    data_str = f"{price}|{realized_vol}|{implied_vol}|{timestamp}"
    key = DATA_PREFIX + pair.encode()
    storage.put(key, data_str)
    
    return True


def get_volatility(pair: str) -> str:
    """Retrieve volatility data for a pair"""
    key = DATA_PREFIX + pair.encode()
    data = storage.get(key)
    
    if data is None:
        return ""
    
    # Try to decode if it's bytes
    if isinstance(data, bytes):
        return data.decode()
    else:
        return str(data)


def verify() -> bool:
    """Simple verification"""
    return True
