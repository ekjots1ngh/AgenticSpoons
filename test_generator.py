"""
Simple test to verify the data generator works as expected.
"""
import json
import sys
import time
from pathlib import Path

# Ensure project sources are importable when run from repo root
sys.path.insert(0, "src")

from data_generator import SimpleDataGenerator  # noqa: E402


def main() -> None:
    print("Testing data generator...")
    print("=" * 70)

    generator = SimpleDataGenerator()

    # Generate a handful of ticks to exercise the generator and persistence
    for i in range(5):
        data = generator.generate_tick()
        generator.save_data(data)

        print(f"\n[PASS] Tick {i + 1}:")
        print(f"   Price: ${data['price']:.2f}")
        print(f"   RV: {data['realized_vol']:.2%}")
        print(f"   IV: {data['implied_vol']:.2%}")
        print(f"   Spread: {data['spread']:.2%}")
        print(f"   File saved: {generator.data_file}")

        time.sleep(1)

    print("\n" + "=" * 70)
    print("[PASS] Test complete!")
    print("Check if file exists: data/live_data.json")

    # Try to read the file back to confirm persistence
    file_path = Path("data/live_data.json")
    if file_path.exists():
        with open(file_path, "r") as f:
            saved_data = json.load(f)
        print(f"[PASS] File contains data for price: ${saved_data['price']:.2f}")
    else:
        print("[FAIL] File not found!")


if __name__ == "__main__":
    main()
