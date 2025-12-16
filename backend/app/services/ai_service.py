from __future__ import annotations

"""
Core AI service for LegalMitra.

This module provides a small, self‑contained abstraction around the underlying
AI provider (Anthropic or OpenAI).  The rest of the codebase should use the
`ai_service` singleton rather than calling providers directly.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional

from app.core.config import get_settings

try:
    import anthropic  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    anthropic = None  # type: ignore

try:
    from openai import OpenAI  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    OpenAI = None  # type: ignore

try:
    import google.generativeai as genai  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    genai = None  # type: ignore

try:
    import httpx  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    httpx = None  # type: ignore


def _load_system_prompt() -> str:
    """Load the system prompt used to steer the model."""
    settings = get_settings()
    path = settings.SYSTEM_PROMPT_PATH
    if not path.is_absolute():
        # Resolve relative to project root (backend/..)
        base = Path(__file__).resolve().parents[2]
        path = base / settings.SYSTEM_PROMPT_PATH

    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        # Fallback simple prompt so the app still works
        return (
            "You are LegalMitra, an AI‑powered Indian legal assistant. "
            "Provide clear, structured, practical legal information based on "
            "Indian laws, without giving personalised legal advice."
        )


class AIService:
    """High‑level interface for all AI interactions."""

    def __init__(self) -> None:
        self.settings = get_settings()
        self.system_prompt = _load_system_prompt()

        self._anthropic_client = None
        self._openai_client = None
        self._gemini_client = None

        if self.settings.AI_PROVIDER.lower() == "anthropic" and anthropic:
            self._anthropic_client = anthropic.Anthropic(
                api_key=self.settings.ANTHROPIC_API_KEY
            )
        if self.settings.AI_PROVIDER.lower() == "openai" and OpenAI:
            self._openai_client = OpenAI(api_key=self.settings.OPENAI_API_KEY)
        if self.settings.AI_PROVIDER.lower() in ["gemini", "google"] and genai:
            genai.configure(api_key=self.settings.GOOGLE_GEMINI_API_KEY)
            self._gemini_client = genai

    async def process_legal_query(
        self,
        query: str,
        query_type: str = "research",
        context: Optional[Dict[str, Any]] = None,
        relevant_cases: Optional[List[Dict[str, Any]]] = None,
        relevant_statutes: Optional[List[Dict[str, Any]]] = None,
    ) -> str:
        """
        General legal Q&A / research helper.
        """
        prompt_parts: List[str] = [
            f"Query type: {query_type}",
            f"User query: {query}",
        ]

        if context:
            prompt_parts.append(f"Additional context: {context}")
        if relevant_cases:
            prompt_parts.append(f"Relevant cases: {relevant_cases}")
        if relevant_statutes:
            prompt_parts.append(f"Relevant statutes: {relevant_statutes}")

        user_text = "\n\n".join(prompt_parts)
        return await self._generate_text(user_text)

    async def draft_document(
        self,
        document_type: str,
        facts: str,
        parties: Dict[str, str],
        legal_grounds: List[str],
        prayer: str,
        supporting_materials: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Draft legal documents (notices, petitions, replies, opinions, etc.).
        """
        prompt = (
            f"Draft a detailed Indian legal document.\n\n"
            f"Document type: {document_type}\n"
            f"Facts: {facts}\n"
            f"Parties: {parties}\n"
            f"Legal grounds: {legal_grounds}\n"
            f"Prayer / relief sought: {prayer}\n"
        )
        if supporting_materials:
            prompt += f"\nSupporting materials: {supporting_materials}\n"

        prompt += (
            "\nFormat the response as a well‑structured, professional document "
            "with headings, numbered paragraphs, and clear sections."
        )

        return await self._generate_text(prompt)

    async def _generate_text(self, user_text: str) -> str:
        """
        Route the request to the configured AI provider.
        """
        provider = self.settings.AI_PROVIDER.lower()

        if provider == "anthropic":
            if not self._anthropic_client:
                raise RuntimeError(
                    "Anthropic client not available. "
                    "Ensure `anthropic` package is installed and "
                    "ANTHROPIC_API_KEY is set."
                )

            message = self._anthropic_client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=2048,
                system=self.system_prompt,
                messages=[{"role": "user", "content": user_text}],
            )
            # Anthropic returns a list of content blocks
            parts = []
            for block in message.content:
                if getattr(block, "type", None) == "text":
                    parts.append(block.text)
            return "\n".join(parts).strip()

        if provider == "openai":
            if not self._openai_client:
                raise RuntimeError(
                    "OpenAI client not available. "
                    "Ensure `openai` package is installed and "
                    "OPENAI_API_KEY is set."
                )

            response = self._openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_text},
                ],
                max_tokens=2048,
            )
            return (response.choices[0].message.content or "").strip()

        if provider in ["gemini", "google"]:
            if not self._gemini_client:
                raise RuntimeError(
                    "Google Gemini client not available. "
                    "Ensure `google-generativeai` package is installed and "
                    "GOOGLE_GEMINI_API_KEY is set."
                )

            # Run Gemini in thread pool since it's synchronous
            import asyncio
            import time
            import re
            loop = asyncio.get_event_loop()
            
            # Try to find an available Gemini model
            # Priority: gemini-pro (60 req/min free tier) > gemini-1.5-pro > gemini-1.5-flash > gemini-2.5-flash
            preferred_models = ["gemini-pro", "gemini-1.5-pro", "gemini-1.5-flash", "gemini-2.5-flash"]
            model_name = None
            
            # First, try to get a working model
            for candidate in preferred_models:
                try:
                    test_model = self._gemini_client.GenerativeModel(candidate)
                    # Test if model is accessible by checking its name (this is a lightweight check)
                    model_name = candidate
                    print(f"✅ Using Gemini model: {model_name}")
                    break
                except Exception:
                    continue
            
            # If no preferred model works, try listing available models
            if not model_name:
                try:
                    available_models = await loop.run_in_executor(
                        None, lambda: list(self._gemini_client.list_models())
                    )
                    for model_info in available_models:
                        if hasattr(model_info, 'name'):
                            model_id = model_info.name.split('/')[-1]
                            if 'generateContent' in getattr(model_info, 'supported_generation_methods', []):
                                try:
                                    test_model = self._gemini_client.GenerativeModel(model_id)
                                    model_name = model_id
                                    print(f"✅ Using available Gemini model: {model_name}")
                                    break
                                except Exception:
                                    continue
                except Exception as list_error:
                    print(f"⚠️ Could not list Gemini models: {list_error}")
            
            if not model_name:
                raise RuntimeError(
                    "No available Gemini models found. "
                    "Please check your API key and ensure you have access to Gemini models. "
                    "Tried models: " + ", ".join(preferred_models)
                )
            
            # Retry logic for rate limit errors (429)
            max_retries = 3
            base_delay = 2
            
            for attempt in range(max_retries):
                try:
                    model = self._gemini_client.GenerativeModel(model_name)
                    
                    # Combine system prompt and user text
                    full_prompt = f"{self.system_prompt}\n\n{user_text}"
                    
                    response = await loop.run_in_executor(
                        None, lambda: model.generate_content(
                            full_prompt,
                            generation_config={
                                "temperature": 0.3,
                                "max_output_tokens": 8000,
                            }
                        )
                    )
                    return response.text.strip()
                    
                except Exception as e:
                    error_str = str(e)
                    
                    # Check if model doesn't exist (404) - try next model in list
                    if "404" in error_str and "not found" in error_str.lower():
                        # Model not available, try next preferred model
                        current_index = preferred_models.index(model_name) if model_name in preferred_models else -1
                        if current_index >= 0 and current_index < len(preferred_models) - 1:
                            model_name = preferred_models[current_index + 1]
                            print(f"⚠️ Model not available, trying: {model_name}")
                            continue
                        else:
                            raise RuntimeError(f"Gemini model not available: {model_name}. Error: {error_str[:300]}")
                    
                    # Check for rate limit error (429)
                    if "429" in error_str or "quota" in error_str.lower() or "rate limit" in error_str.lower() or "exceeded" in error_str.lower():
                        if attempt < max_retries - 1:
                            # Calculate retry delay
                            retry_delay = base_delay * (2 ** attempt)  # Exponential backoff: 2s, 4s, 8s
                            
                            # Try to parse retry delay from error message
                            delay_match = re.search(r'retry.*?(\d+\.?\d*)\s*[sS]', error_str)
                            if delay_match:
                                retry_delay = float(delay_match.group(1)) + 2  # Add 2 second buffer
                            
                            print(f"⚠️ Rate limit exceeded for {model_name}. Retrying in {retry_delay:.1f} seconds... (Attempt {attempt + 1}/{max_retries})")
                            await asyncio.sleep(retry_delay)
                            continue
                        else:
                            raise RuntimeError(
                                f"Rate limit exceeded after {max_retries} attempts. "
                                f"Gemini free tier limits: gemini-pro = 60 requests/minute, gemini-2.5-flash = 5 requests/minute. "
                                f"Using {model_name}. Please wait a minute before trying again. "
                                f"Original error: {error_str[:300]}"
                            )
                    else:
                        # Not a rate limit error, re-raise immediately
                        raise RuntimeError(f"Gemini API error ({model_name}): {error_str}")

        if provider == "grok":
            if not httpx:
                raise RuntimeError(
                    "httpx package required for Grok API. "
                    "Install with: pip install httpx"
                )
            if not self.settings.GROK_API_KEY:
                raise RuntimeError(
                    "GROK_API_KEY not set in .env file."
                )

            # Grok uses OpenAI-compatible API
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.x.ai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.settings.GROK_API_KEY}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": "grok-beta",
                        "messages": [
                            {"role": "system", "content": self.system_prompt},
                            {"role": "user", "content": user_text},
                        ],
                        "max_tokens": 2048,
                    },
                    timeout=60.0,
                )
                response.raise_for_status()
                data = response.json()
                return (data["choices"][0]["message"]["content"] or "").strip()

        raise RuntimeError(
            f"Unsupported AI provider '{self.settings.AI_PROVIDER}'. "
            "Use 'anthropic', 'openai', 'gemini', or 'grok'."
        )


# Singleton instance used by the API routers
ai_service = AIService()


