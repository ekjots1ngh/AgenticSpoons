"""
Test streaming infrastructure
"""
import sys
import time
import numpy as np
from loguru import logger

# Add parent directory to path
sys.path.insert(0, '.')

from src.streaming.redis_stream import streaming

def test_streaming():
    """Test Redis and Kafka streaming"""
    
    print("\n" + "="*60)
    print("Testing AgenticSpoons Streaming Infrastructure")
    print("="*60)
    
    # Check if streaming is available
    if not streaming.is_available():
        print("\n⚠️  No streaming backend available")
        print("   Redis: Not connected (optional)")
        print("   Kafka: Not configured (optional)")
        print("\n💡 Streaming is optional. System works without it.")
        print("   To enable Redis:")
        print("   - Windows: .\\setup_redis.ps1")
        print("   - Linux/Mac: ./setup_redis.sh")
        return
    
    print("\n✅ Streaming backend available")
    
    # Test publishing
    print("\n1. Testing Data Publishing")
    print("-" * 60)
    
    test_pairs = ['BTC/USD', 'ETH/USD', 'NEO/USD']
    
    for pair in test_pairs:
        data = {
            'price': 100.0 + np.random.randn() * 10,
            'realized_vol': 0.20 + np.random.randn() * 0.05,
            'implied_vol': 0.25 + np.random.randn() * 0.05,
            'garch_forecast': 0.22 + np.random.randn() * 0.03,
            'spread': 0.05 + abs(np.random.randn() * 0.02)
        }
        
        success = streaming.publish_update(pair, data)
        status = "✅" if success else "❌"
        print(f"   {status} Published {pair}: ${data['price']:.2f}, Vol={data['realized_vol']:.2%}")
        
        time.sleep(0.1)
    
    # Test retrieval
    print("\n2. Testing Data Retrieval")
    print("-" * 60)
    
    for pair in test_pairs:
        latest = streaming.get_latest(pair)
        if latest:
            print(f"   ✅ Retrieved {pair}:")
            print(f"      Price: ${latest['price']:.2f}")
            print(f"      Realized Vol: {latest['realized_vol']:.2%}")
            print(f"      Implied Vol: {latest['implied_vol']:.2%}")
        else:
            print(f"   ❌ No data for {pair}")
    
    # Test stream history
    print("\n3. Testing Stream History")
    print("-" * 60)
    
    for pair in test_pairs:
        history = streaming.get_stream(pair, count=5)
        print(f"   {pair}: {len(history)} historical entries")
        
        if history:
            latest = history[0]
            oldest = history[-1]
            print(f"      Latest: {latest['timestamp'][:19]}")
            print(f"      Oldest: {oldest['timestamp'][:19]}")
    
    # Test all pairs
    print("\n4. Testing Pair Discovery")
    print("-" * 60)
    
    all_pairs = streaming.get_all_pairs()
    print(f"   Found {len(all_pairs)} pairs with data:")
    for pair in all_pairs:
        print(f"      • {pair}")
    
    # Performance test
    print("\n5. Performance Test")
    print("-" * 60)
    
    n_messages = 100
    start = time.time()
    
    for i in range(n_messages):
        data = {
            'price': 100.0 + np.random.randn() * 10,
            'realized_vol': 0.20 + np.random.randn() * 0.05,
            'implied_vol': 0.25 + np.random.randn() * 0.05,
            'garch_forecast': 0.22 + np.random.randn() * 0.03,
            'spread': 0.05 + abs(np.random.randn() * 0.02)
        }
        streaming.publish_update('BTC/USD', data)
    
    elapsed = time.time() - start
    
    if elapsed > 0:
        throughput = n_messages / elapsed
        print(f"   Published {n_messages} messages in {elapsed:.3f}s")
        print(f"   Throughput: {throughput:.0f} msg/s")
        print(f"   Latency: {elapsed/n_messages*1000:.2f} ms/msg")
    else:
        print(f"   ⚠️  No messages published (Redis not available)")
    
    # Summary
    print("\n" + "="*60)
    print("✅ Streaming Infrastructure Tests Complete!")
    print("="*60)
    
    print("\nFeatures Enabled:")
    if streaming.redis:
        print("   ✅ Redis: Real-time pub/sub + caching")
    if streaming.kafka:
        print("   ✅ Kafka: High-throughput streaming")
    
    print("\nUse Cases:")
    print("   • Real-time volatility monitoring")
    print("   • Sub-second trade signals")
    print("   • Historical data replay")
    print("   • Multi-agent coordination")
    print("   • Dashboard live updates")
    
    print("\nIntegration Example:")
    print("   from src.streaming.redis_stream import streaming")
    print("   streaming.publish_update('BTC/USD', volatility_data)")
    print("   latest = streaming.get_latest('BTC/USD')")

if __name__ == "__main__":
    test_streaming()
