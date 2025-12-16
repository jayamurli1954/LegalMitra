# Indian Legal AI Assistant - Quick Start Guide

## 📋 Overview

This project creates an AI-powered legal assistant that helps with Indian legal research, case law citations, and document drafting. Think of it as a **Junior Lawyer** assisting a Senior Advocate.

## 🎯 What This System Does

✅ **Legal Research**: Answers questions about Indian laws (GST, Income Tax, BNS, etc.)  
✅ **Case Law Search**: Finds relevant Supreme Court, High Court judgments  
✅ **Document Drafting**: Creates petitions, replies, legal notices  
✅ **Case Preparation**: Helps prepare arguments with precedents  
✅ **Act Interpretation**: Explains sections of various Acts

## 📁 Project Files You Have

1. **legal_assistant_system_prompt.md** - Complete system instructions
2. **implementation_guide.md** - Step-by-step coding guide
3. **legal_system_prompt.txt** - AI prompt to use in code
4. **README.md** (this file) - Quick start instructions

## 🚀 Quick Start (Simplest Approach)

### Option 1: Test with Claude/ChatGPT First (No Coding!)

**Step 1:** Open Claude.ai or ChatGPT

**Step 2:** Copy the content from `legal_system_prompt.txt`

**Step 3:** Paste it as a "Custom Instruction" or in the chat

**Step 4:** Ask legal questions like:
```
"What is the limitation period for filing a GST appeal?"
"Draft a reply to an income tax notice for Section 148 reassessment"
"Cite cases on arbitration clause interpretation under Section 7 of Arbitration Act"
```

**Step 5:** See if responses meet your requirements. This helps you understand what the final system will do!

### Option 2: Build Minimum Viable Product (MVP)

If you want to build it yourself, here's the **absolute minimum**:

#### Requirements:
- Python 3.8+
- OpenAI or Anthropic API key
- Basic terminal/command line knowledge

#### 5-Minute Setup:

```bash
# Step 1: Create project folder
mkdir legal-ai-assistant
cd legal-ai-assistant

# Step 2: Create virtual environment
python -m venv venv

# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Step 3: Install minimal dependencies
pip install openai python-dotenv

# Step 4: Create .env file (add your API key)
echo "OPENAI_API_KEY=your_key_here" > .env

# Step 5: Create simple script (see below)
```

**Create `legal_assistant.py`:**

```python
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load system prompt
with open("legal_system_prompt.txt", "r") as f:
    SYSTEM_PROMPT = f.read()

def ask_legal_question(question):
    """Ask a legal question"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question}
        ],
        temperature=0.3,  # Lower temperature for more consistent legal answers
        max_tokens=2000
    )
    return response.choices[0].message.content

# Example usage
if __name__ == "__main__":
    print("Legal AI Assistant - Ask a question (or 'quit' to exit)\n")
    
    while True:
        question = input("\nYour Question: ")
        if question.lower() in ['quit', 'exit', 'q']:
            break
        
        print("\n🔍 Researching...\n")
        answer = ask_legal_question(question)
        print(answer)
        print("\n" + "="*80)
```

**Run it:**
```bash
python legal_assistant.py
```

**Try questions like:**
- "What is Section 9 of CGST Act about?"
- "Limitation for consumer complaints under Consumer Protection Act 2019"
- "Draft a brief legal notice for breach of contract"

## 🏗️ Full System Architecture (For Production)

If you want a complete web application, follow the `implementation_guide.md` which includes:

```
Frontend (React)
     ↓
Backend API (FastAPI)
     ↓
AI Service (Claude/GPT)
     ↓
Vector Database (Case Law Search)
     ↓
MongoDB (Store Cases, Statutes)
```

## 📚 Next Steps Based on Your Skill Level

### Beginner (You are here)
1. ✅ Test with Claude.ai first (Option 1)
2. ✅ Run the simple Python script (Option 2)
3. Read FastAPI basics: https://fastapi.tiangolo.com/
4. Learn React basics: https://react.dev/learn

### Intermediate
1. Build basic FastAPI backend (Week 1-2)
2. Add MongoDB for storing case laws (Week 3)
3. Create simple React frontend (Week 4)
4. Connect frontend to backend (Week 5)

### Advanced
1. Implement vector database for semantic search
2. Add user authentication
3. Create document templates
4. Build citation validator
5. Add multi-lingual support

## 🔑 API Keys You'll Need

### For MVP (Choose one):
- **OpenAI**: https://platform.openai.com/api-keys (~$20 for testing)
- **Anthropic Claude**: https://console.anthropic.com/ (~$20 for testing)

