# CLAUDE.md

## Project Overview

QR Code Replacement Utility — a Python CLI tool that detects and replaces QR codes in poster images. It uses contrast-based image analysis to locate QR code regions in the bottom-right area of an image, then overlays a new QR code.

## Quick Reference

```bash
# Run the tool
python3 replace_qr.py <poster_image> <new_qr_image> <output_image>

# Example
python3 replace_qr.py poster.png new_qr.png output.png
```

## Tech Stack

- **Language:** Python 3.11+
- **Dependencies:** Pillow (PIL) — image processing
- **No build system, no package manager config, no CI/CD**

## Project Structure

```
replace_qr.py    # Single-file application (entire codebase)
```

### Key Functions

| Function | Purpose |
|---|---|
| `find_qr_by_contrast(img)` | Primary detection — block-based contrast analysis (10×10 blocks, threshold > 100) |
| `find_qr_region(img)` | Fallback detection — pixel-by-pixel brightness analysis |
| `replace_qr_code(poster_path, qr_path, output_path)` | Main orchestrator — detect, resize, paste, save |

## Architecture & Detection Logic

1. **Contrast method (preferred):** Divides the bottom-right quadrant (55–100% width, 75–100% height) into 10×10 pixel blocks, identifies blocks with brightness contrast > 100
2. **Brightness method (fallback):** Scans bottom-right (60–100% width, 80–100% height) for pixels with brightness < 80 or > 200
3. Detected region is squared, padded (5px), and centered before replacement
4. Output format: JPG saved at 95% quality; PNG preserves RGBA

## Code Conventions

- **Style:** PEP 8, snake_case for functions and variables
- **Docstrings:** Present on all public functions
- **Image handling:** Convert to RGBA internally, convert back to RGB for JPG output
- **No tests, no linter config** — keep changes simple and manually verified

## Development Guidelines

- This is a single-file utility; avoid splitting into multiple modules unless complexity warrants it
- Preserve the two-method detection fallback pattern (`find_qr_by_contrast` → `find_qr_region`)
- Keep Pillow as the only external dependency
- Use `Image.Resampling.NEAREST` for QR code resizing to preserve sharp edges
- Always handle both PNG (RGBA) and JPG (RGB) output formats
