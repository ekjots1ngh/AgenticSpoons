# Neo Contract Development - Next Steps Guide

## Current State
- ✅ Neo SDKs fully installed (neo3-lib, neo3-boa v1.4.1, neo3crypto, neo-mamba)
- ✅ Smart contract architecture designed
- 🔧 **Blocker**: Contract compilation - boa3 type system strictness
- ✅ Git repository clean, all work committed

## The boa3 Challenge

### Root Cause
boa3 v1.4.1 is very strict about Neo bytecode generation:
- Generic `storage.get()` doesn't work - must use typed variants
- String encoding at compile-time not supported
- Type hints must match exactly what bytecode expects
- Functions must generate meaningful bytecode (not empty)

### Current Error
```
ERROR: Could not compile: An empty script was generated
```
This means the functions aren't being recognized as valid contract entry points.

## Solution Paths (in order of recommendation)

### Path 1: Fix boa3 Compilation (Recommended)
**Effort**: Medium | **Success**: Likely

1. **Study a working boa3 contract example**
   - Search neo3-boa GitHub for `examples/` folder
   - Look for minimal contract that compiles successfully
   - Compare structure with our `minimal_oracle.py`

2. **Key things to verify**
   - Do functions need special decorators or markers?
   - Are there restrictions on what makes a valid entry point?
   - Does the contract need initialization (like in EOS/Tron)?

3. **Test incrementally**
   ```
   minimal_oracle.py (verify compiles)
   → add one method
   → add storage access
   → add type checking
   → build up to full oracle
   ```

### Path 2: Use neo-mamba Instead
**Effort**: Low | **Success**: Unknown

1. **Investigate neo-mamba** as alternative to boa3
   - Check if it supports Python contracts
   - Compare syntax and features
   - May be more flexible

2. **If viable**: Rewrite contracts in neo-mamba
3. **If not viable**: Return to Path 1

### Path 3: Write Contract in Different Language
**Effort**: High | **Success**: Certain

1. **Use C# (official way)**
   - Requires Visual Studio or mono
   - Full support in Neo tooling
   - More examples available

2. **Use other supported languages**
   - Java, Go, etc.
   - Well-documented
   - Official neo-cli support

### Path 4: Deploy Without Compilation
**Effort**: Medium | **Success**: Possible

1. **Use existing contract from Neo**
   - Find published oracle contract
   - Adapt/fork existing work
   - Deploy pre-compiled bytecode

## Recommended Action

### Start Now (5-10 minutes)
```bash
cd neo_contract

# Search GitHub for working examples
# https://github.com/CityOfZion/neo3-boa/tree/main/examples

# Look specifically for:
# - contracts/hello_world.py
# - contracts/storage_example.py
# - Any contract that compiles successfully
```

### Compare Structure
```
Their working example:
- How do methods look?
- What decorators/markers are used?
- How do they handle storage?

Our minimal_oracle.py:
- What's different?
- What are we missing?
```

### Debug Approach
```python
# Try in order:

# 1. Empty contract (should fail with "empty script")
def verify() -> bool:
    return True

# 2. Contract with simple method
def hello() -> str:
    return "Hello"

# 3. Contract with storage read (no write first)
def get_data() -> bytes:
    return storage.get(b'key')

# 4. Contract with storage write
def set_data() -> bool:
    storage.put(b'key', b'value')
    return True
```

### Documentation to Read
1. **boa3 Official Docs**: Check if there's a "Getting Started" guide
2. **Neo N3 Smart Contract Basics**: Understand contract entry points
3. **boa3 API Reference**: See all available storage methods

## Files to Modify
- `neo_contract/minimal_oracle.py` - Use this to experiment
- `neo_contract/volatility_oracle.py` - Final contract once working
- `neo_contract/compile.py` - May need updates for new structure

## Testing Strategy

### Local Testing
```bash
# Test compilation
python -m boa3.cli compile minimal_oracle.py

# If successful, generates:
# - minimal_oracle.nef (bytecode)
# - minimal_oracle.manifest.json (ABI)
```

### Testnet Testing
```bash
# Once compiled successfully:

# 1. Get testnet wallet
python -m neon.cli wallet create --name testnet-wallet

# 2. Get GAS from faucet
# https://faucet.ngd.network/ 

# 3. Deploy contract
python -m neon.cli contract deploy minimal_oracle.nef --wallet testnet-wallet

# 4. Invoke methods
python -m neon.cli contract invoke <contract-hash> verify
```

## Success Metrics

✅ **Phase 1**: Contract compiles to .nef file
✅ **Phase 2**: Contract deploys to testnet 
✅ **Phase 3**: Contract methods callable
✅ **Phase 4**: Volatility data stored/retrieved
✅ **Phase 5**: Integration with AgentSpoons pipeline

## Useful Commands

```bash
# Check boa3 version
python -c "import boa3; print(boa3.__version__)"

# List available storage methods
python -c "from boa3.sc import storage; print([x for x in dir(storage) if not x.startswith('_')])"

# View contract errors in detail
python -m boa3.cli compile minimal_oracle.py --no-failfast --log-level DEBUG

# Check neo3-boa examples
pip show neo3-boa | grep Location
# Then browse <location>/boa3/examples/
```

## Resources

### Code
- Current contract attempts: `neo_contract/` folder
- Session notes: `SESSION_SUMMARY.md`

### External
- neo3-boa: https://github.com/CityOfZion/neo3-boa
- Neo Docs: https://docs.neo.org/n3/
- Neo Testnet Faucet: https://faucet.ngd.network/
- neo-cli: https://github.com/neo-project/neo-cli

## Estimated Timeline

| Task | Time | Difficulty |
|------|------|-----------|
| Study working examples | 15 min | Easy |
| Debug compilation issue | 30 min | Medium |
| Fix contract syntax | 30 min | Medium |
| Test on testnet | 30 min | Easy |
| **Total** | **~2 hours** | - |

---

## Key Takeaway

The foundation is solid - Neo SDKs work, architecture is designed, development environment is ready. The remaining challenge is **purely syntactic** (getting boa3 to accept the contract structure). This is very solvable with the right example to reference.

Next session should start with: **"Find a working boa3 contract example and compare"**
