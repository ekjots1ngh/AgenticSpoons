"""
Bloomberg Terminal-Style Professional Layout
Multi-panel design with professional features
"""
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from datetime import datetime
import numpy as np

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

# Bloomberg-style color scheme
COLORS = {
    'bg_dark': '#0a0a0a',
    'bg_panel': '#1a1a1a',
    'orange': '#ff8c00',
    'green': '#00ff00',
    'red': '#ff0000',
    'blue': '#00bfff',
    'yellow': '#ffff00',
    'text': '#e0e0e0'
}

app.layout = dbc.Container(fluid=True, style={
    'backgroundColor': COLORS['bg_dark'],
    'height': '100vh',
    'padding': '0',
    'overflow': 'hidden'
}, children=[
    
    # Top Bar
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Span('🥄 AGENTSPOONS', style={
                    'color': COLORS['orange'],
                    'fontSize': '20px',
                    'fontWeight': 'bold',
                    'fontFamily': 'monospace'
                }),
                html.Span(' | ', style={'color': COLORS['text'], 'margin': '0 10px'}),
                html.Span('NEO N3 VOLATILITY ORACLE', style={
                    'color': COLORS['text'],
                    'fontSize': '14px',
                    'fontFamily': 'monospace'
                }),
                html.Span(id='live-clock', style={
                    'color': COLORS['green'],
                    'fontSize': '14px',
                    'fontFamily': 'monospace',
                    'float': 'right',
                    'marginRight': '20px'
                })
            ], style={'padding': '10px 20px', 'backgroundColor': '#000'})
        ], width=12)
    ], style={'margin': '0'}),
    
    # Main Content - 3 columns
    dbc.Row([
        
        # LEFT PANEL
        dbc.Col([
            dbc.Card([
                dbc.CardHeader('WATCHLIST', style={
                    'backgroundColor': COLORS['bg_panel'],
                    'color': COLORS['orange'],
                    'fontFamily': 'monospace',
                    'fontSize': '12px',
                    'fontWeight': 'bold',
                    'padding': '5px 10px'
                }),
                dbc.CardBody([
                    html.Div(id='watchlist-table', style={'fontFamily': 'monospace', 'fontSize': '11px'})
                ], style={'padding': '5px', 'backgroundColor': COLORS['bg_panel']})
            ], style={'marginBottom': '10px'}),
            
            dbc.Card([
                dbc.CardHeader('MARKET STATS', style={
                    'backgroundColor': COLORS['bg_panel'],
                    'color': COLORS['orange'],
                    'fontFamily': 'monospace',
                    'fontSize': '12px',
                    'fontWeight': 'bold',
                    'padding': '5px 10px'
                }),
                dbc.CardBody([
                    html.Div(id='market-stats', style={'fontFamily': 'monospace', 'fontSize': '11px'})
                ], style={'padding': '10px', 'backgroundColor': COLORS['bg_panel']})
            ], style={'marginBottom': '10px'}),
            
        ], width=3, style={'padding': '10px 5px'}),
        
        # CENTER PANEL
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.Span('NEO/USDT', style={'color': COLORS['orange'], 'fontWeight': 'bold'}),
                    html.Span(id='current-price', style={'color': COLORS['green'], 'marginLeft': '20px'}),
                ], style={
                    'backgroundColor': COLORS['bg_panel'],
                    'color': COLORS['text'],
                    'fontFamily': 'monospace',
                    'fontSize': '14px',
                    'padding': '5px 10px'
                }),
                dbc.CardBody([
                    dcc.Graph(id='main-chart', config={'displayModeBar': False}, style={'height': '350px'})
                ], style={'padding': '5px', 'backgroundColor': COLORS['bg_panel']})
            ], style={'marginBottom': '10px'}),
            
            dbc.Card([
                dbc.CardHeader('VOLATILITY ANALYSIS', style={
                    'backgroundColor': COLORS['bg_panel'],
                    'color': COLORS['orange'],
                    'fontFamily': 'monospace',
                    'fontSize': '12px',
                    'fontWeight': 'bold',
                    'padding': '5px 10px'
                }),
                dbc.CardBody([
                    dcc.Graph(id='vol-chart', config={'displayModeBar': False}, style={'height': '250px'})
                ], style={'padding': '5px', 'backgroundColor': COLORS['bg_panel']})
            ])
            
        ], width=6, style={'padding': '10px 5px'}),
        
        # RIGHT PANEL
        dbc.Col([
            dbc.Card([
                dbc.CardHeader('OPTIONS CALCULATOR', style={
                    'backgroundColor': COLORS['bg_panel'],
                    'color': COLORS['orange'],
                    'fontFamily': 'monospace',
                    'fontSize': '12px',
                    'fontWeight': 'bold',
                    'padding': '5px 10px'
                }),
                dbc.CardBody([
                    html.Div(id='option-display', style={'fontFamily': 'monospace', 'fontSize': '11px', 'color': COLORS['green']})
                ], style={'padding': '10px', 'backgroundColor': COLORS['bg_panel']})
            ], style={'marginBottom': '10px'}),
            
            dbc.Card([
                dbc.CardHeader('GREEKS', style={
                    'backgroundColor': COLORS['bg_panel'],
                    'color': COLORS['orange'],
                    'fontFamily': 'monospace',
                    'fontSize': '12px',
                    'fontWeight': 'bold',
                    'padding': '5px 10px'
                }),
                dbc.CardBody([
                    html.Div(id='greeks-display', style={'fontFamily': 'monospace', 'fontSize': '11px'})
                ], style={'padding': '10px', 'backgroundColor': COLORS['bg_panel']})
            ]),
            
        ], width=3, style={'padding': '10px 5px'}),
        
    ], style={'height': 'calc(100vh - 60px)', 'margin': '0'}),
    
    # Bottom Status Bar
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Span('🟢 CONNECTED', style={'color': COLORS['green'], 'fontSize': '10px', 'marginRight': '20px'}),
                html.Span('LAST UPDATE: ', style={'color': COLORS['text'], 'fontSize': '10px'}),
                html.Span(id='last-update', style={'color': COLORS['blue'], 'fontSize': '10px', 'marginRight': '20px'}),
                html.Span(id='neo-status', style={'color': COLORS['yellow'], 'fontSize': '10px'})
            ], style={'padding': '5px 20px', 'backgroundColor': '#000'})
        ], width=12)
    ], style={'margin': '0'}),
    
    dcc.Interval(id='interval-update', interval=2000, n_intervals=0),
])

