"""
Interact with deployed volatility oracle
"""
import requests
import json
from neo3.wallet import wallet
from base64 import b64encode

# CONTRACT HASH - Replace with your deployed contract hash!
CONTRACT_HASH = "0xYOUR_CONTRACT_HASH_HERE"  # Get this after deployment

RPC_URL = "https://testnet1.neo.coz.io:443"

def invoke_contract(method, params):
    """Call contract method"""
    
    payload = {
        "jsonrpc": "2.0",
        "method": "invokefunction",
        "params": [
            CONTRACT_HASH,
            method,
            params
        ],
        "id": 1
    }
    
    response = requests.post(RPC_URL, json=payload)
    return response.json()

def update_volatility_data(pair_id, price, rv, iv):
    """
    Update volatility on blockchain
    
    Args:
        pair_id: 1 (integer ID for trading pair)
        price: 15.50 -> 15500000000000 (scaled by 10^12)
        rv: 0.52 -> 520000 (52% as basis points * 10)
        iv: 0.58 -> 580000 (58% as basis points * 10)
    """
    
    # Scale values according to contract specification
    pair_id_int = int(pair_id)
    price_scaled = int(price * 1e12)  # Price in 10^12
    rv_scaled = int(rv * 1e6)  # Realized vol in 10^6
    iv_scaled = int(iv * 1e6)  # Implied vol in 10^6
    
    params = [
        {"type": "Integer", "value": pair_id_int},
        {"type": "Integer", "value": price_scaled},
        {"type": "Integer", "value": rv_scaled},
        {"type": "Integer", "value": iv_scaled}
    ]
    
    result = invoke_contract("store_volatility", params)
    
    print(f"\n📤 Update transaction:")
    print(json.dumps(result, indent=2))
    
    return result

def get_volatility_data():
    """Query volatility from blockchain"""
    
    params = []
    
    result = invoke_contract("get_volatility", params)
    
    print(f"\n📥 Query result:")
    
    if "result" in result and "stack" in result["result"]:
        stack = result["result"]["stack"]
        
        if stack and len(stack) > 0:
            value = stack[0].get("value")
            
            if value:
                # Decode the packed data
                data_int = int(value)
                
                # Unpack: price (12 digits) + rv (6 digits) + iv (6 digits)
                iv = data_int % 1000000
                data_int //= 1000000
                rv = data_int % 1000000
                price = data_int // 1000000
                
                print(f"  Price: ${price / 1e12:.4f}")
                print(f"  Realized Vol: {rv / 1e6:.2%}")
                print(f"  Implied Vol: {iv / 1e6:.2%}")
            else:
                print("  No data stored yet")
        else:
            print("  No data stored yet")
    
    return result

def get_timestamp():
    """Get last update timestamp"""
    
    result = invoke_contract("get_timestamp", [])
    
    print(f"\n🕐 Last update timestamp:")
    
    if "result" in result and "stack" in result["result"]:
        stack = result["result"]["stack"]
        if stack and len(stack) > 0:
            timestamp = stack[0].get("value", 0)
            print(f"  {timestamp}")
        else:
            print("  No timestamp available")
    
    return result

def get_owner():
    """Get contract owner"""
    
    result = invoke_contract("get_owner", [])
    
    print(f"\n👤 Contract owner:")
    print(json.dumps(result, indent=2))
    
    return result

def verify_contract():
    """Simple verification"""
    result = invoke_contract("verify", [])
    
    print(f"\n✅ Contract verification:")
    print(json.dumps(result, indent=2))
    
    return result

if __name__ == "__main__":
    print("="*70)
    print("🔗 INTERACTING WITH NEO CONTRACT")
    print("="*70)
    
    print(f"\n📍 Contract: {CONTRACT_HASH}")
    print(f"🌐 Network: Neo N3 Testnet")
    print(f"🔗 RPC: {RPC_URL}")
    
    if CONTRACT_HASH == "0xYOUR_CONTRACT_HASH_HERE":
        print("\n⚠️  ERROR: Please update CONTRACT_HASH with your deployed contract!")
        print("   Get this from the deployment output or Neo explorer")
        exit(1)
    
    # Test 1: Verify contract
    print("\n" + "="*70)
    print("1️⃣  VERIFYING CONTRACT")
    print("="*70)
    verify_contract()
    
    # Test 2: Get owner
    print("\n" + "="*70)
    print("2️⃣  CHECKING OWNER")
    print("="*70)
    get_owner()
    
    # Test 3: Query volatility (should be empty first time)
    print("\n" + "="*70)
    print("3️⃣  QUERYING VOLATILITY DATA")
    print("="*70)
    get_volatility_data()
    
    # Test 4: Get timestamp
    print("\n" + "="*70)
    print("4️⃣  CHECKING LAST UPDATE")
    print("="*70)
    get_timestamp()
    
    # Test 5: Show how to update (requires wallet)
    print("\n" + "="*70)
    print("5️⃣  UPDATING VOLATILITY (DEMO)")
    print("="*70)
    print("\n💡 To UPDATE data, you need to sign with wallet:")
    print("\n   Option 1: Using NeoLine wallet")
    print("   - Install NeoLine extension")
    print("   - Import your wallet")
    print("   - Call contract.store_volatility() from dApp")
    
    print("\n   Option 2: Using neo-cli")
    print("   - neo-cli> open wallet your_wallet.json")
    print("   - neo-cli> invoke <contract_hash> store_volatility [1, 15500000000000, 520000, 580000]")
    
    print("\n   Option 3: Using this script with wallet")
    print("   - Uncomment the update_volatility_data() call below")
    print("   - Add wallet signing logic")
    
    # Example (will fail without proper signing):
    # update_volatility_data(
    #     pair_id=1,           # NEO/USDT
    #     price=15.50,         # $15.50
    #     rv=0.52,             # 52% realized volatility
    #     iv=0.58              # 58% implied volatility
    # )
    
    print("\n" + "="*70)
    print("✅ INTERACTION SCRIPT READY")
    print("="*70)
    print("\n📝 Next steps:")
    print("   1. Deploy contract and get CONTRACT_HASH")
    print("   2. Update CONTRACT_HASH in this script")
    print("   3. Run: python interact_with_contract.py")
    print("   4. Use wallet to call store_volatility()")
    print("   5. Query with get_volatility() to verify")
    print("\n" + "="*70)
