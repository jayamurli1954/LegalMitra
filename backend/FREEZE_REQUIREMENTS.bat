@echo off
REM Script to freeze current package versions
REM This creates requirements-frozen.txt with exact versions

echo ========================================
echo   Freezing Package Versions
echo ========================================
echo.

cd /d "%~dp0"

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

echo Creating frozen requirements file...
python -m pip freeze > requirements-frozen.txt

echo.
echo ========================================
echo   SUCCESS!
echo ========================================
echo.
echo Frozen requirements saved to: requirements-frozen.txt
echo.
echo To use frozen versions in future:
echo   pip install -r requirements-frozen.txt
echo.
pause


