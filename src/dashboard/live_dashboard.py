"""
Live Dashboard - Connected to Real Data
"""
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from datetime import datetime
import json
from pathlib import Path

# Initialize app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Colors
COLORS = {
    'primary': '#6366f1',
    'success': '#10b981',
    'danger': '#ef4444',
    'warning': '#f59e0b',
    'info': '#3b82f6',
    'dark': '#0f172a',
    'card': '#1e293b',
    'border': '#334155'
}


def load_live_data():
    """Load live data from file"""
    try:
        data_file = Path('data/live_data.json')
        if data_file.exists():
            with open(data_file, 'r') as f:
                return json.load(f)
    except Exception:
        pass

    # Return dummy data if file doesn't exist
    return {
        'timestamp': datetime.now().isoformat(),
        'price': 15.23,
        'price_change': 0,
        'realized_vol': 0.52,
        'implied_vol': 0.58,
        'spread': 0.06,
        'garch_forecast': 0.54,
        'history': {
            'timestamps': [],
            'prices': [],
            'rv': [],
            'iv': []
        }
    }


app.layout = dbc.Container(
    fluid=True,
    style={
        'background': f'linear-gradient(135deg, {COLORS["dark"]} 0%, #1e1b4b 100%)',
        'minHeight': '100vh',
        'padding': '20px'
    },
    children=[
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            html.H3(
                                [
                                    html.Span('🥄 ', style={'fontSize': '32px'}),
                                    html.Span(
                                        'AgentSpoons',
                                        style={
                                            'background': f'linear-gradient(135deg, {COLORS["primary"]}, #8b5cf6)',
                                            'WebkitBackgroundClip': 'text',
                                            'WebkitTextFillColor': 'transparent',
                                            'fontWeight': '700'
                                        }
                                    ),
                                    html.Span(
                                        ' | Live Volatility Oracle',
                                        style={
                                            'color': '#94a3b8',
                                            'fontSize': '16px',
                                            'marginLeft': '15px'
                                        }
                                    )
                                ],
                                style={'margin': '0', 'display': 'inline-block'}
                            ),
                            html.Div(
                                [
                                    html.Span('●', style={'color': COLORS['success'], 'fontSize': '20px'}),
                                    html.Span(
                                        ' LIVE',
                                        style={
                                            'color': COLORS['success'],
                                            'fontSize': '12px',
                                            'fontWeight': '600',
                                            'marginLeft': '5px'
                                        }
                                    )
                                ],
                                style={'float': 'right', 'marginTop': '10px'}
                            )
                        ],
                        style={
                            'backgroundColor': COLORS['card'],
                            'padding': '20px 30px',
                            'borderRadius': '12px',
                            'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.3)',
                            'marginBottom': '20px'
                        }
                    ),
                    width=12
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.P('NEO Price', style={'color': '#94a3b8', 'fontSize': '14px', 'margin': '0 0 10px 0'}),
                                html.H2(id='price', style={'color': 'white', 'fontSize': '32px', 'fontWeight': '700', 'margin': '0'}),
                                html.Div(id='price-change', style={'marginTop': '10px'})
                            ]
                        ),
                        style={'backgroundColor': COLORS['card'], 'border': 'none', 'borderRadius': '12px', 'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.3)'}
                    ),
                    width=3
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.P('Realized Volatility', style={'color': '#94a3b8', 'fontSize': '14px', 'margin': '0 0 10px 0'}),
                                html.H2(id='rv', style={'color': COLORS['success'], 'fontSize': '32px', 'fontWeight': '700', 'margin': '0'}),
                                html.P('GARCH Model', style={'color': '#64748b', 'fontSize': '12px', 'margin': '10px 0 0 0'})
                            ]
                        ),
                        style={'backgroundColor': COLORS['card'], 'border': 'none', 'borderRadius': '12px', 'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.3)'}
                    ),
                    width=3
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.P('Implied Volatility', style={'color': '#94a3b8', 'fontSize': '14px', 'margin': '0 0 10px 0'}),
                                html.H2(id='iv', style={'color': COLORS['warning'], 'fontSize': '32px', 'fontWeight': '700', 'margin': '0'}),
                                html.P('Options Market', style={'color': '#64748b', 'fontSize': '12px', 'margin': '10px 0 0 0'})
                            ]
                        ),
                        style={'backgroundColor': COLORS['card'], 'border': 'none', 'borderRadius': '12px', 'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.3)'}
                    ),
                    width=3
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.P('IV-RV Spread', style={'color': '#94a3b8', 'fontSize': '14px', 'margin': '0 0 10px 0'}),
                                html.H2(id='spread', style={'color': COLORS['info'], 'fontSize': '32px', 'fontWeight': '700', 'margin': '0'}),
                                html.P(id='signal', style={'fontSize': '12px', 'margin': '10px 0 0 0', 'fontWeight': '600'})
                            ]
                        ),
                        style={'backgroundColor': COLORS['card'], 'border': 'none', 'borderRadius': '12px', 'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.3)'}
                    ),
                    width=3
                )
            ],
            style={'marginBottom': '20px'}
        ),
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader(
                            'Volatility Over Time',
                            style={'backgroundColor': COLORS['card'], 'color': 'white', 'borderBottom': f'1px solid {COLORS["border"]}'}
                        ),
                        dbc.CardBody(
                            dcc.Graph(id='chart', config={'displayModeBar': False}, style={'height': '400px'}),
                            style={'padding': '20px', 'backgroundColor': COLORS['card']}
                        )
                    ],
                    style={'backgroundColor': COLORS['card'], 'border': 'none', 'borderRadius': '12px', 'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.3)'}
                ),
                width=12
            )
        ),
        dcc.Interval(id='interval', interval=2000, n_intervals=0)
    ]
)


