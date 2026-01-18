# LegalMitra - System Architecture

## 🏗️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER DEVICES                             │
│  📱 Android  │  📱 iOS  │  💻 Windows  │  💻 Mac  │  🌐 Browser │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           │ HTTPS
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PROGRESSIVE WEB APP (PWA)                     │
│  ┌──────────────┬──────────────┬──────────────┬──────────────┐ │
│  │   index.html │ templates.   │ cost-dash.   │ model-sel.   │ │
│  │   (Research) │ html         │ html         │ html         │ │
│  └──────────────┴──────────────┴──────────────┴──────────────┘ │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Service Worker (Offline Support + Caching)              │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  PWA.js (Install Prompt + Update Notifications)          │  │
│  └──────────────────────────────────────────────────────────┘  │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           │ REST API (JSON)
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FASTAPI BACKEND (Python)                      │
│                     http://localhost:8888                        │
│                                                                  │
│  ┌────────────────────── API ROUTES ──────────────────────────┐ │
│  │                                                             │ │
│  │  /api/v1/research/*      → Legal Research (Enhanced)       │ │
│  │  /api/v1/templates/*     → Template System [NEW]           │ │
│  │  /api/v1/smart-routing/* → Smart Model Router [NEW]        │ │
│  │  /api/v1/cost-tracking/* → Cost Analytics [NEW]            │ │
│  │  /api/v1/models/*        → Model Selection [NEW]           │ │
│  │  /api/v1/diary/*         → Advocate Diary (Existing)       │ │
│  │                                                             │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌────────────────────── SERVICES ────────────────────────────┐ │
│  │                                                             │ │
│  │  OpenRouterService   → 200+ AI Models API [NEW]            │ │
│  │  SmartRouter         → Query Analysis + Model Selection    │ │
│  │  CostTracker         → Usage Logging + Analytics           │ │
│  │  TemplateService     → Template Management + AI Enhance    │ │
│  │  ResearchService     → Legal Research (Existing)           │ │
│  │                                                             │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌────────────────────── DATA STORAGE ─────────────────────────┐│
│  │                                                             │ │
│  │  SQLite Database     → Advocate Diary (Cases, Clients)     │ │
│  │  cost_tracking.json  → Cost Analytics Data [NEW]           │ │
│  │  .env                → API Keys + Configuration            │ │
│  │                                                             │ │
│  └─────────────────────────────────────────────────────────────┘ │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           │ HTTPS API Calls
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    EXTERNAL AI SERVICES                          │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              OpenRouter (https://openrouter.ai)           │  │
│  │                                                           │  │
│  │  Routes to 200+ AI Models:                               │  │
│  │  ├─ OpenAI (GPT-4, GPT-3.5)                              │  │
│  │  ├─ Anthropic (Claude 3.5 Sonnet, Opus, Haiku)           │  │
│  │  ├─ Google (Gemini Pro, Flash)                           │  │
│  │  ├─ Meta (Llama 3.1 8B, 70B, 405B)                       │  │
│  │  ├─ Mistral (Mistral 7B, Mixtral)                        │  │
│  │  └─ 190+ Other Models                                    │  │
│  │                                                           │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📊 Data Flow Diagrams

### 1. Legal Research Query Flow

```
User Query
    │
    ▼
┌─────────────────────────┐
│  Frontend (index.html)  │
│  - User types question  │
│  - Selects model (opt.) │
└──────────┬──────────────┘
           │
           │ POST /api/v1/research/query
           │ { query, model_preference }
           ▼
┌─────────────────────────┐
│   Smart Router Service  │◄─────┐
│  - Analyze complexity   │      │
│  - Select best model    │      │
└──────────┬──────────────┘      │
           │                     │
           │ Model Selected      │
           │ (e.g., claude-3.5)  │
           ▼                     │
┌─────────────────────────┐      │
│ OpenRouter Service      │      │
│ - Call OpenRouter API   │      │
│ - Get AI response       │      │
└──────────┬──────────────┘      │
           │                     │
           │ AI Response +       │
           │ Token Count         │
           ▼                     │
┌─────────────────────────┐      │
│  Cost Tracker Service   │──────┘
│  - Calculate cost       │
│  - Log to JSON          │
└──────────┬──────────────┘
           │
           │ Response + Cost
           ▼
┌─────────────────────────┐
│  Frontend Display       │
│  - Show answer          │
│  - Show model used      │
│  - Show cost            │
└─────────────────────────┘
```

### 2. Template Generation Flow

```
User Wants Document
    │
    ▼
┌─────────────────────────┐
│ Frontend (templates.html)│
│ - Browse categories     │
│ - Select template       │
└──────────┬──────────────┘
           │
           │ GET /api/v1/templates/category/gst
           │
           ▼
┌─────────────────────────┐
│  Template Service       │
│  - Return template list │
│  - Show form fields     │
└──────────┬──────────────┘
           │
           │ Template displayed
           ▼
┌─────────────────────────┐
│  Frontend Form          │
│  - User fills fields    │
│  - Toggles AI enhance   │
│  - Clicks Generate      │
└──────────┬──────────────┘
           │
           │ POST /api/v1/templates/fill
           │ { template_id, field_values, ai_enhance }
           ▼
┌─────────────────────────┐
│  Template Service       │
│  - Validate fields      │
│  - Fill template        │
└──────────┬──────────────┘
           │
           │ If ai_enhance = true
           ▼
┌─────────────────────────┐
│ OpenRouter Service      │
│ - Enhance document      │
│ - Improve language      │
│ - Add legal references  │
└──────────┬──────────────┘
           │
           │ Enhanced Document
           ▼
┌─────────────────────────┐
│  Frontend Display       │
│  - Show generated doc   │
│  - Offer copy/download  │
└─────────────────────────┘
```

### 3. Cost Tracking Flow

```
Every API Call
    │
    ▼
┌─────────────────────────┐
│  OpenRouter Service     │
│  Returns:               │
│  - Response text        │
│  - Tokens used          │
│  - Model name           │
└──────────┬──────────────┘
           │
           │ Usage Data
           ▼
┌─────────────────────────┐
│  Cost Tracker Service   │
│  Calculate:             │
│  - Cost per token       │
│  - Total cost USD       │
└──────────┬──────────────┘
           │
           │ Save to JSON
           ▼
┌─────────────────────────┐
│  cost_tracking.json     │
│  {                      │
│    timestamp,           │
│    model_id,            │
│    tokens_used,         │
│    cost_usd,            │
│    query_type           │
│  }                      │
└──────────┬──────────────┘
           │
           │ When user views dashboard
           ▼
┌─────────────────────────┐
│  GET /api/v1/cost-      │
│  tracking/dashboard     │
└──────────┬──────────────┘
           │
           │ Aggregate data
           ▼
┌─────────────────────────┐
│  Cost Tracker Service   │
│  Calculate:             │
│  - Total spend          │
│  - Daily trends         │
│  - Cost by model        │
│  - vs VIDUR comparison  │
└──────────┬──────────────┘
           │
           │ Dashboard Data
           ▼
┌─────────────────────────┐
│  Frontend Dashboard     │
│  - Charts               │
│  - Savings %            │
│  - Export button        │
└─────────────────────────┘
```

### 4. PWA Installation Flow

```
User Visits LegalMitra
    │
    ▼
┌─────────────────────────┐
│  Browser (Chrome/Edge)  │
│  Loads: index.html      │
└──────────┬──────────────┘
           │
           │ Checks manifest.json
           ▼
┌─────────────────────────┐
│  manifest.json          │
│  - App name             │
│  - Icons (8 sizes)      │
│  - Display: standalone  │
│  - Start URL            │
└──────────┬──────────────┘
           │
           │ PWA Criteria Met
           ▼
┌─────────────────────────┐
│  Browser triggers       │
│  'beforeinstallprompt'  │
└──────────┬──────────────┘
           │
           │ Event caught by pwa.js
           ▼
┌─────────────────────────┐
│  pwa.js                 │
│  - Show install button  │
│  - Store prompt         │
└──────────┬──────────────┘
           │
           │ User clicks "Install"
           ▼
┌─────────────────────────┐
│  pwa.js                 │
│  - Call prompt()        │
│  - Wait for choice      │
└──────────┬──────────────┘
           │
           │ User accepts
           ▼
┌─────────────────────────┐
│  Browser installs PWA   │
│  - Downloads manifest   │
│  - Downloads icons      │
│  - Registers SW         │
└──────────┬──────────────┘
           │
           │ Installation complete
           ▼
┌─────────────────────────┐
│  Device Home Screen     │
│  - LegalMitra icon      │
│  - Custom branding      │
│  - Opens in standalone  │
└─────────────────────────┘
```

### 5. Offline Support Flow

```
Online First Visit
    │
    ▼
┌─────────────────────────┐
│  Browser loads app      │
│  Registers SW           │
└──────────┬──────────────┘
           │
           │ SW install event
           ▼
┌─────────────────────────┐
│  service-worker.js      │
│  Cache static assets:   │
│  - HTML files           │
│  - CSS files            │
│  - JS files             │
│  - Icons                │
│  - Logo                 │
└──────────┬──────────────┘
           │
           │ Assets cached
           ▼
┌─────────────────────────┐
│  Browser Cache          │
│  'legalmitra-v1.0.0'    │
└──────────┬──────────────┘
           │
           │ User goes offline
           ▼
┌─────────────────────────┐
│  User requests page     │
└──────────┬──────────────┘
           │
           │ SW fetch event
           ▼
┌─────────────────────────┐
│  service-worker.js      │
│  - Check cache first    │
│  - Serve cached version │
└──────────┬──────────────┘
           │
           │ Cached asset
           ▼
┌─────────────────────────┐
│  Page loads offline     │
│  - Templates browseable │
│  - Dashboard viewable   │
│  - Cached data shown    │
└─────────────────────────┘
```

---

## 🔧 Component Architecture

### Frontend Components

```
frontend/
│
├── Core Pages
│   ├── index.html           → Legal research interface
│   ├── templates.html       → Template browser & generator
│   ├── cost-dashboard.html  → Cost analytics dashboard
│   ├── model-selector.html  → AI model selection
│   └── diary.html           → Advocate diary (existing)
│
├── PWA Infrastructure
│   ├── manifest.json        → PWA configuration
│   ├── service-worker.js    → Offline support + caching
│   └── pwa.js               → Install prompt handler
│
├── Assets
│   ├── icons/               → PWA icons (8 sizes)
│   ├── logo.png             → Full logo
│   └── logo-video.mp4       → Animated logo
│
└── Utilities
    └── generate-pwa-icons.html → Icon generator tool
```

### Backend Components

```
backend/app/
│
├── API Routes (FastAPI)
│   ├── research.py          → Legal research endpoints (enhanced)
│   ├── templates.py         → Template management [NEW]
│   ├── smart_routing.py     → Model routing [NEW]
│   ├── cost_tracking.py     → Cost analytics [NEW]
│   ├── model_selection.py   → Model browsing [NEW]
│   └── diary.py             → Advocate diary (existing)
│
├── Services (Business Logic)
│   ├── openrouter_service.py    → OpenRouter API integration [NEW]
│   ├── smart_router.py          → Intelligent model selection [NEW]
│   ├── cost_tracker.py          → Usage tracking [NEW]
│   ├── template_service.py      → Template engine [NEW]
│   └── research_service.py      → Research logic (existing)
│
├── Core
│   ├── config.py            → Configuration (enhanced with OpenRouter)
│   └── dependencies.py      → Dependency injection
│
├── Models (Pydantic)
│   ├── research.py          → Research request/response models
│   ├── templates.py         → Template models [NEW]
│   └── cost.py              → Cost tracking models [NEW]
│
└── Main
    └── main.py              → FastAPI app + router registration
```

---

## 🔄 Integration Points

### 1. OpenRouter Integration

```python
# backend/app/services/openrouter_service.py

class OpenRouterService:
    def __init__(self):
        self.base_url = "https://openrouter.ai/api/v1"
        self.api_key = settings.OPENROUTER_API_KEY

    async def generate_text(
        self,
        user_text: str,
        model: str = "anthropic/claude-3.5-sonnet"
    ) -> Dict:
        # Calls OpenRouter API
        # Returns: response, tokens, cost
```

**Connects to:**
- Smart Router (for model selection)
- Cost Tracker (for usage logging)
- Research API (for query processing)
- Template Service (for AI enhancement)

### 2. Smart Router Integration

```python
# backend/app/services/smart_router.py

class SmartRouter:
    def analyze_query_complexity(self, query: str) -> Dict:
        # Returns complexity score 0-100

    def select_model(
        self,
        query: str,
        user_preference: str = "balanced"
    ) -> Tuple[str, Dict]:
        # Returns: (model_id, selection_info)
```

**Connects to:**
- OpenRouter Service (to get available models)
- Cost Tracker (to consider budget)
- Research API (to receive queries)

### 3. Cost Tracker Integration

```python
# backend/app/services/cost_tracker.py

class CostTracker:
    def record_usage(
        self,
        model_id: str,
        tokens_used: int,
        cost_usd: float
    ):
        # Saves to cost_tracking.json

    def get_dashboard_data(self, days: int = 30) -> Dict:
        # Returns aggregated analytics
```

**Connects to:**
- OpenRouter Service (receives usage data)
- Cost Dashboard (provides analytics)
- Smart Router (provides budget info)

### 4. Template Service Integration

```python
# backend/app/templates/template_service.py

class TemplateService:
    def get_templates_by_category(self, category: str) -> List[Template]:
        # Returns template list

    async def fill_template(
        self,
        template_id: str,
        field_values: Dict,
        ai_enhance: bool = True
    ) -> str:
        # Fills template, optionally enhances with AI
```

**Connects to:**
- OpenRouter Service (for AI enhancement)
- Templates API (provides template data)
- Cost Tracker (logs AI enhancement costs)

---

## 📦 Technology Stack

### Frontend
```
├── HTML5              → Semantic markup
├── CSS3               → Styling + animations
├── JavaScript (ES6+)  → Client-side logic
├── Fetch API          → Backend communication
├── Chart.js           → Cost dashboard charts (future)
└── PWA APIs           → Service Workers, Manifest
```

### Backend
```
├── Python 3.11+       → Programming language
├── FastAPI            → Web framework
├── Pydantic           → Data validation
├── SQLAlchemy         → ORM for diary database
├── SQLite             → Database (advocate diary)
├── httpx              → Async HTTP client (OpenRouter)
└── python-dotenv      → Environment variables
```

### External Services
```
├── OpenRouter API     → Multi-model AI access
├── Claude 3.5         → Default AI model
├── GPT-4              → Alternative AI model
└── Gemini Pro         → Budget AI model
```

### Development Tools
```
├── Pillow             → Icon generation
├── Git                → Version control
└── FastAPI Docs       → Auto-generated API docs
```

---

## 🔐 Security Architecture

### API Key Management
```
.env (NOT committed to git)
    │
    │ Loaded by python-dotenv
    ▼
config.py (Settings class)
    │
    │ Injected into services
    ▼
OpenRouterService (uses API key)
```

### Data Privacy
```
User Query
    │
    ▼
Backend (validates, sanitizes)
    │
    ▼
OpenRouter (processes with AI)
    │
    ▼
Response (no data stored by OpenRouter)
    │
    ▼
Cost Tracker (logs only: model, tokens, cost, timestamp)
```

**No sensitive data stored:**
- ✅ User queries not saved permanently
- ✅ API responses not logged
- ✅ Only metadata tracked (cost, tokens)
- ✅ Advocate diary encrypted (existing feature)

---

## 🚀 Deployment Architecture

### Development (Current)
```
┌─────────────────┐
│  Local Machine  │
│  Windows        │
│                 │
│  Backend:       │
│  localhost:8888 │
│                 │
│  Frontend:      │
│  file:/// URL   │
└─────────────────┘
```

### Production (Recommended)
```
┌─────────────────────────────────────────┐
│           Cloud Provider                 │
│  (AWS / Azure / Google Cloud)            │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │  HTTPS Load Balancer               │ │
│  │  SSL Certificate (Let's Encrypt)   │ │
│  └──────────┬─────────────────────────┘ │
│             │                            │
│             ▼                            │
│  ┌────────────────────────────────────┐ │
│  │  FastAPI Backend                   │ │
│  │  (Gunicorn + Uvicorn workers)      │ │
│  │  Port: 8888                        │ │
│  └──────────┬─────────────────────────┘ │
│             │                            │
│             ▼                            │
│  ┌────────────────────────────────────┐ │
│  │  SQLite Database                   │ │
│  │  cost_tracking.json                │ │
│  └────────────────────────────────────┘ │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │  Static File Server (Nginx)        │ │
│  │  Serves: frontend/*.html, PWA      │ │
│  └────────────────────────────────────┘ │
└─────────────────────────────────────────┘
                    │
                    │ HTTPS
                    ▼
            ┌──────────────┐
            │  OpenRouter  │
            │  API         │
            └──────────────┘
```

---

## 📊 Scalability Considerations

### Current Limits
- **Concurrent Users**: ~100 (single FastAPI process)
- **Database**: SQLite (suitable for <100k records)
- **API Rate Limits**: OpenRouter limits (varies by tier)

### Scaling Options

**1. Horizontal Scaling (Multiple Instances)**
```
Load Balancer
    │
    ├─ FastAPI Instance 1
    ├─ FastAPI Instance 2
    └─ FastAPI Instance 3
         │
         └─ Shared PostgreSQL Database
```

**2. Caching Layer**
```
User Request
    │
    ▼
Redis Cache (common queries)
    │
    ├─ Cache Hit → Return cached result
    └─ Cache Miss → Call OpenRouter API
```

**3. Database Upgrade**
```
SQLite (Development)
    │
    └─ Migrate to PostgreSQL (Production)
        │
        ├─ Better concurrency
        ├─ Advanced analytics
        └─ Horizontal scaling
```

---

## 🎯 Performance Metrics

### Target Performance
```
Page Load Time:
- First visit: <2s
- Repeat visit (PWA cached): <500ms

API Response Time:
- Template generation: <1s
- AI query (simple): <3s
- AI query (complex): <10s

PWA Installation:
- Time to install: <10s
- Icon generation: <5s
- Service worker registration: <1s
```

### Monitoring Points
```
1. API Latency (per endpoint)
2. OpenRouter API response time
3. Cache hit rate (service worker)
4. Error rate (4xx, 5xx)
5. Cost per query (tracked automatically)
6. Daily active users (future)
```

---

## 🔄 Update Flow

### Frontend Updates
```
Developer pushes changes
    │
    ▼
Update version in service-worker.js
    │
    ▼
User visits app
    │
    ▼
Service worker detects new version
    │
    ▼
Downloads new assets in background
    │
    ▼
Shows "Update Available" notification
    │
    ▼
User clicks "Update"
    │
    ▼
New version activated
```

### Backend Updates
```
Developer pushes changes
    │
    ▼
Deploy new backend version
    │
    ▼
Restart FastAPI server
    │
    ▼
New endpoints/features available
    │
    ▼
Frontend calls new APIs
```

---

**This architecture supports:**
- ✅ 200+ AI models via OpenRouter
- ✅ Offline-first PWA functionality
- ✅ Real-time cost tracking
- ✅ Smart model routing
- ✅ 20+ document templates
- ✅ Scalability to thousands of users
- ✅ Easy deployment and updates

---

*For implementation details, see: ENHANCEMENTS_SUMMARY.md*
