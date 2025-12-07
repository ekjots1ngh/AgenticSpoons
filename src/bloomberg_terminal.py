"""
AgentSpoons Bloomberg Terminal Clone
Professional institutional-grade trading terminal with all Bloomberg features
"""
import dash
from dash import dcc, html, Input, Output, State, ALL, MATCH, ctx
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from datetime import datetime, timedelta
import numpy as np
import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from dashboard.themes import get_colors

# Initialize app
app = dash.Dash(
    __name__,
    external_stylesheets=[
        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css'
    ],
    suppress_callback_exceptions=True
)

# Bloomberg Terminal Colors (Classic Orange & Black)
BLOOMBERG_COLORS = {
    'bg_black': '#000000',
    'bg_dark': '#0a0a0a',
    'bg_panel': '#1a1a1a',
    'bg_input': '#0d0d0d',
    'orange': '#ff8c00',        # Bloomberg signature orange
    'dark_orange': '#cc7000',   #Darker orange
    'green': '#00ff00',         # Terminal green
    'bright_green': '#00ff41',
    'red': '#ff0000',           # Bright red
    'bright_red': '#ff3333',
    'blue': '#00bfff',          # Deep sky blue
    'cyan': '#00ffff',
    'yellow': '#ffff00',        # Bright yellow
    'gold': '#ffd700',
    'magenta': '#ff00ff',
    'text': '#e0e0e0',          # Light gray text
    'text_dim': '#888888',      # Dimmed text
    'border': '#333333',
    'grid': '#1a1a1a'
}

# ====================================================================================
#  LAYOUT
# ====================================================================================

