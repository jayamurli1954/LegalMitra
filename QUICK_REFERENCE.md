# LegalMitra - Quick Reference Guide

## 🎯 What Changed?

### Before Enhancement
```
LegalMitra v1.0
├── Basic legal research (single AI model)
├── Advocate diary (case management)
└── Simple web interface
```

### After Enhancement
```
LegalMitra v2.0
├── Multi-Model AI (200+ models via OpenRouter)
├── 20+ Document Templates (CA/Corporate focus)
├── Smart Model Routing (auto cost optimization)
├── Cost Tracking Dashboard
├── Progressive Web App (installable)
├── Offline Support
└── Professional Branding
```

---

## 📁 Where to Find Everything

### Main Application Files

**Frontend (User Interface):**
```
D:\SanMitra_Tech\LegalMitra\frontend\

├── index.html              → Main research interface
├── templates.html          → Browse & use 20+ templates [NEW]
├── cost-dashboard.html     → Track spending & savings [NEW]
├── model-selector.html     → Choose AI models [NEW]
├── manifest.json           → PWA configuration [NEW]
├── service-worker.js       → Offline support [NEW]
└── pwa.js                  → Install prompt [NEW]
```

**Backend (API Server):**
```
D:\SanMitra_Tech\LegalMitra\backend\

├── app/services/
│   ├── openrouter_service.py    → 200+ AI models [NEW]
│   ├── smart_router.py          → Auto model selection [NEW]
│   └── cost_tracker.py          → Cost analytics [NEW]
│
├── app/templates/
│   └── template_service.py      → Template engine [NEW]
│
└── app/api/
    ├── templates.py             → Template API [NEW]
    ├── smart_routing.py         → Routing API [NEW]
    └── cost_tracking.py         → Cost API [NEW]
```

**Documentation:**
```
D:\SanMitra_Tech\LegalMitra\

├── ENHANCEMENTS_SUMMARY.md  → Complete feature list [THIS IS COMPREHENSIVE]
├── QUICK_REFERENCE.md       → This file (quick overview)
├── PWA_READY.md            → PWA testing guide
├── PWA_GUIDE.md            → PWA user manual
├── LOGO_USAGE_GUIDE.md     → Branding guidelines
└── GENERATE_ICONS.md       → Icon generation help
```

---

## 🚀 Quick Start Guide

### 1. Start the Application

**Start Backend:**
```bash
cd D:\SanMitra_Tech\LegalMitra\backend
python -m app.main
```
Backend runs at: `http://localhost:8888`

**Open Frontend:**
```bash
# Open in browser:
D:\SanMitra_Tech\LegalMitra\frontend\index.html
```

### 2. Access Features

**Legal Research:**
- URL: `frontend/index.html`
- Use: Ask legal questions, get AI-powered answers
- New: Choose from 200+ AI models

**Document Templates:**
- URL: `frontend/templates.html`
- Use: Generate CA/Corporate documents
- Categories: GST, Income Tax, Corporate, Compliance, Legal

**Cost Dashboard:**
- URL: `frontend/cost-dashboard.html`
- Use: Track spending, compare with VIDUR
- See: Daily trends, cost by model, savings percentage

**Model Selection:**
- URL: `frontend/model-selector.html`
- Use: Browse and select AI models manually
- Tiers: Budget, Balanced, Premium

---

## 📱 20+ Templates Available

### GST (5 Templates)
1. GST Registration Application (Form GST REG-01)
2. GST Annual Return (GSTR-9)
3. GST Refund Application (RFD-01)
4. GST Registration Cancellation (REG-16)
5. Reply to GST Notice

### Income Tax (5 Templates)
6. Tax Audit Report (Form 3CB-3CD)
7. Advance Tax Computation
8. TDS Return Filing Summary
9. Income Tax Appeal (Form 35)
10. Reply to Income Tax Notice

### Corporate (5 Templates)
11. Board Resolution (General Purpose)
12. Annual General Meeting Notice
13. Shareholders Agreement
14. Director Appointment Resolution
15. Share Transfer Resolution

### Compliance (3 Templates)
16. Statutory Compliance Certificate
17. Due Diligence Report
18. Financial Statement Certification

### Legal (2 Templates)
19. Non-Disclosure Agreement (NDA)
20. Legal Notice

