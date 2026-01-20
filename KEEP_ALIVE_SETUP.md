# Keep-Alive Service Setup for Render Free Tier

## 🎯 Why Keep-Alive?

Render's free tier spins down after **~15 minutes of inactivity**, causing **50+ second delays** on first request. A keep-alive service pings your app every 10-14 minutes to keep it awake.

## ✅ Quick Setup (5 minutes)

### Option 1: UptimeRobot (Recommended - Free & Reliable)

**Best for**: Automatic monitoring + keep-alive

1. **Sign up**: Go to https://uptimerobot.com (free account, no credit card)
2. **Add Monitor**:
   - Click **"+ Add New Monitor"**
   - Monitor Type: **HTTP(s)**
   - Friendly Name: `LegalMitra Keep-Alive`
   - URL: `https://legalmitra-app.onrender.com/health`
   - Monitoring Interval: **5 minutes** (free tier allows this)
   - Click **"Create Monitor"**

3. **Done!** UptimeRobot will ping your app every 5 minutes, keeping it awake 24/7.

**Benefits**:
- ✅ Free forever
- ✅ Email alerts if app goes down
- ✅ Uptime statistics
- ✅ Works reliably

---

### Option 2: cron-job.org (Free Cron Service)

**Best for**: Simple scheduled pings

1. **Sign up**: Go to https://cron-job.org (free account)
2. **Create Cron Job**:
   - Click **"Create cronjob"**
   - Title: `LegalMitra Keep-Alive`
   - Address: `https://legalmitra-app.onrender.com/health`
   - Schedule: Every **10 minutes** (free tier allows minimum 1 minute)
   - Click **"Create Cronjob"**

3. **Done!** Your app will be pinged every 10 minutes.

**Benefits**:
- ✅ Free forever
- ✅ Very reliable
- ✅ Simple interface

---

### Option 3: EasyCron (Alternative)

1. Go to https://www.easycron.com
2. Sign up (free account)
3. Create a cron job:
   - URL: `https://legalmitra-app.onrender.com/health`
   - Schedule: Every 10 minutes
   - Save

---

## 🔍 Health Endpoint Details

Your app has a health check endpoint ready:

- **URL**: `https://legalmitra-app.onrender.com/health`
- **Method**: GET
- **Response**: 
  ```json
  {
    "status": "ok",
    "service": "legalmitra-api",
    "timestamp": "2026-01-20T13:00:00",
    "uptime_check": "healthy"
  }
  ```
- **Status Code**: 200 OK (if app is running)

## ⚙️ Recommended Settings

| Setting | Recommended Value | Why |
|---------|------------------|-----|
| **Interval** | 10-14 minutes | Keeps app awake without excessive requests |
| **Timeout** | 30 seconds | Enough for cold start if needed |
| **Alert** | Optional | Notify if app is down (UptimeRobot) |

## 🧪 Testing

After setting up, test by:

1. **Wait 15+ minutes** (let app spin down)
2. **Visit your app**: `https://legalmitra-app.onrender.com`
3. **Should load immediately** (no 50-second delay)

If it still takes 50+ seconds, check:
- ✅ Cron job is actually running (check logs)
- ✅ URL is correct: `https://legalmitra-app.onrender.com/health`
- ✅ Interval is ≤ 14 minutes

## 💰 Cost

All options above are **100% FREE** for basic monitoring/keep-alive.

## 🚀 Alternative: Upgrade to Paid Tier

If you want zero spin-downs and better performance:

- **Render Starter Plan**: $7/month
- Always-on service (no spin-downs)
- No cold starts
- Better for production use
- More reliable for legal professionals

## 📊 Monitoring Your Keep-Alive

### Check if it's working:

1. **Render Logs**: Check Render dashboard → Logs
   - Should see: `"GET /health HTTP/1.1" 200` every 10-14 minutes

2. **UptimeRobot Dashboard**: Shows ping history and uptime stats

3. **Test manually**: Visit `https://legalmitra-app.onrender.com/health` in browser
   - Should return JSON immediately

## 🔧 Troubleshooting

### App still spinning down?

1. **Verify cron job is running**:
   - Check UptimeRobot/cron-job dashboard
   - Look for successful pings in logs

2. **Check URL**:
   - Must be: `https://legalmitra-app.onrender.com/health`
   - Not: `http://` (must be HTTPS)
   - Not: `/api/v1/health` (use root `/health`)

3. **Check interval**:
   - Must be ≤ 14 minutes
   - 10 minutes is ideal

4. **Check Render logs**:
   - Should see health check requests coming in
   - If not, cron service might not be working

### Too many requests?

- Free tier allows reasonable keep-alive pings
- 10-14 minute intervals are safe
- Render won't charge for health check pings
- ~144 requests/day (every 10 min) is acceptable

## 📝 Quick Reference

**Health Endpoint**: `https://legalmitra-app.onrender.com/health`

**Recommended Service**: UptimeRobot (5 min intervals)

**Recommended Interval**: 10 minutes

**Expected Result**: App stays awake, no 50-second delays

---

## ✅ Setup Checklist

- [ ] Choose a keep-alive service (UptimeRobot recommended)
- [ ] Create account (free)
- [ ] Add monitor/cron job with URL: `https://legalmitra-app.onrender.com/health`
- [ ] Set interval to 10 minutes
- [ ] Verify it's working (check logs after 15 minutes)
- [ ] Test app loads immediately (no delay)

---

**Need help?** Check Render logs or the keep-alive service dashboard for ping history.
