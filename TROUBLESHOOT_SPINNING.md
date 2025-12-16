# Troubleshooting: "Spinning" / Loading Issue

## 🔍 What "Spinning" Means

If you see a loading spinner, it usually means:
- ✅ Server is running
- ⏳ Waiting for AI response (this is normal!)
- ❌ OR there's an error happening

## ⏱️ Normal Behavior

**AI responses take time!**
- Typical response: **10-30 seconds**
- Complex queries: **30-60 seconds**
- Document drafting: **20-40 seconds**

This is **normal** - the AI needs time to process your legal query.

## 🔍 How to Check What's Happening

### Option 1: Check Server Window

Look at the server window (the one that shows "LegalMitra - AI Legal Assistant"). You should see:
- Request logs
- Any error messages
- Processing status

### Option 2: Check Browser Console

1. **Press `F12`** in your browser
2. **Click** "Console" tab
3. **Look for:**
   - Error messages (red text)
   - Network requests
   - Connection errors

### Option 3: Test API Directly

1. **Open:** http://localhost:8888/docs
2. **Try** a simple test query
3. **Watch** for errors or timeout

## 🐛 Common Issues

### Issue 1: API Key Error (Causes Timeout)

**Symptom:** Spinning forever, then error

**Check:**
- Server window shows API key error
- Error in browser console

**Fix:**
- Verify API key in `.env` file
- Restart server after fixing

### Issue 2: Network Timeout

**Symptom:** Spinning for 60+ seconds

**Check:**
- Internet connection
- Firewall blocking API calls
- API service status (check xAI console)

**Fix:**
- Check internet connection
- Wait longer (AI can be slow)
- Check API quota/limits

### Issue 3: Server Not Responding

**Symptom:** Spinning immediately, no response

**Check:**
- Is server window still open?
- Is port 8888 accessible?

**Fix:**
- Restart server
- Check `http://localhost:8888/health`

## ✅ Quick Tests

### Test 1: Health Check
Open in browser: http://localhost:8888/health
- Should show: `{"status":"healthy"}`
- If error: Server not running

### Test 2: Simple Query
Try a very simple query first:
- "What is GST?"
- Should respond in 10-20 seconds

### Test 3: Check Server Logs
Look at server window for:
- ✅ "✅ Grok (xAI) client initialized"
- ❌ Error messages
- ⏳ "Processing request..." messages

## 🚀 What to Do Right Now

1. **Check server window** - Look for error messages
2. **Wait** - If it's been less than 60 seconds, wait longer
3. **Try simple query** - Test with a very simple question first
4. **Check browser console** - Press F12, look for errors
5. **Test API docs** - Go to http://localhost:8888/docs and try there

## 💡 Tips

- **Simple queries are faster** - Complex legal research takes longer
- **First request is slowest** - API initialization takes time
- **Check server window** - It shows what's actually happening
- **Be patient** - AI responses take 10-30 seconds normally

## 🔧 If Still Spinning After 60 Seconds

1. **Stop** the request (refresh page)
2. **Check** server window for errors
3. **Try** a simpler query
4. **Check** API key is valid
5. **Restart** server if needed

---

**Most likely: It's just processing! AI responses take time. Check the server window to see what's happening.** ⏳








