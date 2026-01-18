# Restart Server to Apply New Gemini API Key

## Quick Steps:

1. **Stop the current server:**
   - Find the terminal/command prompt where the server is running
   - Press `Ctrl + C` to stop it

2. **Restart the server:**
   ```bash
   cd backend
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8888 --reload
   ```

3. **Verify the new key is loaded:**
   - The server will reload automatically with `--reload` flag
   - Check the console for any errors
   - Try uploading a PDF to test OCR

## Alternative: If server is running in background

If you can't find the terminal, you can:
1. Close all Python processes
2. Restart the server using the command above

## What happens after restart:

✅ The new `GOOGLE_GEMINI_API_KEY` from `.env` will be loaded
✅ Settings cache will be cleared automatically
✅ PDF OCR will work with the new key
✅ Image processing will work with the new key

## Test it:

After restarting, try uploading a PDF document again. The OCR should now work with your new Gemini API key!



