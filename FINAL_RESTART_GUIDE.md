# 🔥 FINAL RESTART GUIDE - READ THIS!

## The Problem
Even after fixing the code, the error persists because **the server needs a COMPLETE restart**.

## Step-by-Step Restart Instructions:

### 1. STOP THE SERVER COMPLETELY
- Find the terminal/command prompt window running the server
- Press `Ctrl+C` to stop it
- **IMPORTANT**: Wait until you see the command prompt (server fully stopped)
- **If Ctrl+C doesn't work**: Close the entire terminal window

### 2. CLEAR CACHE MANUALLY (IMPORTANT!)
Open a NEW command prompt and run:
```bash
cd D:\LegalMitra\backend
rmdir /s /q __pycache__ 2>nul
for /d /r . %d in (__pycache__) do @if exist "%d" rmdir /s /q "%d" 2>nul
del /s /q *.pyc 2>nul
echo Cache cleared!
```

### 3. RESTART USING THE UPDATED BATCH FILE
- Double-click: `START_LEGALMITRA_SIMPLE.bat` (from the project root)
- Wait for "Application startup complete!"
- Watch for any error messages

### 4. VERIFY IT'S WORKING
- Make a query through the frontend
- **Check the SERVER CONSOLE** (the terminal where uvicorn is running)
- You should see:
  ```
  DEBUG: AI_PROVIDER='gemini', normalized provider='gemini'
  DEBUG: ✅✅✅ ENTERED GEMINI BLOCK!
  ```

## If You Still See Errors:
1. **Check server console output** - it will show debug messages
2. **Verify .env file** has: `AI_PROVIDER=gemini`
3. **Make sure you're using the updated batch file** (it now uses uvicorn with --reload)

## Quick Test
Run this to verify config:
```bash
cd backend
python test_provider.py
```

If this shows `✅ Would match`, then the code is correct - you just need to restart the server properly.

