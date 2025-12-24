@echo off
REM Force fix .env file - removes placeholder text

title LegalMitra - Force Fix .env File

echo ========================================
echo    Force Fixing .env File
echo ========================================
echo.

cd /d "%~dp0\backend"

if not exist ".env" (
    echo Creating new .env file...
    (
        echo # LegalMitra Configuration
        echo AI_PROVIDER=grok
        echo DEFAULT_AI_MODEL=grok-4-latest
        echo.
        echo # Your API Keys - REPLACE WITH ACTUAL KEYS!
        echo ANTHROPIC_API_KEY=
        echo GOOGLE_GEMINI_API_KEY=
        echo GROK_API_KEY=
        echo.
        echo # Server Configuration
        echo PORT=8888
        echo MAX_TOKENS=4000
        echo TEMPERATURE=0.3
    ) > .env
    echo Created .env file!
    echo.
)

echo Checking for placeholder text...
echo.

REM Check if placeholder text exists
findstr /C:"your_api" /C:"your_key" /C:"your_gemini" /C:"your_grok" /C:"your_anthropic" /C:"xxxxxxxx" .env >nul 2>&1

if %errorlevel% == 0 (
    echo ========================================
    echo    FOUND PLACEHOLDER TEXT!
    echo ========================================
    echo.
    echo Your .env file contains placeholder text.
    echo.
    echo Lines with issues:
    findstr /C:"your_api" /C:"your_key" /C:"your_gemini" /C:"your_grok" /C:"your_anthropic" /C:"xxxxxxxx" .env
    echo.
    echo ========================================
    echo    ACTION REQUIRED:
    echo ========================================
    echo.
    echo 1. Open the .env file (will open now)
    echo 2. Find lines with "your_api" or "xxxxxxxx"
    echo 3. Replace with your ACTUAL API keys
    echo 4. Save the file
    echo 5. Restart the server
    echo.
    echo Opening .env file...
    timeout /t 2 /nobreak >nul
    notepad .env
) else (
    echo ========================================
    echo    Checking Current Values:
    echo ========================================
    echo.
    echo AI_PROVIDER:
    findstr /C:"AI_PROVIDER" .env
    echo.
    echo GROK_API_KEY (first 20 chars):
    for /f "tokens=2 delims==" %%a in ('findstr /C:"GROK_API_KEY" .env') do (
        set "key=%%a"
        setlocal enabledelayedexpansion
        if "!key!"=="" (
            echo [ERROR] GROK_API_KEY is EMPTY!
        ) else (
            echo [OK] Key exists: !key:~0,20!...
        )
        endlocal
    )
    echo.
    echo ========================================
    echo.
    echo If keys look correct but still getting errors:
    echo 1. Verify keys are ACTUAL keys (not placeholders)
    echo 2. Check keys are active at provider consoles
    echo 3. Make sure no extra spaces or characters
    echo 4. Restart the server after changes
    echo.
)

echo.
pause









