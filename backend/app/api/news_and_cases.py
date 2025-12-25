"""
API endpoints for major cases and latest legal news
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from app.services.ai_service import ai_service
from app.services.web_search_service import web_search_service
from datetime import datetime

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
async def get_major_cases():
    """
    Get recent major judgments from Supreme Court and High Courts
    Preloaded when the page opens
    Uses Google Custom Search to fetch latest information
    """
    try:
        current_year = datetime.now().year
        
        # Use Google Custom Search to get latest major cases
        if web_search_service.is_available():
            try:
                # Search for recent Supreme Court and High Court judgments
                search_query = f"Supreme Court India recent judgments {current_year} OR High Court India recent judgments {current_year} landmark cases"
                search_results = await web_search_service.search_legal_sites(
                    search_query,
                    max_results=5
                )
                
                # Convert search results to CaseItem format
                cases = []
                for result in search_results:
                    title = result.get("title", "Recent Judgment")
                    snippet = result.get("snippet", "")
                    url = result.get("url", "")
                    
                    # Extract court and year from title/snippet
                    court = "Supreme Court of India"
                    year = current_year
                    if "High Court" in title or "High Court" in snippet:
                        court = "High Court"
                    if "Supreme Court" in title or "Supreme Court" in snippet:
                        court = "Supreme Court of India"
                    
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
                    return CasesResponse(cases=cases[:5])
            except Exception as e:
                print(f"Web search error for cases: {e}")
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
async def get_legal_news():
    """
    Get latest legal news and updates
    Preloaded when the page opens
    Uses Google Custom Search to fetch latest information
    """
    try:
        current_year = datetime.now().year
        
        # Use Google Custom Search to get latest legal news
        if web_search_service.is_available():
            try:
                # Search for latest legal news in India
                search_query = f"latest legal news India {current_year} OR legal updates India {current_year} OR legal reforms India {current_year}"
                search_results = await web_search_service.search_legal_sites(
                    search_query,
                    max_results=5
                )
                
                # Convert search results to NewsItem format
                news_items = []
                for result in search_results:
                    title = result.get("title", "Latest Legal News")
                    snippet = result.get("snippet", "")
                    url = result.get("url", "")
                    
                    # Extract source from URL
                    source = None
                    if "pib.gov.in" in url:
                        source = "PIB"
                    elif "prsindia.org" in url:
                        source = "PRS Legislative Research"
                    elif "legislative.gov.in" in url:
                        source = "Legislative Department"
                    elif "legalaffairs.gov.in" in url:
                        source = "Department of Legal Affairs"
                    elif "egazette.nic.in" in url:
                        source = "eGazette"
                    elif "indiancode.nic.in" in url:
                        source = "India Code"
                    
                    # Create news item
                    news_items.append(NewsItem(
                        title=title[:200],
                        source=source,
                        date=str(current_year),
                        summary=snippet[:300] if snippet else "Latest legal news and updates from India.",
                        query=f"Tell me more about: {title}"
                    ))
                
                if news_items:
                    return NewsResponse(news=news_items[:5])
            except Exception as e:
                print(f"Web search error for news: {e}")
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

