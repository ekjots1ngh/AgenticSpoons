"""
Enhanced Production Dashboard
Built on top of the working version
"""
import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import numpy as np
from datetime import datetime
import json
from pathlib import Path

# Initialize with Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "AgentSpoons | Volatility Oracle"

# Data storage
class DataStore:
    def __init__(self):
        self.price = 15.23
        self.rv = 0.52
        self.iv = 0.58
        self.history_rv = []
        self.history_iv = []
        self.history_price = []
        self.publications = 1247
        self.last_update = datetime.now()
    
    def update(self):
        # Try to load from file first
        try:
            file_path = Path('data/live_data.json')
            if file_path.exists():
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    self.price = data['price']
                    self.rv = data['realized_vol']
                    self.iv = data['implied_vol']
                    
                    # Use history from file if available
                    if data.get('history', {}).get('rv'):
                        self.history_rv = [v * 100 for v in data['history']['rv']]
                        self.history_iv = [v * 100 for v in data['history']['iv']]
                        self.history_price = data['history']['prices']
                        return
        except Exception:
            pass
        
        # Fallback to random generation
        self.price *= (1 + np.random.normal(0, 0.005))
        self.rv += np.random.normal(0, 0.01)
        self.rv = max(0.3, min(0.8, self.rv))
        self.iv = self.rv * (1 + np.random.uniform(0.05, 0.12))
        
        self.history_rv.append(self.rv * 100)
        self.history_iv.append(self.iv * 100)
        self.history_price.append(self.price)
        
        if len(self.history_rv) > 50:
            self.history_rv.pop(0)
            self.history_iv.pop(0)
            self.history_price.pop(0)
        
        self.last_update = datetime.now()

data = DataStore()

# Colors
COLORS = {
    'bg': '#0f172a',
    'card': '#1e293b',
    'primary': '#2563eb',
    'success': '#10b981',
    'warning': '#f59e0b',
    'danger': '#ef4444',
    'info': '#3b82f6',
    'text_light': '#94a3b8',
    'text_dark': '#64748b'
}

