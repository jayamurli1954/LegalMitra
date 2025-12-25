# Repository Cleanup Guide

## Files to Remove from GitHub

The following files are temporary/debug documentation and should NOT be pushed to GitHub:

### Debug/Fix Documentation (Remove):
- `TEST_*.md`
- `DEBUG_*.md`
- `FIX_*.md`
- `*_FIX*.md`
- `*_INSTRUCTIONS.md`
- `*_GUIDE.md` (except CODE_STABILITY_GUIDE.md)
- `*_SETUP.md`
- `*_COMPLETE.md`
- `URGENT_*.md`
- `QUICK_*.md`
- `SWITCH_*.md`
- `FINAL_*.md`
- `CHANGELOG_*.md`
- `WEB_*.md`
- `LANDING_*.md`
- `ARTICLE_*.md`
- `GOOGLE_*.md`
- `FULL_*.md`

### Keep These Essential Documentation:
- ✅ `README.md` (if exists)
- ✅ `VERSION_1_FROZEN.md`
- ✅ `CODE_FREEZE_NOTICE.md`
- ✅ `VERSIONING_STRATEGY.md`
- ✅ `CODE_STABILITY_GUIDE.md`
- ✅ `README_VERSIONING.md`

### Text Files to Remove:
- Temporary processed files
- Test files
- Debug files

### Keep These Text Files:
- ✅ `Disclaimer.txt`
- ✅ `Privacy_Policy.txt`
- ✅ `Terms_of_Use.txt`
- ✅ `backend/requirements.txt`

---

## Cleanup Steps

1. **Add to .gitignore** (already done)
2. **Remove files from git tracking** (but keep locally):
   ```bash
   git rm --cached <filename>
   ```
3. **Commit the cleanup**
4. **Push to GitHub**

---

## How to Maintain Clean Repository

1. **Use .gitignore** - Prevents adding unnecessary files
2. **Review before commit** - Check `git status` before committing
3. **Keep only essential docs** - Don't commit every small fix document
4. **Use branches for experiments** - Keep experimental files in branches
5. **Clean up regularly** - Remove temporary files periodically

---

**Remember**: A clean repository is easier to maintain and understand!

