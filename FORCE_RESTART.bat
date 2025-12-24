@echo off
REM Force restart script - ensures clean restart

title LegalMitra - Force Restart

echo ========================================
echo    Force Restart LegalMitra
echo ========================================
echo.

cd /d "%~dp0"

echo Step 1: Checking for running server processes...
tasklist /FI "IMAGENAME eq python.exe" /FI "WINDOWTITLE eq LegalMitra*" 2>nul | find /I "python.exe" >nul
if %errorlevel% == 0 (
    echo Found running server. Stopping...
    taskkill /FI "WINDOWTITLE eq LegalMitra*" /F >nul 2>&1
    timeout /t 2 /nobreak >nul
)

echo.
echo Step 2: Verifying .env file...
cd backend
if exist ".env" (
    echo [OK] .env file exists
    echo.
    echo Current GROK_API_KEY value:
    for /f "tokens=2 delims==" %%a in ('findstr /C:"GROK_API_KEY" .env') do (
        set "key=%%a"
        setlocal enabledelayedexpansion
        if "!key!"=="" (
            echo [ERROR] GROK_API_KEY is EMPTY!
        ) else if "!key:~0,4!"=="xai-" (
            echo [OK] Key format correct: !key:~0,30!...
        ) else (
            echo [WARNING] Key format might be incorrect: !key!
        )
        endlocal
    )
) else (
    echo [ERROR] .env file not found!
    pause
    exit /b 1
)

echo.
echo Step 3: Checking for placeholder text...
findstr /C:"your_api" /C:"your_key" /C:"your_grok" .env >nul 2>&1
if %errorlevel% == 0 (
    echo [ERROR] Found placeholder text in .env!
    echo.
    echo Lines with placeholders:
    findstr /C:"your_api" /C:"your_key" /C:"your_grok" .env
    echo.
    echo Please fix these before restarting!
    pause
    exit /b 1
) else (
    echo [OK] No placeholder text found
)

echo.
echo Step 4: Starting server...
echo.
cd ..

REM Clear any environment variable overrides
set OPENAI_API_KEY=
set GROK_API_KEY=
set ANTHROPIC_API_KEY=

echo ========================================
echo    Starting LegalMitra...
echo ========================================
echo.

call START_LEGALMITRA.vbs









