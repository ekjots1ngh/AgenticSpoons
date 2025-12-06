# Test runner script for Windows PowerShell

Write-Host "================================================================================"
Write-Host "🧪 RUNNING COMPREHENSIVE TEST SUITE"
Write-Host "================================================================================"

# Unit tests
Write-Host "`n1️⃣  Unit Tests"
pytest tests/ -m "not slow" -v

# Integration tests
Write-Host "`n2️⃣  Integration Tests"
pytest tests/ -m integration -v

# Coverage report
Write-Host "`n3️⃣  Coverage Report"
pytest tests/ --cov=src --cov-report=term-missing

# Generate HTML report
pytest tests/ --cov=src --cov-report=html

Write-Host "`n✅ Tests complete! Coverage report: htmlcov/index.html"
