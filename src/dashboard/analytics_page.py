"""
Advanced Analytics Dashboard Page
"""
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.figure_factory as ff
import numpy as np
import pandas as pd
import json

def create_analytics_layout():
    """Create advanced analytics page"""
    return dbc.Container(fluid=True, children=[
        
        dbc.Row([
            dbc.Col([
                html.H2('📊 Advanced Analytics', style={'color': '#00d4ff', 'marginTop': '20px'})
            ])
        ]),
        
        # Metrics Row
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4('Correlation Matrix', className='text-center'),
                        dcc.Graph(id='correlation-matrix')
                    ])
                ], style={'backgroundColor': '#1a1f3a', 'border': 'none'})
            ], width=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4('Distribution Analysis', className='text-center'),
                        dcc.Graph(id='distribution-plot')
                    ])
                ], style={'backgroundColor': '#1a1f3a', 'border': 'none'})
            ], width=6),
        ], className='mb-4'),
        
        # QQ Plot and Autocorrelation
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4('Returns Q-Q Plot', className='text-center'),
                        dcc.Graph(id='qq-plot')
                    ])
                ], style={'backgroundColor': '#1a1f3a', 'border': 'none'})
            ], width=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4('Volatility Autocorrelation', className='text-center'),
                        dcc.Graph(id='acf-plot')
                    ])
                ], style={'backgroundColor': '#1a1f3a', 'border': 'none'})
            ], width=6),
        ], className='mb-4'),
        
        # Risk Metrics
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4('Value at Risk (VaR)', className='text-center'),
                        dcc.Graph(id='var-plot')
                    ])
                ], style={'backgroundColor': '#1a1f3a', 'border': 'none'})
            ], width=12)
        ]),
        
        dcc.Interval(id='analytics-interval', interval=10000)
    ])

def create_correlation_matrix(data):
    """Create correlation heatmap"""
    df = pd.DataFrame(data)
    
    metrics = ['price', 'realized_vol', 'implied_vol', 'garch_forecast', 'spread']
    corr_data = df[metrics].corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=corr_data.values,
        x=metrics,
        y=metrics,
        colorscale='RdBu',
        zmid=0,
        text=corr_data.values,
        texttemplate='%{text:.2f}',
        textfont={"size": 12},
        colorbar=dict(title="Correlation")
    ))
    
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='#1a1f3a',
        height=400
    )
    
    return fig

def create_distribution_plot(data):
    """Create distribution histogram with normal overlay"""
    df = pd.DataFrame(data)
    
    returns = df['price'].pct_change().dropna() * 100
    
    fig = go.Figure()
    
    # Histogram
    fig.add_trace(go.Histogram(
        x=returns,
        nbinsx=50,
        name='Returns',
        marker_color='#00d4ff',
        opacity=0.7
    ))
    
    # Normal distribution overlay
    mu = returns.mean()
    sigma = returns.std()
    x_norm = np.linspace(returns.min(), returns.max(), 100)
    y_norm = ((1 / (np.sqrt(2 * np.pi) * sigma)) * 
              np.exp(-0.5 * ((x_norm - mu) / sigma) ** 2))
    
    # Scale to match histogram
    y_norm = y_norm * len(returns) * (returns.max() - returns.min()) / 50
    
    fig.add_trace(go.Scatter(
        x=x_norm,
        y=y_norm,
        mode='lines',
        name='Normal',
        line=dict(color='#ff6b6b', width=2)
    ))
    
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='#1a1f3a',
        xaxis_title='Returns %',
        yaxis_title='Frequency',
        height=400,
        showlegend=True
    )
    
    return fig

def create_qq_plot(data):
    """Q-Q plot to check normality"""
    df = pd.DataFrame(data)
    returns = df['price'].pct_change().dropna()
    
    from scipy import stats
    
    # Theoretical quantiles
    (osm, osr), (slope, intercept, r) = stats.probplot(returns, dist="norm")
    
    fig = go.Figure()
    
    # Scatter plot
    fig.add_trace(go.Scatter(
        x=osm,
        y=osr,
        mode='markers',
        name='Sample Quantiles',
        marker=dict(color='#00d4ff', size=6)
    ))
    
    # Theoretical line
    fig.add_trace(go.Scatter(
        x=osm,
        y=slope * osm + intercept,
        mode='lines',
        name='Theoretical',
        line=dict(color='#ff6b6b', width=2)
    ))
    
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='#1a1f3a',
        xaxis_title='Theoretical Quantiles',
        yaxis_title='Sample Quantiles',
        height=400
    )
    
    return fig

def create_acf_plot(data):
    """Autocorrelation function plot"""
    df = pd.DataFrame(data)
    vols = df['realized_vol'].values
    
    # Calculate ACF
    from statsmodels.tsa.stattools import acf
    
    acf_vals = acf(vols, nlags=20)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=list(range(len(acf_vals))),
        y=acf_vals,
        marker_color='#00d4ff'
    ))
    
    # Confidence intervals
    conf = 1.96 / np.sqrt(len(vols))
    fig.add_hline(y=conf, line_dash="dash", line_color='#ff6b6b')
    fig.add_hline(y=-conf, line_dash="dash", line_color='#ff6b6b')
    
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='#1a1f3a',
        xaxis_title='Lag',
        yaxis_title='Autocorrelation',
        height=400
    )
    
    return fig

def create_var_plot(data):
    """Value at Risk visualization"""
    df = pd.DataFrame(data)
    returns = df['price'].pct_change().dropna() * 100
    
    # Calculate VaR at different confidence levels
    var_95 = np.percentile(returns, 5)
    var_99 = np.percentile(returns, 1)
    
    fig = go.Figure()
    
    # Histogram
    fig.add_trace(go.Histogram(
        x=returns,
        nbinsx=50,
        name='Returns',
        marker_color='#00d4ff',
        opacity=0.7
    ))
    
    # VaR lines
    fig.add_vline(x=var_95, line_dash="dash", line_color='#ffd43b',
                  annotation_text=f'VaR 95%: {var_95:.2f}%')
    fig.add_vline(x=var_99, line_dash="dash", line_color='#ff6b6b',
                  annotation_text=f'VaR 99%: {var_99:.2f}%')
    
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='#1a1f3a',
        xaxis_title='Returns %',
        yaxis_title='Frequency',
        height=400
    )
    
    return fig
