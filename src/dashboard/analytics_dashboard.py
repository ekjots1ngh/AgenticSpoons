"""
Analytics Dashboard Application
Advanced statistical analysis with Dash
"""
import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import numpy as np
import pandas as pd
import json
from pathlib import Path
from loguru import logger

from src.dashboard.analytics_page import (
    create_analytics_layout,
    create_correlation_matrix,
    create_distribution_plot,
    create_qq_plot,
    create_acf_plot,
    create_var_plot
)

# Initialize app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

# Custom styles
COLORS = {
    'background': '#0a0e27',
    'surface': '#1a1f3a',
    'primary': '#00d4ff',
    'accent': '#ff006e'
}

def load_data():
    """Load market data"""
    try:
        with open('data/results.json', 'r') as f:
            return json.load(f)
    except:
        return []

# App layout
app.layout = dbc.Container(fluid=True, children=[
    dcc.Store(id='data-store'),
    
    # Header
    dbc.Row([
        dbc.Col([
            html.Div(
                html.H1('📊 AgenticSpoons Analytics Dashboard', 
                        style={'color': COLORS['primary'], 'marginTop': '30px', 'marginBottom': '10px'}),
                style={'textAlign': 'center'}
            ),
            html.Hr(style={'borderColor': COLORS['primary']})
        ])
    ], style={'backgroundColor': COLORS['background'], 'padding': '20px'}),
    
    # Navigation tabs
    dbc.Row([
        dbc.Col([
            dcc.Tabs(id='main-tabs', value='overview', children=[
                dcc.Tab(label='📈 Overview', value='overview', children=[
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.H4('Data Summary', className='text-center'),
                                    html.Div(id='summary-stats', children=[
                                        html.P('Loading...', className='text-muted')
                                    ])
                                ])
                            ], style={'backgroundColor': COLORS['surface'], 'border': 'none'}, className='mb-4')
                        ], width=12)
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.H4('Price Series', className='text-center'),
                                    dcc.Graph(id='price-series')
                                ])
                            ], style={'backgroundColor': COLORS['surface'], 'border': 'none'})
                        ], width=6),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.H4('Volatility Series', className='text-center'),
                                    dcc.Graph(id='volatility-series')
                                ])
                            ], style={'backgroundColor': COLORS['surface'], 'border': 'none'})
                        ], width=6)
                    ])
                ]),
                dcc.Tab(label='📊 Advanced Analytics', value='analytics', children=[
                    html.Div(id='analytics-container')
                ]),
                dcc.Tab(label='⚙️ Controls', value='settings', children=[
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.H4('Dashboard Settings'),
                                    dbc.Row([
                                        dbc.Col([
                                            dbc.Label('Refresh Interval (seconds)', html_for='refresh-slider'),
                                            dcc.Slider(
                                                id='refresh-slider',
                                                min=5,
                                                max=60,
                                                step=5,
                                                value=10,
                                                marks={i: str(i) for i in range(5, 65, 10)},
                                                tooltip={"placement": "bottom", "always_visible": True}
                                            )
                                        ])
                                    ], className='mt-3 mb-3'),
                                    dbc.Row([
                                        dbc.Col([
                                            dbc.Label('Correlation Pairs', html_for='correlation-filter'),
                                            dcc.Dropdown(
                                                id='correlation-filter',
                                                options=[
                                                    {'label': 'All', 'value': 'all'},
                                                    {'label': 'NEO/USDT', 'value': 'NEO/USDT'},
                                                    {'label': 'GAS/USDT', 'value': 'GAS/USDT'}
                                                ],
                                                value='all',
                                                style={'color': 'black'}
                                            )
                                        ])
                                    ], className='mt-3')
                                ])
                            ], style={'backgroundColor': COLORS['surface'], 'border': 'none'})
                        ], width=6),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.H4('About'),
                                    html.P('AgenticSpoons Advanced Analytics Dashboard'),
                                    html.P('December 2025', className='text-muted')
                                ])
                            ], style={'backgroundColor': COLORS['surface'], 'border': 'none'})
                        ], width=6)
                    ], className='mt-4')
                ])
            ], style={'backgroundColor': COLORS['surface']})
        ])
    ], className='mt-4'),
    
    # Auto-refresh interval
    dcc.Interval(id='dashboard-interval', interval=10000)
    
], style={'backgroundColor': COLORS['background'], 'minHeight': '100vh', 'padding': '20px'})

@app.callback(
    Output('data-store', 'data'),
    Input('dashboard-interval', 'n_intervals')
)
def update_data(n):
    """Update stored data"""
    data = load_data()
    return data

