"""
Compile Neo3-boa smart contract to bytecode
"""
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from boa3.compiler import compile_file
    
    # Get contract path
    contract_path = Path(__file__).parent / 'volatility_oracle.py'
    
    print("="*70)
    print("Compiling Neo N3 Smart Contract")
    print("="*70)
    print(f"\nSource: {contract_path}")
    
    # Compile
    output_path = contract_path.parent / 'volatility_oracle.nef'
    compile_file(str(contract_path), output=str(output_path))
    
    print(f"Output: {output_path}")
    
    if output_path.exists():
        size = output_path.stat().st_size
        print(f"\n✓ Contract compiled successfully ({size} bytes)")
        print(f"✓ Ready for deployment to Neo N3")
    else:
        print("\n✗ Compilation failed")
        
except ImportError as e:
    print(f"Error: neo3-boa not available: {e}")
except Exception as e:
    print(f"Compilation error: {e}")

print("="*70)
