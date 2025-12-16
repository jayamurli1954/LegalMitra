# Implementation Guide: Indian Legal AI Assistant
## Step-by-Step Guide for Beginners

---

## PHASE 1: PROJECT SETUP (Week 1)

### Step 1.1: Choose Your Technology Stack

**Recommended Stack for Beginners:**
```
Frontend: React.js (Web Interface)
Backend: FastAPI (Python)
Database: MongoDB + Vector Database (Pinecone/Weaviate)
AI Model: OpenAI GPT-4 / Claude API / Gemini Pro
Hosting: AWS/Google Cloud/Azure
```

**Why this stack?**
- You're already familiar with FastAPI and React from MandirSync
- Python is excellent for AI/ML integration
- MongoDB handles unstructured legal data well
- Vector databases enable semantic search of case laws

### Step 1.2: Create Project Structure

```bash
# Create main project directory
mkdir legal-ai-assistant
cd legal-ai-assistant

# Create backend structure
mkdir -p backend/{app,database,models,services,utils,prompts}
mkdir -p backend/app/{api,core}

# Create frontend structure
mkdir -p frontend/{src,public}
mkdir -p frontend/src/{components,pages,services,utils}

# Create data directories
mkdir -p data/{acts,case_laws,templates}
```

### Step 1.3: Initialize Backend

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Create requirements.txt
touch requirements.txt
```

**requirements.txt:**
```txt
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
pymongo==4.6.0
motor==3.3.2
python-dotenv==1.0.0
openai==1.3.0
anthropic==0.7.0
langchain==0.1.0
pinecone-client==3.0.0
PyPDF2==3.0.1
python-docx==1.1.0
pandas==2.1.3
httpx==0.25.2
python-multipart==0.0.6
redis==5.0.1
celery==5.3.4
```

### Step 1.4: Initialize Frontend

```bash
# Navigate to frontend
cd ../frontend

# Create React app
npx create-react-app . --template typescript

# Install additional dependencies
npm install axios react-router-dom @mui/material @emotion/react @emotion/styled
npm install react-markdown react-pdf
```

---

## PHASE 2: BACKEND DEVELOPMENT (Weeks 2-4)

### Step 2.1: Setup Environment Variables

Create `backend/.env`:
```env
# API Keys
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
GOOGLE_API_KEY=your_google_key

# Database
MONGODB_URI=mongodb://localhost:27017/
DATABASE_NAME=legal_ai_db

# Vector Database
PINECONE_API_KEY=your_pinecone_key
PINECONE_ENVIRONMENT=us-west1-gcp

# Security
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Redis (for caching)
REDIS_HOST=localhost
REDIS_PORT=6379
```

### Step 2.2: Create Database Models

**backend/models/legal_models.py:**
```python
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime
from enum import Enum

class CourtLevel(str, Enum):
    SUPREME_COURT = "Supreme Court"
    HIGH_COURT = "High Court"
    DISTRICT_COURT = "District Court"
    MAGISTRATE_COURT = "Magistrate Court"
    TRIBUNAL = "Tribunal"

class LegalDomain(str, Enum):
    CRIMINAL = "Criminal Law"
    CIVIL = "Civil Law"
    TAX = "Tax Law"
    CORPORATE = "Corporate Law"
    FAMILY = "Family Law"
    CONSTITUTIONAL = "Constitutional Law"
    LABOUR = "Labour Law"
    IPR = "Intellectual Property"
    OTHER = "Other"

