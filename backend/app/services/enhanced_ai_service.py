"""
Enhanced AI Service with Query Classification, Failover, and Disclaimers
Integrates all three Step 1-3 features for LegalMitra
"""

import logging
from typing import Dict, Any, Optional
from app.core.config import get_settings
from app.services.query_classifier import query_classifier
from app.services.model_failover import model_failover
from app.services.disclaimer_service import disclaimer_service

logger = logging.getLogger(__name__)


class EnhancedAIService:
    """
    Enhanced AI service with:
    - Smart query classification for cost optimization
    - Automatic model failover for reliability
    - Bar Council-safe disclaimers
    """

    def __init__(self):
        self.settings = get_settings()
        logger.info("Enhanced AI Service initialized")

    async def process_with_intelligence(
        self,
        query: str,
        query_type: str = "research",
        user_preferences: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process query with intelligent routing, failover, and disclaimers

        Args:
            query: User's legal query
            query_type: Type of query (research, drafting, case_search, etc.)
            user_preferences: Optional user preferences (e.g., preferred tier)

        Returns:
            Dict containing:
                - response: str (AI response with disclaimers)
                - classification: Dict (query classification details)
                - model_used: Dict (which model was used)
                - cost_estimate: float (estimated cost in USD)
                - failover_info: Dict (failover attempts if any)
        """

        # Step 1: Classify the query
        classification = query_classifier.classify_query(query)
        logger.info(f"Query classified: {classification['rationale']}")

        # Override tier if user has preferences
        recommended_tier = classification['recommended_model_tier']
        if user_preferences and 'preferred_tier' in user_preferences:
            recommended_tier = user_preferences['preferred_tier']
            logger.info(f"User override: using {recommended_tier} tier")

        # Step 2: Execute with failover
        async def execute_model(provider: str, model_id: str) -> str:
            """Execute AI model based on provider"""
            return await self._call_provider(provider, model_id, query, query_type)

        failover_result = await model_failover.execute_with_failover(
            tier=recommended_tier,
            execute_fn=execute_model,
            max_attempts=3
        )

        if not failover_result['success']:
            # All models failed
            logger.error(f"All models failed: {failover_result['errors']}")
            raise Exception(
                f"Unable to process query. All AI models unavailable. "
                f"Errors: {'; '.join(failover_result['errors'])}"
            )

        ai_response = failover_result['result']
        model_used = failover_result['model_used']

        # Step 3: Add disclaimers
        response_with_disclaimers = disclaimer_service.add_disclaimers(
            ai_response,
            query_type=query_type
        )

        # Calculate actual cost
        tokens_used = classification['estimated_tokens']
        cost_estimate = (tokens_used / 1_000_000) * model_used['cost_per_1m']

        # Check for risky language
        risks = disclaimer_service.check_risks(ai_response)
        if risks:
            logger.warning(f"Risky language detected: {risks}")

        return {
            "response": response_with_disclaimers,
            "classification": {
                "query_type": classification['query_type'],
                "complexity": classification['complexity'],
                "recommended_tier": recommended_tier,
                "rationale": classification['rationale'],
                "estimated_tokens": classification['estimated_tokens']
            },
            "model_used": model_used,
            "cost_estimate": cost_estimate,
            "failover_info": {
                "attempts": failover_result['attempts'],
                "had_failures": failover_result['attempts'] > 1,
                "errors": failover_result['errors'] if failover_result['attempts'] > 1 else []
            },
            "safety": {
                "risks_detected": risks,
                "disclaimers_added": True
            }
        }

    async def _call_provider(
        self,
        provider: str,
        model_id: str,
        query: str,
        query_type: str
    ) -> str:
        """
        Call specific AI provider

        Args:
            provider: Provider name (gemini, anthropic, openrouter, openai)
            model_id: Model identifier
            query: User query
            query_type: Query type

        Returns:
            AI response text
        """
        # Import providers dynamically to avoid import errors
        if provider == "gemini":
            return await self._call_gemini(model_id, query, query_type)
        elif provider == "anthropic":
            return await self._call_anthropic(model_id, query, query_type)
        elif provider == "openrouter":
            return await self._call_openrouter(model_id, query, query_type)
        elif provider == "openai":
            return await self._call_openai(model_id, query, query_type)
        else:
            raise ValueError(f"Unknown provider: {provider}")

    async def _call_gemini(self, model_id: str, query: str, query_type: str) -> str:
        """Call Google Gemini API"""
        try:
            from google import genai

            client = genai.Client(api_key=self.settings.GOOGLE_GEMINI_API_KEY)

            system_prompt = self._get_system_prompt(query_type)

            # Combine system prompt and user query into a single prompt
            full_prompt = f"{system_prompt}\n\nUser query: {query}"

            # Use the correct async method and model format for the new SDK
            response = await client.aio.models.generate_content(
                model=model_id,
                contents=full_prompt
            )

            return response.text
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            raise

    async def _call_anthropic(self, model_id: str, query: str, query_type: str) -> str:
        """Call Anthropic Claude API"""
        try:
            import anthropic

            client = anthropic.Anthropic(api_key=self.settings.ANTHROPIC_API_KEY)

            system_prompt = self._get_system_prompt(query_type)

            message = await client.messages.create(
                model=model_id,
                max_tokens=2048,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": query}
                ]
            )

            return message.content[0].text
        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            raise

    async def _call_openrouter(self, model_id: str, query: str, query_type: str) -> str:
        """Call OpenRouter API"""
        try:
            from app.services.openrouter_service import openrouter_service

            system_prompt = self._get_system_prompt(query_type)

            result = await openrouter_service.generate_text(
                user_text=query,
                system_prompt=system_prompt,
                model=model_id,
                max_tokens=2048
            )

            return result['text']
        except Exception as e:
            logger.error(f"OpenRouter API error: {e}")
            raise

    async def _call_openai(self, model_id: str, query: str, query_type: str) -> str:
        """Call OpenAI API"""
        try:
            from openai import OpenAI

            client = OpenAI(api_key=self.settings.OPENAI_API_KEY)

            system_prompt = self._get_system_prompt(query_type)

            response = client.chat.completions.create(
                model=model_id,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query}
                ],
                max_tokens=2048
            )

            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise

    def _get_system_prompt(self, query_type: str) -> str:
        """Get appropriate system prompt based on query type"""

        base_prompt = (
            "You are LegalMitra, an AI-powered Indian legal assistant. "
            "Provide clear, structured, practical legal information based on "
            "Indian laws. Do not provide personalized legal advice or guarantee outcomes."
        )

        if query_type == "drafting" or query_type == "draft_document":
            return (
                f"{base_prompt} You are assisting with document drafting. "
                "Create a professional draft that can be reviewed by an advocate. "
                "Use formal legal language and proper structure."
            )
        elif query_type == "case_search":
            return (
                f"{base_prompt} You are assisting with case law research. "
                "Provide accurate case citations and key principles. "
                "Indicate that case law should be verified."
            )
        elif query_type == "research":
            return (
                f"{base_prompt} You are assisting with legal research. "
                "Provide comprehensive information with statutory references. "
                "Explain complex concepts clearly."
            )
        else:
            return base_prompt

    async def get_model_health_status(self) -> Dict[str, Any]:
        """Get health status of all models across tiers"""
        return model_failover.get_all_health()


# Singleton instance
enhanced_ai_service = EnhancedAIService()