### For Full System (Optional):
- **MongoDB Atlas**: https://www.mongodb.com/cloud/atlas (Free tier available)
- **Pinecone**: https://www.pinecone.io/ (Free tier: 1M vectors)

## 💡 Pro Tips for Beginners

1. **Start Small**: Don't try to build everything at once
2. **Test Frequently**: Test each component before moving to next
3. **Use Git**: Version control from day 1
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```
4. **Read Error Messages**: They tell you exactly what's wrong
5. **Ask for Help**: Use Claude/ChatGPT to debug errors

## 📖 Learning Path

### Week 1-2: Understand the System
- [ ] Test with Claude.ai (Option 1)
- [ ] Run simple Python script (Option 2)
- [ ] Understand how prompts work
- [ ] Read about Indian legal system basics

### Week 3-4: Backend Basics
- [ ] Learn FastAPI basics
- [ ] Create simple API endpoints
- [ ] Connect to MongoDB
- [ ] Test with Postman/Thunder Client

### Week 5-6: Frontend Basics
- [ ] Learn React basics
- [ ] Create simple form for queries
- [ ] Display AI responses
- [ ] Style with Material-UI

### Week 7-8: Integration
- [ ] Connect frontend to backend
- [ ] Add case law search
- [ ] Implement document drafting
- [ ] Test end-to-end

## 🎓 Resources

### Indian Legal System
- **India Code**: https://www.indiacode.nic.in/ (All Acts)
- **Supreme Court**: https://main.sci.gov.in/
- **SCC Online**: https://www.scconline.com/ (Case laws - paid)
- **Indian Kanoon**: https://indiankanoon.org/ (Free case laws)

### Programming
- **FastAPI Tutorial**: https://fastapi.tiangolo.com/tutorial/
- **React Tutorial**: https://react.dev/learn
- **MongoDB Tutorial**: https://www.mongodb.com/docs/
- **Python for Lawyers**: https://lawyerist.com/python-for-lawyers/

### AI/ML
- **OpenAI Cookbook**: https://cookbook.openai.com/
- **LangChain Docs**: https://python.langchain.com/docs/
- **Anthropic Claude Docs**: https://docs.anthropic.com/

## ⚠️ Important Legal Disclaimer

This system is a **tool for legal professionals**, not a replacement for lawyers. Always:

1. Verify all case law citations
2. Check for latest amendments
3. Consult senior counsel for critical matters
4. Review all AI-generated documents
5. Don't rely solely on AI for court appearances

## 🐛 Common Issues & Solutions

### "ModuleNotFoundError: No module named 'openai'"
```bash
pip install openai
```

### "API key is invalid"
- Check your .env file has correct key
- Make sure there are no extra spaces
- Verify key is active on OpenAI/Anthropic dashboard

### "Connection refused to MongoDB"
- Make sure MongoDB is running
- Check connection string in .env
- Use MongoDB Atlas (cloud) if local installation fails

### Frontend can't connect to backend
- Check if backend is running (http://localhost:8000)
- Verify CORS settings in FastAPI
- Check network/firewall settings

## 📞 Getting Help

1. **Claude/ChatGPT**: Ask for debugging help with error messages
2. **Stack Overflow**: Search for specific errors
3. **GitHub Issues**: Check similar projects
4. **FastAPI Discord**: https://discord.com/invite/VQjSZaeJmf

## 🎯 Success Metrics

Your MVP is successful when it can:
- ✅ Answer basic legal questions accurately
- ✅ Cite at least 3-4 relevant case laws
- ✅ Draft simple legal documents
- ✅ Explain sections of major Acts

## 🚀 Deployment (Future)

Once ready for production:
1. **Backend**: Deploy on AWS/GCP/Heroku
2. **Frontend**: Deploy on Vercel/Netlify
3. **Database**: MongoDB Atlas
4. **Domain**: Buy from GoDaddy/Namecheap
5. **SSL**: Use Let's Encrypt (free)

## 📝 Project Checklist

- [ ] Test with Claude.ai first
- [ ] Run simple Python script
- [ ] Setup development environment
- [ ] Build basic backend API
- [ ] Create simple frontend
- [ ] Connect to database
- [ ] Add case law search
- [ ] Implement document drafting
- [ ] Test with real legal queries
- [ ] Deploy to production

---

**Remember**: Rome wasn't built in a day! Start with the simple script, learn as you go, and gradually build towards the full system. You've got this! 💪

For detailed step-by-step coding instructions, refer to `implementation_guide.md`.
