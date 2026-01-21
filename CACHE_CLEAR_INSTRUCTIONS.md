# How to Clear Browser Cache to Fix Old Error Messages

## The Problem
You're seeing an old error message: "Make sure the backend server is running on http://localhost:8888"
This is because your browser has cached the old JavaScript code.

## Quick Fix (Choose One Method)

### Method 1: Hard Refresh (Fastest)
1. **Press `Ctrl + Shift + R`** (Windows/Linux) or **`Cmd + Shift + R`** (Mac)
2. This forces the browser to reload everything without using cache

### Method 2: Clear Cache via DevTools (Recommended)
1. Open **Developer Tools** (Press `F12` or `Ctrl+Shift+I`)
2. **Right-click** on the refresh/reload button in your browser
3. Select **"Empty Cache and Hard Reload"**
4. Wait for the page to reload

### Method 3: Unregister Service Worker (Most Thorough)
1. Open **Developer Tools** (Press `F12`)
2. Go to **"Application"** tab (or "Storage" in Firefox)
3. Click **"Service Workers"** in the left sidebar
4. Find the LegalMitra service worker
5. Click **"Unregister"** button
6. Go to **"Storage"** → Click **"Clear site data"**
7. **Close and reopen** your browser
8. Visit the site again

### Method 4: Clear All Browser Data (Nuclear Option)
1. Press `Ctrl + Shift + Delete` (Windows) or `Cmd + Shift + Delete` (Mac)
2. Select **"Cached images and files"**
3. Time range: **"All time"**
4. Click **"Clear data"**
5. Restart your browser

## Verify It Worked
After clearing cache:
- The error message should **NOT** mention "localhost:8888"
- New error messages will say: "Please check your connection and try again"
- Check browser console (F12) - should show new service worker version

## Still Seeing the Old Message?
If you still see the old message after clearing cache:
1. Try a **different browser** (Chrome, Firefox, Edge)
2. Try **incognito/private mode**
3. Check if you have any browser extensions blocking updates
4. Contact support with a screenshot
