"""Quick API test"""
import subprocess
import time
import requests
import sys

# Start API
print("Starting API...")
proc = subprocess.Popen(
    ["python", "src/api/rest_api.py"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

time.sleep(10)

try:
    # Test health
    response = requests.get("http://localhost:8000/health", timeout=5)
    print(f"✓ Health: {response.status_code}")
    data = response.json()
    print(f"  Status: {data.get('status')}")
    print(f"  Data points: {data.get('data_points')}")
    
    # Test root
    response = requests.get("http://localhost:8000/", timeout=5)
    print(f"✓ Root: {response.status_code}")
    data = response.json()
    print(f"  API: {data.get('name')} v{data.get('version')}")
    
    print("\n✅ API is working!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    proc.terminate()
    sys.exit(1)

finally:
    proc.terminate()
    print("API stopped")
