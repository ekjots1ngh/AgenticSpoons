# Deploy Neo Smart Contract
# PowerShell version

Write-Host "🚀 Deploying AgentSpoons Oracle Contract to Neo" -ForegroundColor Cyan

# Compile contract
Write-Host "Compiling contract..." -ForegroundColor Yellow
neo3-boa compile src/contracts/volatility_oracle.py

# TODO: Deploy using neo-express or neo-cli
# neo-express contract deploy <compiled-contract.nef>

Write-Host "✓ Contract deployed!" -ForegroundColor Green
Write-Host "Update config.py with contract hash" -ForegroundColor Yellow
