"""
Professional Email Alert System
Send alerts like Bloomberg Terminal
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

class EmailAlertSystem:
    """
    Send professional email alerts
    Triggers on volatility spikes, arbitrage opportunities, etc.
    """
    
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = os.getenv('ALERT_EMAIL', 'agentspoons@example.com')
        self.sender_password = os.getenv('ALERT_PASSWORD', '')
        
    def create_alert_email(self, alert_type, data):
        """Create formatted HTML email"""
        
        if alert_type == "VOLATILITY_SPIKE":
            subject = f"🚨 VOLATILITY SPIKE ALERT - {data['pair']}"
            body = self._volatility_spike_template(data)
        elif alert_type == "ARBITRAGE_OPPORTUNITY":
            subject = f"💰 ARBITRAGE OPPORTUNITY - {data['pair']}"
            body = self._arbitrage_template(data)
        elif alert_type == "DAILY_SUMMARY":
            subject = f"📊 Daily Market Summary - {datetime.now().strftime('%Y-%m-%d')}"
            body = self._daily_summary_template(data)
        else:
            subject = "AgentSpoons Alert"
            body = str(data)
        
        return subject, body
    
    def _volatility_spike_template(self, data):
        """HTML template for volatility spike"""
        return f"""
        <html>
        <head>
            <style>
                body {{ font-family: 'Courier New', monospace; background-color: #0a0a0a; color: #e0e0e0; }}
                .header {{ background-color: #ff8c00; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background-color: #1a1a1a; margin: 20px; }}
                .metric {{ font-size: 18px; margin: 10px 0; }}
                .value {{ color: #ff0000; font-weight: bold; font-size: 24px; }}
                .footer {{ text-align: center; padding: 10px; font-size: 12px; color: #666; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th {{ background-color: #ff8c00; color: white; padding: 10px; }}
                td {{ padding: 10px; border: 1px solid #333; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🥄 AGENTSPOONS ALERT</h1>
                <h2>VOLATILITY SPIKE DETECTED</h2>
            </div>
            
            <div class="content">
                <p><strong>Alert Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
                <p><strong>Asset Pair:</strong> {data.get('pair', 'NEO/USDT')}</p>
                
                <div class="metric">
                    <span>Current Volatility: </span>
                    <span class="value">{data.get('current_vol', 0.65):.2%}</span>
                </div>
                
                <div class="metric">
                    <span>24h Average: </span>
                    <span>{data.get('avg_vol', 0.52):.2%}</span>
                </div>
                
                <div class="metric">
                    <span>Spike: </span>
                    <span class="value">+{data.get('spike_pct', 25):.1f}%</span>
                </div>
                
                <h3>Market Data</h3>
                <table>
                    <tr>
                        <th>Metric</th>
                        <th>Value</th>
                    </tr>
                    <tr>
                        <td>Price</td>
                        <td>${data.get('price', 15.23):.2f}</td>
                    </tr>
                    <tr>
                        <td>Realized Volatility</td>
                        <td>{data.get('rv', 0.65):.2%}</td>
                    </tr>
                    <tr>
                        <td>Implied Volatility</td>
                        <td>{data.get('iv', 0.72):.2%}</td>
                    </tr>
                    <tr>
                        <td>GARCH Forecast</td>
                        <td>{data.get('forecast', 0.68):.2%}</td>
                    </tr>
                </table>
                
                <h3>Recommended Actions</h3>
                <ul>
                    <li>Consider volatility arbitrage strategies</li>
                    <li>Adjust position sizing for increased risk</li>
                    <li>Review stop-loss levels</li>
                    <li>Monitor for continued volatility expansion</li>
                </ul>
                
                <p style="margin-top: 30px;">
                    <strong>Data Source:</strong> AgentSpoons Oracle on Neo N3 Blockchain<br/>
                    <strong>Contract:</strong> 0x7a2b...f3c9<br/>
                    <strong>Confidence:</strong> {data.get('confidence', 0.95):.0%}
                </p>
            </div>
            
            <div class="footer">
                <p>This alert was generated automatically by AgentSpoons Volatility Oracle</p>
                <p>To unsubscribe or modify alert settings, visit: https://agentspoons.io/alerts</p>
            </div>
        </body>
        </html>
        """
    
    def _arbitrage_template(self, data):
        """HTML template for arbitrage opportunity"""
        return f"""
        <html>
        <head>
            <style>
                body {{ font-family: 'Courier New', monospace; background-color: #0a0a0a; color: #e0e0e0; }}
                .header {{ background-color: #00ff00; color: black; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background-color: #1a1a1a; margin: 20px; }}
                .opportunity {{ background-color: #003300; padding: 15px; margin: 20px 0; border-left: 5px solid #00ff00; }}
                .profit {{ color: #00ff00; font-size: 32px; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>💰 ARBITRAGE OPPORTUNITY</h1>
            </div>
            
            <div class="content">
                <div class="opportunity">
                    <h2>STRATEGY: {data.get('strategy', 'Volatility Arbitrage')}</h2>
                    <p class="profit">Expected Profit: {data.get('expected_profit', 0.058):.2%}</p>
                    <p><strong>Confidence Score:</strong> {data.get('confidence', 0.85):.0%}</p>
                </div>
                
                <h3>Setup</h3>
                <p><strong>Asset:</strong> {data.get('pair', 'NEO/USDT')}</p>
                <p><strong>IV-RV Spread:</strong> {data.get('spread', 0.058):.2%}</p>
                <p><strong>Action:</strong> {data.get('action', 'SELL IMPLIED VOL / BUY REALIZED VOL')}</p>
                
                <h3>Entry Parameters</h3>
                <ul>
                    <li>Current IV: {data.get('iv', 0.581):.2%}</li>
                    <li>Current RV: {data.get('rv', 0.523):.2%}</li>
                    <li>Recommended Position Size: {data.get('position_size', 0.10):.0%} of portfolio</li>
                    <li>Expected Holding Period: {data.get('holding_period', '3-5')} days</li>
                </ul>
                
                <h3>Risk Management</h3>
                <ul>
                    <li>Stop Loss: {data.get('stop_loss', -0.02):.2%}</li>
                    <li>Take Profit: {data.get('take_profit', 0.04):.2%}</li>
                    <li>Max Risk: ${data.get('max_risk', 250):.0f}</li>
                </ul>
                
                <p style="margin-top: 30px; font-size: 12px; color: #666;">
                    <em>This is not financial advice. Past performance does not guarantee future results. 
                    Always conduct your own research and risk assessment.</em>
                </p>
            </div>
        </body>
        </html>
        """
    
    def _daily_summary_template(self, data):
        """HTML template for daily summary"""
        return f"""
        <html>
        <head>
            <style>
                body {{ font-family: 'Courier New', monospace; background-color: #0a0a0a; color: #e0e0e0; }}
                .header {{ background-color: #00bfff; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background-color: #1a1a1a; margin: 20px; }}
                .summary-box {{ background-color: #2a2a2a; padding: 15px; margin: 15px 0; }}
                table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
                th {{ background-color: #00bfff; color: white; padding: 10px; text-align: left; }}
                td {{ padding: 10px; border-bottom: 1px solid #333; }}
                .positive {{ color: #00ff00; }}
                .negative {{ color: #ff0000; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>📊 DAILY MARKET SUMMARY</h1>
                <h3>{datetime.now().strftime('%A, %B %d, %Y')}</h3>
            </div>
            
            <div class="content">
                <div class="summary-box">
                    <h2>Market Overview</h2>
                    <table>
                        <tr>
                            <th>Pair</th>
                            <th>Price</th>
                            <th>24h Change</th>
                            <th>Volatility</th>
                        </tr>
                        <tr>
                            <td>NEO/USDT</td>
                            <td>${data.get('neo_price', 15.23):.2f}</td>
                            <td class="{'positive' if data.get('neo_change', 2.4) > 0 else 'negative'}">
                                {data.get('neo_change', 2.4):+.2f}%
                            </td>
                            <td>{data.get('neo_vol', 0.523):.2%}</td>
                        </tr>
                        <tr>
                            <td>GAS/USDT</td>
                            <td>${data.get('gas_price', 5.12):.2f}</td>
                            <td class="{'positive' if data.get('gas_change', -1.2) > 0 else 'negative'}">
                                {data.get('gas_change', -1.2):+.2f}%
                            </td>
                            <td>{data.get('gas_vol', 0.481):.2%}</td>
                        </tr>
                    </table>
                </div>
                
                <div class="summary-box">
                    <h2>Key Metrics</h2>
                    <ul>
                        <li>Total Calculations: {data.get('calculations', 1247)}</li>
                        <li>Blockchain Publications: {data.get('publications', 24)}</li>
                        <li>Arbitrage Opportunities Detected: {data.get('opportunities', 5)}</li>
                        <li>Average IV-RV Spread: {data.get('avg_spread', 0.052):.2%}</li>
                    </ul>
                </div>
                
                <div class="summary-box">
                    <h2>Tomorrow's Forecast</h2>
                    <p><strong>GARCH Prediction:</strong> Volatility expected to 
                    {'increase' if data.get('forecast_direction', 1) > 0 else 'decrease'} 
                    to {data.get('forecast', 0.547):.2%}</p>
                    <p><strong>Regime:</strong> {data.get('regime', 'MEDIUM-HIGH VOLATILITY')}</p>
                    <p><strong>Recommendation:</strong> {data.get('recommendation', 'Monitor for volatility expansion')}</p>
                </div>
                
                <p style="text-align: center; margin-top: 30px;">
                    <strong>Generated by AgentSpoons Oracle on Neo N3 Blockchain</strong>
                </p>
            </div>
        </body>
        </html>
        """
    
    def send_alert(self, recipient, alert_type, data, attach_pdf=None):
        """Send email alert"""
        
        subject, html_body = self.create_alert_email(alert_type, data)
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = self.sender_email
        msg['To'] = recipient
        msg['Subject'] = subject
        
        # Attach HTML body
        msg.attach(MIMEText(html_body, 'html'))
        
        # Attach PDF if provided
        if attach_pdf:
            with open(attach_pdf, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attach_pdf)}')
                msg.attach(part)
        
        try:
            # Send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            
            if self.sender_password:
                server.login(self.sender_email, self.sender_password)
            
            server.send_message(msg)
            server.quit()
            
            print(f"✅ Email alert sent to {recipient}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send email: {e}")
            return False

# Demo usage
if __name__ == "__main__":
    alert_system = EmailAlertSystem()
    
    # Test volatility spike alert
    data = {
        'pair': 'NEO/USDT',
        'current_vol': 0.65,
        'avg_vol': 0.52,
        'spike_pct': 25,
        'price': 15.23,
        'rv': 0.65,
        'iv': 0.72,
        'forecast': 0.68,
        'confidence': 0.95
    }
    
    # Save HTML to file for preview
    _, html = alert_system.create_alert_email("VOLATILITY_SPIKE", data)
    with open('outputs/sample_alert_email.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("OK Sample email saved to: outputs/sample_alert_email.html")
    print("Open in browser to preview")
