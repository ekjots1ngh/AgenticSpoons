"""
AgentSpoons Volatility Oracle Smart Contract
Neo N3 contract for storing and querying volatility data

Usage with neo3-boa:
    from boa3.builtin import CreateMap, NeoAssert, Emit
    from boa3.builtin.interop.storage import get, put
    
    def deploy() -> bool:
        # Initialize storage
        return True
    
    def update_volatility(pair: str, volatility: int, timestamp: int) -> bool:
        # Store: pair -> (volatility, timestamp)
        return True
    
    def get_volatility(pair: str) -> int:
        # Retrieve stored volatility
        return 0
"""

VOLATILITY_CONTRACT = '''
from boa3.builtin import CreateMap, NeoAssert, Emit
from boa3.builtin.interop.storage import get, put, delete
from boa3.builtin.type import UInt160
from typing import Dict, Tuple

# Events
class VolatilityUpdated:
    def __init__(self, pair: str, volatility: int, timestamp: int):
        self.pair = pair
        self.volatility = volatility
        self.timestamp = timestamp

class ContractDeployed:
    def __init__(self, owner: UInt160, timestamp: int):
        self.owner = owner
        self.timestamp = timestamp

# Storage keys
STORAGE_PREFIX = b'vol_'
METADATA_PREFIX = b'meta_'

# State variables
owner: UInt160
total_updates: int
pairs_tracked: list

def deploy() -> bool:
    """Deploy contract - initialize storage"""
    storage.put(METADATA_PREFIX + b'version', 1)
    storage.put(METADATA_PREFIX + b'total_updates', 0)
    storage.put(METADATA_PREFIX + b'active', True)
    return True

def update_volatility(pair: str, volatility: int, timestamp: int) -> bool:
    """
    Update volatility for a pair
    
    Args:
        pair: Trading pair (e.g. 'NEO/USDT')
        volatility: Volatility in basis points (e.g. 4500 = 45.00%)
        timestamp: Unix timestamp
    
    Returns:
        True if successful
    """
    # Validate inputs
    assert len(pair) > 0, "Pair cannot be empty"
    assert volatility > 0, "Volatility must be positive"
    assert timestamp > 0, "Timestamp must be positive"
    
    # Check contract is active
    is_active = storage.get(METADATA_PREFIX + b'active')
    assert is_active == 1, "Contract is not active"
    
    # Store volatility data
    key = STORAGE_PREFIX + pair.encode()
    data = {
        'volatility': volatility,
        'timestamp': timestamp,
        'updated_at': int(timestamp)
    }
    
    storage.put(key, data)
    
    # Update counter
    total = storage.get(METADATA_PREFIX + b'total_updates') or 0
    storage.put(METADATA_PREFIX + b'total_updates', total + 1)
    
    # Emit event
    Emit(VolatilityUpdated(pair, volatility, timestamp))
    
    return True

def get_volatility(pair: str) -> int:
    """
    Get volatility for a pair
    
    Args:
        pair: Trading pair
    
    Returns:
        Current volatility in basis points
    """
    key = STORAGE_PREFIX + pair.encode()
    data = storage.get(key)
    
    if data is None:
        return 0
    
    return data.get('volatility', 0)

def get_volatility_timestamp(pair: str) -> int:
    """Get timestamp of last update for pair"""
    key = STORAGE_PREFIX + pair.encode()
    data = storage.get(key)
    
    if data is None:
        return 0
    
    return data.get('timestamp', 0)

def get_all_volatilities() -> Dict[str, int]:
    """Get all tracked pairs and their volatilities"""
    result = {}
    
    # Iterate storage to find all pairs
    for item in storage.iterator(STORAGE_PREFIX):
        pair = item.key.decode().replace(STORAGE_PREFIX.decode(), '')
        vol = item.value.get('volatility', 0)
        result[pair] = vol
    
    return result

def get_total_updates() -> int:
    """Get total number of updates"""
    total = storage.get(METADATA_PREFIX + b'total_updates') or 0
    return total

def set_active(active: bool) -> bool:
    """Enable/disable contract"""
    storage.put(METADATA_PREFIX + b'active', 1 if active else 0)
    return True

def is_active() -> bool:
    """Check if contract is active"""
    return storage.get(METADATA_PREFIX + b'active') == 1

def get_contract_info() -> Dict:
    """Get contract information"""
    return {
        'version': storage.get(METADATA_PREFIX + b'version') or 1,
        'total_updates': get_total_updates(),
        'active': is_active(),
        'pairs_tracked': len(get_all_volatilities())
    }
'''

