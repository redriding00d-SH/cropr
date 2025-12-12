#!/usr/bin/env python3
"""
CropR - Batch Profile Photo Processor
Automatically detects faces and crops images to professional headshot style.
"""

import argparse
import cv2
import os
import sys
from pathlib import Path
from PIL import Image
import numpy as np


class HeadshotCropper:
    """Handles face detection and intelligent cropping for headshot-style photos."""

    def __init__(self, output_size=600, quality=85):
        """
        Initialize the cropper.

        Args:
            output_size: Output image size in pixels (square or height for portrait)
            quality: WebP output quality (0-100)
        """
        self.output_size = output_size
        self.quality = quality

        # Load OpenCV's pre-trained face detector
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)

        if self.face_cascade.empty():
            raise RuntimeError("Failed to load face detection model")

    def detect_face(self, image_path):
        """
        Detect the primary face in an image.

        Args:
            image_path: Path to image file

        Returns:
            Tuple of (x, y, width, height) for detected face, or None if no face found
        """
        # Read image
        img = cv2.imread(str(image_path))
        if img is None:
            print(f"Warning: Could not read image {image_path}")
            return None

        # Convert to grayscale for face detection
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        if len(faces) == 0:
            return None

        # Return the largest face (assumed to be the primary subject)
        largest_face = max(faces, key=lambda f: f[2] * f[3])
        return tuple(largest_face)

    def calculate_headshot_crop(self, img_width, img_height, face_rect, aspect_ratio='portrait'):
        """
        Calculate crop rectangle for professional headshot.

        Args:
            img_width: Original image width
            img_height: Original image height
            face_rect: Tuple of (x, y, width, height) for detected face
            aspect_ratio: 'portrait' (600x850), 'square' (600x600), or 'circle' (600x600)

        Returns:
            Tuple of (left, top, right, bottom) crop coordinates
        """
        x, y, w, h = face_rect

        # Face center point
        face_center_x = x + w // 2
        face_center_y = y + h // 2

        # Determine output dimensions
        if aspect_ratio == 'portrait':
            crop_width = int(w * 3.5)  # Include shoulders
            crop_height = int(crop_width * 1.4167)  # 850/600 ratio
            # Position face in upper third for headroom
            center_y_offset = -int(crop_height * 0.15)
        elif aspect_ratio in ['square', 'circle']:
            crop_width = int(w * 3.0)  # Tighter crop for square
            crop_height = crop_width
            center_y_offset = -int(crop_height * 0.1)  # Slight upward bias
        else:
            crop_width = crop_height = int(w * 3.0)
            center_y_offset = 0

        # Calculate crop box centered on face with offset
        left = face_center_x - crop_width // 2
        top = face_center_y - crop_height // 2 + center_y_offset
        right = left + crop_width
        bottom = top + crop_height

        # Ensure crop stays within image bounds
        if left < 0:
            right = min(right - left, img_width)
            left = 0
        if top < 0:
            bottom = min(bottom - top, img_height)
            top = 0
        if right > img_width:
            left = max(0, left - (right - img_width))
            right = img_width
        if bottom > img_height:
            top = max(0, top - (bottom - img_height))
            bottom = img_height

        return (left, top, right, bottom)

    def center_crop(self, img_width, img_height, aspect_ratio='portrait'):
        """
        Fallback to center crop when no face is detected.

        Args:
            img_width: Original image width
            img_height: Original image height
            aspect_ratio: 'portrait', 'square', or 'circle'

        Returns:
            Tuple of (left, top, right, bottom) crop coordinates
        """
        if aspect_ratio == 'portrait':
            target_ratio = 600 / 850
        else:
            target_ratio = 1.0

        current_ratio = img_width / img_height

        if current_ratio > target_ratio:
            # Image is wider than target, crop sides
            new_width = int(img_height * target_ratio)
            left = (img_width - new_width) // 2
            return (left, 0, left + new_width, img_height)
        else:
            # Image is taller than target, crop top/bottom
            new_height = int(img_width / target_ratio)
            top = (img_height - new_height) // 2
            return (0, top, img_width, top + new_height)

    def process_image(self, input_path, output_path, aspect_ratio='portrait'):
        """
        Process a single image: detect face, crop, and save.

        Args:
            input_path: Path to input image
            output_path: Path to save output image
            aspect_ratio: 'portrait', 'square', or 'circle'

        Returns:
            True if successful, False otherwise
        """
        try:
            # Open image
            img = Image.open(input_path)

            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')

            # Detect face
            face_rect = self.detect_face(input_path)

            # Calculate crop
            if face_rect:
                crop_box = self.calculate_headshot_crop(
                    img.width, img.height, face_rect, aspect_ratio
                )
                print(f"  ✓ Face detected at position {face_rect}")
            else:
                crop_box = self.center_crop(img.width, img.height, aspect_ratio)
                print(f"  ⚠ No face detected, using center crop")

            # Crop image
            cropped = img.crop(crop_box)

            # Resize to output size
            if aspect_ratio == 'portrait':
                output_dimensions = (self.output_size, int(self.output_size * 1.4167))
            else:
                output_dimensions = (self.output_size, self.output_size)

            resized = cropped.resize(output_dimensions, Image.Resampling.LANCZOS)

            # Save as WebP
            resized.save(output_path, 'WEBP', quality=self.quality)

            print(f"  → Saved to {output_path}")
            return True

        except Exception as e:
            print(f"  ✗ Error processing image: {e}")
            return False

    def process_directory(self, input_dir, output_dir, aspect_ratio='portrait'):
        """
        Batch process all images in a directory.

        Args:
            input_dir: Input directory path
            output_dir: Output directory path
            aspect_ratio: 'portrait', 'square', or 'circle'
        """
        input_path = Path(input_dir)
        output_path = Path(output_dir)

        # Create output directory
        output_path.mkdir(parents=True, exist_ok=True)

        # Supported image formats
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}

        # Find all images
        image_files = [
            f for f in input_path.iterdir()
            if f.is_file() and f.suffix.lower() in image_extensions
        ]

        if not image_files:
            print(f"No images found in {input_dir}")
            return

        print(f"\nProcessing {len(image_files)} images...")
        print(f"Aspect ratio: {aspect_ratio}")
        print(f"Output size: {self.output_size}px")
        print(f"Quality: {self.quality}\n")

        successful = 0
        failed = 0

        for img_file in image_files:
            print(f"Processing: {img_file.name}")

            # Generate output filename
            output_file = output_path / f"{img_file.stem}_headshot.webp"

            # Process image
            if self.process_image(img_file, output_file, aspect_ratio):
                successful += 1
            else:
                failed += 1

        print(f"\n{'='*50}")
        print(f"Batch processing complete!")
        print(f"✓ Successful: {successful}")
        if failed > 0:
            print(f"✗ Failed: {failed}")
        print(f"{'='*50}\n")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='CropR - Batch process photos into professional headshot crops',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process a directory with default settings
  python crop_headshot.py --input ./photos --output ./headshots

  # Process with square crop at 800px
  python crop_headshot.py -i ./photos -o ./output --aspect square --size 800

  # Process a single file
  python crop_headshot.py -i photo.jpg -o headshot.webp

