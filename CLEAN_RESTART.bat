@echo off
REM Clean restart - ensures fresh start

title LegalMitra - Clean Restart

echo ========================================
echo    Clean Restart LegalMitra
echo ========================================
echo.

cd /d "%~dp0"

echo [1/4] Stopping any running servers...
taskkill /FI "WINDOWTITLE eq LegalMitra*" /F >nul 2>&1
taskkill /FI "IMAGENAME eq python.exe" /FI "WINDOWTITLE eq LegalMitra*" /F >nul 2>&1
timeout /t 2 /nobreak >nul

echo [2/4] Verifying .env file...
cd backend
if not exist ".env" (
    echo ERROR: .env file not found!
    pause
    exit /b 1
)

echo [OK] .env file exists
echo.

echo [3/4] Checking GROK_API_KEY...
for /f "tokens=2 delims==" %%a in ('findstr /C:"GROK_API_KEY" .env') do (
    set "key=%%a"
    setlocal enabledelayedexpansion
    if "!key!"=="" (
        echo [ERROR] GROK_API_KEY is EMPTY!
        pause
        exit /b 1
    )
    if "!key:~0,4!"=="xai-" (
        echo [OK] Grok key format correct
        echo Key preview: !key:~0,15!...
    ) else (
        echo [ERROR] Grok key format incorrect - should start with "xai-"
        pause
        exit /b 1
    )
    endlocal
)

echo.
echo [4/4] Starting server with fresh environment...
echo.
cd ..

REM Clear any environment variable overrides that might interfere
set OPENAI_API_KEY=
set GROK_API_KEY=
set ANTHROPIC_API_KEY=
set GOOGLE_GEMINI_API_KEY=

echo ========================================
echo    Starting LegalMitra...
echo ========================================
echo.
echo Server will read from backend\.env file
echo Make sure your API keys are correct!
echo.
timeout /t 2 /nobreak >nul

call START_LEGALMITRA.vbs









