"""
OpenRouter Integration for LegalMitra
Provides access to 200+ AI models through a single API
"""

from typing import Dict, List, Optional, Any
import httpx
from app.core.config import get_settings


class OpenRouterService:
    """
    Service for interacting with OpenRouter API
    Provides access to GPT-4, Claude, Gemini, Llama, Mistral, and 200+ models
    """

    def __init__(self):
        self.settings = get_settings()
        self.base_url = "https://openrouter.ai/api/v1"
        self.api_key = self.settings.OPENROUTER_API_KEY if hasattr(self.settings, 'OPENROUTER_API_KEY') else None

    async def get_available_models(self) -> List[Dict[str, Any]]:
        """
        Get list of all available models from OpenRouter
        Returns model info including pricing, context length, etc.
        """
        if not self.api_key:
            return []

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/models",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    timeout=10.0
                )
                response.raise_for_status()
                data = response.json()
                return data.get("data", [])
            except Exception as e:
                print(f"Failed to fetch OpenRouter models: {e}")
                return []

    async def get_recommended_models_for_legal(self) -> List[Dict[str, str]]:
        """
        Get recommended models for legal work with cost/quality balance
        Now includes FREE and ultra-cheap models!
        """
        return [
            # BUDGET TIER - Very Low Cost (verified working models with full IDs)
            {
                "id": "anthropic/claude-3-haiku-20240307",
                "name": "Claude 3 Haiku 💎 Best Value",
                "tier": "budget",
                "cost_per_1m_tokens": "$0.25",
                "best_for": "Quick queries, excellent quality/price - RECOMMENDED",
                "context_length": "200k"
            },
            {
                "id": "openai/gpt-4o-mini-2024-07-18",
                "name": "GPT-4o Mini 💎",
                "tier": "budget",
                "cost_per_1m_tokens": "$0.15",
                "best_for": "General queries, template filling",
                "context_length": "128k"
            },
            {
                "id": "openai/gpt-3.5-turbo",
                "name": "GPT-3.5 Turbo 💎",
                "tier": "budget",
                "cost_per_1m_tokens": "$0.50",
                "best_for": "Fast, reliable, proven model",
                "context_length": "16k"
            },
            {
                "id": "google/gemini-flash-1.5-8b",
                "name": "Gemini Flash 1.5 8B 💎",
                "tier": "budget",
                "cost_per_1m_tokens": "$0.075",
                "best_for": "Very cheap Google model",
                "context_length": "1M"
            },

            # Premium Tier - Best Quality (for complex legal analysis)
            {
                "id": "anthropic/claude-3.5-sonnet",
                "name": "Claude 3.5 Sonnet ⭐",
                "tier": "premium",
                "cost_per_1m_tokens": "$3.00",
                "best_for": "Complex legal research, detailed analysis",
                "context_length": "200k"
            },
            {
                "id": "anthropic/claude-3-opus",
                "name": "Claude 3 Opus",
                "tier": "premium",
                "cost_per_1m_tokens": "$15.00",
                "best_for": "Most complex analysis, critical work",
                "context_length": "200k"
            },
            {
                "id": "openai/gpt-4-turbo",
                "name": "GPT-4 Turbo",
                "tier": "premium",
                "cost_per_1m_tokens": "$10.00",
                "best_for": "Document drafting, comprehensive analysis",
                "context_length": "128k"
            },
            {
                "id": "openai/gpt-4o",
                "name": "GPT-4o",
                "tier": "premium",
                "cost_per_1m_tokens": "$2.50",
                "best_for": "Latest GPT-4, balanced cost/quality",
                "context_length": "128k"
            },
            {
                "id": "google/gemini-pro-1.5",
                "name": "Gemini Pro 1.5",
                "tier": "premium",
                "cost_per_1m_tokens": "$1.25",
                "best_for": "Large document analysis, 1M context",
                "context_length": "1M"
            },
            {
                "id": "x-ai/grok-beta",
                "name": "Grok Beta",
                "tier": "premium",
                "cost_per_1m_tokens": "$5.00",
                "best_for": "Latest xAI model, real-time knowledge",
                "context_length": "131k"
            },

            # Balanced Tier - Good Quality, Lower Cost
            {
                "id": "anthropic/claude-3-haiku",
                "name": "Claude 3 Haiku",
                "tier": "balanced",
                "cost_per_1m_tokens": "$0.25",
                "best_for": "Quick queries, standard research",
                "context_length": "200k"
            },
            {
                "id": "openai/gpt-4o-mini",
                "name": "GPT-4o Mini",
                "tier": "balanced",
                "cost_per_1m_tokens": "$0.15",
                "best_for": "General legal queries, template filling",
                "context_length": "128k"
            },
            {
                "id": "openai/gpt-3.5-turbo",
                "name": "GPT-3.5 Turbo",
                "tier": "balanced",
                "cost_per_1m_tokens": "$0.50",
                "best_for": "Fast responses, standard queries",
                "context_length": "16k"
            },
            {
                "id": "google/gemini-flash-1.5",
                "name": "Gemini Flash 1.5",
                "tier": "balanced",
                "cost_per_1m_tokens": "$0.075",
                "best_for": "Very fast, good quality, cheap",
                "context_length": "1M"
            },
            {
                "id": "anthropic/claude-3-5-haiku",
                "name": "Claude 3.5 Haiku",
                "tier": "balanced",
                "cost_per_1m_tokens": "$0.80",
                "best_for": "Latest Haiku, improved quality",
                "context_length": "200k"
            },
            {
                "id": "meta-llama/llama-3.1-70b-instruct",
                "name": "Llama 3.1 70B",
                "tier": "balanced",
                "cost_per_1m_tokens": "$0.52",
                "best_for": "Open source, good quality, moderate cost",
                "context_length": "128k"
            },

            # Budget Tier - Very Low Cost (for high-volume tasks)
            {
                "id": "meta-llama/llama-3.1-8b-instruct",
                "name": "Llama 3.1 8B",
                "tier": "budget",
                "cost_per_1m_tokens": "$0.055",
                "best_for": "Simple queries, high volume",
                "context_length": "128k"
            },
            {
                "id": "meta-llama/llama-3.2-3b-instruct",
                "name": "Llama 3.2 3B",
                "tier": "budget",
                "cost_per_1m_tokens": "$0.04",
                "best_for": "Very simple tasks, ultra cheap",
                "context_length": "128k"
            },
            {
                "id": "mistralai/mistral-7b-instruct",
                "name": "Mistral 7B",
                "tier": "budget",
                "cost_per_1m_tokens": "$0.06",
                "best_for": "Simple tasks, fast responses",
                "context_length": "32k"
            },
            {
                "id": "deepseek/deepseek-chat",
                "name": "DeepSeek Chat",
                "tier": "budget",
                "cost_per_1m_tokens": "$0.14",
                "best_for": "General queries, cost-sensitive",
                "context_length": "64k"
            },
            {
                "id": "microsoft/phi-3-medium-128k-instruct",
                "name": "Phi-3 Medium",
                "tier": "budget",
                "cost_per_1m_tokens": "$0.10",
                "best_for": "Efficient, good quality/cost ratio",
                "context_length": "128k"
            },
            {
                "id": "google/gemma-2-9b-it",
                "name": "Gemma 2 9B",
                "tier": "budget",
                "cost_per_1m_tokens": "$0.08",
                "best_for": "Open source Google model, cheap",
                "context_length": "8k"
            },
            {
                "id": "qwen/qwen-2-7b-instruct",
                "name": "Qwen 2 7B",
                "tier": "budget",
                "cost_per_1m_tokens": "$0.09",
                "best_for": "Chinese+English, multilingual",
                "context_length": "128k"
            },
        ]

    async def generate_text(
        self,
        user_text: str,
        system_prompt: str,
        model: str = "anthropic/claude-3.5-sonnet",
        max_tokens: int = 4096,
        temperature: float = 0.3
    ) -> Dict[str, Any]:
        """
        Generate text using OpenRouter

        Args:
            user_text: User's prompt/question
            system_prompt: System instructions
            model: Model ID (e.g., "anthropic/claude-3.5-sonnet")
            max_tokens: Maximum response tokens
            temperature: Sampling temperature (0-1)

        Returns:
            Dict with 'text', 'model_used', 'tokens_used', 'cost'
        """
        if not self.api_key:
            raise RuntimeError(
                "OPENROUTER_API_KEY not set in .env file. "
                "Get your key from https://openrouter.ai/keys"
            )

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": "https://legalmitra.app",  # Optional: for ranking
                        "X-Title": "LegalMitra"  # Optional: shows in OpenRouter dashboard
                    },
                    json={
                        "model": model,
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_text}
                        ],
                        "max_tokens": max_tokens,
                        "temperature": temperature,
                        "route": "fallback"  # Auto-fallback if model unavailable
                    },
                    timeout=120.0
                )
                response.raise_for_status()
                data = response.json()

                # Extract response
                text = data["choices"][0]["message"]["content"]

                # Extract usage info
                usage = data.get("usage", {})
                tokens_used = usage.get("total_tokens", 0)

                # Calculate approximate cost
                model_used = data.get("model", model)
                cost = self._estimate_cost(model_used, tokens_used)

                return {
                    "text": text.strip(),
                    "model_used": model_used,
                    "tokens_used": tokens_used,
                    "cost_usd": cost
                }

            except httpx.HTTPStatusError as e:
                error_detail = e.response.json() if e.response else str(e)
                raise RuntimeError(f"OpenRouter API error: {error_detail}")
            except Exception as e:
                raise RuntimeError(f"OpenRouter request failed: {str(e)}")

    def _estimate_cost(self, model: str, tokens: int) -> float:
        """
        Estimate cost based on model and token count
        This is approximate - actual cost comes from OpenRouter dashboard
        """
        # Rough pricing (per 1M tokens, averaged input/output)
        pricing = {
            "anthropic/claude-3.5-sonnet": 3.00,
            "anthropic/claude-3-haiku": 0.25,
            "openai/gpt-4-turbo": 10.00,
            "openai/gpt-4o-mini": 0.15,
            "google/gemini-pro-1.5": 3.50,
            "google/gemini-flash-1.5": 0.10,
            "meta-llama/llama-3.1-70b-instruct": 0.18,
            "mistralai/mistral-7b-instruct": 0.06,
            "deepseek/deepseek-chat": 0.14,
        }

        cost_per_million = pricing.get(model, 1.0)  # Default fallback
        return (tokens / 1_000_000) * cost_per_million

    async def get_model_info(self, model_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific model"""
        models = await self.get_available_models()
        for model in models:
            if model.get("id") == model_id:
                return model
        return None


# Singleton instance
openrouter_service = OpenRouterService()
