"""
Interactive 3D Volatility Surface Visualization
"""
import plotly.graph_objs as go
import numpy as np
from scipy.interpolate import griddata, interp2d
from loguru import logger

class VolatilitySurface3D:
    """Create stunning 3D volatility surfaces with smile effects"""
    
    def create_surface(self, strikes, maturities, implied_vols):
        """
        Create interactive 3D surface plot
        
        Parameters:
        -----------
        strikes : list
            Strike prices for the surface
        maturities : list
            Time to maturity in years
        implied_vols : 2D array
            Implied volatilities at each strike-maturity combination
        
        Returns:
        --------
        plotly.graph_objects.Figure
            Interactive 3D surface plot
        """
        
        try:
            # Create grid for smooth interpolation
            strike_grid = np.linspace(min(strikes), max(strikes), 50)
            maturity_grid = np.linspace(min(maturities), max(maturities), 50)
            
            # Create meshgrid
            K, T = np.meshgrid(strike_grid, maturity_grid)
            
            # Create 2D array from implied_vols if needed
            if len(np.array(implied_vols).shape) == 1:
                # 1D array - reshape properly
                n_strikes = len(strikes)
                n_maturities = len(maturities)
                IV_data = np.array(implied_vols).reshape(n_strikes, n_maturities)
            else:
                IV_data = np.array(implied_vols)
            
            # Use linear interpolation - more robust than cubic for this data
            try:
                f = interp2d(strikes, maturities, IV_data.T, kind='linear')
                IV = f(strike_grid, maturity_grid)
            except Exception as interp_error:
                logger.warning(f"interp2d failed, using nearest: {interp_error}")
                # Fallback to nearest neighbor
                points = np.array([[s, m] for s in strikes for m in maturities])
                values = IV_data.flatten()
                IV = griddata(points, values, (K, T), method='nearest')
            
            # Create 3D surface trace
            surface = go.Surface(
                x=K,
                y=T,
                z=IV * 100,  # Convert to percentage
                colorscale='Viridis',
                name='Implied Volatility',
                hovertemplate='Strike: %{x:.2f}<br>Maturity: %{y:.2f}y<br>IV: %{z:.1f}%<extra></extra>',
                colorbar=dict(
                    title='IV %',
                    thickness=15,
                    len=0.7
                )
            )
            
            # Create figure
            fig = go.Figure(data=[surface])
            
            # Update layout with professional styling
            fig.update_layout(
                title={
                    'text': 'Volatility Surface',
                    'font': {'size': 24, 'color': '#00D9FF'},
                    'x': 0.5,
                    'xanchor': 'center'
                },
                scene=dict(
                    xaxis_title='Strike Price',
                    yaxis_title='Time to Maturity (years)',
                    zaxis_title='Implied Volatility (%)',
                    camera=dict(
                        eye=dict(x=1.5, y=1.5, z=1.3),
                        center=dict(x=0, y=0, z=0)
                    ),
                    bgcolor='rgba(10, 14, 39, 0.9)',
                    xaxis=dict(
                        backgroundcolor='rgba(20, 30, 60, 0.5)',
                        gridcolor='#1a3a52',
                        showbackground=True,
                        zerolinecolor='#1a3a52'
                    ),
                    yaxis=dict(
                        backgroundcolor='rgba(20, 30, 60, 0.5)',
                        gridcolor='#1a3a52',
                        showbackground=True,
                        zerolinecolor='#1a3a52'
                    ),
                    zaxis=dict(
                        backgroundcolor='rgba(20, 30, 60, 0.5)',
                        gridcolor='#1a3a52',
                        showbackground=True,
                        zerolinecolor='#1a3a52'
                    )
                ),
                template='plotly_dark',
                paper_bgcolor='#0a0e27',
                plot_bgcolor='#0a0e27',
                height=700,
                width=1000,
                margin=dict(l=0, r=0, t=60, b=0),
                hovermode='closest',
                showlegend=True
            )
            
            logger.info("3D volatility surface created successfully")
            return fig
            
        except Exception as e:
            logger.error(f"Error creating surface: {e}")
            return None
    
    def generate_sample_surface(self):
        """Generate realistic sample volatility surface for demonstration"""
        
        # Strike range: 80% to 120% of spot
        spot = 100.0
        strikes = np.linspace(spot * 0.8, spot * 1.2, 25)
        
        # Maturities: 1 week to 1 year
        maturities = np.linspace(7/365, 1.0, 20)
        
        # Generate implied volatilities with realistic smile and term structure
        implied_vols = []
        
        for K in strikes:
            row = []
            for T in maturities:
                # Base ATM volatility
                atm_vol = 0.45
                
                # Volatility smile - OTM options have higher volatility
                moneyness = K / spot
                smile_effect = 0.08 * ((moneyness - 1.0) ** 2)
                
                # Term structure - longer maturity typically higher vol
                term_effect = 0.12 * np.sqrt(T)
                
                # Mean reversion - very short term can be different
                if T < 0.05:
                    term_effect *= 0.8
                
                # Combine effects
                iv = atm_vol + smile_effect + term_effect
                
                # Add slight randomness for realism
                iv += np.random.normal(0, 0.02)
                
                # Ensure positive and reasonable
                iv = np.clip(iv, 0.1, 2.0)
                
                row.append(iv)
            
            implied_vols.append(row)
        
        logger.info(f"Generated sample surface: {len(strikes)} strikes x {len(maturities)} maturities")
        return self.create_surface(strikes.tolist(), maturities.tolist(), implied_vols)
    
    def create_real_data_surface(self, volatility_data):
        """Create surface from real volatility data"""
        
        try:
            # Extract strikes and maturities from data
            strikes = sorted(set(d.get('strike', 100) for d in volatility_data))
            maturities = sorted(set(d.get('maturity', 0.25) for d in volatility_data))
            
            # Create 2D array of implied vols
            implied_vols = []
            for s in strikes:
                row = []
                for m in maturities:
                    # Find matching data point
                    matching = [d for d in volatility_data 
                               if abs(d.get('strike', 100) - s) < 0.1 
                               and abs(d.get('maturity', 0.25) - m) < 0.01]
                    
                    iv = matching[0].get('implied_vol', 0.25) if matching else 0.25
                    row.append(iv)
                
                implied_vols.append(row)
            
            return self.create_surface(strikes, maturities, implied_vols)
            
        except Exception as e:
            logger.error(f"Error creating real data surface: {e}")
            return self.generate_sample_surface()

