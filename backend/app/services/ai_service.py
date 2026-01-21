from __future__ import annotations

"""
Core AI service for LegalMitra.

This module provides a small, self‑contained abstraction around the underlying
AI provider (Anthropic or OpenAI).  The rest of the codebase should use the
`ai_service` singleton rather than calling providers directly.
"""

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from app.core.config import get_settings
from app.services.web_search_service import web_search_service

logger = logging.getLogger(__name__)

try:
    import anthropic  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    anthropic = None  # type: ignore

try:
    from openai import OpenAI  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    OpenAI = None  # type: ignore

# Try new google.genai package (2025 official SDK)
try:
    from google import genai  # type: ignore
    GENAI_NEW_SDK = True
    print("✅ Successfully imported google.genai (new SDK)")
except Exception as e:  # pragma: no cover - optional dependency
    GENAI_NEW_SDK = False
    print(f"⚠️ Failed to import google.genai (new SDK): {e}")
    # Fallback to old deprecated package (should not be used)
    try:
        import google.generativeai as genai  # type: ignore
        print("✅ Successfully imported google.generativeai (old SDK)")
    except Exception as e2:
        genai = None  # type: ignore
        print(f"❌ Failed to import google.generativeai (old SDK): {e2}")
        print("❌ Google Gemini packages not available. Install with: pip install google-genai")

try:
    import httpx  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    httpx = None  # type: ignore

