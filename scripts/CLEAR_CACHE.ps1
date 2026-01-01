# PowerShell script to clear Python cache
Write-Host "Clearing Python cache..." -ForegroundColor Yellow

# Remove __pycache__ directories
Get-ChildItem -Path . -Recurse -Directory -Filter __pycache__ | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

# Remove .pyc files
Get-ChildItem -Path . -Recurse -Filter *.pyc | Remove-Item -Force -ErrorAction SilentlyContinue

Write-Host "Cache cleared!" -ForegroundColor Green



