"""Step 2 of calibration. Calibration of mass analysis."""

import argparse
import logging
from darsia.presets.workflows.calibration.calibration_mass_analysis import (
    calibration_mass_analysis,
)
from darsia.presets.workflows.rig import Rig
from pathlib import Path

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Setup run.")
    parser.add_argument(
        "--config", type=str, default="config.toml", help="Path to config file."
    )
    parser.add_argument(
        "--show", action="store_true", help="Show the labels after each step."
    )
    args = parser.parse_args()

    calibration_mass_analysis(Rig, Path(args.config), args.show)
