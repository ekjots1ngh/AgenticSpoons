"""
Working dashboard with better styling
"""
import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import numpy as np
from datetime import datetime

app = dash.Dash(__name__)

class DataStore:
    def __init__(self):
        self.price = 15.23
        self.rv = 0.52
        self.iv = 0.58
        self.history_rv = []
        self.history_iv = []
        self.history_price = []
    
    def update(self):
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

data = DataStore()

app.layout = html.Div(style={
    'backgroundColor': '#0f172a',
    'minHeight': '100vh',
    'padding': '30px',
    'fontFamily': 'Arial, sans-serif'
}, children=[
    
    html.Div([
        html.H1([
            html.Span('\U0001f944 ', style={'fontSize': '40px'}),
            html.Span('AgentSpoons', style={
                'background': 'linear-gradient(135deg, #2563eb, #7c3aed)',
                'WebkitBackgroundClip': 'text',
                'WebkitTextFillColor': 'transparent',
                'fontWeight': '700'
            })
        ], style={'textAlign': 'center', 'marginBottom': '10px'}),
        
        html.P('Real-Time Volatility Oracle', style={
            'textAlign': 'center',
            'color': '#94a3b8',
            'fontSize': '18px',
            'marginBottom': '40px'
        })
    ]),
    
    html.Div([
        html.Div([
            html.P('Price', style={'color': '#94a3b8', 'fontSize': '14px', 'marginBottom': '10px'}),
            html.H2(id='price', style={'color': 'white', 'fontSize': '36px', 'margin': '0'}),
            html.Div(id='price-change', style={'marginTop': '10px'})
        ], style={
            'backgroundColor': '#1e293b',
            'padding': '30px',
            'borderRadius': '12px',
            'width': '23%',
            'display': 'inline-block',
            'margin': '1%',
            'boxShadow': '0 4px 6px rgba(0,0,0,0.3)',
            'border': '1px solid rgba(255,255,255,0.05)'
        }),
        
        html.Div([
            html.P('Realized Vol', style={'color': '#94a3b8', 'fontSize': '14px', 'marginBottom': '10px'}),
            html.H2(id='rv', style={'color': '#10b981', 'fontSize': '36px', 'margin': '0'}),
            html.P('GARCH Model', style={'color': '#64748b', 'fontSize': '12px', 'marginTop': '10px'})
        ], style={
            'backgroundColor': '#1e293b',
            'padding': '30px',
            'borderRadius': '12px',
            'width': '23%',
            'display': 'inline-block',
            'margin': '1%',
            'boxShadow': '0 4px 6px rgba(0,0,0,0.3)',
            'border': '1px solid rgba(255,255,255,0.05)'
        }),
        
        html.Div([
            html.P('Implied Vol', style={'color': '#94a3b8', 'fontSize': '14px', 'marginBottom': '10px'}),
            html.H2(id='iv', style={'color': '#f59e0b', 'fontSize': '36px', 'margin': '0'}),
            html.P('Options Market', style={'color': '#64748b', 'fontSize': '12px', 'marginTop': '10px'})
        ], style={
            'backgroundColor': '#1e293b',
            'padding': '30px',
            'borderRadius': '12px',
            'width': '23%',
            'display': 'inline-block',
            'margin': '1%',
            'boxShadow': '0 4px 6px rgba(0,0,0,0.3)',
            'border': '1px solid rgba(255,255,255,0.05)'
        }),
        
        html.Div([
            html.P('Spread', style={'color': '#94a3b8', 'fontSize': '14px', 'marginBottom': '10px'}),
            html.H2(id='spread', style={'color': '#3b82f6', 'fontSize': '36px', 'margin': '0'}),
            html.Div(id='signal', style={'marginTop': '10px'})
        ], style={
            'backgroundColor': '#1e293b',
            'padding': '30px',
            'borderRadius': '12px',
            'width': '23%',
            'display': 'inline-block',
            'margin': '1%',
            'boxShadow': '0 4px 6px rgba(0,0,0,0.3)',
            'border': '1px solid rgba(255,255,255,0.05)'
        })
    ], style={'marginBottom': '30px'}),
    
    html.Div([
        dcc.Graph(id='chart', config={'displayModeBar': False})
    ], style={
        'backgroundColor': '#1e293b',
        'padding': '30px',
        'borderRadius': '12px',
        'boxShadow': '0 4px 6px rgba(0,0,0,0.3)',
        'border': '1px solid rgba(255,255,255,0.05)'
    }),
    
    dcc.Interval(id='interval', interval=1000, n_intervals=0)
])

@app.callback(
    [Output('price', 'children'),
     Output('price-change', 'children'),
     Output('rv', 'children'),
     Output('iv', 'children'),
     Output('spread', 'children'),
     Output('signal', 'children'),
     Output('chart', 'figure')],
    [Input('interval', 'n_intervals')]
)
def update(n):
    data.update()
    
    spread = data.iv - data.rv
    price_change = ((data.price - data.history_price[-2]) / data.history_price[-2] * 100) if len(data.history_price) > 1 else 0
    
    price_change_display = html.Span(
        f"{'\u25b2' if price_change > 0 else '\u25bc'} {abs(price_change):.2f}%",
        style={'color': '#10b981' if price_change > 0 else '#ef4444', 'fontSize': '14px', 'fontWeight': '600'}
    )
    
    if spread > 0.08:
        signal_text = html.Span('\U0001f525 Strong Signal', style={'color': '#10b981', 'fontSize': '13px', 'fontWeight': '600'})
    elif spread > 0.05:
        signal_text = html.Span('\U0001f4a1 Moderate', style={'color': '#f59e0b', 'fontSize': '13px', 'fontWeight': '600'})
    else:
        signal_text = html.Span('\U0001f4c8 Normal', style={'color': '#64748b', 'fontSize': '13px', 'fontWeight': '600'})
    
    fig = go.Figure()
    
    if len(data.history_rv) > 0:
        fig.add_trace(go.Scatter(y=data.history_rv, name='Realized Vol', line=dict(color='#10b981', width=3)))
        fig.add_trace(go.Scatter(y=data.history_iv, name='Implied Vol', line=dict(color='#f59e0b', width=3)))
    
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='#1e293b',
        plot_bgcolor='#1e293b',
        margin=dict(l=40, r=20, t=20, b=40),
        yaxis=dict(title='Volatility %', gridcolor='rgba(255,255,255,0.1)'),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)', showticklabels=False),
        height=400,
        legend=dict(orientation='h', y=1.05)
    )
    
    return f"${data.price:.2f}", price_change_display, f"{data.rv:.2%}", f"{data.iv:.2%}", f"{spread:.2%}", signal_text, fig

if __name__ == '__main__':
    print("="*70)
    print("\U0001f680 DASHBOARD STARTING")
    print("="*70)
    print("\U0001f310 URL: http://127.0.0.1:9999")
    print("="*70)
    app.run_server(debug=True, port=9999, host='127.0.0.1')
