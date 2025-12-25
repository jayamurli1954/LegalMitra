# LegalMitra Web Integration Implementation Plan

## Goal
Enable LegalMitra to fetch latest legal information from official government and legal websites for more accurate, up-to-date responses.

## Target Websites

### Judicial & Court Websites:
- eCourts Services
- National Judicial Data Grid (NJDG)
- Supreme Court of India Website

### Legislative & Legal Websites:
- India Code (indiancode.nic.in)
- eGazette Portal (egazette.nic.in)
- Legislative Department website
- Department of Legal Affairs website
- Ministry of Parliamentary Affairs website
- PRS Legislative Research (prsindia.org)
- Press Information Bureau (PIB)

## Implementation Approach

### Phase 1: Web Search Integration (Quickest - Recommended to Start)

**Use Google Custom Search API or Serper API:**
- Target specific domains (site:indiancode.nic.in, site:egazette.nic.in, etc.)
- Search when user queries about latest amendments/recent changes
- Include search results in AI prompt
- Provide citations to source websites

**Benefits:**
- ✅ Fast to implement
- ✅ Respects website ToS
- ✅ Gets latest information
- ✅ Provides citations

**Implementation Steps:**
1. Add `google-api-python-client` or `serper` package
2. Create web search service module
3. Integrate into `process_legal_query()` method
4. Enhance prompt with search results

---

### Phase 2: Direct Website Scraping (For Specific Sites)

**For sites that allow automated access:**
- India Code (check ToS)
- eGazette Portal (check ToS)
- PIB (public information, usually allowed)

**Implementation Steps:**
1. Check Terms of Service for each site
2. Check robots.txt files
3. Implement respectful scraping (rate limiting)
4. Cache results to avoid repeated requests
5. Parse and structure legal documents

---

### Phase 3: RAG (Retrieval Augmented Generation) System

**Build comprehensive legal document database:**
- Download legal documents from official sources
- Store in vector database (Chroma, Pinecone, Weaviate)
- Retrieve relevant documents during queries
- Generate responses based on actual legal text

**Benefits:**
- ✅ Very accurate
- ✅ Fast retrieval
- ✅ Direct citations
- ✅ Can index entire legal databases

---

## Recommended Implementation: Phase 1 (Web Search)

### Step 1: Add Dependencies

```bash
pip install google-api-python-client beautifulsoup4
# OR
pip install serper
```

### Step 2: Create Web Search Service

Create `backend/app/services/web_search_service.py`:

```python
import httpx
from typing import List, Dict
from app.core.config import get_settings

class WebSearchService:
    """Service for searching legal websites"""
    
    LEGAL_SITES = [
        "site:indiancode.nic.in",
        "site:egazette.nic.in",
        "site:prsindia.org",
        "site:pib.gov.in",
        "site:legislative.gov.in",
        "site:legalaffairs.gov.in",
        "site:mpa.gov.in",
        "site:ecourts.gov.in",
        "site:njdg.ecourts.gov.in",
        "site:main.sci.gov.in"
    ]
    
    async def search_legal_sites(self, query: str, max_results: int = 5) -> List[Dict]:
        """
        Search legal websites for latest information
        Returns: List of {title, url, snippet}
        """
        # Implementation using Google Custom Search API or Serper API
        pass
```

### Step 3: Integrate into AI Service

Modify `process_legal_query()` to:
1. Detect if query needs latest information
2. Search legal websites
3. Include search results in prompt
4. Generate response based on latest information

---

## Legal Compliance Checklist

Before implementing:

- [ ] Review Terms of Service for each website
- [ ] Check robots.txt files
- [ ] Implement rate limiting (respectful scraping)
- [ ] Add proper attribution/citations
- [ ] Cache data appropriately
- [ ] Handle errors gracefully
- [ ] Respect copyright (use information, not exact copies)
- [ ] Use official APIs where available
- [ ] Add user agent identification
- [ ] Implement timeout handling

---

## Benefits of Integration

1. **Real-Time Accuracy**: Get latest amendments as published
2. **Official Sources**: Information directly from government websites
3. **Citations**: Provide exact links to source documents
4. **Credibility**: References official government sources
5. **Completeness**: Access comprehensive legal databases
6. **Competitive Advantage**: Makes LegalMitra superior to general AI

---

## Next Steps

**Would you like me to implement Phase 1 (Web Search Integration)?**

This would:
1. Add web search capability
2. Automatically search legal websites for latest information
3. Include search results in responses
4. Provide citations to official sources
5. Make LegalMitra more accurate and up-to-date

**Note**: This requires a Google Custom Search API key or Serper API key (paid service, but affordable).

---

**Conclusion**: Referencing these websites is legal. Implementing web integration would significantly enhance LegalMitra's accuracy and make it a true specialized legal AI assistant with access to the latest legal information.