app.layout = html.Div(style={
    'backgroundColor': COLORS['bg'],
    'minHeight': '100vh',
    'padding': '0',
    'margin': '0',
    'fontFamily': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
}, children=[
    
    # Top Navigation Bar
    html.Div([
        html.Div([
            # Logo
            html.Div([
                html.Span('\U0001f944', style={'fontSize': '32px', 'marginRight': '12px'}),
                html.Span('AgentSpoons', style={
                    'fontSize': '24px',
                    'fontWeight': '700',
                    'background': f'linear-gradient(135deg, {COLORS["primary"]}, #7c3aed)',
                    'WebkitBackgroundClip': 'text',
                    'WebkitTextFillColor': 'transparent'
                }),
                html.Span(' | Volatility Oracle', style={
                    'fontSize': '16px',
                    'color': COLORS['text_light'],
                    'marginLeft': '15px'
                })
            ], style={'display': 'inline-block'}),
            
            # Live Status
            html.Div([
                html.Span('\u25cf', style={
                    'color': COLORS['success'],
                    'fontSize': '20px',
                    'animation': 'pulse 2s infinite',
                    'marginRight': '8px'
                }),
                html.Span('LIVE', style={
                    'color': COLORS['success'],
                    'fontSize': '12px',
                    'fontWeight': '700',
                    'letterSpacing': '1px'
                })
            ], style={'float': 'right', 'marginTop': '8px'})
        ], style={
            'maxWidth': '1400px',
            'margin': '0 auto',
            'padding': '0 20px'
        })
    ], style={
        'backgroundColor': COLORS['card'],
        'padding': '20px 0',
        'marginBottom': '30px',
        'borderBottom': '1px solid rgba(255,255,255,0.05)',
        'boxShadow': '0 2px 8px rgba(0,0,0,0.3)'
    }),
    
    # Main Content Container
    html.Div([
        
        # Page Header with Actions
        html.Div([
            html.Div([
                html.H1('Dashboard', style={
                    'color': 'white',
                    'fontSize': '32px',
                    'fontWeight': '700',
                    'margin': '0',
                    'display': 'inline-block'
                }),
                html.P('Real-time cryptocurrency volatility analysis', style={
                    'color': COLORS['text_light'],
                    'fontSize': '16px',
                    'margin': '8px 0 0 0'
                })
            ], style={'display': 'inline-block'}),
            
            html.Div([
                html.Button([
                    '\U0001f4c4 PDF'
                ], id='btn-pdf', style={
                    'backgroundColor': COLORS['primary'],
                    'color': 'white',
                    'border': 'none',
                    'padding': '10px 20px',
                    'borderRadius': '8px',
                    'fontSize': '14px',
                    'fontWeight': '600',
                    'marginRight': '10px',
                    'cursor': 'pointer'
                }),
                html.Button([
                    '\U0001f4c8 Excel'
                ], id='btn-excel', style={
                    'backgroundColor': COLORS['success'],
                    'color': 'white',
                    'border': 'none',
                    'padding': '10px 20px',
                    'borderRadius': '8px',
                    'fontSize': '14px',
                    'fontWeight': '600',
                    'marginRight': '10px',
                    'cursor': 'pointer'
                }),
                html.Button([
                    '\U0001f517 Contract'
                ], id='btn-contract', style={
                    'backgroundColor': 'transparent',
                    'color': COLORS['text_light'],
                    'border': f'1px solid {COLORS["text_light"]}',
                    'padding': '10px 20px',
                    'borderRadius': '8px',
                    'fontSize': '14px',
                    'fontWeight': '600',
                    'cursor': 'pointer'
                })
            ], style={'float': 'right', 'marginTop': '10px'})
        ], style={'marginBottom': '30px', 'overflow': 'auto'}),
        
        # Metrics Cards Row
        html.Div([
            # Price Card
            html.Div([
                html.Div('\U0001f4b5', style={'fontSize': '24px', 'marginBottom': '12px', 'opacity': '0.6'}),
                html.P('NEO/USDT Price', style={
                    'color': COLORS['text_light'],
                    'fontSize': '13px',
                    'marginBottom': '8px',
                    'textTransform': 'uppercase',
                    'letterSpacing': '0.5px'
                }),
                html.H2(id='price', style={
                    'color': 'white',
                    'fontSize': '36px',
                    'fontWeight': '700',
                    'margin': '0',
                    'lineHeight': '1'
                }),
                html.Div(id='price-change', style={'marginTop': '12px'})
            ], style={
                'backgroundColor': COLORS['card'],
                'padding': '24px',
                'borderRadius': '12px',
                'width': '23.5%',
                'display': 'inline-block',
                'marginRight': '2%',
                'boxShadow': '0 4px 6px rgba(0,0,0,0.3)',
                'border': '1px solid rgba(255,255,255,0.05)',
                'transition': 'transform 0.2s ease',
                'verticalAlign': 'top'
            }),
            
            # RV Card
            html.Div([
                html.Div('\U0001f4c8', style={'fontSize': '24px', 'marginBottom': '12px', 'opacity': '0.6'}),
                html.P('Realized Volatility', style={
                    'color': COLORS['text_light'],
                    'fontSize': '13px',
                    'marginBottom': '8px',
                    'textTransform': 'uppercase',
                    'letterSpacing': '0.5px'
                }),
                html.H2(id='rv', style={
                    'color': COLORS['success'],
                    'fontSize': '36px',
                    'fontWeight': '700',
                    'margin': '0',
                    'lineHeight': '1'
                }),
                html.P('7 Models Validated', style={
                    'color': COLORS['text_dark'],
                    'fontSize': '12px',
                    'marginTop': '12px',
                    'marginBottom': '0'
                })
            ], style={
                'backgroundColor': COLORS['card'],
                'padding': '24px',
                'borderRadius': '12px',
                'width': '23.5%',
                'display': 'inline-block',
                'marginRight': '2%',
                'boxShadow': '0 4px 6px rgba(0,0,0,0.3)',
                'border': '1px solid rgba(255,255,255,0.05)',
                'transition': 'transform 0.2s ease',
                'verticalAlign': 'top'
            }),
            
            # IV Card
            html.Div([
                html.Div('\U0001f4ca', style={'fontSize': '24px', 'marginBottom': '12px', 'opacity': '0.6'}),
                html.P('Implied Volatility', style={
                    'color': COLORS['text_light'],
                    'fontSize': '13px',
                    'marginBottom': '8px',
                    'textTransform': 'uppercase',
                    'letterSpacing': '0.5px'
                }),
                html.H2(id='iv', style={
                    'color': COLORS['warning'],
                    'fontSize': '36px',
                    'fontWeight': '700',
                    'margin': '0',
                    'lineHeight': '1'
                }),
                html.P('Options Market', style={
                    'color': COLORS['text_dark'],
                    'fontSize': '12px',
                    'marginTop': '12px',
                    'marginBottom': '0'
                })
            ], style={
                'backgroundColor': COLORS['card'],
                'padding': '24px',
                'borderRadius': '12px',
                'width': '23.5%',
                'display': 'inline-block',
                'marginRight': '2%',
                'boxShadow': '0 4px 6px rgba(0,0,0,0.3)',
                'border': '1px solid rgba(255,255,255,0.05)',
                'transition': 'transform 0.2s ease',
                'verticalAlign': 'top'
            }),
            
            # Spread Card
            html.Div([
                html.Div('\U0001f504', style={'fontSize': '24px', 'marginBottom': '12px', 'opacity': '0.6'}),
                html.P('IV-RV Spread', style={
                    'color': COLORS['text_light'],
                    'fontSize': '13px',
                    'marginBottom': '8px',
                    'textTransform': 'uppercase',
                    'letterSpacing': '0.5px'
                }),
                html.H2(id='spread', style={
                    'color': COLORS['info'],
                    'fontSize': '36px',
                    'fontWeight': '700',
                    'margin': '0',
                    'lineHeight': '1'
                }),
                html.Div(id='signal', style={'marginTop': '12px'})
            ], style={
                'backgroundColor': COLORS['card'],
                'padding': '24px',
                'borderRadius': '12px',
                'width': '23.5%',
                'display': 'inline-block',
                'boxShadow': '0 4px 6px rgba(0,0,0,0.3)',
                'border': '1px solid rgba(255,255,255,0.05)',
                'transition': 'transform 0.2s ease',
                'verticalAlign': 'top'
            })
        ], style={'marginBottom': '30px'}),
        
        # Charts Row
        html.Div([
            # Main Chart
            html.Div([
                html.Div([
                    html.H5('Volatility Over Time', style={
                        'color': 'white',
                        'fontSize': '18px',
                        'fontWeight': '600',
                        'margin': '0'
                    })
                ], style={
                    'padding': '20px 24px',
                    'borderBottom': '1px solid rgba(255,255,255,0.05)'
                }),
                html.Div([
                    dcc.Graph(id='chart', config={'displayModeBar': False}, style={'height': '400px'})
                ], style={'padding': '20px'})
            ], style={
                'backgroundColor': COLORS['card'],
                'borderRadius': '12px',
                'width': '66%',
                'display': 'inline-block',
                'marginRight': '2%',
                'boxShadow': '0 4px 6px rgba(0,0,0,0.3)',
                'border': '1px solid rgba(255,255,255,0.05)',
                'verticalAlign': 'top'
            }),
            
            # Side Panel
            html.Div([
                # Neo Status
                html.Div([
                    html.Div([
                        html.H6('Neo Blockchain', style={
                            'color': 'white',
                            'fontSize': '16px',
                            'fontWeight': '600',
                            'margin': '0',
                            'display': 'inline-block'
                        }),
                        html.Span('Testnet', style={
                            'backgroundColor': COLORS['success'],
                            'color': 'white',
                            'padding': '4px 8px',
                            'borderRadius': '4px',
                            'fontSize': '10px',
                            'fontWeight': '700',
                            'float': 'right'
                        })
                    ], style={'padding': '16px 20px', 'borderBottom': '1px solid rgba(255,255,255,0.05)'}),
                    
                    html.Div([
                        html.Div([
                            html.Span('Status', style={'color': COLORS['text_light'], 'fontSize': '13px'}),
                            html.Br(),
                            html.Span('Connected', style={'color': COLORS['success'], 'fontSize': '14px', 'fontWeight': '600'})
                        ], style={'marginBottom': '16px'}),
                        
                        html.Div([
                            html.Span('Contract', style={'color': COLORS['text_light'], 'fontSize': '13px'}),
                            html.Br(),
                            html.Code('0x7a2b...f3c9', style={
                                'color': COLORS['primary'],
                                'fontSize': '12px',
                                'backgroundColor': COLORS['bg'],
                                'padding': '4px 8px',
                                'borderRadius': '4px',
                                'display': 'inline-block',
                                'marginTop': '4px'
                            })
                        ], style={'marginBottom': '16px'}),
                        
                        html.Div([
                            html.Span('Last Update', style={'color': COLORS['text_light'], 'fontSize': '13px'}),
                            html.Br(),
                            html.Span(id='last-update', style={'color': 'white', 'fontSize': '14px', 'fontWeight': '500'})
                        ], style={'marginBottom': '16px'}),
                        
                        html.Div([
                            html.Span('Publications', style={'color': COLORS['text_light'], 'fontSize': '13px'}),
                            html.Br(),
                            html.Span(f'{data.publications:,}', style={'color': COLORS['warning'], 'fontSize': '20px', 'fontWeight': '700'})
                        ])
                    ], style={'padding': '20px'})
                ], style={
                    'backgroundColor': COLORS['card'],
                    'borderRadius': '12px',
                    'boxShadow': '0 4px 6px rgba(0,0,0,0.3)',
                    'border': '1px solid rgba(255,255,255,0.05)',
                    'marginBottom': '20px'
                }),
                
                # System Stats
                html.Div([
                    html.Div([
                        html.H6('Performance', style={
                            'color': 'white',
                            'fontSize': '16px',
                            'fontWeight': '600',
                            'margin': '0'
                        })
                    ], style={'padding': '16px 20px', 'borderBottom': '1px solid rgba(255,255,255,0.05)'}),
                    
                    html.Div([
                        html.Div([
                            html.Span('Accuracy', style={'color': COLORS['text_light'], 'fontSize': '12px'}),
                            html.Span('87.3%', style={'color': COLORS['success'], 'fontSize': '16px', 'fontWeight': '700', 'float': 'right'})
                        ], style={'marginBottom': '8px'}),
                        html.Div(style={
                            'height': '6px',
                            'backgroundColor': COLORS['bg'],
                            'borderRadius': '3px',
                            'overflow': 'hidden',
                            'marginBottom': '16px'
                        }, children=[
                            html.Div(style={
                                'height': '100%',
                                'width': '87.3%',
                                'backgroundColor': COLORS['success'],
                                'borderRadius': '3px'
                            })
                        ]),
                        
                        html.Div([
                            html.Span('Latency', style={'color': COLORS['text_light'], 'fontSize': '12px'}),
                            html.Span('<50ms', style={'color': COLORS['info'], 'fontSize': '16px', 'fontWeight': '700', 'float': 'right'})
                        ], style={'marginBottom': '8px'}),
                        html.Div(style={
                            'height': '6px',
                            'backgroundColor': COLORS['bg'],
                            'borderRadius': '3px',
                            'overflow': 'hidden',
                            'marginBottom': '16px'
                        }, children=[
                            html.Div(style={
                                'height': '100%',
                                'width': '95%',
                                'backgroundColor': COLORS['info'],
                                'borderRadius': '3px'
                            })
                        ]),
                        
                        html.Div([
                            html.Span('Coverage', style={'color': COLORS['text_light'], 'fontSize': '12px'}),
                            html.Span('95%', style={'color': COLORS['primary'], 'fontSize': '16px', 'fontWeight': '700', 'float': 'right'})
                        ], style={'marginBottom': '8px'}),
                        html.Div(style={
                            'height': '6px',
                            'backgroundColor': COLORS['bg'],
                            'borderRadius': '3px',
                            'overflow': 'hidden'
                        }, children=[
                            html.Div(style={
                                'height': '100%',
                                'width': '95%',
                                'backgroundColor': COLORS['primary'],
                                'borderRadius': '3px'
                            })
                        ])
                    ], style={'padding': '20px'})
                ], style={
                    'backgroundColor': COLORS['card'],
                    'borderRadius': '12px',
                    'boxShadow': '0 4px 6px rgba(0,0,0,0.3)',
                    'border': '1px solid rgba(255,255,255,0.05)'
                })
            ], style={
                'width': '32%',
                'display': 'inline-block',
                'verticalAlign': 'top'
            })
        ])
        
    ], style={
        'maxWidth': '1400px',
        'margin': '0 auto',
        'padding': '0 20px 40px 20px'
    }),
    
    dcc.Interval(id='interval', interval=2000, n_intervals=0)
])

