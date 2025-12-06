"""
Test all advanced features
"""
import subprocess
import sys

tests = [
    ("C++ Engine", "cd cpp_engine && python test_cpp_engine.py"),
    ("ML Models", "python src/ml/advanced_models.py"),
    ("Quant Analytics", "python src/quant/advanced_analytics.py"),
    ("Time Series", "python src/forecasting/time_series_models.py"),
    ("Backtesting", "echo '1' | python src/backtesting/strategy_backtester.py"),
]

print("="*70)
print("🧪 TESTING ALL FEATURES")
print("="*70)

for name, command in tests:
    print(f"\n Testing {name}...")
    try:
        subprocess.run(command, shell=True, check=True, timeout=60)
        print(f"✅ {name} passed")
    except Exception as e:
        print(f"❌ {name} failed: {e}")

print("\n" + "="*70)
print("🎉 ALL TESTS COMPLETE")
print("="*70)
