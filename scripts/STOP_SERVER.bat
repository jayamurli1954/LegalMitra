@echo off
REM Stop LegalMitra server

title LegalMitra - Stop Server

echo ========================================
echo    Stopping LegalMitra Server
echo ========================================
echo.

echo Stopping all Python processes related to LegalMitra...

REM Try to stop by window title first (gentle)
taskkill /FI "WINDOWTITLE eq LegalMitra*" /F >nul 2>&1

REM Also stop any Python processes (if needed)
for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq python.exe" /FO LIST ^| findstr /C:"PID:"') do (
    taskkill /PID %%a /F >nul 2>&1
)

timeout /t 2 /nobreak >nul

echo.
echo Server stopped!
echo.
echo To start again, run: START_LEGALMITRA.vbs
echo.
pause