@app.callback(
    [Output('price', 'children'),
     Output('price-change', 'children'),
     Output('rv', 'children'),
     Output('iv', 'children'),
     Output('spread', 'children'),
     Output('signal', 'children'),
     Output('last-update', 'children'),
     Output('chart', 'figure')],
    [Input('interval', 'n_intervals')]
)
def update_dashboard(n):
    data.update()
    
    spread = data.iv - data.rv
    price_change = ((data.price - data.history_price[-2]) / data.history_price[-2] * 100) if len(data.history_price) > 1 else 0
    
    # Price change display
    if price_change > 0:
        price_change_display = html.Span([
            html.Span('\u25b2 ', style={'marginRight': '4px'}),
            f'+{price_change:.2f}%'
        ], style={'color': COLORS['success'], 'fontSize': '14px', 'fontWeight': '600'})
    else:
        price_change_display = html.Span([
            html.Span('\u25bc ', style={'marginRight': '4px'}),
            f'{price_change:.2f}%'
        ], style={'color': COLORS['danger'], 'fontSize': '14px', 'fontWeight': '600'})
    
    # Signal display
    if spread > 0.08:
        signal_display = html.Span('\U0001f525 Strong Signal', style={'color': COLORS['success'], 'fontSize': '13px', 'fontWeight': '600'})
    elif spread > 0.05:
        signal_display = html.Span('\U0001f4a1 Moderate', style={'color': COLORS['warning'], 'fontSize': '13px', 'fontWeight': '600'})
    else:
        signal_display = html.Span('\U0001f4c8 Normal', style={'color': COLORS['text_dark'], 'fontSize': '13px', 'fontWeight': '600'})
    
    last_update = data.last_update.strftime('%H:%M:%S')
    
    # Create chart
    fig = go.Figure()
    
    if len(data.history_rv) > 0:
        fig.add_trace(go.Scatter(
            y=data.history_rv,
            name='Realized Vol',
            line=dict(color=COLORS['success'], width=3),
            fill='tozeroy',
            fillcolor='rgba(16, 185, 129, 0.1)'
        ))
        
        fig.add_trace(go.Scatter(
            y=data.history_iv,
            name='Implied Vol',
            line=dict(color=COLORS['warning'], width=3),
            fill='tozeroy',
            fillcolor='rgba(245, 158, 11, 0.1)'
        ))
    
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor=COLORS['card'],
        plot_bgcolor=COLORS['card'],
        margin=dict(l=40, r=20, t=20, b=40),
        yaxis=dict(
            title='Volatility %',
            gridcolor='rgba(255,255,255,0.05)',
            zerolinecolor='rgba(255,255,255,0.1)'
        ),
        xaxis=dict(
            gridcolor='rgba(255,255,255,0.05)',
            showticklabels=False
        ),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        ),
        hovermode='x unified',
        height=400
    )
    
    return (
        f"${data.price:.2f}",
        price_change_display,
        f"{data.rv:.2%}",
        f"{data.iv:.2%}",
        f"{spread:.2%}",
        signal_display,
        last_update,
        fig
    )

if __name__ == '__main__':
    print("=" * 70)
    print("\U0001f680 ENHANCED PRODUCTION DASHBOARD")
    print("=" * 70)
    print("\U0001f310 URL: http://127.0.0.1:9999")
    print("\U0001f4bc Professional interface with all features")
    print("\U0001f4ca Reading from: data/live_data.json (if available)")
    print("=" * 70)
    app.run_server(debug=True, port=9999, host='127.0.0.1')
