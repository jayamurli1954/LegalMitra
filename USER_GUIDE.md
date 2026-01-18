# LegalMitra - Simple User Guide

**For Non-Technical Users**

---

## 🏠 How to Navigate LegalMitra

### Main Page (Home)
**Location:** `index.html` (opens when you start)

**You'll see 5 tabs at the top:**
1. **Legal Research** - Ask legal questions
2. **Document Drafting** - Create legal documents
3. **Case Search** - Find case laws
4. **Statute Search** - Search Indian laws
5. **📔 Advocate Diary** - Manage your cases

---

## 🎯 How to Access New Features

### Method 1: Direct Links (Easiest)

**Open these files in your browser:**

1. **Document Templates** (20+ templates)
   - File: `D:\SanMitra_Tech\LegalMitra\frontend\templates.html`
   - Double-click to open in browser

2. **Cost Dashboard** (track spending)
   - File: `D:\SanMitra_Tech\LegalMitra\frontend\cost-dashboard.html`
   - Double-click to open in browser

3. **AI Model Selector** (choose AI model)
   - File: `D:\SanMitra_Tech\LegalMitra\frontend\model-selector.html`
   - Double-click to open in browser

### Method 2: Create Desktop Shortcuts

**For easy access, create shortcuts:**

1. Right-click on `templates.html`
2. Select "Create shortcut"
3. Drag shortcut to Desktop
4. Rename to "LegalMitra Templates"

Repeat for other pages!

---

## 📋 Feature Guide

### 1. Document Templates (NEW)

**What it does:** Generate professional documents instantly

**How to use:**
1. Open `templates.html`
2. Click a category:
   - **GST** - GST registration, returns, notices
   - **Income Tax** - Tax audits, TDS, appeals
   - **Corporate** - Board resolutions, AGM notices
   - **Compliance** - Certificates, reports
   - **Legal** - NDAs, legal notices
3. Select a template
4. Fill in the form fields
5. Toggle "Enhance with AI" (recommended)
6. Click "Generate Document"
7. Copy or download the result

**Example:**
```
Need GST Registration form?
→ Click "GST"
→ Select "GST Registration (Form REG-01)"
→ Fill: Business name, PAN, Address
→ Click Generate
→ Done in 30 seconds!
```

---

### 2. Cost Dashboard (NEW)

**What it does:** Shows how much you're spending on AI

**How to use:**
1. Open `cost-dashboard.html`
2. Select time period:
   - Last 7 Days
   - Last 30 Days
   - Last 90 Days
3. View your spending
4. See savings vs VIDUR (competitor)

**What you'll see:**
- 💵 Total spend
- 📊 Daily spending chart
- 🥧 Cost by AI model
- 💰 Savings (usually 70-90% vs VIDUR)

**Note:** If spinning, it means no queries made yet. Make a research query first!

---

### 3. AI Model Selector (NEW)

**What it does:** Choose which AI model to use

**How to use:**
1. Open `model-selector.html`
2. Browse three tiers:
   - **Budget** - Cheapest (~$0.10 per 1M words)
     - Gemini Flash, Llama 3.1 8B
   - **Balanced** - Good quality (~$0.25 per 1M words)
     - Claude Haiku, GPT-3.5
   - **Premium** - Best quality (~$3.00 per 1M words)
     - Claude Sonnet, GPT-4
3. Click on a model to select it
4. Use for your next query

**Tip:** Leave on "Auto" to let smart routing choose the best model for you!

---

### 4. Legal Research (Existing)

**How to use:**
1. Open `index.html`
2. Click "Legal Research" tab
3. Type your question in the box
4. Select AI model (or leave as "Auto")
5. Click "Submit Query"
6. Read the answer

**Example questions:**
- "What is the limitation period for GST appeals?"
- "Explain Section 43B of Income Tax Act"
- "How to register a private limited company?"

---

### 5. Document Drafting (Existing)

**How to use:**
1. Open `index.html`
2. Click "Document Drafting" tab
3. Select document type
4. Fill in details
5. Click "Generate"

---

### 6. Case Search (Existing)

**How to use:**
1. Open `index.html`
2. Click "Case Search" tab
3. Enter keywords
4. Select court (Supreme Court, High Court, etc.)
5. Click "Search"
6. View case summaries

---

## 🚀 Quick Start for First-Time Users

### Step 1: Start the Backend (One Time)
```
1. Open Command Prompt
2. Type: cd D:\SanMitra_Tech\LegalMitra\backend
3. Type: python -m app.main
4. Wait for "Uvicorn running on http://127.0.0.1:8888"
5. Keep this window open
```

### Step 2: Open the App
```
1. Open File Explorer
2. Go to: D:\SanMitra_Tech\LegalMitra\frontend
3. Double-click: index.html
4. Browser opens with LegalMitra
```

### Step 3: Try Your First Query
```
1. Type: "What is Section 9 of CGST Act?"
2. Click "Submit Query"
3. Get your answer in 5 seconds!
```

### Step 4: Try Templates
```
1. Double-click: templates.html
2. Click "GST"
3. Select "GST Registration"
4. Fill the form
5. Generate document
```

---

## 📍 Where is Everything?

### All Files Location
```
D:\SanMitra_Tech\LegalMitra\frontend\
```

### Quick Access List

| Feature | File Name | What it Does |
|---------|-----------|--------------|
| Main App | index.html | Legal research, drafting, case search |
| Templates | templates.html | 20+ document templates |
| Cost Dashboard | cost-dashboard.html | Track AI spending |
| Model Selector | model-selector.html | Choose AI model |
| Advocate Diary | diary.html | Case management |

---

## 💡 Tips for Non-Technical Users

