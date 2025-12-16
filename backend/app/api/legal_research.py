"""
Legal Research API endpoints
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, List
from app.services.ai_service import ai_service

router = APIRouter()


class LegalQueryRequest(BaseModel):
    """Request model for legal research query"""
    query: str
    query_type: str = "research"  # research, drafting, opinion, case_prep
    context: Optional[Dict] = None
    relevant_cases: Optional[List[Dict]] = None
    relevant_statutes: Optional[List[Dict]] = None


class LegalQueryResponse(BaseModel):
    """Response model for legal research"""
    response: str
    query_type: str
    confidence_score: Optional[float] = None


@router.post("/legal-research", response_model=LegalQueryResponse)
async def legal_research(request: LegalQueryRequest):
    """
    Perform legal research and analysis
    
    Example:
    {
        "query": "What is the limitation period for filing a GST appeal?",
        "query_type": "research"
    }
    """
    try:
        response_text = await ai_service.process_legal_query(
            query=request.query,
            query_type=request.query_type,
            context=request.context,
            relevant_cases=request.relevant_cases,
            relevant_statutes=request.relevant_statutes
        )
        
        return LegalQueryResponse(
            response=response_text,
            query_type=request.query_type,
            confidence_score=0.85  # Default confidence score
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """Health check for legal research service"""
    from app.core.config import get_settings
    settings = get_settings()
    
    health_info = {
        "status": "healthy",
        "service": "legal_research",
        "ai_provider": settings.AI_PROVIDER,
        "gemini_configured": bool(settings.GOOGLE_GEMINI_API_KEY),
    }
    
    # If using Gemini, show model info
    if settings.AI_PROVIDER.lower() in ["gemini", "google"]:
        health_info["gemini_model"] = "gemini-pro"
        health_info["rate_limit_info"] = "60 requests/minute (free tier)"
    
    return health_info








