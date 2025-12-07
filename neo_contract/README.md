# AgentSpoons Volatility Oracle - Neo N3 Smart Contract

A production-ready smart contract for publishing real-time volatility data to the Neo N3 blockchain.

## Overview

This contract enables AgentSpoons to publish volatility metrics (realized volatility, implied volatility, and prices) directly on-chain, making them available to DeFi protocols, options platforms, and other smart contracts.

## Features

- **Real-time Data Publishing**: Update volatility data for any trading pair
- **Secure Access Control**: Only authorized oracles can update data
- **Efficient Storage**: Compact data format to minimize gas costs
- **Query Interface**: Simple methods to read current volatility
- **Multi-Pair Support**: Handle multiple trading pairs simultaneously

## Contract Methods

### `update_volatility(pair, price, realized_vol, implied_vol) → bool`

Update volatility metrics for a trading pair.

**Parameters:**
- `pair` (str): Trading pair identifier (e.g., "NEO/USDT", "BTC/USD")
- `price` (int): Current price scaled by 10^8 (fixed-point format)
- `realized_vol` (int): Realized volatility scaled by 10^8
- `implied_vol` (int): Implied volatility scaled by 10^8

**Returns:** `true` if successful, `false` if unauthorized

**Example:**
```python
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

Compile the contract to Neo bytecode:

```bash
python compile.py
```

This generates:
- `volatility_oracle.nef` - Compiled bytecode
- `volatility_oracle.manifest.json` - Contract ABI and metadata

## Deployment

### Testnet Deployment

1. Get testnet GAS from faucet
2. Deploy using neo-cli or neon:
   ```bash
   python deploy.py
   ```

### Mainnet Deployment

1. Ensure sufficient GAS available
2. Deploy contract to mainnet
3. Update contract address in AgentSpoons configuration
4. Start publishing volatility feeds

## Integration with AgentSpoons

### Data Flow

```
AgentSpoons Agents
    ↓
Volatility Calculation
    ↓
Neo Contract (on-chain)
    ↓
DeFi Protocols, Options Platforms, etc.
```

### Usage Example

```python
from neo3.wallet import Account
from neo_oracle_client import OracleClient

# Connect to contract
client = OracleClient(contract_hash="0x...")

# Update volatility
client.update_volatility(
    pair="NEO/USDT",
    price=15.00,
    realized_vol=0.52,
    implied_vol=0.58
)

# Read volatility
data = client.get_volatility("NEO/USDT")
print(f"Current volatility: {data['realized_vol']:.2%}")
```

## Security Considerations

1. **Access Control**: Only authorized addresses can update data
2. **Timestamp**: Each update includes blockchain timestamp
3. **Data Validation**: Contract validates input ranges
4. **Storage**: Efficient storage minimizes state bloat

## Gas Costs

Approximate gas costs on Neo N3:

| Operation | Approx. GAS |
|-----------|-------------|
| Update volatility | 0.5-1.0 |
| Read volatility | 0.1 |
| Verify | < 0.01 |

## Testing

Test the contract locally:

```bash
python deploy.py
```

This shows the deployment workflow and contract interface.

## References

- [Neo N3 Documentation](https://docs.neo.org/)
- [neo3-boa](https://github.com/CityOfZion/neo3-boa)
- [neo3-lib](https://github.com/CityOfZion/neo3-lib)

## License

MIT - Part of AgentSpoons project
