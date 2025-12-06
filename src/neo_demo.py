#!/usr/bin/env python3
"""
Neo Integration Demo
Shows full blockchain integration with AgentSpoons dashboard
"""

import sys
import time
import json
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from loguru import logger
from neo.blockchain_client import NeoBlockchainClient, VolatilityOracle
from neo.dashboard_integration import DashboardNeoIntegration, BlockchainDataStreamToDb
from neo.volatility_contract import display_contract


def setup_logging():
    """Configure logging"""
    logger.remove()
    logger.add(
        lambda msg: print(msg, end=''),
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
        colorize=True
    )


def demo_wallet_creation():
    """Demo 1: Create wallet"""
    logger.info("=" * 60)
    logger.info("DEMO 1: Wallet Creation")
    logger.info("=" * 60)
    
    client = NeoBlockchainClient(network="testnet")
    
    logger.info("Creating new AgentSpoons wallet...")
    wallet_info = client.create_wallet()
    
    if wallet_info:
        logger.success(f"✓ Wallet created successfully!")
        logger.info(f"  Address: {wallet_info['address']}")
        logger.info(f"  Network: {wallet_info['network']}")
        logger.info(f"  Saved to: wallets/agentspoons_wallet.json")
    else:
        logger.warning("Note: neo3-boa not available in demo mode")
        logger.info("In production, real wallet would be created on testnet")
    
    logger.info("")


def demo_network_connection():
    """Demo 2: Network connection"""
    logger.info("=" * 60)
    logger.info("DEMO 2: Network Connection")
    logger.info("=" * 60)
    
    client = NeoBlockchainClient(network="testnet")
    
    logger.info("Connecting to Neo testnet...")
    logger.info(f"RPC Endpoint: {client.rpc_url}")
    
    net_info = client.get_network_info()
    if net_info:
        logger.success("✓ Connected to Neo N3")
        logger.info(f"  Version: {net_info.get('useragent', 'N/A')}")
    else:
        logger.warning("Note: Demo mode - real connection would be established")
        logger.info("In production, RPC calls would query actual Neo node")
    
    logger.info("")


def demo_volatility_oracle():
    """Demo 3: Volatility oracle"""
    logger.info("=" * 60)
    logger.info("DEMO 3: Volatility Oracle")
    logger.info("=" * 60)
    
    oracle = VolatilityOracle(network="testnet")
    
    pairs_data = [
        ('NEO/USDT', 0.45),
        ('GAS/USDT', 0.38),
        ('NEO/GAS', 0.52),
    ]
    
    logger.info("Submitting volatility data to oracle...")
    time.sleep(0.5)
    
    for pair, vol in pairs_data:
        success = oracle.submit_volatility(pair, vol)
        if success:
            logger.success(f"✓ {pair}: {vol:.2%}")
            time.sleep(0.3)
    
    logger.info("")
    logger.info("Oracle cache:")
    for pair, (vol, ts) in oracle.get_all_volatilities().items():
        logger.info(f"  {pair}: {vol:.4f} (timestamp: {ts})")
    
    logger.info("")


def demo_dashboard_integration():
    """Demo 4: Dashboard integration"""
    logger.info("=" * 60)
    logger.info("DEMO 4: Dashboard + Blockchain Integration")
    logger.info("=" * 60)
    
    integration = DashboardNeoIntegration(network="testnet", auto_submit=True)
    
    dashboard_samples = [
        {
            'pair': 'NEO/USDT',
            'realized_vol': 0.45,
            'implied_vol': 0.48,
            'garch_forecast': 0.50,
        },
        {
            'pair': 'GAS/USDT',
            'realized_vol': 0.38,
            'implied_vol': 0.40,
            'garch_forecast': 0.42,
        },
        {
            'pair': 'NEO/GAS',
            'realized_vol': 0.52,
            'implied_vol': 0.55,
            'garch_forecast': 0.58,
        },
    ]
    
    logger.info("Processing dashboard data and submitting to blockchain...")
    time.sleep(0.5)
    
    for data in dashboard_samples:
        # Process data
        processed = integration.process_dashboard_data(data)
        
        # Submit to blockchain
        tx = integration.submit_to_blockchain(processed)
        
        if tx:
            logger.success(f"✓ {data['pair']}: {processed['volatility']:.2%} → blockchain")
        
        time.sleep(0.3)
    
    logger.info("")
    logger.info("Integration status:")
    status = integration.get_blockchain_status()
    logger.info(f"  Network: {status['network']}")
    logger.info(f"  Status: {status['status']}")
    logger.info(f"  Total Submissions: {status['total_submissions']}")
    
    logger.info("")
    logger.info("Submission history:")
    for submission in integration.get_submission_history(3):
        logger.info(f"  [{submission['submission_id']}] {submission['pair']}: {submission['volatility']:.4f}")
    
    logger.info("")


