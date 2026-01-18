@echo off
REM Verify .env file configuration

title LegalMitra - Verify .env Configuration

echo ========================================
echo    Verifying .env File Configuration
echo ========================================
echo.

cd /d "%~dp0\backend"

if not exist ".env" (
    echo ERROR: .env file not found!
    pause
    exit /b 1
)

echo Reading .env file...
echo.

echo ========================================
echo    Current Configuration:
echo ========================================
echo.

REM Show non-comment, non-empty lines
for /f "tokens=*" %%a in ('.env') do (
    set "line=%%a"
    setlocal enabledelayedexpansion
    set "line=!line: =!"
    if not "!line!"=="" (
        if not "!line:~0,1!"=="#" (
            echo !line!
        )
    )
    endlocal
)

echo.
echo ========================================
echo    Verification:
echo ========================================
echo.

REM Check AI_PROVIDER
findstr /C:"AI_PROVIDER=grok" .env >nul 2>&1
if %errorlevel% == 0 (
    echo [OK] AI_PROVIDER is set to grok
) else (
    echo [WARNING] AI_PROVIDER might not be set to grok
    findstr /C:"AI_PROVIDER" .env
)

echo.

REM Check for placeholder text
findstr /C:"your_api" /C:"your_key" /C:"your_gemini" /C:"your_grok" /C:"your_anthropic" /C:"xxxxxxxx" .env >nul 2>&1
if %errorlevel% == 0 (
    echo [WARNING] Found placeholder text or masked keys!
    echo Make sure you're using ACTUAL API keys, not placeholders.
    echo.
    echo Lines with potential issues:
    findstr /C:"your_api" /C:"your_key" /C:"your_gemini" /C:"your_grok" /C:"your_anthropic" /C:"xxxxxxxx" .env
) else (
    echo [OK] No obvious placeholder text found
)

echo.

REM Check GROK_API_KEY exists
findstr /C:"GROK_API_KEY=" .env >nul 2>&1
if %errorlevel% == 0 (
    echo [OK] GROK_API_KEY is defined
    for /f "tokens=2 delims==" %%a in ('findstr /C:"GROK_API_KEY=" .env') do (
        set "key=%%a"
        setlocal enabledelayedexpansion
        if "!key!"=="" (
            echo [ERROR] GROK_API_KEY is empty!
        ) else if "!key!"=="your_grok_key_here" (
            echo [ERROR] GROK_API_KEY still has placeholder text!
        ) else if "!key:~0,4!"=="xai-" (
            echo [OK] GROK_API_KEY format looks correct (starts with xai-)
        ) else (
            echo [WARNING] GROK_API_KEY format might be incorrect
        )
        endlocal
    )
) else (
    echo [ERROR] GROK_API_KEY not found!
)

echo.
echo ========================================
echo    Next Steps:
echo ========================================
echo.
echo 1. Make sure all API keys are ACTUAL keys (not placeholders)
echo 2. Verify keys are active at their respective consoles
echo 3. Save the .env file
echo 4. Restart the server (Stop with Ctrl+C, then START_LEGALMITRA.vbs)
echo.
echo ========================================
echo.

pause