app.layout = html.Div(style={
    'backgroundColor': BLOOMBERG_COLORS['bg_black'],
    'height': '100vh',
    'overflow': 'hidden',
    'fontFamily': 'Courier New, monospace',
    'color': BLOOMBERG_COLORS['text']
}, children=[

    # ======================== TOP NAVIGATION BAR ========================
    html.Div(style={
        'backgroundColor': BLOOMBERG_COLORS['orange'],
        'padding': '8px 20px',
        'display': 'flex',
        'justifyContent': 'space-between',
        'alignItems': 'center',
        'borderBottom': f'2px solid {BLOOMBERG_COLORS["dark_orange"]}'
    }, children=[
        html.Div([
            html.Span('[AS] ', style={'fontSize': '20px', 'fontWeight': 'bold'}),
            html.Span('AGENTSPOONS', style={
                'fontSize': '18px',
                'fontWeight': 'bold',
                'color': BLOOMBERG_COLORS['bg_black'],
                'letterSpacing': '1px'
            }),
            html.Span(' TERMINAL', style={
                'fontSize': '14px',
                'color': BLOOMBERG_COLORS['bg_dark'],
                'marginLeft': '10px'
            })
        ]),
        html.Div([
            html.Span(id='top-ticker', children='NEO/USDT $15.23 ▲2.4%', style={
                'color': BLOOMBERG_COLORS['bg_black'],
                'fontSize': '14px',
                'fontWeight': 'bold',
                'marginRight': '30px'
            }),
            html.Span(id='top-clock', children='', style={
                'color': BLOOMBERG_COLORS['bg_dark'],
                'fontSize': '14px',
                'fontWeight': 'bold'
            })
        ])
    ]),

    # ======================== COMMAND LINE ========================
    html.Div(style={
        'backgroundColor': BLOOMBERG_COLORS['bg_input'],
        'padding': '10px 20px',
        'borderBottom': f'1px solid {BLOOMBERG_COLORS["border"]}'
    }, children=[
        html.Div([
            html.Span('>', style={
                'color': BLOOMBERG_COLORS['orange'],
                'fontSize': '16px',
                'fontWeight': 'bold',
                'marginRight': '10px'
            }),
            dcc.Input(
                id='command-input',
                type='text',
                placeholder='Enter command (e.g., NEO <GO>, VOL <GO>, NEWS <GO>, ALERT <GO>)...',
                style={
                    'backgroundColor': 'transparent',
                    'border': 'none',
                    'color': BLOOMBERG_COLORS['green'],
                    'fontSize': '14px',
                    'width': 'calc(100% - 150px)',
                    'fontFamily': 'Courier New, monospace',
                    'outline': 'none'
                },
                autoComplete='off'
            ),
            html.Span(id='command-hint', style={
                'color': BLOOMBERG_COLORS['text_dim'],
                'fontSize': '12px',
                'marginLeft': '20px',
                'fontStyle': 'italic'
            })
        ], style={'display': 'flex', 'alignItems': 'center'})
    ]),

    # ======================== MAIN CONTENT AREA ========================
    html.Div(style={'height': 'calc(100vh - 160px)', 'overflow': 'hidden'}, children=[

        dbc.Row(style={'height': '100%', 'margin': 0}, children=[

            # ============ LEFT SIDEBAR (25%) ============
            dbc.Col(width=3, style={
                'backgroundColor': BLOOMBERG_COLORS['bg_dark'],
                'height': '100%',
                'overflowY': 'auto',
                'borderRight': f'1px solid {BLOOMBERG_COLORS["border"]}',
                'padding': 0
            }, children=[

                # WATCHLIST
                html.Div(style={'borderBottom': f'1px solid {BLOOMBERG_COLORS["border"]}'}, children=[
                    html.Div('WATCHLIST', style={
                        'backgroundColor': BLOOMBERG_COLORS['orange'],
                        'color': BLOOMBERG_COLORS['bg_black'],
                        'padding': '6px 12px',
                        'fontSize': '11px',
                        'fontWeight': 'bold',
                        'letterSpacing': '1px'
                    }),
                    html.Div(id='watchlist-panel', style={'padding': '10px'})
                ]),

                # MARKET OVERVIEW
                html.Div(style={'borderBottom': f'1px solid {BLOOMBERG_COLORS["border"]}'}, children=[
                    html.Div('MARKET OVERVIEW', style={
                        'backgroundColor': BLOOMBERG_COLORS['orange'],
                        'color': BLOOMBERG_COLORS['bg_black'],
                        'padding': '6px 12px',
                        'fontSize': '11px',
                        'fontWeight': 'bold',
                        'letterSpacing': '1px'
                    }),
                    html.Div(id='market-overview', style={'padding': '10px', 'fontSize': '11px'})
                ]),

                # PORTFOLIO
                html.Div(children=[
                    html.Div('PORTFOLIO', style={
                        'backgroundColor': BLOOMBERG_COLORS['orange'],
                        'color': BLOOMBERG_COLORS['bg_black'],
                        'padding': '6px 12px',
                        'fontSize': '11px',
                        'fontWeight': 'bold',
                        'letterSpacing': '1px'
                    }),
                    html.Div(id='portfolio-panel', style={'padding': '10px', 'fontSize': '11px'})
                ]),
            ]),

            # ============ CENTER PANEL (50%) ============
            dbc.Col(width=6, style={
                'backgroundColor': BLOOMBERG_COLORS['bg_panel'],
                'height': '100%',
                'overflowY': 'auto',
                'padding': 0
            }, children=[

                # SECURITY HEADER
                html.Div(id='security-header', style={
                    'backgroundColor': BLOOMBERG_COLORS['bg_black'],
                    'padding': '12px 15px',
                    'borderBottom': f'2px solid {BLOOMBERG_COLORS["orange"]}'
                }),

                # MAIN CHART
                html.Div(style={'height': '40%'}, children=[
                    dcc.Graph(
                        id='main-price-chart',
                        config={'displayModeBar': False},
                        style={'height': '100%'}
                    )
                ]),

                # TABS FOR DIFFERENT VIEWS
                html.Div(style={'borderTop': f'1px solid {BLOOMBERG_COLORS["border"]}'}, children=[
                    dbc.Tabs(id='main-tabs', active_tab='volatility', children=[
                        dbc.Tab(label='VOL', tab_id='volatility', label_style={
                            'backgroundColor': BLOOMBERG_COLORS['bg_panel'],
                            'color': BLOOMBERG_COLORS['text'],
                            'fontSize': '11px',
                            'fontFamily': 'Courier New, monospace'
                        }),
                        dbc.Tab(label='GREEKS', tab_id='greeks', label_style={
                            'backgroundColor': BLOOMBERG_COLORS['bg_panel'],
                            'color': BLOOMBERG_COLORS['text'],
                            'fontSize': '11px',
                            'fontFamily': 'Courier New, monospace'
                        }),
                        dbc.Tab(label='DEPTH', tab_id='depth', label_style={
                            'backgroundColor': BLOOMBERG_COLORS['bg_panel'],
                            'color': BLOOMBERG_COLORS['text'],
                            'fontSize': '11px',
                            'fontFamily': 'Courier New, monospace'
                        }),
                        dbc.Tab(label='NEWS', tab_id='news', label_style={
                            'backgroundColor': BLOOMBERG_COLORS['bg_panel'],
                            'color': BLOOMBERG_COLORS['text'],
                            'fontSize': '11px',
                            'fontFamily': 'Courier New, monospace'
                        }),
                    ], style={'marginBottom': 0})
                ]),

                # TAB CONTENT
                html.Div(id='tab-content', style={
                    'height': 'calc(60% - 100px)',
                    'padding': '10px',
                    'overflowY': 'auto'
                })
            ]),

            # ============ RIGHT SIDEBAR (25%) ============
            dbc.Col(width=3, style={
                'backgroundColor': BLOOMBERG_COLORS['bg_dark'],
                'height': '100%',
                'overflowY': 'auto',
                'borderLeft': f'1px solid {BLOOMBERG_COLORS["border"]}',
                'padding': 0
            }, children=[

                # OPTIONS CALCULATOR
                html.Div(style={'borderBottom': f'1px solid {BLOOMBERG_COLORS["border"]}'}, children=[
                    html.Div('OPTIONS PRICER', style={
                        'backgroundColor': BLOOMBERG_COLORS['orange'],
                        'color': BLOOMBERG_COLORS['bg_black'],
                        'padding': '6px 12px',
                        'fontSize': '11px',
                        'fontWeight': 'bold',
                        'letterSpacing': '1px'
                    }),
                    html.Div(id='options-panel', style={'padding': '10px'})
                ]),

                # ANALYTICS
                html.Div(style={'borderBottom': f'1px solid {BLOOMBERG_COLORS["border"]}'}, children=[
                    html.Div('ANALYTICS', style={
                        'backgroundColor': BLOOMBERG_COLORS['orange'],
                        'color': BLOOMBERG_COLORS['bg_black'],
                        'padding': '6px 12px',
                        'fontSize': '11px',
                        'fontWeight': 'bold',
                        'letterSpacing': '1px'
                    }),
                    html.Div(id='analytics-panel', style={'padding': '10px', 'fontSize': '11px'})
                ]),

                # ALERTS
                html.Div(children=[
                    html.Div('ALERTS', style={
                        'backgroundColor': BLOOMBERG_COLORS['orange'],
                        'color': BLOOMBERG_COLORS['bg_black'],
                        'padding': '6px 12px',
                        'fontSize': '11px',
                        'fontWeight': 'bold',
                        'letterSpacing': '1px'
                    }),
                    html.Div(id='alerts-panel', style={'padding': '10px', 'fontSize': '11px'})
                ]),
            ])
        ])
    ]),

    # ======================== BOTTOM STATUS BAR ========================
    html.Div(style={
        'backgroundColor': BLOOMBERG_COLORS['bg_black'],
        'padding': '6px 20px',
        'borderTop': f'2px solid {BLOOMBERG_COLORS["orange"]}',
        'display': 'flex',
        'justifyContent': 'space-between',
        'fontSize': '10px'
    }, children=[
        html.Div([
            html.Span('[*] ', style={'color': BLOOMBERG_COLORS['green'], 'fontWeight': 'bold'}),
            html.Span('LIVE', style={'color': BLOOMBERG_COLORS['green'], 'fontWeight': 'bold', 'marginRight': '20px'}),
            html.Span('AGENTS: ', style={'color': BLOOMBERG_COLORS['text_dim']}),
            html.Span('5/5 ACTIVE', style={'color': BLOOMBERG_COLORS['green'], 'marginRight': '20px'}),
            html.Span('NEO TESTNET', style={'color': BLOOMBERG_COLORS['blue'], 'marginRight': '20px'}),
        ]),
        html.Div(id='status-bar-right', style={'color': BLOOMBERG_COLORS['text_dim']})
    ]),

    # Hidden components
    dcc.Store(id='current-security', data='NEO/USDT'),
    dcc.Store(id='theme-store', storage_type='local', data='bloomberg'),
    dcc.Interval(id='interval-fast', interval=1000),  # 1 second for clock
    dcc.Interval(id='interval-data', interval=2000),  # 2 seconds for data
])

