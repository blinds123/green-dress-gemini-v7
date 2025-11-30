"""
Collage Splitter Script
Splits grid-based collage images into individual photos
"""

import cv2
import numpy as np
from pathlib import Path
import json

def detect_grid_structure(image):
    """
    Detect grid structure by finding white border lines

    Args:
        image: Input image array

    Returns:
        tuple: (rows, cols, row_positions, col_positions)
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect vertical lines (column separators)
    vertical_projection = np.mean(gray, axis=0)
    # Find white borders (high intensity)
    threshold = np.percentile(vertical_projection, 90)
    vertical_borders = vertical_projection > threshold

    # Find transitions (start of borders)
    col_positions = []
    in_border = False
    for i, is_border in enumerate(vertical_borders):
        if is_border and not in_border:
            col_positions.append(i)
            in_border = True
        elif not is_border and in_border:
            in_border = False

    # Detect horizontal lines (row separators)
    horizontal_projection = np.mean(gray, axis=1)
    threshold = np.percentile(horizontal_projection, 90)
    horizontal_borders = horizontal_projection > threshold

    row_positions = []
    in_border = False
    for i, is_border in enumerate(horizontal_borders):
        if is_border and not in_border:
            row_positions.append(i)
            in_border = True
        elif not is_border and in_border:
            in_border = False

    # Add image boundaries
    col_positions = [0] + col_positions + [image.shape[1]]
    row_positions = [0] + row_positions + [image.shape[0]]

    rows = len(row_positions) - 1
    cols = len(col_positions) - 1

    return rows, cols, row_positions, col_positions

def extract_cells(image, row_positions, col_positions):
    """
    Extract individual cells from grid

    Args:
        image: Input image
        row_positions: List of row boundary positions
        col_positions: List of column boundary positions

    Returns:
        list: List of extracted cell images
    """
    cells = []

    for i in range(len(row_positions) - 1):
        for j in range(len(col_positions) - 1):
            y1 = row_positions[i]
            y2 = row_positions[i + 1]
            x1 = col_positions[j]
            x2 = col_positions[j + 1]

            # Extract cell with some padding removal to exclude borders
            padding = 5
            cell = image[y1+padding:y2-padding, x1+padding:x2-padding]

            # Only add if cell is substantial
            if cell.shape[0] > 50 and cell.shape[1] > 50:
                cells.append(cell)

    return cells

def split_collage(image_path, output_folder, start_index=1):
    """
    Split a collage image into individual photos

    Args:
        image_path: Path to collage image
        output_folder: Folder to save extracted images
        start_index: Starting number for output filenames

    Returns:
        int: Number of images extracted
    """
    # Read image
    image = cv2.imread(str(image_path))
    if image is None:
        print(f"Error: Could not read {image_path}")
        return 0

    # Detect grid structure
    rows, cols, row_positions, col_positions = detect_grid_structure(image)
    print(f"Detected {rows}x{cols} grid in {image_path.name}")

    # Extract cells
    cells = extract_cells(image, row_positions, col_positions)

    # Save each cell
    saved_count = 0
    for idx, cell in enumerate(cells):
        output_name = f"testimonial-{start_index + idx:02d}.jpeg"
        output_path = output_folder / output_name

        # Convert to RGB for JPEG saving
        cell_rgb = cv2.cvtColor(cell, cv2.COLOR_BGR2RGB)
        cell_bgr = cv2.cvtColor(cell_rgb, cv2.COLOR_RGB2BGR)

        # Save with high quality
        cv2.imwrite(str(output_path), cell_bgr, [cv2.IMWRITE_JPEG_QUALITY, 95])
        saved_count += 1
        print(f"  Saved: {output_name}")

    return saved_count

def main():
    """Main execution function"""

    # Setup paths
    images_folder = Path("/Users/nelsonchan/Downloads/secretjeans TEMPLATE SMALL copy 2/images")
    testimonials_folder = images_folder / "testimonials"
    output_folder = images_folder / "testimonials"
    state_folder = Path("/Users/nelsonchan/Downloads/secretjeans TEMPLATE SMALL copy 2/state")

    # Ensure state folder exists
    state_folder.mkdir(exist_ok=True)

    # Find collage images
    collage_extensions = ['.png', '.jpg', '.jpeg', '.webp']
    collage_files = []
    for ext in collage_extensions:
        collage_files.extend(testimonials_folder.glob(f'*{ext}'))

    # Filter to only Gemini generated collages
    collage_files = [f for f in collage_files if 'Gemini_Generated_Image' in f.name]

    print(f"Found {len(collage_files)} collage files to process")

    # Process each collage
    total_extracted = 0
    current_index = 1
    errors = []
    processed_collages = []

    for collage_path in collage_files:
        try:
            print(f"\nProcessing: {collage_path.name}")
            extracted = split_collage(collage_path, output_folder, current_index)
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
