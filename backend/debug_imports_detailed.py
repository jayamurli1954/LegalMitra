import sys
import os

sys.path.append(os.getcwd())

print("Testing imports...")

modules = [
    "app.core.config",
    "app.api.legal_research",
    "app.api.document_drafting",
    "app.api.case_search",
    "app.api.statute_search",
    "app.api.news_and_cases",
    "app.api.document_review"
]

for mod in modules:
    print(f"Importing {mod}...", end=" ")
    try:
        __import__(mod, fromlist=[''])
        print("OK")
    except Exception as e:
        print("FAIL")
        print(e)
        import traceback
        traceback.print_exc()
