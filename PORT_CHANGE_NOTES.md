# Port Configuration Change

## Default Port Changed: 8000 → 8888

The default port has been changed from **8000** to **8888** to avoid conflicts with other projects.

## How to Change Port

### Method 1: Edit .env file (Recommended)
Edit `backend/.env` and change:
```env
PORT=8888
```
Change `8888` to any available port (e.g., 5000, 8889, 9999, etc.)

### Method 2: Environment Variable
Set PORT as environment variable:
```bash
# Windows PowerShell
$env:PORT=8889
python -m app.main

# Windows CMD
set PORT=8889
python -m app.main

# Linux/Mac
export PORT=8889
python -m app.main
```

### Method 3: Command Line (Uvicorn)
```bash
uvicorn app.main:app --port 8889 --reload
```

## Update Frontend if Port Changes

If you change the backend port, also update `frontend/config.js`:
```javascript
const CONFIG = {
    API_BASE_URL: 'http://localhost:YOUR_PORT/api/v1',
    // ...
};
```

Or update `frontend/index.html` directly:
```javascript
const API_BASE_URL = 'http://localhost:YOUR_PORT/api/v1';
```

## Current Configuration

- **Default Port**: 8888
- **Config File**: `backend/.env`
- **Frontend Config**: `frontend/config.js`
- **Startup Script**: Automatically reads from `.env`

## Notes

- Port 8888 was chosen to avoid common port conflicts
- Ports 8000 and 8080 are commonly used by other development servers
- The startup script will display the actual port being used
- All documentation has been updated to reflect port 8888









