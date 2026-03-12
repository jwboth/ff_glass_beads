"""Extract datetime from JPG images and save to CSV.

This script processes a folder of JPG images and extracts datetime information
using either EXIF metadata or file system creation time, then saves the results
to a CSV file.

Usage:
    python setup_imaging_protocol.py --folder <path> [--output <file>] [--format <pattern>] [--pad <int>] [--mode <exif|ctime>]

Example:
    python setup_imaging_protocol.py --folder "E:\\fluidflower_glass_beads\\images" \\
        --output image_dates.csv --format "*.JPG" --pad 5 --mode exif

The output CSV file contains three columns:
    - path: Filename of the image
    - image_id: Extracted ID from the filename stem (last N characters)
    - datetime: Extracted datetime value

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


def get_creation_time(filepath: Path) -> datetime:
    """Get file creation time in a cross-platform manner.

    Uses st_birthtime if available (macOS), otherwise falls back to
    st_ctime (creation time on Windows, metadata change time on Linux).

    Args:
        filepath: Path to the file.

    Returns:
        datetime: File creation time.

    """
    stat = filepath.stat()
    try:
        # macOS and some Linux filesystems
        timestamp = stat.st_mtime
    except AttributeError:
        # Windows: st_ctime is creation time
        # Linux: st_ctime is metadata change time (best available fallback)
        timestamp = stat.st_mtime
    return datetime.fromtimestamp(timestamp)


def build_parser() -> argparse.ArgumentParser:
    """Build and return argument parser.

    Returns:
        ArgumentParser configured with arguments for datetime extraction.

    Arguments:
        --folder (str, required): Path to folder containing JPG images.
        --output (str, optional): Output CSV file path (default: image_dates.csv).
        --format (str, optional): File format glob pattern (default: *.JPG).
        --pad (int, optional): Number of characters to extract from filename stem
                               for image ID (default: 5).
        --mode (str, optional): Datetime extraction mode: 'exif' or 'ctime'
                                (default: exif).

    """
    parser = argparse.ArgumentParser(
        description="Extract datetime from JPG images and save to CSV."
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
    parser.add_argument(
        "--mode",
        type=str,
        choices=["exif", "ctime"],
        default="exif",
        help="Datetime extraction mode: 'exif' (EXIF metadata) or 'ctime' "
        "(file creation time). Default: exif.",
    )
    return parser


def _extract_exif_datetime(filename: Path) -> datetime | None:
    """Extract EXIF datetime from a single image file.

    Args:
        filename: Path to the image file.

    Returns:
        datetime or None if no EXIF datetime found.

    """
    with Image.open(filename) as img:
        exif_data = img._getexif()
        if exif_data:
            for tag_id, value in exif_data.items():
                tag = TAGS.get(tag_id, tag_id)
                if tag in ["DateTimeOriginal", "DateTime"]:
                    return datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
            logger.warning(f"{filename.name}: No EXIF datetime found.")
        else:
            logger.warning(f"{filename.name}: No EXIF data found.")
    return None


def extract_datetimes(
    folder: str,
    output_csv: str,
    format: str = "*.JPG",
    pad: int = 5,
    mode: str = "exif",
) -> None:
    """Extract datetime from images and save to CSV.

    Args:
        folder: Path to folder containing images.
        output_csv: Output CSV file path.
        format: File format glob pattern (default: *.JPG).
        pad: Number of characters to pad from filename stem (default: 5).
        mode: Extraction mode - 'exif' for EXIF metadata, 'ctime' for file
              creation time (default: exif).

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

        if mode == "exif":
            date_time = _extract_exif_datetime(filename)
        elif mode == "ctime":
            date_time = get_creation_time(filename)
        else:
            raise ValueError(f"Unknown mode: {mode}. Use 'exif' or 'ctime'.")

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
    extract_datetimes(
        folder=args.folder,
        output_csv=args.output,
        format=args.format,
        pad=args.pad,
        mode=args.mode,
    )
