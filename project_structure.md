# Legal AI Assistant - Complete Project Structure

## 📁 Project Organization

```
legal-ai-assistant/
│
├── README.md                           # Main project documentation
├── requirements.txt                    # Python dependencies
├── .gitignore                          # Git ignore file
├── .env.example                        # Environment variables template
├── docker-compose.yml                  # Docker configuration
│
├── backend/                            # Backend API
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                    # FastAPI application entry point
│   │   │
│   │   ├── api/                       # API routes
│   │   │   ├── __init__.py
│   │   │   ├── routes.py              # Main API routes
│   │   │   ├── legal_research.py      # Research endpoints
│   │   │   ├── document_drafting.py   # Drafting endpoints
│   │   │   ├── case_search.py         # Case law search
│   │   │   └── statute_search.py      # Statute search
│   │   │
│   │   └── core/                      # Core configurations
│   │       ├── __init__.py
│   │       ├── config.py              # App configuration
│   │       ├── security.py            # Authentication & security
│   │       └── dependencies.py        # Dependency injection
│   │
│   ├── database/                      # Database connections
│   │   ├── __init__.py
│   │   ├── mongodb.py                 # MongoDB connection
│   │   ├── vector_db.py               # Vector database (Pinecone/Chroma)
│   │   └── redis_client.py            # Redis for caching
│   │
│   ├── models/                        # Data models (Pydantic)
│   │   ├── __init__.py
│   │   ├── legal_models.py            # Legal data models
│   │   ├── user_models.py             # User models
│   │   └── document_models.py         # Document models
│   │
│   ├── services/                      # Business logic
│   │   ├── __init__.py
│   │   ├── ai_service.py              # AI/LLM integration
│   │   ├── case_law_service.py        # Case law operations
│   │   ├── statute_service.py         # Statute operations
│   │   ├── document_service.py        # Document generation
│   │   └── search_service.py          # Search functionality
│   │
│   ├── utils/                         # Utility functions
│   │   ├── __init__.py
│   │   ├── text_processing.py         # Text utilities
│   │   ├── citation_parser.py         # Parse citations
│   │   ├── pdf_generator.py           # Generate PDFs
│   │   └── validators.py              # Data validation
│   │
│   ├── prompts/                       # AI prompts
│   │   ├── legal_system_prompt.txt    # Main system prompt
│   │   ├── drafting_prompts.py        # Document drafting prompts
│   │   └── research_prompts.py        # Research prompts
│   │
│   ├── schemas/                       # API schemas
│   │   ├── __init__.py
│   │   ├── request_schemas.py         # Request models
│   │   └── response_schemas.py        # Response models
│   │
│   ├── tests/                         # Unit & integration tests
│   │   ├── __init__.py
│   │   ├── test_api.py                # API tests
│   │   ├── test_services.py           # Service tests
│   │   └── test_utils.py              # Utility tests
│   │
│   ├── scripts/                       # Utility scripts
│   │   ├── populate_database.py       # Populate case laws & statutes
│   │   ├── scrape_judgments.py        # Scrape from legal sites
│   │   ├── generate_embeddings.py     # Create vector embeddings
│   │   └── backup_database.py         # Database backup
│   │
│   └── alembic/                       # Database migrations
│       ├── versions/
│       └── env.py
│
├── frontend/                          # React frontend
│   ├── public/
│   │   ├── index.html
│   │   ├── favicon.ico
│   │   └── manifest.json
│   │
│   ├── src/
│   │   ├── index.tsx                  # Entry point
│   │   ├── App.tsx                    # Main app component
│   │   │
│   │   ├── components/                # Reusable components
│   │   │   ├── common/
│   │   │   │   ├── Header.tsx
│   │   │   │   ├── Footer.tsx
│   │   │   │   ├── Sidebar.tsx
│   │   │   │   └── Loading.tsx
│   │   │   │
│   │   │   ├── legal/
│   │   │   │   ├── QueryInterface.tsx    # Legal query form
│   │   │   │   ├── CaseLawCard.tsx       # Display case law
│   │   │   │   ├── StatuteCard.tsx       # Display statute
│   │   │   │   └── DocumentEditor.tsx    # Edit documents
│   │   │   │
│   │   │   └── search/
│   │   │       ├── SearchBar.tsx
│   │   │       ├── FilterPanel.tsx
│   │   │       └── ResultsList.tsx
│   │   │
│   │   ├── pages/                     # Page components
│   │   │   ├── Home.tsx               # Landing page
│   │   │   ├── Research.tsx           # Legal research
│   │   │   ├── CaseSearch.tsx         # Case law search
│   │   │   ├── Drafting.tsx           # Document drafting
│   │   │   ├── Dashboard.tsx          # User dashboard
│   │   │   └── Login.tsx              # Authentication
│   │   │
│   │   ├── services/                  # API services
│   │   │   ├── api.ts                 # API client
│   │   │   ├── legalService.ts        # Legal operations
│   │   │   └── authService.ts         # Authentication
│   │   │
│   │   ├── hooks/                     # Custom React hooks
│   │   │   ├── useAuth.ts
│   │   │   ├── useLegalQuery.ts
│   │   │   └── useDebounce.ts
│   │   │
│   │   ├── context/                   # React Context
│   │   │   ├── AuthContext.tsx
│   │   │   └── ThemeContext.tsx
│   │   │
│   │   ├── utils/                     # Utility functions
│   │   │   ├── formatting.ts
│   │   │   ├── validation.ts
│   │   │   └── constants.ts
│   │   │
│   │   ├── types/                     # TypeScript types
│   │   │   ├── legal.types.ts
│   │   │   └── api.types.ts
│   │   │
│   │   └── styles/                    # CSS/SCSS files
│   │       ├── global.css
│   │       ├── variables.css
│   │       └── components.css
│   │
│   ├── package.json                   # Node dependencies
│   ├── tsconfig.json                  # TypeScript config
│   └── .env.example                   # Frontend env variables
│
├── data/                              # Data files
│   ├── acts/                          # Statutory acts (JSON/PDF)
│   │   ├── CGST_Act_2017.json
│   │   ├── Income_Tax_Act_1961.json
│   │   ├── BNS_2023.json
│   │   └── ...
│   │
│   ├── case_laws/                     # Case law database
│   │   ├── supreme_court/
│   │   │   ├── 2023/
│   │   │   ├── 2022/
│   │   │   └── ...
│   │   │
│   │   ├── high_courts/
│   │   │   ├── delhi/
│   │   │   ├── bombay/
│   │   │   └── ...
│   │   │
│   │   └── metadata/
│   │       ├── case_index.json
│   │       └── keywords.json
│   │
│   ├── templates/                     # Document templates
│   │   ├── petition_template.docx
│   │   ├── reply_template.docx
│   │   ├── notice_template.docx
│   │   └── opinion_template.docx
│   │
│   └── embeddings/                    # Pre-computed embeddings
│       ├── case_embeddings.pkl
│       └── statute_embeddings.pkl
│
├── docs/                              # Documentation
│   ├── api/                           # API documentation
│   │   ├── endpoints.md
│   │   └── authentication.md
│   │
│   ├── guides/                        # User guides
│   │   ├── getting_started.md
│   │   ├── legal_research_guide.md
│   │   └── document_drafting_guide.md
│   │
│   ├── architecture/                  # Architecture docs
│   │   ├── system_design.md
│   │   ├── database_schema.md
│   │   └── ai_integration.md
│   │
│   └── legal/                         # Legal documentation
│       ├── citation_standards.md
│       ├── supported_acts.md
│       └── disclaimer.md
│
├── notebooks/                         # Jupyter notebooks
│   ├── data_exploration.ipynb
│   ├── embeddings_testing.ipynb
│   └── model_evaluation.ipynb
│
├── deployment/                        # Deployment files
│   ├── nginx/
│   │   └── nginx.conf
│   │
│   ├── docker/
│   │   ├── Dockerfile.backend
│   │   └── Dockerfile.frontend
│   │
│   └── kubernetes/
│       ├── backend-deployment.yaml
│       └── frontend-deployment.yaml
│
├── monitoring/                        # Monitoring & logging
│   ├── prometheus/
│   │   └── prometheus.yml
│   │
│   └── grafana/
│       └── dashboards/
│
└── .github/                          # GitHub Actions
    └── workflows/
        ├── test.yml                   # CI/CD tests
        └── deploy.yml                 # Deployment

```

