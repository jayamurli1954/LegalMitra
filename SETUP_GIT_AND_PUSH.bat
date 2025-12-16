@echo off
echo ========================================
echo Setting up Git and pushing to GitHub
echo ========================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed or not in PATH
    echo Please install Git from https://git-scm.com/
    pause
    exit /b 1
)

echo [1/5] Initializing Git repository...
git init
if errorlevel 1 (
    echo ERROR: Failed to initialize git repository
    pause
    exit /b 1
)

echo.
echo [2/5] Adding all files...
git add .
if errorlevel 1 (
    echo ERROR: Failed to add files
    pause
    exit /b 1
)

echo.
echo [3/5] Creating initial commit...
git commit -m "Initial commit: LegalMitra - AI Legal Assistant (Stable Version)"
if errorlevel 1 (
    echo ERROR: Failed to create commit
    pause
    exit /b 1
)

echo.
echo [4/5] Adding GitHub remote...
git remote add origin https://github.com/jayamurli1954/LegalMitra.git
if errorlevel 1 (
    echo WARNING: Remote might already exist, trying to set URL...
    git remote set-url origin https://github.com/jayamurli1954/LegalMitra.git
)

echo.
echo [5/5] Pushing to GitHub...
echo NOTE: You may be prompted for GitHub credentials
git branch -M main
git push -u origin main
if errorlevel 1 (
    echo.
    echo ERROR: Push failed. Common reasons:
    echo 1. GitHub credentials not configured
    echo 2. Repository doesn't exist on GitHub
    echo 3. Network issues
    echo.
    echo Please check:
    echo - Repository exists at https://github.com/jayamurli1954/LegalMitra
    echo - You have push access
    echo - Your GitHub credentials are configured
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo SUCCESS! Code pushed to GitHub
echo ========================================
echo Repository: https://github.com/jayamurli1954/LegalMitra
echo.
pause

