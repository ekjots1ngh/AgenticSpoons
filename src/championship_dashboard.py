"""
AgentSpoons - Championship Dashboard
This will WIN the hackathon
"""
import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px
import json
import os
from datetime import datetime
import numpy as np
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from dashboard.themes import get_colors, get_plotly_template, get_chart_colors

# Initialize with dark theme
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.CYBORG,
        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css'
    ],
    meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}]
)

# Default to dark theme colors
COLORS = get_colors('dark')

# ==================== LAYOUT ====================
app.layout = dbc.Container(fluid=True, style={'backgroundColor': COLORS['background'], 'minHeight': '100vh', 'padding': '0'}, children=[
    
    # ===== HEADER =====
    dbc.Row([
        dbc.Col([
            html.Div([
                # Logo/Title Section
                html.Div([
                    html.H1([
                        html.Span('[SPOON] ', style={'fontSize': '48px'}),
                        html.Span('AgentSpoons', style={
                            'background': f'linear-gradient(135deg, {COLORS["primary"]}, {COLORS["success"]})',
                            'WebkitBackgroundClip': 'text',
                            'WebkitTextFillColor': 'transparent',
                            'fontWeight': '900',
                            'letterSpacing': '-1px'
                        })
                    ], style={'margin': '0'}),
                    html.P('Decentralized Volatility Oracle on Neo', style={
                        'color': COLORS['muted'],
                        'fontSize': '18px',
                        'margin': '5px 0 0 0',
                        'fontWeight': '300'
                    })
                ], style={'display': 'inline-block', 'verticalAlign': 'middle'}),
                
                # Theme Toggle Button
                html.Div([
                    dbc.Button(
                        id='theme-toggle',
                        children=[
                            html.I(className='fas fa-moon', id='theme-icon', style={'marginRight': '8px'}),
                            html.Span('Theme')
                        ],
                        color='secondary',
                        outline=True,
                        size='sm',
                        style={
                            'borderRadius': '20px',
                            'padding': '6px 16px',
                            'marginRight': '15px'
                        }
                    )
                ], style={'float': 'right', 'marginTop': '20px', 'display': 'inline-block'}),

                # Live Status Badge
                html.Div([
                    html.Div(id='live-status', children=[
                        html.Span('● ', style={'color': COLORS['success'], 'fontSize': '24px'}),
                        html.Span('LIVE', style={'fontWeight': 'bold', 'fontSize': '16px'})
                    ], style={
                        'backgroundColor': 'rgba(81, 207, 102, 0.1)',
                        'border': f'2px solid {COLORS["success"]}',
                        'borderRadius': '30px',
                        'padding': '8px 20px',
                        'display': 'inline-block'
                    })
                ], style={'float': 'right', 'marginTop': '20px'})
            ], style={'padding': '30px 30px 20px 30px'})
        ], width=12)
    ], style={'borderBottom': f'1px solid {COLORS["card"]}'}),
    
    # ===== STATS CARDS ROW =====
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.P('PRICE', style={'fontSize': '16px', 'margin': '0'}),
                        html.H2(id='neo-price', children='$--', style={
                            'color': COLORS['primary'],
                            'fontSize': '36px',
                            'fontWeight': 'bold',
                            'margin': '10px 0 5px 0'
                        }),
                        html.P('NEO/USDT', style={'color': COLORS['muted'], 'margin': '0', 'fontSize': '14px'})
                    ], style={'textAlign': 'center'})
                ])
            ], style={'backgroundColor': COLORS['card'], 'border': 'none', 'borderRadius': '15px', 'height': '100%'})
        ], width=12, lg=3, className='mb-3'),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.P('REALIZED VOL', style={'fontSize': '16px', 'margin': '0'}),
                        html.H2(id='realized-vol', children='--%', style={
                            'color': COLORS['success'],
                            'fontSize': '36px',
                            'fontWeight': 'bold',
                            'margin': '10px 0 5px 0'
                        }),
                        html.P('30-Day', style={'color': COLORS['muted'], 'margin': '0', 'fontSize': '14px'})
                    ], style={'textAlign': 'center'})
                ])
            ], style={'backgroundColor': COLORS['card'], 'border': 'none', 'borderRadius': '15px', 'height': '100%'})
        ], width=12, lg=3, className='mb-3'),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.P('IMPLIED VOL', style={'fontSize': '16px', 'margin': '0'}),
                        html.H2(id='implied-vol', children='--%', style={
                            'color': COLORS['danger'],
                            'fontSize': '36px',
                            'fontWeight': 'bold',
                            'margin': '10px 0 5px 0'
                        }),
                        html.P('ATM', style={'color': COLORS['muted'], 'margin': '0', 'fontSize': '14px'})
                    ], style={'textAlign': 'center'})
                ])
            ], style={'backgroundColor': COLORS['card'], 'border': 'none', 'borderRadius': '15px', 'height': '100%'})
        ], width=12, lg=3, className='mb-3'),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.P('SPREAD', style={'fontSize': '16px', 'margin': '0'}),
                        html.H2(id='spread-value', children='--%', style={
                            'color': COLORS['warning'],
                            'fontSize': '36px',
                            'fontWeight': 'bold',
                            'margin': '10px 0 5px 0'
                        }),
                        html.P('Arbitrage', style={'color': COLORS['muted'], 'margin': '0', 'fontSize': '14px'})
                    ], style={'textAlign': 'center'})
                ])
            ], style={'backgroundColor': COLORS['card'], 'border': 'none', 'borderRadius': '15px', 'height': '100%'})
        ], width=12, lg=3, className='mb-3'),
    ], style={'padding': '30px'}),
    
    # ===== MAIN CHARTS ROW =====
    dbc.Row([
        # Left Column - Volatility Comparison
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H4('VOLATILITY ANALYSIS', style={'margin': '0', 'color': COLORS['text']})
                ], style={'backgroundColor': COLORS['card'], 'border': 'none'}),
                dbc.CardBody([
                    dcc.Graph(id='vol-chart', config={'displayModeBar': False})
                ])
            ], style={'backgroundColor': COLORS['card'], 'border': 'none', 'borderRadius': '15px', 'marginBottom': '20px'})
        ], width=12, lg=8),
        
        # Right Column - Stats
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H4('LIVE METRICS', style={'margin': '0', 'color': COLORS['text']})
                ], style={'backgroundColor': COLORS['card'], 'border': 'none'}),
                dbc.CardBody([
                    html.Div(id='stats-panel')
                ])
            ], style={'backgroundColor': COLORS['card'], 'border': 'none', 'borderRadius': '15px', 'height': '100%'})
        ], width=12, lg=4),
    ], style={'padding': '0 30px'}),
    
    # ===== SECOND CHARTS ROW =====
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H4('ARBITRAGE SIGNAL', style={'margin': '0', 'color': COLORS['text']})
                ], style={'backgroundColor': COLORS['card'], 'border': 'none'}),
                dbc.CardBody([
                    dcc.Graph(id='spread-chart', config={'displayModeBar': False})
                ])
            ], style={'backgroundColor': COLORS['card'], 'border': 'none', 'borderRadius': '15px', 'marginBottom': '20px'})
        ], width=12, lg=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H4('GARCH FORECAST', style={'margin': '0', 'color': COLORS['text']})
                ], style={'backgroundColor': COLORS['card'], 'border': 'none'}),
                dbc.CardBody([
                    dcc.Graph(id='garch-chart', config={'displayModeBar': False})
                ])
            ], style={'backgroundColor': COLORS['card'], 'border': 'none', 'borderRadius': '15px', 'marginBottom': '20px'})
        ], width=12, lg=6),
    ], style={'padding': '0 30px'}),
    
    # ===== FOOTER =====
    dbc.Row([
        dbc.Col([
            html.Div([
                html.P([
                    'Powered by Neo N3 Blockchain | ',
                    html.Span('5 Autonomous Agents', style={'color': COLORS['success']}),
                    ' | Updates Every 2s'
                ], style={'textAlign': 'center', 'color': COLORS['muted'], 'margin': '20px 0'})
            ])
        ])
    ]),
    
    # Auto-refresh
    dcc.Interval(id='interval', interval=2000),  # 2 seconds

    # Theme store (persists theme selection in browser localStorage)
    dcc.Store(id='theme-store', storage_type='local', data='dark')
])