## 📝 File Details

### Backend Files

#### `backend/app/main.py`
Main FastAPI application entry point.

#### `backend/services/ai_service.py`
Handles all AI/LLM interactions (OpenAI, Anthropic).

#### `backend/database/mongodb.py`
MongoDB connection and operations.

#### `backend/prompts/legal_system_prompt.txt`
The comprehensive system prompt for the AI.

### Frontend Files

#### `frontend/src/pages/Research.tsx`
Main legal research interface.

#### `frontend/src/components/legal/QueryInterface.tsx`
Component for submitting legal queries.

#### `frontend/src/services/legalService.ts`
API calls to backend.

### Configuration Files

#### `.env.example`
```env
# Backend
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
MONGODB_URI=mongodb://localhost:27017/
PINECONE_API_KEY=
REDIS_HOST=localhost

# Frontend
REACT_APP_API_URL=http://localhost:8000
```

#### `docker-compose.yml`
Container orchestration for MongoDB, Redis, Backend, Frontend.

## 🚀 Quick Setup Commands

### Initial Setup
```bash
# Clone/Create project
mkdir legal-ai-assistant
cd legal-ai-assistant

# Copy structure
# (Use the structure above to create folders)

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Frontend setup
cd ../frontend
npm install

# Environment variables
cp .env.example .env
# Edit .env with your API keys
```

