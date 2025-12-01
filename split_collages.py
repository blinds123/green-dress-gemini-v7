"""
Collage Splitter Script - Fixed Grid Version
Splits grid-based collage images into individual photos using fixed grid dimensions
"""

import cv2
import numpy as np
from pathlib import Path
import json

def split_collage_fixed_grid(image_path, output_folder, start_index, rows, cols):
    """
    Split a collage using fixed grid dimensions.

    Args:
        image_path: Path to collage image
        output_folder: Folder to save extracted images
        start_index: Starting number for output filenames
        rows: Number of rows in grid
        cols: Number of columns in grid

    Returns:
        int: Number of images extracted
    """
    image = cv2.imread(str(image_path))
    if image is None:
        print(f"Error: Could not read {image_path}")
        return 0

    height, width = image.shape[:2]
    cell_height = height // rows
    cell_width = width // cols

    print(f"  Image: {width}x{height}, Grid: {cols}x{rows}, Cell: {cell_width}x{cell_height}")

    saved_count = 0
    for row in range(rows):
        for col in range(cols):
            # Calculate cell boundaries
            y1 = row * cell_height
            y2 = (row + 1) * cell_height
            x1 = col * cell_width
            x2 = (col + 1) * cell_width

            # Extract cell with small border trim (2px) to remove any grid lines
            border = 2
            cell = image[y1+border:y2-border, x1+border:x2-border]

            # Skip if cell is too small
            if cell.shape[0] < 20 or cell.shape[1] < 20:
                continue

            # Save with sequential numbering
            output_name = f"testimonial-{start_index + saved_count:02d}.jpeg"
            output_path = output_folder / output_name

            cv2.imwrite(str(output_path), cell, [cv2.IMWRITE_JPEG_QUALITY, 95])
            saved_count += 1
            print(f"    Saved: {output_name} ({cell.shape[1]}x{cell.shape[0]})")

    return saved_count

def main():
    """Main execution function"""

    # Get the directory where this script lives (universal - works anywhere)
    SCRIPT_DIR = Path(__file__).parent.resolve()

    # All paths relative to script location
    images_folder = SCRIPT_DIR / "images"
    testimonials_folder = images_folder / "testimonials"
    output_folder = images_folder / "testimonials"
    state_folder = SCRIPT_DIR / "state"

    # Ensure folders exist
    state_folder.mkdir(exist_ok=True)
    output_folder.mkdir(parents=True, exist_ok=True)

    # Find collage images (files starting with 'collage-')
    collage_files = sorted(testimonials_folder.glob('collage-*'))

    print(f"Found {len(collage_files)} collage files to process")

    if len(collage_files) == 0:
        print("No collage files found. Looking for files starting with 'collage-'")
        print(f"Directory contents: {list(testimonials_folder.iterdir())}")
        return {"status": "no_collages_found"}

    # Define grid structure for each collage
    # These will be auto-detected or can be manually specified
    grid_configs = {
        'collage-01': (3, 3),  # 3 rows x 3 cols = 9 images
        'collage-02': (4, 3),  # 4 rows x 3 cols = 12 images
        'collage-03': (4, 3),  # 4 rows x 3 cols = 12 images
    }

    # Default grid if not specified
    default_grid = (3, 3)

    # Process each collage
    total_extracted = 0
    current_index = 1
    errors = []
    processed_collages = []

    for collage_path in collage_files:
        try:
            print(f"\nProcessing: {collage_path.name}")

            # Get grid config for this collage
            collage_key = collage_path.stem  # filename without extension
            rows, cols = grid_configs.get(collage_key, default_grid)

            extracted = split_collage_fixed_grid(
                collage_path, output_folder, current_index, rows, cols
            )
            total_extracted += extracted
            current_index += extracted
            processed_collages.append(str(collage_path))

        except Exception as e:
            error_msg = f"Error processing {collage_path.name}: {str(e)}"
            print(error_msg)
            errors.append(error_msg)

    # Delete original collages after successful extraction
    deleted_count = 0
    if total_extracted > 0 and len(errors) == 0:
        for collage_path in collage_files:
            try:
                collage_path.unlink()
                deleted_count += 1
                print(f"Deleted: {collage_path.name}")
            except Exception as e:
                error_msg = f"Error deleting {collage_path.name}: {str(e)}"
                print(error_msg)
                errors.append(error_msg)

    # Write output state
    state_data = {
        "collages_processed": len(processed_collages),
        "images_extracted": total_extracted,
        "originals_deleted": deleted_count,
        "errors": errors,
        "status": "complete" if len(errors) == 0 else "complete_with_errors"
    }

    state_file = state_folder / "agent-0.5a.json"
    with open(state_file, 'w') as f:
        json.dump(state_data, f, indent=2)

    print(f"\n{'='*60}")
    print(f"SUMMARY:")
    print(f"  Collages processed: {len(processed_collages)}")
    print(f"  Images extracted: {total_extracted}")
    print(f"  Originals deleted: {deleted_count}")
    print(f"  Errors: {len(errors)}")
    print(f"  Status: {state_data['status']}")
    print(f"{'='*60}")

    return state_data

if __name__ == "__main__":
    main()