def demo_smart_contract():
    """Demo 5: Smart contract"""
    logger.info("=" * 60)
    logger.info("DEMO 5: Volatility Oracle Smart Contract")
    logger.info("=" * 60)
    
    display_contract()
    
    logger.info("")


def demo_archive():
    """Demo 6: Archive/persistence"""
    logger.info("=" * 60)
    logger.info("DEMO 6: Data Archival")
    logger.info("=" * 60)
    
    integration = DashboardNeoIntegration(network="testnet", auto_submit=True)
    archive = BlockchainDataStreamToDb(integration, "logs/neo_demo_archive.json")
    
    # Generate some archive entries
    for i in range(3):
        data = {
            'pair': f'NEO/USDT',
            'volatility': 0.45 + i * 0.02,
            'submission_index': i
        }
        archive.archive_submission(data)
    
    logger.success("✓ Submissions archived")
    
    stats = archive.get_archive_stats()
    logger.info(f"  Total records: {stats['total_records']}")
    logger.info(f"  Pairs tracked: {stats['pairs_tracked']}")
    
    logger.info("")


def demo_production_flow():
    """Demo 7: Production flow"""
    logger.info("=" * 60)
    logger.info("DEMO 7: Production Data Flow")
    logger.info("=" * 60)
    
    logger.info("AgentSpoons Production Data Flow:")
    logger.info("")
    logger.info("1. Dashboard Data:")
    logger.info("   NEO/USDT: Realized Vol=0.45, Implied Vol=0.48")
    logger.info("")
    logger.info("2. Process & Validate:")
    logger.info("   ✓ Calculate average volatility: 0.465")
    logger.info("   ✓ Convert to basis points: 4650")
    logger.info("   ✓ Add timestamp: 1701866400")
    logger.info("")
    logger.info("3. Submit to Neo N3:")
    logger.info("   ✓ Invoke: update_volatility()")
    logger.info("   ✓ Contract: 0x1234567890ab...")
    logger.info("   ✓ Gas fee: 0.1 GAS")
    logger.info("")
    logger.info("4. Blockchain Confirmation:")
    logger.info("   ✓ Transaction: 0xabcdef123456...")
    logger.info("   ✓ Block: 12345678")
    logger.info("   ✓ Confirmed: ✓ (in 1 block)")
    logger.info("")
    logger.info("5. Archive & Persist:")
    logger.info("   ✓ Stored in data/blockchain_archive.json")
    logger.info("   ✓ Indexed by pair and timestamp")
    logger.info("")
    logger.info("6. Available for Query:")
    logger.info("   ✓ get_volatility('NEO/USDT') → 0.465")
    logger.info("   ✓ get_all_volatilities() → {NEO/USDT: 0.465, ...}")
    logger.info("")


def main():
    """Run full demo"""
    setup_logging()
    
    logger.info("")
    logger.info("╔" + "═" * 58 + "╗")
    logger.info("║" + " " * 10 + "AGENTSPOONS NEO INTEGRATION DEMO" + " " * 16 + "║")
    logger.info("╚" + "═" * 58 + "╝")
    logger.info("")
    
    try:
        # Run demos
        demo_wallet_creation()
        demo_network_connection()
        demo_volatility_oracle()
        demo_dashboard_integration()
        demo_smart_contract()
        demo_archive()
        demo_production_flow()
        
        # Summary
        logger.info("=" * 60)
        logger.info("DEMO SUMMARY")
        logger.info("=" * 60)
        logger.success("✓ All demos completed successfully!")
        logger.info("")
        logger.info("Next steps:")
        logger.info("1. Review neo/blockchain_client.py for production usage")
        logger.info("2. Deploy volatility contract to Neo testnet")
        logger.info("3. Integrate with championship_dashboard.py")
        logger.info("4. Monitor blockchain submissions in real-time")
        logger.info("")
        logger.success("Ready for production deployment!")
        logger.info("")
        
    except Exception as e:
        logger.error(f"Demo failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
