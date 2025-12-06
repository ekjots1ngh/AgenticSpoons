"""
Advanced Quantitative Analytics
- Risk metrics (VaR, CVaR, Maximum Drawdown)
- Portfolio optimization
- Factor models
- Copula analysis
"""
import numpy as np
import pandas as pd
from scipy import stats
from scipy.optimize import minimize
import matplotlib.pyplot as plt

class RiskMetrics:
    """Calculate various risk metrics"""
    
    @staticmethod
    def value_at_risk(returns, confidence=0.95, method='historical'):
        """
        Calculate Value at Risk
        
        Methods:
        - historical: Use empirical quantile
        - parametric: Assume normal distribution
        - cornish_fisher: Adjust for skewness and kurtosis
        """
        if method == 'historical':
            var = np.percentile(returns, (1 - confidence) * 100)
        
        elif method == 'parametric':
            mu = np.mean(returns)
            sigma = np.std(returns)
            var = stats.norm.ppf(1 - confidence, mu, sigma)
        
        elif method == 'cornish_fisher':
            # Cornish-Fisher expansion
            mu = np.mean(returns)
            sigma = np.std(returns)
            skew = stats.skew(returns)
            kurt = stats.kurtosis(returns)
            
            z = stats.norm.ppf(1 - confidence)
            z_cf = (z + (z**2 - 1) * skew / 6 +
                   (z**3 - 3*z) * kurt / 24 -
                   (2*z**3 - 5*z) * skew**2 / 36)
            
            var = mu + sigma * z_cf
        
        return var
    
    @staticmethod
    def conditional_var(returns, confidence=0.95):
        """
        Calculate Conditional VaR (Expected Shortfall)
        Average of losses beyond VaR
        """
        var = RiskMetrics.value_at_risk(returns, confidence, 'historical')
        cvar = returns[returns <= var].mean()
        return cvar
    
    @staticmethod
    def maximum_drawdown(prices):
        """Calculate maximum drawdown"""
        cumulative = np.maximum.accumulate(prices)
        drawdown = (prices - cumulative) / cumulative
        return np.min(drawdown)
    
    @staticmethod
    def sharpe_ratio(returns, risk_free_rate=0.02):
        """Sharpe ratio (annualized)"""
        excess_returns = returns - risk_free_rate / 252
        return np.sqrt(252) * np.mean(excess_returns) / np.std(excess_returns)
    
    @staticmethod
    def sortino_ratio(returns, risk_free_rate=0.02):
        """Sortino ratio (uses downside deviation)"""
        excess_returns = returns - risk_free_rate / 252
        downside_returns = returns[returns < 0]
        downside_std = np.std(downside_returns)
        
        if downside_std == 0:
            return 0
        
        return np.sqrt(252) * np.mean(excess_returns) / downside_std
    
    @staticmethod
    def calmar_ratio(returns, prices):
        """Calmar ratio = Annual return / Max drawdown"""
        annual_return = (prices[-1] / prices[0]) ** (252 / len(prices)) - 1
        max_dd = abs(RiskMetrics.maximum_drawdown(prices))
        
        return annual_return / max_dd if max_dd > 0 else 0

