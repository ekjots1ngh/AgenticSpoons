"""
Test Advanced Analytics Dashboard
"""
import json
import pandas as pd
from pathlib import Path
from loguru import logger

def test_analytics():
    """Test analytics module"""
    logger.info("Testing Advanced Analytics Dashboard...")
    
    # Test 1: Load analytics module
    try:
        from src.dashboard.analytics_page import (
            create_analytics_layout,
            create_correlation_matrix,
            create_distribution_plot,
            create_qq_plot,
            create_acf_plot,
            create_var_plot
        )
        logger.success("✓ Analytics module imports successfully")
    except Exception as e:
        logger.error(f"✗ Failed to import analytics module: {e}")
        return False
    
    # Test 2: Load data
    try:
        with open('data/results.json', 'r') as f:
            data = json.load(f)
        logger.success(f"✓ Loaded {len(data)} data points")
    except Exception as e:
        logger.error(f"✗ Failed to load data: {e}")
        return False
    
    # Test 3: Create correlation matrix
    try:
        fig = create_correlation_matrix(data)
        logger.success("✓ Correlation matrix created")
    except Exception as e:
        logger.error(f"✗ Failed to create correlation matrix: {e}")
    
    # Test 4: Create distribution plot
    try:
        fig = create_distribution_plot(data)
        logger.success("✓ Distribution plot created")
    except Exception as e:
        logger.error(f"✗ Failed to create distribution plot: {e}")
    
    # Test 5: Create Q-Q plot
    try:
        fig = create_qq_plot(data)
        logger.success("✓ Q-Q plot created")
    except Exception as e:
        logger.error(f"✗ Failed to create Q-Q plot: {e}")
    
    # Test 6: Create ACF plot
    try:
        fig = create_acf_plot(data)
        logger.success("✓ ACF plot created")
    except Exception as e:
        logger.error(f"✗ Failed to create ACF plot: {e}")
    
    # Test 7: Create VaR plot
    try:
        fig = create_var_plot(data)
        logger.success("✓ VaR plot created")
    except Exception as e:
        logger.error(f"✗ Failed to create VaR plot: {e}")
    
    # Test 8: Dashboard layout
    try:
        layout = create_analytics_layout()
        logger.success("✓ Analytics layout created")
    except Exception as e:
        logger.error(f"✗ Failed to create analytics layout: {e}")
    
    # Test 9: Analytics dashboard imports
    try:
        from src.dashboard.analytics_dashboard import app
        logger.success("✓ Analytics dashboard app imports successfully")
    except Exception as e:
        logger.error(f"✗ Failed to import analytics dashboard: {e}")
        return False
    
    # Summary statistics
    print("\n" + "="*60)
    print("📊 Analytics Summary:")
    df = pd.DataFrame(data)
    
    print(f"\n   Total Records: {len(df)}")
    print(f"   Unique Pairs: {df['pair'].nunique()}")
    print(f"   Price Range: ${df['price'].min():.2f} - ${df['price'].max():.2f}")
    
    # Returns analysis
    returns = df['price'].pct_change().dropna()
    print(f"\n   Returns Analysis:")
    print(f"      Mean: {returns.mean():.4f} ({returns.mean()*100:.2f}%)")
    print(f"      Std Dev: {returns.std():.4f} ({returns.std()*100:.2f}%)")
    print(f"      Skewness: {returns.skew():.4f}")
    print(f"      Kurtosis: {returns.kurtosis():.4f}")
    
    # Volatility analysis
    vols = df['realized_vol'].dropna()
    if len(vols) > 0:
        print(f"\n   Volatility Analysis:")
        print(f"      Mean: {vols.mean():.4f}")
        print(f"      Std Dev: {vols.std():.4f}")
        print(f"      Min: {vols.min():.4f}")
        print(f"      Max: {vols.max():.4f}")
    
    print("\n" + "="*60)
    logger.success("Analytics dashboard tests complete!")
    
    return True

if __name__ == "__main__":
    test_analytics()