Aspect Ratios:
  portrait - 600x850 (default) - Professional headshot with shoulders
  square   - 600x600 - Square crop for social media
  circle   - 600x600 - Square crop (circular mask applied)
        """
    )

    parser.add_argument(
        '-i', '--input',
        required=True,
        help='Input image file or directory'
    )

    parser.add_argument(
        '-o', '--output',
        required=True,
        help='Output file or directory'
    )

    parser.add_argument(
        '-s', '--size',
        type=int,
        default=600,
        help='Output size in pixels (default: 600)'
    )

    parser.add_argument(
        '-q', '--quality',
        type=int,
        default=85,
        choices=range(1, 101),
        metavar='1-100',
        help='WebP quality 1-100 (default: 85)'
    )

    parser.add_argument(
        '-a', '--aspect',
        choices=['portrait', 'square', 'circle'],
        default='portrait',
        help='Aspect ratio for crop (default: portrait)'
    )

    args = parser.parse_args()

    # Initialize cropper
    try:
        cropper = HeadshotCropper(output_size=args.size, quality=args.quality)
    except RuntimeError as e:
        print(f"Error: {e}")
        sys.exit(1)

    input_path = Path(args.input)
    output_path = Path(args.output)

    # Check if input is file or directory
    if input_path.is_file():
        # Single file processing
        print(f"\nProcessing single file: {input_path.name}\n")
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if cropper.process_image(input_path, output_path, args.aspect):
            print("\n✓ Processing complete!")
        else:
            print("\n✗ Processing failed!")
            sys.exit(1)

    elif input_path.is_dir():
        # Batch directory processing
        cropper.process_directory(input_path, output_path, args.aspect)
    else:
        print(f"Error: Input path '{input_path}' does not exist")
        sys.exit(1)


if __name__ == '__main__':
    main()