class PortfolioOptimizer:
    """Modern Portfolio Theory optimization"""
    
    def __init__(self, returns_matrix):
        """
        returns_matrix: DataFrame with returns for each asset
        """
        self.returns = returns_matrix
        self.mean_returns = returns_matrix.mean()
        self.cov_matrix = returns_matrix.cov()
        self.n_assets = len(self.mean_returns)
    
    def portfolio_stats(self, weights):
        """Calculate portfolio statistics"""
        portfolio_return = np.dot(weights, self.mean_returns) * 252
        portfolio_std = np.sqrt(
            np.dot(weights.T, np.dot(self.cov_matrix * 252, weights))
        )
        
        return portfolio_return, portfolio_std
    
    def negative_sharpe(self, weights, risk_free_rate=0.02):
        """Negative Sharpe ratio for minimization"""
        p_return, p_std = self.portfolio_stats(weights)
        if p_std == 0:
            return 0
        return -(p_return - risk_free_rate) / p_std
    
    def min_variance(self):
        """Find minimum variance portfolio"""
        def portfolio_variance(weights):
            return self.portfolio_stats(weights)[1]
        
        constraints = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
        bounds = tuple((0, 1) for _ in range(self.n_assets))
        initial_guess = np.array([1/self.n_assets] * self.n_assets)
        
        result = minimize(
            portfolio_variance,
            initial_guess,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints
        )
        
        return result.x
    
    def max_sharpe(self, risk_free_rate=0.02):
        """Find maximum Sharpe ratio portfolio"""
        constraints = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
        bounds = tuple((0, 1) for _ in range(self.n_assets))
        initial_guess = np.array([1/self.n_assets] * self.n_assets)
        
        result = minimize(
            self.negative_sharpe,
            initial_guess,
            args=(risk_free_rate,),
            method='SLSQP',
            bounds=bounds,
            constraints=constraints
        )
        
        return result.x
    
    def efficient_frontier(self, n_points=50):
        """Calculate efficient frontier"""
        target_returns = np.linspace(
            self.mean_returns.min() * 252,
            self.mean_returns.max() * 252,
            n_points
        )
        
        efficient_portfolios = []
        
        for target in target_returns:
            constraints = [
                {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},
                {'type': 'eq', 'fun': lambda x: self.portfolio_stats(x)[0] - target}
            ]
            
            bounds = tuple((0, 1) for _ in range(self.n_assets))
            initial_guess = np.array([1/self.n_assets] * self.n_assets)
            
            result = minimize(
                lambda w: self.portfolio_stats(w)[1],
                initial_guess,
                method='SLSQP',
                bounds=bounds,
                constraints=constraints
            )
            
            if result.success:
                p_return, p_std = self.portfolio_stats(result.x)
                efficient_portfolios.append({
                    'return': p_return,
                    'volatility': p_std,
                    'weights': result.x
                })
        
        return efficient_portfolios

class FactorModels:
    """Factor analysis for returns"""
    
    @staticmethod
    def fama_french_3factor(returns, mkt_returns, smb, hml):
        """
        Fama-French 3-factor model
        R_i - R_f = α + β_mkt(R_m - R_f) + β_smb*SMB + β_hml*HML + ε
        """
        from sklearn.linear_model import LinearRegression
        
        # Prepare data
        X = np.column_stack([mkt_returns, smb, hml])
        y = returns
        
        # Fit model
        model = LinearRegression()
        model.fit(X, y)
        
        alpha = model.intercept_
        betas = model.coef_
        r_squared = model.score(X, y)
        
        return {
            'alpha': alpha,
            'beta_market': betas[0],
            'beta_smb': betas[1],
            'beta_hml': betas[2],
            'r_squared': r_squared
        }
    
    @staticmethod
    def pca_factors(returns_matrix, n_components=3):
        """
        Principal Component Analysis for factor extraction
        """
        from sklearn.decomposition import PCA
        from sklearn.preprocessing import StandardScaler
        
        # Standardize
        scaler = StandardScaler()
        returns_scaled = scaler.fit_transform(returns_matrix)
        
        # PCA
        pca = PCA(n_components=n_components)
        factors = pca.fit_transform(returns_scaled)
        
        return {
            'factors': factors,
            'explained_variance': pca.explained_variance_ratio_,
            'components': pca.components_
        }

