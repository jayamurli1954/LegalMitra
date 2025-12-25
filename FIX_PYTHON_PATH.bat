@echo off
REM Fix Python Path Issue - Recreate Virtual Environment

echo ========================================
echo    Fixing Python Path Issue
echo ========================================
echo.

cd /d "%~dp0backend"

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not in PATH!
    echo Please make sure Python is installed and added to PATH.
    pause
    exit /b 1
)

echo [1/3] Removing old virtual environment...
if exist venv (
    rmdir /s /q venv
    echo Old venv removed.
) else (
    echo No old venv found.
)

echo.
echo [2/3] Creating new virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment!
    pause
    exit /b 1
)
echo Virtual environment created successfully!

echo.
echo [3/3] Activating and installing dependencies...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip -q
python -m pip install -r requirements.txt

echo.
echo ========================================
echo    Fix Complete!
echo ========================================
echo.
echo The virtual environment has been recreated with the correct Python path.
echo You can now run START_LEGALMITRA_SIMPLE.bat
echo.
pause

