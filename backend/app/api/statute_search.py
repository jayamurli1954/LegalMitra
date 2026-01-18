"""
Statute Search API endpoints
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

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
    
    Example:
    {
        "act_name": "CGST Act 2017",
        "section": "16"
    }
    """
    try:
        from app.services.ai_service import ai_service
        
        # Build query
        if request.section:
            query = f"Explain Section {request.section} of {request.act_name}. Provide the section text, meaning, and practical implications."
        else:
            query = f"Provide information about {request.act_name}. Include key sections, purpose, and applicability."
        
        # Get AI response
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))










