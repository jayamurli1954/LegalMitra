import sys
import os

# Ensure backend directory is in path
sys.path.append(os.getcwd())

print("Attempting to import app.main...")
try:
    from app.main import app
    print("Success!")
except Exception as e:
    print(f"FAILED: {e}")
    import traceback
    traceback.print_exc()
