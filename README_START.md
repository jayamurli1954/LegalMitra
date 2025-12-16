# LegalMitra - Quick Start Guide

## 🚀 One-Click Startup

### For Windows Users:

**Option 1: Double-click the batch file**
1. Double-click `START_LEGALMITRA.bat` on your desktop or in the project folder
2. The script will automatically:
   - Check Python installation
   - Create virtual environment
   - Install dependencies
   - Configure environment variables
   - Start the backend server

**Option 2: Run PowerShell script**
1. Right-click `START_LEGALMITRA.ps1`
2. Select "Run with PowerShell"
3. Follow the prompts

## 📋 Prerequisites

Before running, ensure you have:

1. **Python 3.8 or higher** installed
   - Download from: https://www.python.org/
   - During installation, check "Add Python to PATH"

2. **API Key** for AI service:
   - **OpenAI**: Get from https://platform.openai.com/api-keys
   - **Anthropic**: Get from https://console.anthropic.com/
   - (You'll be prompted to add this on first run)

## ⚙️ First Time Setup

1. Run `START_LEGALMITRA.bat`
2. On first run, it will create a `.env` file
3. Edit `backend\.env` and add your API key:
   ```
   OPENAI_API_KEY=your_key_here
   # OR
   ANTHROPIC_API_KEY=your_key_here
   ```
4. Save the file and run the script again

## 🌐 Accessing the Application

Once the server starts:

1. **Backend API**: http://localhost:8888
2. **API Documentation**: http://localhost:8888/docs
3. **Frontend**: Open `frontend\index.html` in your web browser

> **Note**: Port 8888 is used by default. You can change it in `backend\.env` if needed.

## 📖 Using LegalMitra

### Legal Research
- Ask questions about Indian laws
- Example: "What is the limitation period for GST appeal?"

### Document Drafting
- Draft legal notices, petitions, replies
- Provide facts, parties, legal grounds, and prayer

### Case Search
- Search for relevant case laws
- Filter by court, year, or domain

### Statute Search
- Look up specific acts and sections
- Example: "CGST Act 2017 Section 16"

## 🛠️ Manual Setup (Alternative)

If the one-click script doesn't work:

```bash
# 1. Navigate to backend
cd backend

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Configure environment
copy .env.example .env
# Edit .env and add your API key

# 6. Run server
python -m app.main
```

## ❓ Troubleshooting

### "Python is not recognized"
- Install Python and add it to PATH
- Restart terminal/command prompt after installation

### "API key error"
- Check `backend\.env` file
- Ensure API key is correct (no extra spaces)
- Verify key is active on OpenAI/Anthropic dashboard

### "Port already in use"
- Stop other applications using port 8888
- Or change PORT in `backend\.env` to any available port (e.g., 5000, 8889, 9999)

### "Module not found"
- Make sure virtual environment is activated
- Run: `pip install -r backend\requirements.txt`

## 📞 Support

For issues or questions:
1. Check the error message in the terminal
2. Verify all prerequisites are installed
3. Check the `backend\.env` configuration
4. Review the API documentation at http://localhost:8000/docs

## 🎯 Next Steps

1. **Test the API**: Visit http://localhost:8000/docs
2. **Try the Frontend**: Open `frontend\index.html`
3. **Ask Legal Questions**: Use any of the features
4. **Read Documentation**: Check the README files in the project

---

**Enjoy using LegalMitra! ⚖️🤖**

