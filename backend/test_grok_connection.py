#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test Grok connection"""

import sys
import io

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import asyncio
from app.services.ai_service import ai_service
from app.core.config import get_settings

async def test():
    # Clear cache and check settings
    get_settings.cache_clear()
    settings = get_settings()
    print(f"Settings AI_PROVIDER: {settings.AI_PROVIDER}")
    print(f"Grok key exists: {bool(settings.GROK_API_KEY)}")
    
    # Test a simple query
    try:
        result = await ai_service.process_legal_query(
            query="What is 2+2?",
            query_type="research"
        )
        print(f"SUCCESS: Got response (first 100 chars): {result[:100]}")
        return True
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test())
    sys.exit(0 if success else 1)

