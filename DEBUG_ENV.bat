@echo off
REM Debug script to see what's actually in .env

title LegalMitra - Debug .env File

echo ========================================
echo    Debugging .env File
echo ========================================
echo.

cd /d "%~dp0\backend"

if not exist ".env" (
    echo ERROR: .env file not found!
    pause
    exit /b 1
)

echo Reading .env file contents:
echo.
echo ========================================
type .env
echo ========================================
echo.

echo Checking specific values:
echo.

for /f "tokens=1,2 delims==" %%a in ('findstr /C:"GROK_API_KEY" .env') do (
    echo Variable: %%a
    echo Value: %%b
    echo Length: 
    set "val=%%b"
    setlocal enabledelayedexpansion
    echo !val! | find /C /V ""
    endlocal
)

echo.
echo Checking for hidden characters or issues...
echo.

REM Check if file has BOM or encoding issues
powershell -Command "Get-Content .env -Raw | ForEach-Object { Write-Host 'File encoding check...'; $_.Length }"

echo.
echo ========================================
echo    Recommendations:
echo ========================================
echo.
echo 1. Make sure GROK_API_KEY has your ACTUAL key (not placeholder)
echo 2. No spaces around = sign
echo 3. No quotes around the key
echo 4. Key should start with "xai-"
echo 5. Key should be long (50+ characters)
echo.
echo ========================================
echo.

pause








