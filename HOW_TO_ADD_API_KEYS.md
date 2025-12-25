# How to Add API Keys to LegalMitra

## Supported AI Providers

LegalMitra supports multiple AI providers:
- ✅ **OpenAI** (GPT-4, GPT-4o)
- ✅ **Anthropic** (Claude Sonnet, Claude Opus)
- ✅ **Google Gemini** (gemini-pro, gemini-1.5-pro)

## Step-by-Step: Adding API Keys

### 1. Open the .env file

The `.env` file is located at:
```
D:\LegalMitra\backend\.env
```

**To open it:**
- Navigate to `backend` folder
- Double-click `.env` file (opens in Notepad)
- OR right-click → Open with → Notepad

### 2. Edit the .env file

You can add **one or more** API keys. Here's the format:

```env
# LegalMitra Configuration

# Choose your AI provider: "openai", "anthropic", or "gemini"
AI_PROVIDER=anthropic

# AI Model to use
DEFAULT_AI_MODEL=claude-sonnet-4-20250514
# For OpenAI: gpt-4o, gpt-4, gpt-3.5-turbo
# For Anthropic: claude-sonnet-4-20250514, claude-opus-20240229
# For Gemini: gemini-pro, gemini-1.5-pro

# API Keys (add the ones you have)
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
GOOGLE_GEMINI_API_KEY=your_gemini_key_here

# Server Configuration
PORT=8888
HOST=0.0.0.0
DEBUG=True

# AI Model Settings
MAX_TOKENS=4000
TEMPERATURE=0.3
```

### 3. Example Configuration (Your Case)

Since you have **Anthropic** and **Google Gemini** keys, your `.env` should look like:

```env
# LegalMitra Configuration
AI_PROVIDER=anthropic
DEFAULT_AI_MODEL=claude-sonnet-4-20250514

# Your API Keys
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
GOOGLE_GEMINI_API_KEY=your-actual-gemini-key-here

# Server Configuration
PORT=8888
MAX_TOKENS=4000
TEMPERATURE=0.3
```

**OR** to use Gemini instead:

```env
AI_PROVIDER=gemini
DEFAULT_AI_MODEL=gemini-pro

ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
GOOGLE_GEMINI_API_KEY=your-actual-gemini-key-here

PORT=8888
MAX_TOKENS=4000
TEMPERATURE=0.3
```

### 4. Save the File

- Press `Ctrl+S` to save
- OR File → Save
- Make sure you save it as `.env` (not `.env.txt`)

### 5. Restart the Server

After adding/updating API keys:
1. Stop the server (Press `Ctrl+C` in the server window)
2. Start it again (Run `START_LEGALMITRA.vbs`)

## Important Notes

### ⚠️ Security
- **Never share** your `.env` file or API keys
- The `.env` file is already in `.gitignore` (won't be committed to git)
- Don't post your API keys online

### 🔑 Getting API Keys

**Anthropic (Claude):**
1. Go to: https://console.anthropic.com/
2. Sign up / Log in
3. Go to API Keys section
4. Create a new key
5. Copy and paste into `.env`

**Google Gemini:**
1. Go to: https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Create API key
4. Copy and paste into `.env`

**OpenAI (if you want to add later):**
1. Go to: https://platform.openai.com/api-keys
2. Sign up / Log in
3. Create new secret key
4. Copy and paste into `.env`

### 🔄 Switching Providers

To switch between providers, just change the `AI_PROVIDER` line:

```env
# To use Anthropic (Claude)
AI_PROVIDER=anthropic
DEFAULT_AI_MODEL=claude-sonnet-4-20250514

# To use Google Gemini
AI_PROVIDER=gemini
DEFAULT_AI_MODEL=gemini-pro

# To use OpenAI
AI_PROVIDER=openai
DEFAULT_AI_MODEL=gpt-4o
```

Then restart the server.

## Troubleshooting

### "API key not found" error
- Check the `.env` file path: `backend\.env`
- Make sure there are **no spaces** around the `=` sign
- Make sure the key doesn't have quotes (unless the key itself contains special characters)
- Verify you saved the file

### "Failed to initialize" error
- Check if the API key is correct
- Make sure the required package is installed (should auto-install, but check if needed)
- Verify the provider name is correct: `anthropic`, `gemini`, or `openai`

### Want to use multiple providers?
- You can add all keys to `.env`
- Change `AI_PROVIDER` to switch between them
- Restart the server after changing

## Current Configuration Check

After starting the server, you should see a message like:
```
✅ Anthropic client initialized
```
or
```
✅ Google Gemini client initialized
```

This confirms which provider is being used.

---

**Need help?** Check the server window for error messages - they usually tell you exactly what's wrong!