try:
    from app.services.openrouter_service import openrouter_service  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    openrouter_service = None  # type: ignore


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

        # Normalize AI_PROVIDER during initialization to handle misconfigured values
        provider = self.settings.AI_PROVIDER.lower().strip()
        
        # Handle misconfiguration cases (common in deployment environments)
        if "google (or anthropic, openai)" in provider or "or anthropic" in provider or "or openai" in provider:
            logger.warning(f"Invalid AI_PROVIDER detected during init: '{self.settings.AI_PROVIDER}'. Normalizing to 'gemini'.")
            print(f"WARNING: Invalid AI_PROVIDER detected during init: '{self.settings.AI_PROVIDER}'. Normalizing to 'gemini'.")
            provider = "gemini"
        elif provider == "google":
            provider = "gemini"

        if provider == "anthropic" and anthropic:
            self._anthropic_client = anthropic.Anthropic(
                api_key=self.settings.ANTHROPIC_API_KEY
            )
        if provider == "openai" and OpenAI:
            self._openai_client = OpenAI(api_key=self.settings.OPENAI_API_KEY)
        # FIX 5: Don't initialize Gemini client at startup - lazy load it
        # Client will be created on first use to save memory
        # FIX 5: Don't initialize Gemini client at startup - lazy load it
        # Client will be created on first use to save memory
        if provider == "gemini":
            logger.info("Gemini provider selected - client will be initialized on first use (lazy loading)")
            print("DEBUG: Gemini provider selected - lazy loading enabled")
            # Set flag but don't initialize client yet
            self._gemini_use_new_sdk = GENAI_NEW_SDK if genai else False
                        self._gemini_use_new_sdk = True
                        logger.info("✅ Google Gemini client initialized (new SDK)")
                        print("✅ Google Gemini client initialized (new SDK)")
                    else:
                        # Fallback to old deprecated package (should not be used)
                        logger.info(f"Initializing Gemini client with old SDK (API key length: {api_key_length})")
                        print(f"DEBUG: Attempting to configure genai with old SDK")
                        genai.configure(api_key=self.settings.GOOGLE_GEMINI_API_KEY)
                        self._gemini_client = genai
                        self._gemini_use_new_sdk = False
                        logger.info("✅ Google Gemini client initialized (old SDK)")
                        print("✅ Google Gemini client initialized (old SDK)")
                except ImportError as e:
                    error_msg = f"Failed to import Gemini SDK: {e}. Ensure google-genai is installed: pip install google-genai"
                    logger.error(error_msg)
                    print(f"ERROR: {error_msg}")
                    import traceback
                    print(traceback.format_exc())
                    self._gemini_client = None
                    self._gemini_use_new_sdk = False
                except Exception as e:
                    error_msg = f"Failed to initialize Gemini client: {type(e).__name__}: {e}"
                    logger.error(error_msg, exc_info=True)
                    print(f"ERROR: {error_msg}")
                    import traceback
                    print("FULL TRACEBACK:")
                    print(traceback.format_exc())
                    self._gemini_client = None
                    self._gemini_use_new_sdk = False
        else:
            self._gemini_use_new_sdk = False
    
    def _initialize_gemini_client(self):
        """Lazy initialize Gemini client on first use (FIX 5)"""
        if self._gemini_client is not None:
            return  # Already initialized
        
        if genai is None:
            logger.error("Google Gemini package not installed")
            return
        
        if not self.settings.GOOGLE_GEMINI_API_KEY:
            logger.error("GOOGLE_GEMINI_API_KEY is not set")
            return
        
        try:
            api_key_length = len(self.settings.GOOGLE_GEMINI_API_KEY) if self.settings.GOOGLE_GEMINI_API_KEY else 0
            logger.info(f"Initializing Gemini client (lazy load) - API key length: {api_key_length}")
            
            if GENAI_NEW_SDK:
                self._gemini_client = genai.Client(api_key=self.settings.GOOGLE_GEMINI_API_KEY)
                self._gemini_use_new_sdk = True
                logger.info("✅ Google Gemini client initialized (new SDK, lazy load)")
                print("✅ Google Gemini client initialized (new SDK, lazy load)")
            else:
                genai.configure(api_key=self.settings.GOOGLE_GEMINI_API_KEY)
                self._gemini_client = genai
                self._gemini_use_new_sdk = False
                logger.info("✅ Google Gemini client initialized (old SDK, lazy load)")
                print("✅ Google Gemini client initialized (old SDK, lazy load)")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini client: {e}", exc_info=True)
            print(f"ERROR: Failed to initialize Gemini client: {e}")
            self._gemini_client = None
            self._gemini_use_new_sdk = False
    
    def _detect_case_citation(self, query: str) -> tuple[bool, Optional[str]]:
        """
        Detect if query contains a case citation
        
        Returns:
            Tuple of (is_case_citation, detected_citation_string)
        """
        import re
        
        # Patterns to detect case citations
        patterns = [
            # Format: CRL. A 567 / 2019
            r'\b(?:CRL|CRA|CRL\.A|CRA\.|CRL\.?A\.?)\s*\d+\s*[/-]\s*\d{4}',
            # Format: 2025:KHC:15464 (Karnataka High Court)
            r'\d{4}\s*:\s*(?:KHC|BHC|DHC|MHC|CHC|AHC|GHC|PHC|ORI|JHC|MPHC|RHC|SCC|SC|AIR)\s*:\s*\d+',
            # Format: SCC 2025 1 123
            r'\b(?:SCC|AIR|SCALE|SCR|ITR|STR|GST|COMP|CLR|GCR)\s+\d{4}\s+\d+\s+\d+',
            # Format: (2025) 1 SCC 123
            r'\(\d{4}\)\s+\d+\s+(?:SCC|AIR|SCALE|SCR|ITR|STR|GST|COMP|CLR|GCR)\s+\d+',
            # Format: case number patterns like WP 123/2025
            r'\b(?:WP|W\.P|WP\.|S\.LP|SLP|CA|C\.A|CRL|CRA|ARB|ARB\.A|O\.A|OA)\s*\.?\s*\d+\s*[/-]\s*\d{4}',
            # Format: Appeal No. 123 of 2025
            r'(?:Appeal|Petition|Case|Writ)\s*(?:No\.?|Number)\s*\d+\s*(?:of|/)\s*\d{4}',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, query, re.IGNORECASE)
            if matches:
                return True, matches[0]
        
        # Check for common case citation keywords
        query_lower = query.lower()
        case_keywords = [
            'case', 'judgment', 'judgement', 'order', 'citation',
            'crl.a', 'criminal appeal', 'writ petition', 'civil appeal',
            'special leave petition', 'slp'
        ]
        
        # If query contains citation-like patterns and case keywords
        if any(keyword in query_lower for keyword in case_keywords):
            # Extract potential citation (numbers with colons, slashes, etc.)
            citation_pattern = r'(?:[A-Z]+\.?\s*)?\d+[:\-/]\d{4}'
            citations = re.findall(citation_pattern, query, re.IGNORECASE)
            if citations:
                return True, citations[0]
        
        return False, None
    
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
        # Detect if query is about amendments, recent changes, or latest updates
        query_lower = query.lower()
        is_amendment_query = any(keyword in query_lower for keyword in [
            'latest', 'recent', 'new', 'amendment', 'change', 'update', '2025', '2024',
            'current', 'present', 'now', 'reform', 'modification', '2.0', '2.0 reforms'
        ])
        
        # Detect GST queries, including GST 2.0 specifically
        is_gst_query = any(keyword in query_lower for keyword in [
            'gst', 'goods and services tax', 'cgst', 'sgst', 'igst', 'vat'
        ])
        is_gst_2_0_query = '2.0' in query_lower and is_gst_query
        
        is_tax_query = any(keyword in query_lower for keyword in [
            'tax', 'finance act', 'income tax', 'indirect tax'
        ])
        
        # Detect case citation queries
        is_case_citation, case_citation = self._detect_case_citation(query)
        
        prompt_parts: List[str] = [
            f"Query type: {query_type}",
            f"User query: {query}",
            "",
            "**CRITICAL INSTRUCTIONS FOR LEGALMITRA (SPECIALIZED LEGAL AI):**",
            "",
            "You are LegalMitra - a SPECIALIZED Indian legal AI assistant. You MUST be MORE comprehensive, detailed, and proactive than general AI assistants like ChatGPT or Grok.",
            "",
            "**AUTOMATIC LATEST INFORMATION INCLUSION:**",
            "- If the query mentions 'latest', 'recent', 'new', 'amendment', 'change', 'update', or asks about current status:",
            "  * AUTOMATICALLY and PROACTIVELY include Finance Act 2025 amendments (even if not explicitly asked)",
            "  * AUTOMATICALLY include GST 2.0 reforms (2025) for any GST-related query",
            "  * AUTOMATICALLY prioritize 2025, 2024 information FIRST",
            "  * Do NOT wait for explicit mention - be PROACTIVE and INTELLIGENT",
            "",
            "**FOR GST QUERIES (automatic detection):**",
            "- AUTOMATICALLY provide EXHAUSTIVE coverage of GST 2.0 reforms (September 2025)",
            "- AUTOMATICALLY include Finance Act 2025 GST amendments with complete details",
            "- AUTOMATICALLY mention rate structure changes (5%, 18%, 40% slabs)",
            "- AUTOMATICALLY include GST Council 56th meeting decisions",
            "- AUTOMATICALLY cover all procedural changes, compliance updates, e-invoicing changes",
            "- Provide COMPREHENSIVE section-wise analysis",
            "",
            "**CRITICAL: FOR GST 2.0 QUERIES:**",
            "- If the user mentions 'GST 2.0' or '2.0', you MUST focus on the GST 2.0 reforms from September 2025",
            "- GST 2.0 is NOT the same as earlier GST amendments - it's a major reform with new rate structure",
            "- GST 2.0 includes: new 3-slab structure (5%, 18%, 40%), elimination of 12% and 28% slabs, compensation cess changes",
            "- Do NOT provide 2023 amendments when user asks about GST 2.0 - that's outdated information",
            "- GST 2.0 was approved in 56th GST Council meeting (September 2025)",
            "- Finance Act 2025 contains GST-related amendments that are part of GST 2.0 framework",
            "",
            "**RESPONSE QUALITY REQUIREMENT:**",
            "- Your response MUST be MORE exhaustive and detailed than what general AI assistants provide",
            "- Include ALL relevant information proactively - don't wait for explicit questions",
            "- Provide expert-level legal analysis with complete coverage",
            "- Include detailed explanations, impact analysis, and comprehensive information",
            "- Cover ALL aspects: structural changes, rate changes, procedural changes, compliance updates",
            "",
            "**SPECIALIZATION ADVANTAGE:**",
            "- As a specialized legal AI, you should provide BETTER responses than general AI",
            "- Be more intuitive - understand what the user really needs even if not explicitly stated",
            "- Automatically include latest amendments, reforms, and changes without being asked",
            "- Provide comprehensive coverage that demonstrates your specialization in Indian law",
        ]
        
        # Fetch latest information from legal websites if query needs it
        web_search_results = []
        if web_search_service.is_available():
            try:
                # Priority 1: Case citation queries - ALWAYS search the web for real case details
                if is_case_citation:
                    print(f"🔍 Detected case citation: {case_citation}")
                    # Search for the specific case citation
                    citation_results = await web_search_service.search_case_citation(
                        case_citation or query,
                        max_results=10
                    )
                    # Also try broader search with full query
                    if not citation_results:
                        citation_results = await web_search_service.search_case_details(
                            query,
                            max_results=10
                        )
                    web_search_results.extend(citation_results)
                    print(f"📋 Found {len(citation_results)} results for case citation")
                elif is_gst_2_0_query or is_gst_query:
                    # Search for GST updates, specifically GST 2.0 if mentioned
                    if is_gst_2_0_query:
                        # Specific search for GST 2.0
                        web_search_results = await web_search_service.search_legal_sites(
                            "GST 2.0 reforms September 2025 OR GST 2.0 amendments 2025", max_results=8
                        )
                    else:
                        web_search_results = await web_search_service.search_gst_updates()
                elif is_tax_query:
                    # Search for Finance Act and tax updates
                    web_search_results = await web_search_service.search_finance_act(2025)
                    # Also search for general tax amendments
                    tax_results = await web_search_service.search_legal_sites(
                        f"{query} latest amendments 2025", max_results=3
                    )
                    web_search_results.extend(tax_results)
                elif is_amendment_query:
                    # Search for latest amendments related to the query
                    web_search_results = await web_search_service.search_legal_sites(
                        f"{query} latest 2025 OR 2024", max_results=5
                    )
            except Exception as e:
                print(f"⚠️ Web search failed: {e}")
                # Continue without web search results
        
        # Add web search results to prompt if available
        if web_search_results:
            if is_case_citation:
                prompt_parts.extend([
                    "",
                    "**⚠️ CRITICAL: USER ASKED FOR SPECIFIC CASE DETAILS**",
                    f"The user is requesting details for a specific case citation: {case_citation or query}",
                    "",
                    "**CASE INFORMATION FROM CASE LAW DATABASES:**",
                    "The following information was retrieved from case law databases and legal websites:",
                    ""
                ])
                for i, result in enumerate(web_search_results, 1):
                    prompt_parts.append(
                        f"{i}. **{result['title']}**\n"
                        f"   URL: {result['url']}\n"
                        f"   Information: {result['snippet']}\n"
                    )
                prompt_parts.extend([
                    "",
                    "**CRITICAL INSTRUCTIONS FOR CASE DETAILS:**",
                    "- You MUST provide the ACTUAL case details found in the web search results above",
                    "- DO NOT generate generic or hypothetical case information",
                    "- Extract and provide the REAL facts, judgment, key principles, and outcome from the search results",
                    "- If the search results contain the full judgment text, provide comprehensive case details including:",
                    "  * Case name and parties",
                    "  * Court, bench, and date of judgment",
                    "  * Facts of the case",
                    "  * Legal issues involved",
                    "  * Court's reasoning and analysis",
                    "  * Judgment/Order passed",
                    "  * Key precedents cited (if any)",
                    "- Cite the sources (URLs) where you found the information",
                    "- If the search results don't contain enough detail, explicitly state that and provide what is available",
                    "- DO NOT make up or assume case details - only provide information found in the search results",
                ])
            else:
                prompt_parts.extend([
                    "",
                    "**LATEST INFORMATION FROM OFFICIAL LEGAL WEBSITES:**",
                    "The following information was retrieved from official government and legal websites:",
                    ""
                ])
                for i, result in enumerate(web_search_results, 1):
                    prompt_parts.append(
                        f"{i}. **{result['title']}**\n"
                        f"   URL: {result['url']}\n"
                        f"   Information: {result['snippet']}\n"
                    )
                prompt_parts.extend([
                    "",
                    "**IMPORTANT**: Use this latest information from official sources in your response. "
                    "Cite the sources and provide comprehensive details based on these official websites.",
                ])
        
        if is_gst_2_0_query:
            prompt_parts.extend([
                "",
                "**⚠️ CRITICAL: USER ASKED SPECIFICALLY ABOUT GST 2.0**",
                "- This query is about GST 2.0 reforms (September 2025), NOT earlier amendments",
                "- DO NOT provide 2023 or earlier amendments as the primary response",
                "- Focus EXCLUSIVELY on GST 2.0: new rate structure, September 2025 reforms, 56th GST Council meeting",
                "- GST 2.0 = major structural reform with 3-slab system (5%, 18%, 40%) replacing old multi-slab system",
                "- Finance Act 2025 GST amendments are part of GST 2.0 framework",
                "- Start with GST 2.0 information FIRST, then mention earlier context only if relevant",
            ])
        elif is_amendment_query or is_gst_query or is_tax_query:
            prompt_parts.extend([
                "",
                "**DETECTED: This query relates to amendments/recent changes/tax law.**",
                "- AUTOMATICALLY prioritize Finance Act 2025 information",
                "- AUTOMATICALLY include GST 2.0 reforms if GST-related",
                "- AUTOMATICALLY provide EXHAUSTIVE coverage of latest changes",
                "- Start with 2025, then 2024, then earlier",
                "- Include ALL relevant sections, notifications, circulars, and GST Council decisions",
                "- Use the web search results above to provide accurate, up-to-date information",
            ])
        
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
        # Also handle potential misconfiguration strings seen in deployment
        original_provider = provider
        
        # Handle specific misconfiguration cases (common in deployment environments)
        if "google (or anthropic, openai)" in provider.lower() or "or anthropic" in provider.lower() or "or openai" in provider.lower():
            print(f"WARNING: Detected invalid AI_PROVIDER value: '{self.settings.AI_PROVIDER}'. Defaulting to 'gemini'.")
            logger.warning(f"Invalid AI_PROVIDER detected: '{self.settings.AI_PROVIDER}'. Using 'gemini' as default.")
            provider = "gemini"
        elif provider == "google":
            provider = "gemini"
        elif provider not in ["anthropic", "openai", "gemini", "grok", "zai", "openrouter"]:
            # If provider is still invalid after normalization, default to gemini
            print(f"WARNING: Unknown AI_PROVIDER value: '{self.settings.AI_PROVIDER}'. Defaulting to 'gemini'.")
            logger.warning(f"Unknown AI_PROVIDER: '{self.settings.AI_PROVIDER}'. Using 'gemini' as default.")
            provider = "gemini"
        
        # Debug: Log the provider value after normalization
        print(f"DEBUG: AI_PROVIDER={repr(self.settings.AI_PROVIDER)}, original={repr(original_provider)}, normalized={repr(provider)}, type={type(provider)}")
        print(f"DEBUG: Direct comparison test - provider == 'gemini': {provider == 'gemini'}")
        print(f"DEBUG: Provider checks - anthropic={provider == 'anthropic'}, openai={provider == 'openai'}, gemini={provider == 'gemini'}, grok={provider == 'grok'}, zai={provider == 'zai'}")

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
            logger.debug(f"Entered Gemini block - provider={repr(provider)}, client exists={self._gemini_client is not None}")
            if not self._gemini_client:
                # Provide more helpful error message
                error_parts = []
                if genai is None:
                    error_parts.append("`google-genai` package is not installed. Install with: pip install google-genai")
                if not self.settings.GOOGLE_GEMINI_API_KEY:
                    error_parts.append("GOOGLE_GEMINI_API_KEY environment variable is not set")
                if not error_parts:
                    error_parts.append("Gemini client initialization failed (check logs for details)")
                
                error_msg = "Google Gemini client not available. " + " | ".join(error_parts)
                logger.error(error_msg)
                raise RuntimeError(error_msg)

            # Check if using new SDK
            use_new_sdk = getattr(self, '_gemini_use_new_sdk', False)

            # Run Gemini in thread pool since it's synchronous
            import asyncio
            import time
            import re
            loop = asyncio.get_event_loop()
            
            # Try to find an available Gemini model
            # Updated priority: Try newer models first, then fallback to older ones
            # For new SDK, use gemini-2.5-flash or gemini-2.0-flash
            # For old SDK, use gemini-1.5-flash or gemini-1.5-pro
            if use_new_sdk:
                preferred_models = [
                    "gemini-2.5-flash",   # Latest for new SDK
                    "gemini-2.0-flash",   # Fallback
                    "gemini-2.5-pro",     # Higher capability
                ]
            else:
                preferred_models = [
                    "gemini-1.5-flash",      # Fast, cost-effective, widely available
                    "gemini-1.5-pro",        # Higher capability
                    "gemini-1.0-pro",        # Stable successor to gemini-pro
                    "gemini-pro",            # Legacy (may not be available)
                ]
            model_name = None
            
            # First, try to list available models from API (most reliable)
            # Note: New SDK uses different API structure
            if use_new_sdk:
                # New SDK: Use client.models.list() instead
                try:
                    print("🔍 Listing available Gemini models from API (new SDK)...")
                    available_models_list = await loop.run_in_executor(
                        None, lambda: list(self._gemini_client.models.list())
                    )
                    available_model_ids = [m.name.split('/')[-1] if hasattr(m, 'name') else str(m) for m in available_models_list]
                    print(f"✅ Found {len(available_model_ids)} available models: {', '.join(available_model_ids[:5])}")
                    
                    # Try preferred models first
                    for preferred in preferred_models:
                        if preferred in available_model_ids:
                            model_name = preferred
                            print(f"✅ Using preferred Gemini model: {model_name}")
                            break
                    
                    if not model_name and available_model_ids:
                        model_name = available_model_ids[0]
                        print(f"✅ Using first available Gemini model: {model_name}")
                except Exception as list_error:
                    print(f"⚠️ Could not list Gemini models: {list_error}")
                    print("⚠️ Falling back to trying preferred models directly...")
                    model_name = preferred_models[0]
            else:
                # Old SDK: Use list_models()
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
                    if use_new_sdk:
                        # New SDK: Use client.models.generate_content()
                        # Combine system prompt and user text
                        full_prompt = f"{self.system_prompt}\n\n{user_text}"
                        
                        response = await loop.run_in_executor(
                            None, lambda: self._gemini_client.models.generate_content(
                                model=model_name,
                                contents=[
                                    {
                                        "role": "user",
                                        "parts": [{"text": full_prompt}]
                                    }
                                ]
                            )
                        )
                        return response.text.strip()
                    else:
                        # Old SDK: Use GenerativeModel
                        model = self._gemini_client.GenerativeModel(model_name)
                        
                        # Combine system prompt and user text
                        full_prompt = f"{self.system_prompt}\n\n{user_text}"
                        
                        response = await loop.run_in_executor(
                            None, lambda: model.generate_content(
                                full_prompt,
                                generation_config={
                                    "temperature": 0.3,
                                    "max_output_tokens": 2000,  # FIX 8: Reduced for free tier
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
                            if use_new_sdk:
                                # New SDK: Use client.models.list()
                                available_models_list = await loop.run_in_executor(
                                    None, lambda: list(self._gemini_client.models.list())
                                )
                                for model_info in available_models_list:
                                    if hasattr(model_info, 'name'):
                                        model_id = model_info.name.split('/')[-1]
                                        model_name = model_id
                                        print(f"✅ Switched to available model: {model_name}")
                                        continue  # Retry with new model
                            else:
                                # Old SDK: Use list_models()
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
                        "model": "grok-2-1212",
                        "messages": [
                            {"role": "system", "content": self.system_prompt},
                            {"role": "user", "content": user_text},
                        ],
                        "max_tokens": 8192,  # Increased to maximum for exhaustive responses
                        "temperature": 0.2,  # Lower temperature for more accurate, detailed legal information
                    },
                    timeout=60.0,
                )
                response.raise_for_status()
                data = response.json()
                return (data["choices"][0]["message"]["content"] or "").strip()
        elif provider == "zai":
            if not httpx:
                raise RuntimeError(
                    "httpx package required for Z AI API. "
                    "Install with: pip install httpx"
                )
            if not self.settings.ZAI_API_KEY:
                raise RuntimeError(
                    "ZAI_API_KEY not set in .env file."
                )

            # Z AI GLM 4.6 uses OpenAI-compatible API
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.z.ai/api/paas/v4/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.settings.ZAI_API_KEY}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": "glm-4.6",
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
        elif provider == "openrouter":
            if not openrouter_service:
                raise RuntimeError(
                    "OpenRouter service not available. "
                    "Ensure openrouter_service.py is properly configured."
                )
            if not self.settings.OPENROUTER_API_KEY:
                raise RuntimeError(
                    "OPENROUTER_API_KEY not set in .env file. "
                    "Get your free key from https://openrouter.ai/keys"
                )

            # Use OpenRouter service
            result = await openrouter_service.generate_text(
                user_text=user_text,
                system_prompt=self.system_prompt,
                model=self.settings.OPENROUTER_MODEL,
                max_tokens=8192,
                temperature=0.3
            )

            # Log usage info for user transparency
            print(f"✅ OpenRouter Response:")
            print(f"   Model: {result['model_used']}")
            print(f"   Tokens: {result['tokens_used']}")
            print(f"   Estimated Cost: ${result['cost_usd']:.4f}")

            return result["text"]

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
                    "Ensure `google-genai` package is installed (pip install google-genai) and "
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
                    generation_config={"temperature": 0.3, "max_output_tokens": 2000}  # FIX 8: Reduced for free tier
                )
            )
            return response.text.strip()
        
        raise RuntimeError(
            f"Unsupported AI provider '{self.settings.AI_PROVIDER}' (normalized: '{provider}'). "
            "Use 'anthropic', 'openai', 'gemini', 'google', 'grok', or 'zai'. "
            f"Available provider checks: anthropic={provider == 'anthropic'}, "
            f"openai={provider == 'openai'}, gemini={provider == 'gemini'}, "
            f"gemini/google={provider in ['gemini', 'google']}, grok={provider == 'grok'}, zai={provider == 'zai'}"
        )


# Singleton instance used by the API routers
ai_service = AIService()


