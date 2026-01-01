@echo off
REM Script to check .env file for placeholder text

title LegalMitra - Check .env File

echo ========================================
echo    Checking .env File for Issues
echo ========================================
echo.

cd /d "%~dp0..\backend"

if not exist ".env" (
    echo ERROR: .env file not found!
    echo Creating new .env file...
    call QUICK_ADD_KEYS.bat
    exit /b 1
)

echo Checking for placeholder text...
echo.

findstr /C:"your_api" /C:"your_key" /C:"your_gemini" /C:"your_grok" /C:"your_anthropic" .env >nul 2>&1

if %errorlevel% == 0 (
    echo ========================================
    echo    ISSUES FOUND!
    echo ========================================
    echo.
    echo Your .env file still contains placeholder text!
    echo.
    echo Lines with placeholders:
    findstr /C:"your_api" /C:"your_key" /C:"your_gemini" /C:"your_grok" /C:"your_anthropic" .env
    echo.
    echo ========================================
    echo    FIX:
    echo ========================================
    echo.
    echo 1. Replace "your_api_key_here" with your ACTUAL API key
    echo 2. Replace "your_gemini_key_here" with your ACTUAL Gemini key
    echo 3. Replace "your_grok_key_here" with your ACTUAL Grok key
    echo 4. Replace "your_anthropic_key_here" with your ACTUAL Anthropic key
    echo.
    echo Opening .env file now...
    timeout /t 3 /nobreak >nul
    notepad .env
) else (
    echo ========================================
    echo    LOOKS GOOD!
    echo ========================================
    echo.
    echo No placeholder text found.
    echo Your .env file appears to have actual API keys.
    echo.
    echo Current configuration:
    echo.
    findstr /V "^#" .env | findstr /V "^$"
    echo.
    echo ========================================
    echo.
    echo Checking AI_PROVIDER setting...
    findstr /C:"AI_PROVIDER" .env
    echo.
    echo ========================================
    echo.
    echo IMPORTANT: If using Grok, make sure:
    echo - AI_PROVIDER=grok
    echo - GROK_API_KEY has your actual key (not placeholder)
    echo.
    echo Note: Grok errors may say "OpenAI API error" - this is normal!
    echo Grok uses OpenAI-compatible API format.
    echo.
    echo If you're still getting errors:
    echo 1. Verify keys are correct
    echo 2. Check AI_PROVIDER matches your key
    echo 3. Restart the server
    echo.
)

pause