### Tip 1: Bookmark Your Favorites
```
1. Open the page (e.g., templates.html)
2. Press Ctrl+D (bookmark)
3. Access anytime from bookmarks!
```

### Tip 2: Create Desktop Shortcuts
```
1. Right-click on file (e.g., templates.html)
2. "Create shortcut"
3. Drag to Desktop
4. Rename to something easy (e.g., "Legal Templates")
```

### Tip 3: Use Auto Mode
```
Always leave AI model as "Auto"
→ Smart routing picks the best model
→ Saves 60-80% on costs
→ No thinking required!
```

### Tip 4: First Query Costs Might Be Zero
```
Some models have free tiers
→ Your first queries might be free
→ Check cost dashboard to monitor spending
```

---

## 🎓 Common Tasks

### Generate a GST Registration Form
```
1. Open templates.html
2. Click "GST Templates"
3. Select "GST Registration (Form REG-01)"
4. Fill:
   - Legal Name: Your company name
   - Trade Name: Your business name
   - PAN: Your PAN number
   - State: Select your state
   - Business Type: Select type
5. Toggle "Enhance with AI" ON
6. Click "Generate Document"
7. Copy the output
8. Done!
```

### Check How Much You've Spent
```
1. Open cost-dashboard.html
2. Click "Last 30 Days"
3. See total spend
4. Compare with VIDUR (usually 70-90% cheaper!)
```

### Ask a Legal Question
```
1. Open index.html
2. Make sure "Legal Research" tab is selected
3. Type your question
4. Leave model as "Auto"
5. Click "Submit Query"
6. Read answer
7. Check cost at the bottom
```

### Create a Board Resolution
```
1. Open templates.html
2. Click "Corporate Templates"
3. Select "Board Resolution (General Purpose)"
4. Fill in:
   - Company Name
   - Resolution Date
   - Resolution Details
   - Directors Present
5. Click "Generate Document"
6. Done!
```

---

## ❓ Troubleshooting

### Cost Dashboard is Spinning
**Problem:** Shows "Loading dashboard..." forever

**Solution:**
- You haven't made any queries yet
- Go to index.html
- Make at least one research query
- Come back to cost dashboard
- Data will now show!

### Page Says "Backend Not Running"
**Problem:** Can't connect to backend

**Solution:**
1. Open Command Prompt
2. Go to: cd D:\SanMitra_Tech\LegalMitra\backend
3. Run: python -m app.main
4. Keep window open
5. Refresh browser page

### Can't Find Templates Page
**Problem:** Don't know where templates.html is

**Solution:**
1. Open File Explorer
2. Navigate to: D:\SanMitra_Tech\LegalMitra\frontend\
3. Look for: templates.html
4. Double-click to open
5. Bookmark it! (Ctrl+D)

### AI Model Selector Shows Limited Models
**Problem:** Only see 3-4 models, not 200+

**Solution:**
- Need backend running
- The 200+ models load from backend API
- Make sure backend is started
- Refresh the page

---

## 📱 Mobile Access (PWA)

### Install as App on Your Phone
```
1. Open index.html on mobile browser
2. Look for "Install App" button
3. Tap it
4. Confirm installation
5. LegalMitra icon appears on home screen
6. Works like native app!
7. Even works offline!
```

---

## 💰 Cost Guide

### How Much Does It Cost?

**Pay-per-use model:**
- Simple questions: $0.001 - $0.01 (less than 1 rupee!)
- Medium questions: $0.01 - $0.05 (4 rupees)
- Complex questions: $0.05 - $0.15 (12 rupees)

**Typical monthly cost:**
- Light user (5 queries/day): ~$5/month (₹400)
- Regular user (10 queries/day): ~$10/month (₹800)
- Heavy user (20 queries/day): ~$20/month (₹1,600)

**Compare with VIDUR:**
- VIDUR: $50-100/month (₹4,000-8,000)
- LegalMitra: $5-20/month (₹400-1,600)
- **Savings: 70-90%!**

---

## ✅ Quick Reference Card

**Print this and keep on your desk:**

```
┌─────────────────────────────────────────────┐
│    LegalMitra - Quick Reference Card        │
├─────────────────────────────────────────────┤
│                                             │
│  🏠 HOME                                     │
│  D:\...\frontend\index.html                 │
│                                             │
│  📋 TEMPLATES (NEW!)                        │
│  D:\...\frontend\templates.html             │
│  → 20+ documents ready to generate          │
│                                             │
│  💰 COST DASHBOARD (NEW!)                   │
│  D:\...\frontend\cost-dashboard.html        │
│  → Track spending, compare with VIDUR       │
│                                             │
│  🤖 AI MODELS (NEW!)                        │
│  D:\...\frontend\model-selector.html        │
│  → Choose from 200+ AI models               │
│                                             │
│  📔 ADVOCATE DIARY                          │
│  D:\...\frontend\diary.html                 │
│  → Manage cases and clients                 │
│                                             │
│  ⚙️ START BACKEND                           │
│  cd D:\...\backend                          │
│  python -m app.main                         │
│  → Run this first!                          │
│                                             │
└─────────────────────────────────────────────┘
```

---

## 🎉 You're Ready!

**Everything you need:**
- ✅ Main app for research
- ✅ 20+ templates ready to use
- ✅ Cost tracking dashboard
- ✅ 200+ AI models available
- ✅ Simple file navigation

**Start with:**
1. Open `index.html` → Try a question
2. Open `templates.html` → Generate a document
3. Open `cost-dashboard.html` → See your savings!

**Need help?**
→ Read this guide again
→ All files are in: `D:\SanMitra_Tech\LegalMitra\frontend\`

---

**Welcome to LegalMitra! 🎊**

*Making legal work easier, one query at a time.*
