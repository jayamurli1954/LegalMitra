"""
Document Drafting API endpoints
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
from app.services.ai_service import ai_service

router = APIRouter()


class DocumentDraftRequest(BaseModel):
    """Request model for document drafting"""
    document_type: str  # petition, reply, notice, opinion
    facts: str
    parties: Dict[str, str]
    legal_grounds: List[str]
    prayer: str
    supporting_cases: Optional[List[str]] = None
    supporting_statutes: Optional[List[str]] = None


class DocumentDraftResponse(BaseModel):
    """Response model for document drafting"""
    drafted_document: str
    document_type: str


@router.post("/draft-document", response_model=DocumentDraftResponse)
async def draft_document(request: DocumentDraftRequest):
    """
    Draft a legal document
    
    Example:
    {
        "document_type": "legal notice",
        "facts": "Client has not paid invoice of Rs. 10 lakhs",
        "parties": {
            "sender": "ABC Company",
            "recipient": "XYZ Ltd"
        },
        "legal_grounds": ["Breach of contract", "Recovery of dues"],
        "prayer": "Payment of Rs. 10 lakhs within 15 days"
    }
    """
    try:
        supporting_materials = None
        if request.supporting_cases or request.supporting_statutes:
            supporting_materials = {
                "cases": request.supporting_cases or [],
                "statutes": request.supporting_statutes or []
            }
        
        drafted_text = await ai_service.draft_document(
            document_type=request.document_type,
            facts=request.facts,
            parties=request.parties,
            legal_grounds=request.legal_grounds,
            prayer=request.prayer,
            supporting_materials=supporting_materials
        )
        
        return DocumentDraftResponse(
            drafted_document=drafted_text,
            document_type=request.document_type
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))










