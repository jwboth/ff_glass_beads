"""Setp 1 of calibration. Calibration of color signal."""

import argparse
from pathlib import Path
import logging

from darsia.presets.workflows.calibration.calibration_color_signal import (
    calibration_color_signal,
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
    args = parser.parse_args()

    calibration_color_signal(Rig, Path(args.config), args.show)
