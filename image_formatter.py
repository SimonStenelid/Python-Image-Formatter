#!/usr/bin/env python3
"""
Minimal Python script for batch formatting images onto a square canvas.
Preserves original image quality without resampling, centers images on canvas.
"""

import argparse
import os
import sys
from pathlib import Path
from PIL import Image, ImageOps
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.tiff', '.tif', '.bmp', '.webp'}

def apply_exif_orientation(image):
    """Apply EXIF orientation to image if present."""
    try:
        return ImageOps.exif_transpose(image)
    except Exception as e:
        logger.warning(f"Could not apply EXIF orientation: {e}")
        return image

def center_image_on_canvas(image, canvas_size, bg_color):
    """Center image on a new canvas without resizing."""
    if image.width > canvas_size or image.height > canvas_size:
        logger.warning(f"Image {image.width}x{image.height} exceeds canvas size {canvas_size}x{canvas_size} - skipping")
        return None

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

def process_image(input_path, output_path, canvas_size, bg_color):
    """Process a single image file."""
    try:
        with Image.open(input_path) as img:
            # Apply EXIF orientation
            img = apply_exif_orientation(img)

            # Center on canvas
            result = center_image_on_canvas(img, canvas_size, bg_color)
            if result is None:
                return False

            # Preserve metadata
            exif = img.info.get('exif')
            icc_profile = img.info.get('icc_profile')

            # Determine output format and save
            output_ext = output_path.suffix.lower()
            if output_ext == '.webp':
                save_kwargs = {'format': 'WEBP', 'lossless': True}
            else:
                save_kwargs = {'format': 'PNG'}

            if exif:
                save_kwargs['exif'] = exif
            if icc_profile:
                save_kwargs['icc_profile'] = icc_profile

            result.save(output_path, **save_kwargs)
            logger.info(f"Processed: {input_path} -> {output_path}")
            return True

    except Exception as e:
        logger.error(f"Error processing {input_path}: {e}")
        return False

def parse_color(color_str):
    """Parse color string to RGB tuple."""
    if color_str is None:
        return None

    color_str = color_str.strip()
    if color_str.startswith('#'):
        color_str = color_str[1:]

    if len(color_str) == 6:
        return tuple(int(color_str[i:i+2], 16) for i in (0, 2, 4))
    elif len(color_str) == 3:
        return tuple(int(color_str[i], 16) * 17 for i in range(3))
    else:
        raise ValueError(f"Invalid color format: {color_str}")

def main():
    parser = argparse.ArgumentParser(description='Batch format images onto square canvas')
    parser.add_argument('--input', required=True, help='Input file or folder')
    parser.add_argument('--output', required=True, help='Output file or folder')
    parser.add_argument('--size', type=int, default=1200, help='Canvas size (default: 1200)')
    parser.add_argument('--bg', help='Background color (e.g., "#ffffff" for white, default: transparent)')

    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    canvas_size = args.size

    try:
        bg_color = parse_color(args.bg)
    except ValueError as e:
        logger.error(e)
        sys.exit(1)

    if not input_path.exists():
        logger.error(f"Input path does not exist: {input_path}")
        sys.exit(1)

    # Handle single file
    if input_path.is_file():
        if input_path.suffix.lower() not in SUPPORTED_FORMATS:
            logger.error(f"Unsupported file format: {input_path.suffix}")
            sys.exit(1)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        if output_path.suffix.lower() not in {'.png', '.webp'}:
            output_path = output_path.with_suffix('.png')

        success = process_image(input_path, output_path, canvas_size, bg_color)
        sys.exit(0 if success else 1)

    # Handle folder
    if not output_path.exists():
        output_path.mkdir(parents=True, exist_ok=True)
    elif not output_path.is_dir():
        logger.error(f"Output path must be a directory when input is a directory")
        sys.exit(1)

    processed = 0
    skipped = 0

    for file_path in input_path.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_FORMATS:
            output_file = output_path / f"{file_path.stem}.png"
            if process_image(file_path, output_file, canvas_size, bg_color):
                processed += 1
            else:
                skipped += 1

    logger.info(f"Processing complete: {processed} processed, {skipped} skipped")

if __name__ == '__main__':
    main()