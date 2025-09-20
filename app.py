#!/usr/bin/env python3
"""
Simple Flask web app for bulk image formatting to 1200x1200 canvas.
Upload images, get them processed and download as a ZIP file.
"""

import os
import tempfile
import zipfile
from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename
from pathlib import Path
import shutil
from PIL import Image, ImageOps
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max

SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.tiff', '.tif', '.bmp', '.webp'}

def apply_exif_orientation(image):
    """Apply EXIF orientation to image if present."""
    try:
        return ImageOps.exif_transpose(image)
    except Exception as e:
        logger.warning(f"Could not apply EXIF orientation: {e}")
        return image

def center_image_on_canvas(image, canvas_size=1200, bg_color=None):
    """Center image on a canvas, resizing if larger than canvas size."""
    # Check if image needs to be resized
    if image.width > canvas_size or image.height > canvas_size:
        # Calculate scaling factor to fit within canvas while maintaining aspect ratio
        scale_factor = min(canvas_size / image.width, canvas_size / image.height)
        new_width = int(image.width * scale_factor)
        new_height = int(image.height * scale_factor)

        # Resize image using high-quality resampling
        image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        logger.info(f"Resized image from original size to {new_width}x{new_height} to fit {canvas_size}x{canvas_size} canvas")

    # Create new canvas
    if bg_color is None:
        canvas = Image.new('RGBA', (canvas_size, canvas_size), (0, 0, 0, 0))
    else:
        canvas = Image.new('RGB', (canvas_size, canvas_size), bg_color)

    # Calculate center position
    x = (canvas_size - image.width) // 2
    y = (canvas_size - image.height) // 2

    # Paste image on canvas
    if image.mode == 'RGBA' or 'transparency' in image.info:
        canvas.paste(image, (x, y), image)
    else:
        canvas.paste(image, (x, y))

    return canvas

def process_single_image(input_path, output_path, canvas_size=1200, bg_color=None):
    """Process a single image file."""
    try:
        with Image.open(input_path) as img:
            # Apply EXIF orientation
            img = apply_exif_orientation(img)

            # Center on canvas
            result = center_image_on_canvas(img, canvas_size, bg_color)
            if result is None:
                return False

            # Save as PNG
            result.save(output_path, 'PNG')
            logger.info(f"Processed: {input_path} -> {output_path}")
            return True

    except Exception as e:
        logger.error(f"Error processing {input_path}: {e}")
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_images():
    if 'files' not in request.files:
        flash('No files selected')
        return redirect(url_for('index'))

    files = request.files.getlist('files')
    if not files or all(file.filename == '' for file in files):
        flash('No files selected')
        return redirect(url_for('index'))

    # Check total file size
    total_size = sum(file.seek(0, 2) or file.tell() for file in files if file.filename != '')
    for file in files:
        file.seek(0)  # Reset file pointer

    if total_size > 100 * 1024 * 1024:  # 100MB limit
        flash('Total file size exceeds 100MB limit')
        return redirect(url_for('index'))

    # Create temporary directories
    temp_input_dir = tempfile.mkdtemp()
    temp_output_dir = tempfile.mkdtemp()

    try:
        processed_count = 0
        skipped_count = 0
        total_files = len([f for f in files if f.filename != ''])

        logger.info(f"Starting to process {total_files} files")

        # Save and process uploaded files
        for i, file in enumerate(files):
            if file.filename != '':
                filename = secure_filename(file.filename)
                file_ext = Path(filename).suffix.lower()

                logger.info(f"Processing file {i+1}/{total_files}: {filename}")

                if file_ext in SUPPORTED_FORMATS:
                    # Handle duplicate filenames by adding a counter
                    base_name = Path(filename).stem
                    counter = 1
                    while os.path.exists(os.path.join(temp_input_dir, filename)):
                        filename = f"{base_name}_{counter}{file_ext}"
                        counter += 1

                    input_path = os.path.join(temp_input_dir, filename)
                    output_filename = f"{Path(filename).stem}.png"

                    # Handle duplicate output filenames
                    counter = 1
                    while os.path.exists(os.path.join(temp_output_dir, output_filename)):
                        output_filename = f"{Path(filename).stem}_{counter}.png"
                        counter += 1

                    output_path = os.path.join(temp_output_dir, output_filename)

                    try:
                        file.save(input_path)
                        logger.info(f"Saved file to: {input_path}")

                        if process_single_image(input_path, output_path):
                            processed_count += 1
                            logger.info(f"Successfully processed: {filename}")
                        else:
                            skipped_count += 1
                            logger.warning(f"Failed to process: {filename}")
                    except Exception as e:
                        logger.error(f"Error processing file {filename}: {e}")
                        skipped_count += 1
                else:
                    logger.warning(f"Unsupported format: {filename}")
                    skipped_count += 1

        logger.info(f"Processing summary: {processed_count} processed, {skipped_count} skipped")

        if processed_count == 0:
            flash('No images were processed successfully')
            return redirect(url_for('index'))

        # Create ZIP file with all processed images
        zip_path = tempfile.mktemp(suffix='.zip')
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            output_files = os.listdir(temp_output_dir)
            logger.info(f"Adding {len(output_files)} files to ZIP")

            for filename in output_files:
                file_path = os.path.join(temp_output_dir, filename)
                if os.path.isfile(file_path):
                    zipf.write(file_path, filename)
                    logger.info(f"Added to ZIP: {filename}")

        logger.info(f"Processing complete: {processed_count} processed, {skipped_count} skipped")

        return send_file(
            zip_path,
            as_attachment=True,
            download_name='formatted_images.zip',
            mimetype='application/zip'
        )

    except Exception as e:
        logger.error(f"Error processing images: {e}")
        flash(f'An error occurred while processing images: {str(e)}')
        return redirect(url_for('index'))

    finally:
        # Cleanup temporary directories
        shutil.rmtree(temp_input_dir, ignore_errors=True)
        shutil.rmtree(temp_output_dir, ignore_errors=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)