"""
Professional Excel exports with formatting
Bloomberg-quality spreadsheets
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import xlsxwriter
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import LineChart, Reference

class ProfessionalExcelExport:
    """Generate Bloomberg-style Excel reports"""
    
    def __init__(self, filename="AgentSpoons_Data.xlsx"):
        self.filename = f"outputs/{filename}"
        self.writer = pd.ExcelWriter(self.filename, engine='xlsxwriter')
        self.workbook = self.writer.book
        
        # Define formats
        self.header_format = self.workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'fg_color': '#FF8C00',
            'font_color': '#FFFFFF',
            'border': 1
        })
        
        self.number_format = self.workbook.add_format({
            'num_format': '#,##0.00',
            'border': 1
        })
        
        self.percent_format = self.workbook.add_format({
            'num_format': '0.00%',
            'border': 1
        })
        
        self.date_format = self.workbook.add_format({
            'num_format': 'yyyy-mm-dd hh:mm:ss',
            'border': 1
        })
    
    def create_summary_sheet(self):
        """Executive summary sheet"""
        
        # Create data
        summary_data = {
            'Metric': [
                'Report Date',
                'Asset Pair',
                'Current Price',
                'Price Change (24h)',
                'Realized Volatility',
                'Implied Volatility',
                'IV-RV Spread',
                'GARCH Forecast',
                'VaR (95%)',
                'Data Points',
                'Forecast Accuracy'
            ],
            'Value': [
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'NEO/USDT',
                15.23,
                0.024,
                0.523,
                0.581,
                0.058,
                0.547,
                -0.034,
                720,
                0.873
            ]
        }
        
        df = pd.DataFrame(summary_data)
        
        # Write to Excel
        df.to_excel(self.writer, sheet_name='Summary', index=False, startrow=1)
        
        worksheet = self.writer.sheets['Summary']
        
        # Add title
        worksheet.write('A1', 'AGENTSPOONS VOLATILITY REPORT', self.header_format)
        worksheet.merge_range('A1:B1', 'AGENTSPOONS VOLATILITY REPORT', self.header_format)
        
        # Format columns
        worksheet.set_column('A:A', 25)
        worksheet.set_column('B:B', 20)
        
        # Apply formats
        for row in range(2, len(df) + 2):
            worksheet.write(f'A{row+1}', df.iloc[row-2]['Metric'], self.header_format)
            
            value = df.iloc[row-2]['Value']
            if isinstance(value, float) and value < 1 and value > -1:
                worksheet.write(f'B{row+1}', value, self.percent_format)
            elif isinstance(value, (int, float)):
                worksheet.write(f'B{row+1}', value, self.number_format)
    
    def create_timeseries_sheet(self):
        """Time series data sheet"""
        
        # Generate sample data
        dates = pd.date_range(end=datetime.now(), periods=720, freq='H')
        
        data = {
            'Timestamp': dates,
            'Price': [15 + np.sin(i/10) + np.random.normal(0, 0.1) for i in range(720)],
            'Realized_Vol': [0.5 + np.random.normal(0, 0.02) for _ in range(720)],
            'Implied_Vol': [0.55 + np.random.normal(0, 0.02) for _ in range(720)],
            'GARCH_Forecast': [0.52 + np.random.normal(0, 0.01) for _ in range(720)],
            'Spread': [0.05 + np.random.normal(0, 0.01) for _ in range(720)]
        }
        
        df = pd.DataFrame(data)
        
        # Write to Excel
        df.to_excel(self.writer, sheet_name='Time Series', index=False)
        
        worksheet = self.writer.sheets['Time Series']
        
        # Format columns
        worksheet.set_column('A:A', 20)
        worksheet.set_column('B:F', 15)
        
        # Apply formats
        for col_num, col_name in enumerate(df.columns):
            worksheet.write(0, col_num, col_name, self.header_format)
        
        for row in range(len(df)):
            worksheet.write(row + 1, 0, df.iloc[row]['Timestamp'], self.date_format)
            for col in range(1, len(df.columns)):
                worksheet.write(row + 1, col, df.iloc[row, col], 
                              self.percent_format if 'Vol' in df.columns[col] or 'Spread' in df.columns[col] else self.number_format)
        
        # Add chart
        chart = self.workbook.add_chart({'type': 'line'})
        
        chart.add_series({
            'name': 'Realized Vol',
            'categories': f'=\'Time Series\'!$A$2:$A${len(df)+1}',
            'values': f'=\'Time Series\'!$C$2:$C${len(df)+1}',
            'line': {'color': '#00FF00', 'width': 2}
        })
        
        chart.add_series({
            'name': 'Implied Vol',
            'categories': f'=\'Time Series\'!$A$2:$A${len(df)+1}',
            'values': f'=\'Time Series\'!$D$2:$D${len(df)+1}',
            'line': {'color': '#FF8C00', 'width': 2}
        })
        
        chart.set_title({'name': 'Volatility Over Time'})
        chart.set_x_axis({'name': 'Date'})
        chart.set_y_axis({'name': 'Volatility %', 'num_format': '0.00%'})
        chart.set_size({'width': 720, 'height': 400})
        
        worksheet.insert_chart('H2', chart)
    
    def create_statistics_sheet(self):
        """Statistical analysis sheet"""
        
        stats_data = {
            'Statistic': ['Mean', 'Median', 'Std Dev', 'Min', 'Max', 'Skewness', 'Kurtosis'],
            'Price': [15.23, 15.20, 0.45, 14.50, 16.10, 0.12, 2.95],
            'Realized Vol': [0.523, 0.520, 0.025, 0.480, 0.580, 0.15, 3.10],
            'Implied Vol': [0.581, 0.575, 0.030, 0.520, 0.650, 0.20, 3.25]
        }
        
        df = pd.DataFrame(stats_data)
        
        df.to_excel(self.writer, sheet_name='Statistics', index=False)
        
        worksheet = self.writer.sheets['Statistics']
        
        # Format
        worksheet.set_column('A:A', 15)
        worksheet.set_column('B:D', 15)
        
        for col_num in range(len(df.columns)):
            worksheet.write(0, col_num, df.columns[col_num], self.header_format)
        
        for row in range(len(df)):
            worksheet.write(row + 1, 0, df.iloc[row]['Statistic'])
            for col in range(1, len(df.columns)):
                worksheet.write(row + 1, col, df.iloc[row, col], 
                              self.percent_format if 'Vol' in df.columns[col] else self.number_format)
    
    def create_greeks_sheet(self):
        """Options Greeks sheet"""
        
        strikes = range(90, 111, 2)
        
        data = {
            'Strike': list(strikes),
            'Call_Price': [max(0, 15.23 - s) + np.random.uniform(0, 2) for s in strikes],
            'Put_Price': [max(0, s - 15.23) + np.random.uniform(0, 2) for s in strikes],
            'Delta': [0.5 + (15.23 - s)/20 for s in strikes],
            'Gamma': [0.02 + np.random.uniform(-0.005, 0.005) for _ in strikes],
            'Vega': [0.15 + np.random.uniform(-0.02, 0.02) for _ in strikes],
            'Theta': [-0.08 + np.random.uniform(-0.02, 0.02) for _ in strikes]
        }
        
        df = pd.DataFrame(data)
        
        df.to_excel(self.writer, sheet_name='Greeks', index=False)
        
        worksheet = self.writer.sheets['Greeks']
        
        # Format
        for col in 'ABCDEFG':
            worksheet.set_column(f'{col}:{col}', 12)
        
        for col_num in range(len(df.columns)):
            worksheet.write(0, col_num, df.columns[col_num], self.header_format)
    
    def generate(self):
        """Generate complete Excel file"""
        
        print("📊 Generating Excel report...")
        
        self.create_summary_sheet()
        self.create_timeseries_sheet()
        self.create_statistics_sheet()
        self.create_greeks_sheet()
        
        self.writer.close()
        
        print(f"✅ Excel report generated: {self.filename}")
        return self.filename

if __name__ == "__main__":
    exporter = ProfessionalExcelExport()
    exporter.generate()
