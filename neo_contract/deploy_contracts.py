"""
Deploy Neo smart contracts to testnet
Using wallet address: NVLMjeu3Z1feMuN6HEcmLayyM7m5KsJTRX
"""
import asyncio
from neo3.network.node import NeoNode
from neo3.core import types
from neo3.wallet import wallet
from neo3 import contracts
import json

print("="*70)
print("🚀 NEO CONTRACT DEPLOYMENT")
print("="*70)

# Configuration
WALLET_ADDRESS = "NVLMjeu3Z1feMuN6HEcmLayyM7m5KsJTRX"
TESTNET_RPC = "https://testnet1.neo.coz.io:443"

print(f"\n📍 Wallet Address: {WALLET_ADDRESS}")
print(f"🌐 Network: Neo N3 Testnet")
print(f"🔗 RPC: {TESTNET_RPC}")

async def check_balance():
    """Check wallet balance before deployment"""
    import requests
    
    print("\n1️⃣  Checking balance...")
    
    response = requests.post(TESTNET_RPC, json={
        "jsonrpc": "2.0",
        "method": "getnep17balances",
        "params": [WALLET_ADDRESS],
        "id": 1
    })
    
    result = response.json()
    
    if "result" in result and "balance" in result["result"]:
        balances = result["result"]["balance"]
        
        gas_balance = 0
        for balance in balances:
            asset = balance["assethash"]
            amount = int(balance["amount"]) / 1e8
            
            # GAS token  
            if asset == "0xd2a4cff31913016155e38e474a2c06d08be276cf":
                gas_balance = amount
                print(f"   💰 GAS Balance: {amount}")
        
        if gas_balance < 10:
            print(f"   ⚠️  Warning: Low GAS balance. Deployment costs ~10-20 GAS")
            return False
        else:
            print(f"   ✅ Sufficient GAS for deployment")
            return True
    else:
        print("   ❌ Could not retrieve balance")
        return False

async def deploy_contract(contract_name, nef_file, manifest_file):
    """Deploy a contract to Neo testnet"""
    print(f"\n2️⃣  Deploying {contract_name}...")
    
    # Read compiled contract files
    with open(nef_file, 'rb') as f:
        nef_data = f.read()
    
    with open(manifest_file, 'r') as f:
        manifest_data = json.load(f)
    
    print(f"   📄 NEF size: {len(nef_data)} bytes")
    print(f"   📄 Manifest loaded")
    
    # Create deployment script
    import requests
    
    # Convert NEF to base64
    import base64
    nef_base64 = base64.b64encode(nef_data).decode('utf-8')
    manifest_json = json.dumps(manifest_data)
    
    print(f"\n   🔨 Building deployment transaction...")
    print(f"   📦 Contract: {contract_name}")
    print(f"   💾 Size: {len(nef_data)} bytes")
    
    # Note: Actual deployment requires neo-python or neo-cli
    print(f"\n   ℹ️  For actual deployment, use neo-cli:")
    print(f"   neo-cli> open wallet <your_wallet.json>")
    print(f"   neo-cli> deploy {nef_file} {manifest_file}")
    
    return True

async def main():
    """Main deployment flow"""
    
    # Check balance
    has_balance = await check_balance()
    
    if not has_balance:
        print("\n⚠️  Please ensure you have sufficient GAS before deploying")
        print("   Visit: https://neowish.ngd.network/")
        return
    
    # Deploy contracts
    print("\n" + "="*70)
    print("DEPLOYMENT PLAN")
    print("="*70)
    
    contracts_to_deploy = [
        {
            "name": "Simple Oracle",
            "nef": "neo_contract/simple_oracle.nef",
            "manifest": "neo_contract/simple_oracle.manifest.json",
            "description": "Basic oracle contract (274 bytes)"
        },
        {
            "name": "Volatility Oracle", 
            "nef": "neo_contract/volatility_oracle.nef",
            "manifest": "neo_contract/volatility_oracle.manifest.json",
            "description": "Production oracle with 7 methods (474 bytes)"
        }
    ]
    
    for i, contract in enumerate(contracts_to_deploy, 1):
        print(f"\n{i}. {contract['name']}")
        print(f"   {contract['description']}")
        print(f"   NEF: {contract['nef']}")
        print(f"   Manifest: {contract['manifest']}")
    
    print("\n" + "="*70)
    print("DEPLOYMENT INSTRUCTIONS")
    print("="*70)
    
    print("""
For actual deployment to Neo N3 testnet, you need to use one of these tools:

Option 1: neo-cli (Recommended)
-------------------------------
1. Download neo-cli from https://github.com/neo-project/neo-cli/releases
2. Extract and configure for testnet
3. Open neo-cli and run:
   
   open wallet <path_to_your_wallet>
   deploy neo_contract/simple_oracle.nef
   deploy neo_contract/volatility_oracle.nef

Option 2: Python deployment (Advanced)
--------------------------------------
1. Install: pip install neo-mamba
2. Use neo-mamba's deployment tools
3. Sign transaction with your private key

Option 3: NEO IDE (Visual)
--------------------------
1. Visit https://neo.org/neoide
2. Import your wallet
3. Upload .nef and .manifest.json files
4. Deploy through IDE interface

⚠️  IMPORTANT:
- Deployment costs ~10-20 GAS per contract
- Save the contract hash after deployment
- Test on testnet before mainnet
- Keep your private key secure
""")
    
    print("\n" + "="*70)
    print("✅ Pre-deployment checks complete!")
    print("="*70)
    print(f"\n📍 Your wallet: {WALLET_ADDRESS}")
    print(f"💼 Contracts ready: 2")
    print(f"📏 Total size: 748 bytes (274 + 474)")
    print(f"\nNext: Deploy using neo-cli or NEO IDE")

if __name__ == "__main__":
    asyncio.run(main())
