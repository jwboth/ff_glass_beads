"""Extract EXIF datetime from JPG images and save to CSV.

This script processes a folder of JPG images, extracts their EXIF metadata
(specifically the datetime information), and saves the results to a CSV file.

Usage:
    python setup_imaging_protocol.py --folder <path> [--output <file>] [--format <pattern>] [--pad <int>]

Example:
    python setup_imaging_protocol.py --folder "E:\\fluidflower_glass_beads\\images" \\
        --output image_dates.csv --format "*.JPG" --pad 5

The output CSV file contains three columns:
    - path: Filename of the image
    - image_id: Extracted ID from the filename stem (last N characters)
    - datetime: EXIF DateTimeOriginal or DateTime value

"""

import argparse
import logging
from pathlib import Path
from datetime import datetime

import pandas as pd
from PIL import Image
from PIL.ExifTags import TAGS

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def build_parser() -> argparse.ArgumentParser:
    """Build and return argument parser.

    Returns:
        ArgumentParser configured with arguments for EXIF extraction.

    Arguments:
        --folder (str, required): Path to folder containing JPG images.
        --output (str, optional): Output CSV file path (default: image_dates.csv).
        --format (str, optional): File format glob pattern (default: *.JPG).
        --pad (int, optional): Number of characters to extract from filename stem
                               for image ID (default: 5).

    """
    parser = argparse.ArgumentParser(
        description="Extract EXIF datetime from JPG images and save to CSV."
    )
    parser.add_argument(
        "--folder",
        type=str,
        required=True,
        help="Path to folder containing JPG images.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="image_dates.csv",
        help="Output CSV file path (default: image_dates.csv).",
    )
    parser.add_argument(
        "--format",
        type=str,
        default="*.JPG",
        help="File format glob pattern (default: *.JPG).",
    )
    parser.add_argument(
        "--pad",
        type=int,
        default=5,
        help="Number of characters to pad from filename stem (default: 5).",
    )
    return parser


def extract_exif_datetimes(
    folder: str,
    output_csv: str,
    format: str = "*.JPG",
    pad: int = 5,
) -> None:
    """Extract EXIF datetime from JPG images and save to CSV.

    Args:
        folder: Path to folder containing JPG images.
        output_csv: Output CSV file path.
        format: File format glob pattern (default: *.JPG).
        pad: Number of characters to pad from filename stem (default: 5).

    """
    files = sorted(Path(folder).glob(format))
    selection = files

    # Initialize lists to store data
    file_paths = []
    file_ids = []
    date_times = []

    # Process each file
    for i, filename in enumerate(selection):
        logging.info(f"Processing file {i} / {len(selection)}")
        file_path = filename.name
        file_id = Path(filename).stem[-pad:]
        with Image.open(filename) as img:
            exif_data = img._getexif()
            if exif_data:
                # Find DateTimeOriginal or DateTime
                date_str = None
                for tag_id, value in exif_data.items():
                    tag = TAGS.get(tag_id, tag_id)
                    if tag in ["DateTimeOriginal", "DateTime"]:
                        date_str = value
                        break
                if date_str:
                    date_time = datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")
                else:
                    date_time = None
                    logger.warning(f"{file_id}: No EXIF datetime found.")
            else:
                date_time = None
                logger.warning(f"{file_id}: No EXIF data found.")
        logger.info(f"{file_id}: {date_time}")
        file_paths.append(file_path)
        file_ids.append(file_id)
        date_times.append(date_time)

    # Create a DataFrame and save to CSV
    df = pd.DataFrame(
        {"path": file_paths, "image_id": file_ids, "datetime": date_times}
    )
    df.to_csv(output_csv, index=False)
    logger.info(f"Saved results to {output_csv}")


if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()
    extract_exif_datetimes(
        folder=args.folder,
        output_csv=args.output,
        format=args.format,
        pad=args.pad,
    )
