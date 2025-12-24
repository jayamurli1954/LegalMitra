# What to Do After "Application Startup Complete"

Once you see "Application startup complete" or the server starts running, follow these steps:

## ✅ Your Backend is Now Running!

The LegalMitra API server is active and ready to use.

## 🌐 Access the Application

### Option 1: Use the Web Frontend (Easiest)

1. **Open the frontend file:**
   - Navigate to: `D:\LegalMitra\frontend\`
   - Double-click: `index.html`
   - It will open in your default web browser

2. **Start using LegalMitra:**
   - **Legal Research** tab: Ask legal questions
   - **Document Drafting** tab: Create legal documents
   - **Case Search** tab: Search for case laws
   - **Statute Search** tab: Look up acts and sections

### Option 2: Use API Documentation (Advanced)

1. **Open your web browser**
2. **Go to:** http://localhost:8888/docs
3. This opens the interactive API documentation (Swagger UI)
4. You can test the API directly from here

### Option 3: Use API Directly (Programmers)

Use any HTTP client (Postman, curl, Python requests) to call:
- Base URL: `http://localhost:8888/api/v1`
- Endpoints:
  - `POST /api/v1/legal-research`
  - `POST /api/v1/draft-document`
  - `POST /api/v1/search-cases`
  - `POST /api/v1/search-statute`

## 🎯 Quick Examples

### Example 1: Ask a Legal Question

In the frontend (index.html):
1. Go to **Legal Research** tab
2. Type: "What is the limitation period for filing a GST appeal?"
3. Click **🔍 Research**
4. Wait for the AI response

### Example 2: Draft a Legal Notice

In the frontend:
1. Go to **Document Drafting** tab
2. Fill in:
   - Document Type: "legal notice"
   - Facts: "Client has not paid invoice of Rs. 10 lakhs"
   - Parties: `{"sender": "ABC Company", "recipient": "XYZ Ltd"}`
   - Legal Grounds: "Breach of contract"
   - Prayer: "Payment of Rs. 10 lakhs within 15 days"
3. Click **📝 Draft Document**
4. The AI will generate the document

### Example 3: Search for Cases

1. Go to **Case Search** tab
2. Type: "arbitration clause interpretation"
3. Optionally add: Court: "Supreme Court"
4. Click **🔎 Search Cases**

### Example 4: Look Up a Statute

1. Go to **Statute Search** tab
2. Act Name: "CGST Act 2017"
3. Section: "16" (optional)
4. Click **📚 Search Statute**

## 📋 Important Notes

### Keep the Server Running
- **Don't close** the command window where the server is running
- The window title should say "LegalMitra - AI Legal Assistant"
- If you close it, the server stops and you'll need to restart

### To Stop the Server
- Press **Ctrl+C** in the command window
- Or simply close the command window

### To Restart Later
- Just double-click `START_LEGALMITRA.vbs` again
- Or use `START_LEGALMITRA_SIMPLE.bat`

## 🐛 Troubleshooting

### "Connection error" in frontend
- Make sure the server is still running
- Check the URL is: http://localhost:8888
- Verify port 8888 is not blocked by firewall

### Server stops unexpectedly
- Check the command window for error messages
- Verify your API key is correct in `backend\.env`
- Make sure Python is properly installed

### API key error
- Edit `backend\.env` file
- Verify: `ANTHROPIC_API_KEY=your_actual_key_here`
- Restart the server after changing .env

## 📚 More Information

- **API Documentation**: http://localhost:8888/docs
- **ReDoc Documentation**: http://localhost:8888/redoc
- **Health Check**: http://localhost:8888/health

## 🎉 You're All Set!

Your LegalMitra AI Assistant is ready to use. Start asking legal questions or drafting documents!

---

**Remember**: Keep the server window open while using the application!









