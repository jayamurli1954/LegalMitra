# Google Custom Search Engine Setup

## ⚠️ Important: You Need a Custom Search Engine ID

The Google Custom Search API requires TWO things:
1. ✅ **API Key** - You provided: `AIzaSyD1ahL-toBaaHnGSzL8DXHYFDuUKQO98cQ`
2. ❌ **Search Engine ID (CX)** - You need to create this

## How to Get Search Engine ID (CX)

### Step 1: Create Custom Search Engine
1. Go to: https://programmablesearchengine.google.com/controlpanel/create
2. Sign in with your Google account
3. Click "Add" to create a new search engine

### Step 2: Configure Search Engine
1. **Sites to search**: Add these legal websites:
   - `indiancode.nic.in`
   - `egazette.nic.in`
   - `prsindia.org`
   - `pib.gov.in`
   - `legislative.gov.in`
   - `legalaffairs.gov.in`
   - `mpa.gov.in`
   - `ecourts.gov.in`
   - `njdg.ecourts.gov.in`
   - `main.sci.gov.in`

2. **Name**: "LegalMitra Legal Websites Search"
3. **Language**: English
4. Click "Create"

### Step 3: Get Search Engine ID
1. After creation, you'll see your search engine
2. Click on it to open settings
3. Find "Search engine ID" (also called "CX")
4. Copy the ID (looks like: `012345678901234567890:abcdefghijk`)

### Step 4: Add to .env File
Add this line to `backend/.env`:
```
GOOGLE_CUSTOM_SEARCH_ENGINE_ID=your_search_engine_id_here
```

## Alternative: Use "Search the entire web" Option

If you want to search the entire web (not just specific sites):
1. When creating the search engine, select "Search the entire web"
2. This will search all websites, not just legal ones
3. Still need to get the Search Engine ID (CX)

## Current Status

✅ API Key: Added to .env  
❌ Search Engine ID: Need to create and add

## After Setup

Once you add the Search Engine ID to .env:
1. Restart the server
2. LegalMitra will automatically search legal websites for latest information
3. Responses will include citations to official sources

---

**Note**: The free tier of Google Custom Search API allows 100 queries per day. For production use, you may need a paid plan.