class CopulaAnalysis:
    """Copula-based dependence analysis"""
    
    @staticmethod
    def gaussian_copula(u, v, rho):
        """
        Gaussian copula
        C(u,v) = Φ_ρ(Φ^(-1)(u), Φ^(-1)(v))
        """
        from scipy.stats import norm, multivariate_normal
        
        # Transform to standard normal
        x = norm.ppf(u)
        y = norm.ppf(v)
        
        # Correlation matrix
        corr = np.array([[1, rho], [rho, 1]])
        
        # Compute copula
        copula = multivariate_normal.cdf([x, y], cov=corr)
        
        return copula
    
    @staticmethod
    def t_copula(u, v, rho, df):
        """
        Student's t-copula
        Better for fat tails
        """
        from scipy.stats import t as student_t
        
        # Transform to t-distribution
        x = student_t.ppf(u, df)
        y = student_t.ppf(v, df)
        
        # For bivariate t-copula, use numerical approximation
        # This is a simplified implementation
        return u * v  # Placeholder
    
    @staticmethod
    def tail_dependence(returns1, returns2, quantile=0.05):
        """
        Calculate tail dependence coefficient
        Measures dependence in extreme events
        """
        # Lower tail
        threshold = np.quantile(returns1, quantile)
        both_low = np.sum((returns1 <= threshold) & (returns2 <= threshold))
        either_low = np.sum((returns1 <= threshold) | (returns2 <= threshold))
        
        lower_tail = both_low / either_low if either_low > 0 else 0
        
        # Upper tail
        threshold = np.quantile(returns1, 1 - quantile)
        both_high = np.sum((returns1 >= threshold) & (returns2 >= threshold))
        either_high = np.sum((returns1 >= threshold) | (returns2 >= threshold))
        
        upper_tail = both_high / either_high if either_high > 0 else 0
        
        return {'lower_tail': lower_tail, 'upper_tail': upper_tail}

# ========== TESTING SCRIPT ==========
def run_quant_analysis():
    """Run comprehensive quantitative analysis"""
    import json
    import os
    
    if not os.path.exists('data/results.json'):
        print("❌ No data file found. Run enhanced_demo.py first.")
        return
    
    with open('data/results.json', 'r') as f:
        data = json.load(f)
    
    # Handle both list and dict formats
    if isinstance(data, dict):
        data = data.get('data', [])
    
    neo_data = [d for d in data if d.get('pair') == 'NEO/USDT']
    
    if len(neo_data) < 50:
        print(f"❌ Need at least 50 data points, found {len(neo_data)}")
        return
    
    print("="*70)
    print("📊 QUANTITATIVE ANALYSIS")
    print("="*70)
    
    # Calculate returns
    prices = np.array([d['price'] for d in neo_data])
    returns = np.diff(np.log(prices))
    
    if len(returns) == 0:
        print("❌ Not enough price data")
        return
    
    # Risk Metrics
    print("\n1. Risk Metrics")
    print("-"*70)
    
    var_95 = RiskMetrics.value_at_risk(returns, 0.95, 'historical')
    cvar_95 = RiskMetrics.conditional_var(returns, 0.95)
    max_dd = RiskMetrics.maximum_drawdown(prices)
    sharpe = RiskMetrics.sharpe_ratio(returns)
    sortino = RiskMetrics.sortino_ratio(returns)
    calmar = RiskMetrics.calmar_ratio(returns, prices)
    
    print(f"   VaR (95%):        {var_95:.2%}")
    print(f"   CVaR (95%):       {cvar_95:.2%}")
    print(f"   Max Drawdown:     {max_dd:.2%}")
    print(f"   Sharpe Ratio:     {sharpe:.2f}")
    print(f"   Sortino Ratio:    {sortino:.2f}")
    print(f"   Calmar Ratio:     {calmar:.2f}")
    
    # Volatility analysis
    print("\n2. Volatility Analysis")
    print("-"*70)
    
    realized_vols = np.array([d.get('realized_vol', 0) for d in neo_data if d.get('realized_vol')])
    
    if len(realized_vols) > 0:
        print(f"   Mean Vol:         {np.mean(realized_vols):.2%}")
        print(f"   Vol Std:          {np.std(realized_vols):.2%}")
        print(f"   Vol Skewness:     {stats.skew(realized_vols):.2f}")
        print(f"   Vol Kurtosis:     {stats.kurtosis(realized_vols):.2f}")
    else:
        print("   ⚠ No volatility data available")
    
    # Distribution analysis
    print("\n3. Return Distribution")
    print("-"*70)
    
    print(f"   Mean Return:      {np.mean(returns):.2%}")
    print(f"   Std Dev:          {np.std(returns):.2%}")
    print(f"   Skewness:         {stats.skew(returns):.2f}")
    print(f"   Kurtosis:         {stats.kurtosis(returns):.2f}")
    print(f"   Min Return:       {np.min(returns):.2%}")
    print(f"   Max Return:       {np.max(returns):.2%}")
    
    print("\n" + "="*70)
    print("✅ Quantitative analysis complete!")
    print("="*70)

if __name__ == "__main__":
    run_quant_analysis()
