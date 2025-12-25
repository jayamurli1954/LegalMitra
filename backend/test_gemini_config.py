"""
Quick test script to verify Gemini configuration
Run this to check if Gemini is configured correctly and what model will be used
"""

import asyncio
import os
from pathlib import Path

# Add backend to path
import sys
sys.path.insert(0, str(Path(__file__).parent))

from app.core.config import get_settings
from app.services.ai_service import ai_service

async def test_config():
    """Test Gemini configuration"""
    settings = get_settings()
    
    print("=" * 60)
    print("LegalMitra - Gemini Configuration Test")
    print("=" * 60)
    print()
    
    print("📋 Configuration Check:")
    print(f"  AI Provider: {settings.AI_PROVIDER}")
    print(f"  Gemini API Key: {'✅ Set' if settings.GOOGLE_GEMINI_API_KEY else '❌ Not Set'}")
    if settings.GOOGLE_GEMINI_API_KEY:
        # Show only first and last 4 characters for security
        key = settings.GOOGLE_GEMINI_API_KEY
        masked_key = f"{key[:4]}...{key[-4:]}" if len(key) > 8 else "***"
        print(f"  API Key (masked): {masked_key}")
    print()
    
    # Check if provider is Gemini
    if settings.AI_PROVIDER.lower() not in ["gemini", "google"]:
        print("⚠️  WARNING: AI_PROVIDER is not set to 'gemini' or 'google'")
        print(f"   Current value: '{settings.AI_PROVIDER}'")
        print(f"   Update your .env file: AI_PROVIDER=gemini")
        print()
    
    # Check if Gemini client is initialized
    if settings.AI_PROVIDER.lower() in ["gemini", "google"]:
        if ai_service._gemini_client:
            print("✅ Gemini client is initialized")
            print()
            
            # Test a simple query
            print("🧪 Testing Gemini API with simple query...")
            try:
                test_query = "What is 2+2? Answer in one word."
                print(f"  Query: '{test_query}'")
                print("  Sending request...")
                
                result = await ai_service.process_legal_query(
                    query=test_query,
                    query_type="research"
                )
                
                print("  ✅ SUCCESS!")
                print(f"  Response: {result[:100]}...")
                print()
                print("✅ Configuration is working correctly!")
                print(f"✅ Using model: gemini-pro (60 requests/minute on free tier)")
                
            except Exception as e:
                error_msg = str(e)
                print(f"  ❌ ERROR: {error_msg[:200]}")
                print()
                
                if "429" in error_msg or "quota" in error_msg.lower():
                    print("⚠️  Rate limit error detected:")
                    print("   - Free tier limits: gemini-pro = 60 requests/minute")
                    print("   - Wait 60 seconds and try again")
                elif "401" in error_msg or "403" in error_msg or "Invalid API key" in error_msg:
                    print("⚠️  API Key error:")
                    print("   - Check your GOOGLE_GEMINI_API_KEY in .env file")
                    print("   - Verify the key is valid in Google AI Studio")
                else:
                    print("⚠️  Unknown error - check error message above")
        else:
            print("❌ Gemini client is NOT initialized")
            print("   Check that:")
            print("   1. google-generativeai package is installed")
            print("   2. GOOGLE_GEMINI_API_KEY is set in .env")
    else:
        print("ℹ️  Skipping Gemini test (provider is not Gemini)")
    
    print()
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_config())



