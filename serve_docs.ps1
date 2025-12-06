# Documentation server for Windows PowerShell

Write-Host "=========================================="
Write-Host "📚 Starting MkDocs Server"
Write-Host "=========================================="

mkdocs serve -a 0.0.0.0:8001

Write-Host "`n✅ Documentation available at: http://localhost:8001"
