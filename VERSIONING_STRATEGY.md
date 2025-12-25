# Versioning Strategy

## Current Version

**Version 1.0** - FROZEN (December 25, 2025)

---

## Future Versioning

### Version 1.1 (Minor Updates)
For **small improvements** and **minor features**:
- Bug fixes
- Small UI improvements
- Minor feature additions
- Performance optimizations
- Documentation updates

**Branch**: `v1.1` or `release/v1.1`

### Version 2.0 (Major Updates)
For **significant changes** and **major features**:
- Major feature additions
- Significant UI/UX redesigns
- Architecture changes
- Breaking changes
- Major refactoring

**Branch**: `v2.0` or `release/v2.0`

---

## Version 1.0 Status

✅ **FROZEN** - No changes allowed

All future changes must be versioned as:
- **v1.1** (minor updates)
- **v2.0** (major updates)

---

## Git Workflow

### For v1.1 (Minor Updates):
```bash
git checkout -b v1.1
# Make changes
git commit -m "v1.1: Description of changes"
git tag v1.1
```

### For v2.0 (Major Updates):
```bash
git checkout -b v2.0
# Make major changes
git commit -m "v2.0: Description of major changes"
git tag v2.0
```

---

## Decision Guide

**Use v1.1 for**:
- Fixing bugs
- Small improvements
- Minor new features
- Updates that don't change core functionality

**Use v2.0 for**:
- Major new features
- Significant redesigns
- Breaking changes
- Architecture changes
- Major refactoring

---

## Version History

- **v1.0** (December 25, 2025) - Initial stable release - FROZEN
- **v1.1** - Future minor updates (TBD)
- **v2.0** - Future major updates (TBD)

---

**Remember**: Version 1.0 is FROZEN. All changes go to v1.1 or v2.0.

