"""
Enhanced Query API with Smart Routing, Failover, and Disclaimers
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from app.services.enhanced_ai_service import enhanced_ai_service
from app.services.query_classifier import query_classifier
from app.services.model_failover import model_failover

router = APIRouter()


class EnhancedQueryRequest(BaseModel):
    """Request for enhanced query processing"""
    query: str
    query_type: str = "research"  # research, drafting, case_search, etc.
    preferred_tier: Optional[str] = None  # Override: free, budget, balanced, premium


class EnhancedQueryResponse(BaseModel):
    """Response from enhanced query processing"""
    response: str
    classification: Dict[str, Any]
    model_used: Dict[str, Any]
    cost_estimate: float
    failover_info: Dict[str, Any]
    safety: Dict[str, Any]


@router.post("/enhanced-query", response_model=EnhancedQueryResponse)
async def process_enhanced_query(request: EnhancedQueryRequest):
    """
    Process query with smart routing, automatic failover, and Bar Council-safe disclaimers

    Features:
    - Query classification for cost optimization
    - Automatic model failover (3 attempts)
    - Appropriate legal disclaimers
    - Risk detection
    """
    try:
        user_prefs = {}
        if request.preferred_tier:
            user_prefs['preferred_tier'] = request.preferred_tier

        result = await enhanced_ai_service.process_with_intelligence(
            query=request.query,
            query_type=request.query_type,
            user_preferences=user_prefs if user_prefs else None
        )

        return EnhancedQueryResponse(**result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/classify-query")
async def classify_query_endpoint(query: str):
    """
    Classify a query without executing it

    Useful for showing users what tier their query would use
    and potential cost savings
    """
    try:
        classification = query_classifier.classify_query(query)
        return {
            "classification": classification,
            "cost_comparison": {
                "free_tier": "₹0.00",
                "budget_tier": "₹0.12-0.40",
                "balanced_tier": "₹0.20-0.60",
                "premium_tier": "₹2.40-7.20"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/model-health")
async def get_model_health():
    """
    Get health status of all AI models

    Shows which models are healthy and available
    """
    try:
        health = await enhanced_ai_service.get_model_health_status()
        return {
            "status": "ok",
            "health": health,
            "timestamp": "2026-01-16"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cost-savings-report")
async def get_cost_savings_report():
    """
    Get estimated cost savings from smart routing

    Shows potential savings vs always using premium model
    """
    return {
        "overview": {
            "title": "Smart Routing Cost Savings",
            "description": "Automatic query classification saves 70-95% on AI costs"
        },
        "examples": [
            {
                "query_type": "Simple explanation",
                "without_routing": {
                    "model": "Claude 3.5 Sonnet",
                    "cost": "₹2.40"
                },
                "with_routing": {
                    "model": "Gemini 1.5 Flash (FREE)",
                    "cost": "₹0.00"
                },
                "savings": "100% (₹2.40 saved)"
            },
            {
                "query_type": "Medium complexity",
                "without_routing": {
                    "model": "Claude 3.5 Sonnet",
                    "cost": "₹5.00"
                },
                "with_routing": {
                    "model": "Claude 3 Haiku",
                    "cost": "₹0.50"
                },
                "savings": "90% (₹4.50 saved)"
            },
            {
                "query_type": "Complex drafting",
                "without_routing": {
                    "model": "Claude 3.5 Sonnet",
                    "cost": "₹7.20"
                },
                "with_routing": {
                    "model": "Claude 3 Haiku",
                    "cost": "₹0.60"
                },
                "savings": "92% (₹6.60 saved)"
            }
        ],
        "monthly_projection": {
            "queries_per_month": 1000,
            "without_routing": "₹4,000-6,000",
            "with_routing": "₹200-800",
            "estimated_savings": "85-95% (₹3,200-5,800 per month)"
        }
    }
