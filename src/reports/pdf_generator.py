"""
Generate Professional PDF Reports
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import json

class VolatilityReport:
    """Generate professional PDF reports"""
    
    def __init__(self, filename='reports/volatility_report.pdf'):
        self.filename = filename
        self.doc = SimpleDocTemplate(filename, pagesize=letter)
        self.styles = getSampleStyleSheet()
        self.story = []
        
        # Custom styles
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#00d4ff'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
    
    def add_title(self, text):
        """Add title"""
        self.story.append(Paragraph(text, self.title_style))
        self.story.append(Spacer(1, 0.2*inch))
    
    def add_section(self, title, content):
        """Add section with title and content"""
        section_style = self.styles['Heading2']
        self.story.append(Paragraph(title, section_style))
        self.story.append(Spacer(1, 0.1*inch))
        self.story.append(Paragraph(content, self.styles['BodyText']))
        self.story.append(Spacer(1, 0.2*inch))
    
    def add_metrics_table(self, metrics):
        """Add metrics table"""
        data = [['Metric', 'Value']]
        
        for key, value in metrics.items():
            if isinstance(value, float):
                data.append([key, f"{value:.2%}" if abs(value) < 10 else f"${value:.2f}"])
            else:
                data.append([key, str(value)])
        
        table = Table(data, colWidths=[3*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a1f3a')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        self.story.append(table)
        self.story.append(Spacer(1, 0.3*inch))
    
    def add_chart(self, data, chart_type='volatility'):
        """Add matplotlib chart"""
        import pandas as pd
        
        plt.figure(figsize=(8, 4))
        plt.style.use('dark_background')
        
        if chart_type == 'volatility':
            df = pd.DataFrame(data)
            plt.plot(df['realized_vol'] * 100, label='Realized Vol', linewidth=2)
            plt.plot(df['implied_vol'] * 100, label='Implied Vol', linewidth=2)
            plt.xlabel('Time')
            plt.ylabel('Volatility %')
            plt.title('Volatility Comparison')
            plt.legend()
            plt.grid(alpha=0.3)
        
        # Save
        chart_path = 'data/temp_chart.png'
        plt.savefig(chart_path, bbox_inches='tight', facecolor='#0a0e27')
        plt.close()
        
        # Add to PDF
        self.story.append(Image(chart_path, width=6*inch, height=3*inch))
        self.story.append(Spacer(1, 0.3*inch))
    
    def generate(self):
        """Generate PDF"""
        self.doc.build(self.story)
        print(f"✅ Report generated: {self.filename}")

def generate_daily_report():
    """Generate daily volatility report"""
    import os
    import pandas as pd
    
    os.makedirs('reports', exist_ok=True)
    
    # Load data
    with open('data/results.json', 'r') as f:
        data = json.load(f)
    
    neo_data = [d for d in data if d['pair'] == 'NEO/USDT'][-100:]
    
    # Create report
    report = VolatilityReport(f'reports/volatility_report_{datetime.now().strftime("%Y%m%d")}.pdf')
    
    # Title
    report.add_title('🥄 AgentSpoons Volatility Report')
    
    # Executive Summary
    latest = neo_data[-1]
    summary = f"""
    This report provides a comprehensive analysis of volatility metrics for NEO/USDT 
    as of {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.
    
    Current NEO Price: ${latest['price']:.2f}
    Realized Volatility: {latest['realized_vol']:.2%}
    Implied Volatility: {latest['implied_vol']:.2%}
    """
    
    report.add_section('Executive Summary', summary)
    
    # Metrics
    df = pd.DataFrame(neo_data)
    
    metrics = {
        'Current Price': latest['price'],
        'Realized Vol (30D)': latest['realized_vol'],
        'Implied Vol': latest['implied_vol'],
        'GARCH Forecast': latest['garch_forecast'],
        'Volatility Spread': latest['spread'],
        'Avg Vol (Period)': df['realized_vol'].mean(),
        'Max Vol': df['realized_vol'].max(),
        'Min Vol': df['realized_vol'].min(),
    }
    
    report.add_metrics_table(metrics)
    
    # Chart
    report.add_chart(neo_data, 'volatility')
    
    # Analysis
    analysis = f"""
    The current volatility spread of {latest['spread']:.2%} indicates 
    {'a potential arbitrage opportunity' if abs(latest['spread']) > 0.05 else 'balanced market conditions'}.
    
    Over the analysis period, volatility has ranged from {df['realized_vol'].min():.2%} to {df['realized_vol'].max():.2%},
    with an average of {df['realized_vol'].mean():.2%}.
    """
    
    report.add_section('Market Analysis', analysis)
    
    # Generate
    report.generate()

if __name__ == "__main__":
    generate_daily_report()
