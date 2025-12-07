#!/usr/bin/env python
"""
Quick start script for AgentSpoons Dashboard with Theme Toggle
Run this to test the new Dark/Light theme functionality
"""

import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("="*80)
print("🥄 AGENTSPOONS DASHBOARD - WITH THEME TOGGLE")
print("="*80)
print("\n📋 FEATURES:")
print("  ✅ Dark/Light theme toggle")
print("  ✅ Persistent theme selection (localStorage)")
print("  ✅ Dynamic color switching")
print("  ✅ All charts respond to theme changes")
print("\n🎨 THEME OPTIONS:")
print("  • Dark Mode (default) - Navy blue background with cyan accents")
print("  • Light Mode - Clean white background with dark text")
print("\n🔘 HOW TO USE:")
print("  1. Dashboard will open at http://localhost:8050")
print("  2. Look for 'Theme' button in top-right corner")
print("  3. Click to toggle between Dark ☾ and Light ☀ modes")
print("  4. Your choice persists across browser sessions")
print("\n" + "="*80)
print("🚀 Starting dashboard server...")
print("="*80 + "\n")

# Import and run championship dashboard
try:
    from championship_dashboard import app
    app.run(debug=True, host='0.0.0.0', port=8050)
except ImportError:
    print("\n❌ Error: Could not import championship_dashboard")
    print("Make sure you're running from the agentspoons directory")
    print("\nTry:")
    print("  cd agentspoons")
    print("  python run_dashboard_with_theme.py")
    sys.exit(1)
except Exception as e:
    print(f"\n❌ Error starting dashboard: {e}")
    sys.exit(1)
