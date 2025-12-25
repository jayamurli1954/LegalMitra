# Your LegalMitra Configuration

## ✅ Configured for Your Use Case

Your system is now configured to use:
1. **Anthropic API** (Primary/Default)
2. **Google Gemini API** (Alternative)
3. **Grok API** (Alternative)
4. ~~OpenAI~~ (Not used by default)

## 📝 Your .env File Configuration

Edit `backend\.env` file and add your API keys:

```env
# LegalMitra Configuration
# Primary Provider: Anthropic (Claude)
AI_PROVIDER=anthropic
DEFAULT_AI_MODEL=claude-sonnet-4-20250514

# Your API Keys
ANTHROPIC_API_KEY=your_anthropic_key_here
GOOGLE_GEMINI_API_KEY=your_gemini_key_here
GROK_API_KEY=your_grok_key_here

# Server Configuration
PORT=8888
HOST=0.0.0.0
DEBUG=True

# AI Model Settings
MAX_TOKENS=4000
TEMPERATURE=0.3
```

## 🔑 Getting Your API Keys

### Anthropic (Claude) - Primary
1. Go to: https://console.anthropic.com/
2. Sign up / Log in
3. Navigate to API Keys
4. Create new key
5. Copy and paste into `.env`

### Google Gemini
1. Go to: https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Create API key
4. Copy and paste into `.env`

### Grok (xAI)
1. Go to: https://console.x.ai/
2. Sign up / Log in (may require X/Twitter account)
3. Navigate to API Keys
4. Create new key
5. Copy and paste into `.env`

## 🔄 Switching Between Providers

To switch providers, change the `AI_PROVIDER` line in `.env`:

### Use Anthropic (Default)
```env
AI_PROVIDER=anthropic
DEFAULT_AI_MODEL=claude-sonnet-4-20250514
```

### Use Google Gemini
```env
AI_PROVIDER=gemini
DEFAULT_AI_MODEL=gemini-pro
```

### Use Grok
```env
AI_PROVIDER=grok
DEFAULT_AI_MODEL=grok-beta
```

Then restart the server.

## 📋 Supported Models

### Anthropic (Claude)
- `claude-sonnet-4-20250514` (Recommended)
- `claude-opus-20240229`
- `claude-3-5-sonnet-20241022`

### Google Gemini
- `gemini-pro` (Recommended)
- `gemini-1.5-pro`
- `gemini-1.5-flash`

### Grok (xAI)
- `grok-beta` (Recommended)
- `grok-2` (if available)

## 🚀 Quick Start

1. **Add your API keys** to `backend\.env`
2. **Save the file**
3. **Start the server**: Run `START_LEGALMITRA.vbs`
4. **Use the application**: Open `frontend\index.html`

## ⚙️ Default Settings

- **Provider**: Anthropic (Claude)
- **Model**: claude-sonnet-4-20250514
- **Port**: 8888
- **Max Tokens**: 4000
- **Temperature**: 0.3 (lower = more consistent legal answers)

## 💡 Tips

- **Anthropic** is set as default - best for legal research
- **Gemini** is good for quick responses
- **Grok** is useful for real-time information
- You can switch providers anytime by changing `.env` and restarting

## 🔒 Security

- Never share your `.env` file
- Keep your API keys secret
- The `.env` file is already in `.gitignore`

---

**Your system is ready!** Add your API keys and start using LegalMitra! ⚖️🤖