@app.callback(
    [Output('live-clock', 'children'),
     Output('last-update', 'children'),
     Output('watchlist-table', 'children'),
     Output('market-stats', 'children'),
     Output('main-chart', 'figure'),
     Output('vol-chart', 'figure'),
     Output('current-price', 'children'),
     Output('neo-status', 'children'),
     Output('option-display', 'children'),
     Output('greeks-display', 'children')],
    [Input('interval-update', 'n_intervals')]
)
def update_dashboard(n):
    current_time = datetime.now().strftime('%H:%M:%S')
    
    # Watchlist
    watchlist = html.Table([
        html.Thead(html.Tr([
            html.Th('PAIR', style={'color': COLORS['orange']}),
            html.Th('PRICE', style={'color': COLORS['orange']}),
            html.Th('CHG%', style={'color': COLORS['orange']}),
            html.Th('VOL', style={'color': COLORS['orange']})
        ])),
        html.Tbody([
            html.Tr([
                html.Td('NEO/USDT'),
                html.Td('$15.23', style={'color': COLORS['green']}),
                html.Td('+2.4%', style={'color': COLORS['green']}),
                html.Td('52%', style={'color': COLORS['yellow']})
            ]),
            html.Tr([
                html.Td('GAS/USDT'),
                html.Td('$5.12', style={'color': COLORS['red']}),
                html.Td('-1.2%', style={'color': COLORS['red']}),
                html.Td('48%', style={'color': COLORS['yellow']})
            ]),
        ])
    ], style={'width': '100%', 'color': COLORS['text']})
    
    # Market stats
    stats = html.Div([
        html.Div([
            html.Span('24H HIGH: ', style={'color': COLORS['text']}),
            html.Span('$15.67', style={'color': COLORS['green'], 'fontWeight': 'bold'})
        ]),
        html.Div([
            html.Span('24H LOW: ', style={'color': COLORS['text']}),
            html.Span('$14.89', style={'color': COLORS['red'], 'fontWeight': 'bold'})
        ]),
        html.Div([
            html.Span('RV: ', style={'color': COLORS['text']}),
            html.Span('52.3%', style={'color': COLORS['yellow'], 'fontWeight': 'bold'})
        ]),
        html.Div([
            html.Span('IV: ', style={'color': COLORS['text']}),
            html.Span('58.1%', style={'color': COLORS['orange'], 'fontWeight': 'bold'})
        ]),
    ])
    
    # Charts
    x_data = list(range(100))
    price_data = [15 + np.sin(i/10) + np.random.normal(0, 0.1) for i in x_data]
    
    main_chart = {
        'data': [
            go.Candlestick(
                x=x_data,
                open=[p-0.1 for p in price_data],
                high=[p+0.15 for p in price_data],
                low=[p-0.15 for p in price_data],
                close=price_data,
                increasing_line_color=COLORS['green'],
                decreasing_line_color=COLORS['red']
            )
        ],
        'layout': {
            'template': 'plotly_dark',
            'paper_bgcolor': COLORS['bg_panel'],
            'plot_bgcolor': COLORS['bg_panel'],
            'margin': {'l': 40, 'r': 10, 't': 10, 'b': 30},
            'xaxis': {'showgrid': False, 'showticklabels': False},
            'yaxis': {'gridcolor': '#333', 'tickfont': {'size': 10}},
            'font': {'family': 'monospace'}
        }
    }
    
    vol_data = [50 + np.random.normal(0, 2) for _ in range(100)]
    iv_data = [v * 1.1 + np.random.normal(0, 1) for v in vol_data]
    
    vol_chart = {
        'data': [
            go.Scatter(x=x_data, y=vol_data, name='RV', line={'color': COLORS['green'], 'width': 2}),
            go.Scatter(x=x_data, y=iv_data, name='IV', line={'color': COLORS['orange'], 'width': 2})
        ],
        'layout': {
            'template': 'plotly_dark',
            'paper_bgcolor': COLORS['bg_panel'],
            'plot_bgcolor': COLORS['bg_panel'],
            'margin': {'l': 40, 'r': 10, 't': 10, 'b': 30},
            'xaxis': {'showgrid': False, 'showticklabels': False},
            'yaxis': {'gridcolor': '#333', 'title': 'VOL %'},
            'legend': {'x': 0, 'y': 1, 'font': {'size': 10}},
            'font': {'family': 'monospace'}
        }
    }
    
    # Option calc
    option_display = html.Div([
        html.Div('CALL $100 30D', style={'color': COLORS['orange'], 'fontWeight': 'bold', 'marginBottom': '10px'}),
        html.Div([
            html.Span('PRICE: ', style={'color': COLORS['text']}),
            html.Span('$2.45', style={'color': COLORS['green'], 'fontSize': '16px', 'fontWeight': 'bold'})
        ])
    ])
    
    greeks = html.Div([
        html.Div(['DELTA: ', html.Span('0.6500', style={'color': COLORS['green']})]),
        html.Div(['GAMMA: ', html.Span('0.0200', style={'color': COLORS['blue']})]),
        html.Div(['VEGA: ', html.Span('0.1500', style={'color': COLORS['yellow']})]),
        html.Div(['THETA: ', html.Span('-0.0800', style={'color': COLORS['red']})]),
    ])
    
    return (
        current_time,
        current_time,
        watchlist,
        stats,
        main_chart,
        vol_chart,
        '$15.23 ▲',
        'NEO TESTNET | CONTRACT: 0x7a2b...f3c9',
        option_display,
        greeks
    )

if __name__ == '__main__':
    print("="*70)
    print("💼 BLOOMBERG-STYLE TERMINAL")
    print("="*70)
    print("🌐 URL: http://localhost:8060")
    print("💡 Professional institutional interface")
    print("="*70)
    app.run_server(debug=False, port=8060)
