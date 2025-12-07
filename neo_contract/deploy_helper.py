#!/usr/bin/env python3
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
