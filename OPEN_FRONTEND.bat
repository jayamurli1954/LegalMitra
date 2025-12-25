@echo off
REM Quick script to open the frontend

cd /d "%~dp0"
start "" "frontend\index.html"

echo Frontend opened in your browser!
timeout /t 2 /nobreak >nul










