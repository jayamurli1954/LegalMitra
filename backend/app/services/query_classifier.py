"""
Query Classification Service for LegalMitra
Classifies queries to route them to appropriate AI models for cost optimization
"""

import re
from enum import Enum
from typing import Dict, Any


class QueryType(Enum):
    """Query type classification for routing decisions"""
    LEGAL_CORE = "legal_core"  # Premium model (drafting, complex analysis)
    EXPLAINER = "explainer"     # Free/cheap model (simple explanations)
    GENERAL = "general"         # Medium model (standard queries)


class QueryComplexity(Enum):
    """Query complexity levels"""
    SIMPLE = "simple"      # Free tier
    MEDIUM = "medium"      # Budget tier
    COMPLEX = "complex"    # Premium tier


class QueryClassifier:
    """Classifies legal queries for optimal model routing"""

    def __init__(self):
        # Keywords for LEGAL_CORE (complex, needs premium model)
        self.legal_core_keywords = [
            r'\bdraft\b', r'\bdrafting\b', r'\bnotice\b', r'\breply\b',
            r'\bagreement\b', r'\bcontract\b', r'\bpetition\b',
            r'\bsection\s+\d+', r'\bappeal\b', r'\bwrit\b',
            r'\bcompliance\b', r'\banalysis\b', r'\banalyze\b',
            r'\bcompare\b', r'\badvice\b', r'\bstrategy\b'
        ]

        # Keywords for EXPLAINER (simple, can use free tier)
        self.explainer_keywords = [
            r'\bexplain\b', r'\bwhat is\b', r'\bwhat are\b',
            r'\bmeaning\b', r'\bdefine\b', r'\bdefinition\b',
            r'\bhow to\b', r'\bwhen\b', r'\bwho\b', r'\bwhere\b',
            r'\bsimple\b', r'\bbasic\b', r'\bintroduction\b',
            r'\bsummari[sz]e\b', r'\boverview\b'
        ]

        # Complexity indicators
        self.complexity_high_keywords = [
            r'\bdetailed\b', r'\bcomprehensive\b', r'\bthorough\b',
            r'\ball sections\b', r'\ball provisions\b',
            r'\bcase law\b', r'\bprecedent\b', r'\bjudgment\b',
            r'\bmultiple\b', r'\bcomplex\b', r'\badvanced\b'
        ]

        self.complexity_low_keywords = [
            r'\bquick\b', r'\bbrief\b', r'\bshort\b',
            r'\bone\b', r'\bsingle\b', r'\bjust\b'
        ]

    def classify_query(self, query: str) -> Dict[str, Any]:
        """
        Classify a query and determine routing strategy

        Args:
            query: User's legal query

        Returns:
            Dict containing:
                - query_type: QueryType enum
                - complexity: QueryComplexity enum
                - recommended_model_tier: str (free, budget, balanced, premium)
                - estimated_tokens: int (rough estimate)
                - rationale: str (explanation of classification)
        """
        query_lower = query.lower()

        # Determine query type
        query_type = self._determine_type(query_lower)

        # Determine complexity
        complexity = self._determine_complexity(query_lower, query_type)

        # Map to model tier
        model_tier = self._map_to_model_tier(query_type, complexity)

        # Estimate token count (rough)
        estimated_tokens = self._estimate_tokens(query, complexity)

        # Generate rationale
        rationale = self._generate_rationale(query_type, complexity, model_tier)

        return {
            "query_type": query_type.value,
            "complexity": complexity.value,
            "recommended_model_tier": model_tier,
            "estimated_tokens": estimated_tokens,
            "rationale": rationale,
            "cost_savings": self._calculate_savings(complexity)
        }

    def _determine_type(self, query_lower: str) -> QueryType:
        """Determine the query type based on keywords"""

        # Check for LEGAL_CORE patterns
        for pattern in self.legal_core_keywords:
            if re.search(pattern, query_lower):
                return QueryType.LEGAL_CORE

        # Check for EXPLAINER patterns
        for pattern in self.explainer_keywords:
            if re.search(pattern, query_lower):
                return QueryType.EXPLAINER

        # Default to GENERAL
        return QueryType.GENERAL

    def _determine_complexity(self, query_lower: str, query_type: QueryType) -> QueryComplexity:
        """Determine query complexity"""

        # Count complexity indicators
        high_score = sum(1 for pattern in self.complexity_high_keywords
                        if re.search(pattern, query_lower))
        low_score = sum(1 for pattern in self.complexity_low_keywords
                       if re.search(pattern, query_lower))

        # Query length is also an indicator
        word_count = len(query_lower.split())

        # Decision logic
        if high_score > 0 or word_count > 30:
            return QueryComplexity.COMPLEX
        elif low_score > 0 or word_count < 10:
            return QueryComplexity.SIMPLE
        else:
            return QueryComplexity.MEDIUM

    def _map_to_model_tier(self, query_type: QueryType, complexity: QueryComplexity) -> str:
        """Map query type and complexity to model tier"""

        # LEGAL_CORE always gets premium or balanced model
        if query_type == QueryType.LEGAL_CORE:
            if complexity == QueryComplexity.COMPLEX:
                return "premium"  # Claude Sonnet, GPT-4
            else:
                return "balanced"  # Claude Haiku, GPT-4o-mini

        # EXPLAINER can use free/budget models
        if query_type == QueryType.EXPLAINER:
            if complexity == QueryComplexity.COMPLEX:
                return "balanced"
            else:
                return "free"  # Gemini 1.5 Flash (free tier)

        # GENERAL queries
        if complexity == QueryComplexity.COMPLEX:
            return "balanced"
        elif complexity == QueryComplexity.SIMPLE:
            return "free"
        else:
            return "budget"

    def _estimate_tokens(self, query: str, complexity: QueryComplexity) -> int:
        """Rough estimate of total tokens (input + output)"""

        input_tokens = len(query.split()) * 1.3  # Rough approximation

        # Estimate output tokens based on complexity
        if complexity == QueryComplexity.SIMPLE:
            output_tokens = 200
        elif complexity == QueryComplexity.MEDIUM:
            output_tokens = 500
        else:
            output_tokens = 1000

        return int(input_tokens + output_tokens)

    def _generate_rationale(self, query_type: QueryType, complexity: QueryComplexity, model_tier: str) -> str:
        """Generate human-readable rationale"""

        type_str = query_type.value.replace('_', ' ').title()
        complexity_str = complexity.value.title()

        return f"{type_str} query with {complexity_str} complexity → Routed to {model_tier} tier"

    def _calculate_savings(self, complexity: QueryComplexity) -> Dict[str, float]:
        """Calculate potential cost savings vs always using premium model"""

        # Cost per 1M tokens (approximate)
        costs = {
            "free": 0.0,
            "budget": 0.15,
            "balanced": 0.25,
            "premium": 3.00
        }

        # Estimate tokens
        if complexity == QueryComplexity.SIMPLE:
            tokens = 300
        elif complexity == QueryComplexity.MEDIUM:
            tokens = 700
        else:
            tokens = 1500

        # Calculate cost for different tiers
        tier_costs = {tier: (tokens / 1_000_000) * cost for tier, cost in costs.items()}

        # Savings vs premium
        premium_cost = tier_costs["premium"]
        savings = {
            tier: {
                "absolute": premium_cost - cost,
                "percentage": ((premium_cost - cost) / premium_cost * 100) if premium_cost > 0 else 0
            }
            for tier, cost in tier_costs.items()
            if tier != "premium"
        }

        return savings


# Singleton instance
query_classifier = QueryClassifier()
