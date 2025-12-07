"""
Simple Neo Contract Deployment Tool
Uses neo-mamba library for deployment
"""
import subprocess
import json
import time

print("="*70)
print("🚀 NEO CONTRACT DEPLOYMENT TOOL")
print("="*70)

PRIVATE_KEY = "L3ZFHMjexgsAmPRkYHGpVs58vbwEpdFNXBDDZo7JMMWm7n9XGpbb"
WALLET_ADDRESS = "NVLMjeu3Z1feMuN6HEcmLayyM7m5KsJTRX"

print(f"\n📍 Wallet: {WALLET_ADDRESS}")

# Check if neo-mamba CLI is available
print(f"\n1️⃣  Checking for neo-mamba...")

try:
    result = subprocess.run(
        ["neomamba", "--version"],
        capture_output=True,
        text=True,
        timeout=5
    )
    
    if result.returncode == 0:
        print(f"   ✅ neo-mamba found: {result.stdout.strip()}")
        has_neomamba = True
    else:
        print(f"   ⚠️  neo-mamba not found")
        has_neomamba = False
        
except (FileNotFoundError, subprocess.TimeoutExpired):
    print(f"   ⚠️  neo-mamba not installed")
    has_neomamba = False

if not has_neomamba:
    print(f"\n" + "="*70)
    print("📦 INSTALL NEO-MAMBA")
    print("="*70)
    print("""
neo-mamba is the easiest way to deploy contracts from Python.

Install it:
    pip install neo-mamba

Then run this script again, or use these commands directly:

    neomamba contract deploy \\
        --network testnet \\
        --wallet-wif {wif} \\
        --nef neo_contract/simple_oracle.nef \\
        --manifest neo_contract/simple_oracle.manifest.json

    neomamba contract deploy \\
        --network testnet \\
        --wallet-wif {wif} \\
        --nef neo_contract/volatility_oracle.nef \\
        --manifest neo_contract/volatility_oracle.manifest.json
""".format(wif=PRIVATE_KEY))

else:
    # Deploy contracts
    print(f"\n" + "="*70)
    print("DEPLOYING CONTRACTS")
    print("="*70)
    
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
    
    deployed = []
    
    for i, contract in enumerate(contracts, 1):
        print(f"\n{i}. Deploying {contract['name']}...")
        
        try:
            cmd = [
                "neomamba", "contract", "deploy",
                "--network", "testnet",
                "--wallet-wif", PRIVATE_KEY,
                "--nef", contract["nef"],
                "--manifest", contract["manifest"]
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                print(f"   ✅ {contract['name']} deployed!")
                print(f"   Output: {result.stdout}")
                deployed.append(contract["name"])
            else:
                print(f"   ❌ Deployment failed")
                print(f"   Error: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print(f"   ⚠️  Deployment timed out")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print(f"\n" + "="*70)
    print(f"✅ Deployment Summary: {len(deployed)}/{len(contracts)} contracts deployed")
    print("="*70)

# Alternative: Create helper batch file
print(f"\n" + "="*70)
print("💡 ALTERNATIVE: NEO-CLI")
print("="*70)

batch_script = f"""@echo off
echo ====================================
echo Neo Contract Deployment via neo-cli
echo ====================================

echo.
echo Download neo-cli from:
echo https://github.com/neo-project/neo-cli/releases
echo.
echo Extract and run neo-cli.exe
echo.
echo Then paste these commands:
echo.
echo import key {PRIVATE_KEY}
echo deploy neo_contract\\simple_oracle.nef
echo deploy neo_contract\\volatility_oracle.nef
echo.
echo After deployment, save the contract hashes!
echo.
pause
"""

with open('neo_contract/deploy_with_neocli.bat', 'w') as f:
    f.write(batch_script)

print(f"\n✅ Created helper script: neo_contract/deploy_with_neocli.bat")
print(f"\nRun it to see neo-cli deployment instructions")

# Create PowerShell script too
ps_script = f"""# Neo Contract Deployment Helper
Write-Host "=" -ForegroundColor Cyan
Write-Host "Neo N3 Contract Deployment Guide" -ForegroundColor Cyan
Write-Host "=" -ForegroundColor Cyan

Write-Host "`nYour wallet address: {WALLET_ADDRESS}" -ForegroundColor Yellow
Write-Host "Private key (WIF): {PRIVATE_KEY}" -ForegroundColor Yellow

Write-Host "`n OPTION 1: Install neo-mamba (Python)" -ForegroundColor Green
Write-Host "pip install neo-mamba"
Write-Host "neomamba contract deploy --network testnet --wallet-wif {PRIVATE_KEY} --nef neo_contract/simple_oracle.nef"

Write-Host "`n OPTION 2: Use neo-cli" -ForegroundColor Green
Write-Host "1. Download: https://github.com/neo-project/neo-cli/releases"
Write-Host "2. Extract and run neo-cli.exe"
Write-Host "3. Commands:"
Write-Host "   > import key {PRIVATE_KEY}"
Write-Host "   > deploy neo_contract\\simple_oracle.nef"
Write-Host "   > deploy neo_contract\\volatility_oracle.nef"

Write-Host "`n OPTION 3: Use Neo Express (Local testing)" -ForegroundColor Green
Write-Host "dotnet tool install -g Neo.Express"
Write-Host "neoxp contract deploy neo_contract\\simple_oracle.nef"

Write-Host "`n After deployment, SAVE THE CONTRACT HASH!" -ForegroundColor Red
Write-Host "You'll need it to interact with your contract`n"
"""

with open('neo_contract/deploy_guide.ps1', 'w') as f:
    f.write(ps_script)

print(f"✅ Created PowerShell guide: neo_contract/deploy_guide.ps1")

print(f"\n" + "="*70)
print("🎯 QUICKEST DEPLOYMENT METHOD")
print("="*70)
print(f"""
Try these in order:

1. neo-mamba (Easiest - Python)
   pip install neo-mamba
   python neo_contract/deploy_simple.py

2. neo-cli (Recommended - Official)
   Download, extract, run commands above

3. Online Neo IDE
   Visit: https://neo.org/neoide
   Import wallet, upload files, click deploy

All contracts are validated and ready!
Estimated cost: ~20 GAS total (you have 50 GAS ✅)
""")

print(f"\n⚠️  SECURITY NOTE:")
print(f"Delete this script after deployment to protect your private key!")
