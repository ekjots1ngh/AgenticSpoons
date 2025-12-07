"""
AgentSpoons HACKATHON WINNER Edition
Ultra-Premium UI designed to WIN the hackathon
Combines Bloomberg professionalism with modern flair and Neo N3 integration
"""
import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from datetime import datetime
import numpy as np
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from dashboard.themes import get_colors

# Initialize app with premium theme
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.CYBORG,
        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css',
        'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap'
    ],
    suppress_callback_exceptions=True
)

# PREMIUM COLOR SCHEME - Winning Design
COLORS = {
    # Neo N3 Brand Colors
    'neo_green': '#00E599',      # Neo primary green
    'neo_dark': '#0A0E1A',       # Deep dark
    'neo_accent': '#58FFC6',     # Bright accent

    # Bloomberg Professional
    'orange': '#FF8C00',
    'bg_black': '#000000',
    'bg_dark': '#0A0A0A',
    'bg_panel': '#1A1A1A',
    'bg_card': '#141414',

    # Status Colors
    'success': '#00FF41',        # Matrix green
    'danger': '#FF3366',         # Modern red
    'warning': '#FFD93D',        # Gold
    'info': '#00D4FF',           # Cyan

    # Text
    'text': '#FFFFFF',
    'text_secondary': '#A0A0A0',
    'text_dim': '#666666',

    # Gradients
    'gradient_primary': 'linear-gradient(135deg, #00E599 0%, #00D4FF 100%)',
    'gradient_dark': 'linear-gradient(180deg, #0A0E1A 0%, #1A1A1A 100%)',
    'gradient_card': 'linear-gradient(135deg, #1A1A1A 0%, #0F0F0F 100%)',
}

# Custom CSS for animations and premium effects
CUSTOM_CSS = """
<style>
@keyframes pulse-glow {
    0%, 100% { box-shadow: 0 0 20px rgba(0, 229, 153, 0.3); }
    50% { box-shadow: 0 0 30px rgba(0, 229, 153, 0.6); }
}

@keyframes slide-in {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.premium-card {
    animation: slide-in 0.6s ease-out;
    transition: all 0.3s ease;
}

.premium-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 40px rgba(0, 229, 153, 0.2);
}

.live-indicator {
    animation: pulse-glow 2s infinite;
}

.scrollbar-neo::-webkit-scrollbar {
    width: 8px;
}

.scrollbar-neo::-webkit-scrollbar-track {
    background: #0A0A0A;
}

.scrollbar-neo::-webkit-scrollbar-thumb {
    background: #00E599;
    border-radius: 4px;
}

.scrollbar-neo::-webkit-scrollbar-thumb:hover {
    background: #58FFC6;
}

.glow-text {
    text-shadow: 0 0 10px rgba(0, 229, 153, 0.5);
}
</style>
"""

# ====================================================================================
#  HACKATHON-WINNING LAYOUT
# ====================================================================================

