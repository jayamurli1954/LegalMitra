# LegalMitra - One-Click Startup Script
# This script sets up and starts the LegalMitra application

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   LegalMitra - AI Legal Assistant" -ForegroundColor Cyan
Write-Host "   One-Click Startup Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Get the script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

# Check Python installation
Write-Host "[1/6] Checking Python installation..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Python is not installed or not in PATH!" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ from https://www.python.org/" -ForegroundColor Red
    Write-Host ""
    Write-Host "Press any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}
Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green

# Check pip
Write-Host "[2/6] Checking pip..." -ForegroundColor Yellow
$pipVersion = python -m pip --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: pip is not available!" -ForegroundColor Red
    exit 1
}
Write-Host "✓ pip found" -ForegroundColor Green

# Create virtual environment if it doesn't exist
Write-Host "[3/6] Setting up virtual environment..." -ForegroundColor Yellow
$venvPath = Join-Path $ScriptDir "backend" "venv"
if (-not (Test-Path $venvPath)) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv $venvPath
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to create virtual environment!" -ForegroundColor Red
        exit 1
    }
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "✓ Virtual environment already exists" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
$activateScript = Join-Path $venvPath "Scripts" "Activate.ps1"
if (Test-Path $activateScript) {
    & $activateScript
    Write-Host "✓ Virtual environment activated" -ForegroundColor Green
} else {
    Write-Host "ERROR: Activation script not found!" -ForegroundColor Red
    exit 1
}

# Install/upgrade dependencies
Write-Host "[4/6] Installing dependencies..." -ForegroundColor Yellow
$requirementsPath = Join-Path $ScriptDir "backend" "requirements.txt"
if (Test-Path $requirementsPath) {
    Write-Host "Installing packages (this may take a few minutes)..." -ForegroundColor Yellow
    python -m pip install --upgrade pip -q
    python -m pip install -r $requirementsPath
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to install dependencies!" -ForegroundColor Red
        Write-Host "Try running manually: pip install -r backend\requirements.txt" -ForegroundColor Yellow
        exit 1
    }
    Write-Host "✓ Dependencies installed" -ForegroundColor Green
} else {
    Write-Host "WARNING: requirements.txt not found!" -ForegroundColor Yellow
}

# Check .env file
Write-Host "[5/6] Checking configuration..." -ForegroundColor Yellow
$envPath = Join-Path $ScriptDir "backend" ".env"
$envExamplePath = Join-Path $ScriptDir "backend" ".env.example"
if (-not (Test-Path $envPath)) {
    if (Test-Path $envExamplePath) {
        Write-Host "Creating .env file from template..." -ForegroundColor Yellow
        Copy-Item $envExamplePath $envPath
        Write-Host "⚠ IMPORTANT: Please edit backend\.env and add your API keys!" -ForegroundColor Yellow
        Write-Host "  - OPENAI_API_KEY or ANTHROPIC_API_KEY is required" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Opening .env file for editing in 3 seconds..." -ForegroundColor Yellow
        Start-Sleep -Seconds 3
        notepad $envPath
        Write-Host "Press Enter after adding your API keys..." -ForegroundColor Yellow
        Read-Host
    } else {
        Write-Host "WARNING: .env.example not found. Creating basic .env file..." -ForegroundColor Yellow
        @" 
# LegalMitra Configuration
AI_PROVIDER=anthropic
ANTHROPIC_API_KEY=your_anthropic_key_here
GOOGLE_GEMINI_API_KEY=your_gemini_key_here
GROK_API_KEY=your_grok_key_here
PORT=8888
"@ | Out-File -FilePath $envPath -Encoding utf8
        Write-Host "⚠ Please edit backend\.env and add your API key!" -ForegroundColor Yellow
    }
} else {
    Write-Host "✓ Configuration file exists" -ForegroundColor Green
}

# Check if API key is set
$envContent = Get-Content $envPath -Raw
if ($envContent -match "your.*api.*key" -or $envContent -notmatch "API_KEY") {
    Write-Host "⚠ WARNING: API key may not be configured properly!" -ForegroundColor Yellow
    Write-Host "  Please ensure OPENAI_API_KEY or ANTHROPIC_API_KEY is set in backend\.env" -ForegroundColor Yellow
    Write-Host ""
}

# Start the backend server
Write-Host "[6/6] Starting LegalMitra Backend..." -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Starting Server..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
# Read port from .env or use default
$envFile = Join-Path $ScriptDir "backend" ".env"
$port = 8888
if (Test-Path $envFile) {
    $envContent = Get-Content $envFile
    $portLine = $envContent | Where-Object { $_ -match "^PORT=" }
    if ($portLine) {
        $port = ($portLine -split "=")[1].Trim()
    }
}

Write-Host "Backend API will be available at: http://localhost:$port" -ForegroundColor Green
Write-Host "API Documentation: http://localhost:$port/docs" -ForegroundColor Green
Write-Host "Frontend: Open frontend\index.html in your browser" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Change to backend directory
Set-Location (Join-Path $ScriptDir "backend")

# Start the server
try {
    python -m app.main
} catch {
    Write-Host ""
    Write-Host "ERROR: Failed to start server!" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
    Write-Host "Press any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

