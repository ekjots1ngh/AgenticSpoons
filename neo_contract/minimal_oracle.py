"""
Neo N3 Smart Contract: Volatility Oracle - Minimal Version

Simplified contract to test boa3 compilation
"""

from boa3.sc.types import UInt160
from boa3.sc.runtime import check_witness, script_container
from boa3.sc import storage


# Contract owner
OWNER = b'owner'


def set_owner(owner: UInt160) -> bool:
    """Set contract owner"""
    current_owner = storage.get_uint160(OWNER)
    if current_owner is not None and not check_witness(current_owner):
        return False
    
    storage.put_uint160(OWNER, owner)
    return True


def get_owner() -> UInt160:
    """Get contract owner"""
    owner = storage.get_uint160(OWNER)
    if owner is None:
        return UInt160()
    return owner


def verify() -> bool:
    """Verification method"""
    return True