# ====================================================================================
#  CALLBACKS
# ====================================================================================

@app.callback(
    Output('top-clock', 'children'),
    Input('interval-fast', 'n_intervals')
)
def update_clock(n):
    """Update clock every second"""
    now = datetime.now()
    return now.strftime('%H:%M:%S UTC')

@app.callback(
    [Output('watchlist-panel', 'children'),
     Output('market-overview', 'children'),
     Output('portfolio-panel', 'children'),
     Output('security-header', 'children'),
     Output('main-price-chart', 'figure'),
     Output('options-panel', 'children'),
     Output('analytics-panel', 'children'),
     Output('alerts-panel', 'children'),
     Output('top-ticker', 'children'),
     Output('status-bar-right', 'children')],
    [Input('interval-data', 'n_intervals'),
     Input('current-security', 'data')]
)
def update_all_panels(n, security):
    """Update all dashboard panels"""

    # Generate sample data
    price = 15.23 + np.random.normal(0, 0.05)
    change_pct = 2.4 + np.random.normal(0, 0.2)
    rv = 52.3 + np.random.normal(0, 1)
    iv = 58.1 + np.random.normal(0, 1)

    # Watchlist
    watchlist_data = [
        {'symbol': 'NEO/USDT', 'price': price, 'change': change_pct, 'vol': rv},
        {'symbol': 'GAS/USDT', 'price': 5.12, 'change': -1.2, 'vol': 48.2},
        {'symbol': 'BTC/USDT', 'price': 43250, 'change': 3.5, 'vol': 35.8},
        {'symbol': 'ETH/USDT', 'price': 2280, 'change': 2.1, 'vol': 42.3},
    ]

    watchlist = html.Table(style={'width': '100%', 'fontSize': '11px'}, children=[
        html.Thead(html.Tr([
            html.Th('SYM', style={'color': BLOOMBERG_COLORS['text_dim'], 'padding': '4px 2px'}),
            html.Th('LAST', style={'color': BLOOMBERG_COLORS['text_dim'], 'padding': '4px 2px'}),
            html.Th('CHG%', style={'color': BLOOMBERG_COLORS['text_dim'], 'padding': '4px 2px'}),
            html.Th('VOL', style={'color': BLOOMBERG_COLORS['text_dim'], 'padding': '4px 2px'}),
        ])),
        html.Tbody([
            html.Tr([
                html.Td(item['symbol'], style={'color': BLOOMBERG_COLORS['orange'], 'padding': '6px 2px', 'fontWeight': 'bold'}),
                html.Td(f"${item['price']:.2f}", style={
                    'color': BLOOMBERG_COLORS['green'] if item['change'] > 0 else BLOOMBERG_COLORS['red'],
                    'padding': '6px 2px'
                }),
                html.Td(f"{item['change']:+.1f}%", style={
                    'color': BLOOMBERG_COLORS['green'] if item['change'] > 0 else BLOOMBERG_COLORS['red'],
                    'padding': '6px 2px',
                    'fontWeight': 'bold'
                }),
                html.Td(f"{item['vol']:.1f}", style={'color': BLOOMBERG_COLORS['yellow'], 'padding': '6px 2px'}),
            ], style={'borderBottom': f'1px solid {BLOOMBERG_COLORS["border"]}'})
            for item in watchlist_data
        ])
    ])

    # Market Overview
    market_stats = html.Div([
        html.Div([
            html.Span('24H HIGH: ', style={'color': BLOOMBERG_COLORS['text_dim']}),
            html.Span(f'${price*1.03:.2f}', style={'color': BLOOMBERG_COLORS['green'], 'fontWeight': 'bold'})
        ], style={'marginBottom': '8px'}),
        html.Div([
            html.Span('24H LOW: ', style={'color': BLOOMBERG_COLORS['text_dim']}),
            html.Span(f'${price*0.97:.2f}', style={'color': BLOOMBERG_COLORS['red'], 'fontWeight': 'bold'})
        ], style={'marginBottom': '8px'}),
        html.Div([
            html.Span('VOLUME: ', style={'color': BLOOMBERG_COLORS['text_dim']}),
            html.Span('$12.5M', style={'color': BLOOMBERG_COLORS['blue'], 'fontWeight': 'bold'})
        ], style={'marginBottom': '8px'}),
        html.Div([
            html.Span('MARKET CAP: ', style={'color': BLOOMBERG_COLORS['text_dim']}),
            html.Span('$1.52B', style={'color': BLOOMBERG_COLORS['cyan'], 'fontWeight': 'bold'})
        ], style={'marginBottom': '8px'}),
        html.Hr(style={'borderColor': BLOOMBERG_COLORS['border'], 'margin': '10px 0'}),
        html.Div([
            html.Span('RV 30D: ', style={'color': BLOOMBERG_COLORS['text_dim']}),
            html.Span(f'{rv:.1f}%', style={'color': BLOOMBERG_COLORS['yellow'], 'fontWeight': 'bold'})
        ], style={'marginBottom': '8px'}),
        html.Div([
            html.Span('IV ATM: ', style={'color': BLOOMBERG_COLORS['text_dim']}),
            html.Span(f'{iv:.1f}%', style={'color': BLOOMBERG_COLORS['orange'], 'fontWeight': 'bold'})
        ]),
    ])

    # Portfolio
    portfolio = html.Div([
        html.Div([
            html.Span('TOTAL VALUE: ', style={'color': BLOOMBERG_COLORS['text_dim'], 'fontSize': '10px'}),
            html.Div('$125,430.50', style={'color': BLOOMBERG_COLORS['green'], 'fontSize': '16px', 'fontWeight': 'bold', 'margin': '5px 0'})
        ], style={'marginBottom': '12px'}),
        html.Div([
            html.Span('P&L TODAY: ', style={'color': BLOOMBERG_COLORS['text_dim'], 'fontSize': '10px'}),
            html.Div('+$3,245.80 (+2.65%)', style={'color': BLOOMBERG_COLORS['green'], 'fontSize': '12px', 'fontWeight': 'bold'})
        ]),
    ])

    # Security Header
    security_header = html.Div([
        html.Div([
            html.Span(security, style={
                'color': BLOOMBERG_COLORS['orange'],
                'fontSize': '20px',
                'fontWeight': 'bold',
                'marginRight': '20px'
            }),
            html.Span(f'${price:.2f}', style={
                'color': BLOOMBERG_COLORS['green'] if change_pct > 0 else BLOOMBERG_COLORS['red'],
                'fontSize': '24px',
                'fontWeight': 'bold',
                'marginRight': '15px'
            }),
            html.Span(f'{change_pct:+.2f}%' + (' ▲' if change_pct > 0 else ' ▼'), style={
                'color': BLOOMBERG_COLORS['green'] if change_pct > 0 else BLOOMBERG_COLORS['red'],
                'fontSize': '14px',
                'fontWeight': 'bold'
            })
        ]),
        html.Div([
            html.Span(f'BID: ${price-0.01:.2f}  ', style={'color': BLOOMBERG_COLORS['blue'], 'fontSize': '11px', 'marginRight': '15px'}),
            html.Span(f'ASK: ${price+0.01:.2f}  ', style={'color': BLOOMBERG_COLORS['red'], 'fontSize': '11px', 'marginRight': '15px'}),
            html.Span(f'SPREAD: 0.02 (0.13%)', style={'color': BLOOMBERG_COLORS['text_dim'], 'fontSize': '11px'}),
        ], style={'marginTop': '5px'})
    ])

    # Main Chart
    x_data = list(range(100))
    price_data = [price + np.sin(i/10) * 0.3 + np.random.normal(0, 0.05) for i in x_data]

    main_chart = go.Figure()
    main_chart.add_trace(go.Candlestick(
        x=x_data,
        open=[p - 0.05 for p in price_data],
        high=[p + 0.10 for p in price_data],
        low=[p - 0.10 for p in price_data],
        close=price_data,
        increasing_line_color=BLOOMBERG_COLORS['green'],
        decreasing_line_color=BLOOMBERG_COLORS['red'],
        increasing_fillcolor=BLOOMBERG_COLORS['green'],
        decreasing_fillcolor=BLOOMBERG_COLORS['red']
    ))

    main_chart.update_layout(
        template='plotly_dark',
        paper_bgcolor=BLOOMBERG_COLORS['bg_panel'],
        plot_bgcolor=BLOOMBERG_COLORS['bg_black'],
        font={'family': 'Courier New, monospace', 'color': BLOOMBERG_COLORS['text'], 'size': 10},
        margin={'l': 50, 'r': 20, 't': 20, 'b': 30},
        xaxis={'showgrid': False, 'showticklabels': False, 'zeroline': False},
        yaxis={'gridcolor': BLOOMBERG_COLORS['grid'], 'tickformat': '.2f'},
        showlegend=False,
        hovermode='x unified'
    )

    # Options Panel
    options_panel = html.Div([
        html.Div('CALL $16.00 30D', style={
            'color': BLOOMBERG_COLORS['orange'],
            'fontWeight': 'bold',
            'marginBottom': '10px',
            'fontSize': '12px'
        }),
        html.Div([
            html.Span('PRICE: ', style={'color': BLOOMBERG_COLORS['text_dim'], 'fontSize': '10px'}),
            html.Div('$1.45', style={
                'color': BLOOMBERG_COLORS['green'],
                'fontSize': '18px',
                'fontWeight': 'bold',
                'margin': '5px 0'
            })
        ]),
        html.Hr(style={'borderColor': BLOOMBERG_COLORS['border'], 'margin': '12px 0'}),
        html.Div([
            html.Div(['DELTA: ', html.Span('0.6234', style={'color': BLOOMBERG_COLORS['green'], 'float': 'right'})], style={'marginBottom': '6px'}),
            html.Div(['GAMMA: ', html.Span('0.0189', style={'color': BLOOMBERG_COLORS['blue'], 'float': 'right'})], style={'marginBottom': '6px'}),
            html.Div(['VEGA: ', html.Span('0.1456', style={'color': BLOOMBERG_COLORS['yellow'], 'float': 'right'})], style={'marginBottom': '6px'}),
            html.Div(['THETA: ', html.Span('-0.0823', style={'color': BLOOMBERG_COLORS['red'], 'float': 'right'})], style={'marginBottom': '6px'}),
            html.Div(['RHO: ', html.Span('0.0567', style={'color': BLOOMBERG_COLORS['cyan'], 'float': 'right'})]),
        ], style={'fontSize': '10px', 'color': BLOOMBERG_COLORS['text_dim']})
    ])

    # Analytics
    analytics = html.Div([
        html.Div([
            html.Span('SHARPE RATIO: ', style={'color': BLOOMBERG_COLORS['text_dim']}),
            html.Span('1.85', style={'color': BLOOMBERG_COLORS['green'], 'fontWeight': 'bold'})
        ], style={'marginBottom': '8px'}),
        html.Div([
            html.Span('VAR (95%): ', style={'color': BLOOMBERG_COLORS['text_dim']}),
            html.Span('-$2,340', style={'color': BLOOMBERG_COLORS['red'], 'fontWeight': 'bold'})
        ], style={'marginBottom': '8px'}),
        html.Div([
            html.Span('BETA: ', style={'color': BLOOMBERG_COLORS['text_dim']}),
            html.Span('1.23', style={'color': BLOOMBERG_COLORS['blue'], 'fontWeight': 'bold'})
        ], style={'marginBottom': '8px'}),
        html.Div([
            html.Span('CORRELATION: ', style={'color': BLOOMBERG_COLORS['text_dim']}),
            html.Span('0.78', style={'color': BLOOMBERG_COLORS['yellow'], 'fontWeight': 'bold'})
        ]),
    ])

    # Alerts
    alerts = html.Div([
        html.Div([
            html.Div([
                html.Span('[!] ', style={'color': BLOOMBERG_COLORS['yellow'], 'fontWeight': 'bold'}),
                html.Span('VOL SPIKE', style={'color': BLOOMBERG_COLORS['yellow'], 'fontSize': '10px', 'fontWeight': 'bold'})
            ]),
            html.Div('IV > RV by 10%', style={'color': BLOOMBERG_COLORS['text_dim'], 'fontSize': '9px', 'marginTop': '2px'}),
            html.Div('2 min ago', style={'color': BLOOMBERG_COLORS['text_dim'], 'fontSize': '8px', 'marginTop': '2px'})
        ], style={'padding': '8px', 'backgroundColor': BLOOMBERG_COLORS['bg_panel'], 'borderRadius': '4px', 'marginBottom': '8px'}),

        html.Div([
            html.Div([
                html.Span('[+] ', style={'color': BLOOMBERG_COLORS['green'], 'fontWeight': 'bold'}),
                html.Span('ARBITRAGE', style={'color': BLOOMBERG_COLORS['green'], 'fontSize': '10px', 'fontWeight': 'bold'})
            ]),
            html.Div('Spread detected', style={'color': BLOOMBERG_COLORS['text_dim'], 'fontSize': '9px', 'marginTop': '2px'}),
            html.Div('5 min ago', style={'color': BLOOMBERG_COLORS['text_dim'], 'fontSize': '8px', 'marginTop': '2px'})
        ], style={'padding': '8px', 'backgroundColor': BLOOMBERG_COLORS['bg_panel'], 'borderRadius': '4px'})
    ])

    # Top ticker
    top_ticker_text = f'{security} ${price:.2f} {change_pct:+.1f}%'

    # Status bar
    status_text = f'LAST UPDATE: {datetime.now().strftime("%H:%M:%S")} | CONTRACT: 0x7a2b...f3c9'

    return (
        watchlist,
        market_stats,
        portfolio,
        security_header,
        main_chart,
        options_panel,
        analytics,
        alerts,
        top_ticker_text,
        status_text
    )

