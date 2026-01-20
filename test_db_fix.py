
import os
import sys
from sqlalchemy import create_engine

# Mock environment variable for Heroku-style URL
os.environ["DATABASE_URL"] = "postgres://user:pass@localhost:5432/dbname"

# Import the module - this will execute the top-level code we modified
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from backend.app.core import database

print(f"\nFINAL ENGINE URL: {database.engine.url}")

if str(database.engine.url).startswith("postgresql://"):
    print("SUCCESS: URL was converted to postgresql://")
else:
    print("FAILURE: URL remained as postgres://")
