# GitHub Repository Cleanup Instructions

## Goal
Remove unnecessary .md and .txt files from GitHub while keeping essential documentation.

---

## Step 1: Review Current Files

Files currently tracked that may be unnecessary:
- Temporary fix/debug documentation
- Setup guides (once setup is done)
- Test/debug files
- Changelog files

---

## Step 2: Files to Keep (Essential)

### Documentation:
- `VERSION_1_FROZEN.md`
- `CODE_FREEZE_NOTICE.md`
- `VERSIONING_STRATEGY.md`
- `CODE_STABILITY_GUIDE.md`
- `README_VERSIONING.md`

### Legal Documents:
- `Disclaimer.txt`
- `Privacy_Policy.txt`
- `Terms_of_Use.txt`

### Configuration:
- `backend/requirements.txt`
- `.gitignore` (updated)

---

## Step 3: Files to Remove from Git (Keep Locally)

These will be ignored by .gitignore but can be removed from git history:

### Temporary Documentation:
```bash
# Debug/Fix files
git rm --cached TEST_*.md DEBUG_*.md FIX_*.md *_FIX*.md
git rm --cached URGENT_*.md QUICK_*.md SWITCH_*.md FINAL_*.md
git rm --cached CHANGELOG_*.md WEB_*.md LANDING_*.md ARTICLE_*.md
git rm --cached GOOGLE_*.md FULL_*.md
git rm --cached *_INSTRUCTIONS.md *_GUIDE.md *_SETUP.md *_COMPLETE.md
```

---

## Step 4: Commit Cleanup

```bash
git add .gitignore
git commit -m "Cleanup: Remove temporary documentation files, update .gitignore"
git push
```

---

## Future: Prevent Adding Unnecessary Files

The updated `.gitignore` will prevent adding:
- Temporary .md files
- Debug .txt files
- Test files

Always review `git status` before committing!

---

**Note**: Files removed from git will still exist locally but won't be tracked/uploaded to GitHub.

