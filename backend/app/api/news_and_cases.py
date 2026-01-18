"""
API endpoints for major cases and latest legal news
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from app.services.ai_service import ai_service
from app.services.web_search_service import web_search_service
from app.services.document_storage import document_storage
from app.services.search_cache import search_cache
from datetime import datetime
import re
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


class CaseItem(BaseModel):
    """Model for a major case item"""
    title: str
    court: str
    year: Optional[int] = None
    citation: Optional[str] = None
    summary: str
    query: str  # Query to get more details


class NewsItem(BaseModel):
    """Model for a legal news item"""
    title: str
    source: Optional[str] = None
    date: Optional[str] = None
    summary: str
    query: str  # Query to get more details


class CasesResponse(BaseModel):
    """Response model for major cases"""
    cases: List[CaseItem]


class NewsResponse(BaseModel):
    """Response model for latest legal news"""
    news: List[NewsItem]


@router.get("/major-cases", response_model=CasesResponse)
async def get_major_cases(force_web: bool = False):
    """
    Get recent major judgments from Supreme Court and High Courts
    Preloaded when the page opens
    Uses Google Custom Search to fetch latest information
    
    Args:
        force_web: If True, skip uploaded documents and force web search
    """
    try:
        current_year = datetime.now().year
        
        # FIRST: Check for uploaded documents (cases) from users (unless force_web is True)
        if not force_web:
            try:
                uploaded_cases = await document_storage.get_recent_cases(limit=5)
                if uploaded_cases:
                    logger.info(f"Found {len(uploaded_cases)} uploaded cases, using them instead of defaults")
                    # Convert to CaseItem format
                    case_items = [
                        CaseItem(
                            title=case.get("title", "Uploaded Case"),
                            court=case.get("court", "Uploaded Document"),
                            year=case.get("year", current_year),
                            citation=case.get("citation"),
                            summary=case.get("summary", "Case document uploaded by user."),
                            query=case.get("query", f"Tell me about: {case.get('title')}")
                        )
                        for case in uploaded_cases
                    ]
                    return CasesResponse(cases=case_items)
            except Exception as storage_error:
                logger.warning(f"Error retrieving uploaded cases: {storage_error}")
                # Continue to web search fallback
        
        # SECOND: Try web search if no uploaded documents
        # Clear settings cache to ensure fresh API key is loaded
        try:
            from app.core.config import get_settings
            get_settings.cache_clear()
        except Exception as cache_error:
            logger.warning(f"Could not clear settings cache: {cache_error}")
        
        # Reload web search service to get fresh settings
        try:
            from app.services.web_search_service import WebSearchService
            fresh_web_search = WebSearchService()
        except Exception as ws_error:
            logger.error(f"Could not initialize web search service: {ws_error}")
            # Fall through to defaults
            cases = _get_default_cases(current_year)
            return CasesResponse(cases=cases)
        
        # Use Google Custom Search to get latest major cases
        # Log search availability
        logger.info(f"Web search service available: {fresh_web_search.is_available()}")
        logger.info(f"API Key configured: {bool(fresh_web_search.api_key)}")
        logger.info(f"Engine ID configured: {bool(fresh_web_search.search_engine_id)}")
        
        if fresh_web_search.is_available():
            try:
                logger.info(f"Searching for major cases for year {current_year}...")
                
                # Try multiple search strategies with better queries
                # Strategy 1: Search case law databases for recent judgments
                search_queries = [
                    f'"{current_year}" "Supreme Court" "judgment" India',
                    f'"{current_year-1}" "Supreme Court" "judgment" India',
                    f'"{current_year}" "High Court" "judgment" India',
                    f'"recent judgment" "{current_year}" India court',
                ]
                
                all_results = []
                for search_query in search_queries:
                    # First try case law databases
                    case_results = await fresh_web_search.search_legal_sites(
                        search_query,
                        max_results=5,
                        sites=fresh_web_search.CASE_LAW_SITES
                    )
                    all_results.extend(case_results)
                    
                    # If we don't have enough, try broader search without site restriction
                    if len(all_results) < 5:
                        # Use general search (no site restriction) via direct API call
                        try:
                            import httpx
                            
                            url = "https://www.googleapis.com/customsearch/v1"
                            async with httpx.AsyncClient(timeout=15.0) as client:
                                response = await client.get(
                                    url,
                                    params={
                                        "key": fresh_web_search.api_key,
                                        "cx": fresh_web_search.search_engine_id,
                                        "q": f"{search_query} judgment India",
                                        "num": 5,
                                    }
                                )
                                response.raise_for_status()
                                data = response.json()
                                
                                for item in data.get("items", []):
                                    # Only add if not duplicate
                                    if not any(r.get("url") == item.get("link") for r in all_results):
                                        all_results.append({
                                            "title": item.get("title", ""),
                                            "url": item.get("link", ""),
                                            "snippet": item.get("snippet", ""),
                                        })
                                        if len(all_results) >= 5:
                                            break
                        except Exception as e:
                            logger.warning(f"Broader search error: {e}")
                    
                    if len(all_results) >= 5:
                        break
                
                logger.info(f"Found {len(all_results)} search results for major cases")
                
                # Convert search results to CaseItem format
                # Filter out homepage/results that don't look like actual cases
                cases = []
                for result in all_results[:10]:  # Check more to filter better
                    title = result.get("title", "Recent Judgment")
                    snippet = result.get("snippet", "")
                    url = result.get("url", "")
                    
                    # Skip homepages and non-case pages
                    title_lower = title.lower()
                    if any(skip_word in title_lower for skip_word in [
                        'home', 'welcome', 'login', 'register', 'about', 'contact',
                        'main page', 'index', 'search', 'results'
                    ]):
                        continue
                    
                    # Extract court and year from title/snippet
                    court = "Supreme Court of India"
                    year = current_year
                    
                    snippet_lower = snippet.lower()
                    
                    if "karnataka" in title_lower or "karnataka" in snippet_lower:
                        court = "Karnataka High Court"
                    elif "bombay" in title_lower or "bombay" in snippet_lower:
                        court = "Bombay High Court"
                    elif "delhi" in title_lower or "delhi" in snippet_lower:
                        court = "Delhi High Court"
                    elif "calcutta" in title_lower or "calcutta" in snippet_lower or "kolkata" in title_lower:
                        court = "Calcutta High Court"
                    elif "madras" in title_lower or "madras" in snippet_lower or "chennai" in title_lower:
                        court = "Madras High Court"
                    elif "allahabad" in title_lower or "allahabad" in snippet_lower:
                        court = "Allahabad High Court"
                    elif "high court" in title_lower or "high court" in snippet_lower:
                        court = "High Court"
                    elif "supreme court" in title_lower or "supreme court" in snippet_lower or "sc" in title_lower:
                        court = "Supreme Court of India"
                    
                    # Extract year
                    year_match = re.search(r'\b(20\d{2})\b', title + " " + snippet)
                    if year_match:
                        year = int(year_match.group(1))
                    
                    # Create case item
                    cases.append(CaseItem(
                        title=title[:200],
                        court=court,
                        year=year,
                        citation=None,
                        summary=snippet[:300] if snippet else "Recent important judgment from Indian courts.",
                        query=f"Tell me about the case: {title}"
                    ))
                
                if cases:
                    logger.info(f"Returning {len(cases)} cases from web search")
                    return CasesResponse(cases=cases)
                else:
                    logger.warning("No cases found in web search, using defaults")
            except Exception as e:
                import traceback
                logger.error(f"Web search error for cases: {e}")
                logger.error(traceback.format_exc())
                # Fall through to default cases
        
        # Fallback: Return default cases if web search fails or is not available
        cases = _get_default_cases(current_year)
        return CasesResponse(cases=cases)
        
    except Exception as e:
        # Return default cases on any error - never fail, always return something
        import traceback
        print(f"Error in get_major_cases: {e}")
        print(traceback.format_exc())
        current_year = datetime.now().year
        cases = _get_default_cases(current_year)
        return CasesResponse(cases=cases)


@router.get("/legal-news", response_model=NewsResponse)
async def get_legal_news(force_web: bool = False):
    """
    Get latest legal news and updates
    Preloaded when the page opens
    Uses Google Custom Search to fetch latest information
    
    Args:
        force_web: If True, skip uploaded documents and force web search
    """
    try:
        current_year = datetime.now().year
        
        # FIRST: Check for uploaded documents (news) from users (unless force_web is True)
        if not force_web:
            try:
                uploaded_news = await document_storage.get_recent_news(limit=5)
                if uploaded_news:
                    logger.info(f"Found {len(uploaded_news)} uploaded news items, using them instead of defaults")
                    # Convert to NewsItem format
                    news_items = [
                        NewsItem(
                            title=news.get("title", "Uploaded Document"),
                            source=news.get("source", "Uploaded Document"),
                            date=news.get("date", str(current_year)),
                            summary=news.get("summary", "Legal document uploaded by user."),
                            query=news.get("query", f"Tell me more about: {news.get('title')}")
                        )
                        for news in uploaded_news
                    ]
                    return NewsResponse(news=news_items)
            except Exception as storage_error:
                logger.warning(f"Error retrieving uploaded news: {storage_error}")
                # Continue to web search fallback
        
        # SECOND: Try web search if no uploaded documents
        # Clear settings cache to ensure fresh API key is loaded
        from app.core.config import get_settings
        get_settings.cache_clear()
        
        # Reload web search service to get fresh settings
        from app.services.web_search_service import WebSearchService
        fresh_web_search = WebSearchService()
        
        # Use Google Custom Search to get latest legal news
        logger.info(f"Web search service available (news): {fresh_web_search.is_available()}")
        
        if fresh_web_search.is_available():
            try:
                logger.info(f"Searching for legal news for year {current_year}...")
                
                # Try multiple search strategies
                search_queries = [
                    f"latest legal news India {current_year}",
                    f"legal updates India {current_year} OR {current_year-1}",
                    f"legal reforms India {current_year}",
                    f"law amendments India {current_year}",
                ]
                
                all_results = []
                for search_query in search_queries:
                    # Search official legal sites
                    news_results = await fresh_web_search.search_legal_sites(
                        search_query,
                        max_results=5
                    )
                    all_results.extend(news_results)
                    
                    # If we don't have enough, try broader search
                    if len(all_results) < 5:
                        try:
                            import httpx
                            url = "https://www.googleapis.com/customsearch/v1"
                            async with httpx.AsyncClient(timeout=15.0) as client:
                                response = await client.get(
                                    url,
                                    params={
                                        "key": fresh_web_search.api_key,
                                        "cx": fresh_web_search.search_engine_id,
                                        "q": search_query,
                                        "num": 5,
                                    }
                                )
                                response.raise_for_status()
                                data = response.json()
                                
                                for item in data.get("items", []):
                                    # Prefer official sites but accept others if needed
                                    url_check = item.get("link", "").lower()
                                    if not any(r.get("url") == item.get("link") for r in all_results):
                                        all_results.append({
                                            "title": item.get("title", ""),
                                            "url": item.get("link", ""),
                                            "snippet": item.get("snippet", ""),
                                        })
                                        if len(all_results) >= 5:
                                            break
                        except Exception as e:
                            logger.warning(f"Broader news search error: {e}")
                    
                    if len(all_results) >= 5:
                        break
                
                logger.info(f"Found {len(all_results)} search results for legal news")
                
                # Convert search results to NewsItem format
                news_items = []
                for result in all_results[:5]:
                    title = result.get("title", "Latest Legal News")
                    snippet = result.get("snippet", "")
                    url = result.get("url", "")
                    
                    # Extract source from URL
                    source = None
                    url_lower = url.lower()
                    if "pib.gov.in" in url_lower:
                        source = "PIB"
                    elif "prsindia.org" in url_lower:
                        source = "PRS Legislative Research"
                    elif "legislative.gov.in" in url_lower:
                        source = "Legislative Department"
                    elif "legalaffairs.gov.in" in url_lower:
                        source = "Department of Legal Affairs"
                    elif "egazette.nic.in" in url_lower:
                        source = "eGazette"
                    elif "indiancode.nic.in" in url_lower:
                        source = "India Code"
                    elif "cbic.gov.in" in url_lower or "gst.gov.in" in url_lower:
                        source = "CBIC"
                    elif "finmin.nic.in" in url_lower:
                        source = "Ministry of Finance"
                    elif "mca.gov.in" in url_lower:
                        source = "Ministry of Corporate Affairs"
                    else:
                        # Extract domain name as source
                        domain_match = re.search(r'://(?:www\.)?([^/]+)', url)
                        if domain_match:
                            source = domain_match.group(1).replace('.in', '').replace('.org', '').title()
                    
                    # Extract date
                    date_match = re.search(r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+(\d{4})\b', title + " " + snippet, re.IGNORECASE)
                    date_str = str(current_year)
                    if date_match:
                        date_str = date_match.group(2)
                    else:
                        year_match = re.search(r'\b(20\d{2})\b', title + " " + snippet)
                        if year_match:
                            date_str = year_match.group(1)
                    
                    # Create news item
                    news_items.append(NewsItem(
                        title=title[:200],
                        source=source or "Legal Updates",
                        date=date_str,
                        summary=snippet[:300] if snippet else "Latest legal news and updates from India.",
                        query=f"Tell me more about: {title}"
                    ))
                
                if news_items:
                    logger.info(f"Returning {len(news_items)} news items from web search")
                    return NewsResponse(news=news_items)
                else:
                    logger.warning("No news items found in web search, using defaults")
            except Exception as e:
                import traceback
                logger.error(f"Web search error for news: {e}")
                print(traceback.format_exc())
                # Fall through to default news
        
        # Fallback: Return default news if web search fails or is not available
        news_items = _get_default_news(current_year)
        return NewsResponse(news=news_items)
        
    except Exception as e:
        # Return default news on any error - never fail, always return something
        import traceback
        print(f"Error in get_legal_news: {e}")
        print(traceback.format_exc())
        current_year = datetime.now().year
        news_items = _get_default_news(current_year)
        return NewsResponse(news=news_items)


async def _parse_cases_from_response(response_text: str, current_year: int) -> List[CaseItem]:
    """
    Parse AI response to extract structured case information
    This is a simplified parser - in production, use more sophisticated parsing
    """
    cases = []
    
    # Split response by common patterns
    lines = response_text.split('\n')
    current_case = None
    
    for line in lines:
        line = line.strip()
        if not line or len(line) < 10:
            continue
            
        # Try to identify case entries
        # Look for patterns like "1.", "Case Name:", etc.
        if any(line.startswith(f"{i}.") for i in range(1, 10)) or "Case:" in line or "v." in line:
            if current_case and current_case.get('summary'):
                cases.append(CaseItem(**current_case))
            
            # Extract case name
            case_name = line
            if ":" in line:
                case_name = line.split(":", 1)[-1].strip()
            if any(line.startswith(f"{i}.") for i in range(1, 10)):
                case_name = line.split(".", 1)[-1].strip()
            
            current_case = {
                "title": case_name[:200],  # Limit length
                "court": "Supreme Court of India",  # Default
                "year": current_year,
                "citation": None,
                "summary": "",
                "query": f"Explain the case {case_name} in detail"
            }
        
        elif current_case:
            # Extract court, year, citation from line
            if "Supreme Court" in line or "SC" in line:
                current_case["court"] = "Supreme Court of India"
            elif "High Court" in line or "HC" in line:
                # Try to extract state
                current_case["court"] = line
            elif any(str(year) in line for year in range(2000, current_year + 2)):
                # Extract year
                for year in range(2000, current_year + 2):
                    if str(year) in line:
                        current_case["year"] = year
                        break
            
            # Build summary
            if len(current_case["summary"]) < 300:
                current_case["summary"] += " " + line
                current_case["summary"] = current_case["summary"].strip()
    
    # Add last case
    if current_case and current_case.get('summary'):
        cases.append(CaseItem(**current_case))
    
    # If parsing failed, create default structured cases
    if len(cases) < 3:
        cases = _get_default_cases(current_year)
    
    return cases[:5]  # Return max 5 cases


async def _parse_news_from_response(response_text: str, current_year: int) -> List[NewsItem]:
    """
    Parse AI response to extract structured news information
    """
    news_items = []
    
    lines = response_text.split('\n')
    current_news = None
    
    for line in lines:
        line = line.strip()
        if not line or len(line) < 10:
            continue
        
        # Try to identify news entries
        if any(line.startswith(f"{i}.") for i in range(1, 10)) or "News:" in line or "Update:" in line:
            if current_news and current_news.get('summary'):
                news_items.append(NewsItem(**current_news))
            
            # Extract headline
            headline = line
            if ":" in line:
                headline = line.split(":", 1)[-1].strip()
            if any(line.startswith(f"{i}.") for i in range(1, 10)):
                headline = line.split(".", 1)[-1].strip()
            
            current_news = {
                "title": headline[:200],
                "source": None,
                "date": None,
                "summary": "",
                "query": f"Tell me more about {headline}"
            }
        elif current_news:
            # Build summary
            if len(current_news["summary"]) < 300:
                current_news["summary"] += " " + line
                current_news["summary"] = current_news["summary"].strip()
    
    # Add last news item
    if current_news and current_news.get('summary'):
        news_items.append(NewsItem(**current_news))
    
    # If parsing failed, create default structured news
    if len(news_items) < 3:
        news_items = _get_default_news(current_year)
    
    return news_items[:5]  # Return max 5 news items


def _get_default_cases(year: int) -> List[CaseItem]:
    """Default cases if parsing fails"""
    return [
        CaseItem(
            title="Recent GST Case",
            court="Supreme Court of India",
            year=year,
            citation=None,
            summary="Latest important judgment related to GST law and taxation.",
            query="What are the latest important GST judgments from Supreme Court?"
        ),
        CaseItem(
            title="Corporate Law Decision",
            court="Supreme Court of India",
            year=year,
            citation=None,
            summary="Recent significant decision affecting corporate governance and compliance.",
            query="What are the latest corporate law judgments?"
        ),
        CaseItem(
            title="Constitutional Matter",
            court="Supreme Court of India",
            year=year,
            citation=None,
            summary="Recent constitutional interpretation or fundamental rights case.",
            query="What are the latest constitutional law judgments?"
        ),
    ]


def _get_default_news(year: int) -> List[NewsItem]:
    """Default news if parsing fails"""
    return [
        NewsItem(
            title="GST 2.0 Reforms Update",
            source="CBIC",
            date=f"{year}",
            summary="Latest updates on GST 2.0 reforms and rate structure changes.",
            query="Tell me about GST 2.0 reforms and latest amendments"
        ),
        NewsItem(
            title="Finance Act Updates",
            source="Ministry of Finance",
            date=f"{year}",
            summary="Recent amendments introduced through Finance Act affecting tax laws.",
            query="What are the latest Finance Act amendments?"
        ),
        NewsItem(
            title="Legal Reforms News",
            source="Legal Updates",
            date=f"{year}",
            summary="Recent legal reforms and regulatory changes affecting businesses.",
            query="What are the latest legal reforms in India?"
        ),
    ]


@router.get("/cache-stats")
async def get_cache_stats():
    """
    Get search cache statistics and performance metrics
    Helps monitor API usage and cache effectiveness
    """
    try:
        stats = search_cache.get_stats()

        # Add recommendations based on performance
        recommendations = []

        if stats['hit_rate_percent'] < 50:
            recommendations.append(
                "Cache hit rate is low. Consider increasing cache duration or pre-warming cache with common queries."
            )

        if stats['cache_size'] > stats['max_cache_size'] * 0.9:
            recommendations.append(
                "Cache is nearly full. Consider increasing max_cache_size or clearing old entries."
            )

        if stats['api_calls_saved'] > 80:
            recommendations.append(
                f"Great! You've saved approximately ${stats['estimated_cost_saved']:.2f} in API costs. "
                "Cache is working effectively."
            )

        return {
            "status": "success",
            "cache_stats": stats,
            "recommendations": recommendations,
            "quota_info": {
                "google_free_tier_daily_limit": 100,
                "estimated_queries_today": stats['misses'],
                "quota_remaining_approx": max(0, 100 - stats['misses']),
                "quota_status": "OK" if stats['misses'] < 80 else "WARNING" if stats['misses'] < 100 else "EXCEEDED"
            }
        }
    except Exception as e:
        logger.error(f"Error getting cache stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/cache-clear")
async def clear_cache():
    """
    Clear the search cache
    Use this to force fresh results from Google API
    """
    try:
        search_cache.clear()
        return {
            "status": "success",
            "message": "Search cache cleared successfully"
        }
    except Exception as e:
        logger.error(f"Error clearing cache: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/cache-cleanup")
async def cleanup_expired_cache():
    """
    Remove expired cache entries
    Helps free up memory
    """
    try:
        removed_count = search_cache.cleanup_expired()
        return {
            "status": "success",
            "message": f"Removed {removed_count} expired cache entries",
            "removed_count": removed_count
        }
    except Exception as e:
        logger.error(f"Error cleaning up cache: {e}")
        raise HTTPException(status_code=500, detail=str(e))

