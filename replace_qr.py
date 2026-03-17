#!/usr/bin/env python3
"""
Replace the QR code in the poster image with a new QR code.
Usage: python3 replace_qr.py <poster_image> <new_qr_image> <output_image>
"""

from PIL import Image, ImageDraw
import sys


def find_qr_region(img):
    """
    Find the QR code region in the poster image.
    The QR code is in the bottom-right corner of the poster.
    We look for a roughly square region with QR-like characteristics.
    """
    width, height = img.size

    # Based on the poster layout, the QR code is in the bottom-right area
    # Scan from bottom-right to find the QR code region
    # The QR code appears to be roughly in the bottom 15% height, right 25% width

    # We'll use pixel analysis to find the QR code boundaries
    # QR codes have high contrast (black and white patterns)

    pixels = img.load()

    # Search region: bottom-right quadrant
    search_left = int(width * 0.6)
    search_top = int(height * 0.8)
    search_right = width
    search_bottom = height

    # Find the actual QR code boundaries by looking for the high-contrast square region
    # Look for clusters of very dark and very light pixels

    # First, let's try to find the QR code by looking for finder patterns
    # (the three squares in corners of QR codes)

    # Simple approach: find bounding box of high-contrast region in bottom-right
    min_x, min_y = search_right, search_bottom
    max_x, max_y = search_left, search_top

    for y in range(search_top, search_bottom):
        for x in range(search_left, search_right):
            r, g, b = pixels[x, y][:3]
            brightness = (r + g + b) / 3
            # QR code pixels are either very dark or very light
            if brightness < 80 or brightness > 200:
                # Check if neighbors also have high contrast (to filter noise)
                if x < min_x:
                    min_x = x
                if y < min_y:
                    min_y = y
                if x > max_x:
                    max_x = x
                if y > max_y:
                    max_y = y

    # Add some padding
    padding = 5
    min_x = max(0, min_x - padding)
    min_y = max(0, min_y - padding)
    max_x = min(width, max_x + padding)
    max_y = min(height, max_y + padding)

    return (min_x, min_y, max_x, max_y)


def find_qr_by_contrast(img):
    """
    Alternative method: find QR code by analyzing contrast patterns in blocks.
    """
    width, height = img.size
    pixels = img.load()
    block_size = 10

    # Focus on bottom-right area
    search_left = int(width * 0.55)
    search_top = int(height * 0.75)

    contrast_map = []

    for by in range(search_top, height - block_size, block_size):
        for bx in range(search_left, width - block_size, block_size):
            min_bright = 255
            max_bright = 0
            for dy in range(block_size):
                for dx in range(block_size):
                    px = pixels[bx + dx, by + dy]
                    brightness = sum(px[:3]) / 3
                    min_bright = min(min_bright, brightness)
                    max_bright = max(max_bright, brightness)
            contrast = max_bright - min_bright
            if contrast > 100:  # High contrast block
                contrast_map.append((bx, by))

    if not contrast_map:
        return None

    # Find bounding box of high-contrast blocks
    min_x = min(p[0] for p in contrast_map)
    min_y = min(p[1] for p in contrast_map)
    max_x = max(p[0] for p in contrast_map) + block_size
    max_y = max(p[1] for p in contrast_map) + block_size

    return (min_x, min_y, max_x, max_y)


def replace_qr_code(poster_path, qr_path, output_path):
    """Replace QR code in poster with new QR code."""
    poster = Image.open(poster_path).convert("RGBA")
    new_qr = Image.open(qr_path).convert("RGBA")

    width, height = poster.size
    print(f"Poster size: {width}x{height}")
    print(f"New QR size: {new_qr.size}")

    # Try to find QR code region
    region = find_qr_by_contrast(poster)
    if region is None:
        region = find_qr_region(poster)

    print(f"Detected QR region: {region}")

    x1, y1, x2, y2 = region
    region_w = x2 - x1
    region_h = y2 - y1

    # Make it square (QR codes are square)
    size = max(region_w, region_h)

    # Center the region
    cx = (x1 + x2) // 2
    cy = (y1 + y2) // 2
    x1 = cx - size // 2
    y1 = cy - size // 2
    x2 = x1 + size
    y2 = y1 + size

    print(f"Adjusted QR region (square): ({x1}, {y1}, {x2}, {y2}), size: {size}x{size}")

    # Resize new QR code to fit the region
    new_qr_resized = new_qr.resize((size, size), Image.Resampling.NEAREST)

    # Paste the new QR code onto the poster
    poster.paste(new_qr_resized, (x1, y1), new_qr_resized if new_qr_resized.mode == 'RGBA' else None)

    # Save as RGB (for JPG output) or RGBA (for PNG)
    if output_path.lower().endswith('.jpg') or output_path.lower().endswith('.jpeg'):
        poster = poster.convert('RGB')

    poster.save(output_path, quality=95)
    print(f"Saved result to: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <poster_image> <new_qr_image> <output_image>")
        sys.exit(1)

    replace_qr_code(sys.argv[1], sys.argv[2], sys.argv[3])
