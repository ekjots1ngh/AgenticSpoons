"""
Intelligent Alert System
Machine learning-based anomaly detection
"""
import numpy as np
from datetime import datetime
import json
from collections import deque

class SmartAlertSystem:
    """
    Intelligent alert system using statistical anomaly detection
    """
    
    def __init__(self):
        self.price_history = deque(maxlen=100)
        self.vol_history = deque(maxlen=100)
        self.alerts = []
        
        # Alert thresholds
        self.thresholds = {
            'price_spike': 0.05,      # 5% price move
            'vol_spike': 0.20,         # 20% volatility increase
            'spread_threshold': 0.10,  # 10% IV-RV spread
            'volume_spike': 2.0,       # 2x average volume
        }
    
    def add_data_point(self, price, vol, volume):
        """Add new data point and check for alerts"""
        
        self.price_history.append(price)
        self.vol_history.append(vol)
        
        alerts_triggered = []
        
        # Check price spike
        if len(self.price_history) >= 2:
            price_change = (price - self.price_history[-2]) / self.price_history[-2]
            if abs(price_change) > self.thresholds['price_spike']:
                alerts_triggered.append({
                    'type': 'PRICE_SPIKE',
                    'severity': 'HIGH' if abs(price_change) > 0.10 else 'MEDIUM',
                    'message': f"Price {'surged' if price_change > 0 else 'dropped'} {abs(price_change):.2%}",
                    'timestamp': datetime.now().isoformat(),
                    'value': price_change
                })
        
        # Check volatility spike
        if len(self.vol_history) >= 10:
            avg_vol = np.mean(list(self.vol_history)[:-1])
            vol_change = (vol - avg_vol) / avg_vol
            if vol_change > self.thresholds['vol_spike']:
                alerts_triggered.append({
                    'type': 'VOLATILITY_SPIKE',
                    'severity': 'HIGH' if vol_change > 0.40 else 'MEDIUM',
                    'message': f"Volatility increased {vol_change:.2%} above average",
                    'timestamp': datetime.now().isoformat(),
                    'value': vol_change
                })
        
        # Check volume anomaly
        if volume is not None:
            # Simulate average volume check
            avg_volume = 1000000  # Example
            if volume > avg_volume * self.thresholds['volume_spike']:
                alerts_triggered.append({
                    'type': 'VOLUME_SPIKE',
                    'severity': 'MEDIUM',
                    'message': f"Volume {volume/avg_volume:.1f}x above average",
                    'timestamp': datetime.now().isoformat(),
                    'value': volume/avg_volume
                })
        
        # Save alerts
        for alert in alerts_triggered:
            self.alerts.append(alert)
        
        return alerts_triggered
    
    def check_spread_alert(self, iv, rv):
        """Check for IV-RV spread alerts"""
        
        spread = iv - rv
        spread_pct = spread / rv if rv > 0 else 0
        
        if abs(spread_pct) > self.thresholds['spread_threshold']:
            alert = {
                'type': 'SPREAD_ALERT',
                'severity': 'HIGH' if abs(spread_pct) > 0.15 else 'MEDIUM',
                'message': f"IV-RV spread at {spread:.2%} ({spread_pct:.1%} relative)",
                'timestamp': datetime.now().isoformat(),
                'value': spread,
                'action': 'SELL_VOLATILITY' if spread > 0 else 'BUY_VOLATILITY'
            }
            
            self.alerts.append(alert)
            return alert
        
        return None
    
    def get_recent_alerts(self, hours=24, severity=None):
        """Get recent alerts"""
        
        cutoff = datetime.now().timestamp() - (hours * 3600)
        
        recent = [
            a for a in self.alerts
            if datetime.fromisoformat(a['timestamp']).timestamp() > cutoff
        ]
        
        if severity:
            recent = [a for a in recent if a['severity'] == severity]
        
        return sorted(recent, key=lambda x: x['timestamp'], reverse=True)
    
    def generate_alert_dashboard_html(self):
        """Generate HTML dashboard for alerts"""
        
        recent_alerts = self.get_recent_alerts(hours=24)
        
        html = f"""
        <html>
        <head>
            <style>
                body {{ 
                    font-family: 'Courier New', monospace; 
                    background-color: #0a0a0a; 
                    color: #e0e0e0; 
                    padding: 20px;
                }}
                .header {{
                    background-color: #ff8c00;
                    color: white;
                    padding: 15px;
                    text-align: center;
                    margin-bottom: 20px;
                }}
                .alert {{
                    padding: 15px;
                    margin: 10px 0;
                    border-left: 5px solid;
                    background-color: #1a1a1a;
                }}
                .alert.HIGH {{ border-color: #ff0000; }}
                .alert.MEDIUM {{ border-color: #ff8c00; }}
                .alert.LOW {{ border-color: #00ff00; }}
                .alert-time {{
                    color: #666;
                    font-size: 12px;
                }}
                .alert-message {{
                    font-size: 16px;
                    margin: 10px 0;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>AGENTSPOONS ALERTS</h1>
                <p>Last 24 Hours - {len(recent_alerts)} Alerts</p>
            </div>
        """
        
        if not recent_alerts:
            html += "<p style='text-align: center; color: #666;'>No alerts in the last 24 hours</p>"
        else:
            for alert in recent_alerts:
                time_str = datetime.fromisoformat(alert['timestamp']).strftime('%H:%M:%S')
                
                html += f"""
                <div class="alert {alert['severity']}">
                    <div class="alert-time">{time_str} | {alert['type']} | {alert['severity']}</div>
                    <div class="alert-message">{alert['message']}</div>
                </div>
                """
        
        html += """
        </body>
        </html>
        """
        
        return html
    
    def save_alerts_to_file(self, filename='outputs/alerts.json'):
        """Save alerts to JSON file"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                'generated_at': datetime.now().isoformat(),
                'alert_count': len(self.alerts),
                'alerts': self.alerts
            }, f, indent=2)
        
        print(f"OK Alerts saved to: {filename}")

# Demo
if __name__ == "__main__":
    print("="*70)
    print("SMART ALERT SYSTEM DEMO")
    print("="*70)
    
    alert_system = SmartAlertSystem()
    
    # Simulate data points
    print("\nSimulating market data...\n")
    
    for i in range(50):
        price = 15 + np.random.normal(0, 0.2)
        vol = 0.50 + np.random.normal(0, 0.05)
        volume = 1000000 * (1 + np.random.normal(0, 0.3))
        
        # Inject some spikes
        if i == 25:
            price *= 1.08  # 8% price spike
        if i == 30:
            vol *= 1.35   # 35% vol spike
        
        alerts = alert_system.add_data_point(price, vol, volume)
        
        for alert in alerts:
            print(f"[{alert['severity']}] {alert['type']}: {alert['message']}")
    
    # Check spread alert
    print("\nChecking IV-RV spread...")
    spread_alert = alert_system.check_spread_alert(iv=0.65, rv=0.52)
    if spread_alert:
        print(f"{spread_alert['message']}")
        print(f"   Action: {spread_alert['action']}")
    
    # Generate dashboard
    html = alert_system.generate_alert_dashboard_html()
    with open('outputs/alerts_dashboard.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("\nOK Alert dashboard saved to: outputs/alerts_dashboard.html")
    
    # Save to JSON
    alert_system.save_alerts_to_file()
    
    print(f"\nTotal alerts generated: {len(alert_system.alerts)}")
    print("="*70)
