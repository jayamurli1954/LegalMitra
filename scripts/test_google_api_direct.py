"""
Direct test of Google Custom Search API
"""
import sys
import os
import asyncio
import httpx

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from app.core.config import get_settings

async def test_api_direct():
    """Test Google Custom Search API directly"""
    settings = get_settings()

    api_key = settings.GOOGLE_CUSTOM_SEARCH_API_KEY
    engine_id = settings.GOOGLE_CUSTOM_SEARCH_ENGINE_ID

    print(f"API Key: {api_key[:10]}..." if api_key else "API Key: None")
    print(f"Engine ID: {engine_id[:10]}..." if engine_id else "Engine ID: None")

    if not api_key or not engine_id:
        print("ERROR: API credentials not configured!")
        return

    # Test query
    query = '2026 Supreme Court judgment India'

    print(f"\nSearching for: {query}")

    url = "https://www.googleapis.com/customsearch/v1"

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(
                url,
                params={
                    "key": api_key,
                    "cx": engine_id,
                    "q": query,
                    "num": 3,
                }
            )

            print(f"\nStatus Code: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                print(f"Total Results: {data.get('searchInformation', {}).get('totalResults', 0)}")

                items = data.get("items", [])
                print(f"Items Returned: {len(items)}\n")

                for i, item in enumerate(items, 1):
                    print(f"{i}. {item.get('title')}")
                    print(f"   URL: {item.get('link')}")
                    print(f"   Snippet: {item.get('snippet', '')[:100]}...")
                    print()
            else:
                print(f"Error Response: {response.text[:500]}")

    except Exception as e:
        print(f"Exception: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_api_direct())
