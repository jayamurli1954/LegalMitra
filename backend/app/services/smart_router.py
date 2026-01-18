"""
Smart Model Router for LegalMitra
Automatically selects the best AI model based on query complexity and user preferences
"""

from typing import Dict, Optional, Tuple
import re


class SmartModelRouter:
    """
    Intelligently routes queries to appropriate AI models based on:
    - Query complexity
    - Query type (simple/moderate/complex)
    - Cost vs quality preferences
    - Task type (template filling, research, analysis)
    """

    def __init__(self):
        # Model tiers based on capability and cost
        self.models = {
            "budget": [
                {
                    "id": "google/gemini-flash-1.5",
                    "name": "Gemini Flash",
                    "cost_per_1m": 0.10,
                    "quality_score": 7,
                    "speed": "fast",
                    "max_tokens": 1000000
                },
                {
                    "id": "meta-llama/llama-3.1-70b-instruct",
                    "name": "Llama 3.1 70B",
                    "cost_per_1m": 0.18,
                    "quality_score": 7.5,
                    "speed": "fast",
                    "max_tokens": 128000
                }
            ],
            "balanced": [
                {
                    "id": "anthropic/claude-3-haiku",
                    "name": "Claude 3 Haiku",
                    "cost_per_1m": 0.25,
                    "quality_score": 8.5,
                    "speed": "fast",
                    "max_tokens": 200000
                },
                {
                    "id": "openai/gpt-4o-mini",
                    "name": "GPT-4o Mini",
                    "cost_per_1m": 0.15,
                    "quality_score": 8,
                    "speed": "medium",
                    "max_tokens": 128000
                }
            ],
            "premium": [
                {
                    "id": "anthropic/claude-3.5-sonnet",
                    "name": "Claude 3.5 Sonnet",
                    "cost_per_1m": 3.00,
                    "quality_score": 9.5,
                    "speed": "medium",
                    "max_tokens": 200000
                },
                {
                    "id": "google/gemini-pro-1.5",
                    "name": "Gemini Pro 1.5",
                    "cost_per_1m": 3.50,
                    "quality_score": 9,
                    "speed": "medium",
                    "max_tokens": 1000000
                },
                {
                    "id": "openai/gpt-4-turbo",
                    "name": "GPT-4 Turbo",
                    "cost_per_1m": 10.00,
                    "quality_score": 10,
                    "speed": "slow",
                    "max_tokens": 128000
                }
            ]
        }

    def analyze_query_complexity(self, query: str, query_type: str = "research") -> Dict:
        """
        Analyze query to determine complexity level
        Returns: Dict with complexity score and characteristics
        """
        complexity_score = 0
        characteristics = []

        # Length analysis
        word_count = len(query.split())
        if word_count > 100:
            complexity_score += 3
            characteristics.append("long_query")
        elif word_count > 50:
            complexity_score += 2
            characteristics.append("medium_query")
        else:
            complexity_score += 1
            characteristics.append("short_query")

        # Legal complexity indicators
        complex_legal_terms = [
            "section", "act", "regulation", "amendment", "notification",
            "precedent", "judgment", "ratio decidendi", "obiter dicta",
            "constitutional", "statutory", "tribunal", "appellate",
            "detailed analysis", "comprehensive", "exhaustive",
            "comparative study", "multi-jurisdictional"
        ]

        complex_term_count = sum(1 for term in complex_legal_terms if term in query.lower())
        complexity_score += complex_term_count * 0.5

        if complex_term_count > 3:
            characteristics.append("legal_complex")

        # Task-based complexity
        complex_tasks = [
            "draft", "prepare", "analyze", "compare", "evaluate",
            "comprehensive", "detailed", "explain in detail",
            "pros and cons", "advantages and disadvantages"
        ]

        if any(task in query.lower() for task in complex_tasks):
            complexity_score += 2
            characteristics.append("complex_task")

        # Simple queries
        simple_indicators = [
            "what is", "define", "meaning of", "simple explanation",
            "quick question", "brief", "summary"
        ]

        if any(ind in query.lower() for ind in simple_indicators):
            complexity_score -= 1
            characteristics.append("simple_task")

        # GST 2.0 and recent amendments (high priority, need accuracy)
        if any(term in query.lower() for term in ["gst 2.0", "latest amendment", "recent change", "2025", "2026"]):
            complexity_score += 2
            characteristics.append("recent_updates")

        # Template filling is usually simple
        if query_type == "template_fill":
            complexity_score = max(1, complexity_score - 2)
            characteristics.append("template_task")

        # Cap complexity score
        complexity_score = max(1, min(10, complexity_score))

        return {
            "score": complexity_score,
            "level": self._get_complexity_level(complexity_score),
            "characteristics": characteristics,
            "word_count": word_count
        }

    def _get_complexity_level(self, score: float) -> str:
        """Convert complexity score to level"""
        if score <= 3:
            return "simple"
        elif score <= 6:
            return "moderate"
        else:
            return "complex"

    def select_model(
        self,
        query: str,
        query_type: str = "research",
        user_preference: str = "balanced",
        max_cost_per_query: Optional[float] = None
    ) -> Tuple[str, Dict]:
        """
        Select the best model for the query

        Args:
            query: The user's query
            query_type: Type of query (research, template_fill, draft, etc.)
            user_preference: budget/balanced/premium/auto
            max_cost_per_query: Maximum cost willing to pay per query (USD)

        Returns:
            Tuple of (model_id, selection_info)
        """
        # Analyze query
        analysis = self.analyze_query_complexity(query, query_type)

        # Auto mode: select tier based on complexity
        if user_preference == "auto":
            if analysis["level"] == "simple":
                tier = "budget"
            elif analysis["level"] == "moderate":
                tier = "balanced"
            else:
                tier = "premium"
        else:
            tier = user_preference

        # Get models from selected tier
        available_models = self.models.get(tier, self.models["balanced"])

        # Filter by max cost if specified
        if max_cost_per_query:
            estimated_tokens = self._estimate_tokens(query, analysis)
            available_models = [
                m for m in available_models
                if (m["cost_per_1m"] * estimated_tokens / 1_000_000) <= max_cost_per_query
            ]

        # If no models within budget, use cheapest available
        if not available_models:
            all_models = self.models["budget"] + self.models["balanced"] + self.models["premium"]
            available_models = sorted(all_models, key=lambda x: x["cost_per_1m"])[:1]

        # Select best model from available options
        # For complex queries, prioritize quality; for simple, prioritize cost
        if analysis["level"] == "complex":
            selected = max(available_models, key=lambda x: x["quality_score"])
        else:
            # Balance between cost and quality
            selected = min(available_models, key=lambda x: x["cost_per_1m"] / x["quality_score"])

        # Calculate estimated cost
        estimated_tokens = self._estimate_tokens(query, analysis)
        estimated_cost = (selected["cost_per_1m"] * estimated_tokens) / 1_000_000

        selection_info = {
            "model": selected,
            "complexity": analysis,
            "tier_used": tier,
            "estimated_tokens": estimated_tokens,
            "estimated_cost_usd": round(estimated_cost, 4),
            "reasoning": self._get_selection_reasoning(analysis, tier, selected)
        }

        return selected["id"], selection_info

    def _estimate_tokens(self, query: str, analysis: Dict) -> int:
        """Estimate total tokens (prompt + response)"""
        # Rough estimation: 1 word ≈ 1.3 tokens
        prompt_tokens = int(len(query.split()) * 1.3)

        # Estimate response tokens based on complexity
        if analysis["level"] == "simple":
            response_tokens = 300
        elif analysis["level"] == "moderate":
            response_tokens = 1000
        else:
            response_tokens = 2500

        return prompt_tokens + response_tokens

    def _get_selection_reasoning(self, analysis: Dict, tier: str, model: Dict) -> str:
        """Generate human-readable reasoning for model selection"""
        reasons = []

        complexity_msg = {
            "simple": "Simple query detected",
            "moderate": "Moderate complexity query",
            "complex": "Complex legal analysis required"
        }
        reasons.append(complexity_msg.get(analysis["level"], "Standard query"))

        if "legal_complex" in analysis["characteristics"]:
            reasons.append("Multiple legal concepts involved")

        if "recent_updates" in analysis["characteristics"]:
            reasons.append("Recent legal updates require accurate model")

        reasons.append(f"Selected {tier} tier model: {model['name']}")

        reasons.append(f"Est. cost: ${self._estimate_cost_display(model['cost_per_1m'], analysis)}")

        return " • ".join(reasons)

    def _estimate_cost_display(self, cost_per_1m: float, analysis: Dict) -> str:
        """Display estimated cost in user-friendly format"""
        tokens = self._estimate_tokens("", analysis)
        cost = (cost_per_1m * tokens) / 1_000_000
        return f"{cost:.4f}"

    def get_recommendation_for_task(self, task_type: str) -> str:
        """Get model recommendation for specific task types"""
        recommendations = {
            "template_fill": "google/gemini-flash-1.5",  # Fast and cheap
            "simple_query": "anthropic/claude-3-haiku",  # Good quality, low cost
            "legal_research": "anthropic/claude-3.5-sonnet",  # Best for legal work
            "document_draft": "anthropic/claude-3.5-sonnet",  # Quality for important docs
            "case_analysis": "openai/gpt-4-turbo",  # Deep analysis
            "compliance_check": "anthropic/claude-3-haiku",  # Balanced
            "tax_calculation": "google/gemini-flash-1.5"  # Fast and accurate
        }

        return recommendations.get(task_type, "anthropic/claude-3-haiku")


# Singleton instance
smart_router = SmartModelRouter()
