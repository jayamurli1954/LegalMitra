@echo off
title LegalMitra - AI Legal Assistant
color 0A

echo ========================================
echo    LegalMitra - AI Legal Assistant
echo    Starting...
echo ========================================
echo.

REM Get the script directory
cd /d "%~dp0"

REM Change to backend directory
cd ..\backend

REM Check if virtual environment exists, if not create it
if not exist "venv\Scripts\activate.bat" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo.
        echo ERROR: Failed to create virtual environment!
        echo Make sure Python is installed and in your PATH.
        echo.
        pause
        exit /b 1
    )
)

REM Activate virtual environment
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo.
    echo ERROR: Failed to activate virtual environment!
    echo.
    pause
    exit /b 1
)

REM Install/upgrade dependencies
echo Installing dependencies...
python -m pip install --upgrade pip -q
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo WARNING: Some dependencies failed to install!
    echo Continuing anyway...
    echo.
)

REM Check if .env exists, if not create basic one
if not exist ".env" (
    echo.
    echo Creating .env file...
        (
            echo # LegalMitra Configuration
            echo AI_PROVIDER=anthropic
            echo ANTHROPIC_API_KEY=your_anthropic_key_here
            echo GOOGLE_GEMINI_API_KEY=your_gemini_key_here
            echo GROK_API_KEY=your_grok_key_here
            echo PORT=8888
        ) > .env
    echo.
    echo IMPORTANT: Please edit backend\.env and add your API key!
    echo Opening .env file now...
    timeout /t 2 /nobreak >nul
    notepad .env
    echo.
    echo Press Enter to continue after adding your API key...
    pause >nul
)

echo.
echo ========================================
echo    Clearing Python Cache...
echo ========================================
REM Clear Python cache to ensure fresh code load
if exist __pycache__ rmdir /s /q __pycache__ 2>nul
for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d" 2>nul
for /r . %%f in (*.pyc) do @if exist "%%f" del /f /q "%%f" 2>nul
echo Cache cleared!
echo.

echo ========================================
echo    Starting Server...
echo ========================================
echo.
echo [SUCCESS] Application startup complete!
echo.
echo ========================================
echo    NEXT STEPS:
echo ========================================
echo.
echo 1. Frontend (Easiest):
echo    - Open: frontend\index.html in your browser
echo    - Or navigate to: %CD%\..\frontend\index.html
echo.
echo 2. API Documentation:
echo    - Open: http://localhost:8888/docs
echo.
echo 3. Backend API:
echo    - Base URL: http://localhost:8888/api/v1
echo.
echo ========================================
echo.
echo Server is running... Press Ctrl+C to stop
echo.
echo Opening frontend in browser in 3 seconds...
timeout /t 3 /nobreak >nul
REM Get the script directory (project root) and construct absolute path
set "SCRIPT_DIR=%~dp0"
set "FRONTEND_PATH=%SCRIPT_DIR%..\frontend\index.html"
REM Check if index.html exists, if not try index_new.html
if not exist "%FRONTEND_PATH%" (
    set "FRONTEND_PATH=%SCRIPT_DIR%..\frontend\index_new.html"
)
if exist "%FRONTEND_PATH%" (
    REM Use default browser instead of system default handler
    start "" "msedge" "%FRONTEND_PATH%" 2>nul || start "" "chrome" "%FRONTEND_PATH%" 2>nul || start "" "%FRONTEND_PATH%"
) else (
    echo WARNING: Frontend file not found at %FRONTEND_PATH%
    echo Please open frontend\index.html or frontend\index_new.html manually
)
echo.

REM Start the server with uvicorn and reload to pick up code changes
python -m uvicorn app.main:app --reload --port 8888

REM If we get here, server stopped
echo.
echo Server stopped.
pause

