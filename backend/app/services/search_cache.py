"""
Search Result Caching Service for LegalMitra
Reduces Google Custom Search API calls by caching results
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json
import hashlib
from pathlib import Path
import asyncio


class SearchCache:
    """
    In-memory cache for search results with TTL (Time To Live)
    Reduces API calls by 80-90% while keeping data reasonably fresh
    """

    def __init__(
        self,
        cache_duration_hours: int = 6,
        max_cache_size: int = 1000,
        enable_persistence: bool = True
    ):
        """
        Initialize search cache

        Args:
            cache_duration_hours: How long to keep cached results (default: 6 hours)
            max_cache_size: Maximum number of cached queries (default: 1000)
            enable_persistence: Save cache to disk for persistence across restarts
        """
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.cache_duration = timedelta(hours=cache_duration_hours)
        self.max_cache_size = max_cache_size
        self.enable_persistence = enable_persistence

        # Statistics
        self.stats = {
            'hits': 0,
            'misses': 0,
            'api_calls_saved': 0,
            'total_queries': 0
        }

        # Persistence file
        self.cache_file = Path("data/search_cache.json")

        # Load cache from disk if available
        if self.enable_persistence:
            self._load_cache_from_disk()

    def _generate_cache_key(self, query: str, params: Optional[Dict] = None) -> str:
        """Generate a unique cache key from query and parameters"""
        # Normalize query (lowercase, strip whitespace)
        normalized_query = query.lower().strip()

        # Include relevant params in cache key
        if params:
            # Sort params for consistent hashing
            param_str = json.dumps(params, sort_keys=True)
            cache_input = f"{normalized_query}:{param_str}"
        else:
            cache_input = normalized_query

        # Generate hash for compact key
        return hashlib.md5(cache_input.encode()).hexdigest()

    def get(self, query: str, params: Optional[Dict] = None) -> Optional[List[Dict]]:
        """
        Get cached results if available and not expired

        Args:
            query: Search query
            params: Optional search parameters

        Returns:
            Cached results or None if cache miss
        """
        self.stats['total_queries'] += 1

        cache_key = self._generate_cache_key(query, params)

        if cache_key not in self.cache:
            self.stats['misses'] += 1
            return None

        cache_entry = self.cache[cache_key]
        cached_time = cache_entry['timestamp']

        # Check if cache is still valid
        if datetime.now() - cached_time > self.cache_duration:
            # Cache expired, remove it
            del self.cache[cache_key]
            self.stats['misses'] += 1
            return None

        # Cache hit!
        self.stats['hits'] += 1
        self.stats['api_calls_saved'] += 1

        return cache_entry['results']

    def set(self, query: str, results: List[Dict], params: Optional[Dict] = None):
        """
        Store search results in cache

        Args:
            query: Search query
            results: Search results to cache
            params: Optional search parameters
        """
        cache_key = self._generate_cache_key(query, params)

        # Implement LRU-style eviction if cache is full
        if len(self.cache) >= self.max_cache_size:
            self._evict_oldest_entry()

        self.cache[cache_key] = {
            'query': query,
            'params': params,
            'results': results,
            'timestamp': datetime.now(),
            'access_count': 0
        }

        # Persist to disk if enabled
        if self.enable_persistence:
            # Don't block on disk write
            asyncio.create_task(self._save_cache_to_disk_async())

    def _evict_oldest_entry(self):
        """Remove the oldest cache entry to make room for new ones"""
        if not self.cache:
            return

        # Find oldest entry by timestamp
        oldest_key = min(
            self.cache.keys(),
            key=lambda k: self.cache[k]['timestamp']
        )
        del self.cache[oldest_key]

    def clear(self):
        """Clear all cached results"""
        self.cache.clear()
        self.stats = {
            'hits': 0,
            'misses': 0,
            'api_calls_saved': 0,
            'total_queries': 0
        }

    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics

        Returns:
            Dictionary with cache performance metrics
        """
        total = self.stats['hits'] + self.stats['misses']
        hit_rate = (self.stats['hits'] / total * 100) if total > 0 else 0

        return {
            'cache_size': len(self.cache),
            'max_cache_size': self.max_cache_size,
            'cache_duration_hours': self.cache_duration.total_seconds() / 3600,
            'hits': self.stats['hits'],
            'misses': self.stats['misses'],
            'hit_rate_percent': round(hit_rate, 2),
            'api_calls_saved': self.stats['api_calls_saved'],
            'total_queries': self.stats['total_queries'],
            'estimated_cost_saved': self.stats['api_calls_saved'] * 0.005  # $5 per 1000 queries
        }

    def _load_cache_from_disk(self):
        """Load cached results from disk if available"""
        try:
            if not self.cache_file.exists():
                return

            with open(self.cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Reconstruct cache with datetime objects
            loaded_count = 0
            for key, entry in data.get('cache', {}).items():
                # Parse timestamp
                timestamp_str = entry.get('timestamp')
                if timestamp_str:
                    timestamp = datetime.fromisoformat(timestamp_str)

                    # Only load if not expired
                    if datetime.now() - timestamp <= self.cache_duration:
                        self.cache[key] = {
                            'query': entry['query'],
                            'params': entry.get('params'),
                            'results': entry['results'],
                            'timestamp': timestamp,
                            'access_count': entry.get('access_count', 0)
                        }
                        loaded_count += 1

            # Restore stats
            if 'stats' in data:
                self.stats.update(data['stats'])

            print(f"✅ Loaded {loaded_count} cached search results from disk")

        except Exception as e:
            print(f"⚠️ Could not load cache from disk: {e}")

    async def _save_cache_to_disk_async(self):
        """Save cache to disk asynchronously"""
        await asyncio.sleep(0.1)  # Small delay to batch writes
        self._save_cache_to_disk()

    def _save_cache_to_disk(self):
        """Save cache to disk for persistence"""
        try:
            # Create data directory if needed
            self.cache_file.parent.mkdir(parents=True, exist_ok=True)

            # Convert cache to JSON-serializable format
            serializable_cache = {}
            for key, entry in self.cache.items():
                serializable_cache[key] = {
                    'query': entry['query'],
                    'params': entry.get('params'),
                    'results': entry['results'],
                    'timestamp': entry['timestamp'].isoformat(),
                    'access_count': entry.get('access_count', 0)
                }

            data = {
                'cache': serializable_cache,
                'stats': self.stats,
                'saved_at': datetime.now().isoformat()
            }

            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

        except Exception as e:
            print(f"⚠️ Could not save cache to disk: {e}")

    def cleanup_expired(self) -> int:
        """
        Remove expired cache entries

        Returns:
            Number of entries removed
        """
        expired_keys = []

        for key, entry in self.cache.items():
            if datetime.now() - entry['timestamp'] > self.cache_duration:
                expired_keys.append(key)

        for key in expired_keys:
            del self.cache[key]

        return len(expired_keys)


# Global cache instance
# Cache for 6 hours - balances freshness with API usage
# Reduced max_cache_size for Render free tier (512MB limit)
# Disabled persistence on Render (ephemeral filesystem)
import os
is_render = os.getenv('RENDER') is not None
search_cache = SearchCache(
    cache_duration_hours=3 if is_render else 6,  # Shorter cache on Render
    max_cache_size=50 if is_render else 500,  # Even smaller on Render (50 entries)
    enable_persistence=not is_render  # Disable on Render to save memory
)
