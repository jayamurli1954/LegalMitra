# PowerShell Commands to Clear Cache and Restart

## Clear Python Cache (PowerShell)

Run these commands in PowerShell:

```powershell
cd D:\LegalMitra\backend

# Remove __pycache__ directories
Get-ChildItem -Path . -Recurse -Directory -Filter __pycache__ | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

# Remove .pyc files  
Get-ChildItem -Path . -Recurse -Filter *.pyc | Remove-Item -Force -ErrorAction SilentlyContinue

Write-Host "Cache cleared!" -ForegroundColor Green
```

## Or Use the Script

I've created `CLEAR_CACHE.ps1` - just run:
```powershell
.\CLEAR_CACHE.ps1
```

## Then Restart Server

After clearing cache, restart using:
- Double-click: `START_LEGALMITRA_SIMPLE.bat`

Or manually in PowerShell:
```powershell
cd D:\LegalMitra\backend
.\venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload --port 8888
```



