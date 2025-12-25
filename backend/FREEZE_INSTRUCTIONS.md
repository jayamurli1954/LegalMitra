# How to Freeze Dependencies (Prevent Breaking Changes)

## Why Freeze Dependencies?

When you use `>=` (greater than or equal) in requirements.txt, pip can install newer versions that might break your code. **Freezing** locks exact versions so your code works the same way every time.

## Quick Freeze Process

### Step 1: Install Current Requirements
```powershell
cd D:\LegalMitra\backend
pip install -r requirements.txt
```

### Step 2: Freeze Exact Versions
```powershell
pip freeze > requirements-frozen.txt
```

### Step 3: Use Frozen File for Future Installs
```powershell
pip install -r requirements-frozen.txt
```

## Two Requirements Files

1. **requirements.txt** - Flexible (uses `>=`)
   - Good for: Getting latest bug fixes
   - Risk: New versions might break things

2. **requirements-frozen.txt** - Locked (uses `==`)
   - Good for: Stable, reproducible installations
   - Risk: Missing security updates (need manual updates)

## Recommended Approach

**For Production/Stable Use:**
```powershell
pip install -r requirements-frozen.txt
```

**For Development/Testing:**
```powershell
pip install -r requirements.txt
```

## Updating Frozen Requirements

When you want to update packages:

1. Update requirements.txt with new minimum versions
2. Install: `pip install -r requirements.txt --upgrade`
3. Test your application
4. If everything works: `pip freeze > requirements-frozen.txt`
5. Commit the new frozen file

## Current Working Versions

Based on your current setup, these versions are known to work:
- fastapi==0.123.5
- uvicorn==0.38.0
- pydantic==2.12.4
- pydantic-settings==2.12.0
- python-dotenv==1.2.1
- httpx==0.28.1

## Troubleshooting

**If you get "model not found" errors:**
- The AI provider APIs change frequently
- Update the AI package: `pip install --upgrade google-generativeai`
- Check provider documentation for current model names

**If frozen install fails:**
- Some packages may have been removed from PyPI
- Use requirements.txt instead: `pip install -r requirements.txt`



