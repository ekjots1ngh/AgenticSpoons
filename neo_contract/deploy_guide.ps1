# Neo Contract Deployment Helper
Write-Host "=" -ForegroundColor Cyan
Write-Host "Neo N3 Contract Deployment Guide" -ForegroundColor Cyan
Write-Host "=" -ForegroundColor Cyan

Write-Host "`nYour wallet address: NVLMjeu3Z1feMuN6HEcmLayyM7m5KsJTRX" -ForegroundColor Yellow
Write-Host "Private key (WIF): L3ZFHMjexgsAmPRkYHGpVs58vbwEpdFNXBDDZo7JMMWm7n9XGpbb" -ForegroundColor Yellow

Write-Host "`n OPTION 1: Install neo-mamba (Python)" -ForegroundColor Green
Write-Host "pip install neo-mamba"
Write-Host "neomamba contract deploy --network testnet --wallet-wif L3ZFHMjexgsAmPRkYHGpVs58vbwEpdFNXBDDZo7JMMWm7n9XGpbb --nef neo_contract/simple_oracle.nef"

Write-Host "`n OPTION 2: Use neo-cli" -ForegroundColor Green
Write-Host "1. Download: https://github.com/neo-project/neo-cli/releases"
Write-Host "2. Extract and run neo-cli.exe"
Write-Host "3. Commands:"
Write-Host "   > import key L3ZFHMjexgsAmPRkYHGpVs58vbwEpdFNXBDDZo7JMMWm7n9XGpbb"
Write-Host "   > deploy neo_contract\simple_oracle.nef"
Write-Host "   > deploy neo_contract\volatility_oracle.nef"

Write-Host "`n OPTION 3: Use Neo Express (Local testing)" -ForegroundColor Green
Write-Host "dotnet tool install -g Neo.Express"
Write-Host "neoxp contract deploy neo_contract\simple_oracle.nef"

Write-Host "`n After deployment, SAVE THE CONTRACT HASH!" -ForegroundColor Red
Write-Host "You'll need it to interact with your contract`n"
