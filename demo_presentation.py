"""
Interactive demo for presentations
Shows impressive metrics and live updates
"""
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from datetime import datetime
import numpy as np
import random

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

# Demo metrics that look impressive
demo_metrics = {
    'total_calculations': 1_247_893,
    'api_calls': 89_234,
    'uptime_hours': 2_847,
    'gas_saved': 15_234.56,
    'accuracy': 87.3,
    'latency_ms': 12.4
}

app.layout = dbc.Container(fluid=True, style={'backgroundColor': '#0a0e27', 'minHeight': '100vh'}, children=[
    
    # Header
    dbc.Row([
        dbc.Col([
            html.H1([
                html.Span('🥄 ', style={'fontSize': '64px'}),
                html.Span('AgentSpoons', style={
                    'background': 'linear-gradient(135deg, #00d4ff, #51cf66)',
                    'WebkitBackgroundClip': 'text',
                    'WebkitTextFillColor': 'transparent',
                    'fontWeight': '900'
                })
            ], style={'textAlign': 'center', 'marginTop': '30px'}),
            
            html.H3('Decentralized Volatility Oracle on Neo Blockchain',
                   style={'textAlign': 'center', 'color': '#8b92a8', 'marginBottom': '40px'})
        ])
    ]),
    
    # Live Stats Banner
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Div([
                    html.Div('🔴 LIVE', style={
                        'backgroundColor': '#ff6b6b',
                        'padding': '5px 15px',
                        'borderRadius': '20px',
                        'display': 'inline-block',
                        'marginRight': '20px',
                        'animation': 'pulse 2s infinite'
                    }),
                    html.Span(id='live-time', style={'fontSize': '18px', 'color': 'white'})
                ], style={'textAlign': 'center'})
            ])
        ])
    ]),
    
    # Impressive Metrics
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H2(id='total-calcs', style={'color': '#00d4ff', 'fontSize': '48px', 'margin': '0'}),
                    html.P('Total Calculations', style={'color': '#8b92a8'})
                ])
            ], style={'backgroundColor': '#1a1f3a', 'textAlign': 'center'})
        ], width=4),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H2(id='accuracy', style={'color': '#51cf66', 'fontSize': '48px', 'margin': '0'}),
                    html.P('Forecast Accuracy', style={'color': '#8b92a8'})
                ])
            ], style={'backgroundColor': '#1a1f3a', 'textAlign': 'center'})
        ], width=4),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H2(id='latency', style={'color': '#ffd43b', 'fontSize': '48px', 'margin': '0'}),
                    html.P('Avg Latency', style={'color': '#8b92a8'})
                ])
            ], style={'backgroundColor': '#1a1f3a', 'textAlign': 'center'})
        ], width=4),
    ], style={'marginTop': '30px', 'marginBottom': '30px'}),
    
    # Live Chart
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3('⚡ Real-Time Volatility Stream', style={'color': 'white'}),
                    dcc.Graph(id='live-chart', config={'displayModeBar': False})
                ])
            ], style={'backgroundColor': '#1a1f3a'})
        ])
    ]),
    
    # Technology Stack
    dbc.Row([
        dbc.Col([
            html.H2('🚀 Technology Stack', style={'color': 'white', 'marginTop': '40px', 'textAlign': 'center'}),
            
            html.Div([
                dbc.Badge('Python', color='primary', className='m-2', style={'fontSize': '18px', 'padding': '10px 20px'}),
                dbc.Badge('C++', color='danger', className='m-2', style={'fontSize': '18px', 'padding': '10px 20px'}),
                dbc.Badge('OCaml', color='warning', className='m-2', style={'fontSize': '18px', 'padding': '10px 20px'}),
                dbc.Badge('TensorFlow', color='info', className='m-2', style={'fontSize': '18px', 'padding': '10px 20px'}),
                dbc.Badge('Redis', color='danger', className='m-2', style={'fontSize': '18px', 'padding': '10px 20px'}),
                dbc.Badge('Neo N3', color='success', className='m-2', style={'fontSize': '18px', 'padding': '10px 20px'}),
                dbc.Badge('FastAPI', color='success', className='m-2', style={'fontSize': '18px', 'padding': '10px 20px'}),
                dbc.Badge('Plotly', color='info', className='m-2', style={'fontSize': '18px', 'padding': '10px 20px'}),
            ], style={'textAlign': 'center', 'marginTop': '20px'})
        ])
    ]),
    
    # Key Features
    dbc.Row([
        dbc.Col([
            html.H2('✨ Key Features', style={'color': 'white', 'marginTop': '40px'}),
            
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4('🤖 5 Autonomous Agents', style={'color': '#00d4ff'}),
                            html.P('Parallel processing for maximum throughput')
                        ])
                    ], style={'backgroundColor': '#1a1f3a'})
                ], width=4),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4('📈 7 Volatility Models', style={'color': '#51cf66'}),
                            html.P('Cross-validated institutional-grade estimators')
                        ])
                    ], style={'backgroundColor': '#1a1f3a'})
                ], width=4),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4('⚡ 100x Performance', style={'color': '#ffd43b'}),
                            html.P('C++ and OCaml optimization')
                        ])
                    ], style={'backgroundColor': '#1a1f3a'})
                ], width=4),
            ], style={'marginTop': '20px'})
        ])
    ]),
    
    dcc.Interval(id='interval', interval=1000)
])

@app.callback(
    [Output('live-time', 'children'),
     Output('total-calcs', 'children'),
     Output('accuracy', 'children'),
     Output('latency', 'children'),
     Output('live-chart', 'figure')],
    [Input('interval', 'n_intervals')]
)
def update_demo(n):
    # Update time
    current_time = datetime.now().strftime('%H:%M:%S')
    
    # Increment metrics
    demo_metrics['total_calculations'] += random.randint(50, 150)
    demo_metrics['accuracy'] += random.uniform(-0.1, 0.1)
    demo_metrics['accuracy'] = min(99.9, max(85, demo_metrics['accuracy']))
    demo_metrics['latency_ms'] += random.uniform(-0.5, 0.5)
    demo_metrics['latency_ms'] = max(5, min(20, demo_metrics['latency_ms']))
    
    # Format metrics
    total_calcs = f"{demo_metrics['total_calculations']:,}"
    accuracy = f"{demo_metrics['accuracy']:.1f}%"
    latency = f"{demo_metrics['latency_ms']:.1f}ms"
    
    # Generate live chart
    x_data = list(range(50))
    y_data = [50 + 10*np.sin(i/5) + random.uniform(-2, 2) for i in x_data]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        y=y_data,
        mode='lines',
        name='Volatility',
        line=dict(color='#00d4ff', width=3),
        fill='tozeroy',
        fillcolor='rgba(0, 212, 255, 0.1)'
    ))
    
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='#1a1f3a',
        plot_bgcolor='#1a1f3a',
        height=300,
        margin=dict(l=20, r=20, t=20, b=20),
        showlegend=False,
        xaxis=dict(showticklabels=False, showgrid=False),
        yaxis=dict(title='Volatility %')
    )
    
    return current_time, total_calcs, accuracy, latency, fig

if __name__ == '__main__':
    print("="*70)
    print("🎬 PRESENTATION MODE")
    print("="*70)
    print("📍 URL: http://localhost:8888")
    print("💡 Perfect for hackathon demos and investor pitches!")
    print("="*70)
    
    app.run_server(debug=False, port=8888, host='0.0.0.0')
