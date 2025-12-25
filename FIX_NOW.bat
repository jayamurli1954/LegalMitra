@echo off
REM Quick fix script for API key errors

title LegalMitra - Fix API Key Error

echo ========================================
echo    Fixing API Key Configuration
echo ========================================
echo.

cd /d "%~dp0\backend"

if not exist ".env" (
    echo ERROR: .env file not found!
    echo Creating new .env file...
    call ..\QUICK_ADD_KEYS.bat
    exit /b 1
)

echo Opening .env file for editing...
echo.
echo ========================================
echo    INSTRUCTIONS:
echo ========================================
echo.
echo 1. Find lines with "your_api_key_here" or "your_grok_key_here"
echo 2. Replace with your ACTUAL API keys
echo 3. Make sure AI_PROVIDER=grok (if using Grok)
echo 4. Save the file (Ctrl+S)
echo 5. Restart the server
echo.
echo ========================================
echo.

timeout /t 3 /nobreak >nul
notepad .env

echo.
echo ========================================
echo    After Saving:
echo ========================================
echo.
echo 1. Stop the server (Ctrl+C)
echo 2. Run START_LEGALMITRA.vbs again
echo.
echo ========================================
echo.
pause










