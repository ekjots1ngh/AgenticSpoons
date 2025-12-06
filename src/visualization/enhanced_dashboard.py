"""
Enhanced Dashboard with 3D Visualizations
Extends championship_dashboard.py with advanced volatility surface plots
"""

import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import json
import numpy as np
from src.visualization import VolatilitySurface3D, VolatilitySmile, TermStructure

# Initialize 3D visualization
surf_generator = VolatilitySurface3D()

def create_enhanced_dashboard():
    """Create dashboard with 3D volatility surfaces"""
    
    app = dash.Dash(__name__)
    
    # Load sample data
    try:
        with open('data/results.json', 'r') as f:
            data = json.load(f)
    except:
        data = []
    
    app.layout = html.Div([
        html.Div([
            html.Div([
                html.H1("AgentSpoons - Enhanced Analytics", 
                       style={'color': '#00D9FF', 'marginBottom': '10px'}),
                html.P("Real-Time Volatility Analysis with 3D Surface", 
                      style={'color': '#888', 'marginTop': '0px'})
            ], style={'padding': '20px', 'backgroundColor': '#0a0e27', 'borderRadius': '8px'}),
        ], style={'marginBottom': '20px'}),
        
        # Tabs for different views
        dcc.Tabs(id='analysis-tabs', value='surface', children=[
            dcc.Tab(label='3D Volatility Surface', value='surface', children=[
                html.Div([
                    dcc.Loading(
                        id='surface-loading',
                        type='default',
                        children=[
                            dcc.Graph(id='vol-surface-3d')
                        ]
                    )
                ], style={'padding': '20px', 'backgroundColor': '#1a1f3a', 'borderRadius': '8px'})
            ]),
            
            dcc.Tab(label='Volatility Smile', value='smile', children=[
                html.Div([
                    html.Div([
                        html.Label('Select Maturity (days):'),
                        dcc.Slider(
                            id='smile-maturity-slider',
                            min=7,
                            max=365,
                            step=7,
                            value=30,
                            marks={i: f'{i}d' for i in range(0, 366, 60)},
                            tooltip={"placement": "bottom", "always_visible": True}
                        )
                    ], style={'marginBottom': '20px'}),
                    
                    dcc.Graph(id='vol-smile-graph')
                ], style={'padding': '20px', 'backgroundColor': '#1a1f3a', 'borderRadius': '8px'})
            ]),
            
            dcc.Tab(label='Term Structure', value='term', children=[
                html.Div([
                    html.Div([
                        html.Label('Select Strike Price:'),
                        dcc.Slider(
                            id='term-strike-slider',
                            min=80,
                            max=120,
                            step=1,
                            value=100,
                            marks={i: f'{i}' for i in range(80, 121, 10)},
                            tooltip={"placement": "bottom", "always_visible": True}
                        )
                    ], style={'marginBottom': '20px'}),
                    
                    dcc.Graph(id='term-structure-graph')
                ], style={'padding': '20px', 'backgroundColor': '#1a1f3a', 'borderRadius': '8px'})
            ]),
            
            dcc.Tab(label='Statistics', value='stats', children=[
                html.Div([
                    html.Div(id='stats-summary',
                            style={'padding': '20px', 'backgroundColor': '#1a1f3a', 'borderRadius': '8px'})
                ], style={'padding': '20px'})
            ])
        ]),
        
        # Auto-refresh every 5 seconds
        dcc.Interval(id='refresh-interval', interval=5000, n_intervals=0),
        
        html.Div(id='data-store', style={'display': 'none'})
    ], style={
        'backgroundColor': '#0a0e27',
        'color': '#00D9FF',
        'fontFamily': 'Arial, sans-serif',
        'padding': '20px',
        'minHeight': '100vh'
    })
    
    # Callbacks for 3D surface
    @app.callback(
        Output('vol-surface-3d', 'figure'),
        Input('refresh-interval', 'n_intervals')
    )
    def update_3d_surface(n):
        """Update 3D volatility surface"""
        fig = surf_generator.generate_sample_surface()
        return fig if fig else go.Figure()
    
    # Callbacks for volatility smile
    @app.callback(
        Output('vol-smile-graph', 'figure'),
        Input('smile-maturity-slider', 'value')
    )
    def update_smile(maturity_days):
        """Update volatility smile for selected maturity"""
        maturity_years = maturity_days / 365
        
        # Generate smile
        spot = 100.0
        strikes = np.linspace(spot * 0.8, spot * 1.2, 30)
        
        # ATM vol
        atm_vol = 0.40
        
        # Add smile effect
        ivs = atm_vol + 0.08 * ((strikes - spot) / spot) ** 2
        ivs = np.clip(ivs, 0.1, 2.0)
        
        return VolatilitySmile.create_smile(strikes, ivs, maturity_years)
    
    # Callbacks for term structure
    @app.callback(
        Output('term-structure-graph', 'figure'),
        Input('term-strike-slider', 'value')
    )
    def update_term_structure(strike):
        """Update term structure for selected strike"""
        
        # Generate term structure
        maturities = np.linspace(7/365, 2.0, 30)
        
        # Base vol at strike
        spot = 100.0
        moneyness = strike / spot
        atm_vol = 0.40
        smile = 0.08 * ((moneyness - 1.0) ** 2)
        base_vol = atm_vol + smile
        
        # Add term structure
        vols = base_vol + 0.1 * np.sqrt(maturities)
        vols = np.clip(vols, 0.1, 2.0)
        
        return TermStructure.create_term_structure(maturities, vols)
    
    # Callbacks for statistics
    @app.callback(
        Output('stats-summary', 'children'),
        Input('refresh-interval', 'n_intervals')
    )
    def update_stats(n):
        """Update statistics summary"""
        
        if not data:
            return html.P("No data available")
        
        # Calculate statistics
        realized_vols = [d.get('realized_vol', 0) for d in data]
        implied_vols = [d.get('implied_vol', 0) for d in data]
        
        stats = [
            html.Div([
                html.H3("Volatility Statistics", style={'color': '#00D9FF'}),
                html.Table([
                    html.Tr([
                        html.Td("Metric", style={'fontWeight': 'bold', 'padding': '10px', 'borderBottom': '1px solid #444'}),
                        html.Td("Realized Vol", style={'fontWeight': 'bold', 'padding': '10px', 'borderBottom': '1px solid #444', 'textAlign': 'center'}),
                        html.Td("Implied Vol", style={'fontWeight': 'bold', 'padding': '10px', 'borderBottom': '1px solid #444', 'textAlign': 'center'})
                    ]),
                    html.Tr([
                        html.Td("Mean", style={'padding': '10px', 'borderBottom': '1px solid #333'}),
                        html.Td(f"{np.mean(realized_vols):.4f}", style={'padding': '10px', 'borderBottom': '1px solid #333', 'textAlign': 'center'}),
                        html.Td(f"{np.mean(implied_vols):.4f}", style={'padding': '10px', 'borderBottom': '1px solid #333', 'textAlign': 'center'})
                    ]),
                    html.Tr([
                        html.Td("Std Dev", style={'padding': '10px', 'borderBottom': '1px solid #333'}),
                        html.Td(f"{np.std(realized_vols):.4f}", style={'padding': '10px', 'borderBottom': '1px solid #333', 'textAlign': 'center'}),
                        html.Td(f"{np.std(implied_vols):.4f}", style={'padding': '10px', 'borderBottom': '1px solid #333', 'textAlign': 'center'})
                    ]),
                    html.Tr([
                        html.Td("Min", style={'padding': '10px', 'borderBottom': '1px solid #333'}),
                        html.Td(f"{np.min(realized_vols):.4f}", style={'padding': '10px', 'borderBottom': '1px solid #333', 'textAlign': 'center'}),
                        html.Td(f"{np.min(implied_vols):.4f}", style={'padding': '10px', 'borderBottom': '1px solid #333', 'textAlign': 'center'})
                    ]),
                    html.Tr([
                        html.Td("Max", style={'padding': '10px', 'borderBottom': '1px solid #333'}),
                        html.Td(f"{np.max(realized_vols):.4f}", style={'padding': '10px', 'borderBottom': '1px solid #333', 'textAlign': 'center'}),
                        html.Td(f"{np.max(implied_vols):.4f}", style={'padding': '10px', 'borderBottom': '1px solid #333', 'textAlign': 'center'})
                    ])
                ], style={'width': '100%', 'borderCollapse': 'collapse'})
            ], style={'marginBottom': '30px'})
        ]
        
        return stats
    
    return app

if __name__ == "__main__":
    app = create_enhanced_dashboard()
    print("\n" + "="*70)
    print(">> Enhanced Dashboard with 3D Visualizations")
    print("="*70)
    print("Access at: http://localhost:8051")
    print("="*70 + "\n")
    app.run_server(debug=True, port=8051, host='0.0.0.0')
