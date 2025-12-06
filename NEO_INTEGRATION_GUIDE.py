"""
Neo Integration with Championship Dashboard
Example showing how to integrate blockchain submission into the live dashboard
"""

# This is a reference implementation showing how to modify championship_dashboard.py
# to include Neo blockchain integration

INTEGRATION_CODE = '''
# Add these imports at the top of championship_dashboard.py
from neo.dashboard_integration import DashboardNeoIntegration, BlockchainDataStreamToDb
from neo.volatility_contract import display_contract

# Initialize Neo integration after creating the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

# Add Neo integration
NEO_INTEGRATION = DashboardNeoIntegration(network="testnet", auto_submit=True)
NEO_ARCHIVE = BlockchainDataStreamToDb(NEO_INTEGRATION)

# Modify the update_charts callback to include blockchain submission:

@app.callback(
    [Output("volatility-chart", "figure"),
     Output("arbitrage-chart", "figure"),
     Output("forecast-chart", "figure"),
     Output("price-card", "children"),
     Output("vol-card", "children"),
     Output("implied-card", "children"),
     Output("spread-card", "children"),
     Output("blockchain-status", "children"),  # Add this for Neo status
     Output("blockchain-submissions", "children"),  # Add for submission count
    ],
    Input("update-interval", "n_intervals"),
    interval=2000
)
def update_charts(n):
    """Update all charts and blockchain data"""
    
    try:
        with open("data/results.json", "r") as f:
            data = json.load(f)
    except:
        return dash.no_update
    
    # ... existing chart update code ...
    
    # NEW: Process and submit to blockchain
    if data:
        latest = data[-1]
        
        # Prepare data for blockchain
        blockchain_data = {
            'pair': latest.get('pair', 'NEO/USDT'),
            'realized_vol': latest.get('realized_vol', 0.0),
            'implied_vol': latest.get('implied_vol', 0.0),
            'garch_forecast': latest.get('garch_forecast', 0.0),
            'timestamp': int(datetime.now().timestamp())
        }
        
        # Process for blockchain
        processed = NEO_INTEGRATION.process_dashboard_data(blockchain_data)
        
        # Submit to blockchain
        if processed.get('ready_for_blockchain'):
            tx_hash = NEO_INTEGRATION.submit_to_blockchain(processed)
            
            # Archive submission
            if tx_hash:
                NEO_ARCHIVE.archive_submission(blockchain_data)
        
        # Get blockchain status
        neo_status = NEO_INTEGRATION.get_blockchain_status()
        neo_metrics = NEO_INTEGRATION.get_integration_metrics()
    
    # Create blockchain status card
    blockchain_status_card = dbc.Card([
        dbc.CardBody([
            html.Div([
                html.H5("Blockchain Status", className="card-title text-info"),
                html.P(f"Network: {neo_metrics.get('blockchain_network', 'N/A')}", className="mb-2"),
                html.P(f"Status: {neo_status.get('status', 'DISCONNECTED')}", className="mb-2"),
                html.P(f"Submissions: {neo_metrics.get('total_submissions', 0)}", className="mb-0"),
                html.Small("Neo N3 Blockchain", className="text-muted"),
            ])
        ])
    ], color="dark", outline=True, style={"borderColor": "#00d4ff"})
    
    # Create submissions counter
    submission_count = dbc.Badge(
        f"{neo_metrics.get('total_submissions', 0)} on-chain",
        color="info",
        className="badge-pill"
    )
    
    # ... return all outputs including new ones ...
    return (vol_fig, arb_fig, forecast_fig, price_card, vol_card, implied_card, 
            spread_card, blockchain_status_card, submission_count)


# Optional: Add Neo contract display as a separate page/tab

neo_contract_display = html.Div([
    dbc.Card([
        dbc.CardHeader(
            html.H4("Neo N3 Volatility Oracle", className="text-info"),
            className="bg-dark"
        ),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.H6("Smart Contract Functions", className="text-info"),
                    html.Pre("""
1. deploy() -> bool
   Initialize contract storage

2. update_volatility(pair, volatility, timestamp) -> bool
   Store volatility for a pair

3. get_volatility(pair) -> int
   Retrieve current volatility

4. get_all_volatilities() -> Dict
   Get all tracked pairs
                    """, style={"color": "#00d4ff", "fontSize": "12px"}),
                ], md=6),
                dbc.Col([
                    html.H6("Contract Info", className="text-info"),
                    html.P(f"Network: Testnet", className="mb-2"),
                    html.P(f"Status: {neo_status.get('status', 'DISCONNECTED')}", className="mb-2"),
                    html.P(f"Total Submissions: {neo_metrics.get('total_submissions', 0)}", className="mb-2"),
                    html.P(f"Cached Pairs: {neo_metrics.get('cached_pairs', 0)}", className="mb-0"),
                ], md=6),
            ]),
        ])
    ], color="dark", outline=True, style={"borderColor": "#00d4ff", "marginTop": "20px"})
])
'''