**All templates include:**
- ✅ Dynamic form fields
- ✅ Field validation
- ✅ AI enhancement option
- ✅ Professional formatting

---

## 💰 Cost Comparison

### VIDUR Pricing
```
Subscription: $50-100/month (fixed)
Annual: $600-1,200/year

Features:
- Fixed number of queries
- Proprietary AI model
- Template library
- Web access only
```

### LegalMitra Pricing
```
Pay-per-use: $5-75/month (varies by usage)
Annual: $60-900/year (average $180)

Features:
- Unlimited queries (pay per use)
- 200+ AI models
- 20+ customizable templates
- PWA (installable, offline support)
```

### Savings Example
```
Typical CA Practitioner:
- VIDUR: $50/month = $600/year
- LegalMitra: $15/month = $180/year
- SAVINGS: $420/year (70% reduction)
```

---

## 🤖 AI Models Available

### Budget Tier (~$0.10-0.30 per 1M tokens)
- Google Gemini Flash 1.5
- Meta Llama 3.1 8B
- Mistral 7B
- **Use for:** Simple queries, definitions, basic questions

### Balanced Tier (~$0.25-1.00 per 1M tokens)
- Claude 3 Haiku
- GPT-3.5 Turbo
- Gemini Pro 1.5
- **Use for:** Case analysis, document review, moderate research

### Premium Tier (~$3.00-15.00 per 1M tokens)
- Claude 3.5 Sonnet (default)
- GPT-4 Turbo
- Claude 3 Opus
- Gemini Pro 1.5 Ultra
- **Use for:** Complex legal opinions, critical analysis, drafting

**Total Models:** 200+ available through OpenRouter

---

## 🎨 PWA Features

### Installation
- ✅ Install from browser (no app store)
- ✅ One-click install button
- ✅ Works on Android, iOS, Windows, Mac
- ✅ Custom branded icon with lawyer logo

### Offline Support
- ✅ Browse all 20+ templates offline
- ✅ View cost dashboard offline
- ✅ Cached responses available
- ✅ Background sync when online

### App Shortcuts (Long-press icon)
- Legal Research
- Document Templates
- Cost Dashboard
- Advocate Diary

### Native Features
- ✅ Standalone window (no browser UI)
- ✅ Full-screen mode
- ✅ Custom splash screen
- ✅ Automatic updates

---

## ⚙️ Configuration

### Environment Variables (.env)
```env
# AI Provider
AI_PROVIDER=openrouter

# OpenRouter API Key
OPENROUTER_API_KEY=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

# Default Model
OPENROUTER_MODEL=anthropic/claude-3.5-sonnet

# Server
BACKEND_PORT=8888
```

### Smart Routing Preferences
```python
# In API calls, set preference:
"user_preference": "balanced"  # Options: budget, balanced, premium
```

### Cost Limits
```python
# Set maximum cost per query:
"max_cost_per_query": 0.05  # $0.05 max per query
```

---

## 📊 API Endpoints

### Quick Reference
```
Templates:
  GET  /api/v1/templates/categories
  POST /api/v1/templates/fill

Smart Routing:
  POST /api/v1/smart-routing/analyze
  POST /api/v1/smart-routing/select-model

Cost Tracking:
  GET  /api/v1/cost-tracking/dashboard?days=30
  GET  /api/v1/cost-tracking/comparison?days=30

Models:
  GET  /api/v1/models/available
  GET  /api/v1/models/tiers

Research (Enhanced):
  POST /api/v1/research/query
  POST /api/v1/research/follow-up
```

**Full API Docs:** `http://localhost:8888/docs`

---

## 🔍 Common Tasks

### Use a Template
1. Open `frontend/templates.html`
2. Select category (e.g., "GST")
3. Click template (e.g., "GST Registration")
4. Fill in form fields
5. Toggle "Enhance with AI" (optional)
6. Click "Generate Document"
7. Copy or download result

### Check Your Costs
1. Open `frontend/cost-dashboard.html`
2. View total spend (daily, weekly, monthly)
3. See chart of spending trends
4. Check "vs VIDUR" comparison
5. Export data if needed

### Install as PWA
1. Open `frontend/index.html` in Chrome/Edge
2. Look for "Install App" button (bottom-right)
3. Click "Install"
4. App appears on desktop/home screen
5. Open like any native app

