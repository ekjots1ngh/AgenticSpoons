"""
Interactive Options Greeks Visualization
"""
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from scipy.stats import norm

class GreeksVisualizer:
    """Visualize all Option Greeks"""
    
    def __init__(self, S0=100, K=100, T=0.25, r=0.05, sigma=0.2):
        self.S0 = S0
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
    
    def calculate_greeks(self, S, K, T, r, sigma):
        """Calculate all Greeks using Black-Scholes formulas"""
        # Avoid numerical issues
        if T <= 0 or sigma <= 0:
            return {
                'call_price': max(S - K, 0),
                'put_price': max(K - S, 0),
                'delta': 1.0 if S > K else 0.0,
                'gamma': 0.0,
                'vega': 0.0,
                'theta': 0.0,
                'rho': 0.0
            }
        
        # Calculate d1 and d2
        d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
        d2 = d1 - sigma*np.sqrt(T)
        
        # Prices
        call_price = S * norm.cdf(d1) - K * np.exp(-r*T) * norm.cdf(d2)
        put_price = K * np.exp(-r*T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        
        # Greeks
        delta = norm.cdf(d1)
        gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
        vega = S * norm.pdf(d1) * np.sqrt(T)
        theta = (-(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) - r * K * np.exp(-r*T) * norm.cdf(d2)) / 365
        rho = K * T * np.exp(-r*T) * norm.cdf(d2) / 100
        
        return {
            'call_price': float(call_price),
            'put_price': float(put_price),
            'delta': float(delta),
            'gamma': float(gamma),
            'vega': float(vega),
            'theta': float(theta),
            'rho': float(rho)
        }
    
    def create_delta_surface(self):
        """3D surface of Delta vs Spot and Time"""
        spot_range = np.linspace(self.S0 * 0.7, self.S0 * 1.3, 50)
        time_range = np.linspace(0.01, 1.0, 50)
        
        S_grid, T_grid = np.meshgrid(spot_range, time_range)
        delta_grid = np.zeros_like(S_grid)
        
        for i in range(len(time_range)):
            for j in range(len(spot_range)):
                greeks = self.calculate_greeks(
                    S_grid[i,j], self.K, T_grid[i,j], self.r, self.sigma
                )
                delta_grid[i,j] = greeks['delta']
        
        fig = go.Figure(data=[go.Surface(
            x=S_grid,
            y=T_grid,
            z=delta_grid,
            colorscale='Viridis',
            name='Delta'
        )])
        
        fig.update_layout(
            title='Delta Surface',
            scene=dict(
                xaxis_title='Spot Price',
                yaxis_title='Time to Maturity',
                zaxis_title='Delta',
                camera=dict(eye=dict(x=1.5, y=1.5, z=1.3))
            ),
            template='plotly_dark',
            height=600
        )
        
        return fig
    
    def create_gamma_profile(self):
        """Gamma profile across strikes"""
        strikes = np.linspace(self.S0 * 0.7, self.S0 * 1.3, 100)
        gammas = []
        
        for K in strikes:
            greeks = self.calculate_greeks(self.S0, K, self.T, self.r, self.sigma)
            gammas.append(greeks['gamma'])
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=strikes,
            y=gammas,
            mode='lines',
            name='Gamma',
            line=dict(color='#00d4ff', width=3),
            fill='tozeroy',
            fillcolor='rgba(0, 212, 255, 0.1)'
        ))
        
        # Mark ATM
        fig.add_vline(x=self.S0, line_dash="dash", line_color='#ff6b6b',
                     annotation_text='ATM')
        
        fig.update_layout(
            title='Gamma Profile',
            xaxis_title='Strike Price',
            yaxis_title='Gamma',
            template='plotly_dark',
            height=400
        )
        
        return fig
    
    def create_vega_chart(self):
        """Vega vs volatility"""
        vols = np.linspace(0.1, 0.8, 50)
        vegas = []
        
        for vol in vols:
            greeks = self.calculate_greeks(self.S0, self.K, self.T, self.r, vol)
            vegas.append(greeks['vega'])
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=vols * 100,
            y=vegas,
            mode='lines+markers',
            name='Vega',
            line=dict(color='#51cf66', width=3),
            marker=dict(size=6)
        ))
        
        fig.update_layout(
            title='Vega vs Volatility',
            xaxis_title='Volatility %',
            yaxis_title='Vega',
            template='plotly_dark',
            height=400
        )
        
        return fig
    
    def create_theta_decay(self):
        """Theta decay over time"""
        times = np.linspace(self.T, 0.01, 50)
        thetas = []
        
        for t in times:
            greeks = self.calculate_greeks(self.S0, self.K, t, self.r, self.sigma)
            thetas.append(greeks['theta'])
        
        # Days to expiry
        days = times * 365
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=days,
            y=thetas,
            mode='lines',
            name='Theta',
            line=dict(color='#ffd43b', width=3),
            fill='tozeroy',
            fillcolor='rgba(255, 212, 59, 0.1)'
        ))
        
        fig.update_layout(
            title='Theta Decay',
            xaxis_title='Days to Expiry',
            yaxis_title='Theta (Daily)',
            template='plotly_dark',
            height=400
        )
        
        return fig
    
    def create_comprehensive_dashboard(self):
        """Create comprehensive Greeks dashboard"""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Delta', 'Gamma', 'Vega', 'Theta'),
            specs=[[{'type': 'scatter'}, {'type': 'scatter'}],
                   [{'type': 'scatter'}, {'type': 'scatter'}]]
        )
        
        # Spot price range
        spots = np.linspace(self.S0 * 0.7, self.S0 * 1.3, 100)
        
        deltas, gammas, vegas, thetas = [], [], [], []
        
        for S in spots:
            greeks = self.calculate_greeks(S, self.K, self.T, self.r, self.sigma)
            deltas.append(greeks['delta'])
            gammas.append(greeks['gamma'])
            vegas.append(greeks['vega'])
            thetas.append(greeks['theta'])
        
        # Delta
        fig.add_trace(
            go.Scatter(x=spots, y=deltas, name='Delta', line=dict(color='#00d4ff', width=2)),
            row=1, col=1
        )
        
        # Gamma
        fig.add_trace(
            go.Scatter(x=spots, y=gammas, name='Gamma', line=dict(color='#51cf66', width=2)),
            row=1, col=2
        )
        
        # Vega
        fig.add_trace(
            go.Scatter(x=spots, y=vegas, name='Vega', line=dict(color='#ff6b6b', width=2)),
            row=2, col=1
        )
        
        # Theta
        fig.add_trace(
            go.Scatter(x=spots, y=thetas, name='Theta', line=dict(color='#ffd43b', width=2)),
            row=2, col=2
        )
        
        # Add ATM lines
        for row in [1, 2]:
            for col in [1, 2]:
                fig.add_vline(x=self.S0, line_dash="dash", line_color='white',
                            row=row, col=col, opacity=0.3)
        
        fig.update_xaxes(title_text="Spot Price")
        fig.update_yaxes(title_text="Greek Value")
        
        fig.update_layout(
            template='plotly_dark',
            height=800,
            showlegend=False,
            title_text="Options Greeks Dashboard"
        )
        
        return fig

# Create standalone dashboard
def create_greeks_app():
    """Create Greeks dashboard app"""
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
    
    visualizer = GreeksVisualizer()
    
    app.layout = dbc.Container(fluid=True, children=[
        dbc.Row([
            dbc.Col([
                html.H1('Options Greeks Visualizer', 
                       style={'color': '#00d4ff', 'textAlign': 'center', 'marginTop': '20px'})
            ])
        ]),
        
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=visualizer.create_delta_surface())
            ], width=12)
        ]),
        
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=visualizer.create_comprehensive_dashboard())
            ], width=12)
        ])
    ])
    
    return app

if __name__ == "__main__":
    app = create_greeks_app()
    print("Greeks Dashboard: http://localhost:8052")
    app.run(debug=False, port=8052)
