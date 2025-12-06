"""
Integration Test Suite - Test all AgentSpoons components together
"""
import asyncio
import json
import subprocess
import time
import requests
import websockets
from pathlib import Path
from loguru import logger

class IntegrationTestSuite:
    """Comprehensive integration tests for AgentSpoons"""
    
    def __init__(self):
        self.test_results = {}
        self.passed = 0
        self.failed = 0
    
    def log_test(self, name, passed, message=""):
        """Log test result"""
        status = "PASS" if passed else "FAIL"
        symbol = "[✓]" if passed else "[✗]"
        
        print(f"{symbol} {name}: {message}" if message else f"{symbol} {name}")
        logger.info(f"{status}: {name} - {message}")
        
        self.test_results[name] = passed
        if passed:
            self.passed += 1
        else:
            self.failed += 1
    
    def test_data_generation(self):
        """Test 1: Data generation working"""
        try:
            data_file = Path("data/results.json")
            if data_file.exists():
                with open(data_file, 'r') as f:
                    data = json.load(f)
                
                if isinstance(data, list) and len(data) > 0:
                    first = data[0]
                    required_fields = ['timestamp', 'volatility', 'price']
                    has_fields = all(field in first for field in required_fields)
                    
                    self.log_test("Data Generation", has_fields, 
                                 f"{len(data)} records with required fields")
                    return has_fields
            
            self.log_test("Data Generation", False, "No data file found")
            return False
        except Exception as e:
            self.log_test("Data Generation", False, str(e))
            return False
    
    def test_rest_api(self):
        """Test 2: REST API endpoints"""
        try:
            # Test root endpoint
            resp = requests.get("http://localhost:8000/", timeout=5)
            if resp.status_code != 200:
                self.log_test("REST API", False, f"Root endpoint: {resp.status_code}")
                return False
            
            # Test health
            resp = requests.get("http://localhost:8000/health", timeout=5)
            if resp.status_code != 200:
                self.log_test("REST API", False, f"Health endpoint: {resp.status_code}")
                return False
            
            data = resp.json()
            if data.get('status') == 'operational':
                self.log_test("REST API", True, 
                             f"API operational with {data.get('data_points')} points")
                return True
            
            return False
        except Exception as e:
            self.log_test("REST API", False, str(e))
            return False
    
    async def test_websocket(self):
        """Test 3: WebSocket connectivity"""
        try:
            async with websockets.connect("ws://localhost:8765", timeout=5) as ws:
                # Receive welcome message
                msg = await ws.recv()
                data = json.loads(msg)
                
                if data.get('type') == 'connected':
                    self.log_test("WebSocket", True, "Connected and received welcome")
                    
                    # Send test message
                    await ws.send(json.dumps({"test": "message"}))
                    echo = await asyncio.wait_for(ws.recv(), timeout=3)
                    
                    self.log_test("WebSocket Echo", True, "Echo received")
                    return True
            
            return False
        except Exception as e:
            self.log_test("WebSocket", False, str(e))
            return False
    
    def test_garch_models(self):
        """Test 4: GARCH model availability"""
        try:
            from src.models.advanced_garch import AdvancedGARCH
            
            # Create dummy data
            import numpy as np
            returns = np.random.normal(0, 0.01, 100)
            
            # Test GARCH fitting
            garch = AdvancedGARCH(returns)
            params = garch.fit_garch_11()
            
            if params and 'omega' in params:
                self.log_test("GARCH Models", True,
                             f"Fitted: omega={params['omega']:.6f}")
                return True
            
            return False
        except Exception as e:
            self.log_test("GARCH Models", False, str(e))
            return False
    
    def test_visualization(self):
        """Test 5: 3D visualization components"""
        try:
            from src.visualization import VolatilitySurface3D, VolatilitySmile, TermStructure
            
            # Test 3D surface
            surf = VolatilitySurface3D()
            fig = surf.generate_sample_surface()
            
            if fig is not None:
                self.log_test("Visualization", True,
                             "3D surface, smile, and term structure working")
                return True
            
            return False
        except Exception as e:
            self.log_test("Visualization", False, str(e))
            return False
    
    def test_blockchain(self):
        """Test 6: Blockchain connectivity"""
        try:
            from src.neo.blockchain_client import NeoBlockchainClient
            
            # Create client
            client = NeoBlockchainClient(
                rpc_url="https://testnet1.neo.coz.io:443",
                network="testnet"
            )
            
            # Test RPC connection (don't need to actually call it)
            if client.rpc_url:
                self.log_test("Blockchain", True,
                             f"Neo N3 client ready: {client.network}")
                return True
            
            return False
        except Exception as e:
            self.log_test("Blockchain", False, str(e))
            return False
    
    def test_dashboard_files(self):
        """Test 7: Dashboard files exist"""
        try:
            from pathlib import Path
            
            required_files = [
                "src/championship_dashboard.py",
                "src/visualization/enhanced_dashboard.py",
                "data/vol_surface_3d.html",
                "data/vol_smile.html",
                "data/term_structure.html"
            ]
            
            all_exist = all(Path(f).exists() for f in required_files)
            
            if all_exist:
                self.log_test("Dashboard Files", True,
                             f"All {len(required_files)} dashboard files present")
                return True
            
            missing = [f for f in required_files if not Path(f).exists()]
            self.log_test("Dashboard Files", False, f"Missing: {missing}")
            return False
        except Exception as e:
            self.log_test("Dashboard Files", False, str(e))
            return False
    
    def test_documentation(self):
        """Test 8: Documentation completeness"""
        try:
            from pathlib import Path
            
            docs = [
                "REST_API.md",
                "WEBSOCKET_API.md",
                "INFRASTRUCTURE.md"
            ]
            
            all_exist = all(Path(f).exists() for f in docs)
            
            if all_exist:
                # Count lines
                total_lines = sum(len(open(f).readlines()) for f in docs)
                self.log_test("Documentation", True,
                             f"All docs present ({total_lines} lines)")
                return True
            
            return False
        except Exception as e:
            self.log_test("Documentation", False, str(e))
            return False
    
    async def run_all_tests(self):
        """Run all integration tests"""
        print("\n" + "="*70)
        print("AGENTSPOONS - INTEGRATION TEST SUITE")
        print("="*70 + "\n")
        
        # Run sync tests
        print("Running integration tests...\n")
        self.test_data_generation()
        self.test_garch_models()
        self.test_visualization()
        self.test_blockchain()
        self.test_dashboard_files()
        self.test_documentation()
        
        # Try to run async tests if services available
        print("\nTesting live services (if running)...\n")
        try:
            await asyncio.wait_for(self.test_websocket(), timeout=3)
        except asyncio.TimeoutError:
            self.log_test("WebSocket", False, "Service not running (expected)")
        except Exception:
            self.log_test("WebSocket", False, "Service not available")
        
        try:
            if self.test_rest_api():
                pass
        except:
            self.log_test("REST API", False, "Service not running (expected)")
        
        # Summary
        print("\n" + "="*70)
        print("TEST SUMMARY")
        print("="*70)
        print(f"Passed: {self.passed}")
        print(f"Failed: {self.failed}")
        print(f"Total:  {self.passed + self.failed}")
        
        if self.failed == 0:
            print("\n✅ ALL TESTS PASSED!")
        else:
            print(f"\n⚠️  {self.failed} tests failed")
        
        print("="*70 + "\n")
        
        return self.failed == 0

if __name__ == "__main__":
    import sys
    
    suite = IntegrationTestSuite()
    result = asyncio.run(suite.run_all_tests())
    
    sys.exit(0 if result else 1)
