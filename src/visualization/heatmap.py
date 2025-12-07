"""
Volatility heatmap visualization
Like Bloomberg correlation matrices
"""
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime

class VolatilityHeatmap:
    """Generate professional heatmaps"""
    
    def __init__(self):
        self.pairs = ['NEO/USDT', 'GAS/USDT', 'BTC/USDT', 'ETH/USDT', 'BNB/USDT']
    
    def create_correlation_heatmap(self):
        """Correlation matrix heatmap"""
        
        # Generate sample correlation data
        n = len(self.pairs)
        correlation_matrix = np.eye(n)
        
        for i in range(n):
            for j in range(i+1, n):
                corr = np.random.uniform(0.3, 0.9)
                correlation_matrix[i, j] = corr
                correlation_matrix[j, i] = corr
        
        df = pd.DataFrame(
            correlation_matrix,
            index=self.pairs,
            columns=self.pairs
        )
        
        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=df.values,
            x=df.columns,
            y=df.index,
            colorscale=[
                [0, '#ff0000'],      # Red (negative)
                [0.5, '#ffffff'],    # White (neutral)
                [1, '#00ff00']       # Green (positive)
            ],
            text=np.round(df.values, 2),
            texttemplate='%{text}',
            textfont={"size": 12},
            colorbar=dict(
                title=dict(text="Correlation"),
                tickmode="linear",
                tick0=0,
                dtick=0.25
            )
        ))
        
        fig.update_layout(
            title='Price Correlation Matrix',
            xaxis_title='',
            yaxis_title='',
            template='plotly_dark',
            paper_bgcolor='#0a0a0a',
            plot_bgcolor='#1a1a1a',
            font=dict(family='Courier New', size=12),
            height=600,
            width=700
        )
        
        return fig
    
    def create_volatility_surface_heatmap(self):
        """Volatility surface heatmap (Strike vs Maturity)"""
        
        # Generate volatility surface data
        strikes = np.arange(80, 121, 5)
        maturities = [7, 14, 30, 60, 90, 180, 365]
        
        vol_surface = []
        for maturity in maturities:
            row = []
            for strike in strikes:
                # Volatility smile
                moneyness = strike / 100
                vol = 0.50 + 0.15 * (abs(moneyness - 1.0)) ** 2
                vol += np.random.normal(0, 0.02)
                row.append(vol * 100)
            vol_surface.append(row)
        
        fig = go.Figure(data=go.Heatmap(
            z=vol_surface,
            x=strikes,
            y=maturities,
            colorscale='RdYlGn_r',
            text=np.round(vol_surface, 1),
            texttemplate='%{text}%',
            textfont={"size": 10},
            colorbar=dict(title="IV %")
        ))
        
        fig.update_layout(
            title='Implied Volatility Surface',
            xaxis_title='Strike Price',
            yaxis_title='Days to Expiry',
            template='plotly_dark',
            paper_bgcolor='#0a0a0a',
            plot_bgcolor='#1a1a1a',
            font=dict(family='Courier New', size=12),
            height=600,
            width=800
        )
        
        return fig
    
    def create_time_volatility_heatmap(self):
        """Time-based volatility heatmap (hour x day)"""
        
        # Generate hourly volatility data
        hours = list(range(24))
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        
        vol_data = []
        for day in days:
            row = []
            for hour in hours:
                # Simulate higher volatility during trading hours
                base_vol = 50
                if 9 <= hour <= 16:  # Trading hours
                    vol = base_vol + np.random.uniform(5, 15)
                else:
                    vol = base_vol + np.random.uniform(-5, 5)
                row.append(vol)
            vol_data.append(row)
        
        fig = go.Figure(data=go.Heatmap(
            z=vol_data,
            x=hours,
            y=days,
            colorscale='Viridis',
            text=np.round(vol_data, 1),
            texttemplate='%{text}%',
            textfont={"size": 9},
            colorbar=dict(title="Vol %")
        ))
        
        fig.update_layout(
            title='Volatility by Day & Hour (UTC)',
            xaxis_title='Hour of Day',
            yaxis_title='Day of Week',
            template='plotly_dark',
            paper_bgcolor='#0a0a0a',
            plot_bgcolor='#1a1a1a',
            font=dict(family='Courier New', size=12),
            height=500,
            width=900
        )
        
        return fig
    
    def create_greeks_heatmap(self):
        """Options Greeks heatmap"""
        
        strikes = np.arange(90, 111, 2)
        greeks = ['Delta', 'Gamma', 'Vega', 'Theta', 'Rho']
        
        greeks_data = []
        for greek in greeks:
            row = []
            for strike in strikes:
                if greek == 'Delta':
                    value = 0.5 + (100 - strike) / 20
                elif greek == 'Gamma':
                    value = 0.02 * (1 - abs(strike - 100) / 20)
                elif greek == 'Vega':
                    value = 0.15 * (1 - abs(strike - 100) / 30)
                elif greek == 'Theta':
                    value = -0.08 * (1 - abs(strike - 100) / 25)
                else:  # Rho
                    value = 0.05 * (strike / 100)
                
                row.append(value)
            greeks_data.append(row)
        
        fig = go.Figure(data=go.Heatmap(
            z=greeks_data,
            x=strikes,
            y=greeks,
            colorscale='RdBu',
            text=np.round(greeks_data, 3),
            texttemplate='%{text}',
            textfont={"size": 10}
        ))
        
        fig.update_layout(
            title='Options Greeks by Strike',
            xaxis_title='Strike Price',
            yaxis_title='Greek',
            template='plotly_dark',
            paper_bgcolor='#0a0a0a',
            plot_bgcolor='#1a1a1a',
            font=dict(family='Courier New', size=12),
            height=500,
            width=800
        )
        
        return fig
    
    def save_all_heatmaps(self):
        """Generate and save all heatmaps"""
        
        print("Generating heatmaps...")
        
        # Correlation matrix
        fig1 = self.create_correlation_heatmap()
        fig1.write_html('outputs/heatmap_correlation.html')
        print("OK Correlation heatmap saved")
        
        # Volatility surface
        fig2 = self.create_volatility_surface_heatmap()
        fig2.write_html('outputs/heatmap_vol_surface.html')
        print("OK Volatility surface heatmap saved")
        
        # Time-based volatility
        fig3 = self.create_time_volatility_heatmap()
        fig3.write_html('outputs/heatmap_time_vol.html')
        print("OK Time volatility heatmap saved")
        
        # Greeks
        fig4 = self.create_greeks_heatmap()
        fig4.write_html('outputs/heatmap_greeks.html')
        print("OK Greeks heatmap saved")
        
        print("\nOK All heatmaps saved to outputs/")

if __name__ == "__main__":
    heatmap_gen = VolatilityHeatmap()
    heatmap_gen.save_all_heatmaps()
