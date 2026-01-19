# LegalMitra - Quick Start Guide

## 🚀 First Time Setup (One Time Only)

### Step 1: Create Desktop Shortcut
```
Double-click: create_desktop_shortcut.vbs
```
This creates a "LegalMitra" icon on your desktop.

---

## 🎯 Daily Usage (Every Time You Want to Use LegalMitra)

### Launch Application
```
Double-click: LegalMitra (desktop shortcut)
```

**What Happens**:
1. Backend server starts (port 8888)
2. Frontend server starts (port 3005)
3. Browser opens to http://localhost:3005

**Done!** Start using LegalMitra.

---

## 📋 Template Library (48 Templates!)

### Categories Available

1. **GST Templates** (10 templates)
   - Registration, Refund, Notices, Appeals, Cancellation, etc.

2. **Income Tax Templates** (5 templates)
   - TDS Returns, Appeals, Rectifications, etc.

3. **Corporate Templates** (8 templates)
   - Board Resolutions, ROC Filings, Director Appointments, etc.

4. **Contract Templates** (6 templates)
   - Employment, Consultancy, Vendor, Partnership, NDA, etc.

5. **Compliance Templates** (5 templates)
   - PF, ESI, GST Annual Returns, etc.

6. **Legal Notices** (6 templates)
   - Cease & Desist, Consumer Complaints, Payment Demands, etc.

7. **SEBI & Regulatory** (8 templates)
   - Various regulatory compliance templates

### Using Templates

1. Click "📋 Document Templates" on homepage
2. Select category from left sidebar
3. Choose template
4. Fill in the form fields
5. Click "Generate Document"
6. AI enhances the template with your details
7. Copy or download the result

---

## 🛠️ Adding More Templates

Templates are now organized in **separate files** for easy management!

### Location
```
backend/app/templates/categories/
├── gst_templates.py           (GST templates here)
├── income_tax_templates.py    (Income Tax templates here)
├── corporate_templates.py     (Corporate templates here)
├── contract_templates.py      (Contract templates here)
├── compliance_templates.py    (Compliance templates here)
└── legal_notice_templates.py  (Legal Notice templates here)
```

### How to Add

**Example: Add a new GST template**

1. **Open**: `backend/app/templates/categories/gst_templates.py`

2. **Add** to the list:
```python
{
    "id": "gst_your_template_id",
    "name": "Your Template Name",
    "category": "gst",
    "description": "What this template does",
    "applicable_for": ["CA", "Corporate"],
    "fields": [
        {
            "name": "field_name",
            "label": "Label for User",
            "type": "text",  # text, number, date, dropdown, multiline
            "required": True
        }
    ],
    "template_text": """Your template content here.
    Use {field_name} for variables.""",
    "tags": ["GST", "Tag1", "Tag2"],
    "ai_enhanced": True
}
```

3. **Restart backend**:
```bash
cd backend
python -m uvicorn app.main:app --port 8888 --reload
```

4. **Done!** Your template appears in the UI.

**See**: `HOW_TO_ADD_TEMPLATES.md` for detailed guide.

---

## 📊 URLs Reference

| Service | URL | Use For |
|---------|-----|---------|
| **Main App** | http://localhost:3005 | Using LegalMitra |
| **API Docs** | http://localhost:8888/docs | API documentation |
| **Cache Stats** | http://localhost:8888/api/v1/cache-stats | Monitor cache |
| **Template Summary** | http://localhost:8888/api/v1/templates/summary | Template count |

---

## 🔧 Troubleshooting

### Problem: Port already in use

**Check what's using the port**:
```bash
netstat -ano | findstr ":3005"
netstat -ano | findstr ":8888"
```

**Kill the process**:
```bash
taskkill /F /PID <PID>
```

### Problem: Templates not loading

