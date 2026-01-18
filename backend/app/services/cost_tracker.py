"""
Cost Tracking Service for LegalMitra
Tracks AI API usage and costs across all queries
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json
from pathlib import Path
from pydantic import BaseModel


class UsageRecord(BaseModel):
    """Single usage record"""
    timestamp: str
    model_id: str
    model_name: str
    query_type: str
    tokens_used: int
    cost_usd: float
    query_length: int


class CostTracker:
    """Track and analyze AI API costs"""

    def __init__(self):
        self.data_dir = Path(__file__).parent.parent / "data"
        self.data_dir.mkdir(exist_ok=True)
        self.usage_file = self.data_dir / "usage_history.json"
        self._load_history()

    def _load_history(self):
        """Load usage history from file"""
        if self.usage_file.exists():
            with open(self.usage_file, 'r') as f:
                self.history = json.load(f)
        else:
            self.history = []

    def _save_history(self):
        """Save usage history to file"""
        with open(self.usage_file, 'w') as f:
            json.dump(self.history, f, indent=2)

    def record_usage(
        self,
        model_id: str,
        model_name: str,
        query_type: str,
        tokens_used: int,
        cost_usd: float,
        query_length: int
    ):
        """Record a single API usage"""
        record = {
            "timestamp": datetime.now().isoformat(),
            "model_id": model_id,
            "model_name": model_name,
            "query_type": query_type,
            "tokens_used": tokens_used,
            "cost_usd": cost_usd,
            "query_length": query_length
        }

        self.history.append(record)
        self._save_history()

    def get_usage_stats(self, days: int = 30) -> Dict:
        """Get usage statistics for last N days"""
        cutoff_date = datetime.now() - timedelta(days=days)

        filtered = [
            r for r in self.history
            if datetime.fromisoformat(r["timestamp"]) >= cutoff_date
        ]

        if not filtered:
            return {
                "total_queries": 0,
                "total_tokens": 0,
                "total_cost_usd": 0,
                "average_cost_per_query": 0,
                "period_days": days
            }

        total_cost = sum(r["cost_usd"] for r in filtered)
        total_tokens = sum(r["tokens_used"] for r in filtered)

        return {
            "total_queries": len(filtered),
            "total_tokens": total_tokens,
            "total_cost_usd": round(total_cost, 4),
            "average_cost_per_query": round(total_cost / len(filtered), 4) if filtered else 0,
            "average_tokens_per_query": int(total_tokens / len(filtered)) if filtered else 0,
            "period_days": days,
            "period_start": cutoff_date.isoformat(),
            "period_end": datetime.now().isoformat()
        }

    def get_cost_by_model(self, days: int = 30) -> List[Dict]:
        """Get cost breakdown by model"""
        cutoff_date = datetime.now() - timedelta(days=days)

        filtered = [
            r for r in self.history
            if datetime.fromisoformat(r["timestamp"]) >= cutoff_date
        ]

        # Group by model
        by_model = {}
        for record in filtered:
            model_id = record["model_id"]
            if model_id not in by_model:
                by_model[model_id] = {
                    "model_id": model_id,
                    "model_name": record["model_name"],
                    "queries": 0,
                    "total_tokens": 0,
                    "total_cost_usd": 0
                }

            by_model[model_id]["queries"] += 1
            by_model[model_id]["total_tokens"] += record["tokens_used"]
            by_model[model_id]["total_cost_usd"] += record["cost_usd"]

        # Convert to list and round costs
        result = []
        for stats in by_model.values():
            stats["total_cost_usd"] = round(stats["total_cost_usd"], 4)
            stats["avg_cost_per_query"] = round(
                stats["total_cost_usd"] / stats["queries"], 4
            ) if stats["queries"] > 0 else 0
            result.append(stats)

        # Sort by cost descending
        result.sort(key=lambda x: x["total_cost_usd"], reverse=True)

        return result

    def get_cost_by_query_type(self, days: int = 30) -> List[Dict]:
        """Get cost breakdown by query type"""
        cutoff_date = datetime.now() - timedelta(days=days)

        filtered = [
            r for r in self.history
            if datetime.fromisoformat(r["timestamp"]) >= cutoff_date
        ]

        # Group by query type
        by_type = {}
        for record in filtered:
            qtype = record["query_type"]
            if qtype not in by_type:
                by_type[qtype] = {
                    "query_type": qtype,
                    "queries": 0,
                    "total_cost_usd": 0
                }

            by_type[qtype]["queries"] += 1
            by_type[qtype]["total_cost_usd"] += record["cost_usd"]

        # Convert to list
        result = []
        for stats in by_type.values():
            stats["total_cost_usd"] = round(stats["total_cost_usd"], 4)
            stats["avg_cost_per_query"] = round(
                stats["total_cost_usd"] / stats["queries"], 4
            ) if stats["queries"] > 0 else 0
            result.append(stats)

        result.sort(key=lambda x: x["total_cost_usd"], reverse=True)

        return result

    def get_daily_costs(self, days: int = 30) -> List[Dict]:
        """Get daily cost breakdown"""
        cutoff_date = datetime.now() - timedelta(days=days)

        filtered = [
            r for r in self.history
            if datetime.fromisoformat(r["timestamp"]) >= cutoff_date
        ]

        # Group by date
        by_date = {}
        for record in filtered:
            date_str = record["timestamp"][:10]  # YYYY-MM-DD
            if date_str not in by_date:
                by_date[date_str] = {
                    "date": date_str,
                    "queries": 0,
                    "cost_usd": 0,
                    "tokens": 0
                }

            by_date[date_str]["queries"] += 1
            by_date[date_str]["cost_usd"] += record["cost_usd"]
            by_date[date_str]["tokens"] += record["tokens_used"]

        # Convert to list
        result = []
        for stats in by_date.values():
            stats["cost_usd"] = round(stats["cost_usd"], 4)
            result.append(stats)

        result.sort(key=lambda x: x["date"])

        return result

    def get_cost_comparison_with_vidur(self, days: int = 30) -> Dict:
        """
        Compare LegalMitra costs with VIDUR subscription cost
        VIDUR estimated at $50-100/month
        """
        stats = self.get_usage_stats(days)

        # Extrapolate to monthly if days != 30
        if days != 30:
            monthly_cost = (stats["total_cost_usd"] / days) * 30
        else:
            monthly_cost = stats["total_cost_usd"]

        vidur_min_cost = 50  # USD per month
        vidur_max_cost = 100  # USD per month
        vidur_avg_cost = 75

        savings_min = vidur_min_cost - monthly_cost
        savings_max = vidur_max_cost - monthly_cost
        savings_avg = vidur_avg_cost - monthly_cost

        savings_percent_min = (savings_min / vidur_min_cost) * 100 if vidur_min_cost > 0 else 0
        savings_percent_max = (savings_max / vidur_max_cost) * 100 if vidur_max_cost > 0 else 0

        return {
            "legalmitra_monthly_cost": round(monthly_cost, 2),
            "vidur_estimated_cost": {
                "min": vidur_min_cost,
                "max": vidur_max_cost,
                "average": vidur_avg_cost
            },
            "savings": {
                "min_usd": round(savings_min, 2),
                "max_usd": round(savings_max, 2),
                "average_usd": round(savings_avg, 2),
                "percent_min": round(savings_percent_min, 1),
                "percent_max": round(savings_percent_max, 1)
            },
            "message": self._get_savings_message(monthly_cost, savings_avg)
        }

    def _get_savings_message(self, legalmitra_cost: float, savings: float) -> str:
        """Generate user-friendly savings message"""
        if legalmitra_cost < 1:
            return f"🎉 You're spending less than $1/month! Saving ${savings:.2f} vs VIDUR"
        elif legalmitra_cost < 10:
            return f"💰 Great value! Spending ${legalmitra_cost:.2f}/month, saving ${savings:.2f} vs VIDUR"
        elif savings > 0:
            return f"✅ Still saving ${savings:.2f}/month compared to VIDUR subscription"
        else:
            return f"⚠️ Your usage (${legalmitra_cost:.2f}/month) exceeds typical VIDUR subscription cost"

    def get_all_records(self, limit: int = 100) -> List[Dict]:
        """Get recent usage records"""
        return self.history[-limit:] if len(self.history) > limit else self.history


# Singleton instance
cost_tracker = CostTracker()
