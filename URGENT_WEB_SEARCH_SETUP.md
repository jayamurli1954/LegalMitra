# ⚠️ URGENT: Web Search Not Working - Missing Search Engine ID

## Problem

When you asked about "GST Act 2.0 amendments", LegalMitra responded with 2023 amendments instead of 2025/GST 2.0 information.

**Root Cause:** Web search is not configured because the **Search Engine ID (CX)** is missing.

## Current Status

✅ **API Key**: Configured (`AIzaSyD1ahL-toBaaHnGSzL8DXHYFDuUKQO98cQ`)  
❌ **Search Engine ID (CX)**: **MISSING** - Web search cannot work without this

## What Was Fixed

1. ✅ Enhanced detection for "GST 2.0" queries
2. ✅ Added explicit instructions to AI to focus on GST 2.0 (September 2025)
3. ✅ Added instructions to NOT provide 2023 amendments when user asks about GST 2.0
4. ✅ Improved web search query for GST 2.0 specific searches

**However**, without the Search Engine ID, web search still cannot fetch latest information from official websites.

## Quick Fix: Add Search Engine ID

### Step 1: Create Custom Search Engine
1. Go to: **https://programmablesearchengine.google.com/controlpanel/create**
2. Click **"Add"** button
3. Choose one:
   - **Option A**: Select **"Search the entire web"** (Easiest - searches all websites)
   - **Option B**: Add specific sites (indiancode.nic.in, egazette.nic.in, etc.)
4. **Name**: "LegalMitra Search"
5. Click **"Create"**

### Step 2: Get Search Engine ID
1. After creation, you'll see your search engine listed
2. Click on it to open settings
3. Find **"Search engine ID"** (also called **"CX"**)
4. Copy the ID (looks like: `012345678901234567890:abcdefghijk`)

### Step 3: Add to .env File
Open `backend/.env` and add this line:
```
GOOGLE_CUSTOM_SEARCH_ENGINE_ID=your_search_engine_id_here
```

Replace `your_search_engine_id_here` with the ID you copied.

### Step 4: Restart Server
1. Stop the server (Ctrl+C)
2. Restart using `START_LEGALMITRA_SIMPLE.bat`

## After Setup

Once the Search Engine ID is added:
- ✅ LegalMitra will automatically search legal websites
- ✅ Fetch latest GST 2.0 information from official sources
- ✅ Provide citations to source documents
- ✅ Give accurate, up-to-date responses

## Testing

After restart, test with:
```
"can you highlight on the latest GST Act 2.0 amendments"
```

You should see:
1. Web search results in server logs
2. Response includes latest GST 2.0 information
3. Citations to official sources
4. No more 2023 amendments as primary response

---

**Time Required:** 2-3 minutes to create search engine and add ID

