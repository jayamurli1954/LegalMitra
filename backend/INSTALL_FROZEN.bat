@echo off
REM Script to install frozen (exact) package versions
REM This prevents breaking changes from package updates

echo ========================================
echo   Installing Frozen Dependencies
echo ========================================
echo.
echo This will install EXACT versions to prevent breaking changes.
echo.

cd /d "%~dp0"

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

REM Check if frozen file exists
if not exist "requirements-frozen.txt" (
    echo ERROR: requirements-frozen.txt not found!
    echo.
    echo Run FREEZE_REQUIREMENTS.bat first to create it.
    echo.
    pause
    exit /b 1
)

echo Installing frozen dependencies...
python -m pip install --upgrade pip -q
python -m pip install -r requirements-frozen.txt

if errorlevel 1 (
    echo.
    echo WARNING: Some dependencies failed to install!
    echo You may need to update requirements-frozen.txt
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   SUCCESS!
echo ========================================
echo.
echo All frozen dependencies installed successfully.
echo Your code should now work without breaking changes.
echo.
pause


