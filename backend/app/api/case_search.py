"""
Case Law Search API endpoints
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict
from app.services.ai_service import ai_service

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
        # Build search query
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








