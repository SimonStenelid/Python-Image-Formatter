# Image Formatter Web App

A simple web application for bulk image formatting to 1200×1200 canvas.

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the web app:**
   ```bash
   python3 app.py
   ```

3. **Open your browser:**
   Navigate to `http://localhost:8080`

## How to Use

1. **Upload Images**:
   - Click the upload area or drag and drop multiple image files
   - Supports: JPG, PNG, TIFF, BMP, WebP
   - Maximum total upload: 100MB

2. **Process Images**:
   - Click "Format Images (1200×1200)" button
   - All images will be centered on a 1200×1200 transparent canvas
   - Original image quality is preserved (no resizing)

3. **Download Results**:
   - Processed images are automatically downloaded as a ZIP file
   - Images larger than 1200×1200 pixels will be skipped

## Features

- **Bulk Upload**: Select multiple files at once
- **Drag & Drop**: Simple file upload interface
- **Quality Preservation**: No image resizing or quality loss
- **Transparent Background**: Images centered on transparent canvas
- **Instant Download**: Get all processed images as ZIP
- **Error Handling**: Skips unsupported or oversized images

## Technical Details

- Built with Flask (Python web framework)
- Uses Pillow for image processing
- Temporary file handling with automatic cleanup
- Responsive web interface
- File size and format validation

## Original Script

The web app is based on the `image_formatter.py` script. You can still use the command-line version:

```bash
# Process single image
python image_formatter.py --input photo.jpg --output formatted.png

# Process entire folder
python image_formatter.py --input photos/ --output formatted_photos/
```