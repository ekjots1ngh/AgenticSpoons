"""
REST API Test Suite
"""
import asyncio
import aiohttp
import json
from loguru import logger

class RestAPITester:
    """Test REST API endpoints"""
    
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        
    async def test_root(self):
        """Test root endpoint"""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"{self.base_url}/") as resp:
                    data = await resp.json()
                    logger.info(f"✓ Root: {data['name']} v{data['version']}")
                    return True
            except Exception as e:
                logger.error(f"✗ Root failed: {e}")
                return False
    
    async def test_health(self):
        """Test health endpoint"""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"{self.base_url}/health") as resp:
                    data = await resp.json()
                    logger.info(f"✓ Health: {data['status']} ({data['data_points']} points)")
                    return True
            except Exception as e:
                logger.error(f"✗ Health failed: {e}")
                return False
    
    async def test_pairs(self):
        """Test pairs endpoint"""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"{self.base_url}/api/v1/pairs") as resp:
                    data = await resp.json()
                    logger.info(f"✓ Pairs: {data['total_pairs']} pairs available")
                    if data['pairs']:
                        logger.info(f"  Pairs: {data['pairs'][:5]}")
                    return True
            except Exception as e:
                logger.error(f"✗ Pairs failed: {e}")
                return False
    
    async def test_latest(self):
        """Test latest data endpoint"""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"{self.base_url}/api/v1/latest?limit=5") as resp:
                    data = await resp.json()
                    logger.info(f"✓ Latest: Retrieved {len(data)} records")
                    return True
            except Exception as e:
                logger.error(f"✗ Latest failed: {e}")
                return False
    
    async def test_stats(self):
        """Test statistics endpoint"""
        async with aiohttp.ClientSession() as session:
            try:
                # First get available pairs
                async with session.get(f"{self.base_url}/api/v1/pairs") as resp:
                    pairs_data = await resp.json()
                    if not pairs_data['pairs']:
                        logger.warning("⚠ No pairs available for stats test")
                        return False
                    
                    pair = pairs_data['pairs'][0]
                    async with session.get(f"{self.base_url}/api/v1/stats/{pair}") as resp:
                        data = await resp.json()
                        logger.info(f"✓ Stats ({pair}): RV mean={data['realized_vol']['mean']:.4f}")
                        return True
            except Exception as e:
                logger.error(f"✗ Stats failed: {e}")
                return False
    
    async def test_arbitrage(self):
        """Test arbitrage signals endpoint"""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"{self.base_url}/api/v1/arbitrage?min_spread=0.01") as resp:
                    data = await resp.json()
                    logger.info(f"✓ Arbitrage: {data['opportunities_count']} opportunities")
                    return True
            except Exception as e:
                logger.error(f"✗ Arbitrage failed: {e}")
                return False
    
    async def test_status(self):
        """Test status endpoint"""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"{self.base_url}/api/v1/status") as resp:
                    data = await resp.json()
                    logger.info(f"✓ Status: {data['status']} ({data['data_points']} points, {data['pairs']} pairs)")
                    return True
            except Exception as e:
                logger.error(f"✗ Status failed: {e}")
                return False
    
    async def run_all_tests(self):
        """Run all tests"""
        logger.info("Starting REST API tests...")
        logger.info(f"Base URL: {self.base_url}\n")
        
        tests = [
            ("Root", self.test_root),
            ("Health", self.test_health),
            ("Pairs", self.test_pairs),
            ("Latest", self.test_latest),
            ("Stats", self.test_stats),
            ("Arbitrage", self.test_arbitrage),
            ("Status", self.test_status),
        ]
        
        results = []
        for name, test_func in tests:
            try:
                result = await test_func()
                results.append((name, result))
            except Exception as e:
                logger.error(f"Test {name} error: {e}")
                results.append((name, False))
            
            await asyncio.sleep(0.5)
        
        logger.info("\n" + "="*50)
        passed = sum(1 for _, r in results if r)
        total = len(results)
        logger.info(f"Results: {passed}/{total} tests passed")
        logger.info("="*50)
        
        return passed == total

if __name__ == "__main__":
    import sys
    
    # Check if API is running
    import subprocess
    import time
    
    print("\n" + "="*70)
    print("🧪 REST API Test Suite")
    print("="*70)
    
    tester = RestAPITester()
    
    try:
        result = asyncio.run(tester.run_all_tests())
        
        if result:
            print("\n✅ All REST API tests passed!\n")
            sys.exit(0)
        else:
            print("\n❌ Some tests failed\n")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test error: {e}\n")
        print("Make sure the API is running: python src/api/rest_api.py")
        sys.exit(1)
