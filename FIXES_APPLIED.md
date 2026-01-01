# Fixes Applied for Document Classification and Refresh Issues

## Issues Fixed

### 1. **Document Classification (Case vs News)**
**Problem:** Documents were being marked as both cases AND news, causing duplicates in both sections.

**Solution:**
- Implemented scoring system for document classification
- Documents are now classified as EITHER case OR news, not both
- Case keywords have higher weight (judgment, court, petitioner, etc.)
- News keywords (amendment, notification, circular, etc.)
- Document is assigned to category with higher score (minimum threshold: 3 points)
- Filtering logic excludes documents marked as news from cases list and vice versa

### 2. **Refresh Button Not Working**
**Problem:** Refresh button was reloading the same uploaded documents instead of fetching from web.

**Solution:**
- Added `force_web` query parameter to API endpoints
- When `force_web=true`, API skips uploaded documents and goes directly to web search
- Frontend refresh button now passes `force_web=true` to force web search
- Normal page load still shows uploaded documents first (as intended)

### 3. **Web Search Not Being Used**
**Problem:** Uploaded documents always took priority, so web search never ran even when refresh was clicked.

**Solution:**
- API endpoints now check `force_web` parameter
- If `force_web=true`, skip uploaded documents and go to web search
- If `force_web=false` (default), show uploaded documents first, then fallback to web search

## How It Works Now

### Normal Page Load:
1. Check for uploaded documents (cases/news)
2. If found, display them
3. If not found, try web search
4. If web search fails, show defaults

### Refresh Button Click:
1. Skip uploaded documents (force_web=true)
2. Go directly to web search
3. Fetch latest cases/news from web
4. Display fresh content

## Testing

1. **Upload a document** - It should appear in either Cases OR News (not both)
2. **Click Refresh** - Should fetch from web, not show uploaded documents
3. **Reload page** - Should show uploaded documents again (normal behavior)

## API Changes

### `/api/v1/major-cases`
- New parameter: `force_web` (boolean, default: false)
- Example: `/api/v1/major-cases?force_web=true`

### `/api/v1/legal-news`
- New parameter: `force_web` (boolean, default: false)
- Example: `/api/v1/legal-news?force_web=true`

## Document Classification Scoring

### Case Keywords (with weights):
- "supreme court", "high court": 4 points
- "judgment", "petitioner", "respondent", "citation", "verdict": 3 points
- "court", "case", "judge", "order", "legal notice": 2 points

### News Keywords (with weights):
- "notification", "circular", "amendment", "press release": 3 points
- "news", "update", "reform", "gst", "finance act": 2 points
- "ministry", "government": 1-2 points

### Classification Rules:
- If case_score >= 3 AND case_score >= news_score → Mark as CASE
- If news_score >= 3 AND news_score > case_score → Mark as NEWS
- Otherwise → Not explicitly classified (may appear in both as fallback)

