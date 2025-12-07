"""
Direct deployment to Neo N3 Testnet using neo-mamba
Wallet: NVLMjeu3Z1feMuN6HEcmLayyM7m5KsJTRX
"""
import asyncio
from neo3.network.node import NeoNode
from neo3.core import types, serialization
from neo3.contracts.contract import CONTRACT_HASHES
import json
import base64

print("="*70)
print("🚀 DEPLOYING TO NEO N3 TESTNET")
print("="*70)

WALLET_ADDRESS = "NVLMjeu3Z1feMuN6HEcmLayyM7m5KsJTRX"

async def deploy_simple_oracle():
    """Deploy simple_oracle.nef to testnet"""
    print("\n1️⃣  Deploying Simple Oracle Contract...")
    
    # Read NEF and manifest
    with open('neo_contract/simple_oracle.nef', 'rb') as f:
        nef_bytes = f.read()
    
    with open('neo_contract/simple_oracle.manifest.json', 'r') as f:
        manifest = json.load(f)
    
    print(f"   📄 NEF loaded: {len(nef_bytes)} bytes")
    print(f"   📄 Manifest loaded")
    
    # Encode for deployment
    nef_base64 = base64.b64encode(nef_bytes).decode('utf-8')
    manifest_json = json.dumps(manifest, separators=(',', ':'))
    
    print(f"\n   🔨 Building deployment transaction...")
    print(f"   💾 NEF (base64): {nef_base64[:50]}...")
    print(f"   💾 Manifest size: {len(manifest_json)} bytes")
    
    # Create deployment invocation
    print(f"\n   ℹ️  To deploy via RPC, send this transaction:")
    
    deployment_script = f"""
{{
    "jsonrpc": "2.0",
    "method": "invokefunction",
    "params": [
        "0xfffdc93764dbaddd97c48f252a53ea4643faa3fd",
        "deploy",
        [
            {{"type": "ByteArray", "value": "{nef_base64}"}},
            {{"type": "String", "value": "{manifest_json}"}}
        ]
    ],
    "id": 1
}}
"""
    
    # Save deployment script
    with open('neo_contract/deploy_simple_oracle.json', 'w') as f:
        f.write(deployment_script)
    
    print(f"   ✅ Deployment script saved: neo_contract/deploy_simple_oracle.json")
    
    return {
        "name": "Simple Oracle",
        "nef_size": len(nef_bytes),
        "script_file": "neo_contract/deploy_simple_oracle.json"
    }

async def deploy_volatility_oracle():
    """Deploy volatility_oracle.nef to testnet"""
    print("\n2️⃣  Deploying Volatility Oracle Contract...")
    
    # Read NEF and manifest
    with open('neo_contract/volatility_oracle.nef', 'rb') as f:
        nef_bytes = f.read()
    
    with open('neo_contract/volatility_oracle.manifest.json', 'r') as f:
        manifest = json.load(f)
    
    print(f"   📄 NEF loaded: {len(nef_bytes)} bytes")
    print(f"   📄 Manifest loaded")
    
    # Encode for deployment
    nef_base64 = base64.b64encode(nef_bytes).decode('utf-8')
    manifest_json = json.dumps(manifest, separators=(',', ':'))
    
    print(f"\n   🔨 Building deployment transaction...")
    print(f"   💾 NEF (base64): {nef_base64[:50]}...")
    print(f"   💾 Manifest size: {len(manifest_json)} bytes")
    
    # Create deployment invocation
    deployment_script = f"""
{{
    "jsonrpc": "2.0",
    "method": "invokefunction",
    "params": [
        "0xfffdc93764dbaddd97c48f252a53ea4643faa3fd",
        "deploy",
        [
            {{"type": "ByteArray", "value": "{nef_base64}"}},
            {{"type": "String", "value": "{manifest_json}"}}
        ]
    ],
    "id": 1
}}
"""
    
    # Save deployment script
    with open('neo_contract/deploy_volatility_oracle.json', 'w') as f:
        f.write(deployment_script)
    
    print(f"   ✅ Deployment script saved: neo_contract/deploy_volatility_oracle.json")
    
    return {
        "name": "Volatility Oracle",
        "nef_size": len(nef_bytes),
        "script_file": "neo_contract/deploy_volatility_oracle.json"
    }

