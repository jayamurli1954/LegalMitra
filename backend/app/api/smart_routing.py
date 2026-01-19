"""
Smart Routing API - Model selection based on query complexity
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict
from typing import Optional
from app.services.smart_router import smart_router

router = APIRouter()


class AnalyzeQueryRequest(BaseModel):
    query: str
    query_type: str = "research"


class ModelSelectionRequest(BaseModel):
    query: str
    query_type: str = "research"
    user_preference: str = "auto"  # budget/balanced/premium/auto
    max_cost_per_query: Optional[float] = None


class ModelSelectionResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    
    selected_model_id: str
    model_name: str
    tier: str
    complexity_level: str
    complexity_score: float
    estimated_cost_usd: float
    estimated_tokens: int
    reasoning: str


@router.post("/smart-routing/analyze")
async def analyze_query(request: AnalyzeQueryRequest):
    """Analyze query complexity without selecting a model"""
    try:
        analysis = smart_router.analyze_query_complexity(
            query=request.query,
            query_type=request.query_type
        )

        return {
            "query": request.query,
            "analysis": analysis,
            "recommendation": {
                "simple": "Use budget tier models (Gemini Flash, Llama 3.1)",
                "moderate": "Use balanced tier models (Claude Haiku, GPT-4o Mini)",
                "complex": "Use premium tier models (Claude Sonnet, GPT-4 Turbo)"
            }[analysis["level"]]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/smart-routing/select-model", response_model=ModelSelectionResponse)
async def select_model_for_query(request: ModelSelectionRequest):
    """
    Select the best model for a given query

    Modes:
    - auto: Automatically select based on complexity
    - budget: Use cheapest models
    - balanced: Balance cost and quality
    - premium: Use best quality models
    """
    try:
        model_id, selection_info = smart_router.select_model(
            query=request.query,
            query_type=request.query_type,
            user_preference=request.user_preference,
            max_cost_per_query=request.max_cost_per_query
        )

        return ModelSelectionResponse(
            selected_model_id=model_id,
            model_name=selection_info["model"]["name"],
            tier=selection_info["tier_used"],
            complexity_level=selection_info["complexity"]["level"],
            complexity_score=selection_info["complexity"]["score"],
            estimated_cost_usd=selection_info["estimated_cost_usd"],
            estimated_tokens=selection_info["estimated_tokens"],
            reasoning=selection_info["reasoning"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/smart-routing/recommendations/{task_type}")
async def get_task_recommendation(task_type: str):
    """Get recommended model for specific task type"""
    try:
        recommended_model = smart_router.get_recommendation_for_task(task_type)

        task_descriptions = {
            "template_fill": "Filling document templates - uses fast, cost-effective model",
            "simple_query": "Simple legal questions - balanced cost and quality",
            "legal_research": "In-depth legal research - premium quality model",
            "document_draft": "Drafting legal documents - premium quality for accuracy",
            "case_analysis": "Detailed case analysis - highest quality model",
            "compliance_check": "Compliance verification - balanced model",
            "tax_calculation": "Tax calculations and computations - fast and accurate"
        }

        return {
            "task_type": task_type,
            "recommended_model": recommended_model,
            "description": task_descriptions.get(task_type, "General legal task"),
            "note": "This is a recommendation. You can override with user_preference parameter."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
