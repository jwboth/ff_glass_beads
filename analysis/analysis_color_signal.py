"""This module exemmplifies the use of the calibrated color analysis."""

import argparse
from pathlib import Path
import logging

from darsia.presets.workflows.analysis.analysis_color_signal import (
    analysis_color_signal,
)
from darsia.presets.workflows.rig import Rig

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Setup run.")
    parser.add_argument(
        "--config",
        type=str,
        default="config.toml",
        help="Path to config data.",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Show the labels after each step.",
    )
    parser.add_argument(
        "--save-jpg",
        action="store_true",
        help="Save output figures as JPG.",
    )
    parser.add_argument(
        "--save-npz",
        action="store_true",
        help="Save output figures as NPZ.",
    )
    args = parser.parse_args()

    analysis_color_signal(
        Rig,
        Path(args.config),
        args.show,
        args.save_jpg,
        args.save_npz,
    )
