"""
Case Law Search API endpoints
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict
from app.services.ai_service import ai_service
from app.services.web_search_service import web_search_service

router = APIRouter()


class CaseSearchRequest(BaseModel):
    """Request model for case search"""
    query: str
    court: Optional[str] = None  # Supreme Court, High Court, etc.
    year: Optional[int] = None
    domain: Optional[str] = None  # Criminal, Civil, Tax, etc.


class CaseSearchResponse(BaseModel):
    """Response model for case search"""
    cases: List[Dict]
    query: str
    total_found: int


@router.post("/search-cases", response_model=CaseSearchResponse)
async def search_cases(request: CaseSearchRequest):
    """
    Search for relevant case laws
    
    Example:
    {
        "query": "arbitration clause interpretation",
        "court": "Supreme Court"
    }
    """
    try:
        # Detect if the query contains a case citation
        is_case_citation, case_citation = ai_service._detect_case_citation(request.query)
        
        # If it's a specific case citation, search the web for real case details
        if is_case_citation and web_search_service.is_available():
            try:
                print(f"🔍 Case search: Detected citation {case_citation}, searching web...")
                # Search for the specific case
                search_results = await web_search_service.search_case_citation(
                    case_citation or request.query,
                    max_results=10
                )
                
                if not search_results:
                    # Try broader search
                    search_results = await web_search_service.search_case_details(
                        request.query,
                        max_results=10
                    )
                
                if search_results:
                    print(f"📋 Found {len(search_results)} web results for case citation")
                    # Build query with web search results for AI to synthesize
                    search_context = "\n\n".join([
                        f"**{r['title']}**\nURL: {r['url']}\n{r['snippet']}"
                        for r in search_results
                    ])
                    enhanced_query = f"User is asking about case: {request.query}\n\nInformation found from case law databases:\n{search_context}\n\nProvide comprehensive case details based on the above information."
                    response_text = await ai_service.process_legal_query(
                        query=enhanced_query,
                        query_type="research"
                    )
                    return CaseSearchResponse(
                        cases=[{"content": response_text, "source": "web_search", "urls": [r['url'] for r in search_results]}],
                        query=request.query,
                        total_found=len(search_results)
                    )
            except Exception as e:
                print(f"⚠️ Web search failed in case_search: {e}")
                # Fall through to regular AI processing
        
        # Build search query for general case search
        search_query = request.query
        if request.court:
            search_query += f" in {request.court}"
        if request.year:
            search_query += f" in year {request.year}"
        if request.domain:
            search_query += f" related to {request.domain} law"
        
        # Use AI to find relevant cases
        # Note: In full implementation, this would query a vector database
        # For MVP, we use AI to provide case law citations based on the query
        response_text = await ai_service.process_legal_query(
            query=f"Find relevant case laws for: {search_query}. Provide case name, citation, court, year, and key principle.",
            query_type="research"
        )
        
        # For MVP, return the AI response as structured data
        # In production, parse the response and structure it properly
        return CaseSearchResponse(
            cases=[{"content": response_text, "source": "ai_generated"}],
            query=request.query,
            total_found=1
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))








