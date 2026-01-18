# Quick Reference: Caching System

## Quick Commands

### Check Cache Performance
```bash
curl http://localhost:8888/api/v1/cache-stats | python -m json.tool
```

### Clear Cache (Force Fresh Data)
```bash
curl -X POST http://localhost:8888/api/v1/cache-clear
```

### Remove Expired Entries Only
```bash
curl -X POST http://localhost:8888/api/v1/cache-cleanup
```

## Key Metrics

### Good Performance
- **Hit Rate**: > 70%
- **Quota Status**: "OK"
- **API Calls/Day**: < 100

### Warning Signs
- **Hit Rate**: < 50% → Consider increasing cache duration
- **Quota Status**: "WARNING" → Approaching daily limit
- **Cache Size**: > 900 → Consider cleanup

## Configuration

### Adjust Cache Duration
**File**: `backend/app/services/search_cache.py`

```python
# Line 267-271
search_cache = SearchCache(
    cache_duration_hours=6,  # Change this number
    max_cache_size=1000,
    enable_persistence=True
)
```

**Recommendations**:
- **Breaking news**: 2-3 hours
- **Case law**: 12-24 hours
- **Default**: 6 hours (balanced)

### Disable Caching for Specific Query
```python
results = await web_search_service.search_legal_sites(
    query="your query",
    use_cache=False  # Bypass cache
)
```

## Troubleshooting

### Problem: Cache Not Working
```bash
# Check cache stats
curl http://localhost:8888/api/v1/cache-stats

# Look for:
# - hits: 0, misses: 0 → Cache may not be initialized
# - Check backend logs for errors
```

### Problem: Showing Old Data
```bash
# Clear cache to force refresh
curl -X POST http://localhost:8888/api/v1/cache-clear

# Then request fresh data
curl "http://localhost:8888/api/v1/major-cases?force_web=true"
```

### Problem: Quota Exceeded
```bash
# Check quota status
curl http://localhost:8888/api/v1/cache-stats | grep quota_status

# If "EXCEEDED":
# - Wait for daily reset (midnight Pacific)
# - Cache will prevent this in future
# - Default data will be shown meanwhile
```

## File Locations

```
backend/
├── app/
│   ├── services/
│   │   ├── search_cache.py          # Caching logic
│   │   └── web_search_service.py    # Uses cache
│   └── api/
│       └── news_and_cases.py        # Monitoring endpoints
└── data/
    └── search_cache.json            # Persistent cache
```

## Daily Maintenance (Optional)

### Morning Check
```bash
# See overnight performance
curl http://localhost:8888/api/v1/cache-stats
```

### Weekly Cleanup
```bash
# Remove stale entries
curl -X POST http://localhost:8888/api/v1/cache-cleanup
```

### Monthly Review
```bash
# Check if quota usage is stable
curl http://localhost:8888/api/v1/cache-stats | grep estimated_queries_today
# Should be < 50 queries/day with good caching
```

## Cache Stats Explained

```json
{
  "cache_size": 45,              // # of cached queries
  "hits": 120,                   // # of cache hits (no API call)
  "misses": 15,                  // # of cache misses (API called)
  "hit_rate_percent": 88.89,     // Higher is better (target: >70%)
  "api_calls_saved": 120,        // How many API calls avoided
  "quota_remaining_approx": 85   // ~queries left today
}
```

## Common Scenarios

### Scenario 1: Need Fresh Data Now
```bash
# Clear cache and force web search
curl -X POST http://localhost:8888/api/v1/cache-clear
curl "http://localhost:8888/api/v1/major-cases?force_web=true"
```

### Scenario 2: Check If Search Is Working
```bash
# Test the API directly
python scripts/test_google_api_direct.py

# Status 200: Working ✅
# Status 429: Quota exceeded (wait for reset)
# Status 403: Invalid API key
```

### Scenario 3: Monitor Performance
```bash
# Get detailed stats
curl http://localhost:8888/api/v1/cache-stats

# Look for recommendations
```

## Important Notes

1. **Cache resets on server restart** (unless persistence is enabled)
2. **Default cache duration**: 6 hours
3. **Free quota**: 100 queries/day
4. **Quota resets**: Midnight Pacific Time daily
5. **Cache file**: `backend/data/search_cache.json`

## Quick Wins

### Improve Hit Rate
- Increase `cache_duration_hours` (more stale but more hits)
- Pre-warm cache with common queries at startup

### Reduce API Usage
- Use defaults for less critical sections
- Batch similar queries
- Increase cache duration

### Save Costs
- Current setup: FREE (< 100 queries/day)
- Without caching: $52/month (350 queries/day)
- **Savings**: $624/year

---

**For Full Details**: See `CACHING_IMPLEMENTATION.md` and `SIDEBAR_ISSUE_COMPLETE_SOLUTION.md`
