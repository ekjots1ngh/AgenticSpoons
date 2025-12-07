import requests

# Address from wallet
address = "NfdoDDv8xBYnG9aUHtERoQL46pazXvDMtk"

print(f"Checking balance for: {address}")

# Query Neo testnet RPC
rpc_url = "https://testnet1.neo.coz.io:443"

response = requests.post(rpc_url, json={
    "jsonrpc": "2.0",
    "method": "getnep17balances",
    "params": [address],
    "id": 1
})

result = response.json()

if "result" in result and "balance" in result["result"]:
    balances = result["result"]["balance"]
    
    for balance in balances:
        asset = balance["assethash"]
        amount = int(balance["amount"]) / 1e8
        
        # NEO token
        if asset == "0xef4073a0f2b305a38ec4050e4d3d28bc40ea63f5":
            print(f"  NEO: {amount}")
        # GAS token  
        elif asset == "0xd2a4cff31913016155e38e474a2c06d08be276cf":
            print(f"  GAS: {amount}")
else:
    print("No balance yet - request tokens from faucet")
