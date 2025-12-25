# Fix "Which Program to Open" Issue

If clicking `START_LEGALMITRA.bat` asks which program to open it with, try these solutions:

## Solution 1: Use START_LEGALMITRA.vbs (Easiest)

1. **Double-click `START_LEGALMITRA.vbs`** instead of the .bat file
   - This VBScript ensures the batch file runs properly in cmd.exe
   - No file association issues

## Solution 2: Use START_LEGALMITRA.cmd

1. **Double-click `START_LEGALMITRA.cmd`** instead
   - .cmd files are sometimes better recognized by Windows

## Solution 3: Fix .bat File Association

### Windows 10/11:
1. Right-click on `START_LEGALMITRA.bat`
2. Select "Open with" → "Choose another app"
3. Select "Command Prompt" or "Windows Command Processor"
4. Check "Always use this app to open .bat files"
5. Click OK

### Alternative Method:
1. Press `Win + R` to open Run dialog
2. Type: `cmd`
3. Press Enter to open Command Prompt
4. Navigate to LegalMitra folder:
   ```
   cd D:\LegalMitra
   ```
5. Type:
   ```
   START_LEGALMITRA.bat
   ```
6. Press Enter

## Solution 4: Run from Command Prompt

1. Open Command Prompt (cmd.exe)
2. Navigate to LegalMitra directory:
   ```
   cd D:\LegalMitra
   ```
3. Run:
   ```
   START_LEGALMITRA.bat
   ```
   OR
   ```
   .\START_LEGALMITRA.bat
   ```

## Solution 5: Create Desktop Shortcut

1. Right-click `START_LEGALMITRA.vbs` (or .bat file)
2. Select "Create shortcut"
3. Drag shortcut to Desktop
4. Right-click shortcut → Properties
5. Change "Target" to:
   ```
   "D:\LegalMitra\START_LEGALMITRA.bat"
   ```
   (Adjust path to your LegalMitra location)
6. Change "Start in" to:
   ```
   D:\LegalMitra
   ```
7. Click OK
8. Double-click the shortcut

## Why This Happens

Windows sometimes loses the file association for .bat files, especially if:
- Multiple programs claim to handle .bat files
- File associations were reset
- Security software interfered
- Registry entries are corrupted

## Recommended Solution

**Use `START_LEGALMITRA.vbs`** - It's the most reliable and works on all Windows versions without file association issues.

---

**Note**: All launcher files (.bat, .cmd, .vbs) do the same thing - they just use different methods to ensure they run properly.










