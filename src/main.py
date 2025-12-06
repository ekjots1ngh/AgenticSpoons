"""
AgentSpoons - Main Entry Point
Multi-agent volatility oracle system for Neo blockchain
"""
import asyncio
import sys
from loguru import logger

from config import config
from agents.market_data_agent import MarketDataAgent
from agents.volatility_calculator_agent import VolatilityCalculatorAgent
from agents.implied_vol_agent import ImpliedVolAgent
from agents.arbitrage_detector_agent import ArbitrageDetectorAgent
from agents.oracle_publisher_agent import OraclePublisherAgent

# Configure logging
logger.remove()
logger.add(
    sys.stderr,
    level=config.LOG_LEVEL,
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>"
)
logger.add(
    "logs/agentspoons_{time:YYYY-MM-DD}.log",
    rotation="1 day",
    retention="7 days",
    level="DEBUG"
)

async def main():
    """Main function - orchestrate all agents"""
    
    logger.info("=" * 60)
    logger.info("🥄 AgentSpoons - Decentralized Volatility Oracle")
    logger.info("=" * 60)
    logger.info(f"Tracking pairs: {config.TOKEN_PAIRS}")
    logger.info(f"Network: {config.NEO_NETWORK}")
    logger.info("=" * 60)
    
    # Initialize Agent 1: Market Data Collector
    market_data_agent = MarketDataAgent(
        agent_id="MarketDataCollector",
        wallet_address=config.WALLET_PATH,
        token_pairs=config.TOKEN_PAIRS,
        dex_endpoints=config.DEX_ENDPOINTS
    )
    
    # Initialize Agent 2: Volatility Calculator
    vol_calculator_agent = VolatilityCalculatorAgent(
        agent_id="VolatilityCalculator",
        wallet_address=config.WALLET_PATH,
        market_data_agent=market_data_agent
    )
    
    # Initialize Agent 3: Implied Vol Engine
    implied_vol_agent = ImpliedVolAgent(
        agent_id="ImpliedVolEngine",
        wallet_address=config.WALLET_PATH,
        market_data_agent=market_data_agent,
        risk_free_rate=config.RISK_FREE_RATE
    )
    
    # Initialize Agent 4: Arbitrage Detector
    arbitrage_agent = ArbitrageDetectorAgent(
        agent_id="ArbitrageDetector",
        wallet_address=config.WALLET_PATH,
        vol_calculator=vol_calculator_agent,
        implied_vol_agent=implied_vol_agent,
        threshold=0.10  # 10% threshold
    )
    
    # Initialize Agent 5: Oracle Publisher
    oracle_agent = OraclePublisherAgent(
        agent_id="OraclePublisher",
        wallet_address=config.WALLET_PATH,
        vol_calculator=vol_calculator_agent,
        implied_vol_agent=implied_vol_agent,
        contract_hash=""  # Add your Neo contract hash
    )
    
    logger.info("✓ All agents initialized")
    logger.info("Starting agent loops...")
    
    # Run all agents concurrently
    tasks = [
        market_data_agent.run(),
        vol_calculator_agent.run(),
        implied_vol_agent.run(),
        arbitrage_agent.run(),
        oracle_agent.run()
    ]
    
    try:
        await asyncio.gather(*tasks)
    except KeyboardInterrupt:
        logger.info("\nShutting down AgentSpoons...")
        
        # Stop all agents gracefully
        market_data_agent.stop()
        vol_calculator_agent.stop()
        implied_vol_agent.stop()
        arbitrage_agent.stop()
        oracle_agent.stop()
        
        logger.info("✓ All agents stopped")

if __name__ == "__main__":
    asyncio.run(main())
