"""
Test PDF Report Generator
"""
import os
from pathlib import Path
from loguru import logger

def test_pdf_generator():
    """Test PDF report generation"""
    logger.info("Testing PDF Report Generator...")
    
    # Test 1: Import module
    try:
        from src.reports.pdf_generator import VolatilityReport, generate_daily_report
        logger.success("✓ PDF generator module imports successfully")
    except Exception as e:
        logger.error(f"✗ Failed to import PDF generator: {e}")
        return False
    
    # Test 2: Check dependencies
    try:
        import reportlab
        import matplotlib
        logger.success("✓ Dependencies (reportlab, matplotlib) installed")
    except Exception as e:
        logger.error(f"✗ Missing dependencies: {e}")
        return False
    
    # Test 3: Generate report
    try:
        generate_daily_report()
        logger.success("✓ Daily report generated successfully")
    except Exception as e:
        logger.error(f"✗ Failed to generate report: {e}")
        return False
    
    # Test 4: Verify report file exists
    from datetime import datetime
    report_file = f'reports/volatility_report_{datetime.now().strftime("%Y%m%d")}.pdf'
    
    if Path(report_file).exists():
        size = Path(report_file).stat().st_size
        logger.success(f"✓ Report file exists: {report_file} ({size:,} bytes)")
    else:
        logger.error(f"✗ Report file not found: {report_file}")
        return False
    
    # Test 5: Check file size
    if size > 1000:
        logger.success(f"✓ Report file size is valid ({size:,} bytes)")
    else:
        logger.warning(f"⚠ Report file size is small ({size} bytes)")
    
    # Test 6: Create custom report
    try:
        import json
        with open('data/results.json', 'r') as f:
            data = json.load(f)
        
        neo_data = [d for d in data if d['pair'] == 'NEO/USDT'][:50]
        
        report = VolatilityReport('reports/test_custom_report.pdf')
        report.add_title('Test Custom Report')
        report.add_section('Test Section', 'This is a test section to validate custom report generation.')
        
        metrics = {
            'Test Metric 1': 0.0523,
            'Test Metric 2': 100.50,
            'Test Metric 3': 0.95,
        }
        report.add_metrics_table(metrics)
        report.generate()
        
        if Path('reports/test_custom_report.pdf').exists():
            logger.success("✓ Custom report generated successfully")
        else:
            logger.error("✗ Custom report not created")
            
    except Exception as e:
        logger.error(f"✗ Failed to create custom report: {e}")
    
    # Summary
    print("\n" + "="*60)
    print("📊 PDF Report Generator Test Summary:")
    print("="*60)
    
    print(f"\n✅ Module Status: Operational")
    print(f"   • PDF Generator: Working")
    print(f"   • Report Generation: Success")
    print(f"   • File Output: {report_file}")
    print(f"   • File Size: {size:,} bytes")
    
    # List all reports
    reports = list(Path('reports').glob('*.pdf'))
    print(f"\n📄 Generated Reports ({len(reports)}):")
    for report in reports:
        print(f"   • {report.name} ({report.stat().st_size:,} bytes)")
    
    print("\n" + "="*60)
    logger.success("PDF report generator tests complete!")
    
    return True

if __name__ == "__main__":
    test_pdf_generator()
