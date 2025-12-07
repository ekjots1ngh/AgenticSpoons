"""
LIVE DEMO: Publish volatility to Neo in real-time
Run this during your presentation!
"""
import asyncio
import numpy as np
from datetime import datetime
from live_neo_publisher import LiveNeoPublisher

async def live_demo():
    """
    Run live publishing demo
    This actually publishes to Neo testnet!
    """
    
    print("="*70)
    print("🚀 LIVE NEO PUBLISHING DEMO")
    print("="*70)
    
    # Initialize publisher
    publisher = LiveNeoPublisher(
        contract_hash="0xYOUR_CONTRACT_HASH",  # Fill this in
        wallet_path="agentspoons_wallet.json",
        password="agentspoons2024"
    )
    
    print(f"\n📍 Publishing from: {publisher.account.address}")
    print(f"🔗 Contract: {publisher.contract_hash}")
    print(f"🌐 Network: Neo N3 Testnet\n")
    
    # Simulate 5 live updates
    pairs = ["NEO/USDT", "GAS/USDT"]
    
    for i in range(5):
        print(f"\n{'='*70}")
        print(f"📊 UPDATE #{i+1}/5 - {datetime.now().strftime('%H:%M:%S')}")
        print(f"{'='*70}")
        
        for pair in pairs:
            # Generate realistic data
            price = 15.0 + np.random.normal(0, 0.5) if pair == "NEO/USDT" else 5.0 + np.random.normal(0, 0.2)
            rv = 0.50 + np.random.normal(0, 0.05)
            iv = rv * (1.05 + np.random.normal(0, 0.02))
            
            # Publish to blockchain
            tx_hash = publisher.publish_volatility(pair, price, rv, iv)
            
            if tx_hash:
                print(f"   ✅ On-chain!")
            
            await asyncio.sleep(2)  # Wait between publications
        
        if i < 4:
            print(f"\n⏳ Next update in 10 seconds...")
            await asyncio.sleep(10)
    
    # Show stats
    stats = publisher.get_publication_stats()
    
    print(f"\n{'='*70}")
    print("📈 PUBLICATION STATISTICS")
    print(f"{'='*70}")
    print(f"Total Publications: {stats['total_publications']}")
    print(f"Total GAS Used: {stats['total_gas_used']:.8f} GAS")
    print(f"Pairs Published: {', '.join(stats['pairs_published'])}")
    print(f"Duration: {stats['first_publication']} → {stats['last_publication']}")
    print(f"\n💾 All publications saved to: data/neo_publications.jsonl")
    print(f"🔗 Verify on NeoTube: https://testnet.neotube.io/")
    print(f"{'='*70}")

if __name__ == "__main__":
    asyncio.run(live_demo())
