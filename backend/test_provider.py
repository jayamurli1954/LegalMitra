#!/usr/bin/env python3
"""Quick test to verify provider matching logic"""
from app.core.config import get_settings

settings = get_settings()
provider = settings.AI_PROVIDER.lower().strip()

if provider == "google":
    provider = "gemini"

print(f"AI_PROVIDER from config: {repr(settings.AI_PROVIDER)}")
print(f"Normalized provider: {repr(provider)}")
print(f"provider == 'gemini': {provider == 'gemini'}")
print(f"provider in ('gemini', 'google'): {provider in ('gemini', 'google')}")

if provider == "gemini":
    print("✅ Would match: elif provider == 'gemini'")
elif provider in ('gemini', 'google'):
    print("✅ Would match: elif provider in ('gemini', 'google')")
else:
    print("❌ Would NOT match any gemini check!")