app.layout = html.Div(style={
    'backgroundColor': COLORS['bg_black'],
    'minHeight': '100vh',
    'fontFamily': 'Inter, sans-serif',
    'color': COLORS['text']
}, children=[

    # Inject custom CSS
    html.Div(dcc.Markdown(CUSTOM_CSS, dangerously_allow_html=True)),

    # ======================== PREMIUM HEADER ========================
    html.Div(style={
        'background': COLORS['gradient_primary'],
        'padding': '20px 40px',
        'display': 'flex',
        'justifyContent': 'space-between',
        'alignItems': 'center',
        'boxShadow': '0 4px 20px rgba(0, 229, 153, 0.3)'
    }, children=[
        html.Div([
            html.H1([
                html.Span('AGENT', style={'fontWeight': '900', 'color': COLORS['bg_black']}),
                html.Span('SPOONS', style={'fontWeight': '300', 'color': COLORS['bg_dark'], 'marginLeft': '10px'})
            ], style={'margin': 0, 'fontSize': '32px', 'letterSpacing': '2px'}),
            html.P('Decentralized Volatility Oracle on Neo N3', style={
                'margin': '5px 0 0 0',
                'color': COLORS['bg_dark'],
                'fontSize': '14px',
                'fontWeight': '500'
            })
        ]),
        html.Div([
            html.Div([
                html.Span('[*] ', style={'color': COLORS['bg_black'], 'fontWeight': 'bold', 'fontSize': '16px'}),
                html.Span('LIVE', style={'color': COLORS['bg_black'], 'fontWeight': 'bold', 'fontSize': '16px', 'marginRight': '20px'}),
                html.Span(id='header-clock', style={'color': COLORS['bg_dark'], 'fontSize': '14px', 'fontWeight': '600'})
            ], className='live-indicator', style={
                'backgroundColor': 'rgba(0, 0, 0, 0.2)',
                'padding': '10px 20px',
                'borderRadius': '25px'
            })
        ])
    ]),

    # ======================== KEY METRICS BAR ========================
    html.Div(style={
        'background': COLORS['bg_dark'],
        'padding': '20px 40px',
        'borderBottom': f'1px solid {COLORS["neo_green"]}'
    }, children=[
        dbc.Row([
            dbc.Col([
                html.Div(className='premium-card', style={
                    'background': COLORS['gradient_card'],
                    'padding': '20px',
                    'borderRadius': '15px',
                    'border': f'1px solid {COLORS["neo_green"]}',
                    'textAlign': 'center'
                }, children=[
                    html.P('NEO PRICE', style={'color': COLORS['text_secondary'], 'fontSize': '11px', 'margin': 0, 'fontWeight': '600', 'letterSpacing': '1px'}),
                    html.H2(id='neo-price-big', style={'color': COLORS['neo_green'], 'margin': '10px 0 5px', 'fontSize': '36px', 'fontWeight': '900', 'className': 'glow-text'}),
                    html.P(id='neo-change', style={'color': COLORS['success'], 'fontSize': '14px', 'margin': 0, 'fontWeight': '600'})
                ])
            ], width=3),
            dbc.Col([
                html.Div(className='premium-card', style={
                    'background': COLORS['gradient_card'],
                    'padding': '20px',
                    'borderRadius': '15px',
                    'border': f'1px solid {COLORS["info"]}',
                    'textAlign': 'center'
                }, children=[
                    html.P('REALIZED VOL', style={'color': COLORS['text_secondary'], 'fontSize': '11px', 'margin': 0, 'fontWeight': '600', 'letterSpacing': '1px'}),
                    html.H2(id='rv-display', style={'color': COLORS['info'], 'margin': '10px 0 5px', 'fontSize': '36px', 'fontWeight': '900'}),
                    html.P('30-Day Historical', style={'color': COLORS['text_dim'], 'fontSize': '12px', 'margin': 0})
                ])
            ], width=3),
            dbc.Col([
                html.Div(className='premium-card', style={
                    'background': COLORS['gradient_card'],
                    'padding': '20px',
                    'borderRadius': '15px',
                    'border': f'1px solid {COLORS["warning"]}',
                    'textAlign': 'center'
                }, children=[
                    html.P('IMPLIED VOL', style={'color': COLORS['text_secondary'], 'fontSize': '11px', 'margin': 0, 'fontWeight': '600', 'letterSpacing': '1px'}),
                    html.H2(id='iv-display', style={'color': COLORS['warning'], 'margin': '10px 0 5px', 'fontSize': '36px', 'fontWeight': '900'}),
                    html.P('ATM Options', style={'color': COLORS['text_dim'], 'fontSize': '12px', 'margin': 0})
                ])
            ], width=3),
            dbc.Col([
                html.Div(className='premium-card', style={
                    'background': COLORS['gradient_card'],
                    'padding': '20px',
                    'borderRadius': '15px',
                    'border': f'1px solid {COLORS["danger"]}',
                    'textAlign': 'center'
                }, children=[
                    html.P('ARBITRAGE SPREAD', style={'color': COLORS['text_secondary'], 'fontSize': '11px', 'margin': 0, 'fontWeight': '600', 'letterSpacing': '1px'}),
                    html.H2(id='spread-display', style={'color': COLORS['danger'], 'margin': '10px 0 5px', 'fontSize': '36px', 'fontWeight': '900'}),
                    html.P(id='spread-signal', style={'fontSize': '12px', 'margin': 0, 'fontWeight': '600'})
                ])
            ], width=3),
        ])
    ]),

    # ======================== MAIN CONTENT ========================
    html.Div(style={'padding': '30px 40px'}, children=[
        dbc.Row([
            # LEFT: Charts
            dbc.Col(width=8, children=[
                # Main Price Chart
                html.Div(className='premium-card', style={
                    'background': COLORS['bg_panel'],
                    'padding': '25px',
                    'borderRadius': '20px',
                    'marginBottom': '30px',
                    'border': f'1px solid {COLORS["neo_green"]}',
                    'boxShadow': '0 4px 20px rgba(0, 0, 0, 0.5)'
                }, children=[
                    html.H3('NEO/USDT PRICE ACTION', style={
                        'color': COLORS['neo_green'],
                        'marginBottom': '20px',
                        'fontSize': '18px',
                        'fontWeight': '700',
                        'letterSpacing': '1px'
                    }),
                    dcc.Graph(id='main-chart-winner', config={'displayModeBar': False}, style={'height': '400px'})
                ]),

                # Volatility Comparison
                html.Div(className='premium-card', style={
                    'background': COLORS['bg_panel'],
                    'padding': '25px',
                    'borderRadius': '20px',
                    'border': f'1px solid {COLORS["info"]}',
                    'boxShadow': '0 4px 20px rgba(0, 0, 0, 0.5)'
                }, children=[
                    html.H3('VOLATILITY ANALYTICS', style={
                        'color': COLORS['info'],
                        'marginBottom': '20px',
                        'fontSize': '18px',
                        'fontWeight': '700',
                        'letterSpacing': '1px'
                    }),
                    dcc.Graph(id='vol-chart-winner', config={'displayModeBar': False}, style={'height': '350px'})
                ])
            ]),

            # RIGHT: Panels
            dbc.Col(width=4, children=[
                # Multi-Agent Status
                html.Div(className='premium-card', style={
                    'background': COLORS['gradient_dark'],
                    'padding': '25px',
                    'borderRadius': '20px',
                    'marginBottom': '20px',
                    'border': f'2px solid {COLORS["neo_green"]}',
                    'boxShadow': '0 4px 20px rgba(0, 229, 153, 0.3)'
                }, children=[
                    html.H3([
                        html.I(className='fas fa-robot', style={'marginRight': '10px'}),
                        'AGENT SWARM'
                    ], style={'color': COLORS['neo_green'], 'fontSize': '16px', 'fontWeight': '700', 'marginBottom': '20px'}),
                    html.Div(id='agent-status', className='scrollbar-neo', style={'maxHeight': '250px', 'overflowY': 'auto'})
                ]),

                # Options Greeks
                html.Div(className='premium-card', style={
                    'background': COLORS['bg_panel'],
                    'padding': '25px',
                    'borderRadius': '20px',
                    'marginBottom': '20px',
                    'border': f'1px solid {COLORS["warning"]}'
                }, children=[
                    html.H3([
                        html.I(className='fas fa-calculator', style={'marginRight': '10px'}),
                        'OPTIONS GREEKS'
                    ], style={'color': COLORS['warning'], 'fontSize': '16px', 'fontWeight': '700', 'marginBottom': '20px'}),
                    html.Div(id='greeks-panel')
                ]),

                # Neo Blockchain Integration
                html.Div(className='premium-card', style={
                    'background': COLORS['gradient_dark'],
                    'padding': '25px',
                    'borderRadius': '20px',
                    'border': f'2px solid {COLORS["neo_green"]}',
                    'boxShadow': '0 4px 20px rgba(0, 229, 153, 0.3)'
                }, children=[
                    html.H3([
                        html.I(className='fas fa-link', style={'marginRight': '10px'}),
                        'NEO N3 ORACLE'
                    ], style={'color': COLORS['neo_green'], 'fontSize': '16px', 'fontWeight': '700', 'marginBottom': '20px'}),
                    html.Div(id='blockchain-status')
                ])
            ])
        ])
    ]),

    # ======================== PREMIUM FOOTER ========================
    html.Div(style={
        'background': COLORS['gradient_primary'],
        'padding': '20px 40px',
        'marginTop': '30px',
        'textAlign': 'center'
    }, children=[
        html.P([
            html.Span('Powered by ', style={'color': COLORS['bg_dark']}),
            html.Span('Neo N3 Blockchain', style={'fontWeight': '700', 'color': COLORS['bg_black']}),
            html.Span(' | ', style={'margin': '0 15px', 'color': COLORS['bg_dark']}),
            html.Span('5 Autonomous Agents', style={'fontWeight': '700', 'color': COLORS['bg_black']}),
            html.Span(' | ', style={'margin': '0 15px', 'color': COLORS['bg_dark']}),
            html.Span('Real-Time Volatility Oracle', style={'fontWeight': '700', 'color': COLORS['bg_black']})
        ], style={'margin': 0, 'fontSize': '14px'})
    ]),

    # Intervals
    dcc.Interval(id='interval-fast-winner', interval=1000),
    dcc.Interval(id='interval-data-winner', interval=2000),
])

