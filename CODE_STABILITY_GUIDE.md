# Code Stability Guide

## How to Maintain Code Stability and Prevent Bugs

### 1. **Don't Modify Working Code**
- ✅ **DO**: Keep working code unchanged
- ❌ **DON'T**: Make "improvements" to code that's already working
- **Rule**: "If it ain't broke, don't fix it"

### 2. **Use Version Control Properly**
- ✅ Always commit before making changes
- ✅ Use descriptive commit messages
- ✅ Create branches for experiments: `git checkout -b experiment-feature`
- ✅ Test thoroughly before merging to main
- ✅ Use tags for stable releases: `git tag v1.0`

### 3. **Test Before Deploying**
- ✅ Test locally before pushing to GitHub
- ✅ Test all features after changes
- ✅ Check browser console for errors (F12)
- ✅ Verify API endpoints work correctly
- ✅ Test on different browsers if possible

### 4. **Follow Code Freeze Rules**
- ✅ Respect version freezes (v1.0 is FROZEN)
- ✅ Make changes in new versions (v1.1 or v2.0)
- ✅ Document all changes
- ✅ Don't mix bug fixes with new features

### 5. **Code Review Checklist**
Before committing:
- [ ] Does the code compile/run without errors?
- [ ] Are there any console errors/warnings?
- [ ] Do existing features still work?
- [ ] Are API endpoints responding correctly?
- [ ] Is the UI displaying correctly?
- [ ] Have you tested the new changes?

### 6. **Environment Management**
- ✅ Keep `.env` file local (already in .gitignore)
- ✅ Don't commit API keys or secrets
- ✅ Document required environment variables
- ✅ Use consistent Python/Node versions

### 7. **Dependency Management**
- ✅ Use `requirements.txt` with version pins for stability
- ✅ Test after updating dependencies
- ✅ Document dependency changes
- ✅ Avoid unnecessary dependency updates

### 8. **Backup Strategy**
- ✅ Commit frequently to git
- ✅ Push to GitHub regularly
- ✅ Tag stable versions
- ✅ Keep backups of working configurations

### 9. **Error Handling**
- ✅ Always have try-catch blocks
- ✅ Provide fallback mechanisms
- ✅ Log errors properly
- ✅ Show user-friendly error messages

### 10. **Documentation**
- ✅ Document why code exists (not just what it does)
- ✅ Keep README updated
- ✅ Document API changes
- ✅ Note breaking changes

---

## Red Flags (Don't Do These)

❌ **Don't modify code "just because"**  
❌ **Don't skip testing**  
❌ **Don't ignore errors/warnings**  
❌ **Don't commit broken code**  
❌ **Don't mix unrelated changes**  
❌ **Don't remove working code without backup**  
❌ **Don't change multiple things at once**  
❌ **Don't ignore version freeze rules**

---

## Best Practices

1. **One Change at a Time**: Make one change, test it, commit it
2. **Small Commits**: Better to have many small commits than one huge one
3. **Test Locally First**: Always test before pushing
4. **Read Error Messages**: They tell you what's wrong
5. **Check Logs**: Server logs and browser console
6. **Use Git Branches**: For experiments and new features
7. **Document Changes**: Update docs when code changes

---

## When Bugs Appear

1. **Don't Panic**: Bugs happen
2. **Reproduce the Bug**: Can you make it happen again?
3. **Check Recent Changes**: What changed recently?
4. **Check Logs**: Error messages tell you where to look
5. **Revert if Needed**: `git revert` or `git reset` if necessary
6. **Fix Carefully**: Understand the root cause
7. **Test the Fix**: Make sure it actually fixes the issue
8. **Test Everything Else**: Make sure nothing else broke

---

## Maintaining v1.0 (Frozen Version)

For Version 1.0 (FROZEN):
- ❌ No changes allowed
- ✅ Only critical security patches
- ✅ Only critical bug fixes (with approval)
- ✅ All changes go to v1.1 or v2.0

---

**Remember**: Stable code is more valuable than "perfect" code. Don't break what's working!

