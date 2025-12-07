"""Bloomberg terminal inspired dashboard with richer layout and analytics."""
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from datetime import datetime
import numpy as np


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])


# Visual identity approximating a Bloomberg terminal
COLORS = {
    'bg_dark': '#050505',
    'bg_panel': '#111111',
    'grid': '#2a2a2a',
    'orange': '#ff9f1c',
    'green': '#4cd964',
    'red': '#ff3b30',
    'blue': '#3a99d8',
    'yellow': '#ffe066',
    'text': '#d7d7d7',
    'muted': '#808080'
}
FONT_FAMILY = 'IBM Plex Mono, Consolas, monospace'


def card_header(title: str) -> dbc.CardHeader:
    return dbc.CardHeader(
        title.upper(),
        style={
            'backgroundColor': COLORS['bg_panel'],
            'color': COLORS['orange'],
            'fontFamily': FONT_FAMILY,
            'fontSize': '11px',
            'letterSpacing': '1px',
            'padding': '6px 12px'
        }
    )


app.layout = dbc.Container(
    fluid=True,
    style={
        'backgroundColor': COLORS['bg_dark'],
        'height': '100vh',
        'padding': '0',
        'overflow': 'hidden'
    },
    children=[
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.Span(
                            '🥄 AGENTSPOONS',
                            style={
                                'color': COLORS['orange'],
                                'fontSize': '22px',
                                'fontWeight': 'bold',
                                'fontFamily': FONT_FAMILY
                            }
                        ),
                        html.Span(
                            ' | NEO N3 VOLATILITY TERMINAL',
                            style={
                                'color': COLORS['text'],
                                'fontSize': '14px',
                                'marginLeft': '12px',
                                'fontFamily': FONT_FAMILY
                            }
                        ),
                        html.Span(
                            id='live-clock',
                            style={
                                'color': COLORS['green'],
                                'fontSize': '14px',
                                'fontFamily': FONT_FAMILY,
                                'float': 'right'
                            }
                        )
                    ],
                    style={'padding': '12px 18px', 'backgroundColor': '#000000'}
                ),
                width=12
            ),
            style={'margin': '0'}
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                card_header('Watchlist'),
                                dbc.CardBody(
                                    html.Div(id='watchlist-table'),
                                    style={'backgroundColor': COLORS['bg_panel'], 'padding': '8px'}
                                )
                            ],
                            style={'marginBottom': '10px', 'backgroundColor': COLORS['bg_panel']}
                        ),
                        dbc.Card(
                            [
                                card_header('Alerts Monitor'),
                                dbc.CardBody(
                                    html.Div(id='alerts-table'),
                                    style={'backgroundColor': COLORS['bg_panel'], 'padding': '8px'}
                                )
                            ],
                            style={'marginBottom': '10px', 'backgroundColor': COLORS['bg_panel']}
                        ),
                        dbc.Card(
                            [
                                card_header('Risk & Network Pulse'),
                                dbc.CardBody(
                                    html.Div(id='risk-indicators'),
                                    style={'backgroundColor': COLORS['bg_panel'], 'padding': '12px'}
                                )
                            ],
                            style={'marginBottom': '10px', 'backgroundColor': COLORS['bg_panel']}
                        ),
                        dbc.Card(
                            [
                                card_header('Newswire'),
                                dbc.CardBody(
                                    html.Div(id='news-feed', style={'maxHeight': '240px', 'overflowY': 'auto'}),
                                    style={'backgroundColor': COLORS['bg_panel'], 'padding': '8px'}
                                )
                            ],
                            style={'backgroundColor': COLORS['bg_panel']}
                        )
                    ],
                    width=3,
                    style={'padding': '10px 6px'}
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    [
                                        html.Span(
                                            'NEO / USDT',
                                            style={
                                                'color': COLORS['orange'],
                                                'fontFamily': FONT_FAMILY,
                                                'fontWeight': 'bold'
                                            }
                                        ),
                                        html.Span(
                                            id='current-price',
                                            style={
                                                'color': COLORS['green'],
                                                'marginLeft': '18px',
                                                'fontFamily': FONT_FAMILY
                                            }
                                        ),
                                        html.Span(
                                            id='market-stats',
                                            style={
                                                'color': COLORS['text'],
                                                'fontFamily': FONT_FAMILY,
                                                'float': 'right',
                                                'fontSize': '12px'
                                            }
                                        )
                                    ],
                                    style={
                                        'backgroundColor': COLORS['bg_panel'],
                                        'padding': '8px 12px'
                                    }
                                ),
                                dbc.CardBody(
                                    dcc.Graph(id='main-chart', config={'displayModeBar': False}, style={'height': '360px'}),
                                    style={'backgroundColor': COLORS['bg_panel'], 'padding': '4px'}
                                )
                            ],
                            style={'marginBottom': '10px', 'backgroundColor': COLORS['bg_panel']}
                        ),
                        dbc.Card(
                            [
                                card_header('Volatility Intelligence'),
                                dbc.CardBody(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dcc.Graph(
                                                        id='vol-comparison-chart',
                                                        config={'displayModeBar': False},
                                                        style={'height': '220px'}
                                                    ),
                                                    width=6
                                                ),
                                                dbc.Col(
                                                    dcc.Graph(
                                                        id='term-structure-chart',
                                                        config={'displayModeBar': False},
                                                        style={'height': '220px'}
                                                    ),
                                                    width=6
                                                )
                                            ],
                                            className='gx-2'
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dcc.Graph(
                                                        id='option-skew-chart',
                                                        config={'displayModeBar': False},
                                                        style={'height': '220px'}
                                                    ),
                                                    width=6
                                                ),
                                                dbc.Col(
                                                    dcc.Graph(
                                                        id='vol-heatmap',
                                                        config={'displayModeBar': False},
                                                        style={'height': '220px'}
                                                    ),
                                                    width=6
                                                )
                                            ],
                                            className='gx-2 mt-2'
                                        )
                                    ],
                                    style={'backgroundColor': COLORS['bg_panel'], 'padding': '4px 8px'}
                                )
                            ],
                            style={'backgroundColor': COLORS['bg_panel']}
                        )
                    ],
                    width=6,
                    style={'padding': '10px 6px'}
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                card_header('Options & Greeks'),
                                dbc.CardBody(
                                    [
                                        html.Div(id='option-display', style={'marginBottom': '12px'}),
                                        html.Div(id='greeks-display')
                                    ],
                                    style={'backgroundColor': COLORS['bg_panel'], 'padding': '10px'}
                                )
                            ],
                            style={'marginBottom': '10px', 'backgroundColor': COLORS['bg_panel']}
                        ),
                        dbc.Card(
                            [
                                card_header('Order Flow Depth'),
                                dbc.CardBody(
                                    dcc.Graph(id='order-book-chart', config={'displayModeBar': False}, style={'height': '220px'}),
                                    style={'backgroundColor': COLORS['bg_panel'], 'padding': '4px'}
                                )
                            ],
                            style={'marginBottom': '10px', 'backgroundColor': COLORS['bg_panel']}
                        ),
                        dbc.Card(
                            [
                                card_header('Liquidity by Venue'),
                                dbc.CardBody(
                                    dcc.Graph(id='liquidity-by-venue', config={'displayModeBar': False}, style={'height': '220px'}),
                                    style={'backgroundColor': COLORS['bg_panel'], 'padding': '4px'}
                                )
                            ],
                            style={'backgroundColor': COLORS['bg_panel']}
                        )
                    ],
                    width=3,
                    style={'padding': '10px 6px'}
                )
            ],
            style={'margin': '0'}
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.Span('🟢 ', style={'color': COLORS['green'], 'fontFamily': FONT_FAMILY}),
                        html.Span('LAST UPDATE: ', style={'color': COLORS['text'], 'fontFamily': FONT_FAMILY, 'fontSize': '11px'}),
                        html.Span(id='last-update', style={'color': COLORS['blue'], 'fontFamily': FONT_FAMILY, 'fontSize': '11px', 'marginRight': '18px'}),
                        html.Span(id='neo-status', style={'color': COLORS['yellow'], 'fontFamily': FONT_FAMILY, 'fontSize': '11px', 'marginRight': '18px'}),
                        html.Span(id='ticker-tape', style={'color': COLORS['text'], 'fontFamily': FONT_FAMILY, 'fontSize': '11px'})
                    ],
                    style={'padding': '6px 18px', 'backgroundColor': '#000000'}
                ),
                width=12
            ),
            style={'margin': '0'}
        ),
        dcc.Interval(id='interval-update', interval=2500, n_intervals=0)
    ]
)


