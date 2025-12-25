@echo off
REM Quick test of API

title LegalMitra - Test API

echo ========================================
echo    Testing LegalMitra API
echo ========================================
echo.

echo Testing health endpoint...
curl -s http://localhost:8888/health
echo.
echo.

echo Testing root endpoint...
curl -s http://localhost:8888/
echo.
echo.

echo ========================================
echo    Test Results
echo ========================================
echo.
echo If you see JSON responses above, server is working!
echo.
echo To test API in browser:
echo 1. Open: http://localhost:8888/docs
echo 2. Try the /api/v1/legal-research endpoint
echo.
pause