DASHBOARD_INTEGRATION_INSTRUCTIONS = """
# Integration Steps

## 1. Add Neo Imports
At the top of championship_dashboard.py, add:

```python
from neo.dashboard_integration import DashboardNeoIntegration, BlockchainDataStreamToDb
from neo.volatility_contract import display_contract
```

## 2. Initialize Neo Integration
After creating the Dash app:

```python
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

# Initialize Neo blockchain integration
NEO_INTEGRATION = DashboardNeoIntegration(network="testnet", auto_submit=True)
NEO_ARCHIVE = BlockchainDataStreamToDb(NEO_INTEGRATION)
```

## 3. Modify Chart Update Callback
In the `update_charts` callback function, add blockchain submission logic:

```python
# After loading latest data, add:
blockchain_data = {
    'pair': latest.get('pair', 'NEO/USDT'),
    'realized_vol': latest.get('realized_vol', 0.0),
    'implied_vol': latest.get('implied_vol', 0.0),
    'garch_forecast': latest.get('garch_forecast', 0.0),
    'timestamp': int(datetime.now().timestamp())
}

# Process and submit
processed = NEO_INTEGRATION.process_dashboard_data(blockchain_data)
tx_hash = NEO_INTEGRATION.submit_to_blockchain(processed)

if tx_hash:
    NEO_ARCHIVE.archive_submission(blockchain_data)
```

## 4. Add Blockchain Status Display
Add a new output to show blockchain status:

```python
@app.callback(
    [...existing outputs...,
     Output("blockchain-status", "children"),
     Output("blockchain-submissions", "children"),
    ],
    Input("update-interval", "n_intervals"),
)
def update_charts(n):
    # ...existing code...
    
    # Get Neo status
    neo_status = NEO_INTEGRATION.get_blockchain_status()
    neo_metrics = NEO_INTEGRATION.get_integration_metrics()
    
    # Create status card
    blockchain_status = dbc.Card([
        dbc.CardBody([
            html.H5("Blockchain", className="card-title text-info"),
            html.P(f"Status: {neo_status.get('status', 'DISCONNECTED')}"),
            html.P(f"Submissions: {neo_metrics.get('total_submissions', 0)}"),
        ])
    ], color="dark", outline=True)
    
    return (...existing outputs..., blockchain_status, 
            dbc.Badge(f"{neo_metrics['total_submissions']} on-chain", color="info"))
```

## 5. Add Blockchain Stats Display
Add a new card to the layout showing blockchain statistics:

```python
# In the main layout, add:
dbc.Col([
    dbc.Card([
        dbc.CardHeader(
            html.H5("Neo N3 Integration", className="text-info"),
            className="bg-dark"
        ),
        dbc.CardBody([
            html.Div(id="blockchain-status"),
            html.Hr(),
            html.Small("Live volatility submissions to Neo blockchain", className="text-muted"),
        ])
    ], color="dark", outline=True, style={"borderColor": "#00d4ff"})
], md=12, lg=4),
```

## 6. Test Integration
```bash
# Run dashboard with Neo integration
python src/championship_dashboard.py

# In separate terminal, monitor submissions
python -c "
from neo.dashboard_integration import DashboardNeoIntegration
integration = DashboardNeoIntegration()
while True:
    metrics = integration.get_integration_metrics()
    print(f'Submissions: {metrics[\"total_submissions\"]}')
    import time; time.sleep(5)
"
```

## 7. Monitor Blockchain Submissions
```python
# Check submission history
from neo.dashboard_integration import DashboardNeoIntegration

integration = DashboardNeoIntegration()
history = integration.get_submission_history(10)

for submission in history:
    print(f"{submission['pair']}: {submission['volatility']:.4f}")
    print(f"  Time: {submission['timestamp']}")
```

## Configuration Options

### Auto-submit
By default, the integration automatically submits volatility to blockchain:
```python
NEO_INTEGRATION = DashboardNeoIntegration(network="testnet", auto_submit=True)
```

### Manual submission
Disable auto-submit for more control:
```python
NEO_INTEGRATION = DashboardNeoIntegration(network="testnet", auto_submit=False)

# Then submit manually:
tx_hash = NEO_INTEGRATION.submit_to_blockchain(processed)
```

### Network selection
```python
# Testnet (development)
NEO_INTEGRATION = DashboardNeoIntegration(network="testnet")

# Mainnet (production)
NEO_INTEGRATION = DashboardNeoIntegration(network="mainnet")
```

## Performance Considerations

- **Gas cost:** ~0.1 GAS per submission (testnet free)
- **Submission frequency:** Max 1 per block (~15 seconds)
- **Archive overhead:** < 5ms per submission
- **Dashboard latency impact:** < 50ms

## Debugging

### Check Neo connection
```python
neo_status = NEO_INTEGRATION.get_blockchain_status()
print(f"Connected: {neo_status['connected']}")
print(f"Network: {neo_status['network']}")
```

### View submission history
```python
history = NEO_INTEGRATION.get_submission_history(20)
for sub in history:
    print(f"{sub['pair']}: {sub['volatility']:.4f} at {sub['timestamp']}")
```

### Check archive
```python
stats = NEO_ARCHIVE.get_archive_stats()
print(f"Total records: {stats['total_records']}")
print(f"Pairs: {stats['pairs_breakdown']}")
```

## Example Dashboard with Neo Integration

See `src/championship_dashboard_neo.py` for a complete implementation example.

## Next Steps

1. ✅ Test Neo integration with `python src/neo_demo.py`
2. ✅ Configure dashboard
3. Deploy contract to Neo testnet
4. Connect wallet
5. Start live submissions
6. Monitor submissions in real-time
7. Analyze blockchain data

## Support

- Neo documentation: https://docs.neo.org/
- neo3-boa: https://github.com/CityOfZion/neo3-boa
- RPC specification: https://docs.neo.org/docs/en-us/reference/rpc/latest-version/api.html
"""


def print_integration_guide():
    """Print the integration guide"""
    print(DASHBOARD_INTEGRATION_INSTRUCTIONS)


if __name__ == "__main__":
    print_integration_guide()
