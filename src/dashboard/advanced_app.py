"""
AgentSpoons Advanced Dashboard
Real-time volatility monitoring with interactive charts
"""
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd
import sys
sys.path.append('..')

from utils.database import AgentSpoonsDB

# Initialize
app = dash.Dash(__name__, suppress_callback_exceptions=True)
db = AgentSpoonsDB()

# Styling
colors = {
    'background': '#0a0e27',
    'text': '#ffffff',
    'primary': '#00d4ff',
    'secondary': '#ff6b6b',
    'success': '#51cf66',
    'card': '#1a1f3a'
}

app.layout = html.Div(style={'backgroundColor': colors['background'], 'color': colors['text'], 'fontFamily': 'Arial'}, children=[
    
    # Header
    html.Div([
        html.H1('🥄 AgentSpoons Volatility Oracle', 
                style={'textAlign': 'center', 'color': colors['primary'], 'marginTop': 20}),
        html.P('Decentralized Multi-Agent Volatility System on Neo Blockchain',
               style={'textAlign': 'center', 'color': colors['text'], 'opacity': 0.7})
    ]),
    
    # Refresh interval
    dcc.Interval(id='interval-component', interval=5000, n_intervals=0),
    
    # Pair selector
    html.Div([
        html.Label('Select Trading Pair:', style={'color': colors['text']}),
        dcc.Dropdown(
            id='pair-selector',
            options=[
                {'label': 'NEO/USDT', 'value': 'NEO/USDT'},
                {'label': 'GAS/USDT', 'value': 'GAS/USDT'}
            ],
            value='NEO/USDT',
            style={'backgroundColor': colors['card'], 'color': colors['text']}
        )
    ], style={'width': '300px', 'margin': '20px auto'}),
    
    # Metrics cards row
    html.Div(id='metrics-cards', style={'display': 'flex', 'justifyContent': 'space-around', 'margin': '20px'}),
    
    # Charts row 1: Volatility time series
    html.Div([
        html.Div([
            html.H3('Realized vs Implied Volatility', style={'color': colors['primary']}),
            dcc.Graph(id='vol-timeseries')
        ], style={'width': '48%', 'display': 'inline-block', 'backgroundColor': colors['card'], 'padding': 20, 'borderRadius': 10}),
        
        html.Div([
            html.H3('GARCH Forecast', style={'color': colors['primary']}),
            dcc.Graph(id='garch-chart')
        ], style={'width': '48%', 'display': 'inline-block', 'backgroundColor': colors['card'], 'padding': 20, 'borderRadius': 10, 'marginLeft': '2%'})
    ]),
    
    # Charts row 2: Vol surface and Greeks
    html.Div([
        html.Div([
            html.H3('Volatility Surface (3D)', style={'color': colors['primary']}),
            dcc.Graph(id='vol-surface-3d')
        ], style={'width': '48%', 'display': 'inline-block', 'backgroundColor': colors['card'], 'padding': 20, 'borderRadius': 10}),
        
        html.Div([
            html.H3('ATM Greeks', style={'color': colors['primary']}),
            dcc.Graph(id='greeks-chart')
        ], style={'width': '48%', 'display': 'inline-block', 'backgroundColor': colors['card'], 'padding': 20, 'borderRadius': 10, 'marginLeft': '2%'})
    ], style={'marginTop': 20}),
    
    # Arbitrage opportunities table
    html.Div([
        html.H3('🎯 Volatility Arbitrage Opportunities', style={'color': colors['primary']}),
        html.Div(id='arbitrage-table')
    ], style={'backgroundColor': colors['card'], 'padding': 20, 'margin': '20px', 'borderRadius': 10})
])

@app.callback(
    Output('metrics-cards', 'children'),
    [Input('interval-component', 'n_intervals'),
     Input('pair-selector', 'value')]
)
def update_metrics(n, pair):
    """Update metric cards"""
    vol_data = db.get_recent_volatility(pair, limit=1)
    
    if not vol_data:
        return []
    
    latest = vol_data[0]
    
    cards = [
        create_metric_card('Realized Vol (30D)', f"{latest['garman_klass_vol']:.2%}", colors['primary']),
        create_metric_card('GARCH Forecast', f"{latest['garch_forecast']:.2%}", colors['success']),
        create_metric_card('Vol Regime', latest['vol_regime'].upper(), colors['secondary']),
        create_metric_card('Last Update', datetime.fromisoformat(latest['timestamp']).strftime('%H:%M:%S'), colors['text'])
    ]
    
    return cards

def create_metric_card(title, value, color):
    """Create a metric card component"""
    return html.Div([
        html.H4(title, style={'color': colors['text'], 'opacity': 0.7, 'marginBottom': 10}),
        html.H2(value, style={'color': color, 'margin': 0})
    ], style={
        'backgroundColor': colors['card'],
        'padding': 20,
        'borderRadius': 10,
        'textAlign': 'center',
        'minWidth': '200px'
    })

