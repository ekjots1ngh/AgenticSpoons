"""
Launcher for WebSocket server + Dashboard stack
"""
import subprocess
import sys
import time
import os
from pathlib import Path

def run_command(cmd, name, output_file=None):
    """Run command in background"""
    print(f"\n📡 Starting {name}...")
    
    if output_file:
        out = open(output_file, 'w')
        err = open(output_file.replace('.out', '.err'), 'w')
    else:
        out = None
        err = None
    
    process = subprocess.Popen(
        cmd,
        shell=True,
        stdout=out,
        stderr=err
    )
    
    print(f"   ✓ {name} started (PID: {process.pid})")
    return process

def main():
    os.makedirs('logs', exist_ok=True)
    
    print("\n" + "="*60)
    print("  AGENTIC SPOONS - WEBSOCKET INFRASTRUCTURE LAUNCHER")
    print("="*60)
    
    processes = []
    
    # Start data generator
    p1 = run_command(
        'python src/enhanced_demo.py',
        'Data Generator (enhanced_demo)',
        'logs/enhanced_demo_ws.out'
    )
    processes.append(('Data Generator', p1))
    time.sleep(2)
    
    # Start WebSocket server
    p2 = run_command(
        'python src/api/websocket_server.py',
        'WebSocket Server',
        'logs/websocket_server.out'
    )
    processes.append(('WebSocket Server', p2))
    time.sleep(2)
    
    # Start dashboard
    p3 = run_command(
        'python src/championship_dashboard.py',
        'Championship Dashboard',
        'logs/championship_dashboard_ws.out'
    )
    processes.append(('Dashboard', p3))
    time.sleep(2)
    
    print("\n" + "="*60)
    print("  ALL SERVICES RUNNING")
    print("="*60)
    print("\n🌐 Access:")
    print("   Dashboard:      http://localhost:8050")
    print("   WebSocket:      ws://localhost:8765")
    print("\n📊 Data files:")
    print("   Results:        data/results.json")
    print("   Logs:           logs/")
    print("\n💡 To stop all services, press Ctrl+C")
    print("="*60 + "\n")
    
    try:
        # Keep running
        while True:
            time.sleep(1)
            # Check if processes are still alive
            for name, proc in processes:
                if proc.poll() is not None:
                    print(f"⚠️  {name} stopped (exit code: {proc.returncode})")
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down services...")
        for name, proc in processes:
            try:
                proc.terminate()
                print(f"   ✓ {name} terminated")
            except:
                pass
        print("   Done.\n")

if __name__ == "__main__":
    main()
