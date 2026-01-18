@echo off
REM LegalMitra Startup Script
REM Starts both backend and frontend servers

echo ======================================================================
echo LegalMitra Startup Script
echo ======================================================================
echo.
echo Starting LegalMitra application...
echo.
echo This will start:
echo   1. Backend API Server (port 8888)
echo   2. Frontend Web Server (port 3005)
echo.
echo ======================================================================
echo.

REM Start backend in new window
echo [1/2] Starting Backend API Server...
start "LegalMitra Backend" cmd /k "cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8888 --reload"

REM Wait a bit for backend to start
echo Waiting 5 seconds for backend to initialize...
timeout /t 5 /nobreak >nul

REM Start frontend in new window
echo [2/2] Starting Frontend Web Server...
start "LegalMitra Frontend" cmd /k "python start_frontend.py"

echo.
echo ======================================================================
echo LegalMitra is starting!
echo ======================================================================
echo.
echo Frontend: http://localhost:3005
echo Backend:  http://localhost:8888
echo.
echo Two new windows have been opened:
echo   - LegalMitra Backend (API server)
echo   - LegalMitra Frontend (Web server)
echo.
echo Your browser should open automatically in a few seconds.
echo.
echo To stop the servers, close both windows or press Ctrl+C in each.
echo ======================================================================
echo.
pause
