"""
Cost Tracking API - Monitor and analyze AI API usage costs
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict
from typing import List, Dict
from app.services.cost_tracker import cost_tracker

router = APIRouter()


class RecordUsageRequest(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    
    model_id: str
    model_name: str
    query_type: str
    tokens_used: int
    cost_usd: float
    query_length: int


@router.post("/cost-tracking/record")
async def record_usage(request: RecordUsageRequest):
    """Record a single API usage (called automatically by AI service)"""
    try:
        cost_tracker.record_usage(
            model_id=request.model_id,
            model_name=request.model_name,
            query_type=request.query_type,
            tokens_used=request.tokens_used,
            cost_usd=request.cost_usd,
            query_length=request.query_length
        )

        return {"status": "recorded", "message": "Usage recorded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cost-tracking/stats")
async def get_usage_stats(days: int = 30):
    """Get overall usage statistics"""
    try:
        stats = cost_tracker.get_usage_stats(days)
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cost-tracking/by-model")
async def get_cost_by_model(days: int = 30):
    """Get cost breakdown by AI model"""
    try:
        breakdown = cost_tracker.get_cost_by_model(days)
        return {"period_days": days, "models": breakdown}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cost-tracking/by-query-type")
async def get_cost_by_query_type(days: int = 30):
    """Get cost breakdown by query type"""
    try:
        breakdown = cost_tracker.get_cost_by_query_type(days)
        return {"period_days": days, "query_types": breakdown}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cost-tracking/daily")
async def get_daily_costs(days: int = 30):
    """Get daily cost breakdown for charting"""
    try:
        daily = cost_tracker.get_daily_costs(days)
        return {"period_days": days, "daily_costs": daily}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cost-tracking/comparison")
async def compare_with_vidur(days: int = 30):
    """Compare LegalMitra costs with VIDUR subscription"""
    try:
        comparison = cost_tracker.get_cost_comparison_with_vidur(days)
        return comparison
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cost-tracking/records")
async def get_recent_records(limit: int = 100):
    """Get recent usage records"""
    try:
        records = cost_tracker.get_all_records(limit)
        return {"count": len(records), "records": records}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cost-tracking/dashboard")
async def get_dashboard_data(days: int = 30):
    """Get all data for cost tracking dashboard"""
    try:
        stats = cost_tracker.get_usage_stats(days)
        by_model = cost_tracker.get_cost_by_model(days)
        by_type = cost_tracker.get_cost_by_query_type(days)
        daily = cost_tracker.get_daily_costs(days)
        comparison = cost_tracker.get_cost_comparison_with_vidur(days)

        return {
            "summary": stats,
            "by_model": by_model,
            "by_query_type": by_type,
            "daily_trend": daily,
            "vidur_comparison": comparison
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
