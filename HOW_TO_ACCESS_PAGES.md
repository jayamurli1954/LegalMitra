# How to Access Pages Correctly

## ❌ Problem: Opening Files Directly

**DON'T do this:**
```
Double-click: frontend/templates.html
→ Opens as: file:///D:/SanMitra_Tech/LegalMitra/frontend/templates.html
→ ❌ Error: "This page needs to be opened via http://localhost"
```

## ✅ Solution: Use HTTP Server

**DO this instead:**
```
1. Start frontend server
2. Open: http://localhost:3005
3. Navigate using links/buttons
→ ✅ Everything works!
```

---

## 🚀 Quick Start (Easiest Method)

### Option 1: Use Startup Script (Recommended)

**Double-click:**
```
start_legalmitra.bat
```

This automatically:
1. ✅ Starts backend (port 8888)
2. ✅ Starts frontend server (port 3005)
3. ✅ Opens browser to http://localhost:3005

### Option 2: Start Manually

**Step 1: Start Backend** (Terminal 1)
```bash
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8888 --reload
```

**Step 2: Start Frontend Server** (Terminal 2)
```bash
# From project root directory
python start_frontend.py
```

**Step 3: Open Browser**
```
http://localhost:3005
```

---

## 🌐 Navigation Structure

When using `http://localhost:3005`, all navigation works:

### Main Pages:

| Page | URL | How to Access |
|------|-----|---------------|
| **Main App** | `http://localhost:3005/index.html` | Default home page |
| **Templates** | `http://localhost:3005/templates.html` | Click "Document Templates (48)" button |
| **Marketplace** | `http://localhost:3005/template-marketplace.html` | Direct URL or add link |
| **Cost Dashboard** | `http://localhost:3005/cost-dashboard.html` | Click "Cost Dashboard" button |
| **Model Selector** | `http://localhost:3005/model-selector.html` | Click "AI Models" button |

### Navigation Buttons Work:

- ✅ **"← Back to LegalMitra"** on templates page → Goes to `index.html`
- ✅ **"Document Templates (48)"** button → Goes to `templates.html`
- ✅ **"Cost Dashboard"** button → Goes to `cost-dashboard.html`
- ✅ **All links and buttons work correctly**

---

## 📋 Step-by-Step: Access Templates Page

### Method 1: Via Main Page (Recommended)

1. Start servers: `start_legalmitra.bat`
2. Browser opens: `http://localhost:3005` (shows main page)
3. Click: **"📋 Document Templates (48)"** button
4. ✅ Templates page loads with all 48 templates

### Method 2: Direct URL

1. Start servers: `start_legalmitra.bat`
2. Browser: Go to `http://localhost:3005/templates.html`
3. ✅ Templates page loads directly

### Method 3: Access Marketplace

1. Start servers: `start_legalmitra.bat`
2. Browser: Go to `http://localhost:3005/template-marketplace.html`
3. ✅ Marketplace shows all 63 templates

---

## 🔍 Why Navigation Works

### When Using HTTP Server (`http://localhost:3005`):

```
✅ Relative paths work: index.html, templates.html
✅ API calls work: http://localhost:8888/api/v1/...
✅ CORS headers included
✅ All JavaScript works
✅ Back buttons work: window.location.href='index.html'
```

### When Opening Files Directly (`file:///...`):

```
❌ Relative paths broken
❌ API calls blocked (CORS error)
❌ JavaScript fails
❌ Navigation doesn't work
```

---

## 🛠️ Troubleshooting

### Error: "Port 3005 already in use"

**Solution:**
```bash
# Find process using port 3005
netstat -ano | findstr ":3005"

# Kill it (replace PID with actual number)
taskkill /F /PID <PID>
```

### Error: "Backend server not running"

**Check:**
1. Backend running on port 8888?
2. Test: `http://localhost:8888/health`
3. Should return: `{"status": "ok"}`

### Still Seeing File:// Error?

**Check:**
1. ✅ Using `http://localhost:3005` (NOT `file:///...`)
2. ✅ Frontend server running (`python start_frontend.py`)
3. ✅ URL starts with `http://` not `file://`

---

## 📝 Quick Reference

### Start Everything:
```bash
# Double-click or run:
start_legalmitra.bat
```

### Access Pages:
- **Main**: `http://localhost:3005` or `http://localhost:3005/index.html`
- **Templates**: `http://localhost:3005/templates.html`
- **Marketplace**: `http://localhost:3005/template-marketplace.html`
- **Cost Dashboard**: `http://localhost:3005/cost-dashboard.html`

### Stop Servers:
- Press `Ctrl+C` in each terminal window
- Or close the terminal windows

---

## ✅ Summary

**DO:**
- ✅ Use `start_legalmitra.bat` or `python start_frontend.py`
- ✅ Access via `http://localhost:3005`
- ✅ Use navigation buttons/links

**DON'T:**
- ❌ Open HTML files directly from file system
- ❌ Use `file:///` URLs
- ❌ Double-click HTML files

---

**That's it! Just use the startup script and everything works!** 🚀