@app.callback(
    Output('tab-content', 'children'),
    [Input('main-tabs', 'active_tab'),
     Input('interval-data', 'n_intervals')]
)
def update_tab_content(active_tab, n):
    """Update content based on active tab"""

    if active_tab == 'volatility':
        # Volatility Surface
        x_data = list(range(60))
        rv_data = [50 + np.sin(i/10) * 5 + np.random.normal(0, 1) for i in x_data]
        iv_data = [rv * 1.1 + np.random.normal(0, 1.5) for rv in rv_data]
        garch_data = [rv * 1.05 + np.random.normal(0, 0.8) for rv in rv_data]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_data, y=rv_data, name='REALIZED VOL',
                                 line={'color': BLOOMBERG_COLORS['green'], 'width': 2}))
        fig.add_trace(go.Scatter(x=x_data, y=iv_data, name='IMPLIED VOL',
                                 line={'color': BLOOMBERG_COLORS['orange'], 'width': 2}))
        fig.add_trace(go.Scatter(x=x_data, y=garch_data, name='GARCH FORECAST',
                                 line={'color': BLOOMBERG_COLORS['blue'], 'width': 2, 'dash': 'dot'}))

        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor=BLOOMBERG_COLORS['bg_panel'],
            plot_bgcolor=BLOOMBERG_COLORS['bg_black'],
            font={'family': 'Courier New, monospace', 'color': BLOOMBERG_COLORS['text'], 'size': 10},
            margin={'l': 50, 'r': 20, 't': 30, 'b': 40},
            yaxis={'title': 'VOL %', 'gridcolor': BLOOMBERG_COLORS['grid']},
            xaxis={'title': 'TIME', 'gridcolor': BLOOMBERG_COLORS['grid']},
            legend={'x': 0, 'y': 1, 'bgcolor': 'rgba(0,0,0,0.5)'},
            height=300
        )

        return dcc.Graph(figure=fig, config={'displayModeBar': False}, style={'height': '100%'})

    elif active_tab == 'greeks':
        # Greeks heatmap/table
        strikes = [14, 15, 16, 17, 18]
        greeks_data = []

        for strike in strikes:
            greeks_data.append(html.Tr([
                html.Td(f'${strike}', style={'color': BLOOMBERG_COLORS['orange'], 'padding': '8px'}),
                html.Td(f'{0.3 + (strike-15)*0.1:.3f}', style={'color': BLOOMBERG_COLORS['green'], 'padding': '8px'}),
                html.Td(f'{0.02:.3f}', style={'color': BLOOMBERG_COLORS['blue'], 'padding': '8px'}),
                html.Td(f'{0.15 + np.random.normal(0, 0.02):.3f}', style={'color': BLOOMBERG_COLORS['yellow'], 'padding': '8px'}),
                html.Td(f'{-0.08 + np.random.normal(0, 0.01):.3f}', style={'color': BLOOMBERG_COLORS['red'], 'padding': '8px'}),
            ]))

        return html.Table(style={'width': '100%', 'fontSize': '11px'}, children=[
            html.Thead(html.Tr([
                html.Th('STRIKE', style={'color': BLOOMBERG_COLORS['text_dim'], 'padding': '8px', 'borderBottom': f'1px solid {BLOOMBERG_COLORS["border"]}'}),
                html.Th('DELTA', style={'color': BLOOMBERG_COLORS['text_dim'], 'padding': '8px', 'borderBottom': f'1px solid {BLOOMBERG_COLORS["border"]}'}),
                html.Th('GAMMA', style={'color': BLOOMBERG_COLORS['text_dim'], 'padding': '8px', 'borderBottom': f'1px solid {BLOOMBERG_COLORS["border"]}'}),
                html.Th('VEGA', style={'color': BLOOMBERG_COLORS['text_dim'], 'padding': '8px', 'borderBottom': f'1px solid {BLOOMBERG_COLORS["border"]}'}),
                html.Th('THETA', style={'color': BLOOMBERG_COLORS['text_dim'], 'padding': '8px', 'borderBottom': f'1px solid {BLOOMBERG_COLORS["border"]}'}),
            ])),
            html.Tbody(greeks_data)
        ])

    elif active_tab == 'depth':
        # Market Depth / Order Book
        bids = [(15.22, 1250), (15.21, 3400), (15.20, 5600), (15.19, 2300), (15.18, 4100)]
        asks = [(15.23, 1100), (15.24, 2800), (15.25, 4200), (15.26, 1900), (15.27, 3600)]

        return html.Div([
            html.Div('ORDER BOOK', style={
                'color': BLOOMBERG_COLORS['orange'],
                'fontSize': '12px',
                'fontWeight': 'bold',
                'marginBottom': '15px'
            }),
            html.Div(style={'display': 'flex', 'gap': '20px'}, children=[
                # Bids
                html.Div(style={'flex': 1}, children=[
                    html.Div('BIDS', style={'color': BLOOMBERG_COLORS['green'], 'fontSize': '10px', 'fontWeight': 'bold', 'marginBottom': '8px'}),
                    html.Table(style={'width': '100%', 'fontSize': '10px'}, children=[
                        html.Tbody([
                            html.Tr([
                                html.Td(f'${bid[0]:.2f}', style={'color': BLOOMBERG_COLORS['green'], 'padding': '4px'}),
                                html.Td(f'{bid[1]:,}', style={'color': BLOOMBERG_COLORS['text'], 'padding': '4px', 'textAlign': 'right'}),
                            ])
                            for bid in bids
                        ])
                    ])
                ]),
                # Asks
                html.Div(style={'flex': 1}, children=[
                    html.Div('ASKS', style={'color': BLOOMBERG_COLORS['red'], 'fontSize': '10px', 'fontWeight': 'bold', 'marginBottom': '8px'}),
                    html.Table(style={'width': '100%', 'fontSize': '10px'}, children=[
                        html.Tbody([
                            html.Tr([
                                html.Td(f'${ask[0]:.2f}', style={'color': BLOOMBERG_COLORS['red'], 'padding': '4px'}),
                                html.Td(f'{ask[1]:,}', style={'color': BLOOMBERG_COLORS['text'], 'padding': '4px', 'textAlign': 'right'}),
                            ])
                            for ask in asks
                        ])
                    ])
                ])
            ])
        ])

    elif active_tab == 'news':
        # News Feed
        news_items = [
            {'time': '10:45', 'headline': 'NEO N3 MAINNET UPGRADE COMPLETE', 'source': 'CryptoNews'},
            {'time': '09:30', 'headline': 'VOLATILITY SPIKE IN CRYPTO MARKETS', 'source': 'Bloomberg'},
            {'time': '08:15', 'headline': 'NEO DEVELOPER COMMUNITY GROWS 25%', 'source': 'CoinDesk'},
            {'time': '07:00', 'headline': 'NEW DEFI PROTOCOL LAUNCHES ON NEO', 'source': 'The Block'},
        ]

        return html.Div([
            html.Div([
                html.Div([
                    html.Span(item['time'], style={
                        'color': BLOOMBERG_COLORS['blue'],
                        'fontSize': '9px',
                        'marginRight': '10px',
                        'fontWeight': 'bold'
                    }),
                    html.Span(item['headline'], style={
                        'color': BLOOMBERG_COLORS['orange'],
                        'fontSize': '11px',
                        'fontWeight': 'bold'
                    })
                ]),
                html.Div(item['source'], style={
                    'color': BLOOMBERG_COLORS['text_dim'],
                    'fontSize': '9px',
                    'marginTop': '2px',
                    'marginLeft': '45px'
                })
            ], style={
                'padding': '10px',
                'borderBottom': f'1px solid {BLOOMBERG_COLORS["border"]}',
                'cursor': 'pointer'
            })
            for item in news_items
        ])

    return html.Div('Select a tab')

if __name__ == '__main__':
    print("\n" + "="*80)
    print("AGENTSPOONS BLOOMBERG TERMINAL")
    print("="*80)
    print("URL: http://localhost:8050")
    print("Features:")
    print("  * Professional Bloomberg-style interface")
    print("  * Real-time market data & volatility tracking")
    print("  * Options pricing & Greeks calculation")
    print("  * Market depth & order book display")
    print("  * News feed & alerts system")
    print("  * Multi-panel layout with watchlists")
    print("="*80 + "\n")

    app.run(debug=True, host='0.0.0.0', port=8050)
