# Fix: Grok API Error (Shows "OpenAI API error")

## 🔍 Why It Says "OpenAI API error"

**Grok uses OpenAI-compatible API**, so error messages mention "OpenAI" even when using Grok. This is normal!

The **real problem** is: Your `.env` file still has **placeholder text** instead of your actual API key.

## ✅ Quick Fix

### Step 1: Open Your .env File

**Location:** `D:\LegalMitra\backend\.env`

**Quick way:**
- Double-click `QUICK_ADD_KEYS.bat`
- OR double-click `CHECK_ENV_FILE.bat`

### Step 2: Check These Lines

Look for:
```env
AI_PROVIDER=grok
GROK_API_KEY=your_api_key_here
```

### Step 3: Fix Your Configuration

**Make sure you have:**

```env
# Use Grok as provider
AI_PROVIDER=grok
DEFAULT_AI_MODEL=grok-4-latest

# Your ACTUAL Grok API key (replace placeholder!)
GROK_API_KEY=xai-your_actual_grok_key_here

# Other keys (if you have them)
ANTHROPIC_API_KEY=your_actual_anthropic_key
GOOGLE_GEMINI_API_KEY=your_actual_gemini_key
```

### Step 4: Replace Placeholder Text

**Find this line:**
```env
GROK_API_KEY=your_api_key_here
```

**Replace with your ACTUAL Grok key:**
```env
GROK_API_KEY=xai-clgcA24VbrkEQVbpxHzQut1K6ATOMdTGekuay2G9aBXLXaJHwvdFSVzzSIfVdqCbiXZQYtBzZbsjVIq1
```

**Important:**
- ✅ No spaces: `GROK_API_KEY=key` (not `GROK_API_KEY = key`)
- ✅ No quotes: `GROK_API_KEY=key` (not `GROK_API_KEY="key"`)
- ✅ Full key: Copy the entire key from xAI console

### Step 5: Verify Provider Setting

Make sure you have:
```env
AI_PROVIDER=grok
```

**NOT:**
```env
AI_PROVIDER=openai  ❌ (Wrong if you want Grok)
```

### Step 6: Save and Restart

1. **Save** (`Ctrl+S`)
2. **Stop server** (`Ctrl+C`)
3. **Restart** (`START_LEGALMITRA.vbs`)

## 📋 Complete Example .env File

```env
# LegalMitra Configuration
# Using Grok (not OpenAI)
AI_PROVIDER=grok
DEFAULT_AI_MODEL=grok-4-latest

# Your API Keys (REPLACE placeholders with actual keys!)
GROK_API_KEY=xai-clgcA24VbrkEQVbpxHzQut1K6ATOMdTGekuay2G9aBXLXaJHwvdFSVzzSIfVdqCbiXZQYtBzZbsjVIq1
ANTHROPIC_API_KEY=sk-ant-api03-your_actual_key
GOOGLE_GEMINI_API_KEY=AIzaSy-your_actual_key

# Server Configuration
PORT=8888
MAX_TOKENS=4000
TEMPERATURE=0.3
```

## 🎯 Checklist

- [ ] Opened `backend\.env` file
- [ ] Set `AI_PROVIDER=grok`
- [ ] Replaced `GROK_API_KEY=your_api_key_here` with actual key
- [ ] Verified no spaces around `=`
- [ ] Verified no quotes around key
- [ ] Saved the file
- [ ] Restarted the server

## 🐛 Still Getting Error?

1. **Double-check** the key is correct (copy-paste again from https://console.x.ai/)
2. **Verify** the key is active (check xAI console)
3. **Make sure** `AI_PROVIDER=grok` (not `openai`)
4. **Check** you saved the file
5. **Restart** server after changes

## 💡 Why It Says "OpenAI API error"

Grok (xAI) uses OpenAI-compatible API format, so:
- Error messages say "OpenAI API error" (this is normal!)
- But you're actually using Grok
- The real issue is placeholder text in your `.env`

---

**Fix: Replace `your_api_key_here` with your actual Grok API key!** 🔑









