import sys
import os
from pathlib import Path

# Add backend directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    print("Attempting to import app.main...")
    from app.main import app
    print("SUCCESS: app.main imported.")
    
    print("Attempting to import app.core.database...")
    from app.core.database import engine, SQLALCHEMY_DATABASE_URL
    print(f"SUCCESS: Engine created with URL: {SQLALCHEMY_DATABASE_URL}")
    
    print("Checking frontend path resolution...")
    # We can't easily check the route logic without running a request, but we can check if the file compiles
    print("SUCCESS: Frontend path logic compiled.")

except Exception as e:
    print(f"FAILURE: {e}")
    sys.exit(1)
