# How to Run LegalMitra

## Quick Start (Recommended)

### Option 1: Use the Startup Script (Easiest)

**Windows**:
```bash
# Double-click this file:
start_legalmitra.bat

# Or run from command prompt:
start_legalmitra.bat
```

This will:
1. Start the backend server on port 8888
2. Start the frontend server on port 3000
3. Open your browser automatically to http://localhost:3005

---

## Manual Start

### Option 2: Start Servers Separately

**Step 1: Start Backend**
```bash
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8888 --reload
```

**Step 2: Start Frontend (in new terminal)**
```bash
# From project root
python start_frontend.py
```

**Step 3: Open Browser**
```
http://localhost:3005
```

---

## Troubleshooting

### Problem: "Port already in use"

**Solution**: Kill existing processes on ports 8888 and 3000

```bash
# Find process on port 8888
netstat -ano | findstr ":8888"

# Kill process (replace PID with actual process ID)
taskkill /F /PID <PID>

# Same for port 3000
netstat -ano | findstr ":3000"
taskkill /F /PID <PID>
```

### Problem: "This page needs to be opened via http://localhost"

**Cause**: You're opening `frontend/index.html` directly as a file

**Solution**: Use one of the startup methods above (use the web server)

### Problem: Templates not loading

**Check**:
1. Backend server is running (http://localhost:8888)
2. Frontend is accessed via http://localhost:3005 (not file://)
3. API calls are going to the correct endpoint

**Test Backend**:
```bash
curl http://localhost:8888/api/v1/templates/categories
```

Should return JSON with template categories.

### Problem: Sidebar showing default data

**Cause**: Google API quota exceeded

**Status**: This is expected until quota resets tomorrow

**Check Quota**:
```bash
curl http://localhost:8888/api/v1/cache-stats
```

Look for `"quota_status"` in the response.

---

## URLs Reference

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:3005 | Main application |
| Backend API | http://localhost:8888 | API server |
| API Docs | http://localhost:8888/docs | Interactive API documentation |
| Cache Stats | http://localhost:8888/api/v1/cache-stats | Monitor cache performance |

---

## First Time Setup

### Install Dependencies

**Backend**:
```bash
cd backend
pip install -r requirements.txt
```

**Frontend**:
No installation needed! Pure HTML/CSS/JavaScript.

---

## Environment Variables

### Backend Configuration

**File**: `backend/.env`

```env
# AI Provider (anthropic, openai, google, grok, openrouter)
AI_PROVIDER=anthropic
ANTHROPIC_API_KEY=your_key_here

# Google Custom Search (for sidebar)
GOOGLE_CUSTOM_SEARCH_API_KEY=your_key_here
GOOGLE_CUSTOM_SEARCH_ENGINE_ID=your_id_here

# Server
PORT=8888
```

---

## Development Mode

### Backend with Auto-Reload
```bash
cd backend
python -m uvicorn app.main:app --reload --port 8888
```

Changes to Python files will automatically reload the server.

### Frontend Development
The frontend server (`start_frontend.py`) serves static files. Just refresh your browser to see changes.

---

## Production Deployment

### Backend
```bash
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8888 --workers 4
```

### Frontend
Use a production web server like Nginx or Apache to serve the `frontend/` directory.

**Nginx Example**:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    root /path/to/LegalMitra/frontend;
    index index.html;

    location /api {
        proxy_pass http://localhost:8888;
    }
}
```

---

## Testing

### Test Backend API
```bash
# Test health endpoint
curl http://localhost:8888/health

# Test cache stats
curl http://localhost:8888/api/v1/cache-stats

# Test templates
curl http://localhost:8888/api/v1/templates/categories
```

### Test Frontend
1. Open http://localhost:3005
2. Click "Document Templates"
3. Should see categories and search bar (not error message)

---

## Stopping the Servers

### If using startup script
Close the two command windows that were opened:
- "LegalMitra Backend"
- "LegalMitra Frontend"

### If running manually
Press `Ctrl+C` in each terminal window

---

## Common Commands

### Start Everything
```bash
start_legalmitra.bat
```

### Just Backend
```bash
cd backend
python -m uvicorn app.main:app --port 8888 --reload
```

### Just Frontend
```bash
python start_frontend.py
```

### Clear Cache
```bash
curl -X POST http://localhost:8888/api/v1/cache-clear
```

### Check Cache Performance
```bash
curl http://localhost:8888/api/v1/cache-stats | python -m json.tool
```

### Run Tests
```bash
# Test Google API
python scripts/test_google_api_direct.py

# Test caching
python scripts/test_cache_demo.py
```

---

## File Structure

```
LegalMitra/
├── start_legalmitra.bat       # Quick start script
├── start_frontend.py           # Frontend web server
├── frontend/
│   └── index.html             # Main application (open via http://)
├── backend/
│   ├── app/
│   │   ├── main.py            # FastAPI application
│   │   ├── api/               # API endpoints
│   │   ├── services/          # Business logic
│   │   └── models/            # Database models
│   ├── .env                   # Configuration
│   └── data/                  # Cache and data storage
└── scripts/                   # Testing utilities
```

---

## Next Steps

1. ✅ Start the application using `start_legalmitra.bat`
2. ✅ Open http://localhost:3005 in your browser
3. ✅ Test the Document Templates feature
4. ✅ Check cache stats at http://localhost:8888/api/v1/cache-stats
5. ✅ Wait for Google quota reset tomorrow for live sidebar data

---

## Need Help?

### Documentation
- `IMPLEMENTATION_COMPLETE_README.md` - Complete system guide
- `QUICK_REFERENCE_CACHING.md` - Caching quick reference
- `WHATS_NEW.md` - Recent changes and features

### Support
Check the documentation files in the project root for detailed guides.

---

**Quick Reminder**:
- Always use http://localhost:3005 (not file://)
- Backend must be running on port 8888
- Frontend must be served via HTTP server (not opened as file)
