# 🚀 Quick Start - Start the Server

## The Problem
You're seeing "Failed to fetch" because **the backend server is not running**.

## Solution - Choose ONE method:

### Method 1: Double-Click (Easiest) ⭐
1. **Double-click** `START_LEGALMITRA_SIMPLE.bat` in the project root folder
2. Wait for "Application startup complete!"
3. **Keep that window open** (closing it stops the server)
4. Refresh your browser page

### Method 2: PowerShell Script
1. **Right-click** `START_SERVER.ps1` 
2. Select **"Run with PowerShell"**
3. **Keep that window open**
4. Refresh your browser

### Method 3: Manual Command
1. Open PowerShell or Command Prompt
2. Run these commands:
   ```powershell
   cd D:\LegalMitra\backend
   .\venv\Scripts\activate
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8888 --reload
   ```
3. **Keep that window open**
4. Refresh your browser

## ✅ Verify Server is Running

Once started, you should see:
- Logs in the terminal showing "Application startup complete!"
- No errors about port 8888 being in use
- You can visit: http://localhost:8888/docs (API documentation)

## 🔄 Then Refresh Browser

After the server starts:
1. Go back to your browser
2. Press **F5** or **Ctrl+R** to refresh
3. Try your query again

## ⚠️ Important

- **DO NOT close the terminal window** - that stops the server
- The server must stay running while you use the application
- If you close it, you'll see "Failed to fetch" again

---

**Your code is frozen and working correctly - you just need the server running!**

