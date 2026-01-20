import sys
from unittest.mock import MagicMock, patch

# Mock the settings and dependencies
sys.modules['app.core.config'] = MagicMock()
sys.modules['app.services.web_search_service'] = MagicMock()
sys.modules['anthropic'] = MagicMock()
sys.modules['openai'] = MagicMock()
sys.modules['google'] = MagicMock()
sys.modules['google.genai'] = MagicMock()
sys.modules['google.generativeai'] = MagicMock()
sys.modules['httpx'] = MagicMock()
sys.modules['app.services.openrouter_service'] = MagicMock()

# Setup the mock settings
from app.core.config import get_settings
mock_settings = MagicMock()
# THIS IS THE KEY: Simulate the invalid configuration
mock_settings.AI_PROVIDER = "google (or anthropic, openai)"
mock_settings.GOOGLE_GEMINI_API_KEY = "fake_key"
get_settings.return_value = mock_settings

# Import the service (which will use our mocks)
# We need to rely on the module we modified being in the path. 
# Assuming script is run from project root or backend dir
import os
if os.path.exists("backend"):
    sys.path.append("backend")
elif os.path.exists("app"):
    pass # already in backend
else:
    # Try to find backend
    sys.path.append("d:\\SanMitra_Tech\\LegalMitra\\backend")

try:
    from app.services.ai_service import AIService
    
    print("Attempting to initialize AIService with invalid provider string...")
    service = AIService()
    
    # Check if _generate_text (where logic resides) handles it
    # note: the fix I applied was in _generate_text, but wait...
    # The fix logic:
    # provider = self.settings.AI_PROVIDER.lower().strip()
    # if "google (or anthropic, openai)" in provider...
    
    # We need to call _generate_text to trigger the logic, 
    # but _generate_text is async and calls the provider.
    # However, I can inspect the internal properties if I modified __init__?
    # No, I modified _generate_text.
    
    # Let's run _generate_text
    import asyncio
    
    async def test():
        try:
            # We mock the _gemini_client to avoid actual calls
            service._gemini_client = MagicMock()
            service._gemini_use_new_sdk = False # simplified path
            
            # The logic inside _generate_text:
            # It checks provider string, handles it, then calls specific client.
            # If it calls gemini client, success!
            # If it raises RuntimeError, fail.
            
            await service._generate_text("Test query")
            print("SUCCESS: _generate_text executed without RuntimeError!")
        except RuntimeError as e:
            print(f"FAILURE: RuntimeError raised: {e}")
        except Exception as e:
            # If it fails because of mocks (e.g. no generate_content), that's fine, 
            # as long as it's not "Unsupported AI provider"
            if "Unsupported AI provider" in str(e):
                print(f"FAILURE: Unsupported AI provider error: {e}")
            else:
                print(f"SUCCESS (Partial): Parsed provider correctly, failed later on mock: {e}")

    asyncio.run(test())

except Exception as e:
    print(f"CRITICAL FAILURE during init: {e}")
