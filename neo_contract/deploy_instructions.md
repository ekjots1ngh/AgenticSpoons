# 🚀 Deploy to Neo Testnet in 5 Minutes

## Method 1: NeoCompiler (EASIEST - Use This!)

1. **Go to Neo Compiler**
   - Visit: https://neo3.testnet.neocompiler.io/

2. **Upload Files**
   - Click "Upload Contract"
   - Select `volatility_oracle.nef`
   - Select `volatility_oracle.manifest.json`

3. **Connect Wallet**
   - Install NeoLine extension: https://neoline.io/
   - Import your private key from `agentspoons_wallet.json`
   - Connect to TESTNET in NeoLine

4. **Deploy**
   - Click "Deploy Contract"
   - Confirm transaction in NeoLine
   - Wait ~15 seconds
   - Copy CONTRACT HASH!

5. **Verify**
   - Visit: https://testnet.neotube.io/
   - Search your contract hash
   - See your deployed contract!

## Method 2: Neo-Express (For Local Testing)
```bash
# Install neo-express
npm install -g @neo-one/cli

# Initialize project
neo-express create

# Start local blockchain
neo-express run

# Deploy
neo-express contract deploy volatility_oracle.nef
```

## Method 3: Python Script (Advanced)

See `deploy_with_rpc.py` for programmatic deployment.

---

**CRITICAL**: After deployment, save your CONTRACT HASH!
This is what you'll use to interact with your contract.