@app.callback(
    Output('vol-timeseries', 'figure'),
    [Input('interval-component', 'n_intervals'),
     Input('pair-selector', 'value')]
)
def update_vol_timeseries(n, pair):
    """Update volatility time series chart"""
    data = db.get_volatility_timeseries(pair, days=7)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=data['timestamps'],
        y=data['realized_vol'],
        mode='lines',
        name='Realized Vol',
        line=dict(color=colors['primary'], width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=data['timestamps'],
        y=data['garch_forecast'],
        mode='lines',
        name='GARCH Forecast',
        line=dict(color=colors['success'], width=2, dash='dash')
    ))
    
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor=colors['card'],
        plot_bgcolor=colors['card'],
        font=dict(color=colors['text']),
        xaxis_title='Time',
        yaxis_title='Volatility',
        yaxis_tickformat='.0%',
        hovermode='x unified'
    )
    
    return fig

@app.callback(
    Output('garch-chart', 'figure'),
    [Input('interval-component', 'n_intervals'),
     Input('pair-selector', 'value')]
)
def update_garch_chart(n, pair):
    """Update GARCH parameters chart"""
    vol_data = db.get_recent_volatility(pair, limit=50)
    
    if not vol_data:
        return go.Figure()
    
    df = pd.DataFrame(vol_data)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df['timestamp'].tail(10),
        y=df['garch_alpha'].tail(10),
        name='Alpha (ARCH)',
        marker_color=colors['primary']
    ))
    
    fig.add_trace(go.Bar(
        x=df['timestamp'].tail(10),
        y=df['garch_beta'].tail(10),
        name='Beta (GARCH)',
        marker_color=colors['secondary']
    ))
    
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor=colors['card'],
        plot_bgcolor=colors['card'],
        font=dict(color=colors['text']),
        barmode='group',
        xaxis_title='Time',
        yaxis_title='Coefficient Value'
    )
    
    return fig

@app.callback(
    Output('vol-surface-3d', 'figure'),
    [Input('interval-component', 'n_intervals'),
     Input('pair-selector', 'value')]
)
def update_vol_surface(n, pair):
    """Create 3D volatility surface (mock for demo)"""
    # Generate mock surface data
    strikes = list(range(10, 21))
    maturities = [0.08, 0.25, 0.5, 1.0]
    
    import numpy as np
    Z = [[0.4 + 0.1 * abs(s-15)/5 + 0.05*t for s in strikes] for t in maturities]
    
    fig = go.Figure(data=[go.Surface(
        x=strikes,
        y=maturities,
        z=Z,
        colorscale='Viridis'
    )])
    
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor=colors['card'],
        scene=dict(
            xaxis_title='Strike',
            yaxis_title='Maturity (years)',
            zaxis_title='Implied Vol',
            bgcolor=colors['card']
        ),
        font=dict(color=colors['text'])
    )
    
    return fig

@app.callback(
    Output('greeks-chart', 'figure'),
    [Input('interval-component', 'n_intervals'),
     Input('pair-selector', 'value')]
)
def update_greeks(n, pair):
    """Update Greeks chart (mock data)"""
    greeks = {
        'Delta': 0.52,
        'Gamma': 0.08,
        'Vega': 0.15,
        'Theta': -0.03
    }
    
    fig = go.Figure(data=[
        go.Bar(
            x=list(greeks.keys()),
            y=list(greeks.values()),
            marker_color=[colors['primary'], colors['success'], colors['secondary'], '#ffd43b']
        )
    ])
    
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor=colors['card'],
        plot_bgcolor=colors['card'],
        font=dict(color=colors['text']),
        yaxis_title='Value'
    )
    
    return fig

@app.callback(
    Output('arbitrage-table', 'children'),
    [Input('interval-component', 'n_intervals')]
)
def update_arbitrage_table(n):
    """Update arbitrage opportunities table"""
    opportunities = db.get_arbitrage_opportunities(hours=24)
    
    if not opportunities:
        return html.P('No arbitrage opportunities detected', 
                     style={'color': colors['text'], 'opacity': 0.5, 'textAlign': 'center'})
    
    df = pd.DataFrame(opportunities)
    df = df.sort_values('confidence', ascending=False).head(10)
    
    return dash_table.DataTable(
        data=df[['pair', 'strategy', 'vol_spread_pct', 'confidence', 'recommended_action']].to_dict('records'),
        columns=[
            {'name': 'Pair', 'id': 'pair'},
            {'name': 'Strategy', 'id': 'strategy'},
            {'name': 'Spread %', 'id': 'vol_spread_pct', 'type': 'numeric', 'format': {'specifier': '.2%'}},
            {'name': 'Confidence', 'id': 'confidence', 'type': 'numeric', 'format': {'specifier': '.1f'}},
            {'name': 'Action', 'id': 'recommended_action'}
        ],
        style_table={'overflowX': 'auto'},
        style_cell={
            'backgroundColor': colors['background'],
            'color': colors['text'],
            'border': '1px solid ' + colors['card']
        },
        style_header={
            'backgroundColor': colors['card'],
            'fontWeight': 'bold'
        },
        style_data_conditional=[
            {
                'if': {'column_id': 'confidence', 'filter_query': '{confidence} > 70'},
                'backgroundColor': colors['success'],
                'color': 'white'
            }
        ]
    )

if __name__ == '__main__':
    print("🚀 Starting AgentSpoons Dashboard on http://localhost:8050")
    app.run(debug=True, host='0.0.0.0', port=8050)
