
# AgentSpoons API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication
Currently no authentication required for testnet. Production will use API keys.

---

## Endpoints

### GET `/volatility/{pair}`

Get latest volatility data for a trading pair.

**Parameters:**
- `pair` (string, required): Trading pair (e.g., "NEO/USDT")

**Example Request:**
```bash
curl http://localhost:8000/volatility/NEO/USDT
```

**Example Response:**
```json
{
  "pair": "NEO/USDT",
  "timestamp": "2024-12-07T10:30:00Z",
  "price": 15.23,
  "realized_volatility": 0.523,
  "implied_volatility": 0.581,
  "spread": 0.058,
  "garch_forecast": 0.547,
  "estimators": {
    "close_to_close": 0.520,
    "parkinson": 0.525,
    "garman_klass": 0.523,
    "rogers_satchell": 0.522,
    "yang_zhang": 0.524,
    "realized_kernel": 0.523,
    "bipower_variation": 0.521
  },
  "confidence": 0.95,
  "neo_tx_hash": "0x7a2bf3c9..."
}
```

---

### GET `/forecast/{pair}`

Get GARCH volatility forecast.

**Parameters:**
- `pair` (string, required): Trading pair
- `horizon` (int, optional): Days ahead (default: 7)

**Example:**
```bash
curl http://localhost:8000/forecast/NEO/USDT?horizon=30
```

**Response:**
```json
{
  "pair": "NEO/USDT",
  "model": "GARCH(1,1)",
  "forecasts": {
    "1d": 0.547,
    "7d": 0.562,
    "30d": 0.538
  },
  "accuracy_historical": 0.873,
  "parameters": {
    "omega": 0.00001,
    "alpha": 0.08,
    "beta": 0.90
  }
}
```

---

### GET `/arbitrage/{pair}`

Detect IV-RV arbitrage opportunities.

**Response:**
```json
{
  "opportunities_found": 3,
  "best_opportunity": {
    "strategy": "sell_implied_buy_realized",
    "expected_profit_pct": 5.8,
    "confidence": 0.85,
    "implied_vol": 0.581,
    "realized_vol": 0.523,
    "spread": 0.058,
    "recommended_action": "SELL IV / BUY RV"
  }
}
```

---

### GET `/neo/status`

Get Neo blockchain integration status.

**Response:**
```json
{
  "network": "Neo N3 Testnet",
  "contract_hash": "0x7a2b...f3c9",
  "last_publication": "2024-12-07T10:25:00Z",
  "total_publications": 1247,
  "gas_used_total": 12.47,
  "status": "healthy",
  "explorer_url": "https://testnet.neotube.io/contract/0x7a2b...f3c9"
}
```

---

## Rate Limits

| Tier | Requests/Minute | Cost |
|------|-----------------|------|
| Free (Testnet) | 60 | $0 |
| Basic | 600 | $49/month |
| Pro | 6000 | $199/month |
| Enterprise | Unlimited | Contact us |

---

## WebSocket API

Subscribe to real-time updates:
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/volatility/NEO/USDT');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('New volatility:', data.realized_volatility);
};
```

---

## Error Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Invalid request |
| 404 | Pair not found |
| 429 | Rate limit exceeded |
| 500 | Internal server error |
| 503 | Neo blockchain unavailable |

---

## SDK Examples

### Python
```python
import requests

response = requests.get('http://localhost:8000/volatility/NEO/USDT')
data = response.json()
print(f"Realized Vol: {data['realized_volatility']:.2%}")
```

### JavaScript
```javascript
fetch('http://localhost:8000/volatility/NEO/USDT')
  .then(res => res.json())
  .then(data => console.log(`RV: ${data.realized_volatility}`));
```

### cURL
```bash
curl -X GET "http://localhost:8000/volatility/NEO/USDT"      -H "accept: application/json"
```

---

## Support

- Email: support@agentspoons.io
- Discord: [Join Community](https://discord.gg/agentspoons)
- GitHub Issues: [Report Bug](https://github.com/yourusername/agentspoons/issues)