# Volatility smile visualizer
class VolatilitySmile:
    """Create 2D volatility smile plots"""
    
    @staticmethod
    def create_smile(strikes, implied_vols, maturity=0.25):
        """Create volatility smile visualization"""
        
        fig = go.Figure()
        
        # Add scatter and line
        fig.add_trace(go.Scatter(
            x=strikes,
            y=np.array(implied_vols) * 100,
            mode='lines+markers',
            name='Vol Smile',
            line=dict(color='#00D9FF', width=3),
            marker=dict(size=8, color='#00D9FF', symbol='circle'),
            hovertemplate='Strike: %{x:.0f}<br>IV: %{y:.1f}%<extra></extra>'
        ))
        
        fig.update_layout(
            title=f'Volatility Smile (T={maturity:.2f}y)',
            xaxis_title='Strike Price',
            yaxis_title='Implied Volatility (%)',
            template='plotly_dark',
            paper_bgcolor='#0a0e27',
            plot_bgcolor='#1a1f3a',
            hovermode='x unified',
            height=400,
            showlegend=True
        )
        
        return fig

# Term structure visualizer
class TermStructure:
    """Create term structure of volatility plots"""
    
    @staticmethod
    def create_term_structure(maturities, volatilities):
        """Create term structure visualization"""
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=np.array(maturities) * 365,  # Convert to days
            y=np.array(volatilities) * 100,
            mode='lines+markers',
            name='Term Structure',
            line=dict(color='#FF006E', width=3),
            marker=dict(size=8, color='#FF006E', symbol='diamond'),
            hovertemplate='Days: %{x:.0f}<br>IV: %{y:.1f}%<extra></extra>'
        ))
        
        fig.update_layout(
            title='Volatility Term Structure',
            xaxis_title='Days to Maturity',
            yaxis_title='Implied Volatility (%)',
            template='plotly_dark',
            paper_bgcolor='#0a0e27',
            plot_bgcolor='#1a1f3a',
            hovermode='x',
            height=400,
            showlegend=True
        )
        
        return fig

if __name__ == "__main__":
    # Test 3D surface
    surf = VolatilitySurface3D()
    fig = surf.generate_sample_surface()
    
    if fig:
        fig.write_html('data/vol_surface_3d.html')
        logger.info("3D surface saved to data/vol_surface_3d.html")
    
    # Test smile
    strikes = np.linspace(80, 120, 20)
    ivs = 0.25 + 0.05 * ((strikes - 100) / 100) ** 2
    smile_fig = VolatilitySmile.create_smile(strikes, ivs)
    smile_fig.write_html('data/vol_smile.html')
    logger.info("Vol smile saved to data/vol_smile.html")
    
    # Test term structure
    terms = np.linspace(0.05, 1.0, 20)
    vols = 0.25 + 0.1 * np.sqrt(terms)
    term_fig = TermStructure.create_term_structure(terms, vols)
    term_fig.write_html('data/term_structure.html')
    logger.info("Term structure saved to data/term_structure.html")
