# LegalMitra Server Startup Script
Write-Host "========================================" -ForegroundColor Green
Write-Host "   LegalMitra - Starting Server..." -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Change to backend directory
Set-Location -Path "$PSScriptRoot\..\backend"

# Check if virtual environment exists
if (-not (Test-Path "venv\Scripts\activate.ps1")) {
    Write-Host "ERROR: Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please run START_LEGALMITRA_SIMPLE.bat first to create it." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Cyan
& ".\venv\Scripts\Activate.ps1"

# Check if .env exists
if (-not (Test-Path ".env")) {
    Write-Host "WARNING: .env file not found!" -ForegroundColor Yellow
    Write-Host "Server may not work without API keys configured." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Starting server on http://localhost:8888..." -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start the server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8888 --reload


