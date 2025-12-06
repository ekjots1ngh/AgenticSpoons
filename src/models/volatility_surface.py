"""
Volatility Surface Construction and Interpolation
"""
import numpy as np
import pandas as pd
from scipy.interpolate import griddata, RBFInterpolator, interp1d
from typing import Dict, List, Tuple, Optional
from loguru import logger

class VolatilitySurface:
    """Construct and query volatility surfaces"""
    
    def __init__(self):
        self.strikes = []
        self.maturities = []
        self.implied_vols = []
        self.surface_data = None
        self.spot_price = None
    
    def add_point(self, strike: float, maturity: float, implied_vol: float):
        """Add a single point to the surface"""
        self.strikes.append(strike)
        self.maturities.append(maturity)
        self.implied_vols.append(implied_vol)
    
    def add_points_bulk(self, data: List[Dict]):
        """
        Add multiple points at once
        
        data format: [{'strike': K, 'maturity': T, 'iv': σ}, ...]
        """
        for point in data:
            self.add_point(point['strike'], point['maturity'], point['iv'])
    
    def clear(self):
        """Clear all data points"""
        self.strikes = []
        self.maturities = []
        self.implied_vols = []
        self.surface_data = None
    
    def build_surface(self, method: str = 'cubic', grid_resolution: int = 50) -> Dict:
        """
        Build volatility surface using interpolation
        
        Args:
            method: 'cubic', 'linear', or 'rbf' (radial basis function)
            grid_resolution: Number of points in each dimension
        
        Returns:
            Dict with 'strikes', 'maturities', 'implied_vols' meshgrids
        """
        if len(self.strikes) < 4:
            logger.warning("Need at least 4 points to build surface")
            return {}
        
        try:
            points = np.column_stack([self.strikes, self.maturities])
            values = np.array(self.implied_vols)
            
            # Create interpolation grid
            K_min, K_max = min(self.strikes), max(self.strikes)
            T_min, T_max = min(self.maturities), max(self.maturities)
            
            K_grid = np.linspace(K_min, K_max, grid_resolution)
            T_grid = np.linspace(T_min, T_max, grid_resolution)
            K_mesh, T_mesh = np.meshgrid(K_grid, T_grid)
            
            # Interpolate
            if method == 'rbf':
                rbf = RBFInterpolator(points, values, kernel='thin_plate_spline')
                grid_points = np.column_stack([K_mesh.ravel(), T_mesh.ravel()])
                IV_mesh = rbf(grid_points).reshape(K_mesh.shape)
            else:
                IV_mesh = griddata(points, values, (K_mesh, T_mesh), method=method)
            
            self.surface_data = {
                'strikes': K_mesh,
                'maturities': T_mesh,
                'implied_vols': IV_mesh
            }
            
            logger.success(f"Surface built with {len(self.strikes)} points using {method} interpolation")
            
            return self.surface_data
            
        except Exception as e:
            logger.error(f"Surface building error: {e}")
            return {}
    
    def get_vol(self, strike: float, maturity: float) -> Optional[float]:
        """Query volatility for specific strike and maturity"""
        if len(self.strikes) < 3:
            return None
        
        try:
            points = np.column_stack([self.strikes, self.maturities])
            values = np.array(self.implied_vols)
            
            vol = griddata(points, values, (strike, maturity), method='linear')
            
            if np.isnan(vol):
                # Fallback to nearest neighbor
                vol = griddata(points, values, (strike, maturity), method='nearest')
            
            return float(vol)
            
        except Exception as e:
            logger.error(f"Vol query error: {e}")
            return None
    
    def get_atm_term_structure(self, spot_price: float) -> Dict[float, float]:
        """
        Extract ATM volatility term structure
        
        Returns:
            Dict mapping maturity -> ATM vol
        """
        self.spot_price = spot_price
        atm_vols = {}
        
        unique_maturities = sorted(set(self.maturities))
        
        for T in unique_maturities:
            # Get all strikes for this maturity
            indices = [i for i, mat in enumerate(self.maturities) if abs(mat - T) < 0.001]
            
            if not indices:
                continue
            
            strikes_T = [self.strikes[i] for i in indices]
            vols_T = [self.implied_vols[i] for i in indices]
            
            # Find strike closest to ATM
            atm_idx = np.argmin(np.abs(np.array(strikes_T) - spot_price))
            atm_vols[T] = vols_T[atm_idx]
        
        return atm_vols
    
    def calculate_skew(self, maturity: float, put_strike_pct: float = 0.9, 
                       call_strike_pct: float = 1.1) -> Optional[float]:
        """
        Calculate volatility skew
        
        Skew = IV(OTM Put) - IV(OTM Call)
        
        Args:
            maturity: Target maturity
            put_strike_pct: OTM put strike as % of spot (default 90%)
            call_strike_pct: OTM call strike as % of spot (default 110%)
        """
        if self.spot_price is None:
            logger.warning("Set spot_price before calculating skew")
            return None
        
        try:
            # Get vols for this maturity
            indices = [i for i, T in enumerate(self.maturities) if abs(T - maturity) < 0.01]
            
            if len(indices) < 2:
                return None
            
            strikes_T = np.array([self.strikes[i] for i in indices])
            vols_T = np.array([self.implied_vols[i] for i in indices])
            
            # Sort by strike
            sorted_idx = np.argsort(strikes_T)
            strikes_T = strikes_T[sorted_idx]
            vols_T = vols_T[sorted_idx]
            
            # Interpolate
            interp_func = interp1d(strikes_T, vols_T, kind='linear', 
                                   fill_value='extrapolate')
            
            otm_put_strike = self.spot_price * put_strike_pct
            otm_call_strike = self.spot_price * call_strike_pct
            
            iv_put = float(interp_func(otm_put_strike))
            iv_call = float(interp_func(otm_call_strike))
            
            skew = iv_put - iv_call
            
            return skew
            
        except Exception as e:
            logger.error(f"Skew calculation error: {e}")
            return None
    
    def calculate_smile_curvature(self, maturity: float) -> Optional[float]:
        """
        Calculate volatility smile curvature (convexity)
        
        Measures how "curved" the smile is
        """
        if self.spot_price is None:
            return None
        
        try:
            # Get ATM, 90%, 110% strikes
            atm_vol = self.get_vol(self.spot_price, maturity)
            put_vol = self.get_vol(self.spot_price * 0.9, maturity)
            call_vol = self.get_vol(self.spot_price * 1.1, maturity)
            
            if any(v is None for v in [atm_vol, put_vol, call_vol]):
                return None
            
            # Convexity = (Put + Call - 2*ATM) / ATM
            curvature = (put_vol + call_vol - 2 * atm_vol) / atm_vol
            
            return float(curvature)
            
        except Exception as e:
            logger.error(f"Curvature calculation error: {e}")
            return None
    
    def to_dataframe(self) -> pd.DataFrame:
        """Export surface data to DataFrame"""
        return pd.DataFrame({
            'strike': self.strikes,
            'maturity': self.maturities,
            'implied_vol': self.implied_vols
        })
    
    def get_summary_stats(self) -> Dict:
        """Get summary statistics of the surface"""
        if not self.strikes:
            return {}
        
        return {
            'n_points': len(self.strikes),
            'strike_range': (min(self.strikes), max(self.strikes)),
            'maturity_range': (min(self.maturities), max(self.maturities)),
            'vol_range': (min(self.implied_vols), max(self.implied_vols)),
            'avg_vol': np.mean(self.implied_vols),
            'vol_std': np.std(self.implied_vols)
        }
