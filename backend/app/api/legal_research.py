"""
Legal Research API endpoints

Implements production-grade error handling with graceful fallbacks.
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, List
from app.services.ai_service import ai_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


class LegalQueryRequest(BaseModel):
    """Request model for legal research query"""
    query: str
    query_type: str = "research"  # research, drafting, opinion, case_prep, summary, section_lookup, interpretation
    context: Optional[Dict] = None
    relevant_cases: Optional[List[Dict]] = None
    relevant_statutes: Optional[List[Dict]] = None


class LegalQueryResponse(BaseModel):
    """Response model for legal research"""
    response: str
    query_type: str
    confidence_score: Optional[float] = None
    status: str = "success"  # success, partial, error
    mode: str = "ai"  # ai, non_ai, cached
    message: Optional[str] = None


@router.post("/legal-research", response_model=LegalQueryResponse)
async def legal_research(request: LegalQueryRequest):
    """
    Perform legal research and analysis
    
    Implements graceful fallback if AI is unavailable.
    
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
            status="success",
            mode="ai"
        )
    except RuntimeError as ai_error:
        # AI service unavailable - return graceful fallback
        error_msg = str(ai_error)
        logger.warning(f"AI service unavailable for legal research: {error_msg}")
        
        # FIX 4: Production-grade error UX with fallback
        return JSONResponse(
            status_code=503,
            content={
                "status": "partial",
                "mode": "non_ai",
                "message": "AI legal analysis temporarily unavailable. Showing verified information only.",
                "response": (
                    f"Legal research query: {request.query}\n\n"
                    "AI analysis is currently unavailable. "
                    "Please check your AI provider configuration or try again later.\n\n"
                    "For verified statute information, please use the statute search feature."
                ),
                "query_type": request.query_type,
                "confidence_score": None,
                "error": error_msg
            }
        )
            query_type=request.query_type,
            confidence_score=0.85  # Default confidence score
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """Health check for legal research service"""
    from app.core.config import get_settings
    # Clear cache to ensure fresh settings
    get_settings.cache_clear()
    settings = get_settings()
    
    provider = settings.AI_PROVIDER.lower().strip()
    
    health_info = {
        "status": "healthy",
        "service": "legal_research",
        "ai_provider": provider,
    }
    
    # Provider-specific info
    if provider in ["gemini", "google"]:
        health_info["gemini_configured"] = bool(settings.GOOGLE_GEMINI_API_KEY)
        health_info["gemini_model"] = "gemini-pro"
        health_info["rate_limit_info"] = "60 requests/minute (free tier)"
    elif provider == "grok":
        health_info["grok_configured"] = bool(settings.GROK_API_KEY)
        health_info["grok_model"] = "grok-2-1212"
    elif provider == "zai":
        health_info["zai_configured"] = bool(settings.ZAI_API_KEY)
        health_info["zai_model"] = "glm-4.6"
    elif provider == "anthropic":
        health_info["anthropic_configured"] = bool(settings.ANTHROPIC_API_KEY)
    elif provider == "openai":
        health_info["openai_configured"] = bool(settings.OPENAI_API_KEY)
    
    return health_info








