# Port Configuration for LegalMitra

## LegalMitra Ports ✅

| Service | Port | URL |
|---------|------|-----|
| **Backend API** | **8888** | http://localhost:8888 |
| **Frontend** | **3005** | http://localhost:3005 |

---

## Your Other Projects (Reserved Ports)

To avoid conflicts with your other projects:

| Project | Likely Port(s) |
|---------|----------------|
| GharMitra | 3000, 8000 ? |
| MandirMitra | 3001, 8001 ? |
| MitraBooks | 3002, 8002 ? |
| InvestPro | 3003, 8003 ? |
| TradingBot | 3004, 8004 ? |
| **LegalMitra** | **3005, 8888** ✅ |

---

## Port Selection Rationale

### Frontend: Port 3005
- **Avoids**: Your port 3000 project
- **Pattern**: Sequential numbering for "Mitra" projects
- **Easy to Remember**: 3005 = LegalMitra frontend

### Backend: Port 8888
- **Unique**: Unlikely to conflict with typical dev ports (3000-3010, 8000-8010)
- **Memorable**: Repeating digits (8888)
- **Traditional**: Many backend servers use 8xxx range

---

## How to Change Ports (If Needed)

### Change Frontend Port

**File**: `start_frontend.py` (line 13)

```python
PORT = 3005  # Change this number
```

### Change Backend Port

**File**: `backend/.env`

```env
PORT=8888  # Change this number
```

**Or** when starting manually:

```bash
cd backend
python -m uvicorn app.main:app --port 9000  # Any port you want
```

### Update Startup Script

**File**: `start_legalmitra.bat`

Update the port numbers in the echo statements and the startup commands.

---

## Recommended Port Scheme for All Projects

### Pattern: 30XX for Frontend, 80XX for Backend

| Project | Frontend | Backend |
|---------|----------|---------|
| GharMitra | 3000 | 8000 |
| MandirMitra | 3001 | 8001 |
| MitraBooks | 3002 | 8002 |
| InvestPro | 3003 | 8003 |
| TradingBot | 3004 | 8004 |
| **LegalMitra** | **3005** | **8888** |

**Benefits**:
- Easy to remember pattern
- No conflicts between projects
- Frontend and backend ports clearly related (3000 ↔ 8000)

---

## Checking for Port Conflicts

### Windows

```bash
# Check if port is in use
netstat -ano | findstr ":3005"
netstat -ano | findstr ":8888"

# If port is occupied, kill process
taskkill /F /PID <PID>
```

### Quick Test

```bash
# Test frontend
curl http://localhost:3005

# Test backend
curl http://localhost:8888/health
```

---

## All LegalMitra URLs

| Purpose | URL |
|---------|-----|
| **Main App** | http://localhost:3005 |
| **Templates** | http://localhost:3005 (click Templates button) |
| **API Health** | http://localhost:8888/health |
| **API Docs** | http://localhost:8888/docs |
| **Cache Stats** | http://localhost:8888/api/v1/cache-stats |
| **Template Categories** | http://localhost:8888/api/v1/templates/categories |

---

## Firewall/Security Notes

### Development (Current Setup)
- Both servers listen on `localhost` only
- Not accessible from other machines
- Safe for development

### Production Deployment
- Use reverse proxy (Nginx/Apache)
- Single public port (80/443)
- Backend not directly exposed

**Example Nginx Config**:
```nginx
server {
    listen 80;
    server_name legalmitra.com;

    # Frontend
    location / {
        proxy_pass http://localhost:3005;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8888;
    }
}
```

---

## Troubleshooting

### "Address already in use" Error

**Symptom**: Can't start server, port already occupied

**Solution 1**: Kill the existing process
```bash
netstat -ano | findstr ":3005"
taskkill /F /PID <PID>
```

**Solution 2**: Use a different port
```python
# In start_frontend.py
PORT = 3006  # Or any available port
```

### Can't Access from Browser

**Check**:
1. ✅ Server is running (check terminal output)
2. ✅ Using correct URL (http://localhost:3005)
3. ✅ No firewall blocking localhost
4. ✅ Browser not forcing HTTPS

---

## Multi-Project Development

### Running Multiple Projects Simultaneously

If you need to run LegalMitra + GharMitra + others at the same time:

```bash
# LegalMitra
Frontend: http://localhost:3005
Backend:  http://localhost:8888

# GharMitra (example)
Frontend: http://localhost:3000
Backend:  http://localhost:8000

# All running simultaneously without conflicts ✅
```

### Quick Switch Script

Create a `switch-project.bat`:

```batch
@echo off
echo Which project?
echo 1. GharMitra (3000/8000)
echo 2. MandirMitra (3001/8001)
echo 3. LegalMitra (3005/8888)
choice /c 123 /n /m "Select: "

if errorlevel 3 goto legalmitra
if errorlevel 2 goto mandirmitra
if errorlevel 1 goto gharmitra

:gharmitra
start chrome http://localhost:3000
goto end

:mandirmitra
start chrome http://localhost:3001
goto end

:legalmitra
start chrome http://localhost:3005
goto end

:end
```

---

## Summary

✅ **LegalMitra Frontend**: Port 3005 (avoids your port 3000)
✅ **LegalMitra Backend**: Port 8888 (unique, memorable)
✅ **No Conflicts**: Won't clash with your other projects
✅ **Easy to Change**: If you need different ports later

---

**Current Configuration**:
```
LegalMitra Frontend → http://localhost:3005
LegalMitra Backend  → http://localhost:8888
```

**Updated**: January 17, 2026
**Status**: ✅ Configured to avoid port conflicts
