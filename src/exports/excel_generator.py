"""
Professional Excel Export with Charts
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import xlsxwriter


class ExcelReportGenerator:
    """Generate professional Excel reports"""

    def __init__(self):
        self.output_dir = Path('outputs')
        self.output_dir.mkdir(exist_ok=True)

    def generate(self, data):
        """Generate Excel report"""

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = self.output_dir / f'AgentSpoons_Data_{timestamp}.xlsx'

        # Create workbook
        workbook = xlsxwriter.Workbook(str(filename))

        # Formats
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#2563eb',
            'font_color': 'white',
            'align': 'center',
            'valign': 'vcenter',
            'border': 1
        })

        number_format = workbook.add_format({
            'num_format': '#,##0.00',
            'border': 1
        })

        percent_format = workbook.add_format({
            'num_format': '0.00%',
            'border': 1
        })

        # Summary Sheet
        summary = workbook.add_worksheet('Summary')
        summary.set_column('A:A', 25)
        summary.set_column('B:B', 20)

        summary.write('A1', 'AGENTSPOONS VOLATILITY REPORT', header_format)
        summary.merge_range('A1:B1', 'AGENTSPOONS VOLATILITY REPORT', header_format)

        summary_data = [
            ['Report Date', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            ['Asset Pair', 'NEO/USDT'],
            ['Current Price', data.get('price', 15.23)],
            ['Price Change (24h)', data.get('price_change', 0) / 100],
            ['Realized Volatility', data.get('realized_vol', 0.52)],
            ['Implied Volatility', data.get('implied_vol', 0.58)],
            ['IV-RV Spread', data.get('spread', 0.06)],
            ['GARCH Forecast', data.get('garch_forecast', 0.54)],
        ]

        row = 2
        for metric, value in summary_data:
            summary.write(row, 0, metric, header_format)
            if isinstance(value, (int, float)) and abs(value) < 1:
                summary.write(row, 1, value, percent_format)
            elif isinstance(value, (int, float)):
                summary.write(row, 1, value, number_format)
            else:
                summary.write(row, 1, value)
            row += 1

        # Time Series Sheet
        timeseries = workbook.add_worksheet('Time Series')

        history = data.get('history', {})
        if history.get('rv'):
            df_data = {
                'Timestamp': [datetime.now() - timedelta(minutes=2 * i) for i in range(len(history['rv']) - 1, -1, -1)],
                'Price': history.get('prices', [15.23] * len(history['rv'])),
                'Realized_Vol': history['rv'],
                'Implied_Vol': history['iv']
            }

            df = pd.DataFrame(df_data)

            # Write headers
            for col_num, col_name in enumerate(df.columns):
                timeseries.write(0, col_num, col_name, header_format)

            # Write data
            for row_num, row_data in df.iterrows():
                timeseries.write(row_num + 1, 0, row_data['Timestamp'].strftime('%Y-%m-%d %H:%M:%S'))
                timeseries.write(row_num + 1, 1, row_data['Price'], number_format)
                timeseries.write(row_num + 1, 2, row_data['Realized_Vol'], percent_format)
                timeseries.write(row_num + 1, 3, row_data['Implied_Vol'], percent_format)

            timeseries.set_column('A:A', 20)
            timeseries.set_column('B:D', 15)

            # Add chart
            chart = workbook.add_chart({'type': 'line'})

            chart.add_series({
                'name': 'Realized Vol',
                'categories': f"='Time Series'!$A$2:$A${len(df) + 1}",
                'values': f"='Time Series'!$C$2:$C${len(df) + 1}",
                'line': {'color': '#10b981', 'width': 2}
            })

            chart.add_series({
                'name': 'Implied Vol',
                'categories': f"='Time Series'!$A$2:$A${len(df) + 1}",
                'values': f"='Time Series'!$D$2:$D${len(df) + 1}",
                'line': {'color': '#f59e0b', 'width': 2}
            })

            chart.set_title({'name': 'Volatility Over Time'})
            chart.set_x_axis({'name': 'Time'})
            chart.set_y_axis({'name': 'Volatility', 'num_format': '0.00%'})
            chart.set_size({'width': 720, 'height': 400})

            timeseries.insert_chart('F2', chart)

        # Statistics Sheet
        stats = workbook.add_worksheet('Statistics')

        if history.get('rv'):
            rv_array = np.array(history['rv'])
            iv_array = np.array(history['iv'])

            stats_rows = (
                ['Statistic', 'Realized Vol', 'Implied Vol'],
                ['Mean', float(np.mean(rv_array)), float(np.mean(iv_array))],
                ['Median', float(np.median(rv_array)), float(np.median(iv_array))],
                ['Std Dev', float(np.std(rv_array)), float(np.std(iv_array))],
                ['Min', float(np.min(rv_array)), float(np.min(iv_array))],
                ['Max', float(np.max(rv_array)), float(np.max(iv_array))],
                ['25th Percentile', float(np.percentile(rv_array, 25)), float(np.percentile(iv_array, 25))],
                ['75th Percentile', float(np.percentile(rv_array, 75)), float(np.percentile(iv_array, 75))],
            )

            for row_idx, row_values in enumerate(stats_rows):
                for col_idx, cell_value in enumerate(row_values):
                    if row_idx == 0 or col_idx == 0:
                        stats.write(row_idx, col_idx, cell_value, header_format)
                    else:
                        stats.write(row_idx, col_idx, cell_value, percent_format)

            stats.set_column('A:A', 20)
            stats.set_column('B:C', 15)

        workbook.close()

        print(f"✅ Excel generated: {filename}")
        return filename


if __name__ == "__main__":
    # Test
    generator = ExcelReportGenerator()

    test_data = {
        'price': 15.23,
        'price_change': 2.4,
        'realized_vol': 0.52,
        'implied_vol': 0.58,
        'spread': 0.06,
        'garch_forecast': 0.54,
        'history': {
            'prices': [15 + np.random.normal(0, 0.5) for _ in range(50)],
            'rv': [0.50 + np.random.normal(0, 0.02) for _ in range(50)],
            'iv': [0.56 + np.random.normal(0, 0.02) for _ in range(50)]
        }
    }

    generator.generate(test_data)
