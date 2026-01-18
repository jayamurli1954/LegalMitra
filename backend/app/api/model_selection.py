"""
Model Selection API - Allows users to choose AI models via OpenRouter
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from app.services.openrouter_service import openrouter_service

router = APIRouter()


class ModelInfo(BaseModel):
    """Model information"""
    id: str
    name: str
    tier: str  # premium, balanced, budget
    cost_per_1m_tokens: str
    best_for: str
    context_length: str


class ModelListResponse(BaseModel):
    """Response with available models"""
    models: List[ModelInfo]
    current_model: str


@router.get("/models/recommended", response_model=List[Dict[str, str]])
async def get_recommended_models():
    """
    Get recommended models for legal work
    Categorized by tier: premium, balanced, budget
    """
    try:
        models = await openrouter_service.get_recommended_models_for_legal()
        return models
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/models/all")
async def get_all_models():
    """
    Get complete list of all available models from OpenRouter
    """
    try:
        models = await openrouter_service.get_available_models()
        return {"models": models, "count": len(models)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/models/{model_id}")
async def get_model_details(model_id: str):
    """
    Get detailed information about a specific model
    """
    try:
        # Decode URL-encoded model ID (e.g., anthropic%2Fclaude-3.5-sonnet)
        import urllib.parse
        model_id = urllib.parse.unquote(model_id)

        model_info = await openrouter_service.get_model_info(model_id)
        if not model_info:
            raise HTTPException(status_code=404, detail="Model not found")
        return model_info
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/models/estimate-cost")
async def estimate_cost(model_id: str, prompt_tokens: int, response_tokens: int = 1000):
    """
    Estimate cost for a query with given model
    """
    try:
        total_tokens = prompt_tokens + response_tokens
        cost = openrouter_service._estimate_cost(model_id, total_tokens)

        return {
            "model_id": model_id,
            "prompt_tokens": prompt_tokens,
            "response_tokens": response_tokens,
            "total_tokens": total_tokens,
            "estimated_cost_usd": round(cost, 4)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