@app.callback(
    Output('summary-stats', 'children'),
    Input('data-store', 'data')
)
def update_summary(data):
    """Update summary statistics"""
    if not data:
        return html.P('No data available', className='text-muted')
    
    df = pd.DataFrame(data)
    
    return dbc.Row([
        dbc.Col([
            html.Div([
                html.H6('Total Records', className='text-muted'),
                html.H4(f"{len(df):,}", style={'color': COLORS['primary']})
            ], className='text-center mb-3')
        ], width=3),
        dbc.Col([
            html.Div([
                html.H6('Avg Price', className='text-muted'),
                html.H4(f"${df['price'].mean():.2f}", style={'color': COLORS['primary']})
            ], className='text-center mb-3')
        ], width=3),
        dbc.Col([
            html.Div([
                html.H6('Price Range', className='text-muted'),
                html.H4(f"${df['price'].max() - df['price'].min():.2f}", style={'color': COLORS['primary']})
            ], className='text-center mb-3')
        ], width=3),
        dbc.Col([
            html.Div([
                html.H6('Volatility', className='text-muted'),
                html.H4(f"{df['price'].std():.4f}", style={'color': COLORS['primary']})
            ], className='text-center mb-3')
        ], width=3)
    ])

@app.callback(
    Output('price-series', 'figure'),
    Input('data-store', 'data')
)
def update_price_series(data):
    """Update price series chart"""
    if not data:
        return go.Figure()
    
    df = pd.DataFrame(data)
    
    # Group by pair
    neo_data = df[df['pair'] == 'NEO/USDT']
    gas_data = df[df['pair'] == 'GAS/USDT']
    
    fig = go.Figure()
    
    if not neo_data.empty:
        fig.add_trace(go.Scatter(
            y=neo_data['price'],
            name='NEO/USDT',
            line=dict(color=COLORS['primary'], width=2)
        ))
    
    if not gas_data.empty:
        fig.add_trace(go.Scatter(
            y=gas_data['price'],
            name='GAS/USDT',
            line=dict(color=COLORS['accent'], width=2)
        ))
    
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor=COLORS['surface'],
        xaxis_title='Time Period',
        yaxis_title='Price (USDT)',
        height=400,
        hovermode='x unified'
    )
    
    return fig

@app.callback(
    Output('volatility-series', 'figure'),
    Input('data-store', 'data')
)
def update_volatility_series(data):
    """Update volatility series chart"""
    if not data:
        return go.Figure()
    
    df = pd.DataFrame(data)
    
    # Calculate rolling volatility
    df['returns'] = df['price'].pct_change()
    df['rolling_vol'] = df['returns'].rolling(5).std() * 100
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        y=df['rolling_vol'],
        fill='tozeroy',
        name='Volatility',
        line=dict(color=COLORS['primary']),
        fillcolor='rgba(0, 212, 255, 0.2)'
    ))
    
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor=COLORS['surface'],
        xaxis_title='Time Period',
        yaxis_title='Volatility %',
        height=400,
        hovermode='x unified'
    )
    
    return fig

@app.callback(
    Output('analytics-container', 'children'),
    Input('data-store', 'data')
)
def update_analytics(data):
    """Update analytics page"""
    if not data:
        return html.P('No data available', className='text-muted text-center mt-4')
    
    return create_analytics_layout()

@app.callback(
    Output('correlation-matrix', 'figure'),
    Input('data-store', 'data'),
    Input('correlation-filter', 'value')
)
def update_correlation(data, filter_val):
    """Update correlation matrix"""
    if not data:
        return go.Figure()
    
    df = pd.DataFrame(data)
    
    if filter_val != 'all':
        df = df[df['pair'] == filter_val]
    
    return create_correlation_matrix(df)

@app.callback(
    Output('distribution-plot', 'figure'),
    Input('data-store', 'data')
)
def update_distribution(data):
    """Update distribution plot"""
    if not data:
        return go.Figure()
    
    return create_distribution_plot(data)

@app.callback(
    Output('qq-plot', 'figure'),
    Input('data-store', 'data')
)
def update_qq(data):
    """Update Q-Q plot"""
    if not data:
        return go.Figure()
    
    try:
        return create_qq_plot(data)
    except:
        return go.Figure().add_annotation(text="Unable to generate Q-Q plot")

@app.callback(
    Output('acf-plot', 'figure'),
    Input('data-store', 'data')
)
def update_acf(data):
    """Update ACF plot"""
    if not data:
        return go.Figure()
    
    try:
        return create_acf_plot(data)
    except:
        return go.Figure().add_annotation(text="Unable to generate ACF plot")

@app.callback(
    Output('var-plot', 'figure'),
    Input('data-store', 'data')
)
def update_var(data):
    """Update VaR plot"""
    if not data:
        return go.Figure()
    
    try:
        return create_var_plot(data)
    except:
        return go.Figure().add_annotation(text="Unable to generate VaR plot")

if __name__ == '__main__':
    logger.info("Starting Analytics Dashboard on port 8052...")
    app.run_server(debug=False, host='0.0.0.0', port=8052)