**Check**:
1. ✅ Backend running (http://localhost:8888)
2. ✅ Using http://localhost:3005 (not file://)
3. ✅ No errors in browser console (F12)

**Test backend**:
```bash
curl http://localhost:8888/api/v1/templates/summary
```

### Problem: Shortcut doesn't work

**Check**:
1. ✅ Path in shortcut is correct
2. ✅ `start_legalmitra.bat` exists
3. ✅ You're in the right directory

**Fix**: Delete and recreate using `create_desktop_shortcut.vbs`

---

## 🎓 Features

### 1. Document Templates (48 templates)
- Professional legal/business documents
- AI-enhanced generation
- Categorized and searchable

### 2. Legal Research
- Search Indian law cases
- Google Custom Search integration
- Recent judgments sidebar

### 3. Legal News
- Latest legal news in sidebar
- Cached for performance

### 4. Smart Caching
- Reduces API calls
- Faster responses
- Quota management

---

## 📂 File Structure

```
LegalMitra/
├── backend/
│   ├── app/
│   │   ├── templates/
│   │   │   ├── categories/      (NEW - Modular templates!)
│   │   │   │   ├── gst_templates.py
│   │   │   │   ├── income_tax_templates.py
│   │   │   │   ├── corporate_templates.py
│   │   │   │   ├── contract_templates.py
│   │   │   │   ├── compliance_templates.py
│   │   │   │   └── legal_notice_templates.py
│   │   │   └── template_service.py
│   │   └── ...
│   └── ...
├── frontend/
│   └── index.html
├── start_legalmitra.bat           (Main startup script)
├── start_frontend.py              (Frontend server)
├── create_desktop_shortcut.vbs    (Create shortcut)
└── Documentation files (.md)
```

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | Project overview |
| `HOW_TO_RUN.md` | Detailed startup instructions |
| `HOW_TO_ADD_TEMPLATES.md` | Guide to adding templates |
| `TEMPLATE_REFACTORING_SUMMARY.md` | New modular structure explained |
| `CREATE_SHORTCUT_README.md` | Desktop shortcut guide |
| `PORT_CONFIGURATION.md` | Port setup (3005, 8888) |
| `TEMPLATE_COUNT_FIX.md` | Dynamic template count |
| `QUICK_START_GUIDE.md` | This file! |

---

## 💡 Tips

### Organize Your Workflow
1. **Morning**: Double-click desktop shortcut
2. **Work**: Use templates and research
3. **Evening**: Close terminal windows

### Keyboard Shortcuts
- **F12**: Open browser console (for debugging)
- **Ctrl+F5**: Hard refresh (clear cache)
- **Ctrl+C**: Stop server in terminal

### Best Practices
- Keep both terminal windows open while using
- Don't close windows until you're done
- Check backend terminal for errors
- Use appropriate template categories

---

## 🎯 Next Steps

1. ✅ Create desktop shortcut (first time only)
2. ✅ Double-click shortcut to launch
3. ✅ Try a few templates
4. ✅ Add custom templates if needed
5. ✅ Enjoy using LegalMitra!

---

## 📞 Need Help?

### Check Documentation
1. Read relevant .md files in project root
2. Check `HOW_TO_ADD_TEMPLATES.md` for template help
3. See `TEMPLATE_REFACTORING_SUMMARY.md` for structure

### Common Questions

**Q: How many templates are there?**
A: 48 templates across 7 categories

**Q: Can I add my own templates?**
A: Yes! Edit the category files in `backend/app/templates/categories/`

**Q: Do I need to restart after adding templates?**
A: Yes, restart the backend server

**Q: Where is the data stored?**
A: Templates in Python files, cache in memory, no database yet

---

## ⚡ Performance

### Cache System
- Google API results cached for 24 hours
- Template data loaded at startup
- Fast response times

### Quota Management
- Google Custom Search: 100 queries/day
- Cached results prevent quota exhaustion
- Auto-reset daily

---

## 🔄 Updates

### Template Library
- **Before**: 12 templates
- **After**: 48 templates (4x increase!)
- **Structure**: Modular and organized

### Recent Changes
- ✅ Refactored to modular structure
- ✅ Added 36 new templates
- ✅ Fixed PF members list field
- ✅ Created desktop shortcut
- ✅ Dynamic template count

---

**Version**: 2.0 (Modular Templates)
**Date**: January 19, 2026
**Status**: Ready to Use!

---

## 🚀 Launch Now!

```
👆 Double-click: LegalMitra (desktop shortcut)
```

**Happy Lawyering! ⚖️**
