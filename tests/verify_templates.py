import sys
from unittest.mock import MagicMock

# Mock dependencies that might not be available or needed
sys.modules['app.core.config'] = MagicMock()
sys.modules['app.services.web_search_service'] = MagicMock()
sys.modules['anthropic'] = MagicMock()
sys.modules['openai'] = MagicMock()
sys.modules['google'] = MagicMock()
sys.modules['google.genai'] = MagicMock()
sys.modules['httpx'] = MagicMock()
sys.modules['app.services.openrouter_service'] = MagicMock()

# Setup paths
import os
if os.path.exists("backend"):
    sys.path.append("backend")
elif os.path.exists("app"):
    pass 
else:
    sys.path.append("d:\\SanMitra_Tech\\LegalMitra\\backend")

try:
    from app.services.template_service import template_service
    
    print("Attempting to load templates...")
    templates = template_service.list_templates()
    
    print(f"Loaded {len(templates)} templates.")
    
    if len(templates) > 0:
        print("SUCCESS: Templates loaded successfully.")
        # Check a few categories
        categories = set(t['category'] for t in templates)
        print(f"Categories found: {categories}")
    else:
        print("FAILURE: No templates loaded.")
        
except Exception as e:
    print(f"CRITICAL FAILURE during template loading: {e}")
    # Print stack trace
    import traceback
    traceback.print_exc()