# ==================== CALLBACKS ====================

@app.callback(
    [Output('theme-store', 'data'),
     Output('theme-icon', 'className')],
    [Input('theme-toggle', 'n_clicks')],
    [State('theme-store', 'data')]
)
def toggle_theme(n_clicks, current_theme):
    """Toggle between light and dark themes"""
    if n_clicks is None:
        # Initial load - return current theme
        icon = 'fas fa-sun' if current_theme == 'light' else 'fas fa-moon'
        return current_theme or 'dark', icon

    # Toggle theme
    new_theme = 'light' if current_theme == 'dark' else 'dark'
    icon = 'fas fa-sun' if new_theme == 'light' else 'fas fa-moon'

    return new_theme, icon

def load_data():
    """Load data with comprehensive error handling"""
    try:
        filepath = 'data/results.json'
        if not os.path.exists(filepath):
            return None
        
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        if not data or len(data) == 0:
            return None
        
        return data
    
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

@app.callback(
    [Output('neo-price', 'children'),
     Output('realized-vol', 'children'),
     Output('implied-vol', 'children'),
     Output('spread-value', 'children'),
     Output('vol-chart', 'figure'),
     Output('spread-chart', 'figure'),
     Output('garch-chart', 'figure'),
     Output('stats-panel', 'children'),
     Output('live-status', 'children')],
    [Input('interval', 'n_intervals'),
     Input('theme-store', 'data')]
)
def update_dashboard(n, theme):
    # Get colors for current theme
    theme = theme or 'dark'
    COLORS = get_colors(theme)
    chart_colors = get_chart_colors(theme)
    plotly_template = get_plotly_template(theme)

    data = load_data()

    # Default empty state
    empty_fig = go.Figure()
    empty_fig.update_layout(
        template=plotly_template,
        paper_bgcolor=COLORS['card'],
        plot_bgcolor=COLORS['card'],
        font=dict(color=COLORS['text']),
        height=300
    )
    
    if data is None:
        return (
            '$--', '--%', '--%', '--%',
            empty_fig, empty_fig, empty_fig,
            html.P('Waiting for data...', style={'color': COLORS['muted'], 'textAlign': 'center'}),
            [html.Span('● ', style={'color': COLORS['warning'], 'fontSize': '24px'}),
             html.Span('STARTING...', style={'fontWeight': 'bold', 'fontSize': '16px'})]
        )
    
    # Filter NEO data
    neo_data = [d for d in data if d.get('pair') == 'NEO/USDT'][-60:]
    
    if not neo_data:
        return (
            '$--', '--%', '--%', '--%',
            empty_fig, empty_fig, empty_fig,
            html.P('Generating data...', style={'color': COLORS['muted'], 'textAlign': 'center'}),
            [html.Span('● ', style={'color': COLORS['warning'], 'fontSize': '24px'}),
             html.Span('LOADING...', style={'fontWeight': 'bold', 'fontSize': '16px'})]
        )
    
    latest = neo_data[-1]
    
    # === METRIC CARDS ===
    price_display = f"${latest['price']:.2f}"
    rv_display = f"{latest['realized_vol']*100:.1f}%"
    iv_display = f"{latest['implied_vol']*100:.1f}%"
    spread_display = f"{latest['spread']*100:.1f}%"
    
    # === VOLATILITY COMPARISON CHART ===
    vol_fig = go.Figure()

    # Realized volatility
    vol_fig.add_trace(go.Scatter(
        y=[d['realized_vol']*100 for d in neo_data],
        mode='lines',
        name='Realized Vol',
        line=dict(color=chart_colors['success_line'], width=3),
        fill='tozeroy',
        fillcolor=chart_colors['success_fill']
    ))

    # Implied volatility
    vol_fig.add_trace(go.Scatter(
        y=[d['implied_vol']*100 for d in neo_data],
        mode='lines',
        name='Implied Vol',
        line=dict(color=chart_colors['danger_line'], width=3),
        fill='tozeroy',
        fillcolor=chart_colors['danger_fill']
    ))

    # GARCH forecast
    vol_fig.add_trace(go.Scatter(
        y=[d['garch_forecast']*100 for d in neo_data],
        mode='lines',
        name='GARCH Forecast',
        line=dict(color=chart_colors['primary_line'], width=2, dash='dot')
    ))

    vol_fig.update_layout(
        template=plotly_template,
        paper_bgcolor=COLORS['card'],
        plot_bgcolor=COLORS['card'],
        font=dict(color=COLORS['text'], size=12),
        yaxis_title='Volatility %',
        xaxis_title='Time',
        hovermode='x unified',
        height=350,
        margin=dict(l=50, r=20, t=20, b=40),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        transition_duration=500
    )
    
    # === SPREAD CHART ===
    spread_colors = [COLORS['success'] if s > 0 else COLORS['danger'] 
                     for s in [d['spread'] for d in neo_data]]
    
    spread_fig = go.Figure()
    spread_fig.add_trace(go.Bar(
        y=[d['spread']*100 for d in neo_data],
        marker_color=spread_colors,
        hovertemplate='Spread: %{y:.2f}%<extra></extra>',
        showlegend=False
    ))
    
    # Add zero line
    spread_fig.add_hline(y=0, line_dash="dash", line_color=chart_colors['zero_line'], line_width=1)

    spread_fig.update_layout(
        template=plotly_template,
        paper_bgcolor=COLORS['card'],
        plot_bgcolor=COLORS['card'],
        font=dict(color=COLORS['text'], size=12),
        yaxis_title='IV - RV Spread %',
        xaxis_title='Time',
        height=300,
        margin=dict(l=50, r=20, t=20, b=40),
        transition_duration=500
    )
    
    # === GARCH CHART ===
    garch_fig = go.Figure()
    garch_fig.add_trace(go.Scatter(
        y=[d['garch_forecast']*100 for d in neo_data],
        mode='lines+markers',
        name='Forecast',
        line=dict(color=chart_colors['primary_line'], width=3),
        marker=dict(size=4)
    ))

    # Add confidence band
    garch_vals = [d['garch_forecast']*100 for d in neo_data]
    garch_fig.add_trace(go.Scatter(
        y=[v*1.1 for v in garch_vals],
        mode='lines',
        line=dict(width=0),
        showlegend=False,
        hoverinfo='skip'
    ))
    garch_fig.add_trace(go.Scatter(
        y=[v*0.9 for v in garch_vals],
        mode='lines',
        line=dict(width=0),
        fillcolor=chart_colors['primary_fill'],
        fill='tonexty',
        showlegend=False,
        hoverinfo='skip'
    ))

    garch_fig.update_layout(
        template=plotly_template,
        paper_bgcolor=COLORS['card'],
        plot_bgcolor=COLORS['card'],
        font=dict(color=COLORS['text'], size=12),
        yaxis_title='Forecast Vol %',
        xaxis_title='Time',
        height=300,
        margin=dict(l=50, r=20, t=20, b=40),
        transition_duration=500
    )
    
    # === STATS PANEL ===
    stats_panel = html.Div([
        # Volatility Regime
        html.Div([
            html.P('Volatility Regime', style={'color': COLORS['muted'], 'fontSize': '12px', 'margin': '0'}),
            html.H3('NORMAL', style={'color': COLORS['success'], 'margin': '5px 0 20px 0'})
        ]),
        
        # Data points
        html.Div([
            html.P('Data Points', style={'color': COLORS['muted'], 'fontSize': '12px', 'margin': '0'}),
            html.H4(f'{len(neo_data)}', style={'color': COLORS['text'], 'margin': '5px 0 20px 0'})
        ]),
        
        # Agents active
        html.Div([
            html.P('Active Agents', style={'color': COLORS['muted'], 'fontSize': '12px', 'margin': '0'}),
            html.H4('5 / 5', style={'color': COLORS['success'], 'margin': '5px 0 20px 0'})
        ]),
        
        # Last update
        html.Div([
            html.P('Last Update', style={'color': COLORS['muted'], 'fontSize': '12px', 'margin': '0'}),
            html.H4(datetime.now().strftime('%H:%M:%S'), 
                   style={'color': COLORS['text'], 'margin': '5px 0 20px 0'})
        ]),
        
        # Trading signal
        html.Div([
            html.Div([
                html.P('Trading Signal', style={'fontSize': '12px', 'margin': '0 0 10px 0'}),
                dbc.Badge(
                    'BULLISH VOL' if latest['spread'] > 0 else 'BEARISH VOL',
                    color='success' if latest['spread'] > 0 else 'danger',
                    className='w-100',
                    style={'fontSize': '14px', 'padding': '10px'}
                )
            ], style={'marginTop': '20px'})
        ])
    ])
    
    # Live status
    live_status = [
        html.Span('● ', style={'color': COLORS['success'], 'fontSize': '24px'}),
        html.Span('LIVE', style={'fontWeight': 'bold', 'fontSize': '16px'})
    ]
    
    return (
        price_display, rv_display, iv_display, spread_display,
        vol_fig, spread_fig, garch_fig,
        stats_panel, live_status
    )

if __name__ == '__main__':
    print("\n" + "="*70)
    print("AGENTSPOONS CHAMPIONSHIP DASHBOARD")
    print("="*70)
    print("URL: http://localhost:8050")
    print("Auto-refresh: Every 2 seconds")
    print("UI: Production-ready championship design")
    print("="*70 + "\n")
    
    app.run(debug=False, host='0.0.0.0', port=8050)
