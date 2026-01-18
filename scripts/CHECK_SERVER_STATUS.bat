@echo off
REM Check if server is running and responding

title LegalMitra - Check Server Status

echo ========================================
echo    Checking Server Status
echo ========================================
echo.

echo [1/3] Checking if server process is running...
tasklist /FI "IMAGENAME eq python.exe" | find /I "python.exe" >nul 2>&1
if %errorlevel% == 0 (
    echo [OK] Python process is running
) else (
    echo [ERROR] No Python process found - server is not running!
    echo Start the server with START_LEGALMITRA.vbs
    pause
    exit /b 1
)

echo.
echo [2/3] Testing server connection...
curl -s http://localhost:8888/health >nul 2>&1
if %errorlevel% == 0 (
    echo [OK] Server is responding on port 8888
) else (
    echo [WARNING] Server might not be responding
    echo Try: http://localhost:8888/health
)

echo.
echo [3/3] Testing API endpoint...
curl -s http://localhost:8888/api/v1/legal-research -X POST -H "Content-Type: application/json" -d "{\"query\":\"test\",\"query_type\":\"research\"}" >nul 2>&1
if %errorlevel% == 0 (
    echo [OK] API endpoint is accessible
) else (
    echo [WARNING] API endpoint might have issues
)

echo.
echo ========================================
echo    Server Status Summary
echo ========================================
echo.
echo If "spinning" means loading:
echo 1. Server might be processing (normal for AI calls)
echo 2. Check server window for error messages
echo 3. AI responses can take 10-30 seconds
echo.
echo To check server logs, look at the server window
echo that shows "LegalMitra - AI Legal Assistant"
echo.
echo ========================================
echo.

pause










