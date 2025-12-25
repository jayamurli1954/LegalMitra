#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test Gemini client initialization"""

import sys
import io

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

try:
    # Test 1: Import package
    import google.generativeai as genai
    print("Test 1: Package imported successfully")
    
    # Test 2: Import settings
    from app.core.config import get_settings
    settings = get_settings()
    print(f"Test 2: Settings loaded - AI_PROVIDER={settings.AI_PROVIDER}")
    print(f"Test 2: GOOGLE_GEMINI_API_KEY exists: {bool(settings.GOOGLE_GEMINI_API_KEY)}")
    
    # Test 3: Configure Gemini
    genai.configure(api_key=settings.GOOGLE_GEMINI_API_KEY)
    print("Test 3: Gemini configured successfully")
    
    # Test 4: Initialize AIService
    from app.services.ai_service import ai_service
    print(f"Test 4: AIService initialized")
    print(f"Test 4: _gemini_client is None: {ai_service._gemini_client is None}")
    
    if ai_service._gemini_client is None:
        print("ERROR: Gemini client is None in AIService!")
        sys.exit(1)
    else:
        print("SUCCESS: Gemini client is properly initialized!")
        sys.exit(0)
        
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)


