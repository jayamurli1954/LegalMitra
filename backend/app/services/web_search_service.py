"""
Web Search Service for LegalMitra
Fetches latest legal information from official government and legal websites
"""

from typing import List, Dict, Optional
import httpx
from app.core.config import get_settings
from app.services.search_cache import search_cache


class WebSearchService:
    """Service for searching legal websites to get latest information"""
    
    # Official legal websites to search
    LEGAL_SITES = [
        "indiancode.nic.in",           # India Code
        "egazette.nic.in",              # eGazette Portal
        "prsindia.org",                 # PRS Legislative Research
        "pib.gov.in",                   # Press Information Bureau
        "legislative.gov.in",           # Legislative Department
        "legalaffairs.gov.in",          # Department of Legal Affairs
        "mpa.gov.in",                   # Ministry of Parliamentary Affairs
        "ecourts.gov.in",               # eCourts Services
        "njdg.ecourts.gov.in",          # National Judicial Data Grid
        "main.sci.gov.in",              # Supreme Court of India
    ]
    
    # Case law databases and legal websites (publicly accessible)
    CASE_LAW_SITES = [
        "indiankanoon.org",             # Indian Kanoon - Free case law database
        "manupatra.com",                # Manupatra - Legal database
        "casemine.com",                 # Casemine - Case law search
        "judis.nic.in",                 # Judgments Information System (official)
        "main.sci.gov.in",              # Supreme Court of India
        "ecourts.gov.in",               # eCourts Services
        "karnatakajudiciary.kar.nic.in", # Karnataka High Court
        "hckarnataka.gov.in",           # Karnataka High Court official
        "bombayhighcourt.nic.in",       # Bombay High Court
        "allahabadhighcourt.in",        # Allahabad High Court
        "calcuttahighcourt.gov.in",     # Calcutta High Court
        "madrashighcourt.nic.in",       # Madras High Court
        "delhihighcourt.nic.in",        # Delhi High Court
    ]
    
    def __init__(self):
        self.settings = get_settings()
        self.api_key = self.settings.GOOGLE_CUSTOM_SEARCH_API_KEY
        self.search_engine_id = self.settings.GOOGLE_CUSTOM_SEARCH_ENGINE_ID
        
    def is_available(self) -> bool:
        """Check if web search is configured"""
        return bool(self.api_key and self.search_engine_id)
    
    async def search_legal_sites(
        self,
        query: str,
        max_results: int = 5,
        sites: Optional[List[str]] = None,
        use_cache: bool = True
    ) -> List[Dict[str, str]]:
        """
        Search legal websites for latest information

        Args:
            query: Search query
            max_results: Maximum number of results to return
            sites: Optional list of specific sites to search (defaults to all legal sites)
            use_cache: Whether to use cached results (default: True)

        Returns:
            List of search results with title, url, and snippet
        """
        if not self.is_available():
            return []

        # Use specific sites if provided, otherwise use all legal sites
        target_sites = sites or self.LEGAL_SITES

        # Build site-specific search query
        # Format: "query site:example.com OR site:example2.com"
        site_filters = " OR ".join([f"site:{site}" for site in target_sites])
        search_query = f"{query} ({site_filters})"

        # Check cache first
        cache_params = {
            'max_results': max_results,
            'sites': ','.join(sorted(target_sites)) if target_sites else 'all'
        }

        if use_cache:
            cached_results = search_cache.get(search_query, cache_params)
            if cached_results is not None:
                print(f"✅ Cache HIT for query: {query[:50]}...")
                return cached_results
            print(f"❌ Cache MISS for query: {query[:50]}...")

        try:
            # Google Custom Search API endpoint
            url = "https://www.googleapis.com/customsearch/v1"
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    url,
                    params={
                        "key": self.api_key,
                        "cx": self.search_engine_id,
                        "q": search_query,
                        "num": min(max_results, 10),  # Google API max is 10
                    }
                )
                response.raise_for_status()
                data = response.json()

                results = []
                for item in data.get("items", [])[:max_results]:
                    results.append({
                        "title": item.get("title", ""),
                        "url": item.get("link", ""),
                        "snippet": item.get("snippet", ""),
                    })

                # Cache the results
                if use_cache and results:
                    search_cache.set(search_query, results, cache_params)
                    print(f"💾 Cached {len(results)} results for query: {query[:50]}...")

                return results

        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"⚠️ Web search error: {e}")
            print(f"Error details: {error_details}")
            # Check for specific error types
            if hasattr(e, 'response'):
                try:
                    error_response = e.response.json() if hasattr(e.response, 'json') else str(e.response.text)
                    print(f"API Error Response: {error_response}")
                except:
                    print(f"API Error Status: {e.response.status_code if hasattr(e.response, 'status_code') else 'N/A'}")
            return []
    
    async def search_latest_amendments(
        self, 
        act_name: str, 
        year: Optional[int] = None
    ) -> List[Dict[str, str]]:
        """
        Search for latest amendments to a specific act
        
        Args:
            act_name: Name of the act (e.g., "GST Act", "Income Tax Act")
            year: Optional year to search for (defaults to 2025, 2024)
        
        Returns:
            List of search results
        """
        if year:
            query = f"latest amendments {act_name} {year}"
        else:
            query = f"latest amendments {act_name} 2025 OR 2024"
        
        return await self.search_legal_sites(query, max_results=5)
    
    async def search_finance_act(self, year: int = 2025) -> List[Dict[str, str]]:
        """Search for Finance Act of specific year"""
        query = f"Finance Act {year} amendments changes"
        return await self.search_legal_sites(query, max_results=5)
    
    async def search_gst_updates(self) -> List[Dict[str, str]]:
        """Search for latest GST updates and reforms"""
        query = "GST 2.0 reforms 2025 OR GST latest amendments 2025 OR GST Council decisions"
        return await self.search_legal_sites(query, max_results=5)
    
    async def search_case_citation(
        self, 
        case_citation: str,
        max_results: int = 10
    ) -> List[Dict[str, str]]:
        """
        Search for a specific case by citation
        
        Args:
            case_citation: Case citation (e.g., "CRL. A 567 / 2019", "2025:KHC:15464")
            max_results: Maximum number of results to return
        
        Returns:
            List of search results with title, url, and snippet
        """
        if not self.is_available():
            return []
        
        # Search across case law databases
        try:
            # Use general web search for case citations (without site restriction first to cast wider net)
            # Then try case law specific sites
            search_query = f'"{case_citation}" judgment OR case'
            
            # First, try searching case law databases specifically
            case_results = await self.search_legal_sites(
                search_query, 
                max_results=max_results,
                sites=self.CASE_LAW_SITES
            )
            
            # If we got results from case law sites, return them
            if case_results:
                return case_results
            
            # If no results from case law sites, try general search without site restriction
            # We'll use the Google Custom Search API without site filters
            url = "https://www.googleapis.com/customsearch/v1"
            
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.get(
                    url,
                    params={
                        "key": self.api_key,
                        "cx": self.search_engine_id,
                        "q": search_query,
                        "num": min(max_results, 10),
                    }
                )
                response.raise_for_status()
                data = response.json()
                
                results = []
                for item in data.get("items", [])[:max_results]:
                    results.append({
                        "title": item.get("title", ""),
                        "url": item.get("link", ""),
                        "snippet": item.get("snippet", ""),
                    })
                
                return results
                
        except Exception as e:
            print(f"⚠️ Case citation search error: {e}")
            return []
    
    async def search_case_details(
        self,
        case_query: str,
        max_results: int = 10
    ) -> List[Dict[str, str]]:
        """
        Search for case details using a query string (may contain citation or description)
        
        Args:
            case_query: Case query (citation or description)
            max_results: Maximum number of results to return
        
        Returns:
            List of search results with title, url, and snippet
        """
        if not self.is_available():
            return []
        
        # Build comprehensive search query
        search_query = f'"{case_query}" case judgment India'
        
        # Search both case law databases and official court websites
        all_sites = self.CASE_LAW_SITES + self.LEGAL_SITES
        return await self.search_legal_sites(
            search_query,
            max_results=max_results,
            sites=all_sites
        )


# Singleton instance
web_search_service = WebSearchService()