# Example manifest for contract deployment
CONTRACT_MANIFEST = {
    "name": "VolatilityOracle",
    "groups": [],
    "features": {},
    "supportedstandards": [],
    "abi": {
        "methods": [
            {
                "name": "deploy",
                "parameters": [],
                "returntype": "Boolean",
                "offset": 0,
                "safe": False
            },
            {
                "name": "update_volatility",
                "parameters": [
                    {"name": "pair", "type": "String"},
                    {"name": "volatility", "type": "Integer"},
                    {"name": "timestamp", "type": "Integer"}
                ],
                "returntype": "Boolean",
                "offset": 100,
                "safe": False
            },
            {
                "name": "get_volatility",
                "parameters": [
                    {"name": "pair", "type": "String"}
                ],
                "returntype": "Integer",
                "offset": 200,
                "safe": True
            },
            {
                "name": "get_volatility_timestamp",
                "parameters": [
                    {"name": "pair", "type": "String"}
                ],
                "returntype": "Integer",
                "offset": 300,
                "safe": True
            },
            {
                "name": "get_all_volatilities",
                "parameters": [],
                "returntype": "Map",
                "offset": 400,
                "safe": True
            },
            {
                "name": "get_total_updates",
                "parameters": [],
                "returntype": "Integer",
                "offset": 500,
                "safe": True
            },
            {
                "name": "get_contract_info",
                "parameters": [],
                "returntype": "Map",
                "offset": 600,
                "safe": True
            }
        ],
        "events": [
            {
                "name": "VolatilityUpdated",
                "parameters": [
                    {"name": "pair", "type": "String"},
                    {"name": "volatility", "type": "Integer"},
                    {"name": "timestamp", "type": "Integer"}
                ]
            },
            {
                "name": "ContractDeployed",
                "parameters": [
                    {"name": "owner", "type": "Hash160"},
                    {"name": "timestamp", "type": "Integer"}
                ]
            }
        ]
    },
    "permissions": [
        {
            "contract": "*",
            "methods": "*"
        }
    ],
    "trusts": [],
    "extra": {
        "author": "AgentSpoons",
        "version": "1.0.0",
        "description": "Volatility Oracle for NEO blockchain"
    }
}


def display_contract():
    """Display contract information"""
    from loguru import logger
    
    logger.info("=== AgentSpoons Volatility Oracle Contract ===")
    logger.info("Network: Neo N3")
    logger.info("Language: Python (boa3)")
    logger.info("")
    
    logger.info("Contract Functions:")
    logger.info("1. deploy() -> bool")
    logger.info("   Initialize contract storage")
    logger.info("")
    
    logger.info("2. update_volatility(pair: str, volatility: int, timestamp: int) -> bool")
    logger.info("   Store volatility data for a trading pair")
    logger.info("   Args:")
    logger.info("     pair: Trading pair (e.g. 'NEO/USDT')")
    logger.info("     volatility: Basis points (4500 = 45%)")
    logger.info("     timestamp: Unix timestamp")
    logger.info("")
    
    logger.info("3. get_volatility(pair: str) -> int")
    logger.info("   Retrieve current volatility for pair")
    logger.info("")
    
    logger.info("4. get_all_volatilities() -> Dict")
    logger.info("   Get all tracked pairs and values")
    logger.info("")
    
    logger.info("5. get_contract_info() -> Dict")
    logger.info("   Get contract metadata")
    logger.info("")
    
    logger.info("Events:")
    logger.info("- VolatilityUpdated(pair, volatility, timestamp)")
    logger.info("- ContractDeployed(owner, timestamp)")
    logger.info("")
    
    logger.info("Use Cases:")
    logger.info("✓ Store real-time volatility from AgentSpoons")
    logger.info("✓ Query volatility from other contracts")
    logger.info("✓ Track volatility history on-chain")
    logger.info("✓ Enable trustless volatility derivatives")


if __name__ == "__main__":
    display_contract()
