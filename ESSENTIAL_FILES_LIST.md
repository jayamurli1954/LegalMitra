# Essential Files in Repository

## Files That SHOULD Be in GitHub

### Documentation (Essential):
- ✅ `README.md` - Main project readme
- ✅ `VERSION_1_FROZEN.md` - Version documentation
- ✅ `CODE_FREEZE_NOTICE.md` - Freeze notice
- ✅ `VERSIONING_STRATEGY.md` - Versioning guidelines
- ✅ `CODE_STABILITY_GUIDE.md` - Stability guide
- ✅ `README_VERSIONING.md` - Versioning quick reference

### Legal Documents:
- ✅ `Disclaimer.txt`
- ✅ `Privacy_Policy.txt`
- ✅ `Terms_of_Use.txt`

### Configuration:
- ✅ `backend/requirements.txt`
- ✅ `backend/app/prompts/legal_system_prompt.txt`
- ✅ `.gitignore`

### Code:
- ✅ All files in `backend/app/`
- ✅ All files in `frontend/` (except .old files)

### Scripts (Essential):
- ✅ `START_LEGALMITRA_SIMPLE.bat`
- ✅ `START_LEGALMITRA.bat`
- ✅ `STOP_SERVER.bat`

---

## Files That Should NOT Be in GitHub

### Temporary Documentation:
- ❌ Debug/Fix files (FIX_*.md, DEBUG_*.md)
- ❌ Setup guides (*_SETUP.md)
- ❌ Status docs (*_COMPLETE.md, *_WORKING.md)
- ❌ Implementation notes (WEB_*.md, LANDING_*.md)
- ❌ Changelogs (CHANGELOG_*.md)
- ❌ Troubleshooting guides

### Secrets/Keys:
- ❌ API key files (*API-Key*.txt)
- ❌ `.env` files
- ❌ Configuration with secrets

### Temporary Files:
- ❌ `.old` files
- ❌ Test files
- ❌ Query/response dumps
- ❌ Duplicate prompt files

---

**The .gitignore has been updated to automatically exclude these unnecessary files.**

