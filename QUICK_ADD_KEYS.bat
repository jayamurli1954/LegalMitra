@echo off
REM Quick script to open .env file for editing

title LegalMitra - Open .env File

echo ========================================
echo    Opening .env File for Editing
echo ========================================
echo.

cd /d "%~dp0\backend"

if exist ".env" (
    echo Opening .env file...
    notepad .env
    echo.
    echo ========================================
    echo    Instructions:
    echo ========================================
    echo.
    echo 1. Find these lines:
    echo    GOOGLE_GEMINI_API_KEY=your_gemini_key_here
    echo    GROK_API_KEY=your_grok_key_here
    echo.
    echo 2. Replace "your_gemini_key_here" with your actual Gemini key
    echo 3. Replace "your_grok_key_here" with your actual Grok key
    echo 4. Save the file (Ctrl+S)
    echo.
    echo ========================================
    echo    Getting API Keys:
    echo ========================================
    echo.
    echo Google Gemini: https://makersuite.google.com/app/apikey
    echo Grok (xAI): https://console.x.ai/
    echo.
    echo ========================================
    echo.
    echo After saving, restart the server!
    echo.
) else (
    echo .env file not found!
    echo Creating new .env file...
    (
        echo # LegalMitra Configuration
        echo AI_PROVIDER=anthropic
        echo DEFAULT_AI_MODEL=claude-sonnet-4-20250514
        echo.
        echo # Your API Keys
        echo ANTHROPIC_API_KEY=your_anthropic_key_here
        echo GOOGLE_GEMINI_API_KEY=your_gemini_key_here
        echo GROK_API_KEY=your_grok_key_here
        echo.
        echo # Server Configuration
        echo PORT=8888
        echo MAX_TOKENS=4000
        echo TEMPERATURE=0.3
    ) > .env
    echo Created .env file!
    echo Opening it now...
    timeout /t 2 /nobreak >nul
    notepad .env
)

pause









