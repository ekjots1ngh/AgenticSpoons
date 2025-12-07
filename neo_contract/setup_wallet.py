"""
Create Neo wallet and get testnet tokens
"""
from neo3.wallet import wallet
import requests
import json

print("="*70)
print("🔐 NEO WALLET SETUP")
print("="*70)

# Create wallet
print("\n1️⃣  Creating wallet...")
wallet_path = "agentspoons_wallet.json"
password = "agentspoons2024"

# Create wallet from file (or new if doesn't exist)
try:
    w = wallet.Wallet.from_file(wallet_path, password)
    print("   Wallet already exists, loading...")
    acc = w.account_default
except:
    # Create new wallet
    w = wallet.Wallet(name="AgentSpoons Testnet Wallet")
    acc = w.account_new(label="default", is_default=True)
    
    # Save to file
    with open(wallet_path, 'w') as f:
        json.dump(w.to_json(password), f, indent=2)

print(f"\n✅ Wallet created!")
print(f"📍 Address: {acc.address}")
print(f"🔑 Script Hash: {acc.script_hash}")
print(f"💾 Wallet file: agentspoons_wallet.json")

# Save address to file for later use
with open('wallet_address.txt', 'w') as f:
    f.write(acc.address)

print(f"\n2️⃣  Getting testnet tokens...")
print(f"🌐 Visit: https://neowish.ngd.network/")
print(f"📋 Paste this address: {acc.address}")
print(f"🎁 Request NEO and GAS tokens")
print(f"\n⏳ Wait ~30 seconds for tokens to arrive")

# Create helper script to check balance
with open('check_balance.py', 'w') as f:
    f.write(f'''from neo3.wallet import wallet
import requests

# Load wallet
w = wallet.Wallet.from_file("agentspoons_wallet.json", "agentspoons2024")
address = "{acc.address}"

print(f"Checking balance for: {{address}}")

# Query Neo testnet RPC
rpc_url = "https://testnet1.neo.coz.io:443"

response = requests.post(rpc_url, json={{
    "jsonrpc": "2.0",
    "method": "getnep17balances",
    "params": [address],
    "id": 1
}})

result = response.json()

if "result" in result and "balance" in result["result"]:
    balances = result["result"]["balance"]
    
    for balance in balances:
        asset = balance["assethash"]
        amount = int(balance["amount"]) / 1e8
        
        # NEO token
        if asset == "0xef4073a0f2b305a38ec4050e4d3d28bc40ea63f5":
            print(f"  NEO: {{amount}}")
        # GAS token  
        elif asset == "0xd2a4cff31913016155e38e474a2c06d08be276cf":
            print(f"  GAS: {{amount}}")
else:
    print("No balance yet - request tokens from faucet")
''')

print(f"\n3️⃣  After getting tokens, check balance:")
print(f"   python check_balance.py")

print("\n" + "="*70)
