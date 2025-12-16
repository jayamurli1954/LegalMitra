# How to Add Google Gemini and Grok API Keys to .env File

## 📝 Step-by-Step Instructions

### Step 1: Open the .env File

**Location:** `D:\LegalMitra\backend\.env`

**Ways to open it:**
1. **Navigate manually:**
   - Open File Explorer
   - Go to: `D:\LegalMitra\backend\`
   - Find `.env` file
   - Double-click to open in Notepad

2. **From Command Prompt:**
   - Press `Win + R`
   - Type: `notepad D:\LegalMitra\backend\.env`
   - Press Enter

3. **Quick way:**
   - Right-click on `backend` folder
   - Select "Open in Terminal" or "Open PowerShell here"
   - Type: `notepad .env`
   - Press Enter

### Step 2: Edit the .env File

Your `.env` file should look like this:

```env
# LegalMitra Configuration
AI_PROVIDER=anthropic
DEFAULT_AI_MODEL=claude-sonnet-4-20250514

# Your API Keys
ANTHROPIC_API_KEY=your_anthropic_key_here
GOOGLE_GEMINI_API_KEY=your_gemini_key_here
GROK_API_KEY=your_grok_key_here

# Server Configuration
PORT=8888
MAX_TOKENS=4000
TEMPERATURE=0.3
```

### Step 3: Replace the Placeholder Values

**For Google Gemini:**
- Find the line: `GOOGLE_GEMINI_API_KEY=your_gemini_key_here`
- Replace `your_gemini_key_here` with your actual Gemini API key
- Example: `GOOGLE_GEMINI_API_KEY=AIzaSyAbc123xyz...`

**For Grok:**
- Find the line: `GROK_API_KEY=your_grok_key_here`
- Replace `your_grok_key_here` with your actual Grok API key
- Example: `GROK_API_KEY=xai-abc123xyz...`

### Step 4: Save the File

- Press `Ctrl + S` to save
- OR click File → Save
- Make sure it saves as `.env` (not `.env.txt`)

## 🔑 Getting Your API Keys

### Google Gemini API Key

1. **Go to:** https://makersuite.google.com/app/apikey
   OR
   https://aistudio.google.com/app/apikey

2. **Sign in** with your Google account

3. **Click** "Create API Key" or "Get API Key"

4. **Copy** the API key (it starts with `AIza...`)

5. **Paste** it into `.env` file after `GOOGLE_GEMINI_API_KEY=`

### Grok (xAI) API Key

1. **Go to:** https://console.x.ai/

2. **Sign up / Log in**
   - You may need an X (Twitter) account
   - Or create a new xAI account

3. **Navigate to API Keys** section

4. **Create a new API key**

5. **Copy** the API key (it starts with `xai-...`)

6. **Paste** it into `.env` file after `GROK_API_KEY=`

## ✅ Example of Correct .env File

```env
# LegalMitra Configuration
AI_PROVIDER=anthropic
DEFAULT_AI_MODEL=claude-sonnet-4-20250514

# Your API Keys
ANTHROPIC_API_KEY=sk-ant-api03-abc123xyz...
GOOGLE_GEMINI_API_KEY=AIzaSyAbc123xyz456...
GROK_API_KEY=xai-abc123xyz456...

# Server Configuration
PORT=8888
MAX_TOKENS=4000
TEMPERATURE=0.3
```

## ⚠️ Important Notes

### DO:
- ✅ Keep the `=` sign (no spaces around it)
- ✅ Put the key directly after `=` (no quotes needed)
- ✅ Save the file after editing
- ✅ Keep your keys secret - never share them

### DON'T:
- ❌ Don't add spaces: `GOOGLE_GEMINI_API_KEY = key` (WRONG)
- ❌ Don't add quotes: `GOOGLE_GEMINI_API_KEY="key"` (WRONG)
- ❌ Don't leave extra spaces at the end
- ❌ Don't commit `.env` to git (already in .gitignore)

## 🔍 Verify Your Keys Are Correct

After saving, check:
1. No spaces around `=`
2. Keys are on separate lines
3. No extra characters
4. File saved as `.env` (not `.env.txt`)

## 🚀 After Adding Keys

1. **Save** the `.env` file
2. **Restart** the server:
   - Stop current server (Press `Ctrl+C`)
   - Run `START_LEGALMITRA.vbs` again
3. **Check** the server window - you should see:
   ```
   ✅ Anthropic client initialized
   ```
   (This confirms the server read your keys)

## 🐛 Troubleshooting

### "API key not found" error
- Check the `.env` file path: `backend\.env`
- Make sure there are **no spaces** around `=`
- Verify you saved the file
- Check the key doesn't have extra characters

### "Failed to initialize" error
- Verify the API key is correct
- Check if you copied the entire key
- Make sure the key is active (not expired/revoked)

### Keys not working
- Double-check you copied the complete key
- Verify the key is active in the provider's dashboard
- Make sure there are no hidden characters

## 📋 Quick Checklist

- [ ] Opened `backend\.env` file
- [ ] Added `GOOGLE_GEMINI_API_KEY=your_actual_key`
- [ ] Added `GROK_API_KEY=your_actual_key`
- [ ] No spaces around `=`
- [ ] Saved the file
- [ ] Restarted the server

---

**That's it!** Your API keys are now configured. 🎉








