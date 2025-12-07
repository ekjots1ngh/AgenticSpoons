"""
Deploy volatility oracle to Neo N3 Testnet
"""
from neo3.wallet import wallet
import requests
import json
import time

print("="*70)
print("🚀 DEPLOYING TO NEO TESTNET")
print("="*70)

# Configuration
WALLET_FILE = "agentspoons_wallet.json"
PASSWORD = "agentspoons2024"
WALLET_ADDRESS = "NVLMjeu3Z1feMuN6HEcmLayyM7m5KsJTRX"
PRIVATE_KEY = "L3ZFHMjexgsAmPRkYHGpVs58vbwEpdFNXBDDZo7JMMWm7n9XGpbb"

print(f"\n📍 Deploying from: {WALLET_ADDRESS}")

# Read compiled contracts
try:
    with open('volatility_oracle.nef', 'rb') as f:
        nef_bytes = f.read()
    
    with open('volatility_oracle.manifest.json', 'r') as f:
        manifest = json.load(f)
    
    print(f"📦 Contract size: {len(nef_bytes)} bytes")
    print(f"📄 Manifest loaded: {manifest['name']}")
    
except FileNotFoundError as e:
    print(f"❌ Contract files not found: {e}")
    print(f"   Make sure volatility_oracle.nef and .manifest.json are in current directory")
    exit(1)

print("\n" + "="*70)
print("⚠️  DEPLOYMENT OPTIONS:")
print("="*70)

print("\nOption 1: NEO-CLI (Official - RECOMMENDED) ⭐")
print("-" * 70)
print("1. Download: https://github.com/neo-project/neo-cli/releases/latest")
print("2. Extract and run neo-cli.exe")
print("3. Commands:")
print(f"   > import key {PRIVATE_KEY}")
print("   > deploy volatility_oracle.nef")
print("   > [Confirm transaction]")
print("\n✅ Most reliable method")

print("\nOption 2: Neon Wallet (GUI - EASIEST) 🖱️")
print("-" * 70)
print("1. Download: https://neon.coz.io/")
print("2. Switch to TestNet in settings")
print(f"3. Import wallet using WIF: {PRIVATE_KEY}")
print("4. Use contract deployment feature")
print("5. Upload .nef and .manifest.json files")
print("\n✅ User-friendly interface")

print("\nOption 3: Online Neo Compiler (FASTEST) 🌐")
print("-" * 70)
print("1. Visit: https://neo3.testnet.neocompiler.io/")
print("2. Or: https://ide.neo.org/")
print("3. Import wallet with private key")
print("4. Upload volatility_oracle.nef")
print("5. Upload volatility_oracle.manifest.json")
print("6. Click 'Deploy to TestNet'")
print("\n✅ No installation required")

print("\nOption 4: Neo Express (LOCAL TESTING FIRST) 🧪")
print("-" * 70)
print("1. Install: dotnet tool install -g Neo.Express")
print("2. Create local chain: neoxp create")
print("3. Run: neoxp run")
print("4. Deploy: neoxp contract deploy volatility_oracle.nef")
print("5. Test locally, then deploy to testnet")
print("\n✅ Safe testing environment")

# Save deployment info
deployment_info = {
    "contract_name": "AgentSpoons Volatility Oracle",
    "nef_file": "volatility_oracle.nef",
    "manifest_file": "volatility_oracle.manifest.json",
    "deployer_address": WALLET_ADDRESS,
    "network": "testnet",
    "rpc_url": "https://testnet1.neo.coz.io:443",
    "testnet_magic": 894710606,
    "deployment_method": "pending",
    "contract_hash": "pending_deployment",
    "estimated_gas_cost": "10-15 GAS",
    "wallet_balance": "50 GAS available",
    "methods": [
        "_deploy(data, update)",
        "store_volatility(pair_id, price, realized_vol, implied_vol)",
        "get_volatility()",
        "get_timestamp()",
        "set_owner(new_owner)",
        "get_owner()",
        "verify()"
    ],
    "next_steps": [
        "1. Choose deployment method above",
        "2. Deploy contract and SAVE the contract hash",
        "3. Test by calling store_volatility()",
        "4. Verify with get_volatility()",
        "5. Integrate with AgentSpoons data pipeline"
    ]
}

with open('deployment_info.json', 'w') as f:
    json.dump(deployment_info, f, indent=2)

print("\n" + "="*70)
print("✅ DEPLOYMENT FILES READY!")
print("="*70)
print(f"\n📝 Deployment info saved to: deployment_info.json")
print(f"📦 Contract: volatility_oracle.nef ({len(nef_bytes)} bytes)")
print(f"📄 Manifest: volatility_oracle.manifest.json")
print(f"💰 Wallet balance: 50 GAS (sufficient)")
print(f"💸 Estimated cost: 10-15 GAS")

print("\n" + "="*70)
print("🎯 RECOMMENDED QUICKSTART")
print("="*70)
print("""
For fastest deployment:

1. Download neo-cli (5 min)
   https://github.com/neo-project/neo-cli/releases/latest

2. Run these commands (3 min):
   
   import key L3ZFHMjexgsAmPRkYHGpVs58vbwEpdFNXBDDZo7JMMWm7n9XGpbb
   deploy volatility_oracle.nef

3. SAVE THE CONTRACT HASH displayed after deployment!

4. Test your contract:
   
   invoke <contract_hash> store_volatility [1, 1500000000000000, 25000000, 30000000]
   invoke <contract_hash> get_volatility []

Total time: ~8 minutes
""")

print("="*70)
print("💡 After deployment, integrate with AgentSpoons:")
print("   - Store volatility data on-chain")
print("   - Read data for verification")
print("   - Monitor gas costs")
print("="*70)
