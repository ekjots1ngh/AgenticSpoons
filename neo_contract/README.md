# AgentSpoons Volatility Oracle - Neo N3 Smart Contract

A Neo N3 smart contract for publishing real-time volatility data on-chain.

## Status

**Current State**: Development in progress
- ✅ Neo SDK installed and verified (neo3-lib, neo3-boa v1.4.1, neo3crypto, neo-mamba)
- ✅ Contract architecture designed
- 🔧 Compilation: Working with boa3 compiler (resolving type system details)
- ⏳ Testing: Pending contract deployment on testnet
- ⏳ Integration: Ready for volatility data pipeline

## Files

- `volatility_oracle.py` - Main contract implementation (in development)
- `minimal_oracle.py` - Simplified contract for testing compilation
- `volatility_oracle_simple.py` - Alternative simpler version
- `compile.py` - Compilation helper script
- `deploy.py` - Deployment workflow documentation

## Overview

This contract enables AgentSpoons to publish volatility metrics (realized volatility, implied volatility, and prices) directly on the Neo N3 blockchain, making them available to DeFi protocols, options platforms, and other smart contracts.

## Features

- **Real-time Data Publishing**: Update volatility data for any trading pair
- **Secure Access Control**: Only authorized oracles can update data
- **Efficient Storage**: Compact data format to minimize gas costs
- **Query Interface**: Simple methods to read current volatility
- **Multi-Pair Support**: Handle multiple trading pairs simultaneously

## Contract Methods (Target API)

### `update_volatility(pair, price, realized_vol, implied_vol) → bool`

Update volatility metrics for a trading pair.

**Parameters:**
- `pair` (str): Trading pair identifier (e.g., "NEO/USDT", "BTC/USD")
- `price` (int): Current price scaled by 10^8 (fixed-point format)
- `realized_vol` (int): Realized volatility scaled by 10^8
- `implied_vol` (int): Implied volatility scaled by 10^8

**Returns:** `true` if successful, `false` if unauthorized

**Example:**
```
# Update NEO/USDT: price=$15.00, RV=52%, IV=58%
update_volatility("NEO/USDT", 1500000000, 52000000, 58000000)
```

### `get_volatility(pair) → str`

Retrieve latest volatility data for a pair.

**Parameters:**
- `pair` (str): Trading pair identifier

**Returns:** Data string in format `"price|realized_vol|implied_vol|timestamp"` or empty if no data

**Example:**
```
get_volatility("NEO/USDT")
→ "1500000000|52000000|58000000|1701964800"
```

### `get_owner() → UInt160`

Get the contract owner address.

### `verify() → bool`

Simple test method to verify contract is deployed and working.

## Data Format

All numerical values use fixed-point representation with 8 decimal places:

| Field | Raw Value | Scaled By | Example |
|-------|-----------|-----------|---------|
| Price | 1500000000 | 10^8 | $15.00 |
| Volatility | 52000000 | 10^8 | 52.00% |
| Timestamp | Unix timestamp | 1 | 1701964800 |

## Compilation

To compile the contract to Neo bytecode:

```bash
# Using boa3 CLI directly
python -m boa3.cli compile volatility_oracle.py

# This generates:
# - volatility_oracle.nef - Compiled bytecode
# - volatility_oracle.manifest.json - Contract ABI and metadata
```

**Note**: Requires boa3 v1.4.1+ and proper Neo SDK setup

## Development Notes

### boa3 Type System

boa3 v1.4.1 has strict typing requirements:
- Use `storage.get_uint160()`, `storage.get_str()`, etc. instead of generic `storage.get()`
- All function parameters must have type hints
- Storage keys must be bytes (prefixed with `b''`)
- Complex string operations may require workarounds

### Next Steps

1. **Resolve compilation issues** with current contract implementation
   - Ensure all type hints match boa3 requirements
   - Test with minimal contract first
   - Gradually add features

2. **Test on testnet**
   - Deploy compiled contract to Neo N3 testnet
   - Verify all methods execute correctly
   - Check gas costs

3. **Integration**
   - Create Python client library for contract interaction
   - Connect to AgentSpoons volatility calculation pipeline
   - Set up automated data publication

4. **Mainnet deployment**
   - Audit contract for security
   - Deploy to Neo N3 mainnet
   - Monitor contract state

## Neo N3 Resources

- [Neo N3 Documentation](https://docs.neo.org/)
- [neo3-boa GitHub](https://github.com/CityOfZion/neo3-boa)
- [neo3-lib GitHub](https://github.com/CityOfZion/neo3-lib)
- [Neo Smart Contract ABI](https://docs.neo.org/n3/intro/index.html)

## Development Environment

- **Python**: 3.12.4
- **neo3-boa**: v1.4.1
- **neo3-lib**: v4.x
- **neo3crypto**: Latest
- **neo-mamba**: v3.1.0

## License

MIT - Part of AgentSpoons project
