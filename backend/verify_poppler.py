"""
Poppler Verification Script
Checks if Poppler is installed and accessible for pdf2image
"""

import sys
import subprocess
import os

def check_poppler():
    """Check if Poppler is installed and in PATH"""
    print("=" * 60)
    print("Poppler Installation Verification")
    print("=" * 60)
    print()
    
    # Check if pdftoppm command is available
    print("Checking for pdftoppm command...")
    try:
        result = subprocess.run(
            ['pdftoppm', '-h'],
            capture_output=True,
            text=True,
            timeout=5,
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
        )
        if result.returncode == 0 or 'pdftoppm' in result.stdout or 'pdftoppm' in result.stderr:
            print("[SUCCESS] Poppler is installed and accessible!")
            print(f"   pdftoppm command found and working")
            return True
        else:
            print("[ERROR] pdftoppm command found but not working correctly")
            return False
    except FileNotFoundError:
        print("[ERROR] Poppler is NOT installed or not in PATH")
        print()
        print("Poppler (pdftoppm) command not found.")
        return False
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return False

def check_common_paths():
    """Check common installation paths for Poppler on Windows"""
    print()
    print("Checking common installation paths...")
    common_paths = [
        r"C:\Program Files\poppler\Library\bin",
        r"C:\poppler\Library\bin",
        r"C:\Program Files (x86)\poppler\Library\bin",
        r"C:\tools\poppler\Library\bin",
    ]
    
    found_paths = []
    for path in common_paths:
        if os.path.exists(path):
            pdftoppm_path = os.path.join(path, "pdftoppm.exe")
            if os.path.exists(pdftoppm_path):
                found_paths.append(path)
                print(f"[FOUND] Poppler at: {path}")
    
    if found_paths:
        print()
        print("[WARNING] Poppler is installed but not in your PATH!")
        print()
        print("To fix this:")
        print("1. Open System Properties (Win+R, type: sysdm.cpl)")
        print("2. Click 'Environment Variables'")
        print("3. Under 'System variables', find 'Path' and click 'Edit'")
        print("4. Click 'New' and add one of these paths:")
        for path in found_paths:
            print(f"   {path}")
        print("5. Click OK on all dialogs")
        print("6. Restart your terminal/server")
        return False
    else:
        print("[NOT FOUND] Poppler not found in common installation paths")
        return False

def main():
    """Main verification function"""
    is_installed = check_poppler()
    
    if not is_installed:
        check_common_paths()
        print()
        print("=" * 60)
        print("Installation Instructions")
        print("=" * 60)
        print()
        print("1. Download Poppler from:")
        print("   https://github.com/oschwartz10612/poppler-windows/releases")
        print()
        print("2. Extract the ZIP file to a location like:")
        print("   C:\\Program Files\\poppler")
        print()
        print("3. Add the bin folder to your system PATH:")
        print("   C:\\Program Files\\poppler\\Library\\bin")
        print()
        print("4. Restart your terminal/server after adding to PATH")
        print()
    else:
        print()
        print("=" * 60)
        print("[SUCCESS] All checks passed! Poppler is ready to use.")
        print("=" * 60)
        print()

if __name__ == "__main__":
    main()