class CaseLaw(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    case_name: str
    citation: str
    court: CourtLevel
    year: int
    judges: List[str]
    ratio_decidendi: str
    obiter_dicta: Optional[str] = None
    legal_domain: List[LegalDomain]
    relevant_sections: List[str]
    headnotes: str
    full_text: str
    current_status: str = "Valid"  # Valid/Overruled/Distinguished
    overruled_by: Optional[str] = None
    keywords: List[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    vector_embedding: Optional[List[float]] = None

class Statute(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    act_name: str
    act_year: int
    sections: List[Dict[str, str]]  # {"section": "123", "content": "..."}
    short_title: str
    legal_domain: List[LegalDomain]
    enforced_from: datetime
    repealed: bool = False
    repealed_by: Optional[str] = None
    latest_amendment: Optional[str] = None
    keywords: List[str]
    full_text: str
    vector_embedding: Optional[List[float]] = None

class LegalQuery(BaseModel):
    query_text: str
    query_type: str  # research/drafting/opinion/case_prep
    legal_domain: Optional[List[LegalDomain]] = None
    context: Optional[Dict] = None

class LegalResponse(BaseModel):
    query_id: str
    response_text: str
    relevant_statutes: List[str]
    relevant_cases: List[Dict]
    confidence_score: float
    sources: List[Dict]
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class DocumentDraft(BaseModel):
    document_type: str  # petition/reply/notice/opinion
    parties: Dict[str, str]
    facts: str
    legal_grounds: List[str]
    prayer: str
    supporting_cases: List[str]
    supporting_statutes: List[str]
    generated_text: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserQuery(BaseModel):
    user_id: str
    query: LegalQuery
    response: Optional[LegalResponse] = None
    feedback: Optional[Dict] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

### Step 2.3: Database Connection

**backend/database/mongodb.py:**
```python
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
import os
from dotenv import load_load_dotenv()

class MongoDB:
    client: Optional[AsyncIOMotorClient] = None
    database = None

mongodb = MongoDB()

async def connect_to_mongo():
    """Connect to MongoDB"""
    mongodb.client = AsyncIOMotorClient(os.getenv("MONGODB_URI"))
    mongodb.database = mongodb.client[os.getenv("DATABASE_NAME")]
    print("✅ Connected to MongoDB")

async def close_mongo_connection():
    """Close MongoDB connection"""
    if mongodb.client:
        mongodb.client.close()
        print("❌ Closed MongoDB connection")

def get_database():
    """Get database instance"""
    return mongodb.database
```

### Step 2.4: Vector Database Setup

**backend/database/vector_db.py:**
```python
import pinecone
from typing import List, Dict
import os
from openai import OpenAI

class VectorDatabase:
    def __init__(self):
        # Initialize Pinecone
        pinecone.init(
            api_key=os.getenv("PINECONE_API_KEY"),
            environment=os.getenv("PINECONE_ENVIRONMENT")
        )
        self.index_name = "legal-cases"
        
        # Create index if doesn't exist
        if self.index_name not in pinecone.list_indexes():
            pinecone.create_index(
                name=self.index_name,
                dimension=1536,  # OpenAI embedding dimension
                metric="cosine"
            )
        
        self.index = pinecone.Index(self.index_name)
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for text using OpenAI"""
        response = self.openai_client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding
    
    async def add_case_law(self, case_id: str, case_text: str, metadata: Dict):
        """Add case law to vector database"""
        embedding = self.generate_embedding(case_text)
        self.index.upsert(vectors=[(case_id, embedding, metadata)])
    
    async def search_similar_cases(self, query: str, top_k: int = 10) -> List[Dict]:
        """Search for similar cases"""
        query_embedding = self.generate_embedding(query)
        results = self.index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True
        )
        return results['matches']
    
    async def search_by_citation(self, citation: str) -> Dict:
        """Search case by citation"""
        results = self.index.query(
            filter={"citation": citation},
            top_k=1,
            include_metadata=True
        )
        return results['matches'][0] if results['matches'] else None

vector_db = VectorDatabase()
```

### Step 2.5: AI Service Integration

**backend/services/ai_service.py:**
```python
from anthropic import Anthropic
from openai import OpenAI
import os
from typing import Dict, List

class LegalAIService:
    def __init__(self):
        self.anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Load system prompt
        with open("prompts/legal_system_prompt.txt", "r") as f:
            self.system_prompt = f.read()
    
    async def process_legal_query(
        self, 
        query: str, 
        context: Dict = None,
        relevant_cases: List[Dict] = None,
        relevant_statutes: List[Dict] = None
    ) -> str:
        """Process legal query using Claude"""
        
        # Build context
        context_text = self._build_context(context, relevant_cases, relevant_statutes)
        
        # Create message
        message = self.anthropic_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            system=self.system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": f"{context_text}\n\nQuery: {query}"
                }
            ]
        )
        
        return message.content[0].text
    
    def _build_context(
        self, 
        context: Dict,
        relevant_cases: List[Dict],
        relevant_statutes: List[Dict]
    ) -> str:
        """Build context for AI"""
        context_parts = []
        
        if context:
            context_parts.append(f"CONTEXT:\n{context}")
        
        if relevant_statutes:
            statutes_text = "\n\n".join([
                f"**{s['act_name']}**\nSection {s['section']}: {s['content']}"
                for s in relevant_statutes
            ])
            context_parts.append(f"RELEVANT STATUTES:\n{statutes_text}")
        
        if relevant_cases:
            cases_text = "\n\n".join([
                f"**{c['case_name']}**\n"
                f"Citation: {c['citation']}\n"
                f"Principle: {c['ratio_decidendi']}"
                for c in relevant_cases
            ])
            context_parts.append(f"RELEVANT CASE LAWS:\n{cases_text}")
        
        return "\n\n---\n\n".join(context_parts)
    
    async def draft_document(
        self,
        document_type: str,
        facts: str,
        parties: Dict,
        legal_grounds: List[str],
        prayer: str,
        supporting_materials: Dict
    ) -> str:
        """Draft legal document"""
        
        prompt = f"""
Draft a {document_type} with the following details:

PARTIES:
{self._format_parties(parties)}

FACTS:
{facts}

LEGAL GROUNDS:
{chr(10).join(f"{i+1}. {ground}" for i, ground in enumerate(legal_grounds))}

PRAYER:
{prayer}

SUPPORTING MATERIALS:
{self._format_supporting_materials(supporting_materials)}

Please provide a complete, professionally formatted {document_type}.
"""
        
        message = self.anthropic_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=8000,
            system=self.system_prompt,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return message.content[0].text
    
    def _format_parties(self, parties: Dict) -> str:
        """Format parties information"""
        return "\n".join([f"{role}: {name}" for role, name in parties.items()])
    
    def _format_supporting_materials(self, materials: Dict) -> str:
        """Format supporting materials"""
        parts = []
        if materials.get("cases"):
            parts.append("Case Laws:\n" + "\n".join(materials["cases"]))
        if materials.get("statutes"):
            parts.append("Statutory Provisions:\n" + "\n".join(materials["statutes"]))
        return "\n\n".join(parts)

ai_service = LegalAIService()
```

### Step 2.6: API Routes

**backend/app/api/routes.py:**
```python
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict
from models.legal_models import (
    LegalQuery, LegalResponse, DocumentDraft,
    CaseLaw, Statute
)
from services.ai_service import ai_service
from database.vector_db import vector_db
from database.mongodb import get_database

router = APIRouter()

@router.post("/query/research", response_model=LegalResponse)
async def legal_research(query: LegalQuery):
    """Handle legal research queries"""
    try:
        # Search for relevant cases
        similar_cases = await vector_db.search_similar_cases(
            query.query_text,
            top_k=10
        )
        
        # Get case details from MongoDB
        db = get_database()
        case_ids = [match['id'] for match in similar_cases]
        cases = await db.case_laws.find({"_id": {"$in": case_ids}}).to_list(length=10)
        
        # Search for relevant statutes
        # (Implement statute search logic)
        
        # Process query with AI
        response_text = await ai_service.process_legal_query(
            query=query.query_text,
            context=query.context,
            relevant_cases=cases,
            relevant_statutes=[]  # Add statute search results
        )
        
        return LegalResponse(
            query_id=str(ObjectId()),
            response_text=response_text,
            relevant_statutes=[],
            relevant_cases=[{
                "case_name": c["case_name"],
                "citation": c["citation"],
                "ratio_decidendi": c["ratio_decidendi"]
            } for c in cases],
            confidence_score=0.85,
            sources=similar_cases
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/draft/petition")
async def draft_petition(draft_request: DocumentDraft):
    """Draft a petition"""
    try:
        # Get supporting case laws and statutes
        db = get_database()
        
        supporting_cases = await db.case_laws.find({
            "citation": {"$in": draft_request.supporting_cases}
        }).to_list(length=50)
        
        supporting_statutes = await db.statutes.find({
            "_id": {"$in": draft_request.supporting_statutes}
        }).to_list(length=50)
        
        # Draft document
        drafted_text = await ai_service.draft_document(
            document_type=draft_request.document_type,
            facts=draft_request.facts,
            parties=draft_request.parties,
            legal_grounds=draft_request.legal_grounds,
            prayer=draft_request.prayer,
            supporting_materials={
                "cases": [c["citation"] for c in supporting_cases],
                "statutes": [s["act_name"] for s in supporting_statutes]
            }
        )
        
        # Save draft
        draft_request.generated_text = drafted_text
        result = await db.document_drafts.insert_one(draft_request.dict())
        
        return {"draft_id": str(result.inserted_id), "text": drafted_text}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/cases/search")
async def search_cases(
    query: str,
    court: str = None,
    year: int = None,
    domain: str = None,
    limit: int = 10
):
    """Search case laws"""
    try:
        db = get_database()
        
        # Build search filter
        search_filter = {}
        if court:
            search_filter["court"] = court
        if year:
            search_filter["year"] = year
        if domain:
            search_filter["legal_domain"] = domain
        
        # Text search
        search_filter["$text"] = {"$search": query}
        
        cases = await db.case_laws.find(search_filter).limit(limit).to_list(length=limit)
        
        return cases
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/statutes/section")
async def get_statute_section(act_name: str, section: str):
    """Get specific section of an act"""
    try:
        db = get_database()
        
        statute = await db.statutes.find_one({
            "act_name": act_name,
            "sections.section": section
        })
        
        if not statute:
            raise HTTPException(status_code=404, detail="Section not found")
        
        # Extract specific section
        section_content = next(
            (s for s in statute["sections"] if s["section"] == section),
            None
        )
        
        return section_content
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/limitation/calculate")
async def calculate_limitation(
    cause_of_action_date: str,
    act: str,
    case_type: str
):
    """Calculate limitation period"""
    # Implement limitation calculation logic
    pass
```

### Step 2.7: Main FastAPI Application

**backend/app/main.py:**
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database.mongodb import connect_to_mongo, close_mongo_connection
from app.api.routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_to_mongo()
    yield
    # Shutdown
    await close_mongo_connection()

app = FastAPI(
    title="Legal AI Assistant API",
    description="AI-powered legal research and drafting assistant",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router, prefix="/api/v1", tags=["legal"])

@app.get("/")
async def root():
    return {
        "message": "Legal AI Assistant API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

## PHASE 3: FRONTEND DEVELOPMENT (Weeks 5-6)

### Step 3.1: Create Main Components

**frontend/src/components/QueryInterface.tsx:**
```typescript
import React, { useState } from 'react';
import axios from 'axios';
import { TextField, Button, Paper, CircularProgress } from '@mui/material';

const QueryInterface: React.FC = () => {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const result = await axios.post('http://localhost:8000/api/v1/query/research', {
        query_text: query,
        query_type: 'research'
      });
      setResponse(result.data);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Paper style={{ padding: '20px', margin: '20px' }}>
      <TextField
        fullWidth
        multiline
        rows={4}
        variant="outlined"
        label="Enter your legal query"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <Button
        variant="contained"
        color="primary"
        onClick={handleSubmit}
        disabled={loading}
        style={{ marginTop: '10px' }}
      >
        {loading ? <CircularProgress size={24} /> : 'Research'}
      </Button>
      
      {response && (
        <div style={{ marginTop: '20px' }}>
          <h3>Response:</h3>
          <div>{response.response_text}</div>
          
          <h4>Relevant Cases:</h4>
          <ul>
            {response.relevant_cases.map((c: any, i: number) => (
              <li key={i}>
                <strong>{c.case_name}</strong> - {c.citation}
                <br />
                {c.ratio_decidendi}
              </li>
            ))}
          </ul>
        </div>
      )}
    </Paper>
  );
};

export default QueryInterface;
```

---

## PHASE 4: DATA POPULATION (Weeks 7-8)

### Step 4.1: Data Collection Script

**backend/scripts/populate_database.py:**
```python
import asyncio
from pymongo import MongoClient
import json
from datetime import datetime

async def populate_case_laws():
    """Populate database with case laws"""
    client = MongoClient("mongodb://localhost:27017/")
    db = client["legal_ai_db"]
    
    # Sample case law data
    sample_cases = [
        {
            "case_name": "Kesavananda Bharati v. State of Kerala",
            "citation": "AIR 1973 SC 1461",
            "court": "Supreme Court",
            "year": 1973,
            "judges": ["S.M. Sikri", "K.S. Hegde", "A.N. Grover"],
            "ratio_decidendi": "Basic Structure Doctrine - Parliament cannot amend the Constitution to destroy its basic structure",
            "legal_domain": ["Constitutional Law"],
            "relevant_sections": ["Article 368"],
            "headnotes": "Landmark case establishing the basic structure doctrine",
            "full_text": "...",  # Full judgment text
            "current_status": "Valid",
            "keywords": ["basic structure", "constitutional amendment", "judicial review"]
        },
        # Add more cases...
    ]
    
    result = db.case_laws.insert_many(sample_cases)
    print(f"Inserted {len(result.inserted_ids)} case laws")

async def populate_statutes():
    """Populate database with statutes"""
    # Implement statute population
    pass

if __name__ == "__main__":
    asyncio.run(populate_case_laws())
    asyncio.run(populate_statutes())
```

---

## PHASE 5: TESTING & DEPLOYMENT (Weeks 9-10)

### Step 5.1: Testing

Create test files in `backend/tests/`:

```python
# tests/test_api.py
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_legal_research():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/v1/query/research", json={
            "query_text": "What is the limitation period for filing a consumer complaint?",
            "query_type": "research"
        })
    assert response.status_code == 200
    assert "limitation" in response.json()["response_text"].lower()
```

### Step 5.2: Docker Setup

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  mongodb:
    image: mongo:latest
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db
  
  redis:
    image: redis:latest
    ports:
      - "6379:6379"
  
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    depends_on:
      - mongodb
      - redis
    environment:
      - MONGODB_URI=mongodb://mongodb:27017/
  
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend

volumes:
  mongo_data:
```

---

## NEXT STEPS & ENHANCEMENTS

1. **Advanced Features:**
   - Citation validator
   - Court fee calculator
   - Limitation period calculator
   - Multi-lingual support (Hindi, regional languages)
   - Document OCR for scanned judgments
   - Legal dictionary/glossary

2. **Security:**
   - User authentication (JWT)
   - Role-based access control
   - Audit logging
   - Data encryption

3. **Performance:**
   - Redis caching for common queries
   - Query optimization
   - Load balancing
   - CDN for static assets

4. **Integration:**
   - Court website APIs
   - Government legal databases
   - E-filing systems
   - Payment gateways for court fees

---

## LEARNING RESOURCES

1. **FastAPI:** https://fastapi.tiangolo.com/
2. **LangChain:** https://python.langchain.com/
3. **Vector Databases:** Pinecone documentation
4. **React + TypeScript:** Official React documentation
5. **Indian Legal System:** Bare Acts from IndiaCode.nic.in

---

## ESTIMATED TIMELINE

- **Week 1-2:** Setup & Backend foundation
- **Week 3-4:** AI integration & API development
- **Week 5-6:** Frontend development
- **Week 7-8:** Data population
- **Week 9-10:** Testing & deployment
- **Week 11-12:** Refinement & additional features

---

## SUPPORT & MAINTENANCE

1. Regular updates for new judgments
2. Legislative amendment tracking
3. Bug fixes and improvements
4. User feedback integration
5. Performance monitoring

---

**Remember:** Start small, test frequently, and iterate based on feedback!
