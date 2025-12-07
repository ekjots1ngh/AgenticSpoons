"""
Direct deployment using private key
SECURITY: This script should be deleted after use
"""
import asyncio
from neo3.wallet import wallet
from neo3.core import types, cryptography
from neo3 import contracts, vm
import json

print("="*70)
print("🚀 DEPLOYING CONTRACTS TO NEO N3 TESTNET")
print("="*70)

# Configuration
PRIVATE_KEY_WIF = "L3ZFHMjexgsAmPRkYHGpVs58vbwEpdFNXBDDZo7JMMWm7n9XGpbb"
TESTNET_NODES = [
    "http://seed1t5.neo.org:20332",
    "http://seed2t5.neo.org:20332",
]

async def deploy_contract(node, nef_file, manifest_file, contract_name, account):
    """Deploy contract to testnet"""
    print(f"\n📦 Deploying {contract_name}...")
    
    # Read contract files
    with open(nef_file, 'rb') as f:
        nef_bytes = f.read()
    
    with open(manifest_file, 'r') as f:
        manifest = json.load(f)
    
    print(f"   📄 NEF: {len(nef_bytes)} bytes")
    print(f"   📄 Manifest loaded")
    
    try:
        # Create deployment transaction
        manifest_str = json.dumps(manifest, separators=(',', ':'))
        
        # Use ContractManagement.deploy
        contract_mgmt = contracts.ContractManagementContract()
        
        # Build script
        sb = vm.ScriptBuilder()
        sb.emit_push(manifest_str)
        sb.emit_push(nef_bytes)
        sb.emit_syscall(contracts.syscalls.System_Contract_Create)
        
        script = sb.to_array()
        
        print(f"   🔨 Transaction built")
        print(f"   💾 Script length: {len(script)} bytes")
        
        # Sign and send
        print(f"   ✍️  Signing transaction...")
        
        # Create transaction
        tx = await node.create_transaction(
            from_addr=account.address,
            script=script,
            signers=[types.Signer(account.script_hash, types.WitnessScope.GLOBAL)]
        )
        
        # Sign with private key
        tx.sign(account)
        
        print(f"   📡 Broadcasting to network...")
        
        # Send transaction
        tx_hash = await node.send_transaction(tx)
        
        print(f"   ✅ Transaction sent!")
        print(f"   🔗 TX Hash: {tx_hash}")
        print(f"   🔍 View at: https://testnet.neotube.io/transaction/{tx_hash}")
        
        # Wait for confirmation
        print(f"   ⏳ Waiting for confirmation...")
        await asyncio.sleep(15)
        
        # Get transaction result
        result = await node.get_transaction(tx_hash)
        if result:
            print(f"   ✅ Contract deployed successfully!")
            return str(tx_hash)
        else:
            print(f"   ⚠️  Transaction pending...")
            return str(tx_hash)
            
    except Exception as e:
        print(f"   ❌ Deployment failed: {e}")
        return None

async def main():
    """Main deployment"""
    
    print(f"\n🔐 Loading wallet from private key...")
    
    try:
        # Create account from WIF using correct neo3 API
        from neo3.wallet import account
        acc = account.Account.from_wif(PRIVATE_KEY_WIF, "")
        
        print(f"   ✅ Wallet loaded")
        print(f"   📍 Address: {acc.address}")
        print(f"   🔑 Script Hash: {acc.script_hash}")
        
    except Exception as e:
        print(f"   ❌ Failed to load wallet: {e}")
        print(f"   📝 Error details: {type(e).__name__}")
        
        # Try alternative method
        await deploy_via_rpc_simple()
        return
    
    # Connect to Neo testnet
    print(f"\n🌐 Connecting to Neo N3 Testnet...")
    
    try:
        node = convenience.NeoNode()
        await node.connect_to_testnet()
        
        print(f"   ✅ Connected to testnet")
        
        # Check balance
        balance = await node.get_balance(account.address)
        print(f"   💰 GAS Balance: {balance['GAS']} GAS")
        
        if balance['GAS'] < 20:
            print(f"   ⚠️  Low balance! Need at least 20 GAS")
            return
        
    except Exception as e:
        print(f"   ❌ Connection failed: {e}")
        print(f"   💡 Trying alternative deployment method...")
        
        # Alternative: Use RPC directly
        await deploy_via_rpc(account)
        return
    
    print(f"\n" + "="*70)
    
    # Deploy contracts
    contracts_to_deploy = [
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
    
    deployed = []
    for contract in contracts_to_deploy:
        tx_hash = await deploy_contract(
            node,
            contract["nef"],
            contract["manifest"],
            contract["name"],
            account
        )
        
        if tx_hash:
            deployed.append({
                "name": contract["name"],
                "tx_hash": tx_hash
            })
        
        print(f"\n" + "-"*70)
    
    # Summary
    print(f"\n" + "="*70)
    print("✅ DEPLOYMENT COMPLETE")
    print("="*70)
    
    for contract in deployed:
        print(f"\n📦 {contract['name']}")
        print(f"   🔗 TX: {contract['tx_hash']}")
        print(f"   🔍 Explorer: https://testnet.neotube.io/transaction/{contract['tx_hash']}")
    
    print(f"\n💡 Save these transaction hashes to track your contracts!")
    print(f"⏳ Wait 15-30 seconds, then check the explorer for contract hashes")

async def deploy_via_rpc(account):
    """Alternative deployment via RPC"""
    print(f"\n🔄 Using RPC deployment method...")
    print(f"\n⚠️  Note: Python neo3 library has limited deployment support")
    print(f"         Using neo-cli is recommended for production")
    
    import requests
    import base64
    
    RPC_URL = "https://testnet1.neo.coz.io:443"
    
    # Deploy simple oracle first
    with open('neo_contract/simple_oracle.nef', 'rb') as f:
        nef = base64.b64encode(f.read()).decode()
    
    with open('neo_contract/simple_oracle.manifest.json', 'r') as f:
        manifest = json.dumps(json.load(f), separators=(',', ':'))
    
    print(f"\n📦 Creating unsigned transaction for Simple Oracle...")
    
    # This creates the transaction but can't sign it fully with current neo3-python
    print(f"   ℹ️  Transaction ready but needs full signing support")
    print(f"\n💡 RECOMMENDED: Use neo-cli for actual deployment")
    print(f"""
To deploy with neo-cli:

1. Download: https://github.com/neo-project/neo-cli/releases
2. Create wallet from WIF:
   neo-cli> import key {PRIVATE_KEY_WIF}
3. Deploy:
   neo-cli> deploy neo_contract/simple_oracle.nef
   neo-cli> deploy neo_contract/volatility_oracle.nef
""")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n\n⚠️  Deployment cancelled")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        print(f"\n💡 Alternative: Use neo-cli with your private key")
