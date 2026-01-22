"""
Statute Search API endpoints
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


class StatuteSearchRequest(BaseModel):
    """Request model for statute search"""
    act_name: str
    section: Optional[str] = None


class StatuteSearchResponse(BaseModel):
    """Response model for statute search"""
    act_name: str
    section: Optional[str] = None
    content: str
    explanation: Optional[str] = None


@router.post("/search-statute", response_model=StatuteSearchResponse)
async def search_statute(request: StatuteSearchRequest):
    """
    Search for statute/section information
    
    FIX 4: Includes graceful fallback when AI service is unavailable.
    
    Example:
    {
        "act_name": "CGST Act 2017",
        "section": "16"
    }
    """
    try:
        from app.services.ai_service import ai_service
        from app.core.config import get_settings
        
        # FIX 4: Check if AI service is available before attempting query
        settings = get_settings()
        ai_provider = settings.AI_PROVIDER.lower().strip()
        ai_available = False
        
        # Check AI client availability
        if ai_provider == "gemini":
            # For Gemini, check if client exists or can be initialized
            if hasattr(ai_service, '_gemini_client') and ai_service._gemini_client is not None:
                ai_available = True
            else:
                # Try to initialize
                try:
                    ai_service._initialize_gemini_client()
                    ai_available = ai_service._gemini_client is not None
                except Exception as init_error:
                    logger.warning(f"Gemini client not available: {init_error}")
                    ai_available = False
        elif ai_provider == "anthropic":
            ai_available = hasattr(ai_service, '_anthropic_client') and ai_service._anthropic_client is not None
        elif ai_provider == "openai":
            ai_available = hasattr(ai_service, '_openai_client') and ai_service._openai_client is not None
        else:
            # For other providers, assume available (will fail gracefully if not)
            ai_available = True
        
        # FIX 4: Graceful fallback if AI is not available
        if not ai_available:
            logger.warning(f"AI service unavailable for provider '{ai_provider}'. Returning fallback response.")
            return JSONResponse(
                status_code=503,
                content={
                    "error": "AI service unavailable",
                    "message": "Legal research AI is temporarily unavailable. "
                               "Statute search is running in keyword-only mode.",
                    "act_name": request.act_name,
                    "section": request.section,
                    "content": (
                        f"Statute search for {request.act_name}"
                        + (f", Section {request.section}" if request.section else "")
                        + " is currently unavailable. "
                        "Please check your AI provider configuration or try again later."
                    ),
                    "explanation": (
                        "The AI service is not available. "
                        "Please ensure your API keys are correctly configured in the environment variables."
                    )
                }
            )
        
        # Build query
        if request.section:
            query = f"Explain Section {request.section} of {request.act_name}. Provide the section text, meaning, and practical implications."
        else:
            query = f"Provide information about {request.act_name}. Include key sections, purpose, and applicability."
        
        # Get AI response
        try:
            response_text = await ai_service.process_legal_query(
                query=query,
                query_type="research"
            )
            
            return StatuteSearchResponse(
                act_name=request.act_name,
                section=request.section,
                content=response_text,
                explanation=response_text
            )
        except RuntimeError as ai_error:
            # FIX 4: Catch AI initialization errors and return graceful response
            logger.error(f"AI query failed: {ai_error}")
            return JSONResponse(
                status_code=503,
                content={
                    "error": "AI service error",
                    "message": "Legal research AI encountered an error. "
                               "Please check your AI provider configuration.",
                    "act_name": request.act_name,
                    "section": request.section,
                    "content": f"Unable to process query for {request.act_name} due to AI service error.",
                    "explanation": str(ai_error)
                }
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in search_statute: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")