### Choose AI Model Manually
1. Open `frontend/model-selector.html`
2. Browse Budget/Balanced/Premium tiers
3. Compare costs per 1M tokens
4. Select preferred model
5. Model will be used for next query

### Switch to Automatic Routing
1. In research interface, leave model as "Auto"
2. Smart router analyzes query
3. Selects best model for cost/quality
4. See selection in response metadata

---

## 🐛 Troubleshooting

### Backend Not Running
```bash
# Check if running:
curl http://localhost:8888/

# If not, start it:
cd D:\SanMitra_Tech\LegalMitra\backend
python -m app.main
```

### PWA Install Button Not Showing
1. Use Chrome or Edge (best PWA support)
2. Ensure HTTPS or localhost
3. Clear cache (Ctrl+Shift+R)
4. Check DevTools → Application → Manifest

### Templates Not Loading
1. Check backend is running (port 8888)
2. Open browser console (F12) for errors
3. Verify API endpoint: `http://localhost:8888/api/v1/templates/categories`

### Cost Dashboard Shows "No Data"
1. Make at least one research query first
2. Cost tracking starts after first API call
3. Data stored in `backend/data/cost_tracking.json`

### Icons Not Showing in PWA
1. Verify icons exist: `frontend/icons/icon-*.png`
2. Run `generate_icons.py` if missing
3. Hard refresh browser (Ctrl+Shift+R)
4. Reinstall PWA

---

## 📈 Performance Tips

### Reduce Costs
1. Use "balanced" preference (default)
2. Let smart routing auto-select models
3. Set max cost per query limit
4. Use budget tier for simple questions

### Improve Speed
1. Install as PWA (caching enabled)
2. Use offline mode for templates
3. Choose faster models (Gemini Flash)
4. Enable service worker caching

### Best Practices
1. Review cost dashboard weekly
2. Use templates instead of writing from scratch
3. Let AI enhance templates (better quality)
4. Install PWA on mobile for on-the-go access

---

## 📞 Getting Help

### Documentation Files
- **ENHANCEMENTS_SUMMARY.md** → Complete feature documentation
- **PWA_READY.md** → PWA testing checklist
- **PWA_GUIDE.md** → PWA user manual
- **LOGO_USAGE_GUIDE.md** → Branding guidelines

### API Documentation
- Swagger UI: `http://localhost:8888/docs`
- ReDoc: `http://localhost:8888/redoc`

### Quick Tests
```bash
# Test backend:
curl http://localhost:8888/

# Test templates API:
curl http://localhost:8888/api/v1/templates/categories

# Test cost tracking:
curl http://localhost:8888/api/v1/cost-tracking/dashboard?days=7
```

---

## ✅ Feature Checklist

### Completed Features
- ✅ OpenRouter integration (200+ models)
- ✅ Template system (20+ templates)
- ✅ Smart model routing
- ✅ Cost tracking dashboard
- ✅ PWA with offline support
- ✅ Professional branding with custom icons
- ✅ API documentation
- ✅ User guides

### Ready for Production
- ✅ All features tested and working
- ✅ Documentation complete
- ✅ Icons generated
- ✅ PWA installable
- ✅ Cost optimization active

---

## 🎯 Next Steps

### For Testing
1. Install PWA on your phone
2. Try 5 different templates
3. Check cost dashboard after 1 week
4. Compare savings with VIDUR pricing

### For Production
1. Get SSL certificate (HTTPS required for PWA)
2. Deploy backend to server
3. Update manifest.json with production URL
4. Test on multiple devices
5. Share with beta users

### For Marketing
1. Highlight 70-90% cost savings vs VIDUR
2. Showcase 200+ AI model options
3. Demo template system for CA professionals
4. Show PWA mobile installation

---

## 💡 Pro Tips

### Cost Optimization
- Use "balanced" mode for 80% of queries
- Switch to "premium" only for critical work
- Review cost dashboard weekly
- Set alerts for spending limits

### Template Efficiency
- Save frequently used templates
- Use AI enhancement for professional output
- Customize templates for your practice
- Share templates with team members

### PWA Advantages
- Install on all devices (phone, tablet, desktop)
- Works offline during client meetings
- Updates automatically (no manual downloads)
- Professional appearance (custom icon)

---

**LegalMitra v2.0 - Your AI-Powered Legal Assistant**

*For detailed documentation, see: ENHANCEMENTS_SUMMARY.md*