@app.callback(
    [
        Output('live-clock', 'children'),
        Output('last-update', 'children'),
        Output('watchlist-table', 'children'),
        Output('market-stats', 'children'),
        Output('main-chart', 'figure'),
        Output('vol-comparison-chart', 'figure'),
        Output('term-structure-chart', 'figure'),
        Output('option-skew-chart', 'figure'),
        Output('vol-heatmap', 'figure'),
        Output('order-book-chart', 'figure'),
        Output('liquidity-by-venue', 'figure'),
        Output('alerts-table', 'children'),
        Output('news-feed', 'children'),
        Output('current-price', 'children'),
        Output('neo-status', 'children'),
        Output('option-display', 'children'),
        Output('greeks-display', 'children'),
        Output('risk-indicators', 'children'),
        Output('ticker-tape', 'children')
    ],
    Input('interval-update', 'n_intervals')
)
def update_dashboard(n):
    n = n or 0
    clock = datetime.utcnow()
    rng = np.random.default_rng(n + 42)

    # Synthetic yet structured watchlist (closer to an actual terminal sheet)
    base_pairs = [
        ('NEO/USDT', 15.35, 0.024, 0.58, 0.52, 1240000),
        ('GAS/USDT', 5.08, -0.011, 0.47, 0.44, 840000),
        ('FLM/USDT', 0.184, 0.019, 0.71, 0.66, 460000),
        ('BNEO/USDT', 18.95, -0.006, 0.62, 0.59, 310000),
        ('USDN/USDT', 0.994, 0.001, 0.09, 0.12, 1540000)
    ]
    watch_rows = []
    for name, price, change, iv, rv, volume in base_pairs:
        price_variation = price * (1 + rng.normal(0, 0.0008))
        pct_change = change + rng.normal(0, 0.002)
        iv_live = max(iv + rng.normal(0, 0.003), 0.05)
        rv_live = max(rv + rng.normal(0, 0.003), 0.03)
        color = COLORS['green'] if pct_change >= 0 else COLORS['red']
        row = html.Tr(
            [
                html.Td(name),
                html.Td(f"${price_variation:,.2f}", style={'textAlign': 'right'}),
                html.Td(f"{pct_change:+.2%}", style={'color': color, 'textAlign': 'right'}),
                html.Td(f"{iv_live:.1%}", style={'color': COLORS['yellow'], 'textAlign': 'right'}),
                html.Td(f"{rv_live:.1%}", style={'color': COLORS['blue'], 'textAlign': 'right'}),
                html.Td(f"{volume/1_000_000:.2f}M", style={'textAlign': 'right'})
            ],
            style={'color': COLORS['text'], 'fontSize': '11px'}
        )
        watch_rows.append(row)
    watchlist_table = html.Table(
        [
            html.Thead(
                html.Tr(
                    [
                        html.Th('PAIR'),
                        html.Th('LAST'),
                        html.Th('CHG'),
                        html.Th('IV'),
                        html.Th('RV'),
                        html.Th('VOL'),
                    ],
                    style={'color': COLORS['orange'], 'fontSize': '11px'}
                )
            ),
            html.Tbody(watch_rows)
        ],
        style={'width': '100%', 'fontFamily': FONT_FAMILY}
    )

    # Market stat string for header inline display
    high = 15.72 + rng.normal(0, 0.04)
    low = 14.88 + rng.normal(0, 0.04)
    vol_spread = (base_pairs[0][3] - base_pairs[0][4]) * 100
    header_stats = html.Span(
        f"24H {high:,.2f}/{low:,.2f} | VOL SPREAD {vol_spread:+.2f}bps",
        style={'color': COLORS['muted']}
    )

    # Price series and candle chart
    time_axis = np.arange(0, 75)
    spot = 15.3 + np.cumsum(rng.normal(0, 0.02, size=time_axis.size))
    open_prices = spot + rng.normal(0, 0.04, size=time_axis.size)
    high_prices = np.maximum(open_prices, spot) + rng.random(time_axis.size) * 0.12
    low_prices = np.minimum(open_prices, spot) - rng.random(time_axis.size) * 0.12
    main_chart_fig = go.Figure(
        data=[
            go.Candlestick(
                x=time_axis,
                open=open_prices,
                high=high_prices,
                low=low_prices,
                close=spot,
                increasing_line_color=COLORS['green'],
                decreasing_line_color=COLORS['red'],
                increasing_fillcolor=COLORS['green'],
                decreasing_fillcolor=COLORS['red'],
                hoverinfo='skip'
            )
        ]
    )
    main_chart_fig.update_layout(
        template='plotly_dark',
        paper_bgcolor=COLORS['bg_panel'],
        plot_bgcolor=COLORS['bg_panel'],
        margin={'l': 40, 'r': 20, 't': 10, 'b': 20},
        xaxis={'visible': False},
        yaxis={'gridcolor': COLORS['grid'], 'tickfont': {'family': FONT_FAMILY, 'size': 10}},
        font={'family': FONT_FAMILY}
    )

    # Vol comparison chart (RV vs IV vs GARCH)
    rv_series = np.clip(rng.normal(0.55, 0.02, size=time_axis.size), 0.1, 1.2)
    iv_series = rv_series + rng.normal(0.03, 0.01, size=time_axis.size)
    garch_series = rv_series + rng.normal(0.01, 0.005, size=time_axis.size)
    vol_comp_fig = go.Figure()
    vol_comp_fig.add_trace(go.Scatter(x=time_axis, y=rv_series * 100, name='RV 30D', line={'color': COLORS['yellow'], 'width': 2}))
    vol_comp_fig.add_trace(go.Scatter(x=time_axis, y=iv_series * 100, name='ATM IV', line={'color': COLORS['orange'], 'width': 2}))
    vol_comp_fig.add_trace(go.Scatter(x=time_axis, y=garch_series * 100, name='GARCH', line={'color': COLORS['blue'], 'width': 1.5, 'dash': 'dash'}))
    vol_comp_fig.update_layout(
        template='plotly_dark',
        paper_bgcolor=COLORS['bg_panel'],
        plot_bgcolor=COLORS['bg_panel'],
        margin={'l': 40, 'r': 10, 't': 20, 'b': 30},
        yaxis={'title': 'VOL (%)', 'gridcolor': COLORS['grid'], 'tickfont': {'family': FONT_FAMILY, 'size': 10}},
        legend={'orientation': 'h', 'y': 1.15, 'font': {'size': 9}},
        font={'family': FONT_FAMILY, 'size': 10}
    )

    # Term structure chart
    tenors = np.array([7, 14, 30, 60, 90, 180])
    term_base = np.array([0.54, 0.56, 0.58, 0.60, 0.63, 0.68])
    term_live = term_base + rng.normal(0, 0.01, size=term_base.size)
    term_fig = go.Figure(
        data=[
            go.Scatter(
                x=tenors,
                y=term_live * 100,
                mode='lines+markers',
                line={'color': COLORS['green'], 'width': 2},
                marker={'size': 8, 'color': COLORS['green']},
                name='ATM VOL'
            )
        ]
    )
    term_fig.update_layout(
        template='plotly_dark',
        paper_bgcolor=COLORS['bg_panel'],
        plot_bgcolor=COLORS['bg_panel'],
        margin={'l': 40, 'r': 10, 't': 20, 'b': 30},
        xaxis={'title': 'TENOR (DAYS)', 'gridcolor': COLORS['grid'], 'tickfont': {'family': FONT_FAMILY}},
        yaxis={'title': 'VOL (%)', 'gridcolor': COLORS['grid']},
        font={'family': FONT_FAMILY, 'size': 10}
    )

    # Option skew chart
    strikes = np.linspace(0.6, 1.4, 17)
    smile = 0.58 + 0.12 * (strikes - 1) ** 2 + rng.normal(0, 0.005, size=strikes.size)
    skew_fig = go.Figure(
        data=[
            go.Scatter(
                x=strikes * 100,
                y=smile * 100,
                mode='lines',
                line={'color': COLORS['orange'], 'width': 2},
                name='Smile'
            )
        ]
    )
    skew_fig.update_layout(
        template='plotly_dark',
        paper_bgcolor=COLORS['bg_panel'],
        plot_bgcolor=COLORS['bg_panel'],
        margin={'l': 40, 'r': 10, 't': 20, 'b': 30},
        xaxis={'title': 'MONEYNESS (%)', 'gridcolor': COLORS['grid']},
        yaxis={'title': 'VOL (%)', 'gridcolor': COLORS['grid']},
        font={'family': FONT_FAMILY, 'size': 10}
    )

    # Vol heatmap (surface slice)
    maturities = np.array([7, 14, 30, 60, 90, 180])
    moneyness = np.array([70, 80, 90, 100, 110, 120, 130])
    base_surface = 0.55 + 0.07 * np.random.default_rng(7).random((maturities.size, moneyness.size))
    perturb = rng.normal(0, 0.01, size=base_surface.shape)
    surface = np.clip(base_surface + perturb, 0.25, 1.1)
    heatmap_fig = go.Figure(
        data=[
            go.Heatmap(
                z=surface * 100,
                x=moneyness,
                y=maturities,
                colorscale='Turbo'
            )
        ]
    )
    heatmap_fig.update_layout(
        template='plotly_dark',
        paper_bgcolor=COLORS['bg_panel'],
        plot_bgcolor=COLORS['bg_panel'],
        margin={'l': 50, 'r': 10, 't': 30, 'b': 30},
        xaxis={'title': 'MONEYNESS (%)', 'tickfont': {'family': FONT_FAMILY}},
        yaxis={'title': 'TENOR (DAYS)', 'tickfont': {'family': FONT_FAMILY}},
        font={'family': FONT_FAMILY, 'size': 10}
    )

    # Order book depth (mock ladder)
    depth_levels = np.arange(-5, 6)
    bids = np.clip(600 + rng.normal(0, 40, size=depth_levels.size), 50, None)
    asks = np.clip(620 + rng.normal(0, 40, size=depth_levels.size), 50, None)
    order_fig = go.Figure()
    order_fig.add_trace(
        go.Bar(
            x=bids[depth_levels < 0],
            y=depth_levels[depth_levels < 0],
            orientation='h',
            marker={'color': COLORS['green']},
            name='BIDS'
        )
    )
    order_fig.add_trace(
        go.Bar(
            x=asks[depth_levels > 0],
            y=depth_levels[depth_levels > 0],
            orientation='h',
            marker={'color': COLORS['red']},
            name='ASKS'
        )
    )
    order_fig.update_layout(
        template='plotly_dark',
        paper_bgcolor=COLORS['bg_panel'],
        plot_bgcolor=COLORS['bg_panel'],
        margin={'l': 40, 'r': 20, 't': 20, 'b': 30},
        barmode='overlay',
        xaxis={'title': 'SIZE (k NEO)', 'gridcolor': COLORS['grid']},
        yaxis={'title': 'TICKS', 'gridcolor': COLORS['grid']},
        font={'family': FONT_FAMILY, 'size': 10},
        legend={'font': {'size': 9}}
    )

    # Liquidity by venue bars
    venues = ['Flamingo', 'GhostMarket', 'DeFiYield', 'PolyNetwork']
    liquidity = np.clip(rng.normal([34, 22, 18, 12], 2.5), 5, None)
    liquidity_fig = go.Figure(
        data=[
            go.Bar(
                x=venues,
                y=liquidity,
                marker={'color': [COLORS['orange'], COLORS['green'], COLORS['blue'], COLORS['yellow']]},
                name='Liquidity'
            )
        ]
    )
    liquidity_fig.update_layout(
        template='plotly_dark',
        paper_bgcolor=COLORS['bg_panel'],
        plot_bgcolor=COLORS['bg_panel'],
        margin={'l': 30, 'r': 10, 't': 20, 'b': 40},
        yaxis={'title': 'DEPTH (k USDT)', 'gridcolor': COLORS['grid']},
        font={'family': FONT_FAMILY, 'size': 10}
    )

    # Alerts table
    alerts_payload = [
        ('VOL ARB', 'NEO 30D IV 62% vs RV 55%', 'SELL STRADDLE', 84),
        ('SKEW', 'GAS 45D skew +18%', 'ROLL CALL SPREAD', 63),
        ('GARCH', 'NEO forecast 59% > hedge limit', 'RAISE HEDGE', 47)
    ]
    alert_rows = []
    for tag, desc, action, score in alerts_payload:
        score_color = COLORS['green'] if score >= 75 else COLORS['yellow'] if score >= 50 else COLORS['red']
        alert_rows.append(
            html.Tr(
                [
                    html.Td(tag),
                    html.Td(desc),
                    html.Td(action, style={'color': COLORS['orange']}),
                    html.Td(f"{score}", style={'color': score_color, 'textAlign': 'right'})
                ],
                style={'color': COLORS['text'], 'fontSize': '11px'}
            )
        )
    alerts_table = html.Table(
        [
            html.Thead(
                html.Tr(
                    [html.Th('TAG'), html.Th('DETAIL'), html.Th('ACTION'), html.Th('CONF')],
                    style={'color': COLORS['orange'], 'fontSize': '11px'}
                )
            ),
            html.Tbody(alert_rows)
        ],
        style={'width': '100%', 'fontFamily': FONT_FAMILY}
    )

    # News list
    news_wire = [
        ('Flamingo Pools Add Cross-Chain Liquidity Hub', '07:32:14'),
        ('Neo Council Approves Oracle Incentives For Q1', '07:28:05'),
        ('GAS Utilization Hits 4-Week High Amid Options Demand', '07:18:49'),
        ('AgentSpoons Publishes v1.2 Forecast Model to Testnet', '07:10:17'),
        ('USDN Peg Restored After Overnight Wobble', '06:58:02')
    ]
    news_component = dbc.ListGroup(
        [
            dbc.ListGroupItem(
                [
                    html.Span(ts, style={'color': COLORS['yellow'], 'marginRight': '12px', 'fontFamily': FONT_FAMILY}),
                    html.Span(headline, style={'color': COLORS['text'], 'fontFamily': FONT_FAMILY})
                ],
                style={'backgroundColor': COLORS['bg_panel'], 'border': 'none', 'padding': '6px 8px'}
            )
            for headline, ts in news_wire
        ]
    )

    # Option snapshot
    atm_price = 2.58 + rng.normal(0, 0.03)
    option_component = html.Div(
        [
            html.Div('NEO 30D ATM CALL', style={'color': COLORS['orange'], 'fontWeight': 'bold', 'fontFamily': FONT_FAMILY}),
            html.Div(
                [
                    html.Span('MARK ', style={'color': COLORS['muted'], 'fontFamily': FONT_FAMILY}),
                    html.Span(f"${atm_price:.2f}", style={'color': COLORS['green'], 'fontFamily': FONT_FAMILY, 'fontSize': '18px'})
                ]
            ),
            html.Div(
                f"Delta 0.55 | Gamma 0.021 | Vega 0.14 | Theta -0.07",
                style={'color': COLORS['text'], 'fontFamily': FONT_FAMILY, 'fontSize': '11px', 'marginTop': '6px'}
            )
        ]
    )

    # Greeks table
    greeks_component = html.Table(
        [
            html.Tbody(
                [
                    html.Tr([html.Td('DELTA'), html.Td('0.55', style={'textAlign': 'right'})], style={'color': COLORS['green']}),
                    html.Tr([html.Td('GAMMA'), html.Td('0.021', style={'textAlign': 'right'})], style={'color': COLORS['blue']}),
                    html.Tr([html.Td('VEGA'), html.Td('0.14', style={'textAlign': 'right'})], style={'color': COLORS['yellow']}),
                    html.Tr([html.Td('THETA'), html.Td('-0.07', style={'textAlign': 'right'})], style={'color': COLORS['red']}),
                    html.Tr([html.Td('RHO'), html.Td('0.042', style={'textAlign': 'right'})], style={'color': COLORS['orange']})
                ]
            )
        ],
        style={'width': '100%', 'fontFamily': FONT_FAMILY, 'fontSize': '11px'}
    )

    # Risk indicators
    realized = rv_series[-1]
    implied = iv_series[-1]
    regime = 'ELEVATED' if realized > 0.65 else 'NORMAL' if realized > 0.45 else 'LOW'
    spread_bps = (implied - realized) * 10000
    risk_component = html.Div(
        [
            html.Div(
                [html.Span('VOL REGIME: ', style={'color': COLORS['muted']}), html.Span(regime, style={'color': COLORS['orange']})],
                style={'fontFamily': FONT_FAMILY, 'fontSize': '11px'}
            ),
            html.Div(
                [html.Span('IV-RV SPREAD: ', style={'color': COLORS['muted']}), html.Span(f"{spread_bps:+.0f} bps", style={'color': COLORS['green'] if spread_bps < 0 else COLORS['red']})],
                style={'fontFamily': FONT_FAMILY, 'fontSize': '11px'}
            ),
            html.Div(
                [html.Span('GARCH 1D: ', style={'color': COLORS['muted']}), html.Span(f"{garch_series[-1]*100:.2f}%", style={'color': COLORS['yellow']})],
                style={'fontFamily': FONT_FAMILY, 'fontSize': '11px'}
            ),
            html.Div(
                [html.Span('REALIZED 7D: ', style={'color': COLORS['muted']}), html.Span(f"{rv_series[-7:].mean()*100:.2f}%", style={'color': COLORS['blue']})],
                style={'fontFamily': FONT_FAMILY, 'fontSize': '11px'}
            )
        ]
    )

    # Summary strings
    mid_price = spot[-1]
    price_change = (spot[-1] / spot[-2]) - 1
    price_label = f"{mid_price:,.2f} {'▲' if price_change >= 0 else '▼'} {price_change:+.2%}"
    status_label = 'NEO N3 TESTNET | ORACLE HASH 0x7A2B...F3C9 | LATENCY 42ms'
    ticker_pairs = [
        f"NEO {mid_price:,.2f} {price_change:+.2%}",
        f"GAS {base_pairs[1][1]:.2f} {base_pairs[1][2]:+.2%}",
        f"FLM {base_pairs[2][1]:.3f} {base_pairs[2][2]:+.2%}",
        f"USDN {base_pairs[4][1]:.3f} {base_pairs[4][2]:+.2%}"
    ]
    ticker_text = ' | '.join(ticker_pairs)

    return (
        clock.strftime('%H:%M:%S UTC'),
        clock.strftime('%Y-%m-%d %H:%M:%S'),
        watchlist_table,
        header_stats,
        main_chart_fig,
        vol_comp_fig,
        term_fig,
        skew_fig,
        heatmap_fig,
        order_fig,
        liquidity_fig,
        alerts_table,
        news_component,
        price_label,
        status_label,
        option_component,
        greeks_component,
        risk_component,
        ticker_text
    )


if __name__ == '__main__':
    print('=' * 70)
    print('Bloomberg-inspired AgentSpoons terminal running on http://localhost:8060')
    print('=' * 70)
    app.run(debug=False, port=8060, host='0.0.0.0')
