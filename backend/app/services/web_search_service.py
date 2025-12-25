"""
Web Search Service for LegalMitra
Fetches latest legal information from official government and legal websites
"""

from typing import List, Dict, Optional
import httpx
from app.core.config import get_settings


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
        sites: Optional[List[str]] = None
    ) -> List[Dict[str, str]]:
        """
        Search legal websites for latest information
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
            sites: Optional list of specific sites to search (defaults to all legal sites)
        
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
                
                return results
                
        except Exception as e:
            print(f"⚠️ Web search error: {e}")
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


# Singleton instance
web_search_service = WebSearchService()