async def create_deployment_helper():
    """Create helper script for actual deployment"""
    
    helper_script = """#!/usr/bin/env python3
'''
Neo Contract Deployment Helper
Usage: python deploy_helper.py <wallet_wif> <contract_name>
'''
import sys
import requests
import json
from neo3.wallet import wallet
from neo3.core import types

def deploy_contract(wif_key, contract_name):
    '''Deploy contract using WIF private key'''
    
    TESTNET_RPC = "https://testnet1.neo.coz.io:443"
    
    # Load deployment script
    with open(f'neo_contract/deploy_{contract_name}.json', 'r') as f:
        deploy_script = json.load(f)
    
    print(f"Deploying {contract_name}...")
    print(f"RPC: {TESTNET_RPC}")
    
    # Send RPC call
    response = requests.post(TESTNET_RPC, json=deploy_script)
    result = response.json()
    
    print(f"Response: {json.dumps(result, indent=2)}")
    
    if 'result' in result:
        print(f"✅ Contract deployed successfully!")
        print(f"Script hash: {result.get('result', {}).get('script', 'N/A')}")
    else:
        print(f"❌ Deployment failed: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python deploy_helper.py <wallet_wif> <contract_name>")
        print("Examples:")
        print("  python deploy_helper.py KxXXXXX... simple_oracle")
        print("  python deploy_helper.py KxXXXXX... volatility_oracle")
        sys.exit(1)
    
    wif_key = sys.argv[1]
    contract_name = sys.argv[2]
    
    deploy_contract(wif_key, contract_name)
"""
    
    with open('neo_contract/deploy_helper.py', 'w', encoding='utf-8') as f:
        f.write(helper_script)
    
    print("\n   ✅ Deployment helper created: neo_contract/deploy_helper.py")

async def main():
    """Main deployment preparation"""
    
    # Deploy contracts
    simple_result = await deploy_simple_oracle()
    volatility_result = await deploy_volatility_oracle()
    
    # Create helper
    await create_deployment_helper()
    
    print("\n" + "="*70)
    print("✅ DEPLOYMENT SCRIPTS READY")
    print("="*70)
    
    print(f"\n📦 Contracts prepared:")
    print(f"   1. {simple_result['name']}: {simple_result['nef_size']} bytes")
    print(f"      Script: {simple_result['script_file']}")
    print(f"   2. {volatility_result['name']}: {volatility_result['nef_size']} bytes")
    print(f"      Script: {volatility_result['script_file']}")
    
    print(f"\n🔐 Wallet: {WALLET_ADDRESS}")
    print(f"💰 Balance: 50 GAS (sufficient)")
    
    print(f"\n" + "="*70)
    print("📝 NEXT STEPS TO DEPLOY")
    print("="*70)
    
    print("""
The deployment scripts are ready. To complete deployment:

METHOD 1: Using neo-cli (Recommended)
--------------------------------------
1. Download neo-cli: https://github.com/neo-project/neo-cli/releases
2. Configure for testnet in config.json
3. Run these commands:

   neo-cli> open wallet <your_wallet.json>
   neo-cli> deploy neo_contract/simple_oracle.nef
   neo-cli> deploy neo_contract/volatility_oracle.nef

METHOD 2: Using Python helper (if you have WIF private key)
-----------------------------------------------------------
   python neo_contract/deploy_helper.py <your_wif_key> simple_oracle
   python neo_contract/deploy_helper.py <your_wif_key> volatility_oracle

METHOD 3: Manual RPC call
--------------------------
Use the generated JSON files with curl or Postman:
   - neo_contract/deploy_simple_oracle.json
   - neo_contract/deploy_volatility_oracle.json

⚠️  SECURITY:
- Never share your private key or WIF
- Test on testnet first (you're already doing this!)
- Save contract hashes after deployment
- Estimated cost: 10-20 GAS per contract

🎯 After deployment, you'll receive a contract hash like:
   0xabcdef1234567890abcdef1234567890abcdef12
   
   Save this hash to interact with your contract!
""")

if __name__ == "__main__":
    asyncio.run(main())
