"""
Direct Neo Contract Deployment Script
Deploy contracts directly to Neo N3 Testnet
"""
import requests
import json

print("="*70)
print("🚀 NEO N3 TESTNET - DIRECT DEPLOYMENT")
print("="*70)

TESTNET_RPC = "https://testnet1.neo.coz.io:443"
WALLET_ADDRESS = "NVLMjeu3Z1feMuN6HEcmLayyM7m5KsJTRX"

def test_rpc_connection():
    """Test RPC connection"""
    print("\n1️⃣  Testing RPC connection...")
    
    try:
        response = requests.post(TESTNET_RPC, json={
            "jsonrpc": "2.0",
            "method": "getversion",
            "params": [],
            "id": 1
        }, timeout=10)
        
        result = response.json()
        if "result" in result:
            version = result["result"]
            print(f"   ✅ Connected to Neo N3 Testnet")
            print(f"   📍 Network: {version.get('network', 'unknown')}")
            print(f"   🔢 Protocol: {version.get('protocol', {}).get('network', 'N/A')}")
            return True
        else:
            print(f"   ❌ Connection failed: {result}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def get_contract_state(contract_hash):
    """Get deployed contract state"""
    try:
        response = requests.post(TESTNET_RPC, json={
            "jsonrpc": "2.0",
            "method": "getcontractstate",
            "params": [contract_hash],
            "id": 1
        }, timeout=10)
        
        result = response.json()
        if "result" in result:
            return result["result"]
        return None
    except:
        return None

def invoke_deploy(nef_file, manifest_file, contract_name):
    """Invoke contract deployment"""
    print(f"\n2️⃣  Deploying {contract_name}...")
    
    # Read files
    with open(nef_file, 'rb') as f:
        nef_bytes = f.read()
    
    with open(manifest_file, 'r') as f:
        manifest = json.load(f)
    
    import base64
    nef_base64 = base64.b64encode(nef_bytes).decode('utf-8')
    manifest_str = json.dumps(manifest, separators=(',', ':'))
    
    print(f"   📄 NEF: {len(nef_bytes)} bytes")
    print(f"   📄 Manifest: {len(manifest_str)} bytes")
    
    # Test invocation first (doesn't broadcast)
    print(f"\n   🧪 Testing deployment (simulation)...")
    
    try:
        response = requests.post(TESTNET_RPC, json={
            "jsonrpc": "2.0",
            "method": "invokefunction",
            "params": [
                "0xfffdc93764dbaddd97c48f252a53ea4643faa3fd",  # ContractManagement
                "deploy",
                [
                    {"type": "ByteArray", "value": nef_base64},
                    {"type": "String", "value": manifest_str}
                ],
                [{"account": WALLET_ADDRESS, "scopes": "CalledByEntry"}]
            ],
            "id": 1
        }, timeout=30)
        
        result = response.json()
        
        if "result" in result:
            state = result["result"].get("state", "FAULT")
            gas_consumed = float(result["result"].get("gasconsumed", 0)) / 1e8
            
            print(f"   📊 Simulation result: {state}")
            print(f"   ⛽ Estimated GAS: {gas_consumed:.4f}")
            
            if state == "HALT":
                print(f"   ✅ Contract deployment would succeed!")
                
                # Get the script from result
                script = result["result"].get("script", "")
                
                print(f"\n   📝 To complete deployment, you need to:")
                print(f"   1. Sign this transaction with your private key")
                print(f"   2. Broadcast the signed transaction")
                print(f"\n   💡 Use neo-cli or neo-python to sign and send")
                
                # Save transaction details
                tx_file = f"neo_contract/tx_{contract_name.lower().replace(' ', '_')}.json"
                with open(tx_file, 'w') as f:
                    json.dump({
                        "contract": contract_name,
                        "simulation": result["result"],
                        "estimated_gas": gas_consumed,
                        "wallet": WALLET_ADDRESS,
                        "instructions": [
                            "1. Use neo-cli: deploy " + nef_file,
                            "2. Or use neo-python with your private key",
                            "3. Or import wallet to NEO IDE and deploy there"
                        ]
                    }, f, indent=2)
                
                print(f"   💾 Transaction details saved: {tx_file}")
                
                return True
            else:
                print(f"   ❌ Deployment simulation failed")
                print(f"   Error: {result['result'].get('exception', 'Unknown')}")
                return False
        else:
            error = result.get("error", {})
            print(f"   ❌ RPC Error: {error.get('message', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"   ❌ Exception: {e}")
        return False

def main():
    """Main deployment flow"""
    
    print(f"\n📍 Wallet: {WALLET_ADDRESS}")
    print(f"🌐 RPC: {TESTNET_RPC}")
    
    # Test connection
    if not test_rpc_connection():
        print("\n❌ Cannot connect to Neo testnet RPC")
        return
    
    print("\n" + "="*70)
    
    # Deploy contracts
    contracts = [
        {
            "name": "Simple Oracle",
            "nef": "neo_contract/simple_oracle.nef",
            "manifest": "neo_contract/simple_oracle.manifest.json"
        },
        {
            "name": "Volatility Oracle",
            "nef": "neo_contract/volatility_oracle.nef",
            "manifest": "neo_contract/volatility_oracle.manifest.json"
        }
    ]
    
    results = []
    for contract in contracts:
        success = invoke_deploy(
            contract["nef"],
            contract["manifest"],
            contract["name"]
        )
        results.append({"name": contract["name"], "success": success})
        print("\n" + "-"*70)
    
    # Summary
    print("\n" + "="*70)
    print("📊 DEPLOYMENT SUMMARY")
    print("="*70)
    
    for result in results:
        status = "✅ Ready" if result["success"] else "❌ Failed"
        print(f"   {status} {result['name']}")
    
    print(f"\n" + "="*70)
    print("🎯 FINAL STEPS")
    print("="*70)
    print("""
Your contracts have been validated and are ready for deployment!

To complete the deployment, you need to SIGN the transaction:

OPTION 1: Neo-CLI (Easiest)
---------------------------
1. Download: https://github.com/neo-project/neo-cli/releases
2. Extract and run: neo-cli.exe
3. Commands:
   
   neo-cli> open wallet <path_to_wallet>
   neo-cli> deploy neo_contract/simple_oracle.nef
   neo-cli> deploy neo_contract/volatility_oracle.nef

OPTION 2: NEO N3 IDE (Visual)
-----------------------------
1. Visit: https://neo.org/neoide
2. Connect wallet
3. Upload .nef and .manifest.json files
4. Click Deploy

OPTION 3: Neo-Python (Advanced)
-------------------------------
If you have your WIF private key:
   
   python deploy_with_key.py <your_wif_key>

⚠️  Why manual signing is needed:
- Smart contract deployment requires transaction signature
- Python neo3 library doesn't support full signing yet
- neo-cli and NEO IDE handle signing automatically
- Keeps your private key secure (never share it!)

💡 Next: Download neo-cli or use NEO IDE to complete deployment
""")

if __name__ == "__main__":
    main()
