# Quick Guide: Update Your .env File with Gemini Support

Since you already have the .env file set up, here's how to add Google Gemini:

## Quick Steps

1. **Open:** `D:\LegalMitra\backend\.env`

2. **Add this line** (if not already there):
   ```env
   GOOGLE_GEMINI_API_KEY=your_actual_gemini_key_here
   ```

3. **Your .env should now have:**
   ```env
   AI_PROVIDER=anthropic
   ANTHROPIC_API_KEY=your_anthropic_key
   GOOGLE_GEMINI_API_KEY=your_gemini_key
   PORT=8888
   ```

4. **Save the file**

5. **Restart the server** (Stop with Ctrl+C, then run START_LEGALMITRA.vbs again)

## To Switch to Gemini

Just change:
```env
AI_PROVIDER=gemini
DEFAULT_AI_MODEL=gemini-pro
```

Then restart the server.

That's it! 🎉










