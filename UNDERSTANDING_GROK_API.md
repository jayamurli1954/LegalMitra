# Understanding the Grok API Curl Command

## What is that curl command?

The curl command you saw is just a **test/example** from Grok API documentation. It shows how to make a direct API call.

**You DON'T need to run this!** LegalMitra handles everything automatically.

## What the command does:

```bash
curl https://api.x.ai/v1/chat/completions \
    -H "Authorization: Bearer YOUR_API_KEY" \
    -d '{...}'
```

This is a **manual test** that:
- Calls Grok API directly
- Sends a test message
- Gets a response

## ✅ What YOU need to do:

### Step 1: Add Your Grok API Key to .env

**IMPORTANT:** If you've shared your API key publicly (like in this conversation), **create a new one immediately!**

1. **Go to:** https://console.x.ai/
2. **Revoke the old key** (if possible)
3. **Create a NEW API key**
4. **Add it to your .env file:**

```env
GROK_API_KEY=your_new_grok_api_key_here
```

### Step 2: That's It!

LegalMitra will automatically:
- ✅ Use your Grok API key from .env
- ✅ Format the API requests correctly
- ✅ Handle authentication
- ✅ Process responses

You **don't need to run any curl commands** - the system does it all!

## 🔒 Security Warning

If you've shared your API key:
1. **Create a new key** at https://console.x.ai/
2. **Delete/revoke the old key** if possible
3. **Use the new key** in your .env file
4. **Never share API keys publicly**

## 📝 Your .env File Should Have:

```env
# LegalMitra Configuration
AI_PROVIDER=anthropic
DEFAULT_AI_MODEL=claude-sonnet-4-20250514

# Your API Keys
ANTHROPIC_API_KEY=your_anthropic_key
GOOGLE_GEMINI_API_KEY=your_gemini_key
GROK_API_KEY=your_new_grok_key_here

# Server Configuration
PORT=8888
```

## 🔄 To Use Grok Instead of Anthropic:

Change in `.env`:
```env
AI_PROVIDER=grok
DEFAULT_AI_MODEL=grok-4-latest
```

Then restart the server.

## Summary

- ❌ **Don't run** the curl command
- ✅ **Just add** your API key to `.env`
- ✅ **LegalMitra handles** everything automatically
- 🔒 **Create new key** if you shared yours

That's all you need to do! 🎉









