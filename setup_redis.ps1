# Setup Redis on Windows
Write-Host "Setting up Redis on Windows..." -ForegroundColor Cyan

# Check if Redis is installed via Chocolatey
if (Get-Command redis-server -ErrorAction SilentlyContinue) {
    Write-Host "✅ Redis already installed" -ForegroundColor Green
} else {
    Write-Host "Redis not found. Installing via Chocolatey..." -ForegroundColor Yellow
    
    # Check if Chocolatey is installed
    if (Get-Command choco -ErrorAction SilentlyContinue) {
        choco install redis-64 -y
    } else {
        Write-Host "❌ Chocolatey not found. Please install Redis manually:" -ForegroundColor Red
        Write-Host "   1. Download from: https://github.com/microsoftarchive/redis/releases" -ForegroundColor Yellow
        Write-Host "   2. Or use WSL: wsl sudo apt-get install redis-server" -ForegroundColor Yellow
        Write-Host "   3. Or use Docker: docker run -d -p 6379:6379 redis" -ForegroundColor Yellow
        exit 1
    }
}

# Start Redis server
Write-Host "Starting Redis server..." -ForegroundColor Cyan

# Try Docker first (most common on Windows)
if (Get-Command docker -ErrorAction SilentlyContinue) {
    $redisContainer = docker ps -a --filter "name=agentspoons-redis" --format "{{.Names}}"
    
    if ($redisContainer -eq "agentspoons-redis") {
        Write-Host "Redis container exists. Starting..." -ForegroundColor Yellow
        docker start agentspoons-redis | Out-Null
    } else {
        Write-Host "Creating new Redis container..." -ForegroundColor Yellow
        docker run -d --name agentspoons-redis -p 6379:6379 redis:latest | Out-Null
    }
    
    Write-Host "✅ Redis running on localhost:6379 (Docker)" -ForegroundColor Green
} elseif (Get-Command redis-server -ErrorAction SilentlyContinue) {
    Start-Process -FilePath "redis-server" -WindowStyle Hidden
    Write-Host "✅ Redis running on localhost:6379" -ForegroundColor Green
} else {
    Write-Host "⚠️  Redis not running. Install Docker or Redis manually." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Test Redis connection:" -ForegroundColor Cyan
Write-Host "  python -c `"import redis; r = redis.Redis(); print('Connected:', r.ping())`"" -ForegroundColor White
