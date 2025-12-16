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
        provider = self.settings.AI_PROVIDER.lower().strip()
        
        # Normalize provider names - handle variations (google -> gemini)
        original_provider = provider
        if provider == "google":
            provider = "gemini"
        
        # Debug: Log the provider value after normalization
        print(f"DEBUG: AI_PROVIDER={repr(self.settings.AI_PROVIDER)}, original={repr(original_provider)}, normalized={repr(provider)}, type={type(provider)}")
        print(f"DEBUG: Direct comparison test - provider == 'gemini': {provider == 'gemini'}")
        print(f"DEBUG: Provider checks - anthropic={provider == 'anthropic'}, openai={provider == 'openai'}, gemini={provider == 'gemini'}, grok={provider == 'grok'}")

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
        elif provider == "openai":
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
        elif provider == "gemini":
            print(f"DEBUG: ✅✅✅ ENTERED GEMINI BLOCK! provider={repr(provider)}, _gemini_client exists={self._gemini_client is not None}")
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
            # Updated priority: Try newer models first, then fallback to older ones
            # gemini-1.5-flash is the most widely available and cost-effective
            preferred_models = [
                "gemini-1.5-flash",      # Fast, cost-effective, widely available
                "gemini-1.5-pro",        # Higher capability
                "gemini-1.0-pro",        # Stable successor to gemini-pro
                "gemini-pro",            # Legacy (may not be available)
                "gemini-2.5-flash"       # Latest (may have rate limits)
            ]
            model_name = None
            
            # First, try to list available models from API (most reliable)
            model_name = None
            try:
                print("🔍 Listing available Gemini models from API...")
                available_models = await loop.run_in_executor(
                    None, lambda: list(self._gemini_client.list_models())
                )
                
                # Create a list of available model IDs
                available_model_ids = []
                for model_info in available_models:
                    if hasattr(model_info, 'name') and 'generateContent' in getattr(model_info, 'supported_generation_methods', []):
                        model_id = model_info.name.split('/')[-1]
                        available_model_ids.append(model_id)
                
                print(f"✅ Found {len(available_model_ids)} available models: {', '.join(available_model_ids[:5])}")
                
                # Try preferred models first (in order), but only if they're in the available list
                for preferred in preferred_models:
                    if preferred in available_model_ids:
                        model_name = preferred
                        print(f"✅ Using preferred Gemini model: {model_name}")
                        break
                
                # If no preferred model is available, use the first available model
                if not model_name and available_model_ids:
                    model_name = available_model_ids[0]
                    print(f"✅ Using first available Gemini model: {model_name}")
                    
            except Exception as list_error:
                print(f"⚠️ Could not list Gemini models: {list_error}")
                print("⚠️ Falling back to trying preferred models directly...")
                # Fallback: try preferred models in order
                model_name = preferred_models[0]
            
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
                    
                    # Check if model doesn't exist (404) - try to list available models and use one
                    if "404" in error_str and ("not found" in error_str.lower() or "is not found" in error_str.lower()):
                        print(f"⚠️ Model {model_name} not available (404). Trying to find alternative...")
                        try:
                            # List available models and pick the first one that supports generateContent
                            available_models = await loop.run_in_executor(
                                None, lambda: list(self._gemini_client.list_models())
                            )
                            for model_info in available_models:
                                if hasattr(model_info, 'name') and 'generateContent' in getattr(model_info, 'supported_generation_methods', []):
                                    model_id = model_info.name.split('/')[-1]
                                    model_name = model_id
                                    print(f"✅ Switched to available model: {model_name}")
                                    continue  # Retry with new model
                            
                            # If we get here, no models were found
                            raise RuntimeError(
                                f"No available Gemini models found. Please check your API key. "
                                f"Last error: {error_str[:200]}"
                            )
                        except RuntimeError:
                            raise  # Re-raise if it's our RuntimeError
                        except Exception as list_err:
                            # If listing fails, raise original error
                            raise RuntimeError(f"Gemini model {model_name} not available and could not list alternatives. Error: {error_str[:200]}")
                    
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
        elif provider == "grok":
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

        # This should never be reached if provider checks are correct
        # But if we're here, try one more time with explicit handling
        print(f"ERROR: Reached final error block! provider={repr(provider)}, type={type(provider)}")
        print(f"ERROR: provider == 'gemini': {provider == 'gemini'}")
        print(f"ERROR: provider in ('gemini', 'google'): {provider in ('gemini', 'google')}")
        print(f"ERROR: All elif checks failed - this shouldn't happen!")
        
        # Last resort: handle gemini/google directly here by recursing
        if provider in ('gemini', 'google') or provider == 'gemini':
            print(f"WARNING: Caught gemini provider in fallback - handling directly")
            # Call the gemini logic directly
            if not self._gemini_client:
                raise RuntimeError(
                    "Google Gemini client not available. "
                    "Ensure `google-generativeai` package is installed and "
                    "GOOGLE_GEMINI_API_KEY is set."
                )
            # Use the same logic as the elif block - just copy it here as fallback
            import asyncio
            import time
            import re
            loop = asyncio.get_event_loop()
            preferred_models = [
                "gemini-1.5-flash",      # Fast, cost-effective, widely available
                "gemini-1.5-pro",        # Higher capability
                "gemini-1.0-pro",        # Stable successor to gemini-pro
                "gemini-pro",            # Legacy (may not be available)
                "gemini-2.5-flash"       # Latest (may have rate limits)
            ]
            model_name = None
            for candidate in preferred_models:
                try:
                    test_model = self._gemini_client.GenerativeModel(candidate)
                    model_name = candidate
                    print(f"✅ Using Gemini model: {model_name}")
                    break
                except Exception:
                    continue
            if not model_name:
                raise RuntimeError("No available Gemini models found.")
            model = self._gemini_client.GenerativeModel(model_name)
            full_prompt = f"{self.system_prompt}\n\n{user_text}"
            response = await loop.run_in_executor(
                None, lambda: model.generate_content(
                    full_prompt,
                    generation_config={"temperature": 0.3, "max_output_tokens": 8000}
                )
            )
            return response.text.strip()
        
        raise RuntimeError(
            f"Unsupported AI provider '{self.settings.AI_PROVIDER}' (normalized: '{provider}'). "
            "Use 'anthropic', 'openai', 'gemini', 'google', or 'grok'. "
            f"Available provider checks: anthropic={provider == 'anthropic'}, "
            f"openai={provider == 'openai'}, gemini={provider == 'gemini'}, "
            f"gemini/google={provider in ['gemini', 'google']}, grok={provider == 'grok'}"
        )


# Singleton instance used by the API routers
ai_service = AIService()


