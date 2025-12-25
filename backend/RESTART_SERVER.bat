@echo off
echo ========================================
echo RESTARTING LegalMitra Server
echo ========================================
echo.
echo Stopping any running server...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *uvicorn*" 2>nul
timeout /t 2 /nobreak >nul
echo.
echo Clearing Python cache...
if exist __pycache__ rmdir /s /q __pycache__ 2>nul
for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d" 2>nul
for /r . %%f in (*.pyc) do @if exist "%%f" del /f /q "%%f" 2>nul
echo.
echo Starting server...
python -m uvicorn app.main:app --reload --port 8888
pause



