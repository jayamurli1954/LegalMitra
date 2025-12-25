# Fix: "Incorrect API key provided" Error

## 🔍 What the Error Means

The error shows:
```
Incorrect API key provided: your_api*****here
```

This means your `.env` file still has **placeholder text** instead of your **actual API key**.

## ✅ Quick Fix

### Step 1: Open Your .env File

**Location:** `D:\LegalMitra\backend\.env`

**Quick way:**
- Double-click `QUICK_ADD_KEYS.bat`
- OR navigate to `backend` folder and open `.env`

### Step 2: Check Your API Keys

Look for lines like:
```env
GROK_API_KEY=your_api_key_here
```

**This is WRONG!** You need to replace `your_api_key_here` with your **actual** Grok API key.

### Step 3: Replace with Real Keys

**For Grok:**
```env
GROK_API_KEY=xai-abc123xyz456...your_actual_key
```

**For Anthropic:**
```env
ANTHROPIC_API_KEY=sk-ant-api03-abc123...your_actual_key
```

**For Gemini:**
```env
GOOGLE_GEMINI_API_KEY=AIzaSyAbc123...your_actual_key
```

### Step 4: Verify Format

✅ **CORRECT:**
```env
GROK_API_KEY=xai-clgcA24VbrkEQVbpxHzQut1K6ATOMdTGekuay2G9aBXLXaJHwvdFSVzzSIfVdqCbiXZQYtBzZbsjVIq1
```

❌ **WRONG:**
```env
GROK_API_KEY=your_api_key_here
GROK_API_KEY = xai-abc123  (space around =)
GROK_API_KEY="xai-abc123"  (quotes)
```

### Step 5: Save and Restart

1. **Save** the file (`Ctrl+S`)
2. **Stop** the server (`Ctrl+C`)
3. **Restart** (`START_LEGALMITRA.vbs`)

## 🔍 Common Mistakes

### Mistake 1: Still Has Placeholder Text
```env
GROK_API_KEY=your_api_key_here  ❌
```
**Fix:** Replace with actual key

### Mistake 2: Spaces Around =
```env
GROK_API_KEY = xai-abc123  ❌
```
**Fix:** Remove spaces: `GROK_API_KEY=xai-abc123`

### Mistake 3: Added Quotes
```env
GROK_API_KEY="xai-abc123"  ❌
```
**Fix:** Remove quotes: `GROK_API_KEY=xai-abc123`

### Mistake 4: Wrong Provider Selected
If you're using Grok but have:
```env
AI_PROVIDER=openai  ❌
```
**Fix:** Change to:
```env
AI_PROVIDER=grok  ✅
```

## 📋 Complete .env Example

```env
# LegalMitra Configuration
AI_PROVIDER=grok
DEFAULT_AI_MODEL=grok-4-latest

# Your ACTUAL API Keys (replace placeholders!)
ANTHROPIC_API_KEY=sk-ant-api03-your_actual_anthropic_key
GOOGLE_GEMINI_API_KEY=AIzaSy-your_actual_gemini_key
GROK_API_KEY=xai-your_actual_grok_key

# Server Configuration
PORT=8888
MAX_TOKENS=4000
TEMPERATURE=0.3
```

## 🎯 Step-by-Step Checklist

- [ ] Opened `backend\.env` file
- [ ] Found `GROK_API_KEY=your_api_key_here`
- [ ] Replaced `your_api_key_here` with actual Grok key
- [ ] Checked no spaces around `=`
- [ ] Checked no quotes around key
- [ ] Saved the file
- [ ] Restarted the server
- [ ] Verified server shows: `✅ Grok (xAI) client initialized`

## 🐛 Still Getting Error?

1. **Double-check** the key is correct (copy-paste again)
2. **Verify** the key is active at https://console.x.ai/
3. **Check** you're using the right provider:
   - For Grok: `AI_PROVIDER=grok`
   - For Anthropic: `AI_PROVIDER=anthropic`
   - For Gemini: `AI_PROVIDER=gemini`
4. **Make sure** you saved the file
5. **Restart** the server after changes

---

**The key is: Replace placeholder text with your actual API keys!** 🔑










