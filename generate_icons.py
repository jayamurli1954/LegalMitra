"""
Generate all PWA icon sizes from Logo_Icon_pwa.png
Requires: Pillow (pip install Pillow)
"""

from PIL import Image
import os

# Input file
source_image = "Logo_Icon_pwa.png"

# Required sizes for PWA
sizes = [72, 96, 128, 144, 152, 192, 384, 512]

# Output directory
output_dir = "frontend/icons"

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

try:
    # Open source image
    print(f"Opening {source_image}...")
    img = Image.open(source_image)

    # Convert to RGBA if not already
    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    print(f"Source image size: {img.size}")
    print(f"Source image mode: {img.mode}")

    # Generate all sizes
    for size in sizes:
        # Create resized image
        resized = img.resize((size, size), Image.Resampling.LANCZOS)

        # Output filename
        output_file = os.path.join(output_dir, f"icon-{size}x{size}.png")

        # Save
        resized.save(output_file, "PNG", optimize=True)

        print(f"[OK] Created: {output_file}")

    print(f"\n[SUCCESS] Generated {len(sizes)} icon sizes in {output_dir}/")
    print("\nGenerated icons:")
    for size in sizes:
        print(f"  - icon-{size}x{size}.png")

    print("\nNext steps:")
    print("1. Icons are ready in frontend/icons/ folder")
    print("2. Open LegalMitra in browser")
    print("3. Look for 'Install App' button")
    print("4. Install and check your home screen!")

except FileNotFoundError:
    print(f"[ERROR] {source_image} not found!")
    print("Make sure the file exists in the current directory.")
except Exception as e:
    print(f"[ERROR] {e}")
    print("\nMake sure Pillow is installed:")
    print("  pip install Pillow")
