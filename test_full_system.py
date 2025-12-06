"""
Comprehensive system test
"""
import asyncio
from src.utils.database import AgentSpoonsDB
from src.config import config


async def test_full_stack():
    print("🧪 Testing Full AgentSpoons Stack\n")
    
    # Test 1: Database
    print("1. Testing Database...")
    db = AgentSpoonsDB("data/test.db")
    print("   ✓ Database created")
    
    # Test 2: Agents can be imported
    print("\n2. Testing Agent Imports...")
    from src.agents.market_data_agent import MarketDataAgent
    from src.agents.volatility_calculator_agent import VolatilityCalculatorAgent
    print("   ✓ All agents import successfully")
    
    # Test 3: Models work
    print("\n3. Testing Quant Models...")
    from src.models.black_scholes import BlackScholesEngine
    call = BlackScholesEngine.call_price(100, 100, 0.25, 0.05, 0.3)
    print(f"   ✓ BS Call Price: ${call:.2f}")
    
    from src.models.garch_forecaster import GARCHForecaster
    import pandas as pd
    import numpy as np
    returns = pd.Series(np.random.normal(0, 0.01, 100))
    garch = GARCHForecaster(returns)
    params = garch.fit()
    print(f"   ✓ GARCH α={params['alpha']:.4f}, β={params['beta']:.4f}")
    
    print("\n" + "="*50)
    print("✅ ALL TESTS PASSED!")
    print("="*50)
    print("\nReady for hackathon demo! 🚀")
    print("\nNext steps:")
    print("1. Run agents: python src/main.py")
    print("2. Run dashboard: python src/dashboard/advanced_app.py")
    print("3. Visit: http://localhost:8050")


if __name__ == "__main__":
    asyncio.run(test_full_stack())
