"""Utility to launch the production dashboard on an available port."""
from __future__ import annotations

import os
import sys
from pathlib import Path


def _ensure_src_on_path() -> None:
    """Prepend the repository's src directory to sys.path if needed."""
    base_dir = Path(__file__).resolve().parent
    src_dir = base_dir / "src"
    if src_dir.is_dir():
        sys.path.insert(0, str(src_dir))


def main() -> None:
    _ensure_src_on_path()

    from dashboard.production_dashboard import app  # pylint: disable=import-error

    print("=" * 70)
    print("Starting production dashboard launcher")
    print("=" * 70)

    ports = [8080, 8081, 8082, 5000, 3000]

    for port in ports:
        try:
            print(f"\nAttempting to bind to port {port}...")
            print(f"Visit: http://localhost:{port}")
            print(f"Or:    http://127.0.0.1:{port}")
            print("-" * 70)

            app.run(
                debug=False,
                port=port,
                host="127.0.0.1",
            )
            break
        except OSError as exc:
            print(f"Port {port} unavailable: {exc}")
            continue
    else:
        print("\nNo listed ports were available.")
        print("Try running: python -m http.server 8000")


if __name__ == "__main__":
    main()
