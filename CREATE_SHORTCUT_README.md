# How to Create Desktop Shortcut for LegalMitra

## One-Click Desktop Shortcut Creation

**Double-click this file**: `create_desktop_shortcut.vbs`

This will automatically:
1. Create a shortcut named "LegalMitra" on your Desktop
2. Link it to the `start_legalmitra.bat` startup script
3. Show a confirmation message

---

## What the Shortcut Does

When you double-click the "LegalMitra" shortcut on your desktop:

1. ✅ Starts Backend API Server (port 8888)
2. ✅ Starts Frontend Web Server (port 3005)
3. ✅ Opens your browser to http://localhost:3005

---

## Manual Shortcut Creation (Alternative)

If the VBS script doesn't work, create manually:

1. **Right-click on Desktop** → New → Shortcut
2. **Location**: Browse to `D:\SanMitra_Tech\LegalMitra\start_legalmitra.bat`
3. **Name**: LegalMitra
4. **Click Finish**

---

## Usage

### Desktop Shortcut
```
Double-click "LegalMitra" icon on Desktop
```

### Or Use Start Menu
Pin the shortcut to Start Menu:
1. Right-click the desktop shortcut
2. Click "Pin to Start"

---

## Icon Customization (Optional)

To change the shortcut icon:

1. Right-click the shortcut → Properties
2. Click "Change Icon"
3. Choose from:
   - `shell32.dll` - Windows system icons
   - `imageres.dll` - More modern icons
   - Custom `.ico` file (if you have one)

---

## Troubleshooting

### Shortcut doesn't work
**Check**:
1. ✅ Path to `start_legalmitra.bat` is correct
2. ✅ You're in the right directory (D:\SanMitra_Tech\LegalMitra)

### VBS script blocked
**Solution**:
- Right-click `create_desktop_shortcut.vbs`
- Click "Run as administrator"

---

## What Gets Created

**Desktop Icon**: LegalMitra
- **Target**: D:\SanMitra_Tech\LegalMitra\start_legalmitra.bat
- **Working Directory**: D:\SanMitra_Tech\LegalMitra
- **Description**: Launch LegalMitra Application

---

## After Creating Shortcut

**To Launch LegalMitra**:
1. Double-click desktop shortcut
2. Two command windows will open:
   - LegalMitra Backend (keep running)
   - LegalMitra Frontend (keep running)
3. Browser opens automatically to http://localhost:3005

**To Stop LegalMitra**:
- Close both command windows
- Or press Ctrl+C in each window

---

## Quick Start Workflow

1. **First Time**: Run `create_desktop_shortcut.vbs`
2. **Every Time**: Double-click "LegalMitra" desktop icon
3. **Done**: App is running!

---

**Date Created**: January 19, 2026
**Purpose**: Easy one-click launch of LegalMitra
