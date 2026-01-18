"""
Model Failover Service for LegalMitra
Provides automatic fallback when primary AI models fail
"""

import logging
from typing import List, Dict, Any, Optional, Callable
from datetime import datetime, timedelta


logger = logging.getLogger(__name__)


class ModelConfig:
    """Configuration for a model in the failover chain"""

    def __init__(
        self,
        provider: str,
        model_id: str,
        tier: str,
        cost_per_1m: float,
        description: str
    ):
        self.provider = provider
        self.model_id = model_id
        self.tier = tier
        self.cost_per_1m = cost_per_1m
        self.description = description
        self.failures = 0
        self.last_failure = None
        self.last_success = None

    def record_failure(self):
        """Record a failure for this model"""
        self.failures += 1
        self.last_failure = datetime.now()

    def record_success(self):
        """Record a success for this model"""
        self.failures = max(0, self.failures - 1)  # Decay failures
        self.last_success = datetime.now()

    def is_healthy(self) -> bool:
        """Check if model is healthy enough to try"""
        # If never failed, it's healthy
        if self.last_failure is None:
            return True

        # If it succeeded recently, it's healthy
        if self.last_success and self.last_success > self.last_failure:
            return True

        # If it failed too many times recently, mark unhealthy
        if self.failures >= 3:
            # Wait 5 minutes before retry
            if datetime.now() - self.last_failure < timedelta(minutes=5):
                return False

        return True


class ModelFailoverService:
    """Manages automatic failover between AI models"""

    def __init__(self):
        # Define failover chains for different tiers
        # Note: Using gemini-2.0-flash-exp (2025 model) instead of deprecated gemini-1.5-flash
        self.model_chains = {
            "free": [
                ModelConfig("gemini", "gemini-2.0-flash-exp", "free", 0.0, "Gemini 2.0 Flash (FREE)"),
            ],
            "budget": [
                ModelConfig("gemini", "gemini-2.0-flash-exp", "free", 0.0, "Gemini 2.0 Flash (FREE)"),
                ModelConfig("openrouter", "openai/gpt-4o-mini-2024-07-18", "budget", 0.15, "GPT-4o Mini"),
                ModelConfig("openrouter", "openai/gpt-3.5-turbo", "budget", 0.50, "GPT-3.5 Turbo"),
            ],
            "balanced": [
                ModelConfig("anthropic", "claude-3-haiku-20240307", "balanced", 0.25, "Claude 3 Haiku"),
                ModelConfig("gemini", "gemini-2.0-flash-exp", "free", 0.0, "Gemini 2.0 Flash (FREE)"),
                ModelConfig("openrouter", "openai/gpt-4o-mini-2024-07-18", "budget", 0.15, "GPT-4o Mini"),
            ],
            "premium": [
                ModelConfig("anthropic", "claude-3-5-sonnet-20241022", "premium", 3.00, "Claude 3.5 Sonnet"),
                ModelConfig("anthropic", "claude-3-haiku-20240307", "balanced", 0.25, "Claude 3 Haiku (Fallback)"),
                ModelConfig("gemini", "gemini-2.0-flash-exp", "free", 0.0, "Gemini 2.0 Flash (FREE Fallback)"),
            ]
        }

    async def execute_with_failover(
        self,
        tier: str,
        execute_fn: Callable[[str, str], Any],
        max_attempts: int = 3
    ) -> Dict[str, Any]:
        """
        Execute a function with automatic failover

        Args:
            tier: Model tier (free, budget, balanced, premium)
            execute_fn: Async function that takes (provider, model_id) and returns result
            max_attempts: Maximum number of models to try

        Returns:
            Dict with:
                - success: bool
                - result: Any (the actual result if successful)
                - model_used: ModelConfig (which model worked)
                - attempts: int (how many models were tried)
                - errors: List[str] (errors from failed attempts)
        """
        chain = self.model_chains.get(tier, self.model_chains["balanced"])
        errors = []
        attempts = 0

        for model in chain[:max_attempts]:
            # Skip unhealthy models
            if not model.is_healthy():
                logger.warning(f"Skipping unhealthy model: {model.description}")
                continue

            attempts += 1
            try:
                logger.info(f"Attempting {model.description} (provider: {model.provider})")

                # Execute the function
                result = await execute_fn(model.provider, model.model_id)

                # Success!
                model.record_success()
                logger.info(f"✅ Success with {model.description}")

                return {
                    "success": True,
                    "result": result,
                    "model_used": {
                        "provider": model.provider,
                        "model_id": model.model_id,
                        "tier": model.tier,
                        "cost_per_1m": model.cost_per_1m,
                        "description": model.description
                    },
                    "attempts": attempts,
                    "errors": errors
                }

            except Exception as e:
                error_msg = f"{model.description}: {str(e)}"
                logger.warning(f"❌ Failed: {error_msg}")
                model.record_failure()
                errors.append(error_msg)
                continue

        # All models failed
        logger.error(f"All models failed for tier '{tier}' after {attempts} attempts")
        return {
            "success": False,
            "result": None,
            "model_used": None,
            "attempts": attempts,
            "errors": errors
        }

    def get_model_health(self, tier: str) -> List[Dict[str, Any]]:
        """Get health status of all models in a tier"""
        chain = self.model_chains.get(tier, [])
        return [
            {
                "description": model.description,
                "provider": model.provider,
                "model_id": model.model_id,
                "tier": model.tier,
                "cost_per_1m": model.cost_per_1m,
                "is_healthy": model.is_healthy(),
                "failures": model.failures,
                "last_failure": model.last_failure.isoformat() if model.last_failure else None,
                "last_success": model.last_success.isoformat() if model.last_success else None,
            }
            for model in chain
        ]

    def get_all_health(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get health status of all models across all tiers"""
        return {
            tier: self.get_model_health(tier)
            for tier in self.model_chains.keys()
        }


# Singleton instance
model_failover = ModelFailoverService()
