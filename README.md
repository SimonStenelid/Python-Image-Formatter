# Image Formatter

Minimal Python script for batch formatting images onto a square canvas without quality loss.

## Usage Examples

```bash
# Install dependencies
pip install -r requirements.txt

# Process single image with white background
python image_formatter.py --input photo.jpg --output formatted.png --bg "#ffffff"

# Process folder with transparent background (default)
python image_formatter.py --input photos/ --output formatted_photos/

# Process with custom canvas size
python image_formatter.py --input photos/ --output formatted/ --size 800

# Process with different background colors
python image_formatter.py --input photos/ --output formatted/ --bg "#f0f0f0"
```

## Features

- Preserves original image quality (no resampling)
- Applies EXIF orientation automatically
- Centers images on canvas without resizing
- Skips images larger than canvas size
- Supports PNG and lossless WebP output
- Preserves EXIF and ICC metadata
- Transparent background by default

1. Open Terminal/Command Prompt:
    - Mac: Press Cmd + Space, type "Terminal", press Enter
    - Windows: Press Win + R, type "cmd", press Enter
  2. Navigate to the folder:
  cd "/Users/simonstenelid/Desktop/Python Image Formatter"
  3. Run the command:
  python image_formatter.py --input "1 (1).jpg" --output "formatted_by_me.png"

  What each part means:
  - python image_formatter.py = Run the script
  - --input "1 (1).jpg" = Your original image file
  - --output "formatted_by_me.png" = What to name the new file

  Optional extras:
  - Add --bg "#ffffff" for white background instead of transparent
  - Add --size 800 to make canvas smaller than 1200x1200

  The script will create a new PNG file with your image centered on a square canvas!