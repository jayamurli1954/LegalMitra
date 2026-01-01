@echo off
REM LegalMitra - One-Click Startup Script
REM This script sets up and starts the LegalMitra application

title LegalMitra - AI Legal Assistant
color 0A

REM Prevent window from closing on error
setlocal enabledelayedexpansion

echo ========================================
echo    LegalMitra - AI Legal Assistant
echo    One-Click Startup Script
echo ========================================
echo.

REM Get the script directory
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

REM Check Python installation
echo [1/6] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python 3.8+ from https://www.python.org/
    echo.
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] Python found: %PYTHON_VERSION%

REM Check pip
echo [2/6] Checking pip...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip is not available!
    pause
    exit /b 1
)
echo [OK] pip found

REM Create virtual environment if it doesn't exist
echo [3/6] Setting up virtual environment...
set "VENV_PATH=%SCRIPT_DIR%..\backend\venv"
if not exist "%VENV_PATH%" (
    echo Creating virtual environment...
    python -m venv "%VENV_PATH%"
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment!
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment already exists
)

REM Activate virtual environment
echo Activating virtual environment...
call "%VENV_PATH%\Scripts\activate.bat"
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment!
    pause
    exit /b 1
)
echo [OK] Virtual environment activated

REM Install/upgrade dependencies
echo [4/6] Installing dependencies...
set "REQUIREMENTS_PATH=%SCRIPT_DIR%..\backend\requirements.txt"
if exist "%REQUIREMENTS_PATH%" (
    echo Installing packages (this may take a few minutes)...
    python -m pip install --upgrade pip -q
    python -m pip install -r "%REQUIREMENTS_PATH%"
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies!
        echo Try running manually: pip install -r backend\requirements.txt
        pause
        exit /b 1
    )
    echo [OK] Dependencies installed
) else (
    echo WARNING: requirements.txt not found!
)

REM Check .env file
echo [5/6] Checking configuration...
set "ENV_PATH=%SCRIPT_DIR%..\backend\.env"
set "ENV_EXAMPLE_PATH=%SCRIPT_DIR%..\backend\.env.example"
if not exist "%ENV_PATH%" (
    if exist "%ENV_EXAMPLE_PATH%" (
        echo Creating .env file from template...
        copy "%ENV_EXAMPLE_PATH%" "%ENV_PATH%" >nul
        echo.
        echo IMPORTANT: Please edit backend\.env and add your API keys!
        echo   - OPENAI_API_KEY or ANTHROPIC_API_KEY is required
        echo.
        echo Opening .env file for editing in 3 seconds...
        timeout /t 3 /nobreak >nul
        notepad "%ENV_PATH%"
        echo.
        echo Press Enter after adding your API keys...
        pause >nul
    ) else (
        echo Creating basic .env file...
        (
            echo # LegalMitra Configuration
            echo AI_PROVIDER=openai
            echo OPENAI_API_KEY=your_api_key_here
            echo PORT=8888
        ) > "%ENV_PATH%"
        echo IMPORTANT: Please edit backend\.env and add your API key!
        notepad "%ENV_PATH%"
        pause
    )
) else (
    echo [OK] Configuration file exists
)

REM Start the backend server
echo [6/6] Starting LegalMitra Backend...
echo.
echo ========================================
echo    Starting Server...
echo ========================================
echo.
echo Backend API will be available at: http://localhost:8888
echo API Documentation: http://localhost:8888/docs
echo Frontend: Open frontend\index.html in your browser
echo.
echo Press Ctrl+C to stop the server
echo.

REM Change to backend directory
cd /d "%SCRIPT_DIR%..\backend"

REM Start the server
python -m app.main

REM If we get here, server stopped
echo.
echo Server stopped.
pause

