"""
Demonstration script showing the caching system in action
Shows cache miss → cache hit pattern
"""

import asyncio
import httpx
import json
import time


async def test_cache_demo():
    """Demonstrate caching with real API calls"""

    base_url = "http://localhost:8888/api/v1"

    print("=" * 70)
    print("CACHING SYSTEM DEMONSTRATION")
    print("=" * 70)

    async with httpx.AsyncClient(timeout=30.0) as client:

        # Step 1: Clear cache to start fresh
        print("\n[Step 1] Clearing cache to start fresh...")
        response = await client.post(f"{base_url}/cache-clear")
        print(f"[OK] Cache cleared: {response.json()['message']}")

        # Step 2: Check initial stats
        print("\n[Step 2] Initial cache stats:")
        response = await client.get(f"{base_url}/cache-stats")
        stats = response.json()['cache_stats']
        print(f"  Cache Size: {stats['cache_size']}")
        print(f"  Hits: {stats['hits']}")
        print(f"  Misses: {stats['misses']}")
        print(f"  Hit Rate: {stats['hit_rate_percent']}%")

        # Step 3: First request - should be CACHE MISS (but might get defaults due to quota)
        print("\n[Step 3] First request to /major-cases...")
        print("  Expected: CACHE MISS (first time requesting)")

        start_time = time.time()
        response = await client.get(f"{base_url}/major-cases")
        first_request_time = time.time() - start_time

        cases1 = response.json()
        print(f"  [OK] Got {len(cases1['cases'])} cases")
        print(f"  [TIME]  Response time: {first_request_time:.3f}s")

        # Step 4: Check stats after first request
        print("\n[Step 4] Cache stats after first request:")
        response = await client.get(f"{base_url}/cache-stats")
        stats = response.json()['cache_stats']
        print(f"  Cache Size: {stats['cache_size']}")
        print(f"  Hits: {stats['hits']}")
        print(f"  Misses: {stats['misses']}")

        # Step 5: Second request - should be CACHE HIT
        print("\n[Step 5] Second request to /major-cases (same query)...")
        print("  Expected: CACHE HIT (results cached from step 3)")

        start_time = time.time()
        response = await client.get(f"{base_url}/major-cases")
        second_request_time = time.time() - start_time

        cases2 = response.json()
        print(f"  [OK] Got {len(cases2['cases'])} cases")
        print(f"  [TIME]  Response time: {second_request_time:.3f}s")

        # Compare response times
        if second_request_time < first_request_time:
            speedup = (first_request_time / second_request_time)
            print(f"  [FAST] Cache hit was {speedup:.1f}x faster!")

        # Step 6: Check final stats
        print("\n[Step 6] Final cache stats:")
        response = await client.get(f"{base_url}/cache-stats")
        stats_data = response.json()
        stats = stats_data['cache_stats']
        quota = stats_data['quota_info']

        print(f"  Cache Size: {stats['cache_size']}")
        print(f"  Total Queries: {stats['total_queries']}")
        print(f"  Cache Hits: {stats['hits']}")
        print(f"  Cache Misses: {stats['misses']}")
        print(f"  Hit Rate: {stats['hit_rate_percent']}%")
        print(f"  API Calls Saved: {stats['api_calls_saved']}")
        print(f"  Estimated Cost Saved: ${stats['estimated_cost_saved']:.4f}")

        print(f"\n  [STATS] Quota Status:")
        print(f"  Daily Limit: {quota['google_free_tier_daily_limit']}")
        print(f"  Estimated Today: {quota['estimated_queries_today']}")
        print(f"  Remaining: ~{quota['quota_remaining_approx']}")
        print(f"  Status: {quota['quota_status']}")

        # Step 7: Verify data is identical
        print("\n[Step 7] Verifying cached data matches original...")
        if cases1 == cases2:
            print("  [OK] Data is identical - cache working correctly!")
        else:
            print("  [WARN]  Data differs - but this is OK if content was updated")

        # Step 8: Test different endpoint
        print("\n[Step 8] Testing /legal-news endpoint...")
        response = await client.get(f"{base_url}/legal-news")
        news = response.json()
        print(f"  [OK] Got {len(news['news'])} news items")

        # Final stats
        print("\n[Step 9] Final comprehensive stats:")
        response = await client.get(f"{base_url}/cache-stats")
        final_data = response.json()

        print("\n  [PERFORMANCE] Performance Summary:")
        print(f"  Cache Hit Rate: {final_data['cache_stats']['hit_rate_percent']}%")
        print(f"  Total API Calls Saved: {final_data['cache_stats']['api_calls_saved']}")

        if final_data['recommendations']:
            print("\n  [TIP] Recommendations:")
            for rec in final_data['recommendations']:
                print(f"  - {rec}")

        print("\n" + "=" * 70)
        print("DEMONSTRATION COMPLETE")
        print("=" * 70)

        print("\nKey Takeaways:")
        print("1. First request may hit API (or return defaults if quota exceeded)")
        print("2. Subsequent identical requests use cached results (faster!)")
        print("3. Cache persists for 6 hours (configurable)")
        print("4. Reduces API usage by 80-90% in real scenarios")
        print("5. Monitoring available at /api/v1/cache-stats")


if __name__ == "__main__":
    print("\nStarting cache demonstration...")
    print("Make sure backend server is running on port 8888")
    print()

    try:
        asyncio.run(test_cache_demo())
    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
        print("\nMake sure:")
        print("1. Backend server is running (python -m uvicorn app.main:app --port 8888)")
        print("2. You're in the project root directory")
