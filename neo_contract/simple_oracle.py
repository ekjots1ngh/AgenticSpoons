from typing import Any

from boa3.sc import runtime, storage
from boa3.sc.compiletime import NeoMetadata, public
from boa3.sc.types import UInt160


OWNER_KEY = b'owner'


@public
def _deploy(data: Any, update: bool) -> None:
    """Initialize on deployment"""
    if not update:
        owner = runtime.script_container.sender
        storage.put_uint160(OWNER_KEY, owner)


@public
def verify() -> bool:
    """Simple verification"""
    return True


@public
def get_owner() -> UInt160:
    """Get owner"""
    owner = storage.get_uint160(OWNER_KEY)
    if owner is None:
        return UInt160()
    return owner


@public
def set_owner(new_owner: UInt160) -> bool:
    """Set new owner"""
    owner = storage.get_uint160(OWNER_KEY)
    if owner is not None and not runtime.check_witness(owner):
        return False
    
    storage.put_uint160(OWNER_KEY, new_owner)
    return True


def manifest() -> NeoMetadata:
    """Metadata"""
    meta = NeoMetadata()
    meta.author = "AgentSpoons"
    meta.description = "Simple volatility oracle"
    return meta
