
import sys
import os
import asyncio
from dotenv import load_dotenv

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from app.core.config import get_settings
from app.services.web_search_service import WebSearchService

async def check_search():
    print("--- Checking Web Search Configuration ---")
    settings = get_settings()
    print(f"Settings API Key present: {bool(settings.GOOGLE_CUSTOM_SEARCH_API_KEY)}")
    print(f"Settings Engine ID present: {bool(settings.GOOGLE_CUSTOM_SEARCH_ENGINE_ID)}")
    
    service = WebSearchService()
    print(f"Service initialized. Available: {service.is_available()}")
    print(f"Service Key: {service.api_key[:5]}..." if service.api_key else "Service Key: None")
    print(f"Service CX: {service.search_engine_id[:5]}..." if service.search_engine_id else "Service CX: None")
    
    if service.is_available():
        print("\n--- Attempting Real Search ---")
        try:
            results = await service.search_legal_sites("latest supreme court judgment India 2025", max_results=2)
            print(f"Found {len(results)} results.")
            for r in results:
                print(f"- {r.get('title')}: {r.get('url')}")
        except Exception as e:
            print(f"Search failed: {e}")
    else:
        print("\nSkipping search test as service is unavailable.")

if __name__ == "__main__":
    asyncio.run(check_search())