### Running the Application

```bash
# Terminal 1 - MongoDB
docker-compose up mongodb

# Terminal 2 - Backend
cd backend
source venv/bin/activate
uvicorn app.main:app --reload

# Terminal 3 - Frontend
cd frontend
npm start
```

## 📦 Key Dependencies by Component

### Backend Core
- FastAPI, Uvicorn, Pydantic
- Motor (async MongoDB)
- OpenAI/Anthropic SDK

### AI/ML
- LangChain
- Pinecone/ChromaDB
- Sentence Transformers

### Document Processing
- python-docx
- PyPDF2
- ReportLab

### Frontend Core
- React 18
- TypeScript
- Material-UI
- Axios

## 🔐 Security Considerations

1. **API Keys**: Store in environment variables, never commit
2. **Authentication**: Implement JWT for user auth
3. **Rate Limiting**: Protect endpoints from abuse
4. **Input Validation**: Validate all user inputs
5. **CORS**: Configure properly for production

## 📊 Database Schema

### MongoDB Collections

```javascript
// case_laws
{
  _id: ObjectId,
  case_name: String,
  citation: String,
  court: String,
  year: Number,
  judges: [String],
  ratio_decidendi: String,
  full_text: String,
  keywords: [String],
  vector_embedding: [Number]
}

// statutes
{
  _id: ObjectId,
  act_name: String,
  sections: [{section: String, content: String}],
  year: Number,
  keywords: [String]
}

// user_queries
{
  _id: ObjectId,
  user_id: String,
  query: String,
  response: String,
  timestamp: Date
}
```

## 🎯 Development Workflow

1. **Feature Development**
   - Create feature branch
   - Implement in backend/frontend
   - Write tests
   - Update documentation

2. **Testing**
   ```bash
   # Backend
   pytest backend/tests/
   
   # Frontend
   npm test
   ```

3. **Deployment**
   ```bash
   docker-compose up --build
   ```

## 📈 Scalability Considerations

- **Caching**: Use Redis for frequent queries
- **Load Balancing**: Nginx for multiple backend instances
- **Database**: MongoDB Atlas for cloud scaling
- **CDN**: CloudFlare for static assets
- **Async**: Use async/await throughout

---

**Note**: This structure is comprehensive. For MVP, you can start with just:
- `backend/app/main.py`
- `backend/services/ai_service.py`
- `frontend/src/App.tsx`
- And gradually add more components as needed.