@app.callback(
    [
        Output('price', 'children'),
        Output('price-change', 'children'),
        Output('rv', 'children'),
        Output('iv', 'children'),
        Output('spread', 'children'),
        Output('signal', 'children'),
        Output('signal', 'style'),
        Output('chart', 'figure')
    ],
    Input('interval', 'n_intervals')
)
def update(_n):
    data = load_live_data()

    price = f"${data['price']:.2f}"
    price_chg = data['price_change']
    price_change_html = html.Span(
        f"{'▲' if price_chg > 0 else '▼'} {abs(price_chg):.2f}%",
        style={'color': COLORS['success'] if price_chg > 0 else COLORS['danger'], 'fontSize': '14px', 'fontWeight': '600'}
    )

    rv_value = data['realized_vol']
    iv_value = data['implied_vol']
    spread_value = data['spread']

    rv = f"{rv_value:.2%}"
    iv = f"{iv_value:.2%}"
    spread = f"{spread_value:.2%}"

    if spread_value > 0.08:
        signal_text = '🔥 Strong Arbitrage'
        signal_color = COLORS['success']
    elif spread_value > 0.05:
        signal_text = '💡 Moderate Signal'
        signal_color = COLORS['warning']
    else:
        signal_text = '📊 Normal Range'
        signal_color = '#64748b'

    history = data.get('history', {})
    timestamps = history.get('timestamps', [])
    rv_series = history.get('rv', [])
    iv_series = history.get('iv', [])

    figure = go.Figure()

    if rv_series:
        figure.add_trace(
            go.Scatter(
                x=timestamps,
                y=[vol * 100 for vol in rv_series],
                name='Realized Vol',
                line={'color': COLORS['success'], 'width': 3},
                fill='tozeroy',
                fillcolor='rgba(16, 185, 129, 0.1)'
            )
        )

    if iv_series:
        figure.add_trace(
            go.Scatter(
                x=timestamps,
                y=[vol * 100 for vol in iv_series],
                name='Implied Vol',
                line={'color': COLORS['warning'], 'width': 3},
                fill='tozeroy',
                fillcolor='rgba(245, 158, 11, 0.1)'
            )
        )

    figure.update_layout(
        template='plotly_dark',
        paper_bgcolor=COLORS['card'],
        plot_bgcolor=COLORS['card'],
        margin={'l': 40, 'r': 20, 't': 20, 'b': 40},
        font={'family': 'system-ui', 'size': 12},
        yaxis={'title': 'Volatility %', 'gridcolor': 'rgba(255, 255, 255, 0.1)'},
        xaxis={'gridcolor': 'rgba(255, 255, 255, 0.1)', 'showticklabels': False},
        legend={'orientation': 'h', 'yanchor': 'bottom', 'y': 1.02, 'xanchor': 'right', 'x': 1},
        hovermode='x unified'
    )

    return (
        price,
        price_change_html,
        rv,
        iv,
        spread,
        signal_text,
        {'color': signal_color},
        figure
    )


if __name__ == '__main__':
    print('=' * 70)
    print('🎨 LIVE DASHBOARD WITH REAL DATA')
    print('=' * 70)
    print('🌐 Dashboard: http://localhost:8080')
    print('📊 Reading from: data/live_data.json')
    print('💡 Start data generator in another terminal:')
    print('   python src/data_generator.py')
    print('=' * 70)
    app.run(debug=True, port=8080, host='0.0.0.0')