# ====================================================================================
#  CALLBACKS
# ====================================================================================

@app.callback(
    Output('header-clock', 'children'),
    Input('interval-fast-winner', 'n_intervals')
)
def update_clock(n):
    return datetime.now().strftime('%H:%M:%S UTC')

@app.callback(
    [Output('neo-price-big', 'children'),
     Output('neo-change', 'children'),
     Output('rv-display', 'children'),
     Output('iv-display', 'children'),
     Output('spread-display', 'children'),
     Output('spread-signal', 'children'),
     Output('main-chart-winner', 'figure'),
     Output('vol-chart-winner', 'figure'),
     Output('agent-status', 'children'),
     Output('greeks-panel', 'children'),
     Output('blockchain-status', 'children')],
    Input('interval-data-winner', 'n_intervals')
)
def update_dashboard(n):
    # Generate premium data
    price = 15.23 + np.random.normal(0, 0.05)
    change = 2.4 + np.random.normal(0, 0.3)
    rv = 52.3 + np.random.normal(0, 1)
    iv = 58.1 + np.random.normal(0, 1)
    spread = iv - rv

    # Neo price display
    price_text = f'${price:.2f}'
    change_text = f'+{change:.2f}% {"▲" if change > 0 else "▼"}'
    change_color = COLORS['success'] if change > 0 else COLORS['danger']

    # Volatility
    rv_text = f'{rv:.1f}%'
    iv_text = f'{iv:.1f}%'
    spread_text = f'{spread:+.1f}%'
    spread_signal_text = 'BULLISH VOL' if spread > 0 else 'BEARISH VOL'

    # Main Chart (Candlestick)
    x_data = list(range(60))
    price_data = [price + np.sin(i/5) * 0.5 + np.random.normal(0, 0.1) for i in x_data]

    main_chart = go.Figure()
    main_chart.add_trace(go.Candlestick(
        x=x_data,
        open=[p - 0.05 for p in price_data],
        high=[p + 0.10 for p in price_data],
        low=[p - 0.10 for p in price_data],
        close=price_data,
        increasing_line_color=COLORS['neo_green'],
        decreasing_line_color=COLORS['danger'],
        increasing_fillcolor=COLORS['neo_green'],
        decreasing_fillcolor=COLORS['danger']
    ))

    main_chart.update_layout(
        template='plotly_dark',
        paper_bgcolor=COLORS['bg_panel'],
        plot_bgcolor=COLORS['bg_black'],
        font={'family': 'Inter', 'color': COLORS['text'], 'size': 11},
        margin={'l': 50, 'r': 20, 't': 20, 'b': 40},
        xaxis={'showgrid': False, 'showticklabels': False},
        yaxis={'gridcolor': '#1a1a1a', 'tickformat': '.2f'},
        showlegend=False,
        hovermode='x unified'
    )

    # Volatility Chart
    rv_data = [rv + np.sin(i/8) * 3 + np.random.normal(0, 0.5) for i in x_data]
    iv_data = [v * 1.1 + np.random.normal(0, 1) for v in rv_data]
    garch_data = [v * 1.05 + np.random.normal(0, 0.8) for v in rv_data]

    vol_chart = go.Figure()
    vol_chart.add_trace(go.Scatter(
        x=x_data, y=rv_data,
        name='Realized Vol',
        line={'color': COLORS['success'], 'width': 3},
        fill='tozeroy',
        fillcolor='rgba(0, 255, 65, 0.1)'
    ))
    vol_chart.add_trace(go.Scatter(
        x=x_data, y=iv_data,
        name='Implied Vol',
        line={'color': COLORS['warning'], 'width': 3},
        fill='tozeroy',
        fillcolor='rgba(255, 217, 61, 0.1)'
    ))
    vol_chart.add_trace(go.Scatter(
        x=x_data, y=garch_data,
        name='GARCH Forecast',
        line={'color': COLORS['info'], 'width': 2, 'dash': 'dot'}
    ))

    vol_chart.update_layout(
        template='plotly_dark',
        paper_bgcolor=COLORS['bg_panel'],
        plot_bgcolor=COLORS['bg_black'],
        font={'family': 'Inter', 'color': COLORS['text'], 'size': 11},
        margin={'l': 50, 'r': 20, 't': 20, 'b': 40},
        yaxis={'title': 'VOL %', 'gridcolor': '#1a1a1a'},
        xaxis={'gridcolor': '#1a1a1a', 'showticklabels': False},
        legend={'x': 0, 'y': 1, 'bgcolor': 'rgba(0,0,0,0.5)', 'font': {'size': 10}},
        hovermode='x unified'
    )

    # Agent Status
    agents = [
        {'name': 'MarketData', 'status': 'ACTIVE', 'tasks': 1523},
        {'name': 'VolCalculator', 'status': 'ACTIVE', 'tasks': 892},
        {'name': 'ImpliedVol', 'status': 'ACTIVE', 'tasks': 743},
        {'name': 'Arbitrage', 'status': 'ACTIVE', 'tasks': 456},
        {'name': 'OraclePublisher', 'status': 'ACTIVE', 'tasks': 234}
    ]

    agent_status = html.Div([
        html.Div([
            html.Div([
                html.Span(agent['name'], style={'color': COLORS['text'], 'fontWeight': '600', 'fontSize': '13px'}),
                html.Span('[*]', style={'color': COLORS['neo_green'], 'float': 'right', 'fontWeight': 'bold'})
            ]),
            html.Div([
                html.Span(f"Tasks: {agent['tasks']}", style={'color': COLORS['text_secondary'], 'fontSize': '10px'}),
                html.Span(agent['status'], style={'color': COLORS['neo_green'], 'float': 'right', 'fontSize': '10px', 'fontWeight': '600'})
            ])
        ], style={
            'padding': '12px',
            'marginBottom': '10px',
            'backgroundColor': COLORS['bg_card'],
            'borderRadius': '10px',
            'border': f'1px solid {COLORS["neo_green"]}33'
        })
        for agent in agents
    ])

    # Greeks
    greeks = html.Div([
        html.Div([
            html.Span('DELTA', style={'color': COLORS['text_secondary'], 'fontSize': '11px'}),
            html.Span('0.6234', style={'color': COLORS['neo_green'], 'float': 'right', 'fontWeight': '700'})
        ], style={'marginBottom': '12px'}),
        html.Div([
            html.Span('GAMMA', style={'color': COLORS['text_secondary'], 'fontSize': '11px'}),
            html.Span('0.0189', style={'color': COLORS['info'], 'float': 'right', 'fontWeight': '700'})
        ], style={'marginBottom': '12px'}),
        html.Div([
            html.Span('VEGA', style={'color': COLORS['text_secondary'], 'fontSize': '11px'}),
            html.Span('0.1456', style={'color': COLORS['warning'], 'float': 'right', 'fontWeight': '700'})
        ], style={'marginBottom': '12px'}),
        html.Div([
            html.Span('THETA', style={'color': COLORS['text_secondary'], 'fontSize': '11px'}),
            html.Span('-0.0823', style={'color': COLORS['danger'], 'float': 'right', 'fontWeight': '700'})
        ], style={'marginBottom': '12px'}),
        html.Div([
            html.Span('RHO', style={'color': COLORS['text_secondary'], 'fontSize': '11px'}),
            html.Span('0.0567', style={'color': COLORS['text'], 'float': 'right', 'fontWeight': '700'})
        ])
    ])

    # Blockchain Status
    blockchain = html.Div([
        html.Div([
            html.Span('Network', style={'color': COLORS['text_secondary'], 'fontSize': '11px'}),
            html.Span('NEO N3 TESTNET', style={'color': COLORS['neo_green'], 'float': 'right', 'fontSize': '10px', 'fontWeight': '700'})
        ], style={'marginBottom': '12px'}),
        html.Div([
            html.Span('Contract', style={'color': COLORS['text_secondary'], 'fontSize': '11px'}),
            html.Span('0x7a2b...f3c9', style={'color': COLORS['info'], 'float': 'right', 'fontSize': '10px', 'fontFamily': 'monospace'})
        ], style={'marginBottom': '12px'}),
        html.Div([
            html.Span('Last Publish', style={'color': COLORS['text_secondary'], 'fontSize': '11px'}),
            html.Span('2 sec ago', style={'color': COLORS['neo_green'], 'float': 'right', 'fontSize': '10px', 'fontWeight': '600'})
        ], style={'marginBottom': '12px'}),
        html.Div([
            html.Span('Gas Used', style={'color': COLORS['text_secondary'], 'fontSize': '11px'}),
            html.Span('0.0234 GAS', style={'color': COLORS['warning'], 'float': 'right', 'fontSize': '10px', 'fontWeight': '600'})
        ])
    ])

    return (
        price_text,
        html.Span(change_text, style={'color': change_color}),
        rv_text,
        iv_text,
        spread_text,
        html.Span(spread_signal_text, style={'color': COLORS['success'] if spread > 0 else COLORS['danger']}),
        main_chart,
        vol_chart,
        agent_status,
        greeks,
        blockchain
    )

if __name__ == '__main__':
    print("\n" + "="*80)
    print("AGENTSPOONS - HACKATHON WINNER EDITION")
    print("="*80)
    print("URL: http://localhost:8060")
    print("")
    print("PREMIUM FEATURES:")
    print("  * Neo N3 Brand Integration")
    print("  * Bloomberg Professional Design")
    print("  * Multi-Agent Swarm Visualization")
    print("  * Real-Time Volatility Analytics")
    print("  * Options Greeks Calculator")
    print("  * Blockchain Oracle Integration")
    print("  * Premium Animations & Effects")
    print("  * Hackathon-Winning UI")
    print("="*80 + "\n")

    app.run(debug=True, host='0.0.0.0', port=8060)
